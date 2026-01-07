from typing import Annotated, List

from pydantic import BaseModel, StringConstraints, field_validator, EmailStr
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
    tech_id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


# Project model
class ProjectCreate(BaseSchema):
    name: Annotated[str, StringConstraints(max_length=100)]
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None

class ProjectUpdate(BaseSchema):
    name: Annotated[str | None, StringConstraints(max_length=100)] = None
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None

class ProjectRead(BaseModel):
    project_id: int
    name: str
    description: str | None = None
    techs: List[TechRead] = []

    model_config = ConfigDict(from_attributes=True)

class ProjectTechLink(BaseModel):
    tech_ids: List[int]


# User model
class UserRegister(BaseSchema):
    username: str
    password: str
    email: EmailStr

class UserRead(BaseModel):
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
