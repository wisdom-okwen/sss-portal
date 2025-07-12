from pydantic import BaseModel, EmailStr
from ..models.user import User, UserType

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    middle_name: str = ''
    email: EmailStr
    password: str
    user_type: UserType = UserType.administrator
    otp: str

class NewUser(BaseModel):
    first_name: str
    last_name: str
    middle_name: str = ''
    email: EmailStr
    password: str
    user_type: UserType = UserType.student

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    email: EmailStr
    otp: str
    password: str

class MessageResponse(BaseModel):
    message: str

class AuthResponse(BaseModel):
    access_token: str
    user: User
