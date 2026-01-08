from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud import create_project, read_project, read_all_project, update_project, delete_project, link_techs_to_project
from src.schemas import ProjectCreateSchema, ProjectReadSchema, ProjectUpdateSchema
from src.database import get_db

router = APIRouter(prefix="/projects", tags=["Projects"])

# Create Project
@router.post("/", response_model=ProjectReadSchema, status_code=201)
def create_project_endpoint(data: ProjectCreateSchema, db: Session = Depends(get_db)):
    """
    Create a new Project object.
    """
    project = create_project(db, data)
    return project

# Read single Project
@router.get("/{project_id}", response_model=ProjectReadSchema, status_code=200)
def read_project_endpoint(project_id: int, db: Session = Depends(get_db)):
    """
    Get a Project by ID.
    """
    project = read_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Read all Projects
@router.get("/", response_model=List[ProjectReadSchema])
def read_all_project_endpoint(db: Session = Depends(get_db)):
    """
    Get all Project objects.
    """
    return read_all_project(db)

# Update Project
@router.patch("/{project_id}", response_model=ProjectReadSchema, status_code=200)
def update_project_endpoint(project_id: int, data: ProjectUpdateSchema, db: Session = Depends(get_db)):
    """
    Update an existing Project object by ID.
    """
    project = update_project(db, project_id, data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Delete Project
@router.delete("/{project_id}", status_code=204)
def delete_project_endpoint(project_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing Project object by ID.
    """
    delete_project(db, project_id)

# Link Techs to Project
@router.put("/{project_id}/techs", response_model=ProjectReadSchema, status_code=200)
def link_techs_to_project_endpoint(project_id: int, tech_ids: list[int], db: Session = Depends(get_db)):
    project = link_techs_to_project(db, project_id, tech_ids)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project