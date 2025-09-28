"""
Unit tests for era_config module.
"""

import pytest
from era_config import get_era_config, get_era_session_variables, ERA_CONFIGS


class TestEraConfig:
    """Test cases for era configuration functionality."""

    def test_era_configs_structure(self):
        """Test that ERA_CONFIGS has the expected structure."""
        assert isinstance(ERA_CONFIGS, dict)
        assert len(ERA_CONFIGS) > 0
        
        # Check that all entries have tuple keys and EraConfig values
        for key, config in ERA_CONFIGS.items():
            assert isinstance(key, tuple)
            assert len(key) == 2  # (start_year, end_year)
            assert key[0] <= key[1]  # start <= end
            assert hasattr(config, 'era_name')
            assert hasattr(config, 'expressions')
            assert hasattr(config, 'voice_settings')

    def test_get_era_config_valid_years(self):
        """Test era config retrieval for valid years."""
        # Test a few known eras
        medieval = get_era_config(1000)
        assert medieval is not None
        assert medieval.era_name == "early_medieval"
        
        renaissance = get_era_config(1500)
        assert renaissance is not None
        # 1500 is actually in the renaissance era (1400-1600)
        assert renaissance.era_name == "renaissance"
        
        contemporary = get_era_config(2020)
        assert contemporary is not None
        assert contemporary.era_name == "mobile_social_cloud"

    def test_get_era_config_edge_cases(self):
        """Test era config for edge cases."""
        # Very old year - should default to late_bronze_early_iron
        ancient = get_era_config(-1000)
        assert ancient is not None
        assert ancient.era_name == "late_bronze_early_iron"
        
        # Very far future - should default to far_future
        far_future = get_era_config(10000)
        assert far_future is not None
        assert far_future.era_name == "far_future"

    def test_get_era_config_boundary_years(self):
        """Test era config at year boundaries."""
        # Test some specific boundary years that should work clearly
        ancient = get_era_config(0)  # Start of classical antiquity era
        assert ancient.era_name == "classical_antiquity"
        
        medieval_mid = get_era_config(1000)  # Clearly in early_medieval
        assert medieval_mid.era_name == "early_medieval"
        
        renaissance_mid = get_era_config(1550)  # Clearly in renaissance  
        assert renaissance_mid.era_name == "renaissance"
        
        contemporary = get_era_config(2010)  # Clearly mobile_social_cloud
        assert contemporary.era_name == "mobile_social_cloud"

    def test_get_era_session_variables_structure(self):
        """Test structure of era session variables."""
        variables = get_era_session_variables(1350, "es")
        
        # Check required keys
        required_keys = [
            'era_year', 'language', 'language_name', 'era_name',
            'time_period', 'era_context', 'expression_1', 
            'expression_2', 'expression_3', 'voice_settings'
        ]
        
        for key in required_keys:
            assert key in variables, f"Missing required key: {key}"

    def test_get_era_session_variables_spanish(self):
        """Test era session variables for Spanish."""
        variables = get_era_session_variables(1350, "es")
        
        assert variables['language'] == "es"
        assert variables['language_name'] == "Spanish"
        assert variables['era_year'] == 1350
        assert variables['era_name'] == "late_medieval"
        
        # Check that expressions are in Spanish
        assert "En estos años convulsos" in variables['expression_1']

    def test_get_era_session_variables_english(self):
        """Test era session variables for English."""
        variables = get_era_session_variables(1580, "en")
        
        assert variables['language'] == "en"
        assert variables['language_name'] == "English"
        assert variables['era_year'] == 1580
        assert variables['era_name'] == "renaissance"
        
        # Check that expressions are in English
        assert "marvel" in variables['expression_1'].lower()

    def test_get_era_session_variables_fallback_language(self):
        """Test era session variables with unsupported language."""
        variables = get_era_session_variables(1350, "fr")  # French not supported
        
        assert variables['language'] == "fr"
        assert variables['language_name'] == "fr"  # Should pass through
        # Should get English expressions as fallback
        assert len(variables['expression_1']) > 0

    def test_voice_settings_structure(self):
        """Test that voice settings have required keys."""
        variables = get_era_session_variables(1350, "es")
        voice_settings = variables['voice_settings']
        
        required_voice_keys = ['stability', 'similarity_boost', 'style', 'speed']
        for key in required_voice_keys:
            assert key in voice_settings, f"Missing voice setting: {key}"
            assert isinstance(voice_settings[key], (int, float))

    def test_voice_speed_range(self):
        """Test that voice speed is within valid ElevenLabs range."""
        # Test various eras to ensure speed is within 0.7-1.2
        test_years = [100, 1000, 1500, 1800, 1950, 2000, 2080, 2300, 3000]
        
        for year in test_years:
            variables = get_era_session_variables(year, "en")
            speed = variables['voice_settings']['speed']
            assert 0.7 <= speed <= 1.2, f"Speed {speed} out of range for year {year}"

    def test_expressions_not_empty(self):
        """Test that expressions are not empty."""
        variables = get_era_session_variables(1350, "es")
        
        assert len(variables['expression_1']) > 0
        assert len(variables['expression_2']) > 0
        assert len(variables['expression_3']) > 0

    def test_different_eras_have_different_settings(self):
        """Test that different eras have different characteristics."""
        medieval = get_era_session_variables(1000, "en")
        modern = get_era_session_variables(2000, "en")
        future = get_era_session_variables(3000, "en")
        
        # Should have different era names
        assert medieval['era_name'] != modern['era_name']
        assert modern['era_name'] != future['era_name']
        
        # Should have different expressions
        assert medieval['expression_1'] != modern['expression_1']
        assert modern['expression_1'] != future['expression_1']
