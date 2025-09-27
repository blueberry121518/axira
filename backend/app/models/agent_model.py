"""
SQLAlchemy ORM model for autonomous recruitment agents.
This model defines the database schema for storing agent information and status.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Agent(Base):
    """
    SQLAlchemy model representing an autonomous recruitment agent.
    Stores agent information, status, and configuration details.
    """
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    status = Column(String(50), default="inactive", nullable=False)  # inactive, active, deployed, stopped
    seed_phrase = Column(Text, nullable=True)  # For Fetch.ai agent identity
    agent_address = Column(String(255), nullable=True)  # Fetch.ai agent address
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deployed_at = Column(DateTime(timezone=True), nullable=True)
    stopped_at = Column(DateTime(timezone=True), nullable=True)
    
    # Configuration fields
    max_candidates = Column(Integer, default=100)
    search_criteria = Column(Text, nullable=True)  # JSON string for search parameters
    email_config = Column(Text, nullable=True)  # JSON string for AgentMail configuration
    
    # Relationship to job
    job = relationship("Job", back_populates="agents")


class AgentActivity(Base):
    """
    SQLAlchemy model for tracking agent activities and logs.
    Stores detailed information about agent operations and communications.
    """
    __tablename__ = "agent_activities"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    activity_type = Column(String(100), nullable=False)  # email_sent, candidate_found, error, etc.
    description = Column(Text, nullable=True)
    metadata = Column(Text, nullable=True)  # JSON string for additional data
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to agent
    agent = relationship("Agent")
