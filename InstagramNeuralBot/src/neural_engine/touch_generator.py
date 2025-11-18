"""
Touch Pattern Generator using Variational Autoencoder (VAE)
Generates realistic touch coordinates with human-like imprecision and variance
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Tuple, List
import os


class TouchVAE(nn.Module):
    """Variational Autoencoder for generating realistic touch patterns"""

    def __init__(self, latent_dim=16):
        super(TouchVAE, self).__init__()

        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(2, 64),  # Input: (x, y) normalized coordinates
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU()
        )

        self.fc_mu = nn.Linear(64, latent_dim)
        self.fc_logvar = nn.Linear(64, latent_dim)

        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 2),  # Output: (x, y) normalized coordinates
            nn.Sigmoid()  # Normalize to [0, 1]
        )

    def encode(self, x):
        h = self.encoder(x)
        return self.fc_mu(h), self.fc_logvar(h)

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar


class TouchPatternGenerator:
    """
    Generates human-like touch patterns using neural networks
    Handles coordinate generation with natural variance and finger imprecision
    """

    def __init__(self, model_path=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = TouchVAE(latent_dim=16).to(self.device)
        self.model.eval()

        # Load pre-trained weights if available
        if model_path and os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        else:
            # Initialize with synthetic human-like patterns
            self._initialize_with_synthetic_data()

    def _initialize_with_synthetic_data(self):
        """Initialize model with synthetic human touch patterns"""
        # Generate synthetic training data based on human touch characteristics
        # Humans tend to touch with Gaussian distribution around center of elements
        synthetic_data = []

        for _ in range(1000):
            # Center-biased touches with natural variance
            center_x = np.random.normal(0.5, 0.15)  # 68% within 0.35-0.65
            center_y = np.random.normal(0.5, 0.15)

            # Clip to valid range
            center_x = np.clip(center_x, 0.1, 0.9)
            center_y = np.clip(center_y, 0.1, 0.9)

            synthetic_data.append([center_x, center_y])

        # Quick training on synthetic data
        self._train_on_data(synthetic_data, epochs=50)

    def _train_on_data(self, data, epochs=50):
        """Train the VAE on touch pattern data"""
        self.model.train()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)

        data_tensor = torch.FloatTensor(data).to(self.device)

        for epoch in range(epochs):
            optimizer.zero_grad()
            recon, mu, logvar = self.model(data_tensor)

            # VAE loss = reconstruction loss + KL divergence
            recon_loss = nn.functional.mse_loss(recon, data_tensor, reduction='sum')
            kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())

            loss = recon_loss + kl_loss
            loss.backward()
            optimizer.step()

        self.model.eval()

    def generate_touch(self, element_bounds: Tuple[int, int, int, int],
                       bias='center', variance=0.15) -> Tuple[int, int]:
        """
        Generate a human-like touch coordinate within element bounds

        Args:
            element_bounds: (left, top, right, bottom) in pixels
            bias: 'center', 'random', or tuple of (x_bias, y_bias) in [0, 1]
            variance: Amount of natural variance (higher = more spread)

        Returns:
            (x, y) pixel coordinates for touch
        """
        left, top, right, bottom = element_bounds
        width = right - left
        height = bottom - top

        # Generate normalized coordinates using the model
        with torch.no_grad():
            # Sample from latent space
            z = torch.randn(1, 16).to(self.device)
            normalized_coords = self.model.decode(z).cpu().numpy()[0]

        # Apply bias
        if bias == 'center':
            # Center-biased with variance
            normalized_coords[0] = np.clip(np.random.normal(0.5, variance), 0.1, 0.9)
            normalized_coords[1] = np.clip(np.random.normal(0.5, variance), 0.1, 0.9)
        elif bias == 'random':
            # More uniform distribution but avoiding edges
            normalized_coords[0] = np.random.uniform(0.15, 0.85)
            normalized_coords[1] = np.random.uniform(0.15, 0.85)
        elif isinstance(bias, tuple):
            # Custom bias point with variance
            bias_x, bias_y = bias
            normalized_coords[0] = np.clip(np.random.normal(bias_x, variance), 0.1, 0.9)
            normalized_coords[1] = np.clip(np.random.normal(bias_y, variance), 0.1, 0.9)

        # Convert to pixel coordinates
        x = int(left + normalized_coords[0] * width)
        y = int(top + normalized_coords[1] * height)

        # Add micro-jitter to simulate finger imprecision (sub-pixel level represented as int)
        x += int(np.random.normal(0, 2))
        y += int(np.random.normal(0, 2))

        # Ensure within bounds
        x = np.clip(x, left + 5, right - 5)
        y = np.clip(y, top + 5, bottom - 5)

        return (x, y)

    def generate_touch_sequence(self, element_bounds: Tuple[int, int, int, int],
                               num_touches: int = 5) -> List[Tuple[int, int]]:
        """
        Generate a sequence of touches (useful for multi-tap gestures)

        Args:
            element_bounds: (left, top, right, bottom) in pixels
            num_touches: Number of touch points to generate

        Returns:
            List of (x, y) coordinates
        """
        return [self.generate_touch(element_bounds) for _ in range(num_touches)]

    def generate_double_tap(self, element_bounds: Tuple[int, int, int, int]) -> List[Tuple[int, int]]:
        """
        Generate a human-like double-tap (two touches very close together)

        Args:
            element_bounds: (left, top, right, bottom) in pixels

        Returns:
            List of 2 (x, y) coordinates for double tap
        """
        # First tap
        first_touch = self.generate_touch(element_bounds)

        # Second tap very close to first (humans don't tap exactly same spot)
        second_touch = (
            first_touch[0] + int(np.random.normal(0, 3)),
            first_touch[1] + int(np.random.normal(0, 3))
        )

        return [first_touch, second_touch]

    def save_model(self, path: str):
        """Save the trained model"""
        torch.save(self.model.state_dict(), path)

    def load_model(self, path: str):
        """Load a trained model"""
        self.model.load_state_dict(torch.load(path, map_location=self.device))
        self.model.eval()


if __name__ == '__main__':
    # Test the touch pattern generator
    generator = TouchPatternGenerator()

    # Simulate a button at position (100, 200, 300, 280)
    button_bounds = (100, 200, 300, 280)

    print("Generating 10 human-like touch coordinates:")
    for i in range(10):
        x, y = generator.generate_touch(button_bounds)
        print(f"Touch {i+1}: ({x}, {y})")
