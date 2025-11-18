"""
Bot Configuration
Configuration management for Instagram Neural Bot
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass
class BotConfig:
    """Bot configuration settings"""

    # Device settings
    device_id: str = ""
    emulator_type: str = "BlueStacks"
    auto_start_emulator: bool = True

    # Instagram account
    username: str = ""

    # Action limits (per session)
    max_likes_per_session: int = 50
    max_follows_per_session: int = 30
    max_comments_per_session: int = 10
    max_unfollows_per_session: int = 40

    # Behavior settings
    like_probability: float = 0.7
    follow_probability: float = 0.3
    comment_probability: float = 0.1

    # Timing settings (in seconds)
    min_action_delay: float = 2.0
    max_action_delay: float = 8.0
    session_duration_minutes: int = 30

    # Targets
    target_hashtags: List[str] = None
    target_users: List[str] = None
    target_locations: List[str] = None

    # Comments
    comment_templates: List[str] = None

    # Advanced settings
    use_neural_timing: bool = True
    enable_stories: bool = True
    enable_reels: bool = False

    def __post_init__(self):
        """Initialize default values for lists"""
        if self.target_hashtags is None:
            self.target_hashtags = []
        if self.target_users is None:
            self.target_users = []
        if self.target_locations is None:
            self.target_locations = []
        if self.comment_templates is None:
            self.comment_templates = [
                "Nice! 🔥",
                "Love this! ❤️",
                "Amazing! 😍",
                "Great post! 👍",
                "Awesome content! ✨"
            ]

    def save(self, filepath: str):
        """Save configuration to JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(asdict(self), f, indent=4)

    @classmethod
    def load(cls, filepath: str) -> 'BotConfig':
        """Load configuration from JSON file"""
        if not os.path.exists(filepath):
            # Return default config
            return cls()

        with open(filepath, 'r') as f:
            data = json.load(f)

        return cls(**data)

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'BotConfig':
        """Create from dictionary"""
        return cls(**data)


if __name__ == '__main__':
    # Test config
    config = BotConfig(
        username="test_user",
        target_hashtags=["fitness", "motivation"],
        max_likes_per_session=100
    )

    print("Configuration:")
    print(json.dumps(config.to_dict(), indent=2))
