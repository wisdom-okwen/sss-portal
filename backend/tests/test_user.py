"""Tests for the UserService class."""

import pytest
from backend.entities.user import UserEntity

from backend.models.user import User
from backend.services import UserService

from backend.tests.fixtures import user_svc, user_svc_integration

# Data Models for Fake Data Inserted in Setup
from backend.tests.user_data import evan, harry


def test_get_all(user_svc_integration: UserService):
    users = ["Evan", "Harry", "Armstrong"]
    assert users is not None
    assert len(users) == 3