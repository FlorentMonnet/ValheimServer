from utils import (
    backup_folder,
    delete_old_backups,
    get_config,
    print_info,
    print_success,
    unzip_backup
)
from os import path, remove
from kdrive import KdriveApi

config = get_config()

def pull_valheim_world():
    home = path.expanduser("~")
    valheim_path = config.valheim.default_folder

    import_backup_folder = config.backup.import_backup_folder
    purge_days = config.backup.purge_days
    print_info("Purge des backup en cours ...")
    delete_old_backups(
        backup_folder=import_backup_folder,
        days_limit=config.backup.purge_days,
    )
    day_message = "jours" if purge_days > 1 else "jour"
    print_success(
        f"Les backup datant de plus de {purge_days} {day_message} dans le dossier `{import_backup_folder}` ont été supprimés !"
    )

    print_info("Génération du backup d'import en cours ...")
    backup_folder(
        backup_path=valheim_path,
        destination_folder=import_backup_folder,
    )
    print_success(f"Le backup a été généré dans le dossier `{import_backup_folder}`")

    print_info("Telechargement du fichier en cours ...")
    kdrive_api = KdriveApi(config.k_drive.api_key)
    temp_file = path.join(home, "temp.zip")
    kdrive_api.download_file(
        remote_path="/backup_valheim",
        local_path=temp_file,
    )
    print_success("Le fichier présent sur Kdrive a été téléchargé")

    print_info("Import du fichier en cours ...")
    worlds_local_path = config.valheim.worlds_local_folder
    unzip_backup(
        compressed_file_path=temp_file,
        extract_folder=worlds_local_path,
    )
    remove(temp_file)

    print_success("Le fichier a été récupéré depuis le drive et correctement importé !")
    input("Appuyer sur une touche pour quitter le programme ...")