import os, uuid
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
import bcrypt
import jwt

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.database import Session, get_db
from src.models import RefreshToken, User


bearer_scheme = HTTPBearer()

# ENV
load_dotenv()
TOKEN_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not TOKEN_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY not set")
TOKEN_ALGORITHM = "HS256"
FAKE_PASSWORD_HASH = "$2b$12$C6UzMDM.H6dfI/f/IKcEeO8M0Y2F9v4K4D1R5Jt3fY6G6Z0p6E9eW"  # for timing-hardening


# Password handling
def hash_password(password: str) -> str:
    """
    Hash a password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# User authentication
def user_authentication(user_data, db: Session) -> User:
    """
    User Authentication with password timing-hardening  protection.
    """
    user: User | None = db.query(User).filter(User.username == user_data.username).first()

    # Timing-hardening
    user_password = (
        user.password_hash
        if user
        else FAKE_PASSWORD_HASH
    )

    # Authentication
    if not verify_password(user_data.password, user_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return user

# Token handling
def create_access_token(user_id: int, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    """
    Create JWT access token with user_id and expiration date.
    """
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + expires_delta
    }

    token = jwt.encode(payload, TOKEN_SECRET_KEY, algorithm=TOKEN_ALGORITHM)
    return token

def create_refresh_token(user_id: int, expires_delta: timedelta = timedelta(days=3)) -> dict:
    """
    Generate a new refresh token entry for a user.
    """
    now = datetime.now(timezone.utc)
    refresh_token = {
        "user_id": str(user_id),
        "token": str(uuid.uuid4()),
        "created_at": now,
        "expires_at": now + expires_delta,
        "active": True
    }

    return refresh_token

def validate_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    """
       Validate a JWT access token and return its payload.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload

def get_current_user(db: Session = Depends(get_db), payload: dict = Depends(validate_jwt_token)) -> User:
    """
    Retrieve the current user from the database using the JWT payload.
    """
    user_id = int(payload['sub'])
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def validate_refresh_token(token_obj: RefreshToken) -> RefreshToken:
    """
    Validate refresh token and return itself
    """
    if not token_obj:
        raise HTTPException(status_code=401, detail="Token not found")
    if not token_obj.active:
        raise HTTPException(status_code=401, detail="Token revoked")
    if token_obj.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Token has expired")

    return token_obj


