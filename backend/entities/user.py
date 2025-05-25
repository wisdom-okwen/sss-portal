from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from base_entity import EntityBase


class UserEntity(EntityBase):
    # entity for user table
    __table__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False, default="")
    last_name: Mapped[str] = mapped_column(String, nullable=False, default="")
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, default="")
    