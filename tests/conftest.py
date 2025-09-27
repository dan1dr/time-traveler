"""
Pytest configuration and fixtures for the time-traveler project.
"""

import sys
import os
from pathlib import Path

# Add packages to Python path for testing
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "packages" / "shared-py"))
sys.path.append(str(project_root / "apps" / "server"))

import pytest
from voice_manager import VoiceManager
from agent_manager import AgentManager


@pytest.fixture
def voice_manager():
    """Create a VoiceManager instance for testing."""
    return VoiceManager()


@pytest.fixture
def agent_manager():
    """Create an AgentManager instance for testing."""
    return AgentManager()


@pytest.fixture
def sample_voice_data():
    """Sample voice data for testing."""
    return {
        "spanish": [
            {"id": "test_voice_es_1", "name": "Test Spanish Voice 1"},
            {"id": "test_voice_es_2", "name": "Test Spanish Voice 2"}
        ],
        "english": [
            {"id": "test_voice_en_1", "name": "Test English Voice 1"},
            {"id": "test_voice_en_2", "name": "Test English Voice 2"}
        ]
    }


@pytest.fixture
def sample_agent_data():
    """Sample agent data for testing."""
    return {
        "agents": [
            {"name": "Test Agent 1", "env_var": "TEST_AGENT_1"},
            {"name": "Test Agent 2", "env_var": "TEST_AGENT_2"}
        ]
    }
