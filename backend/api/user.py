from fastapi import APIRouter, Depends
from ..services.user import UserService
from ..models.user import User

api = APIRouter(prefix='/api/users')
openapi_tags = {
    "name": "Users",
    "description": "User profile search and related operations."
}

@api.get('', response_model=list[User], tags=["Users"])
def get_users(
    user_service: UserService = Depends()
) -> list[User]:
    """
    Get all users

    Parameters:
        user_service: a valid UserService

    Returns:
        list[User]: All `User`s in the user table
    """
    return user_service.get_all()
