from typing import List
from typing import Optional
from sqlalchemy import String, ForeignKey, Table, Column, Integer
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
    Column('tech_id', Integer, ForeignKey('techs.techs_id'), primary_key=True)
)

class Tech(Base):
    __tablename__ = 'techs'

    techs_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[Optional[str]]

    projects: Mapped[List["Project"]] = relationship(secondary=project_techs, back_populates='techs')

class Project(Base):
    __tablename__ = 'projects'

    project_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[Optional[str]]

    techs: Mapped[List["Tech"]] = relationship(secondary=project_techs, back_populates='projects')


