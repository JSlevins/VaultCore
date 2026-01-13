from fastapi import HTTPException
from sqlalchemy.orm import Session

from typing import List

from src.models import Tech, Project
from src.schemas import TechCreateSchema, TechUpdateSchema, ProjectCreateSchema, ProjectUpdateSchema

### Tech CRUD
def create_tech(db: Session, data: TechCreateSchema) -> Tech:
    """
    Create a new Tech object and save it to the database.
    """
    tech = Tech(
        name = data.name,
        description = data.description,
    )

    db.add(tech)
    db.commit()
    db.refresh(tech)
    return tech

def read_tech(db: Session, tech_id: int) -> Tech | None:
    """
    Get a Tech object by its ID.
    """
    return db.get(Tech, tech_id)

def read_all_tech(db: Session) -> List[Tech]:
    """
    Get all Tech objects
    """
    return db.query(Tech).all()  #type: ignore

def update_tech(db: Session, tech_id: int, data: TechUpdateSchema) -> Tech | None:
    """
     Update an existing Tech object in the database.
     """
    tech: Tech | None = db.get(Tech, tech_id)  # IDE doesn't like it without type annotation for some reason
    if not tech:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tech, key, value)

    db.commit()
    db.refresh(tech)
    return tech

def delete_tech(db: Session, tech_id: int) -> None:
    """
    Delete a Tech object from the database.
    """
    tech = db.get(Tech, tech_id)

    if not tech:
        raise HTTPException(status_code=404, detail="Tech does not found.")

    db.delete(tech)
    db.commit()

### Project CRUD
def create_project(db: Session, data: ProjectCreateSchema) -> Project:
    """
    Create a new Project object and save it to the database.
    """
    project = Project(
        name = data.name,
        description = data.description,
    )

    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def read_project(db: Session, project_id: int) -> Project | None:
    """
    Get a Project object by its ID.
    """
    return db.get(Project, project_id)

def read_all_project(db: Session) -> List[Project]:
    """
    Get all Project objects.
    """
    return db.query(Project).all()  #type: ignore

def update_project(db: Session, project_id: int, data: ProjectUpdateSchema) -> Project | None:
    """
     Update an existing Project object in the database.
     """
    project: Project | None = db.get(Project, project_id)
    if not project:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project_id: int) -> None:
    """
    Delete a Project object from the database.
    """
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

def link_techs_to_project(db: Session, project_id: int, tech_ids: list[int]) -> Project | None:
    project = db.get(Project, project_id)
    if not project:
        return None

    techs = db.query(Tech).filter(Tech.tech_id.in_(tech_ids)).all()

    for t in techs:
        if t not in project.techs:
            project.techs.append(t)

    db.commit()
    db.refresh(project)
    return project  #type: ignore

