"""
Database configuration and session management for the Autonomous Recruitment Platform.
This module sets up SQLAlchemy engine, sessionmaker, and database dependencies.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/recruitment_db")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()


def get_db() -> Session:
    """
    A FastAPI dependency that provides a database session for each request.
    Yields a database session and ensures it's properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables.
    This function can be called during application startup.
    """
    Base.metadata.create_all(bind=engine)
