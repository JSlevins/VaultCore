from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.security import hash_password
from src.models import User, UserRole
from src.database import get_db
from src.schemas import UserRegister, UserRead

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_user(db: Session, user_data: UserRegister) -> User:
    # Check the uniqueness of a username and email
    if db.query(User).filter(User.username == user_data.username).first() is not None:
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(User).filter(User.email == user_data.email).first() is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        email=user_data.email,
        role=UserRole.USER
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# User Register (by User)
@auth_router.post("/register", response_model=UserRead, status_code=201)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    user = create_user(db, user_data)
    return user
