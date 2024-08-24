import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from api.config.settings import settings

postgresql_settings = settings.postgresql_settings

logger = logging.getLogger(__name__)

# SQLALCHEMY_DATABASE_URL = f"postgresql://{postgresql_settings.user}:{postgresql_settings.password}@{postgresql_settings.hostname}:{str(postgresql_settings.port)}/{postgresql_settings.database_name}"

engine = create_engine(postgresql_settings.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    #TODO: finish docstring
    """_summary:

    Yields:
        _type_: _description_
    """    
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error("Session rollback because of exception: %s", e)
        db.rollback()
        raise
    finally:
        db.close()

