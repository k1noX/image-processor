import yaml
import os
from enum import Enum


class BaseConfig:
    class LoadType(Enum):
        FILE = 0
        ENV = 1

    def load_from_file(
        self, config_file="config/config.yml", section="postgresql", attr: dict = None
    ):
        with open(config_file, "r") as stream:
            data_loaded = yaml.safe_load(stream)
            if section in data_loaded:
                for k in attr:
                    if k in data_loaded[section]:
                        setattr(self, k, data_loaded[section][k])

    def load_from_env(self, attr: dict = None):
        for k in attr:
            if k in os.environ:
                setattr(self, k, os.environ[k])


class DatabaseConfig(BaseConfig):
    def __init__(
        self,
        load_type: BaseConfig.LoadType,
        config_file="config/config.yml",
        section="postgresql",
    ):
        self.user: str = ""
        self.password: str = ""
        self.host: str = ""
        self.database: str = ""
        self.table: str = ""
        self.port: int = 5432

        if load_type == BaseConfig.LoadType.FILE:
            BaseConfig.load_from_file(
                self,
                config_file,
                section,
                ["user", "password", "host", "database", "table", "port"],
            )
        elif load_type == BaseConfig.LoadType.ENV:
            BaseConfig.load_from_env(self, ["user", "password", "host", "database", "port"])


class FlaskConfig(BaseConfig):
    def __init__(
        self,
        load_type: BaseConfig.LoadType,
        config_file="config/config.yml",
        section="flask",
    ):
        self.secret: str = ""
        self.host: str = ""
        self.port: str = ""
        self.debug_mode: bool = False

        if load_type == BaseConfig.LoadType.FILE:
            BaseConfig.load_from_file(
                self, config_file, section, ["secret", "host", "port", "debug_mode"]
            )
        elif load_type == BaseConfig.LoadType.ENV:
            BaseConfig.load_from_env(self, ["secret", "host", "port", "debug_mode"])


class AppConfig(BaseConfig):
    def __init__(
        self,
        load_type: BaseConfig.LoadType,
        config_file="config/config.yml",
        section="app",
    ):
        self.image_formats: list = []
        self.base_image_url: str = ""
        self.download_path: str = "/local-download"

        if load_type == BaseConfig.LoadType.FILE:
            BaseConfig.load_from_file(
                self,
                config_file,
                section,
                ["image_formats", "base_image_url"],
            )
        elif load_type == BaseConfig.LoadType.ENV:
            BaseConfig.load_from_env(
                self, ["image_formats", "base_image_url"]
            )

class PikaConfig(BaseConfig):
    def __init__(
        self,
        load_type: BaseConfig.LoadType,
        config_file="config/config.yml",
        section="pika",
    ):
        self.rabbitmq_host: str = ""
        self.rabbitmq_username: str = ""
        self.rabbitmq_password: str = ""
        self.rabbitmq_exchange: str = ""
        self.rabbitmq_routing_key: str = ""
        self.rabbitmq_queue: str = ""

        if load_type == BaseConfig.LoadType.FILE:
            BaseConfig.load_from_file(
                self,
                config_file,
                section,
                ["rabbitmq_host", 
                 "rabbitmq_username", 
                 "rabbitmq_password",
                 "rabbitmq_exchange",
                 "rabbitmq_routing_key",
                 "rabbitmq_queue"],
            )
        elif load_type == BaseConfig.LoadType.ENV:
            BaseConfig.load_from_env(
                self, 
                ["rabbitmq_host", 
                 "rabbitmq_username", 
                 "rabbitmq_password",
                 "rabbitmq_exchange",
                 "rabbitmq_routing_key",
                 "rabbitmq_queue"]
            )
