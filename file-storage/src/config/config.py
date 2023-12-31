import yaml
import os


class BaseConfig:
    def __init__(
        self, config_file="/etc/config.yml", section="postgresql", attr: dict = None
    ):
        with open(config_file, "r") as stream:
            data_loaded = yaml.safe_load(stream)
            if section in data_loaded:
                for k in attr:
                    if k in data_loaded[section]:
                        setattr(self, k, os.environ.get(k, data_loaded[section][k]))
                    else:
                        setattr(self, k, os.environ.get(k, None))
            else:
                for k in attr:
                    setattr(self, k, os.environ.get(k, None))


class DatabaseConfig(BaseConfig):
    def __init__(self, config_file="/etc/config.yml", section="postgresql"):
        self.host = ""
        self.user = ""
        self.password = ""
        self.database = ""
        BaseConfig.__init__(
            self, config_file, section, ["user", "password", "host", "database"]
        )


class FlaskConfig(BaseConfig):
    def __init__(self, config_file="/etc/config.yml", section="flask"):
        self.host = ""
        self.port = ""
        self.secret = ""
        BaseConfig.__init__(self, config_file, section, ["secret", "host", "port"])


class AppConfig(BaseConfig):
    def __init__(self, config_file="/etc/config.yml", section="app"):
        self.path = ""
        self.forbidden_characters = ""
        self.static_redirect_url = ""
        self.local_static_redirect_url = ""
        BaseConfig.__init__(
            self,
            config_file,
            section,
            [
                "path",
                "forbidden_characters",
                "static_redirect_url",
                "local_static_redirect_url",
            ],
        )
