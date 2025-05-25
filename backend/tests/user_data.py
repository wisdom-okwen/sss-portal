"""
Mock data for users.

Three users are setup for testing and development purposes:
"""

import pytest
from sqlalchemy.orm import Session
from ..models.user import User
from ..entities.user import UserEntity
from .reset_table_id_sequence import reset_table_id_seq

    # id: int | None = None
    # first_name: str = ''
    # last_name: str = ''
    # middle_name: str = ''
    # email: str = ''
    # password: str = ''


evan = User(
    id=1,
    first_name="Evan",
    last_name="Explorer",
    middle_name="E.",
    email="evanexplorer@gmail.com",
    password='password'
)

harry = User(
    id=2,
    first_name="Harry",
    last_name="Helper",
    middle_name="H.",
    email="harryhelper@gmail.com",
    password='password'
)

users = [evan, harry]

def insert_fake_data(session: Session):
    global users
    entities = []
    for user in users:
        entity = UserEntity.from_model(user)
        session.add(entity)
        entities.append(entity)
    reset_table_id_seq(session, UserEntity, UserEntity.id, len(users) + 1)
    session.commit()  # Commit to ensure User IDs in database

@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield