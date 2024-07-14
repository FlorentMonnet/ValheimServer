from os import path

from requests import (
    post,
    get,
)
from utils import (
    print_error,
    get_config,
)
from urllib.parse import urljoin


class KdriveApiEndpoint:
    drive_id = get_config().k_drive.id

    def __init__(self, api_version: str, endpoint: str) -> None:
        self.api_version = api_version
        self.endpooint = endpoint

    def get_base_url(self) -> str:
        return urljoin(
            f"https://api.infomaniak.com/{self.api_version}/drive/{self.drive_id}/",
            self.endpooint,
        )


class KdriveApi:
    endpoints = {
        "DOWNLOAD_FILE": KdriveApiEndpoint(
            api_version=2, endpoint="files/<FILE_ID>/download"
        ),
        "SEARCH_FILE": KdriveApiEndpoint(
            api_version=3,
            endpoint="files/search/",
        ),
        "UPLOAD_FILE": KdriveApiEndpoint(
            api_version=2,
            endpoint="upload/",
        )
    }

    def __init__(self, api_key: str) -> None:
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def get_base_url(self, key: str) -> str:
        return KdriveApi.endpoints.get(key).get_base_url()

    def upload_file(self, local_path: str, remote_path: str = "/") -> None:
        if not path.isfile(local_path):
            print_error(f"{local_path} n'est pas un fichier !")
        
        with open(local_path, "rb") as file:
            data = file.read()
            data_size = len(data)

        directory_path = path.dirname(remote_path)
        file_name = path.basename(remote_path)
        payload = {
            "conflict": "version",
            "directory_path": directory_path,
            "file_name": file_name,
            "total_size": data_size,
        }

        uploaded_file_request = post(
            url=self.get_base_url("UPLOAD_FILE"),
            headers=self.headers,
            params=payload,
            data=data,
        )

        uploaded_file_request.raise_for_status()

    def download_file(self, remote_path: str, local_path: str) -> None:
        remote_path_id = self.search_file(remote_path)
        download_file_requests = get(
            url=self.get_base_url("DOWNLOAD_FILE").replace(
                "<FILE_ID>", str(remote_path_id)
            ),
            headers=self.headers,
        )
        download_file_requests.raise_for_status()

        binary_data = download_file_requests.content
        with open(local_path, "wb") as file:
            file.write(binary_data)

    def search_file(self, remote_path: str) -> int:
        payload = {"query": remote_path}

        search_file_request = get(
            url=self.get_base_url("SEARCH_FILE"), headers=self.headers, params=payload
        )
        data = search_file_request.json().get("data")

        if not data:
            print_error(
                f"Aucun fichier présent sur le drive pour le chemin {remote_path} !"
            )

        matched_files = len(data)

        if matched_files > 1:
            print_error(
                f"Plusieurs fichiers ({matched_files}) existent sur le drive pour le chemin {remote_path} !"
            )

        return data[0].get("id")
