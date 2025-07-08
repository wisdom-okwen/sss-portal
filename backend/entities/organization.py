from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum
from backend.models.organization import Organization
from backend.models.user import User
from backend.utility.shared_enum import OrganizationType
from backend.entities.base_entity import EntityBase
from backend.entities.user import UserEntity


class OrganizationEntity(EntityBase):
    # Entity for organization table
    __tablename__ = "organization"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    organization_type: Mapped[OrganizationType] = mapped_column(
        Enum(OrganizationType), default=OrganizationType.other
    )

    members = relationship(
        "UserEntity",
        secondary="organization_members",
        back_populates="organizations_as_member",
    )
    admin_members = relationship(
        "UserEntity",
        secondary="organization_admin_members",
        back_populates="organizations_as_admin",
    )
    teachers = relationship(
        "UserEntity",
        secondary="organization_teachers",
        back_populates="organizations_as_teacher",
    )

    advisor_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("user.id"), nullable=True
    )
    advisor = relationship(
        "UserEntity", foreign_keys=[advisor_id], back_populates="advised_organizations"
    )

    def to_model(self) -> Organization:
        """Create pydantic model from the entity."""
        return Organization(
            id=self.id,
            name=self.name,
            slug=self.slug,
            description=self.description,
            members=[member.to_model() for member in self.members],
            admin_members=[admin.to_model() for admin in self.admin_members],
            teachers=[teacher.to_model() for teacher in self.teachers],
            advisor=self.advisor.to_model() if self.advisor else None,
            organization_type=self.organization_type,
        )

    @classmethod
    def from_model(cls, organization: Organization) -> "OrganizationEntity":
        """Create an entity from the pydantic model."""
        return cls(
            id=organization.id,
            name=organization.name,
            slug=organization.slug,
            description=organization.description,
            organization_type=organization.organization_type,
            members=(
                [UserEntity.from_model(member) for member in organization.members]
                if organization.members
                else []
            ),
            admin_members=(
                [UserEntity.from_model(admin) for admin in organization.admin_members]
                if organization.admin_members
                else []
            ),
            teachers=(
                [UserEntity.from_model(teacher) for teacher in organization.teachers]
                if organization.teachers
                else []
            ),
            advisor=(
                UserEntity.from_model(organization.advisor)
                if organization.advisor
                else None
            ),
        )

