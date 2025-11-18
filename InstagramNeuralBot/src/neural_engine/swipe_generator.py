"""
Swipe Trajectory Generator using LSTM
Generates realistic swipe paths with human-like curves and acceleration profiles
"""

import torch
import torch.nn as nn
import numpy as np
from typing import List, Tuple
import os


class SwipeLSTM(nn.Module):
    """LSTM model for generating swipe trajectory points"""

    def __init__(self, hidden_size=64, num_layers=2):
        super(SwipeLSTM, self).__init__()

        # Input: (velocity_x, velocity_y, acceleration)
        # Output: (delta_x, delta_y, velocity)
        self.lstm = nn.LSTM(
            input_size=3,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2
        )

        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Linear(32, 3),  # Output: (delta_x, delta_y, velocity)
            nn.Tanh()  # Normalize outputs
        )

    def forward(self, x, hidden=None):
        lstm_out, hidden = self.lstm(x, hidden)
        output = self.fc(lstm_out)
        return output, hidden


class SwipeTrajectoryGenerator:
    """
    Generates human-like swipe trajectories using LSTM
    Mimics natural acceleration/deceleration and curved paths
    """

    def __init__(self, model_path=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = SwipeLSTM(hidden_size=64, num_layers=2).to(self.device)
        self.model.eval()

        if model_path and os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        else:
            self._initialize_with_synthetic_data()

    def _initialize_with_synthetic_data(self):
        """Initialize with synthetic human swipe patterns"""
        # Generate synthetic swipe data with human characteristics:
        # - Fast start, slow end (or vice versa)
        # - Slight curves, not perfectly straight
        # - Variable velocity
        synthetic_sequences = []

        for _ in range(200):
            seq_length = np.random.randint(15, 30)
            sequence = []

            # Random swipe characteristics
            initial_velocity = np.random.uniform(0.5, 1.0)
            deceleration = np.random.uniform(0.9, 0.99)
            curve_factor = np.random.uniform(-0.1, 0.1)

            velocity = initial_velocity
            for t in range(seq_length):
                velocity *= deceleration

                # Add curve
                delta_x = velocity
                delta_y = curve_factor * np.sin(t / seq_length * np.pi)
                accel = velocity - (velocity * deceleration)

                sequence.append([delta_x, delta_y, accel])

            synthetic_sequences.append(sequence)

        self._train_on_sequences(synthetic_sequences, epochs=30)

    def _train_on_sequences(self, sequences, epochs=30):
        """Train LSTM on swipe sequences"""
        self.model.train()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        criterion = nn.MSELoss()

        for epoch in range(epochs):
            total_loss = 0
            for sequence in sequences:
                if len(sequence) < 2:
                    continue

                # Convert to tensor
                seq_tensor = torch.FloatTensor(sequence[:-1]).unsqueeze(0).to(self.device)
                target_tensor = torch.FloatTensor(sequence[1:]).unsqueeze(0).to(self.device)

                optimizer.zero_grad()
                output, _ = self.model(seq_tensor)
                loss = criterion(output, target_tensor)
                loss.backward()
                optimizer.step()

                total_loss += loss.item()

        self.model.eval()

    def generate_swipe(self, start: Tuple[int, int], end: Tuple[int, int],
                       duration_ms: int = None, num_points: int = None) -> List[Tuple[int, int, int]]:
        """
        Generate a human-like swipe trajectory from start to end

        Args:
            start: (x, y) starting coordinates
            end: (x, y) ending coordinates
            duration_ms: Total swipe duration in milliseconds (default: random 200-500ms)
            num_points: Number of points in trajectory (default: based on distance)

        Returns:
            List of (x, y, timestamp_ms) tuples forming the swipe path
        """
        start_x, start_y = start
        end_x, end_y = end

        # Calculate distance
        distance = np.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)

        # Determine duration and number of points
        if duration_ms is None:
            # Longer swipes take more time, but with variance
            duration_ms = int(np.random.normal(300, 50))
            duration_ms = np.clip(duration_ms, 200, 600)

        if num_points is None:
            # More points for longer swipes, but keep it reasonable
            num_points = int(distance / 20)
            num_points = np.clip(num_points, 10, 50)

        # Generate trajectory using LSTM
        trajectory = self._generate_lstm_trajectory(start, end, num_points)

        # Add timestamps with human-like timing (not perfectly uniform)
        trajectory_with_time = self._add_realistic_timestamps(trajectory, duration_ms)

        return trajectory_with_time

    def _generate_lstm_trajectory(self, start: Tuple[int, int], end: Tuple[int, int],
                                  num_points: int) -> List[Tuple[int, int]]:
        """Generate trajectory points using LSTM"""
        start_x, start_y = start
        end_x, end_y = end

        # Direction vector
        direction_x = end_x - start_x
        direction_y = end_y - start_y
        distance = np.sqrt(direction_x**2 + direction_y**2)

        if distance == 0:
            return [(start_x, start_y)]

        # Normalize direction
        norm_dir_x = direction_x / distance
        norm_dir_y = direction_y / distance

        # Generate trajectory
        points = [(start_x, start_y)]
        current_x, current_y = float(start_x), float(start_y)

        # Initial conditions
        velocity = np.random.uniform(0.7, 1.0)
        step_size = distance / num_points

        with torch.no_grad():
            hidden = None
            for i in range(num_points - 1):
                # Create input
                progress = i / num_points
                curve_offset = np.random.normal(0, 0.1)  # Natural curve variation

                input_tensor = torch.FloatTensor([[
                    velocity * norm_dir_x,
                    velocity * norm_dir_y,
                    -velocity * 0.01  # Deceleration factor
                ]]).unsqueeze(0).to(self.device)

                # Get prediction
                output, hidden = self.model(input_tensor, hidden)
                delta_x, delta_y, new_velocity = output[0, 0].cpu().numpy()

                # Apply movement with curve
                perpendicular_x = -norm_dir_y
                perpendicular_y = norm_dir_x

                current_x += norm_dir_x * step_size + perpendicular_x * curve_offset * step_size
                current_y += norm_dir_y * step_size + perpendicular_y * curve_offset * step_size

                # Update velocity with human-like deceleration
                velocity *= np.random.uniform(0.95, 0.99)

                # Add point
                points.append((int(current_x), int(current_y)))

        # Ensure we end at the target (with small natural offset)
        final_offset_x = int(np.random.normal(0, 3))
        final_offset_y = int(np.random.normal(0, 3))
        points.append((end_x + final_offset_x, end_y + final_offset_y))

        return points

    def _add_realistic_timestamps(self, points: List[Tuple[int, int]],
                                  total_duration_ms: int) -> List[Tuple[int, int, int]]:
        """Add human-like timestamps to trajectory points"""
        if len(points) <= 1:
            return [(points[0][0], points[0][1], 0)]

        # Human swipes have non-uniform timing:
        # - Faster at the start
        # - Slower at the end
        # - Some random variation

        timestamps = [0]
        time_accum = 0

        for i in range(1, len(points)):
            # Progress through swipe
            progress = i / len(points)

            # Deceleration profile (more time towards the end)
            time_factor = 1.0 + (progress * 0.5)

            # Add random jitter
            time_factor *= np.random.uniform(0.9, 1.1)

            time_step = (total_duration_ms / len(points)) * time_factor
            time_accum += time_step
            timestamps.append(int(time_accum))

        # Normalize to fit total duration
        if timestamps[-1] > 0:
            scale = total_duration_ms / timestamps[-1]
            timestamps = [int(t * scale) for t in timestamps]

        return [(points[i][0], points[i][1], timestamps[i]) for i in range(len(points))]

    def generate_scroll(self, start_x: int, start_y: int, direction: str,
                       distance: int = None, speed: str = 'medium') -> List[Tuple[int, int, int]]:
        """
        Generate a scrolling swipe (up, down, left, right)

        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            direction: 'up', 'down', 'left', 'right'
            distance: Scroll distance in pixels (default: random based on direction)
            speed: 'slow', 'medium', 'fast'

        Returns:
            List of (x, y, timestamp_ms) tuples
        """
        # Default distances if not specified
        if distance is None:
            if direction in ['up', 'down']:
                distance = int(np.random.normal(500, 100))
                distance = np.clip(distance, 300, 800)
            else:
                distance = int(np.random.normal(400, 80))
                distance = np.clip(distance, 250, 600)

        # Calculate end point
        end_x, end_y = start_x, start_y
        if direction == 'up':
            end_y = start_y - distance
        elif direction == 'down':
            end_y = start_y + distance
        elif direction == 'left':
            end_x = start_x - distance
        elif direction == 'right':
            end_x = start_x + distance

        # Duration based on speed
        speed_map = {
            'slow': (400, 700),
            'medium': (250, 450),
            'fast': (150, 300)
        }
        duration_range = speed_map.get(speed, speed_map['medium'])
        duration_ms = int(np.random.uniform(*duration_range))

        return self.generate_swipe((start_x, start_y), (end_x, end_y), duration_ms)

    def save_model(self, path: str):
        """Save the trained model"""
        torch.save(self.model.state_dict(), path)

    def load_model(self, path: str):
        """Load a trained model"""
        self.model.load_state_dict(torch.load(path, map_location=self.device))
        self.model.eval()


if __name__ == '__main__':
    # Test the swipe generator
    generator = SwipeTrajectoryGenerator()

    print("Generating a scroll down gesture:")
    trajectory = generator.generate_scroll(540, 1000, 'down', distance=600)
    print(f"Generated {len(trajectory)} points:")
    for i, (x, y, t) in enumerate(trajectory[:5]):  # Show first 5 points
        print(f"Point {i+1}: ({x}, {y}) at {t}ms")
    print("...")
    print(f"Last point: ({trajectory[-1][0]}, {trajectory[-1][1]}) at {trajectory[-1][2]}ms")
