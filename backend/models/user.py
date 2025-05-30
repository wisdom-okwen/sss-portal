from pydantic import BaseModel

class User(BaseModel):
    id: int | None = None
    first_name: str = ''
    last_name: str = ''
    middle_name: str = ''
    email: str = ''
    password: str = ''

