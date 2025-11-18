"""
Timing Pattern Generator using Neural Networks
Models human-like timing for actions, reading, and pauses
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Dict, Any
import os


class TimingNetwork(nn.Module):
    """
    Neural network for predicting human-like timing delays
    Based on action type, context, and previous actions
    """

    def __init__(self, input_size=10, hidden_size=64):
        super(TimingNetwork, self).__init__()

        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Linear(32, 3)  # Output: (mean_delay, std_delay, reading_factor)
        )

    def forward(self, x):
        return self.network(x)


class TimingPatternGenerator:
    """
    Generates human-like timing patterns for bot actions
    Models reading time, pause durations, and action delays
    """

    def __init__(self, model_path=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = TimingNetwork(input_size=10, hidden_size=64).to(self.device)
        self.model.eval()

        # Action type encodings
        self.action_types = {
            'tap': 0,
            'double_tap': 1,
            'swipe': 2,
            'scroll': 3,
            'read': 4,
            'watch': 5,
            'type': 6,
            'navigate': 7
        }

        # Base timing profiles (milliseconds) - human research-based
        self.base_timings = {
            'tap': {'mean': 150, 'std': 50, 'min': 80, 'max': 300},
            'double_tap': {'mean': 200, 'std': 60, 'min': 120, 'max': 400},
            'swipe': {'mean': 300, 'std': 80, 'min': 200, 'max': 600},
            'scroll': {'mean': 350, 'std': 100, 'min': 200, 'max': 700},
            'read_short': {'mean': 1500, 'std': 400, 'min': 800, 'max': 3000},
            'read_medium': {'mean': 3000, 'std': 800, 'min': 1500, 'max': 6000},
            'read_long': {'mean': 5000, 'std': 1200, 'min': 2500, 'max': 10000},
            'watch_video': {'mean': 8000, 'std': 3000, 'min': 3000, 'max': 20000},
            'type_char': {'mean': 180, 'std': 60, 'min': 100, 'max': 400},
            'between_actions': {'mean': 500, 'std': 200, 'min': 200, 'max': 1500},
            'think_pause': {'mean': 2000, 'std': 800, 'min': 800, 'max': 5000},
            'navigation': {'mean': 400, 'std': 150, 'min': 200, 'max': 800}
        }

        if model_path and os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        else:
            self._initialize_with_human_patterns()

        # State tracking for context-aware timing
        self.action_history = []
        self.last_action_time = 0
        self.fatigue_factor = 1.0  # Increases over time to simulate user fatigue

    def _initialize_with_human_patterns(self):
        """Initialize with human timing patterns"""
        # Generate synthetic training data based on human behavior research
        training_data = []
        targets = []

        for _ in range(1000):
            # Random action type
            action_type = np.random.randint(0, 8)

            # Context features
            time_of_day = np.random.uniform(0, 24)  # Hour of day
            session_duration = np.random.uniform(0, 60)  # Minutes into session
            actions_count = np.random.randint(0, 100)  # Number of actions so far
            fatigue = min(session_duration / 30, 1.5)  # Fatigue increases with time

            # Create input vector
            input_vec = [
                action_type / 7,  # Normalized action type
                time_of_day / 24,
                session_duration / 60,
                actions_count / 100,
                fatigue,
                np.random.uniform(0, 1),  # Random factor 1
                np.random.uniform(0, 1),  # Random factor 2
                np.random.uniform(0, 1),  # Random factor 3
                np.random.uniform(0, 1),  # Engagement level
                np.random.uniform(0, 1)   # Interest level
            ]

            # Generate target timing (normalized)
            base_delay = np.random.uniform(200, 800)
            std_delay = np.random.uniform(50, 200)
            reading_factor = np.random.uniform(0.5, 2.0)

            target = [base_delay / 1000, std_delay / 1000, reading_factor]

            training_data.append(input_vec)
            targets.append(target)

        # Quick training
        self._train_model(training_data, targets, epochs=30)

    def _train_model(self, data, targets, epochs=30):
        """Train the timing model"""
        self.model.train()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        criterion = nn.MSELoss()

        data_tensor = torch.FloatTensor(data).to(self.device)
        target_tensor = torch.FloatTensor(targets).to(self.device)

        for epoch in range(epochs):
            optimizer.zero_grad()
            output = self.model(data_tensor)
            loss = criterion(output, target_tensor)
            loss.backward()
            optimizer.step()

        self.model.eval()

    def get_delay(self, action_type: str, context: Dict[str, Any] = None) -> float:
        """
        Get a human-like delay for an action

        Args:
            action_type: Type of action ('tap', 'swipe', 'read_short', etc.)
            context: Optional context information (text_length, complexity, etc.)

        Returns:
            Delay in seconds (float)
        """
        if context is None:
            context = {}

        # Get base timing
        base_timing = self.base_timings.get(action_type, self.base_timings['between_actions'])

        # Generate delay with Gaussian distribution
        delay_ms = np.random.normal(base_timing['mean'], base_timing['std'])

        # Clip to min/max
        delay_ms = np.clip(delay_ms, base_timing['min'], base_timing['max'])

        # Apply context modifications
        if 'text_length' in context and 'read' in action_type:
            # Adjust reading time based on text length
            # Average reading speed: 200-250 words per minute
            words = context['text_length'] / 5  # Approximate words
            reading_time_ms = (words / 200) * 60 * 1000  # Convert to ms
            delay_ms = max(delay_ms, reading_time_ms * np.random.uniform(0.7, 1.3))

        if 'complexity' in context:
            # More complex actions take longer
            complexity = context['complexity']  # 0-1 scale
            delay_ms *= (1.0 + complexity * 0.5)

        # Apply fatigue factor (actions get slower over time)
        delay_ms *= self.fatigue_factor

        # Add micro-variations (humans are never perfectly consistent)
        delay_ms *= np.random.uniform(0.95, 1.05)

        # Track action for context
        self._update_state(action_type, delay_ms)

        return delay_ms / 1000  # Return in seconds

    def get_reading_time(self, text_length: int, has_images: bool = False,
                        engagement_level: float = 0.5) -> float:
        """
        Calculate realistic reading time for content

        Args:
            text_length: Number of characters to read
            has_images: Whether content has images (adds viewing time)
            engagement_level: 0-1, how engaged the user is (affects reading speed)

        Returns:
            Reading time in seconds
        """
        # Words per minute based on engagement
        wpm = 200 + (engagement_level * 50)  # 200-250 WPM

        # Estimate words (average 5 chars per word)
        words = max(1, text_length / 5)

        # Calculate reading time
        reading_time = (words / wpm) * 60  # In seconds

        # Add time for images
        if has_images:
            image_time = np.random.uniform(1, 3)  # 1-3 seconds per image set
            reading_time += image_time

        # Add natural variance
        reading_time *= np.random.uniform(0.8, 1.2)

        # Minimum reading time (quick glance)
        reading_time = max(reading_time, 0.5)

        return reading_time

    def get_typing_delay(self, text: str) -> list:
        """
        Generate realistic typing delays for each character

        Args:
            text: Text to type

        Returns:
            List of delays (in seconds) for each character
        """
        delays = []

        for i, char in enumerate(text):
            base_delay = self.base_timings['type_char']['mean'] / 1000

            # Longer delay after punctuation (thinking)
            if i > 0 and text[i-1] in '.!?,;:':
                base_delay *= np.random.uniform(2, 4)

            # Longer delay for spaces (word boundaries)
            elif char == ' ':
                base_delay *= np.random.uniform(1.2, 1.8)

            # Occasional longer pauses (thinking/hesitation)
            elif np.random.random() < 0.1:
                base_delay *= np.random.uniform(2, 5)

            # Add variance
            delay = np.random.normal(base_delay, base_delay * 0.3)
            delay = max(0.05, delay)  # Minimum 50ms

            delays.append(delay)

        return delays

    def get_between_action_delay(self) -> float:
        """
        Get delay between actions (thinking time)

        Returns:
            Delay in seconds
        """
        return self.get_delay('between_actions')

    def get_think_pause(self) -> float:
        """
        Get a longer thinking pause (deciding what to do next)

        Returns:
            Delay in seconds
        """
        return self.get_delay('think_pause')

    def _update_state(self, action_type: str, delay_ms: float):
        """Update internal state for context-aware timing"""
        current_time = len(self.action_history)
        self.action_history.append({
            'type': action_type,
            'delay': delay_ms,
            'time': current_time
        })

        # Keep only recent history
        if len(self.action_history) > 50:
            self.action_history = self.action_history[-50:]

        # Update fatigue factor (increases slowly over time)
        self.fatigue_factor = min(1.5, 1.0 + len(self.action_history) * 0.002)

    def reset_session(self):
        """Reset timing state for a new session"""
        self.action_history = []
        self.fatigue_factor = 1.0
        self.last_action_time = 0

    def simulate_attention_span(self) -> bool:
        """
        Simulate human attention span and fatigue
        Returns True if user should take a break
        """
        # Check session length
        session_length = len(self.action_history)

        # Probability of needing break increases with actions
        # Most humans can focus for 15-45 minutes
        break_probability = min(0.9, session_length / 500)

        return np.random.random() < break_probability

    def save_model(self, path: str):
        """Save the trained model"""
        torch.save(self.model.state_dict(), path)

    def load_model(self, path: str):
        """Load a trained model"""
        self.model.load_state_dict(torch.load(path, map_location=self.device))
        self.model.eval()


if __name__ == '__main__':
    # Test the timing generator
    generator = TimingPatternGenerator()

    print("Testing timing patterns:\n")

    print("1. Tap delay:")
    for i in range(5):
        delay = generator.get_delay('tap')
        print(f"   Tap {i+1}: {delay:.3f}s")

    print("\n2. Reading time for 100 character text:")
    reading = generator.get_reading_time(100, has_images=True, engagement_level=0.7)
    print(f"   Reading time: {reading:.2f}s")

    print("\n3. Typing 'Hello World':")
    delays = generator.get_typing_delay("Hello World!")
    for i, char in enumerate("Hello World!"):
        print(f"   '{char}': {delays[i]:.3f}s")

    print("\n4. Between action delays:")
    for i in range(3):
        delay = generator.get_between_action_delay()
        print(f"   Delay {i+1}: {delay:.3f}s")
