"""
Unit tests for VoiceManager class.
"""

import pytest
import tempfile
import json
from unittest.mock import patch, mock_open
from voice_manager import VoiceManager


class TestVoiceManager:
    """Test cases for VoiceManager functionality."""

    def test_voice_manager_initialization(self, voice_manager):
        """Test that VoiceManager initializes correctly."""
        assert voice_manager is not None
        assert hasattr(voice_manager, 'voices_data')
        assert hasattr(voice_manager, 'voices_file')

    def test_get_voice_statistics(self, voice_manager):
        """Test voice statistics retrieval."""
        stats = voice_manager.get_voice_statistics()
        assert isinstance(stats, dict)
        assert 'spanish' in stats
        assert 'english' in stats
        assert isinstance(stats['spanish'], int)
        assert isinstance(stats['english'], int)

    def test_get_random_voice_for_language_english(self, voice_manager):
        """Test random voice selection for English."""
        voice = voice_manager.get_random_voice_for_language('en')
        assert voice is not None
        assert 'id' in voice
        assert 'name' in voice
        assert voice['name'].startswith('English')

    def test_get_random_voice_for_language_spanish(self, voice_manager):
        """Test random voice selection for Spanish."""
        voice = voice_manager.get_random_voice_for_language('es')
        assert voice is not None
        assert 'id' in voice
        assert 'name' in voice
        assert voice['name'].startswith('Spanish')

    def test_get_random_voice_invalid_language(self, voice_manager):
        """Test random voice selection for invalid language."""
        voice = voice_manager.get_random_voice_for_language('invalid')
        # Should default to English
        assert voice is not None
        assert voice['name'].startswith('English')

    def test_randomization_distribution(self, voice_manager):
        """Test that voice randomization has reasonable distribution."""
        selected_voices = []
        num_tests = 20
        
        for _ in range(num_tests):
            voice = voice_manager.get_random_voice_for_language('en')
            selected_voices.append(voice['id'])
        
        # Should have some variety (not all the same voice)
        unique_voices = set(selected_voices)
        assert len(unique_voices) > 1, "Should select different voices"

    def test_custom_voices_file(self, sample_voice_data):
        """Test VoiceManager with custom voices file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_voice_data, f)
            f.flush()
            
            vm = VoiceManager(voices_file=f.name)
            stats = vm.get_voice_statistics()
            
            assert stats['spanish'] == 2
            assert stats['english'] == 2
            
            voice_en = vm.get_random_voice_for_language('en')
            assert voice_en['id'] in ['test_voice_en_1', 'test_voice_en_2']

    @patch('builtins.open', mock_open(read_data='invalid json'))
    def test_invalid_json_handling(self):
        """Test handling of invalid JSON in voices file."""
        vm = VoiceManager()
        # Should not crash and should have empty data
        assert vm.voices_data == {"spanish": [], "english": []}

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_missing_file_handling(self, mock_open):
        """Test handling of missing voices file."""
        vm = VoiceManager()
        # Should not crash and should have empty data
        assert vm.voices_data == {"spanish": [], "english": []}

    def test_voice_id_from_env(self, voice_manager):
        """Test voice ID retrieval from environment variables."""
        with patch.dict('os.environ', {'ELEVENLABS_VOICES_EN': 'voice1,voice2,voice3'}):
            voice_id = voice_manager.get_voice_id_from_env('en')
            assert voice_id in ['voice1', 'voice2', 'voice3']

    def test_voice_id_from_env_missing(self, voice_manager):
        """Test voice ID retrieval when env var is missing."""
        with patch.dict('os.environ', {}, clear=True):
            voice_id = voice_manager.get_voice_id_from_env('nonexistent')
            assert voice_id is None
