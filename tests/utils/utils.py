import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

Base = declarative_base()

@pytest.fixture(scope="function")
def db_session():
    # Create the SQLite in-memory database
    engine = create_engine('sqlite:///:memory:')
    
    # Bind the sessionmaker to the engine
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create the tables in the in-memory database
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    db: Session = TestingSessionLocal()
    
    try:
        # Provide the session to the test
        yield db
    finally:
        # Tear down the session and drop the tables after the test
        db.close()
        Base.metadata.drop_all(bind=engine)
