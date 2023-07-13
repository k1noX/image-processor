from routers.api import app
from config.config import FlaskConfig

flask_config = FlaskConfig()

if __name__ == "__main__":
    app.run(host=flask_config.host, port=flask_config.port)
