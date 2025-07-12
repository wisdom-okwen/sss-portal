from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.entities.user import UserEntity
from backend.models.organization import Organization
from backend.models.user import User
from backend.entities.organization import OrganizationEntity
from backend.utility.shared_enum import UserType
from backend.services.exceptions import (
    ResourceNotFoundException,
    ResourceExistsException,
)


class OrganizationService:
    """Service class for organization-related operations."""

    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> list[Organization]:
        """Retrieve all organizations from the database."""
        query = select(OrganizationEntity)
        result = self._session.scalars(query).all()
        return [entity.to_model() for entity in result]

    def get_organization_by_id(self, organization_id: int) -> Organization:
        """Fetch an organization by its ID."""
        stmt = select(OrganizationEntity).where(
            OrganizationEntity.id == organization_id
        )
        result = self._session.execute(stmt).scalar_one_or_none()
        if not result:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} not found."
            )
        return result.to_model()

    def get_organization_by_slug(self, slug: str) -> Organization:
        """Fetch an organization by its slug."""
        stmt = select(OrganizationEntity).where(OrganizationEntity.slug == slug)
        result = self._session.execute(stmt).scalar_one_or_none()

        if not result:
            raise ResourceNotFoundException(
                f"Organization with slug '{slug}' not found."
            )
        return result.to_model()

    def create_organization(self, organization: Organization) -> Organization:
        """Create a new organization."""
        existing_org = self._session.execute(
            select(OrganizationEntity).where(
                OrganizationEntity.slug == organization.slug
            )
        ).scalar_one_or_none()
        if existing_org:
            raise ResourceExistsException(
                f"Organization with slug '{organization.slug}' already exists."
            )
        org_entity = OrganizationEntity.from_model(organization)
        self._session.add(org_entity)
        self._session.commit()
        self._session.refresh(org_entity)
        return org_entity.to_model()

    def update_organization(
        self, organization_id: int, organization: Organization
    ) -> Organization:
        """Update an existing organization."""
        org_entity = self._session.get(OrganizationEntity, organization_id)

        if not org_entity:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} not found."
            )

        for key, value in organization.model_dump().items():
            if key == "executive_members":
                continue
            if hasattr(org_entity, key):
                setattr(org_entity, key, value)
        self._session.commit()
        self._session.refresh(org_entity)
        return org_entity.to_model()

    def delete_organization(self, organization_id: int) -> Organization:
        """Delete an organization by its ID."""
        org_entity = self._session.get(OrganizationEntity, organization_id)

        if not org_entity:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} not found."
            )

        self._session.delete(org_entity)
        self._session.commit()
        return org_entity.to_model()

    def get_organizations_by_user(self, user_id: int) -> list[Organization]:
        """Retrieve organizations associated with a user by checking user_id in member/admin/teacher arrays."""
        user = self._session.get(UserEntity, user_id)

        if not user:
            raise ResourceNotFoundException(f"User with ID {user_id} not found.")

        query = select(OrganizationEntity).where(
            (OrganizationEntity.member_ids.contains([user_id]))
            | (OrganizationEntity.admin_ids.contains([user_id]))
            | (OrganizationEntity.teacher_ids.contains([user_id]))
        )
        result = self._session.scalars(query).all()
        return [entity.to_model() for entity in result]

    def get_organization_members(self, organization_id: int) -> list[User]:
        """Retrieve members of a specific organization by user ID list."""
        org = self._session.get(OrganizationEntity, organization_id)
        if not org:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} not found."
            )
        if not org.member_ids:
            return []
        query = select(UserEntity).where(UserEntity.id.in_(org.member_ids))
        members = self._session.scalars(query).all()
        return [user.to_model() for user in members]

    def add_member_to_organization(
        self, organization_id: int, user_id: int
    ) -> Organization:
        """Add a member to an organization by appending user ID to member_ids array."""
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} not found."
            )

        user = self._session.get(UserEntity, user_id)
        if not user:
            raise ResourceNotFoundException(f"User with ID {user_id} not found.")
        if user.user_type != UserType.student:
            raise ValueError("Only students can be added as members")
        if user.id in org_entity.member_ids:
            raise ResourceExistsException(
                "User is already a member of this organization"
            )

        org_entity.member_ids.append(user.id)
        self._session.commit()
        self._session.refresh(org_entity)
        return org_entity.to_model()

    def remove_member_from_organization(
        self, organization_id: int, user_id: int
    ) -> Organization:
        """Remove a member from an organization by removing user ID from member_ids array."""
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} not found."
            )
        if user_id not in org_entity.member_ids:
            raise ResourceNotFoundException(
                f"User with ID {user_id} is not a member of this organization."
            )

        org_entity.member_ids.remove(user_id)
        self._session.commit()
        return org_entity.to_model()

    def get_org_teachers(self, organization_id: int) -> list[User]:
        """Retrieve teachers of a specific organization by user ID list."""
        org = self._session.get(OrganizationEntity, organization_id)
        if not org:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} not found."
            )
        if not org.teacher_ids:
            return []
        query = select(UserEntity).where(UserEntity.id.in_(org.teacher_ids))
        result = self._session.scalars(query).all()
        return [user.to_model() for user in result]

    def add_teacher_to_organization(
        self, organization_id: int, user_id: int
    ) -> Organization:
        """Add a teacher to an organization by appending user ID to teacher_ids array."""
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} not found."
            )

        user = self._session.get(UserEntity, user_id)
        if not user:
            raise ResourceNotFoundException(f"User with ID {user_id} not found.")
        if user.id in org_entity.teacher_ids:
            raise ResourceExistsException(
                "User is already a teacher of this organization"
            )

        org_entity.teacher_ids.append(user.id)
        self._session.commit()
        self._session.refresh(org_entity)
        return org_entity.to_model()

    def get_org_admins(self, organization_id: int) -> list[User]:
        """Retrieve admin members of a specific organization by user ID list."""
        org = self._session.get(OrganizationEntity, organization_id)
        if not org:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} not found."
            )
        if not org.admin_ids:
            return []
        query = select(UserEntity).where(UserEntity.id.in_(org.admin_ids))
        result = self._session.scalars(query).all()
        return [user.to_model() for user in result]

    def add_admin_to_organization(
        self, organization_id: int, user_id: int
    ) -> Organization:
        """Add an admin to an organization by appending user ID to admin_ids array."""
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} not found."
            )

        user = self._session.get(UserEntity, user_id)
        if not user:
            raise ResourceNotFoundException(f"User with ID {user_id} not found.")
        if user.id in org_entity.admin_ids:
            raise ResourceExistsException(
                "User is already an admin of this organization"
            )

        org_entity.admin_ids.append(user.id)
        self._session.commit()
        self._session.refresh(org_entity)
        return org_entity.to_model()

    def remove_admin_from_organization(
        self, organization_id: int, user_id: int
    ) -> Organization:
        """Remove an admin from an organization by removing user ID from admin_ids array."""
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} not found."
            )
        if user_id not in org_entity.admin_ids:
            raise ResourceNotFoundException(
                f"User with ID {user_id} is not an admin of this organization."
            )

        org_entity.admin_ids.remove(user_id)
        self._session.commit()
        return org_entity.to_model()

    def get_organization_advisor(self, organization_id: int) -> User | None:
        """Retrieve the advisor of a specific organization."""
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} not found."
            )
        if not org_entity.advisor:
            return None
        user_entity = self._session.get(UserEntity, org_entity.advisor)
        return user_entity.to_model()

    def set_advisor_for_organization(
        self, organization_id: int, user_id: int
    ) -> Organization:
        """Set an advisor for an organization."""
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} not found."
            )

        user = self._session.get(UserEntity, user_id)
        if not user:
            raise ResourceNotFoundException(f"User with ID {user_id} not found.")

        org_entity.advisor = user.id
        self._session.commit()
        self._session.refresh(org_entity)
        return org_entity.to_model()

    def remove_advisor_from_organization(self, organization_id: int) -> Organization:
        """Remove the advisor from an organization."""
        org_entity = self._session.get(OrganizationEntity, organization_id)
        if not org_entity:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} not found."
            )

        if not org_entity.advisor:
            raise ResourceNotFoundException(
                f"Organization with ID {organization_id} has no advisor to remove."
            )
        
        org_entity.advisor = None
        self._session.commit()
        return org_entity.to_model()