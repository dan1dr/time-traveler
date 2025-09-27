import json
import random
import os
from typing import Dict, List, Optional


class FirstMessageManager:
    def __init__(self, first_messages_file: str = None):
        """
        Initialize the FirstMessageManager with era-specific first messages.
        
        Args:
            first_messages_file: Path to the first messages JSON file
        """
        if first_messages_file is None:
            current_dir = os.path.dirname(__file__)
            first_messages_file = os.path.join(current_dir, "data", "first_messages.json")
        
        self.first_messages_file = first_messages_file
        self.first_messages = self._load_first_messages()
    
    def _load_first_messages(self) -> Dict:
        """Load first messages from JSON file."""
        try:
            with open(self.first_messages_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: First messages file not found at {self.first_messages_file}")
            return {}
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in first messages file: {self.first_messages_file}")
            return {}
    
    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about available first messages."""
        stats = {
            "total_eras": len(self.first_messages),
            "languages_per_era": {},
            "messages_per_era_language": {}
        }
        
        for era, languages in self.first_messages.items():
            stats["languages_per_era"][era] = len(languages)
            stats["messages_per_era_language"][era] = {}
            for lang, messages in languages.items():
                stats["messages_per_era_language"][era][lang] = len(messages)
        
        return stats
    
    def get_random_first_message(self, era_name: str, language: str) -> Optional[str]:
        """
        Get a random first message for the specified era and language.
        
        Args:
            era_name: The era identifier (e.g., 'medieval', 'renaissance')
            language: The language code (e.g., 'en', 'es')
            
        Returns:
            A random first message string, or None if not found
        """
        if era_name not in self.first_messages:
            print(f"Warning: Era '{era_name}' not found in first messages")
            return None
        
        era_messages = self.first_messages[era_name]
        if language not in era_messages:
            print(f"Warning: Language '{language}' not found for era '{era_name}'")
            return None
        
        messages = era_messages[language]
        if not messages:
            print(f"Warning: No messages found for era '{era_name}', language '{language}'")
            return None
        
        selected_message = random.choice(messages)
        print(f"💬 Selected first message: '{selected_message[:50]}...' for {era_name} ({language})")
        return selected_message
    
    def get_all_messages_for_era(self, era_name: str) -> Dict[str, List[str]]:
        """Get all first messages for a specific era in all languages."""
        return self.first_messages.get(era_name, {})
    
    def get_supported_eras(self) -> List[str]:
        """Get list of all supported era names."""
        return list(self.first_messages.keys())
    
    def get_supported_languages_for_era(self, era_name: str) -> List[str]:
        """Get list of supported languages for a specific era."""
        return list(self.first_messages.get(era_name, {}).keys())


# Example usage and testing
if __name__ == "__main__":
    # Test the FirstMessageManager
    manager = FirstMessageManager()
    
    print("📊 First Message Statistics:")
    stats = manager.get_statistics()
    print(f"Total eras: {stats['total_eras']}")
    
    # Test some random selections
    test_cases = [
        ("medieval", "en"),
        ("renaissance", "es"),
        ("digital", "en"),
        ("ai_renaissance", "es"),
        ("far_future", "en")
    ]
    
    print("\n🎲 Random First Message Examples:")
    for era, lang in test_cases:
        message = manager.get_random_first_message(era, lang)
        if message:
            print(f"{era} ({lang}): {message}")
