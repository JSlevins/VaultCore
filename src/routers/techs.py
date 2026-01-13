from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud import create_tech, read_tech, read_all_tech, update_tech, delete_tech
from src.models import UserRole, User
from src.schemas import TechCreateSchema, TechReadSchema, TechUpdateSchema
from src.database import get_db
from src.security import get_current_user

techs_router = APIRouter(prefix="/techs", tags=["Techs"])

# Create Tech
@techs_router.post("/", response_model=TechReadSchema, status_code=201)
def create_tech_endpoint(data: TechCreateSchema, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    """
    Create a new Tech object.
    """
    if not current_user.role in [UserRole.ADMIN, UserRole.EDITOR]:
        raise HTTPException(status_code=403, detail="You are not allowed to create techs.")
    tech = create_tech(db, data)
    return tech

# Read single Tech
@techs_router.get("/{tech_id}", response_model=TechReadSchema, status_code=200)
def read_tech_endpoint(tech_id: int, db: Session = Depends(get_db)):
    """
    Get a Tech object by ID.
    """
    tech = read_tech(db, tech_id)
    if not tech:
        raise HTTPException(status_code=404, detail="Tech not found")
    return tech

# Read all Techs
@techs_router.get("/", response_model=List[TechReadSchema])
def read_all_techs_endpoint(db: Session = Depends(get_db)):
    """
    Get all Tech objects.
    """
    return read_all_tech(db)

# Update Tech
@techs_router.patch("/{tech_id}", response_model=TechReadSchema, status_code=200)
def update_tech_endpoint(tech_id: int, data: TechUpdateSchema, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    """
    Update an existing Tech object by ID.
    """
    if not current_user.role in [UserRole.ADMIN, UserRole.EDITOR]:
        raise HTTPException(status_code=403, detail="You are not allowed to update techs.")
    tech = update_tech(db, tech_id, data)
    if not tech:
        raise HTTPException(status_code=404, detail="Tech not found")
    return tech

# Delete Tech
@techs_router.delete("/{tech_id}", status_code=204)
def delete_tech_endpoint(tech_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete an existing Tech object by ID.
    """
    if not current_user.role in [UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="You are not allowed to delete techs.")
    delete_tech(db, tech_id)