from typing import List
from typing import Optional
import enum
from sqlalchemy import String, ForeignKey, Table, Column, Integer, Boolean, Enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

project_techs = Table(
    'project_techs',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.project_id'), primary_key=True),
    Column('tech_id', Integer, ForeignKey('techs.tech_id'), primary_key=True)
)

class Tech(Base):
    __tablename__ = 'techs'

    tech_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[Optional[str]]

    projects: Mapped[List["Project"]] = relationship(secondary=project_techs, back_populates='techs')

class Project(Base):
    __tablename__ = 'projects'

    project_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[Optional[str]]

    techs: Mapped[List["Tech"]] = relationship(secondary=project_techs, back_populates='projects')

class UserRole(enum.Enum):
    ADMIN = 'admin'
    EDITOR = 'editor'
    USER = 'user'

class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.USER
    )

    # Not currently used
    fullname: Mapped[str | None] = mapped_column(String(150), nullable=True)

