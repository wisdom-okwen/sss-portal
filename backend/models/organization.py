from pydantic import BaseModel
from backend.models.user import User
from enum import Enum
from backend.utility.shared_enum import OrganizationType


class Organization(BaseModel):
    id: int | None = None
    name: str
    slug: str
    description: str | None = None
    members: list[int] | None = None
    admin_members: list[int] | None = None
    teachers: list[int] | None = None
    advisor: int | None = None
    organization_type: OrganizationType = OrganizationType.other
