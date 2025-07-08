from pydantic import BaseModel
from backend.models.user import User
from enum import Enum
from backend.utility.shared_enum import OrganizationType


class Organization(BaseModel):
    id: str
    name: str
    slug: str
    description: str | None = None
    members: list[User] | None = None
    admin_members: list[User] | None = None
    teachers: list[User] | None = None
    advisor: User | None = None
    organization_type: OrganizationType = OrganizationType.other
