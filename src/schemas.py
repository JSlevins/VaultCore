from typing import Annotated

from pydantic import BaseModel, StringConstraints
from pydantic.config import ConfigDict

# Tech model
class TechAdd(BaseModel):
    name: Annotated[str, StringConstraints(max_length=50)]
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None

class TechUpdate(BaseModel):
    name: Annotated[str | None, StringConstraints(max_length=50)] = None
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None

class TechRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tech_id: int
    name: str
    description: str | None = None


# Project model
class ProjectAdd(BaseModel):
    name: Annotated[str, StringConstraints(max_length=100)]
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None

class ProjectUpdate(BaseModel):
    name: Annotated[str | None, StringConstraints(max_length=100)] = None
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None

class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: int
    name: str
    description: str | None = None
