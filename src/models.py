from datetime import datetime, timedelta, timezone
from typing import List
from typing import Optional
import enum
from sqlalchemy import String, ForeignKey, Table, Column, Integer, Enum, DateTime
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
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        nullable=False,
        server_default=str(UserRole.USER)
    )


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), nullable=False)
    token: Mapped[str] = mapped_column(String(250), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                                                 nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 default=lambda: datetime.now(timezone.utc) + timedelta(days=3),
                                                 nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
