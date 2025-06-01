from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..utility.security import hash_password
from ..models.user import User
from ..database import db_session
from ..entities.user import UserEntity
from .exceptions import UserPermissionException


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
