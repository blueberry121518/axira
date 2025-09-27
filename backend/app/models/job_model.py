"""
SQLAlchemy ORM model for job postings and recruitment requirements.
This model defines the database schema for storing job information.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Job(Base):
    """
    SQLAlchemy model representing a job posting for recruitment.
    Stores job details, requirements, and associated agent information.
    """
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    employment_type = Column(String(50), nullable=True)  # full-time, part-time, contract, etc.
    experience_level = Column(String(50), nullable=True)  # entry, mid, senior, executive
    
    # Job requirements
    required_skills = Column(Text, nullable=True)  # JSON string of required skills
    preferred_skills = Column(Text, nullable=True)  # JSON string of preferred skills
    education_requirements = Column(Text, nullable=True)
    years_experience = Column(Integer, nullable=True)
    
    # Job status and metadata
    status = Column(String(50), default="active", nullable=False)  # active, paused, closed, filled
    priority = Column(Integer, default=1, nullable=False)  # 1=low, 2=medium, 3=high
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    posted_at = Column(DateTime(timezone=True), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Contact information
    contact_email = Column(String(255), nullable=True)
    hiring_manager = Column(String(255), nullable=True)
    
    # Relationships
    agents = relationship("Agent", back_populates="job")


class Candidate(Base):
    """
    SQLAlchemy model for storing candidate information discovered by agents.
    Stores candidate profiles and their interaction history.
    """
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    
    # Candidate information
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    resume_url = Column(String(500), nullable=True)
    
    # Professional details
    current_title = Column(String(255), nullable=True)
    current_company = Column(String(255), nullable=True)
    years_experience = Column(Integer, nullable=True)
    skills = Column(Text, nullable=True)  # JSON string of skills
    education = Column(Text, nullable=True)  # JSON string of education history
    
    # Recruitment status
    status = Column(String(50), default="discovered", nullable=False)  # discovered, contacted, interested, not_interested, applied
    response_received = Column(Boolean, default=False)
    application_submitted = Column(Boolean, default=False)
    
    # Timestamps
    discovered_at = Column(DateTime(timezone=True), server_default=func.now())
    contacted_at = Column(DateTime(timezone=True), nullable=True)
    responded_at = Column(DateTime(timezone=True), nullable=True)
    
    # Notes and metadata
    notes = Column(Text, nullable=True)
    metadata = Column(Text, nullable=True)  # JSON string for additional data
    
    # Relationships
    job = relationship("Job")
    agent = relationship("Agent")
