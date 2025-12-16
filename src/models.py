from typing import List
from typing import Optional
from sqlalchemy import String, ForeignKey, Table, Column, Integer, Boolean
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

class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
    is_admin: Mapped[bool] = mapped_column(Boolean)

    # Those two actually for possible future functional extension
    fullname: Mapped[str | None] = mapped_column(String(150), nullable=True)
    email: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)

