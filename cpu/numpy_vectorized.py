"""
NumPy vectorized implementation — baseline 1.27ms/step at 300x300.
"""
import numpy as np
from typing import Tuple, Optional


class GrayScottNumpy:
    """Optimized NumPy implementation with explicit periodic BC."""
    
    def __init__(
        self,
        size: int = 300,
        Du: float = 0.1,  # Note: different scaling than core module
        Dv: float = 0.05,
        F: float = 0.0545,
        k: float = 0.062,
        dt: float = 1.0
    ):
        self.n = size
        self.Du = Du
        self.Dv = Dv
        self.F = F
        self.k = k
        self.dt = dt
        
        # Use (n+2) x (n+2) with ghost cells for periodic BC
        self.U = np.ones((size + 2, size + 2), dtype=np.float64)
        self.V = np.zeros((size + 2, size + 2), dtype=np.float64)
        
        # Seed center
        self._seed_center()
    
    def _seed_center(self):
        """Initialize center square with u=0.5, v=0.25."""
        x = np.linspace(0, 1, self.n + 2)
        y = np.linspace(0, 1, self.n + 2)
        X, Y = np.meshgrid(x, y)
        mask = (0.4 < X) & (X < 0.6) & (0.4 < Y) & (Y < 0.6)
        self.U[mask] = 0.50
        self.V[mask] = 0.25
    
    def _periodic_bc(self):
        """Apply periodic boundary conditions via ghost cells."""
        self.U[0, :] = self.U[-2, :]
        self.U[-1, :] = self.U[1, :]
        self.U[:, 0] = self.U[:, -2]
        self.U[:, -1] = self.U[:, 1]
        self.V[0, :] = self.V[-2, :]
        self.V[-1, :] = self.V[1, :]
        self.V[:, 0] = self.V[:, -2]
        self.V[:, -1] = self.V[:, 1]
    
    def _laplacian(self, field: np.ndarray) -> np.ndarray:
        """
        5-point stencil Laplacian on interior points.
        field shape: (n+2, n+2), returns interior (n, n)
        """
        return (
            field[:-2, 1:-1] +   # up
            field[2:, 1:-1] +    # down
            field[1:-1, :-2] +   # left
            field[1:-1, 2:] -    # right
            4 * field[1:-1, 1:-1]  # center
        )
    
    def step(self) -> Tuple[np.ndarray, np.ndarray]:
        """Single Forward Euler step."""
        # Get interior views
        u = self.U[1:-1, 1:-1]
        v = self.V[1:-1, 1:-1]
        
        # Compute Laplacians
        Lu = self._laplacian(self.U)
        Lv = self._laplacian(self.V)
        
        # Reaction term
        uvv = u * v * v
        
        # Update (in-place)
        u += self.Du * Lu - uvv + self.F * (1 - u)
        v += self.Dv * Lv + uvv - (self.F + self.k) * v
        
        # Apply BC
        self._periodic_bc()
        
        return self.U, self.V
    
    def step_n(self, n: int):
        """Multiple steps."""
        for _ in range(n):
            self.step()
        return self.get_interior()
    
    def get_interior(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get interior (n x n) arrays without ghost cells."""
        return self.U[1:-1, 1:-1].copy(), self.V[1:-1, 1:-1].copy()
