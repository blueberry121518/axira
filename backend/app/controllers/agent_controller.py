"""
Agent controller for handling HTTP requests related to agent management.
This module contains the controller logic that interfaces between the API routes and the service layer.
"""

from typing import Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.services.agent_service import AgentService
from app.schemas.agent_schema import (
    AgentDeployRequest, 
    AgentStatusResponse, 
    AgentListResponse,
    AgentCreate,
    AgentUpdate
)


class AgentController:
    """
    Controller class for managing agent-related HTTP requests.
    Handles request validation, calls appropriate services, and formats responses.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the agent controller with a database session.
        """
        self.db = db
        self.agent_service = AgentService(db)
    
    async def create_agent(self, job_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create and deploy a new autonomous recruitment agent.
        
        Args:
            job_details: Dictionary containing job information and agent configuration
            
        Returns:
            Dictionary with agent creation result
            
        Raises:
            HTTPException: If agent creation fails
        """
        try:
            result = await self.agent_service.deploy_new_agent(job_details)
            
            if not result.get("success", False):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to deploy agent: {result.get('error', 'Unknown error')}"
                )
            
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error during agent creation: {str(e)}"
            )
    
    async def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """
        Get the current status and activity summary of a specific agent.
        
        Args:
            agent_id: ID of the agent to check (as string from URL parameter)
            
        Returns:
            Dictionary with agent status information
            
        Raises:
            HTTPException: If agent is not found or status retrieval fails
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
            
            result = await self.agent_service.get_agent_status(agent_id_int)
            
            if not result.get("success", False):
                if "not found" in result.get("error", "").lower():
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Agent with ID {agent_id} not found"
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Failed to get agent status: {result.get('error', 'Unknown error')}"
                    )
            
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error during status retrieval: {str(e)}"
            )
    
    async def list_agents(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        List all agents with pagination support.
        
        Args:
            page: Page number for pagination (default: 1)
            page_size: Number of agents per page (default: 10)
            
        Returns:
            Dictionary with paginated agent list
            
        Raises:
            HTTPException: If agent listing fails
        """
        try:
            # Validate pagination parameters
            if page < 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Page number must be greater than 0"
                )
            
            if page_size < 1 or page_size > 100:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Page size must be between 1 and 100"
                )
            
            result = await self.agent_service.list_agents(page, page_size)
            
            if not result.get("success", False):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to list agents: {result.get('error', 'Unknown error')}"
                )
            
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error during agent listing: {str(e)}"
            )
    
    async def stop_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Stop a running agent.
        
        Args:
            agent_id: ID of the agent to stop (as string from URL parameter)
            
        Returns:
            Dictionary with stop operation result
            
        Raises:
            HTTPException: If agent is not found or stop operation fails
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
            
            result = await self.agent_service.stop_agent(agent_id_int)
            
            if not result.get("success", False):
                if "not found" in result.get("error", "").lower():
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Agent with ID {agent_id} not found"
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Failed to stop agent: {result.get('error', 'Unknown error')}"
                    )
            
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error during agent stop: {str(e)}"
            )
    
    async def create_agent_from_schema(self, agent_data: AgentCreate) -> Dict[str, Any]:
        """
        Create a new agent using Pydantic schema validation.
        
        Args:
            agent_data: Validated agent creation data from request body
            
        Returns:
            Dictionary with agent creation result
            
        Raises:
            HTTPException: If agent creation fails
        """
        try:
            # Convert Pydantic model to dictionary
            job_details = {
                "agent_name": agent_data.name,
                "job_id": agent_data.job_id,
                "max_candidates": agent_data.max_candidates,
                "search_criteria": agent_data.search_criteria,
                "email_config": agent_data.email_config
            }
            
            return await self.create_agent(job_details)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error during agent creation: {str(e)}"
            )
    
    async def update_agent(self, agent_id: str, agent_data: AgentUpdate) -> Dict[str, Any]:
        """
        Update an existing agent's configuration.
        
        Args:
            agent_id: ID of the agent to update (as string from URL parameter)
            agent_data: Validated agent update data from request body
            
        Returns:
            Dictionary with update operation result
            
        Raises:
            HTTPException: If agent is not found or update fails
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
            
            # TODO: Implement agent update logic in AgentService
            # This would involve updating agent configuration and restarting if necessary
            
            # Placeholder implementation
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Agent update functionality is not yet implemented"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error during agent update: {str(e)}"
            )
