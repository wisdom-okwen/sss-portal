"""
Mock data for users.

Three users are setup for testing and development purposes:
"""

import pytest
from sqlalchemy.orm import Session
from ..models.auth import NewUser
from ..entities.user import UserEntity
# from .reset_table_id_sequence import reset_table_id_seq
from ..utility.shared_enum import UserType



evan = NewUser(
    first_name="Evan",
    last_name="Explorer",
    middle_name="E.",
    email="evanexplorer@gmail.com",
    password='password',
    user_type=UserType.student
)

harry = NewUser(
    first_name="Harry",
    last_name="Helper",
    middle_name="H.",
    email="harryhelper@gmail.com",
    password='password',
    user_type=UserType.guardian
)

armstrong = NewUser(
    first_name="Armstrong",
    last_name="Allen",
    middle_name="A.",
    email="armstrong@gmail.com",
    password="armstrong",
    user_type=UserType.administrator
)

isaac = NewUser(
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
    entities: list[UserEntity] = []
    for user in users:
        entity = UserEntity.from_model(user)
        session.add(entity)
        entities.append(entity)
    
    print("Entities: ", entities)
    # we'll not need to reset this anymore
    # reset_table_id_seq(session, UserEntity, UserEntity.id, len(users) + 1)
    session.commit()  # Commit to ensure User IDs in database

@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield