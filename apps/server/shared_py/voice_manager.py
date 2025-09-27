"""
Voice Management Module for Time Traveler Agent.
Handles randomization and selection of ElevenLabs voice IDs based on language and era.
"""

import json
import os
import random
from typing import Dict, List, Optional, Any
from pathlib import Path


class VoiceManager:
    """Manages voice selection and randomization for the Time Traveler agent."""
    
    def __init__(self, voices_file: Optional[str] = None):
        """Initialize VoiceManager with voice configuration."""
        self.voices_file = voices_file or self._get_default_voices_file()
        self.voices_data = self._load_voices()
    
    def _get_default_voices_file(self) -> str:
        """Get the default path to voices.json."""
        current_dir = Path(__file__).parent
        voices_path = current_dir / "data" / "voices.json"
        return str(voices_path)
    
    def _load_voices(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load voice configuration from JSON file."""
        try:
            with open(self.voices_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Warning: Voice file not found at {self.voices_file}")
            return {"spanish": [], "english": []}
        except json.JSONDecodeError as e:
            print(f"⚠️ Warning: Invalid JSON in voice file: {e}")
            return {"spanish": [], "english": []}
    
    def get_voice_statistics(self) -> Dict[str, int]:
        """Get statistics about available voices."""
        stats = {}
        for lang, voices in self.voices_data.items():
            stats[lang] = len(voices)
        return stats
    
    def get_random_voice(self, language: str) -> Optional[Dict[str, Any]]:
        """Get a random voice for the specified language."""
        # Normalize language code
        lang_key = "spanish" if language.lower() in ["es", "spanish"] else "english"
        
        voices = self.voices_data.get(lang_key, [])
        if not voices:
            print(f"⚠️ Warning: No voices available for language: {language}")
            return None
        
        return random.choice(voices)
    
    def get_random_voice_for_language(self, language: str) -> Optional[Dict[str, Any]]:
        """Get a random voice for the specified language (era-agnostic)."""
        # Normalize language code  
        lang_key = "spanish" if language.lower() in ["es", "spanish"] else "english"
        
        voices = self.voices_data.get(lang_key, [])
        if not voices:
            print(f"⚠️ Warning: No voices available for language: {language}")
            return None
        
        selected_voice = random.choice(voices)
        # Enhanced logging with metadata
        gender = selected_voice.get('gender', 'unknown')
        age_range = selected_voice.get('age_range', 'unknown')
        print(f"🎤 Selected voice: {selected_voice['name']} (ID: {selected_voice['id'][:8]}...) - {gender} {age_range}")
        return selected_voice
    
    def get_voice_id_from_env(self, language: str) -> Optional[str]:
        """Get voice ID from environment variables as fallback."""
        env_var = f"ELEVENLABS_VOICES_{language.upper()}"
        voice_list_str = os.getenv(env_var)
        
        if voice_list_str:
            voice_ids = [vid.strip() for vid in voice_list_str.split(",")]
            if voice_ids:
                return random.choice(voice_ids)
        
        return None


def get_voice_override_from_env(language: str) -> Optional[str]:
    """Utility function to get voice ID from environment variables."""
    vm = VoiceManager()
    return vm.get_voice_id_from_env(language)
