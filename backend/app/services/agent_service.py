"""
Agent service layer for managing autonomous recruitment agents.
This module contains business logic for agent deployment, management, and monitoring.
"""

import subprocess
import json
import asyncio
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from app.models.agent_model import Agent, AgentActivity
from app.models.job_model import Job, Candidate
from app.schemas.agent_schema import AgentCreate, AgentUpdate, AgentStatus
from datetime import datetime
import uuid
import os


class AgentService:
    """
    Service class for managing autonomous recruitment agents.
    Handles agent deployment, status monitoring, and lifecycle management.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the agent service with a database session.
        """
        self.db = db
    
    async def deploy_new_agent(self, job_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deploy a new autonomous recruitment agent for a specific job.
        Creates agent record, generates seed phrase, and starts agent process.
        
        Args:
            job_details: Dictionary containing job information and agent configuration
            
        Returns:
            Dictionary with deployment status and agent information
        """
        try:
            # Create agent record in database
            agent = Agent(
                name=job_details.get('agent_name', f"Agent_{uuid.uuid4().hex[:8]}"),
                status=AgentStatus.INACTIVE,
                job_id=job_details.get('job_id'),
                max_candidates=job_details.get('max_candidates', 100),
                search_criteria=json.dumps(job_details.get('search_criteria', {})),
                email_config=json.dumps(job_details.get('email_config', {}))
            )
            
            self.db.add(agent)
            self.db.commit()
            self.db.refresh(agent)
            
            # Generate seed phrase for Fetch.ai agent
            seed_phrase = self._generate_seed_phrase()
            agent.seed_phrase = seed_phrase
            
            # Start agent process
            agent_process = await self._start_agent_process(agent.id, seed_phrase, job_details)
            
            # Update agent status
            agent.status = AgentStatus.DEPLOYED
            agent.deployed_at = datetime.utcnow()
            self.db.commit()
            
            # Log activity
            await self._log_agent_activity(
                agent.id, 
                "deployed", 
                f"Agent {agent.name} deployed successfully",
                {"process_id": agent_process.pid if agent_process else None}
            )
            
            return {
                "success": True,
                "agent_id": agent.id,
                "agent_name": agent.name,
                "status": agent.status,
                "seed_phrase": seed_phrase,
                "deployed_at": agent.deployed_at.isoformat()
            }
            
        except Exception as e:
            # Update agent status to error if deployment fails
            if 'agent' in locals():
                agent.status = AgentStatus.ERROR
                self.db.commit()
                await self._log_agent_activity(agent.id, "error", f"Deployment failed: {str(e)}")
            
            return {
                "success": False,
                "error": str(e),
                "agent_id": agent.id if 'agent' in locals() else None
            }
    
    async def get_agent_status(self, agent_id: int) -> Dict[str, Any]:
        """
        Get the current status and activity summary of an agent.
        
        Args:
            agent_id: ID of the agent to check
            
        Returns:
            Dictionary with agent status and activity metrics
        """
        try:
            agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent:
                return {"success": False, "error": "Agent not found"}
            
            # Get activity counts
            candidates_count = self.db.query(Candidate).filter(Candidate.agent_id == agent_id).count()
            emails_sent = self.db.query(AgentActivity).filter(
                AgentActivity.agent_id == agent_id,
                AgentActivity.activity_type == "email_sent"
            ).count()
            
            # Get last activity
            last_activity = self.db.query(AgentActivity).filter(
                AgentActivity.agent_id == agent_id
            ).order_by(AgentActivity.timestamp.desc()).first()
            
            return {
                "success": True,
                "agent_id": agent.id,
                "name": agent.name,
                "status": agent.status,
                "agent_address": agent.agent_address,
                "job_id": agent.job_id,
                "candidates_found": candidates_count,
                "emails_sent": emails_sent,
                "last_activity": last_activity.timestamp if last_activity else None,
                "created_at": agent.created_at.isoformat(),
                "deployed_at": agent.deployed_at.isoformat() if agent.deployed_at else None
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def stop_agent(self, agent_id: int) -> Dict[str, Any]:
        """
        Stop a running agent and update its status.
        
        Args:
            agent_id: ID of the agent to stop
            
        Returns:
            Dictionary with stop operation result
        """
        try:
            agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent:
                return {"success": False, "error": "Agent not found"}
            
            # TODO: Implement actual process termination logic
            # This would involve finding and killing the agent process
            
            agent.status = AgentStatus.STOPPED
            agent.stopped_at = datetime.utcnow()
            self.db.commit()
            
            await self._log_agent_activity(agent.id, "stopped", f"Agent {agent.name} stopped by user")
            
            return {
                "success": True,
                "agent_id": agent.id,
                "status": agent.status,
                "stopped_at": agent.stopped_at.isoformat()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def list_agents(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        List all agents with pagination.
        
        Args:
            page: Page number for pagination
            page_size: Number of agents per page
            
        Returns:
            Dictionary with paginated agent list
        """
        try:
            offset = (page - 1) * page_size
            
            agents = self.db.query(Agent).offset(offset).limit(page_size).all()
            total = self.db.query(Agent).count()
            
            agent_list = []
            for agent in agents:
                agent_data = {
                    "id": agent.id,
                    "name": agent.name,
                    "status": agent.status,
                    "job_id": agent.job_id,
                    "created_at": agent.created_at.isoformat(),
                    "deployed_at": agent.deployed_at.isoformat() if agent.deployed_at else None
                }
                agent_list.append(agent_data)
            
            total_pages = (total + page_size - 1) // page_size
            
            return {
                "success": True,
                "agents": agent_list,
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_seed_phrase(self) -> str:
        """
        Generate a seed phrase for Fetch.ai agent identity.
        In a real implementation, this would generate a proper mnemonic.
        """
        # TODO: Implement proper seed phrase generation using Fetch.ai libraries
        return f"seed_phrase_{uuid.uuid4().hex}"
    
    async def _start_agent_process(self, agent_id: int, seed_phrase: str, job_details: Dict[str, Any]) -> Optional[subprocess.Popen]:
        """
        Start the agent process as a subprocess.
        This is where the logic to run the agent script as a subprocess will be implemented.
        
        Args:
            agent_id: ID of the agent
            seed_phrase: Seed phrase for agent identity
            job_details: Job configuration details
            
        Returns:
            Process object if successful, None otherwise
        """
        try:
            # TODO: Implement actual agent process startup
            # This would involve:
            # 1. Creating a temporary configuration file with agent settings
            # 2. Starting the sourcing_agent.py script as a subprocess
            # 3. Passing the seed phrase and job details as arguments or environment variables
            
            # Placeholder implementation
            print(f"Starting agent process for agent_id={agent_id}, seed_phrase={seed_phrase}")
            print(f"Job details: {job_details}")
            
            # Example of how this might work:
            # agent_script_path = os.path.join(os.path.dirname(__file__), "../../agents/sourcing_agent.py")
            # process = subprocess.Popen([
            #     "python", agent_script_path,
            #     "--agent-id", str(agent_id),
            #     "--seed-phrase", seed_phrase,
            #     "--job-details", json.dumps(job_details)
            # ])
            # return process
            
            return None
            
        except Exception as e:
            print(f"Error starting agent process: {e}")
            return None
    
    async def _log_agent_activity(self, agent_id: int, activity_type: str, description: str, metadata: Optional[Dict] = None):
        """
        Log agent activity to the database.
        
        Args:
            agent_id: ID of the agent
            activity_type: Type of activity
            description: Description of the activity
            metadata: Additional metadata as dictionary
        """
        try:
            activity = AgentActivity(
                agent_id=agent_id,
                activity_type=activity_type,
                description=description,
                metadata=json.dumps(metadata) if metadata else None
            )
            self.db.add(activity)
            self.db.commit()
        except Exception as e:
            print(f"Error logging agent activity: {e}")
