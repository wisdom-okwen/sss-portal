from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..utility.security import hash_password
from ..models.user import User, UserUpdate
from ..database import db_session
from ..entities.user import UserEntity
from .exceptions import (
    ResourceNotFoundException,
    ResourceExistsException,
)
from ..utility.shared_enum import UserType
from ..models.auth import NewUser


class UserService:
    """Initialize service for communication to user table in db."""

    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session


    def get_all(self) -> list[User]:
        """Retrieve all users from user table in DB."""
        query = select(UserEntity)
        entities = self._session.scalars(query).all()
        return [entity.to_model() for entity in entities]


    def get_user(self, user_id: int) -> User:
        """Get user by id."""
        user = (
            self._session
            .query(UserEntity)
            .where(UserEntity.id == user_id)
            .one_or_none()
        )

        if not user:
            raise ResourceNotFoundException(
                f"No user found with matching id {user_id}"
            )
        
        return user.to_model()


    def get_by_email(self, email: str) -> User:
        """Get a user by unique email id."""
        user = (
            self._session
            .query(UserEntity)
            .where(UserEntity.email == email)
            .one_or_none()
        )

        if not user:
            raise ResourceNotFoundException(
                f"No user found with matching email id {email}"
            )
        
        return user.to_model()


    def get_users_by_type(self, user_type: UserType) -> list[User]:
        """Get all users with user_type of student."""
        query = select(UserEntity).where(UserEntity.user_type == user_type)
        students = self._session.scalars(query).all()
        return [student.to_model() for student in students]

      
    def add_user(self, user: NewUser) -> User:
        """Add new user."""
        query = select(UserEntity).where(UserEntity.email == user.email)
        existing_user = self._session.scalars(query).one_or_none()
        if existing_user:
            raise ResourceExistsException(
                f"User with email {user.email} already exists."
            )
        
        # Hash password if provided
        hashed_password = hash_password(user.password) if user.password else ""
        
        user_entity = UserEntity.from_model(user)
        user_entity.password = hashed_password
        self._session.add(user_entity)
        self._session.commit()
        
        return user_entity.to_model()


    def update_user(self, user_id: int, user: UserUpdate) -> User:
        """Update existing user with new data."""
        user_entity = self._session.get(UserEntity, user_id)
        if user_entity is None:

            raise ResourceNotFoundException(
                f"User does not exist in table."
            )
        if user.first_name is not None:
            user_entity.first_name = user.first_name
        if user.last_name is not None:
            user_entity.last_name = user.last_name
        if user.middle_name is not None:
            user_entity.middle_name = user.middle_name
        if user.user_type is not None:
            user_entity.user_type = user.user_type

        self._session.commit()
        return user_entity.to_model()


    
    def delete_user(self, user_id: int) -> User:
        """Delete user by id."""
        user = (
            self._session
            .query(UserEntity)
            .where(UserEntity.id == user_id)
            .one_or_none()
        )

        if user is None:
            raise ResourceNotFoundException(
                f"No user found with matching id: {user_id}"
            )
        self._session.delete(user)
        self._session.commit()
        return user.to_model()
