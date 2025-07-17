"""Tests for the UserService class."""

import pytest
from backend.models.auth import NewUser
from backend.utility.shared_enum import UserType

from backend.models.user import UserUpdate
from backend.services import UserService
from backend.services.exceptions import ResourceNotFoundException

from backend.tests.fixtures import user_svc, user_svc_integration

# # Data Models for Fake Data Inserted in Setup
# from backend.tests.user_data import evan, harry


def test_get_all(user_svc_integration: UserService):
    users = user_svc_integration.get_all()
    assert users is not None
    assert len(users) >= 1


def test_get_user_by_id_invalid(user_svc_integration: UserService):
    user_id = 100000
    with pytest.raises(ResourceNotFoundException):
        _user = user_svc_integration.get_user(user_id)


def test_get_user_by_id(user_svc_integration: UserService):
    user_id_1 = 1
    user_1 = user_svc_integration.get_user(user_id_1)
    assert user_1 is not None
    assert user_1.first_name == "Evan"
    assert user_1.last_name == "Explorer"


def test_get_user_by_email(user_svc_integration: UserService):
    email = "evanexplorer@gmail.com"
    user = user_svc_integration.get_by_email(email)
    assert user.email == email


def test_get_users_by_type(user_svc_integration: UserService):
    type1, type2, type3 = UserType.student, UserType.administrator, UserType.teacher

    students = user_svc_integration.get_users_by_type(type1)
    assert len(students) >= 0
    assert students[0].user_type == type1
    
    administrators = user_svc_integration.get_users_by_type(type2)
    assert len(administrators) >= 0

    teachers = user_svc_integration.get_users_by_type(type3)
    assert len(teachers) >= 1
    assert teachers[0].user_type == type3



def test_add_user(user_svc_integration: UserService):
    user = NewUser(
        first_name="Hosana",
        last_name="Elorm",
        middle_name="Mawusi",
        password="MyP@ssWorldIsHiiliCompucated!",
        email="hosanamawulorm@yahoo.com",
        user_type=UserType.student
    )

    new_user = user_svc_integration.add_user(user)
    assert new_user is not None
    assert new_user.first_name == user.first_name
    assert new_user.email == user.email


def test_update_user(user_svc_integration: UserService):
    user = user_svc_integration.get_by_email("hosanamawulorm@yahoo.com")

    user_update = UserUpdate(
        first_name="Fuggor",
        middle_name="Ralphson"
    )

    updated_user = user_svc_integration.update_user(user.id, user_update)
    assert updated_user is not None
    assert updated_user.email == user.email


def test_delete_user(user_svc_integration: UserService):
    id = 1
    last_name = "Explorer"
    deleted_user = user_svc_integration.delete_user(id)
    assert deleted_user.last_name == last_name


