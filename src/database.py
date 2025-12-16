from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base

SQLALCHEMY_DATABASE_URL = 'sqlite:///database.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True
)

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()