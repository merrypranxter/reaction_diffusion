"""
Schnakenberg model with cross-diffusion.
Generates shape-shifting grids (stripes → hexagons).
"""
import numpy as np


class Schnakenberg:
    """
    Schnakenberg reaction-diffusion with cross-diffusion terms:
        ∂u/∂t = Du∇²u + ∂x(Dux∂v/∂x) + f(u,v)
        ∂v/∂t = Dv∇²v + ∂y(Dvy∂u/∂y) + g(u,v)
    
    where cross-diffusion drives subcritical bifurcations.
    """
    
    def __init__(
        self,
        size: int = 256,
        Du: float = 0.05,
        Dv: float = 1.0,
        Dux: float = 0.1,  # Cross-diffusion u responding to v gradient
        Dvy: float = 0.1,  # Cross-diffusion v responding to u gradient
        a: float = 0.1,    # Production rate
        b: float = 0.9,    # Saturation
        dt: float = 0.01
    ):
        self.size = size
        self.Du = Du
        self.Dv = Dv
        self.Dux = Dux
        self.Dvy = Dvy
        self.a = a
        self.b = b
        self.dt = dt
        
        self.u = np.ones((size, size)) * a + b
        self.v = np.ones((size, size)) * b / (a + b)**2
        
        # Add perturbation
        self.u += np.random.random((size, size)) * 0.01
    
    def _gradients(self, field: np.ndarray):
        """Compute gradients (central differences)."""
        dx = (np.roll(field, -1, axis=1) - np.roll(field, 1, axis=1)) / 2
        dy = (np.roll(field, -1, axis=0) - np.roll(field, 1, axis=0)) / 2
        return dx, dy
    
    def _divergence(self, fx: np.ndarray, fy: np.ndarray) -> np.ndarray:
        """Compute divergence."""
        return (
            np.roll(fx, -1, axis=1) - np.roll(fx, 1, axis=1) +
            np.roll(fy, -1, axis=0) - np.roll(fy, 1, axis=0)
        ) / 2
    
    def _laplacian(self, field: np.ndarray) -> np.ndarray:
        """Standard Laplacian."""
        return (
            np.roll(field, 1, axis=0) + np.roll(field, -1, axis=0) +
            np.roll(field, 1, axis=1) + np.roll(field, -1, axis=1) -
            4 * field
        )
    
    def step(self):
        """Integration with cross-diffusion."""
        u, v = self.u, self.v
        
        # Standard reaction terms
        reaction_u = self.a - u + u**2 * v
        reaction_v = self.b - u**2 * v
        
        # Standard diffusion
        Lu = self._laplacian(u)
        Lv = self._laplacian(v)
        
        # Cross-diffusion terms
        dudx, dudy = self._gradients(u)
        dvdx, dvdy = self._gradients(v)
        
        # Divergence of cross-fluxes
        cross_u = self._divergence(self.Dux * dvdx, self.Dux * dvdy)
        cross_v = self._divergence(self.Dvy * dudx, self.Dvy * dudy)
        
        # Update
        self.u = u + self.dt * (self.Du * Lu + cross_u + reaction_u)
        self.v = v + self.dt * (self.Dv * Lv + cross_v + reaction_v)
        
        return self.u, self.v
    
    def get_pattern(self) -> np.ndarray:
        """Return visualization."""
        return (self.v / np.max(self.v) * 255).astype(np.uint8)
