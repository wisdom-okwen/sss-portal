from typing import TYPE_CHECKING, Self
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from backend.models.organization import Organization
from backend.utility.shared_enum import OrganizationType
from backend.entities.base_entity import EntityBase


class OrganizationEntity(EntityBase):
    # Entity for organization table
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False) # Abbreviation or shortname
    description: Mapped[str] = mapped_column(String, nullable=True)
    organization_type: Mapped[OrganizationType] = mapped_column(Enum(OrganizationType), default=OrganizationType.other) 

    # Store lists of user IDs for members, admins, and teachers
    member_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=list)
    admin_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=list)
    teacher_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=list)
    advisor: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)

    def to_model(self) -> Organization:
        return Organization(
            id=self.id,
            name=self.name,
            slug=self.slug,
            description=self.description,
            members=self.member_ids,
            admin_members=self.admin_ids,
            teachers=self.teacher_ids,
            advisor=self.advisor,
            organization_type=self.organization_type,
        )

    @classmethod
    def from_model(cls, organization: Organization) -> Self:
        """Create an entity from the pydantic model, using user ID lists."""
        return cls(
            id=organization.id,
            name=organization.name,
            slug=organization.slug,
            description=organization.description,
            organization_type=organization.organization_type,
            member_ids=organization.members or [],
            admin_ids=organization.admin_members or [],
            teacher_ids=organization.teachers or [],
            advisor=organization.advisor,
        )
