from dataclasses import dataclass, field
from utils import (
    print_debug,
    print_error,
)
from os import path
from json import load

home = path.expanduser("~")

sensitive_keys = [
    "kdrive",
]


def get_safe_config_dict(config_dict: dict, sensitive_keys: list[str]) -> dict:
    for sensitive_key in sensitive_keys:
        config_dict.pop(sensitive_key, None)
    return config_dict

@dataclass
class BackupConfig:
    archive_type: str = "zip"
    date_format: str = "%m%d%Y_%H%M%S"
    default_folder: str = path.join(home, "ValheimBackup")
    export_folder_name: str = "WorldsLocal"
    import_folder_name: str = "Valheim"
    prefix: str = "backup_"
    purge_days: int = 7
    
    def __post_init__(
        self,
    ):
        self.import_backup_folder: str = path.join(
            self.default_folder,
            self.import_folder_name,
        )
        self.export_backup_folder: str = path.join(
            self.default_folder,
            self.export_folder_name,
        )

@dataclass
class ValheimConfig:
    default_folder: str = path.join(home, "AppData", "LocalLow", "IronGate", "Valheim")
    worlds_local_folder_name: str = "worlds_local"
    
    def __post_init__(
        self,
    ):
        self.worlds_local_folder: str = path.join(
            self.default_folder,
            self.worlds_local_folder_name,
        )


@dataclass
class KDriveConfig:
    api_key: str
    id: int

@dataclass
class Config:
    backup: BackupConfig = field(default_factory=BackupConfig)
    k_drive: KDriveConfig = field(default_factory=KDriveConfig)
    valheim: ValheimConfig = field(default_factory=ValheimConfig)
   
    def __post_init__(self):
        if isinstance(self.backup, dict):
            self.backup = BackupConfig(**self.backup)
            
        if isinstance(self.k_drive, dict):
            self.k_drive = KDriveConfig(**self.k_drive)
            
        if isinstance(self.valheim, dict):
            self.valheim = ValheimConfig(**self.valheim)


def get_config() -> Config:
    try:
        with open("../config.json", "r") as config_file:
            config_dict = load(config_file)
    except Exception as error:
        print_error(
            message="Le fichier de configuration n'a pas été trouvé. Veuillez créer un fichier de config (config.json) à la racine du projet",
            exit=False,
        )
        raise error

    try:
        return Config(**config_dict)
    except Exception as error:
        safe_config_dict = get_safe_config_dict(
            config_dict=config_dict,
            sensitive_keys=sensitive_keys,
        )
        print_debug(safe_config_dict)
        print_error(error)
