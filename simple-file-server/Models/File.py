import os
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, create_engine
from sqlalchemy.orm import declarative_base
import datetime

from Config.Config import DatabaseConfig, AppConfig
from Models.SessionMaker import get_db_session


db_config = DatabaseConfig()
app_config = AppConfig()
engine = create_engine(
    f"postgresql+psycopg2://{db_config.user}:{db_config.password}" +
        f"@{db_config.host}/{db_config.database}",
    future=True,
)

print(engine.url)

Base = declarative_base()


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    extension = Column("extension", String, nullable=False)
    size = Column("size", BigInteger)
    created_at = Column("created_at", DateTime, default=datetime.datetime.now())
    updated_at = Column("updated_at", DateTime)
    comment = Column("comment", String)

    @property
    def dict(self) -> dict:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "result_id": self.result_id,
            "status": self.status.name,
            "algorithm": self.algorithm,
            "params": self.params,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    class FileError(Exception):
        pass

    def rename(self, name: str):
        if not self.exists:
            raise File.FileError(f"File Not Found: {self.name}!")

        if len(name) == 0:
            raise File.FileError(f"Invalid File Name: {name}!")

        if name == self.name:
            raise File.FileError(f"File is Already Named {self.name}!")

        with get_db_session(engine) as session:
            if (
                session.query(File)
                .filter(File.name == name)
                .filter(File.extension == self.extension)
                .count()
                > 0
            ):
                raise File.FileError(f"Name {name} is Already Taken!")

        self.name = name
        self.updated_at = datetime.datetime.now()

    def set_comment(self, comment: str):
        self.comment = comment
        self.updated_at = datetime.datetime.now()

    @staticmethod
    def create_if_not_exists(
        session, path: str, name: str, extension: str, size: int = None
    ) -> "File":
        file: "File" = None

        file = (
            session.query(File)
            .filter(File.name == name)
            .filter(File.extension == extension)
            .first()
        )
        if not file:
            file = File(
                name=name,
                extension=extension,
                size=size,
                created_at=datetime.datetime.now(),
            )
            session.add(file)

        return file

    @property
    def exists(self) -> bool:
        return os.path.isfile(
            os.path.join(
                app_config.path, str(self.id) + self.extension
            )
        )

    @property
    def relative_path(self) -> str:
        return os.path.join(str(self.id) + self.extension)

    @property
    def full_path(self) -> str:
        return os.path.join(
            app_config.path, str(self.id) + self.extension
        )

    @property
    def dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "extension": self.extension,
            "size": self.size,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "comment": self.comment,
        }
