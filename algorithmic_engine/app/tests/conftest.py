import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
import sys

# Add project root to sys.path to allow 'from app...' imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from main import app # FastAPI app instance, assuming main.py is in project_root
from app.database.connection import Base, get_db # Base for table creation, get_db for overriding
from app.models.scraped_data import ScrapedData
from app.models.deep_model_result import DeepModelResult

# Use a separate SQLite database for testing
TEST_DATABASE_URL = "sqlite:///./test_sql_app.db"

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    # Create tables for the test DB
    Base.metadata.create_all(bind=engine)
    yield engine
    # Clean up the test database file after tests are done
    if os.path.exists("./test_sql_app.db"):
        os.remove("./test_sql_app.db")

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    # Begin a non-ORM transaction
    transaction = connection.begin()
    # Bind an ORM session to the transaction
    SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionTesting()

    yield session

    session.close()
    transaction.rollback() # Rollback to ensure test isolation
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    # Override the get_db dependency for API tests
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close() # Should be handled by db_session fixture's teardown

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    del app.dependency_overrides[get_db] # Clean up override

# Helper to clear tables if needed between tests, though transactions should handle it
def clear_tables(session: Session):
    session.query(DeepModelResult).delete()
    session.query(ScrapedData).delete()
    session.commit()
