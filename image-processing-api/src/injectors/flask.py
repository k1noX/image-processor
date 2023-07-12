from config.config import FlaskConfig
from flask import Flask
from flask_cors import CORS

from routes.api import image_processing_bp


class FlaskContainer:
    config = FlaskConfig(
        load_type=FlaskConfig.LoadType.FILE,
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
            cls.cors = CORS(image_processing_bp, resources={r"/*": {"origins": "*"}})
            cls.flask_app.register_blueprint(image_processing_bp)
            cls.flask_app.url_map.strict_slashes = False
        return cls.flask_app

    @classmethod
    def run(cls):
        cls.app.run(cls.config.host, cls.config.port, debug=cls.config.debug_mode)
        
app = FlaskContainer.app