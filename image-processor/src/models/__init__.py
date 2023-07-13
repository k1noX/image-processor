from sqlalchemy_utils import database_exists, create_database
from injectors.db import DbContainer
from models.task import Base

engine = DbContainer.engine
if not database_exists(engine.url):
    print(engine.url)
    create_database(engine.url)

Base.metadata.create_all(engine)