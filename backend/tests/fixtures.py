"""Fixtures used for testing the core services."""

import pytest
from sqlalchemy.orm import Session
from ..services import UserService, OrganizationService


@pytest.fixture()
def user_svc(session: Session):
    """This fixture is used to test the UserService class."""
    return UserService(session)


@pytest.fixture()
def user_svc_integration(session: Session):
    """This fixture is used to test the UserService class."""
    return UserService(session)

@pytest.fixture()
def organization_svc(session: Session):
    """This fixture is used to test the OrganizationService class."""
    return OrganizationService(session)

@pytest.fixture()
def organization_svc_integration(session: Session):
    """This fixture is used to test the OrganizationService class."""
    return OrganizationService(session)