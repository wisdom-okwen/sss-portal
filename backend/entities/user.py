from typing import Self
from sqlalchemy import String, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column
from .base_entity import EntityBase
from backend.models.user import User
from ..utility.shared_enum import UserType


class UserEntity(EntityBase):
    # Entity for user table
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    last_name: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    middle_name: Mapped[str] = mapped_column(String(64), nullable=True)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, default="")
    password: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    user_type: Mapped[UserType] = mapped_column(Enum(UserType), nullable=False, default=UserType.other)

    

    def to_model(self) -> User:
        """Create pydantic model from the entity."""
        return User(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            email=self.email,
            user_type=self.user_type
        )

    @classmethod
    def from_model(cls, model: User) -> Self:
        """Create an entity from corresponding pydantic model."""
        return cls(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            middle_name=model.middle_name,
            email=model.email,
            user_type=model.user_type
        )