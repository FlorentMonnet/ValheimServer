from utils import (
    backup_folder,
    delete_old_backups,
    get_config,
    print_info,
    print_success
)
from kdrive import KdriveApi

config = get_config()


def push_valheim_world():
    worlds_local_folder = config.valheim.worlds_local_folder

    export_backup_folder = config.backup.export_backup_folder
    purge_days = config.backup.purge_days
    print_info("Purge des backup en cours ...")
    delete_old_backups(
        backup_folder=export_backup_folder,
        days_limit=config.backup.purge_days,
    )
    day_message = "jours" if purge_days > 1 else "jour"
    print_success(
        f"Les backup datant de plus de {purge_days} {day_message} dans le dossier `{export_backup_folder}` ont été supprimés !"
    )

    print_info("Génération du backup d'export en cours ...")
    worlds_local_backup = backup_folder(
        backup_path=worlds_local_folder,
        destination_folder=export_backup_folder,
    )
    print_success(
        f"Le backup d'export a été généré dans le dossier `{export_backup_folder}`"
    )

    print_info("Upload du fichier en cours ...")
    kdrive_api = KdriveApi(config.k_drive.api_key)

    kdrive_api.upload_file(
        local_path=worlds_local_backup, remote_path="/backup_valheim"
    )
    print_success("Le fichier a été upload sur Kdrive !")