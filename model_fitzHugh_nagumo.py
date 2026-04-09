"""
FitzHugh-Nagumo model — neural action potentials and excitable media.
"""
import numpy as np
from typing import Tuple, Optional


class FitzHughNagumo:
    """
    Classic FHN model:
        dv/dt = v - v^3/3 - w + I_ext + D*laplacian(v)
        dw/dt = epsilon*(v + a - b*w)
    
    Where:
    - v: membrane potential (fast variable)
    - w: recovery variable (slow variable)
    - a, b, epsilon: parameters controlling dynamics
    """
    
    def __init__(
        self,
        size: int = 256,
        a: float = 0.7,
        b: float = 0.8,
        epsilon: float = 0.08,
        D: float = 1.0,
        dt: float = 0.05,
        I_ext: Optional[np.ndarray] = None
    ):
        self.size = size
        self.a = a
        self.b = b
        self.epsilon = epsilon
        self.D = D
        self.dt = dt
        
        # State variables
        self.v = np.zeros((size, size), dtype=np.float32)
        self.w = np.zeros((size, size), dtype=np.float32)
        
        # External current (stimulus)
        self.I_ext = I_ext if I_ext is not None else np.zeros((size, size))
        
        # Initialize with resting state perturbation
        self._seed_pulse()
    
    def _seed_pulse(self):
        """Initialize with propagating pulse."""
        cx = self.size // 2
        self.v[:, cx-5:cx+5] = 1.5  # Depolarized strip
    
    def _laplacian(self, field: np.ndarray) -> np.ndarray:
        """Periodic boundary Laplacian."""
        return (
            np.roll(field, 1, axis=0) + np.roll(field, -1, axis=0) +
            np.roll(field, 1, axis=1) + np.roll(field, -1, axis=1) -
            4 * field
        )
    
    def step(self) -> Tuple[np.ndarray, np.ndarray]:
        """Integrate one time step."""
        v, w = self.v, self.w
        
        # FHN equations
        dv = v - v**3 / 3.0 - w + self.I_ext + self.D * self._laplacian(v)
        dw = self.epsilon * (v + self.a - self.b * w)
        
        self.v = v + self.dt * dv
        self.w = w + self.dt * dw
        
        return self.v, self.w
    
    def add_stimulus(self, x: int, y: int, strength: float = 2.0, radius: int = 5):
        """Add localized external stimulus."""
        ygrid, xgrid = np.ogrid[:self.size, :self.size]
        mask = (xgrid - x)**2 + (ygrid - y)**2 < radius**2
        self.I_ext[mask] = strength
    
    def clear_stimulus(self):
        """Remove external stimulus."""
        self.I_ext.fill(0)
    
    def get_activation_front(self) -> np.ndarray:
        """Return binary activation map."""
        return (self.v > 0.5).astype(np.uint8) * 255


class FHNNetwork:
    """
    FHN on a network/graph structure for neural tissue simulation.
    """
    
    def __init__(
        self,
        adjacency: np.ndarray,  # Connectivity matrix
        n_nodes: int,
        **fhn_params
    ):
        self.adjacency = adjacency
        self.n_nodes = n_nodes
        self.v = np.zeros(n_nodes)
        self.w = np.zeros(n_nodes)
        self.a = fhn_params.get('a', 0.7)
        self.b = fhn_params.get('b', 0.8)
        self.epsilon = fhn_params.get('epsilon', 0.08)
        self.dt = fhn_params.get('dt', 0.05)
    
    def _network_laplacian(self, field: np.ndarray) -> np.ndarray:
        """Graph Laplacian: L = D - A."""
        # Degree matrix diagonal
        degrees = np.sum(self.adjacency, axis=1)
        # Laplacian applied to field
        return degrees * field - self.adjacency @ field
    
    def step(self):
        """Network integration step."""
        dv = self.v - self.v**3 / 3.0 - self.w + \
             0.1 * self._network_laplacian(self.v)  # Coupling
        dw = self.epsilon * (self.v + self.a - self.b * self.w)
        
        self.v += self.dt * dv
        self.w += self.dt * dw
        
        return self.v, self.w
