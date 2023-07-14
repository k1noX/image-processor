from config.config import AppConfig


class ApiContainer:
    config = AppConfig(
        load_type=AppConfig.LoadType.FILE,
        config_file="config/config.yml",
        section="app",
    )
    app = None

    @classmethod
    def get_file_download_url(cls, file_id: int) -> str:
        return cls.config.base_image_url + str(file_id) + cls.config.download_path

