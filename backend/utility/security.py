from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from ..env import getenv
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..models.user import User

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Stuff
SECRET_KEY = getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def hash_password(password: str) -> str:
    """Hashes a plain-text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user: User, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token for a given user.

    Args:
        user: The user object for whom to create the token.
              The user's email is used as the token's subject ('sub').
        expires_delta: An optional timedelta to override the default token expiration.

    Returns:
        The encoded JWT access token as a string.
    """
    
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode: Dict[str, Any] = { "sub": user.model_dump_json(), "exp": expire }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def generate_otp() -> str:
    """Generate a 6-digit OTP."""
    return str(secrets.randbelow(1000000)).zfill(6)


def _create_html_email_body(title: str, content_html: str) -> str:
    """Creates a standardized HTML email body with a header and footer."""
    logo_url = "https://via.placeholder.com/200x60.png?text=SSS+Portal+Logo"

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }}
            .container {{ max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            .header {{ background-color: #004aad; padding: 20px; text-align: center; }}
            .header img {{ max-width: 200px; }}
            .content {{ padding: 30px; line-height: 1.6; color: #333333; }}
            .content h1 {{ color: #004aad; }}
            .content strong {{ color: #004aad; font-size: 1.2em; }}
            .footer {{ background-color: #f4f4f4; color: #888888; text-align: center; padding: 20px; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="{logo_url}" alt="SSS Portal Logo">
            </div>
            <div class="content">
                <h1>{title}</h1>
                {content_html}
                <p>If you did not request this, please ignore this email.</p>
                <p>Best regards,<br>The SSS Portal Team</p>
            </div>
            <div class="footer">
                © {datetime.now().year} SSS Portal. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """


def _send_email(email: str, subject: str, html_body: str) -> bool:
    """Send an email using SMTP with an HTML body."""
    try:
        # Email configuration
        smtp_server = getenv("SMTP_SERVER")
        smtp_port = int(getenv("SMTP_PORT"))
        smtp_username = getenv("SMTP_USERNAME")
        smtp_password = getenv("SMTP_PASSWORD")
        emailer = getenv("EMAILER")
        
        # Create message
        message = MIMEMultipart()
        message["From"] = emailer
        message["To"] = email
        message["Subject"] = subject

        # Attach the HTML body
        message.attach(MIMEText(html_body, "html"))

        # Send email
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server: # Using SMTP_SSL for security
            server.login(smtp_username, smtp_password)
            server.send_message(message)

        return True
    except Exception as e:
        # In a real app, you would use a proper logger instead of print
        print(f"Error sending email: {e}")
        return False


def send_forgot_password_email(email: str, otp: str) -> bool:
    """Send OTP for password reset to user's email."""
    subject = "Password Reset Request - SSS Portal"
    title = "Password Reset Request"
    content_html = f"""
    <p>Dear User,</p>
    <p>We received a request to reset your password. Use the One-Time Password (OTP) below to proceed:</p>
    <p>Your OTP is: <strong>{otp}</strong></p>
    <p>This OTP is valid for 10 minutes.</p>
    """
    html_body = _create_html_email_body(title, content_html)
    return _send_email(email, subject, html_body)


def send_verification_email(email: str, code: str) -> bool:
    """Send verification code to user's email for account activation."""
    subject = "Verify Your Email Address - SSS Portal"
    title = "Email Verification"
    content_html = f"""
    <p>Dear User,</p>
    <p>Thank you for signing up! Please use the following verification code to complete your registration:</p>
    <p>Your verification code is: <strong>{code}</strong></p>
    <p>This code is valid for 10 minutes.</p>
    """
    html_body = _create_html_email_body(title, content_html)
    return _send_email(email, subject, html_body)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
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
        
        user_json = payload.get("sub")
        if user_json is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = User.model_validate_json(user_json)

        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
