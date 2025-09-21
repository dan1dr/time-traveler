"""
Agent Management Module for Time Traveler Agent.
Handles randomization and selection of ElevenLabs agent IDs based on era and personality.
"""

import json
import os
import random
from typing import Dict, List, Optional, Any
from pathlib import Path


class AgentManager:
    """Manages agent selection and randomization for the Time Traveler agent."""
    
    def __init__(self, agents_file: Optional[str] = None):
        """Initialize AgentManager with agent configuration."""
        self.agents_file = agents_file or self._get_default_agents_file()
        self.agents_data = self._load_agents()
    
    def _get_default_agents_file(self) -> str:
        """Get the default path to agents.json."""
        current_dir = Path(__file__).parent
        agents_path = current_dir / "data" / "agents.json"
        return str(agents_path)
    
    def _load_agents(self) -> List[Dict[str, Any]]:
        """Load agent configuration from JSON file."""
        try:
            with open(self.agents_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("agents", [])
        except FileNotFoundError:
            print(f"⚠️ Warning: Agent file not found at {self.agents_file}")
            return []
        except json.JSONDecodeError as e:
            print(f"⚠️ Warning: Invalid JSON in agent file: {e}")
            return []
    
    def get_agent_statistics(self) -> Dict[str, Any]:
        """Get statistics about available agents."""
        stats = {
            "total_agents": len(self.agents_data),
            "agent_names": [agent.get("name", "unknown") for agent in self.agents_data]
        }
        
        return stats
    
    def get_random_agent(self) -> Optional[Dict[str, Any]]:
        """Get a random agent from all available agents."""
        if not self.agents_data:
            print("⚠️ Warning: No agents available")
            return None
        
        return random.choice(self.agents_data)
    
    # Removed era_appropriate_agent - we now use simple randomization
    
    def get_agent_id(self, agent_config: Dict[str, Any]) -> Optional[str]:
        """Get the actual ElevenLabs agent ID from environment variables."""
        env_var = agent_config.get("env_var")
        if not env_var:
            print(f"⚠️ Warning: No env_var specified for agent: {agent_config.get('name')}")
            return None
        
        agent_id = os.getenv(env_var)
        if not agent_id:
            print(f"⚠️ Warning: Environment variable {env_var} not set")
            # Fallback to base agent ID
            fallback_id = os.getenv("ELEVENLABS_AGENT_ID")
            if fallback_id:
                print(f"🔄 Using fallback agent ID from ELEVENLABS_AGENT_ID")
            return fallback_id
        
        return agent_id
    
    def get_available_agent_ids(self) -> List[str]:
        """Get all available agent IDs from environment variables."""
        available_ids = []
        
        for agent in self.agents_data:
            env_var = agent.get("env_var")
            if env_var:
                agent_id = os.getenv(env_var)
                if agent_id:
                    available_ids.append(agent_id)
        
        # Also check for base agent
        base_agent = os.getenv("ELEVENLABS_AGENT_ID")
        if base_agent and base_agent not in available_ids:
            available_ids.append(base_agent)
        
        return available_ids
    
    def get_random_agent_id(self) -> Optional[str]:
        """Get a random agent ID from all available configured agents."""
        available_ids = self.get_available_agent_ids()
        
        if not available_ids:
            print("⚠️ Warning: No agent IDs configured in environment variables")
            return None
        
        selected_id = random.choice(available_ids)
        print(f"🎯 Randomly selected agent ID: {selected_id[:8]}...")
        return selected_id


def get_random_agent_from_env() -> Optional[str]:
    """Utility function to get a random agent ID from environment variables."""
    am = AgentManager()
    return am.get_random_agent_id()

def get_random_agent_config() -> Optional[Dict[str, Any]]:
    """Utility function to get a random agent configuration."""
    am = AgentManager()
    return am.get_random_agent()
