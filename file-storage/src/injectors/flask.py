from config.config import FlaskConfig
from flask import Flask
from flask_cors import CORS

class FlaskContainer:
    config = FlaskConfig(
        config_file="config/config.yml",
        section="flask",
    )
    flask_app = None

    @classmethod
    @property
    def app(cls) -> Flask:
        if cls.flask_app is None:
            cls.flask_app = Flask(__name__)
            cls.flask_app.config["CORS_HEADERS"] = "Content-Type"
            cls.flask_app.secret_key = cls.config.secret
            cls.flask_app.url_map.strict_slashes = False
        return cls.flask_app

    @classmethod
    def run(cls):
        cls.app.run(cls.config.host, cls.config.port, debug=cls.config.debug_mode)
        
app = FlaskContainer.app