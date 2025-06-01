from fastapi import APIRouter, Depends
from ..services.user import UserService
from ..models.user import User
from ..utility.shared_enum import UserType


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


@api.get('/by_user_type{user_type}', response_model=list[User], tags=["Users"])
def get_by_user_type(
    user_type: UserType,
    user_service: UserService = Depends()
) -> list[User]:
    """
    Get all users of a particular type

    Parameters:
        user_service: a valid UserService
        user_type: type of user

    Returns:
        list[User]: All `User`s in the user table of user_type
    """
    return user_service.get_users_by_type(user_type)


@api.get('/{user_id}', response_model=User, tags=["Users"])
def get_user(
    user_id: int,
    user_service: UserService = Depends()
) -> User:
    """
    Get a user by id

    Parameters:
        user_service: a valid UserService
        user_id: id correponding to the user

    Returns:
        User: A `User` with id matching user_id in the user table
    """
    return user_service.get_user(user_id)


@api.get('/by_email/{email}', response_model=User, tags=["Users"])
def get_by_email(
    email: str,
    user_service: UserService = Depends()
) -> User:
    """
    Get a user by their unique email id

    Parameters:
        user_service: a valid UserService
        email: email correponding to the user

    Returns:
        User: A `User` with matching email in the user table
    """
    return user_service.get_by_email(email)


@api.post("/", response_model=User, tags=["Users"])
def add_user(
    user: User,
    user_service: UserService = Depends()
) -> User:
    """
    Add  a new user

    Parameters:
        user_service: a valid UserService
        user: new user to be added

    Returns:
        User: the new user when added successfully
    """
    return user_service.add_user(user)


@api.put("/{user_id}", responses={404: {"model": None}}, response_model=User, tags=["Users"])
def update_user(
    user_id: int,
    user: User,
    user_service: UserService = Depends()
):
    """
    Update a user in table

    Parameters:
        user_service: a valid UserService
        user: user data for user
        user_id: id corresponding to user to be updated

    Returns:
        User: the new user data if user was successfully updated
    """
    return user_service.update_user(user_id, user)


@api.delete('/{id}', response_model=User, tags=["Users"])
def delete_user(
    user_id: int,
    user_service: UserService = Depends()
) -> User:
    """
    Delete a user by id

    Parameters:
        user_service: a valid UserService
        user_id: id correponding to the user

    Returns:
        User: the user data if user was successfully deleted
    """
    return user_service.delete_user(user_id)