from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, Session


@contextmanager
def get_db_session(engine) -> Session:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
