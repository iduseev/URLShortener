# backend/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config.config import get_settings

# engine is the entry point to the database
engine = create_engine(
    get_settings().db_url, 
    connect_args={"check_same_thread": False}  # because we working with an SQLite DB
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# returns a class that connects the DB engine to the SQLAlchemy functionality of the models
Base = declarative_base()
