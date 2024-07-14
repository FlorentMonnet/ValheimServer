from utils import (
    print_error,
    get_config
)
from os import path, remove
from shutil import (
    make_archive,
    unpack_archive,
)
from datetime import datetime
from glob import glob
config = get_config()

def backup_folder(
    backup_path: str,
    destination_folder: str
):
    if not path.isdir(backup_path):
        print_error(f"{backup_path} n'est pas un dossier !")

    date_format = config.backup.date_format
    formated_date = datetime.now().strftime(date_format)
    destination_path = path.join(destination_folder, f"{config.backup.prefix}{formated_date}")
    archive_type = config.backup.archive_type
    try:
        make_archive(destination_path, archive_type, backup_path)
    except Exception as error:
        print_error(error)

    return f"{destination_path}.{archive_type}"

def delete_old_backups(
    backup_folder: str,
    days_limit: int,
):
    prefix = config.backup.prefix
    backup_files = glob(path.join(backup_folder, f"{prefix}"))
    for backup in backup_files:
        timestamp_of_file_modified = path.getmtime(backup)
        modification_date = datetime.fromtimestamp(timestamp_of_file_modified)
        time_delta = datetime.now() - modification_date
        if time_delta.days > days_limit:
            remove(backup)

def unzip_backup(compressed_file_path: str, extract_folder: str):
    if not path.isfile(compressed_file_path):
        print_error(f"Le fichier compréssé `{compressed_file_path}` n'existe pas !")

    archive_type = config.backup.archive_type
    try:
        unpack_archive(
            filename=compressed_file_path,
            extract_dir=extract_folder,
            format=archive_type,
        )
    except Exception as error:
        print_error(error)
