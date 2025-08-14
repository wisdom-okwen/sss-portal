"""
Mock data for organizations.
"""

import pytest
from sqlalchemy.orm import Session
from backend.entities.organization import OrganizationEntity
from backend.tests.reset_table_id_sequence import reset_table_id_seq
from ..models.organization import Organization
from ..utility.shared_enum import OrganizationType
from .user_data import amy, evan, armstrong, wisdom, prince, samuel

debate = Organization(
    id=1,
    name="Debate Club",
    slug="debate_club",
    description="A club for debating various topics.",
    organization_type=OrganizationType.academic,
    members=[],
    admin_members=[],
    teachers=[],
    advisor=None,
)

science_and_math = Organization(
    id=2,
    name="Science Club",
    slug="smc",
    description="A club for science enthusiasts.",
    organization_type=OrganizationType.academic,
    members=[],
    admin_members=[],
    teachers=[],
    advisor=None,
)

scripture_union = Organization(
    id=3,
    name="Scripture Union",
    slug="su",
    description="A club for scripture study and discussion.",
    organization_type=OrganizationType.religious,
    members=[],
    admin_members=[],
    teachers=[],
    advisor=None,
)

robotics = Organization(
    id=4,
    name="Robotics Club",
    slug="robotics_club",
    description="A club for robotics enthusiasts.",
    organization_type=OrganizationType.academic,
    members=[],
    admin_members=[],
    teachers=[],
    advisor=None,
)

basketball = Organization(
    id=5,
    name="Basketball Team",
    slug="basketball_team",
    description="A team for basketball players.",
    organization_type=OrganizationType.sports,
    members=[],
    admin_members=[],
    teachers=[],
    advisor=None,
)


acapella = Organization(
    id=6,
    name="Acapella Group",
    slug="acapella_group",
    description="A group for acapella singers.",
    organization_type=OrganizationType.cultural,
    members=[],
    admin_members=[],
    teachers=[],
    advisor=None,
)

school_choir = Organization(
    id=7,
    name="School Choir",
    slug="school_choir",
    description="A choir for school students.",
    organization_type=OrganizationType.cultural,
    members=[],
    admin_members=[],
    teachers=[],
    advisor=None,
)

organizations = [
    debate,
    science_and_math,
    scripture_union,
    robotics,
    basketball,
    acapella,
    school_choir,
]


def insert_fake_data(session: Session):
    global organizations
    entities = []
    for org in organizations:
        entity = OrganizationEntity.from_model(org)
        session.add(entity)
        entities.append(entity)
    reset_table_id_seq(
        session, OrganizationEntity, OrganizationEntity.id, len(organizations) + 1
    )
    session.commit()
    # return entities


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
