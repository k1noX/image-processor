from sqlalchemy_utils import database_exists, create_database
from models.file import Base

from injectors.db import DbContainer

engine = DbContainer.engine
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)