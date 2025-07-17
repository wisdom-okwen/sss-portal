from pydantic import BaseModel
from ..utility.shared_enum import UserType
from typing import Optional

class User(BaseModel):
    id: int
    first_name: str = ''
    last_name: str = ''
    middle_name: str = ''
    email: str = ''
    user_type: UserType = UserType.other

class UserUpdate(BaseModel):
    first_name: Optional[str] =  None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    user_type: Optional[UserType] = None