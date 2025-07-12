from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..services.auth import AuthService
from ..services.user import UserService

from ..models.auth import (
    UserRegister,
    UserLogin,
    ForgotPassword,
    ResetPassword,
    AuthResponse,
    MessageResponse,
)
from ..models.user import User
from ..utility.security import verify_token


api = APIRouter(prefix="/api/auth")
security = HTTPBearer()

openapi_tags = {
    "name": "Authentication",
    "description": "User authentication, registration, and password reset operations.",
}


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(),
) -> User:
    """Get current authenticated user from JWT token."""
    try:
        token = credentials.credentials
        payload = verify_token(token)
        
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = user_service.get_by_email(email)

        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


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
def auth_google(
    auth_service: AuthService = Depends()
) -> AuthResponse:
    """
    Login with Google OAuth.
    
    NOTE: This endpoint is a placeholder and will be implemented later.
    It should handle Google OAuth token verification and user registration/login.

    Parameters:
        auth_service: Authentication service dependency

    Returns:
        AuthResponse: Access token and user information
    """
    # This will be implemented later with Google OAuth integration
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Google OAuth login not yet implemented"
    )
