from sqlalchemy import Engine, create_engine
from config.config import DatabaseConfig
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, Session


class DbContainer:
    config = DatabaseConfig(
        config_file="config/config.yml",
        section="postgresql",
    )

    db_engine = None

    @classmethod
    @property
    def engine(cls) -> Engine:
        if cls.db_engine is None:
            cls.db_engine = create_engine(
                f"postgresql+psycopg2://{cls.config.user}:{cls.config.password}" +
                    f"@{cls.config.host}/{cls.config.database}",
            future=True,
        )
        print(f"postgresql+psycopg2://{cls.config.user}:{cls.config.password}" +
                    f"@{cls.config.host}/{cls.config.database}")
        return cls.db_engine

    @classmethod
    @contextmanager
    def get_db_session(cls, engine: Engine) -> Session:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        try:
            yield db
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
