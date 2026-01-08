import os, uuid
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
import bcrypt
import jwt

# Password handling
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# Token handling

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def create_access_token(user_id: int, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    """
    Create JWT access token with user_id and expiration date.

    Args:
        user_id (int): ID of the user.
        expires_delta (timedelta, optional): Token lifetime. Defaults to 30 minutes.

    Returns:
        str: Encoded JWT token.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + expires_delta
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def create_refresh_token(user_id: int, expires_delta: timedelta = timedelta(days=3)) -> dict:
    """
    Generate a new refresh token entry for a user.

    Args:
        user_id (int): ID of the user.
        expires_delta (timedelta, optional): Lifetime of the token. Defaults to 3 days.

    Returns:
        dict: Token data matching the RefreshToken model.
    """
    now = datetime.now(timezone.utc)
    refresh_token = {
        "user_id": user_id,
        "token": str(uuid.uuid4()),
        "created_at": now,
        "expires_at": now + expires_delta,
        "active": True
    }

    return refresh_token