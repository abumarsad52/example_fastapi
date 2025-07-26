# databse.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
# print("🔌 Connected to database:", engine.url)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
