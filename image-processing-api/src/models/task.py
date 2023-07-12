from injectors.db import DbContainer
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
import enum
import datetime

Base = declarative_base()


class TaskStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    FINISHED = "finished"
    ERROR = "error"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, nullable=False)
    result_id = Column(Integer)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    algorithm = Column(String, nullable=False)
    params = Column(MutableDict.as_mutable(JSONB))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime)

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
