"""
FastAPI routes for agent management endpoints.
This module defines the REST API endpoints for managing autonomous recruitment agents.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.database import get_db
from app.controllers.agent_controller import AgentController
from app.schemas.agent_schema import (
    AgentDeployRequest, 
    AgentStatusResponse, 
    AgentListResponse,
    AgentCreate,
    AgentUpdate
)

# Create router instance
router = APIRouter()


@router.post("/agents/deploy", response_model=Dict[str, Any])
async def deploy_agent(
    deploy_request: AgentDeployRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Deploy a new autonomous recruitment agent for a specific job.
    
    This endpoint creates and starts a new Fetch.ai agent that will handle
    candidate sourcing and outreach for the specified job posting.
    
    Args:
        deploy_request: Job details and agent configuration
        db: Database session dependency
        
    Returns:
        Dictionary with deployment status and agent information
        
    Raises:
        HTTPException: If deployment fails or validation errors occur
    """
    controller = AgentController(db)
    
    # Convert Pydantic model to dictionary for service layer
    job_details = {
        "agent_name": deploy_request.agent_name,
        "job_id": deploy_request.job_id,
        "max_candidates": deploy_request.max_candidates,
        "search_criteria": deploy_request.search_criteria,
        "email_config": None  # Will be configured by the agent service
    }
    
    return await controller.create_agent(job_details)


@router.post("/agents", response_model=Dict[str, Any])
async def create_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Create a new agent with full configuration options.
    
    This endpoint allows creating an agent with comprehensive configuration
    including search criteria and email settings.
    
    Args:
        agent_data: Complete agent configuration data
        db: Database session dependency
        
    Returns:
        Dictionary with agent creation result
    """
    controller = AgentController(db)
    return await controller.create_agent_from_schema(agent_data)


@router.get("/agents/{agent_id}/status", response_model=Dict[str, Any])
async def get_agent_status(
    agent_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get the current status and activity summary of a specific agent.
    
    Returns detailed information about the agent's current state, including
    candidates found, emails sent, and last activity timestamp.
    
    Args:
        agent_id: Unique identifier of the agent
        db: Database session dependency
        
    Returns:
        Dictionary with agent status and activity metrics
    """
    controller = AgentController(db)
    return await controller.get_agent_status(agent_id)


@router.get("/agents", response_model=Dict[str, Any])
async def list_agents(
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Number of agents per page"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    List all agents with pagination support.
    
    Returns a paginated list of all agents in the system with their
    basic information and current status.
    
    Args:
        page: Page number for pagination (minimum: 1)
        page_size: Number of agents per page (1-100)
        db: Database session dependency
        
    Returns:
        Dictionary with paginated agent list and metadata
    """
    controller = AgentController(db)
    return await controller.list_agents(page, page_size)


@router.put("/agents/{agent_id}", response_model=Dict[str, Any])
async def update_agent(
    agent_id: str,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Update an existing agent's configuration.
    
    Allows modification of agent settings such as name, search criteria,
    and email configuration. The agent may need to be restarted for
    changes to take effect.
    
    Args:
        agent_id: Unique identifier of the agent to update
        agent_data: Updated agent configuration
        db: Database session dependency
        
    Returns:
        Dictionary with update operation result
    """
    controller = AgentController(db)
    return await controller.update_agent(agent_id, agent_data)


@router.delete("/agents/{agent_id}/stop", response_model=Dict[str, Any])
async def stop_agent(
    agent_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Stop a running agent and update its status.
    
    Gracefully stops the agent process and updates its status to 'stopped'.
    This operation is irreversible and the agent will need to be redeployed
    to resume operations.
    
    Args:
        agent_id: Unique identifier of the agent to stop
        db: Database session dependency
        
    Returns:
        Dictionary with stop operation result
    """
    controller = AgentController(db)
    return await controller.stop_agent(agent_id)


@router.get("/agents/{agent_id}/activities", response_model=Dict[str, Any])
async def get_agent_activities(
    agent_id: str,
    limit: int = Query(50, ge=1, le=200, description="Maximum number of activities to return"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get the activity log for a specific agent.
    
    Returns a list of recent activities performed by the agent, including
    emails sent, candidates found, errors encountered, etc.
    
    Args:
        agent_id: Unique identifier of the agent
        limit: Maximum number of activities to return (1-200)
        db: Database session dependency
        
    Returns:
        Dictionary with agent activity log
        
    Raises:
        HTTPException: If agent is not found
    """
    try:
        # Convert string agent_id to integer
        try:
            agent_id_int = int(agent_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid agent ID format. Must be a number."
            )
        
        # TODO: Implement activity retrieval in AgentService
        # This would query the AgentActivity model for the specified agent
        
        return {
            "success": True,
            "agent_id": agent_id_int,
            "activities": [],
            "total": 0,
            "message": "Activity retrieval not yet implemented"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error retrieving agent activities: {str(e)}"
        )


@router.get("/agents/{agent_id}/candidates", response_model=Dict[str, Any])
async def get_agent_candidates(
    agent_id: str,
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Number of candidates per page"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get candidates discovered by a specific agent.
    
    Returns a paginated list of candidates that have been found and
    potentially contacted by the specified agent.
    
    Args:
        agent_id: Unique identifier of the agent
        page: Page number for pagination (minimum: 1)
        page_size: Number of candidates per page (1-100)
        db: Database session dependency
        
    Returns:
        Dictionary with paginated candidate list
        
    Raises:
        HTTPException: If agent is not found
    """
    try:
        # Convert string agent_id to integer
        try:
            agent_id_int = int(agent_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid agent ID format. Must be a number."
            )
        
        # TODO: Implement candidate retrieval in AgentService
        # This would query the Candidate model filtered by agent_id
        
        return {
            "success": True,
            "agent_id": agent_id_int,
            "candidates": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
            "total_pages": 0,
            "message": "Candidate retrieval not yet implemented"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error retrieving agent candidates: {str(e)}"
        )
