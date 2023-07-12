from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Engine, create_engine
from Models.File import Base
from Config.Config import DatabaseConfig, AppConfig


db_config = DatabaseConfig()
app_config = AppConfig()
engine = create_engine(
    f"postgresql+psycopg2://{db_config.user}:{db_config.password}" +
        f"@{db_config.host}/{db_config.database}",
    future=True,
)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)