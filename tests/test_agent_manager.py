"""
Unit tests for AgentManager class.
"""

import pytest
import tempfile
import json
import os
from unittest.mock import patch, mock_open
from agent_manager import AgentManager


class TestAgentManager:
    """Test cases for AgentManager functionality."""

    def test_agent_manager_initialization(self, agent_manager):
        """Test that AgentManager initializes correctly."""
        assert agent_manager is not None
        assert hasattr(agent_manager, 'agents_data')
        assert hasattr(agent_manager, 'agents_file')

    def test_get_agent_statistics(self, agent_manager):
        """Test agent statistics retrieval."""
        stats = agent_manager.get_agent_statistics()
        assert isinstance(stats, dict)
        assert 'total_agents' in stats
        assert 'agent_names' in stats
        assert isinstance(stats['total_agents'], int)
        assert isinstance(stats['agent_names'], list)
        assert stats['total_agents'] == len(stats['agent_names'])

    def test_get_random_agent(self, agent_manager):
        """Test random agent selection."""
        agent = agent_manager.get_random_agent()
        assert agent is not None
        assert 'name' in agent
        assert 'env_var' in agent
        assert agent['name'].startswith('Time Traveler')

    def test_randomization_distribution(self, agent_manager):
        """Test that agent randomization has reasonable distribution."""
        selected_agents = []
        num_tests = 20
        
        for _ in range(num_tests):
            agent = agent_manager.get_random_agent()
            selected_agents.append(agent['name'])
        
        # Should have some variety (not all the same agent)
        unique_agents = set(selected_agents)
        assert len(unique_agents) > 1, "Should select different agents"

    def test_get_agent_id_with_env_var(self, agent_manager):
        """Test getting agent ID from environment variable."""
        test_agent = {"name": "Test Agent", "env_var": "TEST_AGENT_ID"}
        
        with patch.dict('os.environ', {'TEST_AGENT_ID': 'agent_12345'}):
            agent_id = agent_manager.get_agent_id(test_agent)
            assert agent_id == 'agent_12345'

    def test_get_agent_id_missing_env_var(self, agent_manager):
        """Test getting agent ID when environment variable is missing."""
        test_agent = {"name": "Test Agent", "env_var": "MISSING_AGENT_ID"}
        
        with patch.dict('os.environ', {'ELEVENLABS_AGENT_ID': 'fallback_agent'}, clear=True):
            agent_id = agent_manager.get_agent_id(test_agent)
            assert agent_id == 'fallback_agent'

    def test_get_agent_id_no_env_var_key(self, agent_manager):
        """Test getting agent ID when agent config has no env_var."""
        test_agent = {"name": "Test Agent"}  # No env_var key
        
        agent_id = agent_manager.get_agent_id(test_agent)
        assert agent_id is None

    def test_get_available_agent_ids(self, agent_manager):
        """Test getting all available agent IDs from environment."""
        env_vars = {
            'ELEVENLABS_AGENT_ID': 'base_agent',
            'ELEVENLABS_AGENT_ID_ALT_1': 'scholar_agent',
            'ELEVENLABS_AGENT_ID_ALT_2': 'adventurer_agent'
        }
        
        with patch.dict('os.environ', env_vars):
            agent_ids = agent_manager.get_available_agent_ids()
            # Should include all configured agents
            assert len(agent_ids) >= 3
            assert 'base_agent' in agent_ids

    def test_get_random_agent_id(self, agent_manager):
        """Test random agent ID selection from environment."""
        env_vars = {
            'ELEVENLABS_AGENT_ID': 'base_agent',
            'ELEVENLABS_AGENT_ID_ALT_1': 'scholar_agent'
        }
        
        with patch.dict('os.environ', env_vars):
            agent_id = agent_manager.get_random_agent_id()
            assert agent_id in ['base_agent', 'scholar_agent']

    def test_get_random_agent_id_no_env_vars(self, agent_manager):
        """Test random agent ID when no environment variables are set."""
        with patch.dict('os.environ', {}, clear=True):
            agent_id = agent_manager.get_random_agent_id()
            assert agent_id is None

    def test_custom_agents_file(self, sample_agent_data):
        """Test AgentManager with custom agents file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_agent_data, f)
            f.flush()
            
            am = AgentManager(agents_file=f.name)
            stats = am.get_agent_statistics()
            
            assert stats['total_agents'] == 2
            assert 'Test Agent 1' in stats['agent_names']
            assert 'Test Agent 2' in stats['agent_names']

    @patch('builtins.open', mock_open(read_data='invalid json'))
    def test_invalid_json_handling(self):
        """Test handling of invalid JSON in agents file."""
        am = AgentManager()
        # Should not crash and should have empty data
        assert am.agents_data == []

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_missing_file_handling(self, mock_open):
        """Test handling of missing agents file."""
        am = AgentManager()
        # Should not crash and should have empty data
        assert am.agents_data == []

    def test_empty_agents_list(self, agent_manager):
        """Test behavior when agents list is empty."""
        # Mock empty agents data
        agent_manager.agents_data = []
        
        agent = agent_manager.get_random_agent()
        assert agent is None
        
        stats = agent_manager.get_agent_statistics()
        assert stats['total_agents'] == 0
        assert stats['agent_names'] == []
