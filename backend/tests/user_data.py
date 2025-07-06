"""
Mock data for users.

Three users are setup for testing and development purposes:
"""

import pytest
from sqlalchemy.orm import Session
from ..models.user import User
from ..entities.user import UserEntity
from .reset_table_id_sequence import reset_table_id_seq
from ..utility.shared_enum import UserType



evan = User(
    id=1,
    first_name="Evan",
    last_name="Explorer",
    middle_name="E.",
    email="evanexplorer@gmail.com",
    password='password',
    user_type=UserType.student
)

harry = User(
    id=2,
    first_name="Harry",
    last_name="Helper",
    middle_name="H.",
    email="harryhelper@gmail.com",
    password='password',
    user_type=UserType.guardian
)

armstrong = User(
    id=3,
    first_name="Armstrong",
    last_name="Allen",
    middle_name="A.",
    email="armstrong@gmail.com",
    password="armstrong",
    user_type=UserType.administrator
)

isaac = User(
    id=4,
    first_name="Isaac",
    last_name="Israel",
    middle_name="I.",
    email="isaacs@hotmail.com",
    password="IISAAC@creatin.com",
    user_type=UserType.teacher
)

users = [evan, harry, armstrong, isaac]

def insert_fake_data(session: Session):
    global users
    entities = []
    for user in users:
        print("Entities: ", entities)
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