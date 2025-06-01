from pydantic import BaseModel
from ..utility.shared_enum import UserType

class User(BaseModel):
    id: int | None = None
    first_name: str = ''
    last_name: str = ''
    middle_name: str = ''
    email: str = ''
    password: str = ''
    user_type: UserType = UserType.other

