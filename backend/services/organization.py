from fastapi import Depends
from sqlalchemy import select, String, ForeignKey, Enum
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship
from backend.entities.user import UserEntity
from backend.models.organization import Organization
from backend.models.user import User
from backend.utility.shared_enum import OrganizationType
from backend.entities.organization import OrganizationEntity
from backend.entities.base_entity import EntityBase
from backend.entities.association_tables import (
    members_table,
    admin_members_table,
    teachers_table,
)
from backend.utility.shared_enum import UserType


class OrganizationService:
    """Service class for organization-related operations."""

    _sesssion: Session

    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> list[Organization]:
        """Retrieve all organizations from the database."""
        query = select(OrganizationEntity)
        result = self._session.scalars(query).all()
        return [entity.to_model() for entity in result]

    def get_organization_by_id(self, organization_id: str) -> Organization | None:
        """Fetch an organization by its ID."""
        stmt = select(OrganizationEntity).where(
            OrganizationEntity.id == organization_id
        )
        result = self._session.execute(stmt).scalar_one_or_none()
        return result.to_model() if result else None

    def get_organization_by_slug(self, slug: str) -> Organization | None:
        """Fetch an organization by its slug."""
        stmt = select(OrganizationEntity).where(OrganizationEntity.slug == slug)
        result = self._session.execute(stmt).scalar_one_or_none()
        return result.to_model() if result else None

    def create_organization(self, organization: Organization) -> Organization:
        """Create a new organization."""
        org_entity = OrganizationEntity.from_model(organization)
        self._session.add(org_entity)
        self._session.commit()
        self._session.refresh(org_entity)
        return org_entity.to_model()

    def update_organization(
        self, organization_id: str, organization: Organization
    ) -> Organization | None:
        """Update an existing organization."""
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity:
            return None
        for key, value in organization.model_dump().items():
            if key == "executive_members":
                continue
            if hasattr(org_entity, key):
                setattr(org_entity, key, value)
        self._session.commit()
        self._session.refresh(org_entity)
        return org_entity.to_model()

    def delete_organization(self, organization_id: str) -> bool:
        """Delete an organization by its ID."""
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity:
            return False

        self._session.delete(org_entity)
        self._session.commit()
        return True

    def get_organizations_by_user(self, user_id: str) -> list[Organization]:
        """Retrieve organizations associated with a user."""
        query = (
            select(OrganizationEntity)
            .join(
                members_table, OrganizationEntity.id == members_table.c.organization_id
            )
            .where(members_table.c.user_id == user_id)
        )
        result = self._session.scalars(query).all()
        return [entity.to_model() for entity in result]

    def get_members_by_organization(self, organization_id: str) -> list[User]:
        """Retrieve members of a specific organization."""
        query = (
            select(User)
            .join(members_table, User.id == members_table.c.user_id)
            .where(members_table.c.organization_id == organization_id)
        )
        result = self._session.scalars(query).all()
        return [user.to_model() for user in result]

    def add_member_to_organization(
        self, organization_id: str, user: User
    ) -> Organization:
        """Add a member to an organization."""
        if user.user_type != UserType.student:
            raise ValueError("Only students can be added as members")
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity:
            raise ValueError("Organization not found")

        user_entity = UserEntity.from_model(user)

        org_entity.members.append(user_entity)
        self._session.commit()
        self._session.refresh(org_entity)
        return org_entity.to_model()

    def remove_member_from_organization(
        self, organization_id: str, user_id: str
    ) -> bool:
        """Remove a member from an organization."""
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity:
            return False

        user_entity = self._session.get(UserEntity, user_id)
        if not user_entity or user_entity not in org_entity.members:
            return False

        org_entity.members.remove(user_entity)
        self._session.commit()
        return True

    def get_admins_by_organization(self, organization_id: str) -> list[User]:
        """Retrieve admin members of a specific organization."""
        query = (
            select(User)
            .join(admin_members_table, User.id == admin_members_table.c.user_id)
            .where(admin_members_table.c.organization_id == organization_id)
        )
        result = self._session.scalars(query).all()
        return [user.to_model() for user in result]

    def add_admin_to_organization(
        self, organization_id: str, user: User
    ) -> Organization:
        """Add an admin to an organization."""
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity:
            raise ValueError("Organization not found")

        user_entity = UserEntity.from_model(user)
        org_entity.admin_members.append(user_entity)
        self._session.commit()
        self._session.refresh(org_entity)
        return org_entity.to_model()

    def get_advisor_by_organization(self, organization_id: str) -> User | None:
        """Retrieve the advisor of a specific organization."""
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity or not org_entity.advisor:
            return None
        return org_entity.advisor.to_model()

    def set_advisor_for_organization(
        self, organization_id: str, user: User
    ) -> Organization:
        """Set an advisor for an organization."""
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity:
            raise ValueError("Organization not found")

        user_entity = UserEntity.from_model(user)
        org_entity.advisor = user_entity
        self._session.commit()
        self._session.refresh(org_entity)
        return org_entity.to_model()
