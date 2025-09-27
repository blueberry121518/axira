"""
Pydantic schemas for agent-related API requests and responses.
This module defines data validation and serialization models for agent operations.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class AgentStatus(str, Enum):
    """
    Enumeration of possible agent statuses.
    """
    INACTIVE = "inactive"
    ACTIVE = "active"
    DEPLOYED = "deployed"
    STOPPED = "stopped"
    ERROR = "error"


class AgentCreate(BaseModel):
    """
    Pydantic schema for creating a new agent.
    Validates input data when deploying a new recruitment agent.
    """
    name: str = Field(..., min_length=1, max_length=255, description="Unique name for the agent")
    job_id: Optional[int] = Field(None, description="ID of the job this agent will work on")
    max_candidates: int = Field(100, ge=1, le=1000, description="Maximum number of candidates to source")
    search_criteria: Optional[Dict[str, Any]] = Field(None, description="Search parameters for candidate sourcing")
    email_config: Optional[Dict[str, Any]] = Field(None, description="AgentMail configuration settings")
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Agent name cannot be empty')
        return v.strip()


class AgentUpdate(BaseModel):
    """
    Pydantic schema for updating an existing agent.
    Validates input data when modifying agent configuration.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[AgentStatus] = None
    max_candidates: Optional[int] = Field(None, ge=1, le=1000)
    search_criteria: Optional[Dict[str, Any]] = None
    email_config: Optional[Dict[str, Any]] = None


class AgentResponse(BaseModel):
    """
    Pydantic schema for agent response data.
    Serializes agent information for API responses.
    """
    id: int
    name: str
    status: AgentStatus
    seed_phrase: Optional[str] = None
    agent_address: Optional[str] = None
    job_id: Optional[int] = None
    max_candidates: int
    search_criteria: Optional[Dict[str, Any]] = None
    email_config: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deployed_at: Optional[datetime] = None
    stopped_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AgentListResponse(BaseModel):
    """
    Pydantic schema for paginated agent list responses.
    Provides pagination metadata along with agent data.
    """
    agents: List[AgentResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class AgentDeployRequest(BaseModel):
    """
    Pydantic schema for agent deployment requests.
    Validates job details when deploying a new agent.
    """
    job_id: int = Field(..., description="ID of the job to create agent for")
    agent_name: Optional[str] = Field(None, description="Custom name for the agent")
    max_candidates: int = Field(100, ge=1, le=1000, description="Maximum candidates to source")
    search_criteria: Optional[Dict[str, Any]] = Field(None, description="Custom search parameters")
    
    @validator('agent_name')
    def validate_agent_name(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Agent name cannot be empty if provided')
        return v.strip() if v else None


class AgentStatusResponse(BaseModel):
    """
    Pydantic schema for agent status check responses.
    Provides detailed status information about a specific agent.
    """
    id: int
    name: str
    status: AgentStatus
    agent_address: Optional[str] = None
    job_id: Optional[int] = None
    candidates_found: int = Field(0, description="Number of candidates discovered")
    emails_sent: int = Field(0, description="Number of emails sent")
    last_activity: Optional[datetime] = Field(None, description="Timestamp of last agent activity")
    created_at: datetime
    deployed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AgentActivityCreate(BaseModel):
    """
    Pydantic schema for creating agent activity logs.
    Validates activity data when logging agent operations.
    """
    agent_id: int
    activity_type: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentActivityResponse(BaseModel):
    """
    Pydantic schema for agent activity responses.
    Serializes activity log information for API responses.
    """
    id: int
    agent_id: int
    activity_type: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime
    
    class Config:
        from_attributes = True
