"""
Belousov-Zhabotinsky reaction — excitable medium with spiral waves.
Uses Oregonator model for simplified kinetics.
"""
import numpy as np
from typing import Tuple


class OregonatorBZ:
    """
    Oregonator model for BZ reaction.
    
    Three-variable simplification:
    - x: HBrO2 (activator)
    - y: Br- (inhibitor)
    - z: Ce(IV) (oxidized catalyst)
    """
    
    def __init__(
        self,
        size: int = 256,
        q: float = 0.002,  # Reaction parameter
        f: float = 1.4,    # Stoichiometric factor
        epsilon: float = 0.04,  # Time scale separation
        Du: float = 1.0,
        Dv: float = 0.6,
        dt: float = 0.01
    ):
        self.size = size
        self.q = q
        self.f = f
        self.epsilon = epsilon
        self.Du = Du
        self.Dv = Dv
        self.dt = dt
        
        # Initialize: uniform with small perturbations
        self.x = np.ones((size, size), dtype=np.float32) * 0.5
        self.y = np.ones((size, size), dtype=np.float32) * 0.5
        self.z = np.zeros((size, size), dtype=np.float32)
        
        # Seed spiral
        self._seed_spiral()
    
    def _seed_spiral(self):
        """Initialize broken wave front to seed spiral."""
        cx, cy = self.size // 2, self.size // 2
        y, x = np.ogrid[:self.size, :self.size]
        
        # Create angular perturbation
        angle = np.arctan2(y - cy, x - cx)
        radius = np.sqrt((x - cx)**2 + (y - cy)**2)
        
        # Broken circle: high x in quadrant, low elsewhere
        mask = (radius < self.size // 4) & (angle > 0)
        self.x[mask] = 1.0
        self.y[mask] = 0.0
    
    def _laplacian(self, field: np.ndarray) -> np.ndarray:
        """5-point stencil with periodic BC."""
        return (
            np.roll(field, 1, axis=0) + np.roll(field, -1, axis=0) +
            np.roll(field, 1, axis=1) + np.roll(field, -1, axis=1) -
            4 * field
        )
    
    def step(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Single integration step."""
        # Reaction terms (Oregonator)
        x, y, z = self.x, self.y, self.z
        reaction_x = (x + y - self.q * x**2 - x * y) / self.epsilon
        reaction_y = -y + 2 * self.f * z - x * y
        reaction_z = x - z
        
        # Diffusion
        Lx = self._laplacian(x)
        # y and z typically don't diffuse in simple Oregonator
        
        # Update
        self.x = np.clip(x + self.dt * (self.Du * Lx + reaction_x), 0, 10)
        self.y = np.clip(y + self.dt * reaction_y, 0, 10)
        self.z = np.clip(z + self.dt * reaction_z, 0, 10)
        
        return self.x, self.y, self.z
    
    def get_render_target(self) -> np.ndarray:
        """Return visualization array (x channel shows waves)."""
        return (self.x / np.max(self.x) * 255).astype(np.uint8)


class BZExcitableMedium:
    """
    Simplified two-variable BZ model for faster simulation.
    """
    
    def __init__(
        self,
        size: int = 256,
        a: float = 0.5,  # Excitation threshold
        b: float = 0.05,  # Recovery rate
        epsilon: float = 0.02,
        D: float = 1.0
    ):
        self.size = size
        self.a = a
        self.b = b
        self.epsilon = epsilon
        self.D = D
        
        # u: excitation, v: recovery
        self.u = np.zeros((size, size), dtype=np.float32)
        self.v = np.zeros((size, size), dtype=np.float32)
        
        self._seed_target()
    
    def _seed_target(self):
        """Create target pattern seed."""
        cx, cy = self.size // 2, self.size // 2
        y, x = np.ogrid[:self.size, :self.size]
        r = np.sqrt((x - cx)**2 + (y - cy)**2)
        # Concentric rings
        self.u = (np.sin(r / 5) > 0).astype(np.float32) * 0.5
    
    def _laplacian(self, field: np.ndarray) -> np.ndarray:
        return np.roll(field, 1, axis=0) + np.roll(field, -1, axis=0) + \
               np.roll(field, 1, axis=1) + np.roll(field, -1, axis=1) - 4 * field
    
    def step(self):
        u, v = self.u, self.v
        
        # FitzHugh-Nagumo-like kinetics for excitable medium
        du = self.D * self._laplacian(u) + \
             (u * (1 - u) * (u - self.a) - v) / self.epsilon
        dv = self.b * u - v
        
        self.u = np.clip(u + 0.1 * du, 0, 1)
        self.v = np.clip(v + 0.1 * dv, 0, 1)
        
        # Refractory period: recently excited cells can't re-excite
        self.u[self.u > 0.9] *= 0.99  # Slow decay at peak
        
        return self.u, self.v
