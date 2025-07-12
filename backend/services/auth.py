from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta, timezone

from google.oauth2.id_token import verify_oauth2_token # type: ignore
from google.auth.transport import requests

from ..database import db_session
from ..entities.user import UserEntity
from ..entities.otp import OTPEntity
from ..models.auth import UserRegister, UserLogin, ForgotPassword, ResetPassword, AuthResponse, MessageResponse
from ..utility.security import (
    hash_password,
    verify_password,
    create_access_token,
    generate_otp,
    send_forgot_password_email,
    send_verify_email_email,
)
from ..utility.shared_enum import UserType
from .exceptions import (
    ResourceNotFoundException,
    ResourceExistsException,
)

from ..env import getenv

GOOGLE_CLIENT_ID = getenv("GOOGLE_CLIENT_ID")


class AuthService:
    """Authentication service for user registration, login, and password reset."""

    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def verify_email(self, email: str) -> MessageResponse:
        otp = generate_otp()
        success = send_verify_email_email(email, otp)
        if success:
            return MessageResponse(message="An verification code has been sent to your email")
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send verification code"
            )

    def register_user(self, user_data: UserRegister) -> AuthResponse:
        """Register a new user."""
        # Check if user already exists
        existing_user = self._session.query(UserEntity).filter(
            UserEntity.email == user_data.email
        ).first()
        
        if existing_user:
            raise ResourceExistsException(f"User with email {user_data.email} already exists")
        
        # Create new user
        user_entity = UserEntity(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            middle_name=user_data.middle_name,
            email=user_data.email,
            password=hash_password(user_data.password),
            user_type=UserType(user_data.user_type)
        )
        
        self._session.add(user_entity)
        self._session.commit()
        self._session.refresh(user_entity)
        
        # Generate access token
        access_token = create_access_token(user_entity.to_model())
        
        return AuthResponse(
            access_token=access_token,
            user=user_entity.to_model()
        )

    def login_user(self, user_data: UserLogin) -> AuthResponse:
        """Login user with email and password."""
        # Find user by email
        user = self._session.query(UserEntity).filter(
            UserEntity.email == user_data.email
        ).first()
        
        if not user:
            raise ResourceNotFoundException("Invalid email or password")
        
        # Verify password
        if not verify_password(user_data.password, user.password):
            raise ResourceNotFoundException("Invalid email or password")
        
        # Generate access token
        access_token = create_access_token(user.to_model())
        
        return AuthResponse(
            access_token=access_token,
            user=user.to_model()
        )

    def forgot_password(self, forgot_data: ForgotPassword) -> MessageResponse:
        """Send OTP for password reset."""
        # Check if user exists
        user = self._session.query(UserEntity).filter(
            UserEntity.email == forgot_data.email
        ).first()
        
        if not user:
            raise ResourceNotFoundException("User with this email does not exist")
        
        # Generate OTP
        otp_code = generate_otp()
        
        # Set expiration time (10 minutes from now)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        
        # Invalidate any existing OTPs for this email
        self._session.query(OTPEntity).filter(
            and_(
                OTPEntity.email == forgot_data.email,
                OTPEntity.is_used == False
            )
        ).update({"is_used": True})
        
        # Create new OTP entry
        otp_entity = OTPEntity(
            email=forgot_data.email,
            otp_code=otp_code,
            expires_at=expires_at,
            is_used=False
        )
        
        self._session.add(otp_entity)
        self._session.commit()
        
        # Send OTP via email
        email_sent = send_forgot_password_email(forgot_data.email, otp_code)
        
        if not email_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send OTP email"
            )
        
        return MessageResponse(message="OTP sent to your email address")

    def reset_password(self, reset_data: ResetPassword) -> AuthResponse:
        """Reset password using OTP."""
        # Find valid OTP
        otp_entity = self._session.query(OTPEntity).filter(
            and_(
                OTPEntity.email == reset_data.email,
                OTPEntity.otp_code == reset_data.otp,
                OTPEntity.is_used == False,
                OTPEntity.expires_at > datetime.now(timezone.utc)
            )
        ).first()
        
        if not otp_entity:
            raise ResourceNotFoundException("Invalid or expired OTP")
        
        # Find user
        user = self._session.query(UserEntity).filter(
            UserEntity.email == reset_data.email
        ).first()
        
        if not user:
            raise ResourceNotFoundException("User not found")
        
        # Update password
        user.password = hash_password(reset_data.password)
        
        # Mark OTP as used
        otp_entity.is_used = True
        
        self._session.commit()
        
        # Generate access token (log user in)
        access_token = create_access_token(user.to_model())
        
        return AuthResponse(
            access_token=access_token,
            user=user.to_model()
        )

    def google_login(self, google_token: str) -> AuthResponse:
        """
        Handles the Google login flow by registering or logging in a user.

        Args:
            google_token: The ID token received from Google.

        Returns:
            An AuthResponse containing the user model and a JWT access token.
        """
        try:
            id_info = verify_oauth2_token(
                google_token, requests.Request(), GOOGLE_CLIENT_ID
            )
            email = id_info["email"]
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token"
            )

        existing_user = self._session.query(UserEntity).filter(
            UserEntity.email == email
        ).first()

        if existing_user:
            access_token = create_access_token(existing_user.to_model())
            return AuthResponse(
                access_token=access_token,
                user=existing_user.to_model()
            )

        new_user = UserEntity(
            first_name=id_info.get("given_name", ""),
            last_name=id_info.get("family_name", ""),
            email=email,
            password="",
        )

        self._session.add(new_user)
        self._session.commit()
        self._session.refresh(new_user)

        access_token = create_access_token(new_user.to_model())

        return AuthResponse(
            access_token=access_token,
            user=new_user.to_model()
        )