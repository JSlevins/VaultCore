from typing import Annotated, List

from pydantic import BaseModel, StringConstraints, field_validator, EmailStr, Field
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
class TechCreateSchema(BaseSchema):
    name: Annotated[str, StringConstraints(max_length=50)]
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None


class TechUpdateSchema(BaseSchema):
    name: Annotated[str | None, StringConstraints(max_length=50)] = None
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None


class TechReadSchema(BaseModel):
    tech_id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


# Project model
class ProjectCreateSchema(BaseSchema):
    name: Annotated[str, StringConstraints(max_length=100)]
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None


class ProjectUpdateSchema(BaseSchema):
    name: Annotated[str | None, StringConstraints(max_length=100)] = None
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None


class ProjectReadSchema(BaseModel):
    project_id: int
    name: str
    description: str | None = None
    techs: List[TechReadSchema] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ProjectTechLinkSchema(BaseModel):
    tech_ids: List[int]


# User model
class UserRegisterSchema(BaseSchema):
    username: str
    password: str
    email: EmailStr


class UserReadSchema(BaseModel):
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)

class UserLoginSchema(BaseSchema):
    username: str
    password: str


# Token models
class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str
