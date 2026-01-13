from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import User, UserRole, RefreshToken
from src.schemas import (UserRegisterSchema, UserReadSchema, UserLoginSchema, RefreshTokenSchema,
                         TokenResponseSchema)
from src.security import (hash_password, create_access_token, create_refresh_token,
                          validate_refresh_token, user_authentication)

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


def create_user(db: Session, user_data: UserRegisterSchema) -> User:
    # Check the uniqueness of a username and email
    if db.query(User).filter(User.username == user_data.username).first() is not None:
        raise HTTPException(status_code=409, detail="Username already registered")
    if db.query(User).filter(User.email == user_data.email).first() is not None:
        raise HTTPException(status_code=409, detail="Email already registered")

    new_user = User(
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        email=user_data.email,
        role=UserRole.USER
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# User Register (by User)
@auth_router.post("/register", response_model=UserReadSchema, status_code=201)
def register_user(user_data: UserRegisterSchema, db: Session = Depends(get_db)) -> User:
    """
    Register a new user
    """
    user = create_user(db, user_data)
    return user


# User Auth

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 3

@auth_router.post("/login", response_model=TokenResponseSchema, status_code=200)
def user_login(user_data: UserLoginSchema, db: Session = Depends(get_db)) -> dict:
    """
    Authenticate a user and return access and refresh tokens.

    Raises:
        HTTPException: 401 if username/password are incorrect.

    Returns:
        dict: access_token (JWT), refresh_token (UUID), token_type ("bearer").
    """
    user = user_authentication(user_data, db)

    # Token generation
    access_token = create_access_token(
        user.user_id,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Refresh token generation
    refresh_token_data = create_refresh_token(
        user.user_id,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    refresh_token = RefreshToken(**refresh_token_data)
    # Add refresh token to Db
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token.token,
        "token_type": "bearer"
    }


@auth_router.post("/refresh", response_model=TokenResponseSchema, status_code=200)
def refresh_access_token(request: RefreshTokenSchema, db: Session = Depends(get_db)) -> dict:
    """
    Update access token using a valid refresh token.
    """
    token_obj: RefreshToken | None = db.query(RefreshToken).filter(RefreshToken.token == request.refresh_token).first()

    token_obj: RefreshToken = validate_refresh_token(token_obj)

    #Create new token
    access_token = create_access_token(
        user_id = token_obj.user_id,
        expires_delta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    #Deactivate old token
    token_obj.active = False
    db.add(token_obj)

    #Create new refresh token
    refresh_token_data = create_refresh_token(
        user_id = token_obj.user_id,
        expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    refresh_token = RefreshToken(**refresh_token_data)
    db.add(refresh_token)
    db.commit()

    return {
        'access_token': access_token,
        'refresh_token': refresh_token.token,
        'token_type': 'bearer'
    }