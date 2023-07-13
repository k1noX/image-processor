from config.config import AppConfig
from os import path


class AppContainer:
    config = AppConfig(
        config_file="config/config.yml",
        section="app",
    )

    @classmethod
    def get_absolute_path(cls, relative_path: str) -> str:
        return path.join(cls.config.path, relative_path)
