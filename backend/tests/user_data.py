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


amy = NewUser(
    first_name="Amy",
    last_name="Adams",
    middle_name="A.",
    email="amyadams@gmail.com",
    password="amyadams",
    user_type=UserType.student
)

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

rhonda = NewUser(
    first_name="Rhonda",
    last_name="Rhodes",
    middle_name="R.",
    email="rhondarhodes@gmail.com",
    password="rhondarhodes",
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

prince = NewUser(
    first_name="Prince",
    last_name="Peters",
    middle_name="P.",
    email="princepeters@gmail.com",
    password="princepeters",
    user_type=UserType.student
)

wisdom = NewUser(
    first_name="Wisdom",
    last_name="Wright",
    middle_name="W.",
    email="wisdomwright@gmail.com",
    password="wisdomwright",
    user_type=UserType.student
)

daisy = NewUser(
    first_name="Daisy",
    last_name="Doe",
    middle_name="D.",
    email="daisyd@gmail.com",
    password="daisyd",
    user_type=UserType.administrator
)

samuel = NewUser(
    first_name="Samuel",
    last_name="Smith",
    middle_name="S.",
    email="samuel@gmail.com",
    password="samuel",
    user_type=UserType.teacher
)

users = [
    amy,
    daisy,
    evan,
    harry,
    armstrong,
    isaac,
    prince,
    wisdom,
    samuel,
    rhonda
]

def insert_fake_data(session: Session):
    """Inserts fake user data into the database."""
    global users
    for user in users:
        entity = UserEntity.from_model(user)
        session.add(entity)
    session.commit()

@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Pytest fixture to insert fake data automatically."""
    insert_fake_data(session)
    yield