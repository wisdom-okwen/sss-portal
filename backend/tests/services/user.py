"""Tests for the UserService class."""

import pytest
from ...entities.user import UserEntity

from ...models.user import User
from ...services import UserService

from ..fixtures import user_svc, user_svc_integration

# Data Models for Fake Data Inserted in Setup
from ..user_data import evan, harry


def test_get_all(user_svc_integration: UserService):
    """Test that a user can be retrieved by PID."""
    users = user_svc_integration.all()
    assert users is not None
    assert len(users) == 2