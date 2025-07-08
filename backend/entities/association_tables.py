from sqlalchemy import Table, Column, ForeignKey
from backend.entities.base_entity import EntityBase

members_table = Table(
    "organization_members",
    EntityBase.metadata,
    Column("organization_id", ForeignKey("organization.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)

admin_members_table = Table(
    "organization_admin_members",
    EntityBase.metadata,
    Column("organization_id", ForeignKey("organization.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)

teachers_table = Table(
    "organization_teachers",
    EntityBase.metadata,
    Column("organization_id", ForeignKey("organization.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)
