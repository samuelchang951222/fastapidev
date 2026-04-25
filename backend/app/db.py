from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import settings

DATABASE_URL = settings.DATABASE_URL

connect_args = {}
# The check_same_thread argument is only needed for SQLite.
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
