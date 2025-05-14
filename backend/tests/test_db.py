import os
import sys
print(f"--- EXECUTING: {__file__}")
print(f"--- CWD: {os.getcwd()}")
print(f"--- SYS.PATH ---")
for p in sys.path:
    print(f"    {p}")
print(f"--- END SYS.PATH ---")
import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database import engine, SessionLocal, Base
from db.models import User

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL must be set for DB tests")

@pytest.fixture(scope="module")
def db_session():
    """
    Creates all tables, yields a session, and then closes it.
    We’re using the same engine & SessionLocal your app uses.
    """
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

def test_connection(db_session):
    """
    Verify the engine can connect and run a simple query.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except SQLAlchemyError as e:
        pytest.fail(f"Database connection failed: {e}")

def test_create_and_get_user(db_session):
    """
    Insert a User, commit, then fetch by ID and assert fields.
    """
    user = User(email="alice@example.com", name="Alice")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    fetched = db_session.query(User).filter(User.id == user.id).first()
    assert fetched is not None
    assert fetched.id == user.id
    assert fetched.email == "alice@example.com"
    assert fetched.name == "Alice"
