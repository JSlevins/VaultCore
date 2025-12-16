from typing import Annotated

from pydantic import BaseModel, StringConstraints, field_validator
from pydantic.config import ConfigDict

class BaseSchema(BaseModel):

    @field_validator("description", check_fields=False)
    @classmethod
    def empty_string_to_none(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            v = v.strip()
            return v if v else None
        return v

# Tech model
class TechCreate(BaseSchema):
    name: Annotated[str, StringConstraints(max_length=50)]
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None

class TechUpdate(BaseSchema):
    name: Annotated[str | None, StringConstraints(max_length=50)] = None
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None

class TechRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tech_id: int
    name: str
    description: str | None = None


# Project model
class ProjectCreate(BaseSchema):
    name: Annotated[str, StringConstraints(max_length=100)]
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None

class ProjectUpdate(BaseSchema):
    name: Annotated[str | None, StringConstraints(max_length=100)] = None
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None

class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: int
    name: str
    description: str | None = None
