
"""
Agent Router AI Integration
Provides routing and orchestration for AI agents via Agent Router service
"""

import os
import requests
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class AgentRouterClient:
    """Client for Agent Router AI service"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.agentrouter.org"):
        """
        Initialize Agent Router client
        
        Args:
            api_key: Agent Router API key (from env AGENT_ROUTER_API_KEY if not provided)
            base_url: Base URL for Agent Router API
        """
        self.api_key = api_key or os.getenv("AGENT_ROUTER_API_KEY")
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })
    
    def route_request(self, 
                     task_type: str,
                     input_data: Dict[str, Any],
                     agents: Optional[List[str]] = None,
                     metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Route a request to appropriate agent(s)
        
        Args:
            task_type: Type of task (e.g., "image_to_music", "audio_transcription")
            input_data: Input data for the task
            agents: Optional list of preferred agents
            metadata: Additional metadata
            
        Returns:
            Response from Agent Router
        """
        payload = {
            "task_type": task_type,
            "input": input_data,
            "agents": agents or [],
            "metadata": metadata or {}
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/v1/route",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Agent Router request failed: {e}")
            return {"error": str(e), "success": False}
    
    def register_agent(self, 
                       agent_name: str,
                       capabilities: List[str],
                       metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Register an agent with Agent Router
        
        Args:
            agent_name: Name of the agent
            capabilities: List of capabilities
            metadata: Additional agent metadata
            
        Returns:
            Registration response
        """
        payload = {
            "name": agent_name,
            "capabilities": capabilities,
            "metadata": metadata or {}
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/v1/agents/register",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Agent registration failed: {e}")
            return {"error": str(e), "success": False}
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get status of a specific agent"""
        try:
            response = self.session.get(
                f"{self.base_url}/v1/agents/{agent_id}/status",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get agent status: {e}")
            return {"error": str(e), "success": False}
    
    def list_available_agents(self, capability: Optional[str] = None) -> Dict[str, Any]:
        """List all available agents, optionally filtered by capability"""
        try:
            params = {"capability": capability} if capability else {}
            response = self.session.get(
                f"{self.base_url}/v1/agents",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to list agents: {e}")
            return {"error": str(e), "success": False}
