from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud import create_tech, read_tech, read_all_tech, update_tech, delete_tech
from src.schemas import TechCreate, TechRead, TechUpdate
from src.database import get_db

router = APIRouter(prefix="/techs", tags=["Techs"])

# Create Tech
@router.post("/", response_model=TechRead, status_code=201)
def create_tech_endpoint(data: TechCreate, db: Session = Depends(get_db)):
    """
    Create a new Tech object.
    """
    tech = create_tech(db, data)
    return tech

# Read single Tech
@router.get("/{tech_id}", response_model=TechRead, status_code=200)
def read_tech_endpoint(tech_id: int, db: Session = Depends(get_db)):
    """
    Get a Tech object by ID.
    """
    tech = read_tech(db, tech_id)
    if not tech:
        raise HTTPException(status_code=404, detail="Tech not found")
    return tech

# Read all Techs
@router.get("/", response_model=List[TechRead])
def read_all_techs_endpoint(db: Session = Depends(get_db)):
    """
    Get all Tech objects.
    """
    return read_all_tech(db)

# Update Tech
@router.patch("/{tech_id}", response_model=TechRead, status_code=200)
def update_tech_endpoint(tech_id: int, data: TechUpdate, db: Session = Depends(get_db)):
    """
    Update an existing Tech object by ID.
    """
    tech = update_tech(db, tech_id, data)
    if not tech:
        raise HTTPException(status_code=404, detail="Tech not found")
    return tech

# Delete Tech
@router.delete("/{tech_id}", status_code=204)
def delete_tech_endpoint(tech_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing Tech object by ID.
    """
    delete_tech(db, tech_id)