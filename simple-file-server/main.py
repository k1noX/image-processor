from App.Api import app
from Config.Config import FlaskConfig

flask_config = FlaskConfig()

app.run(host=flask_config.host, port=flask_config.port)
