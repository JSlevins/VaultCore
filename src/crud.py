from sqlalchemy.orm import Session

from typing import List

from src.models import Tech, Project
from src.schemas import TechCreate, TechUpdate
from src.schemas import ProjectCreate, ProjectUpdate

### Tech CRUD
def create_tech(db: Session, data: TechCreate) -> Tech:
    """
    Create a new Tech object and save it to the database.

    Args:
        db (Session): SQLAlchemy database session
        data (TechCreate): Pydantic schema containing tech data to create

    Returns:
        Tech: The newly created Tech object
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

    Args:
        db (Session): SQLAlchemy database session
        tech_id (int): ID of the tech to retrieve

    Returns:
        Tech | None: The Tech object if found, otherwise None
    """
    return db.get(Tech, tech_id)

def read_all_tech(db: Session) -> List[Tech]:
    """
    Get all Tech objects
    """
    return db.query(Tech).all()  #type: ignore

def update_tech(db: Session, tech_id: int, data: TechUpdate) -> Tech | None:
    """
     Update an existing Tech object in the database.

     Args:
         db (Session): SQLAlchemy database session
         tech_id (int): ID of the Tech object to update
         data (TechUpdate): Pydantic schema with fields to update (only provided fields are updated)

     Returns:
         Tech | None: The updated Tech object if found, otherwise None
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

    Args:
        db (Session): SQLAlchemy database session
        tech_id (int): ID of the Tech object to delete

    Returns:
        None
    """
    tech = db.get(Tech, tech_id)

    if not tech:
        return

    db.delete(tech)
    db.commit()

### Project CRUD
def create_project(db: Session, data: ProjectCreate) -> Project:
    """
    Create a new Project object and save it to the database.

    Args:
        db (Session): SQLAlchemy database session
        data (ProjectCreate): Pydantic schema containing project data to create

    Returns:
        Project: The newly created Project object
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

    Args:
        db (Session): SQLAlchemy database session
        project_id (int): ID of the project to retrieve

    Returns:
        Project | None: The Project object if found, otherwise None
    """
    return db.get(Project, project_id)

def read_all_project(db: Session) -> List[Project]:
    """
    Get all Project objects.
    """
    return db.query(Project).all()  #type: ignore

def update_project(db: Session, project_id: int, data: ProjectUpdate) -> Project | None:
    """
     Update an existing Project object in the database.

     Args:
         db (Session): SQLAlchemy database session
         project_id (int): ID of the Project object to update
         data (ProjectUpdate): Pydantic schema with fields to update (only provided fields are updated)

     Returns:
         Project | None: The updated Project object if found, otherwise None
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

    Args:
        db (Session): SQLAlchemy database session
        project_id (int): ID of the Project object to delete

    Returns:
        None
    """
    project = db.get(Project, project_id)
    if not project:
        return

    db.delete(project)
    db.commit()