from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer

from ..services.auth import AuthService

from ..models.auth import (
    UserRegister,
    UserLogin,
    ForgotPassword,
    ResetPassword,
    AuthResponse,
    MessageResponse,
    Token
)
from ..models.user import User
from ..utility.security import get_current_user


api = APIRouter(prefix="/api/auth")
security = HTTPBearer()

openapi_tags = {
    "name": "Authentication",
    "description": "User authentication, registration, and password reset operations.",
}


@api.post("/register", response_model=AuthResponse, tags=["Authentication"])
def register(
    user_data: UserRegister,
    auth_service: AuthService = Depends()
) -> AuthResponse:
    """
    Register a new user.

    Parameters:
        user_data: User registration data including name, email, and password
        auth_service: Authentication service dependency

    Returns:
        AuthResponse: Access token and user information
    """
    return auth_service.register_user(user_data)


@api.post("/login", response_model=AuthResponse, tags=["Authentication"])
def login(
    user_data: UserLogin,
    auth_service: AuthService = Depends()
) -> AuthResponse:
    """
    Login user with email and password.

    Parameters:
        user_data: User login credentials
        auth_service: Authentication service dependency

    Returns:
        AuthResponse: Access token and user information
    """
    return auth_service.login_user(user_data)


@api.post("/forgot-password", tags=["Authentication"])
def forgot_password(
    forgot_data: ForgotPassword,
    auth_service: AuthService = Depends()
) -> MessageResponse:
    """
    Send OTP for password reset.

    Parameters:
        forgot_data: User email for password reset
        auth_service: Authentication service dependency

    Returns:
        dict: Success message
    """
    return auth_service.forgot_password(forgot_data)


@api.post("/reset-password", response_model=AuthResponse, tags=["Authentication"])
def reset_password(
    reset_data: ResetPassword,
    auth_service: AuthService = Depends()
) -> AuthResponse:
    """
    Reset password using OTP and login user.

    Parameters:
        reset_data: Email, OTP, and new password
        auth_service: Authentication service dependency

    Returns:
        AuthResponse: Access token and user information
    """
    return auth_service.reset_password(reset_data)


@api.get("/me", response_model=User, tags=["Authentication"])
def get_me(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current user information.

    Parameters:
        current_user: Current authenticated user

    Returns:
        User: Current user information
    """
    return current_user


@api.post("/google", response_model=AuthResponse, tags=["Authentication"])
def google_login(
    token: Token, auth_service: AuthService = Depends()
) -> AuthResponse:
    """
    Handles login via Google's OAuth.
    The frontend should send the ID token from Google.
    """
    try:
        return auth_service.google_login(token.token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))