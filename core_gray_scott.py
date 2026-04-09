"""
Gray-Scott reaction-diffusion simulation — NumPy implementation.
"""
import numpy as np
from typing import Optional, Tuple, Callable
from pathlib import Path
from .laplacian import laplacian_9point
from .seeding import seed_center_square


class GrayScottNumpy:
    """
    Gray-Scott reaction-diffusion simulator using NumPy.
    
    Equations:
        du/dt = Du * laplacian(u) - u*v^2 + F*(1-u)
        dv/dt = Dv * laplacian(v) + u*v^2 - (F+k)*v
    """
    
    def __init__(
        self,
        size: int = 256,
        Du: float = 1.0,
        Dv: float = 0.5,
        F: float = 0.0545,
        k: float = 0.062,
        dt: float = 1.0,
        seed: Optional[str] = "center_square"
    ):
        """
        Initialize Gray-Scott simulation.
        
        Args:
            size: Grid dimension (size x size)
            Du: Diffusion coefficient for U
            Dv: Diffusion coefficient for V
            F: Feed rate
            k: Kill rate
            dt: Time step
            seed: Initial condition type ("center_square", "center_circle", "scattered")
        """
        self.size = size
        self.Du = Du
        self.Dv = Dv
        self.F = F
        self.k = k
        self.dt = dt
        
        # Initialize fields
        if seed == "center_square":
            self.u, self.v = seed_center_square(size)
        elif seed == "center_circle":
            from .seeding import seed_center_circle
            self.u, self.v = seed_center_circle(size)
        elif seed == "scattered":
            from .seeding import seed_scattered
            self.u, self.v = seed_scattered(size)
        else:
            from .seeding import seed_uniform
            self.u, self.v = seed_uniform(size)
        
        self.iteration = 0
    
    def step(self, n_steps: int = 1) -> Tuple[np.ndarray, np.ndarray]:
        """
        Advance simulation by n_steps.
        
        Args:
            n_steps: Number of integration steps
            
        Returns:
            (u, v) arrays after stepping
        """
        for _ in range(n_steps):
            # Compute Laplacians
            Lu = laplacian_9point(self.u)
            Lv = laplacian_9point(self.v)
            
            # Reaction term
            uvv = self.u * self.v * self.v
            
            # Update equations (Forward Euler)
            self.u = self.u + self.dt * (
                self.Du * Lu - uvv + self.F * (1.0 - self.u)
            )
            self.v = self.v + self.dt * (
                self.Dv * Lv + uvv - (self.F + self.k) * self.v
            )
            
            # Clamp to physical range [0, 1]
            np.clip(self.u, 0, 1, out=self.u)
            np.clip(self.v, 0, 1, out=self.v)
            
            self.iteration += 1
        
        return self.u, self.v
    
    def run(self, n_steps: int) -> Tuple[np.ndarray, np.ndarray]:
        """Run for n_steps (convenience wrapper)."""
        return self.step(n_steps)
    
    def get_state(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get current (u, v) state."""
        return self.u.copy(), self.v.copy()
    
    def set_parameters(self, F: Optional[float] = None, k: Optional[float] = None):
        """Update parameters mid-simulation."""
        if F is not None:
            self.F = F
        if k is not None:
            self.k = k
    
    def to_image(self, mode: str = "v") -> np.ndarray:
        """
        Convert state to image array.
        
        Args:
            mode: "v" (V concentration), "u" (U concentration),
                  "uv" (both as RGB), "munafo" (u + du/dt coloring)
                  
        Returns:
            Image array uint8 (H, W) or (H, W, 3)
        """
        if mode == "v":
            img = (1.0 - self.v) * 255
            return img.astype(np.uint8)
        elif mode == "u":
            img = self.u * 255
            return img.astype(np.uint8)
        elif mode == "uv":
            img = np.zeros((self.size, self.size, 3), dtype=np.uint8)
            img[:, :, 0] = (self.u * 255).astype(np.uint8)
            img[:, :, 1] = ((1.0 - self.v) * 255).astype(np.uint8)
            return img
        else:
            raise ValueError(f"Unknown mode: {mode}")
    
    def save_image(self, path: str, mode: str = "v"):
        """Save current state to image file."""
        from PIL import Image
        img_array = self.to_image(mode)
        if img_array.ndim == 2:
            img = Image.fromarray(img_array, mode='L')
        else:
            img = Image.fromarray(img_array, mode='RGB')
        img.save(path)
    
    def save_state(self, path: str):
        """Save full state to NPZ file."""
        np.savez(path, u=self.u, v=self.v, iteration=self.iteration,
                 F=self.F, k=self.k, Du=self.Du, Dv=self.Dv)
    
    @classmethod
    def load_state(cls, path: str) -> "GrayScottNumpy":
        """Load from NPZ file."""
        data = np.load(path)
        sim = cls.__new__(cls)
        sim.u = data['u']
        sim.v = data['v']
        sim.iteration = int(data['iteration'])
        sim.F = float(data['F'])
        sim.k = float(data['k'])
        sim.Du = float(data['Du'])
        sim.Dv = float(data['Dv'])
        sim.size = sim.u.shape[0]
        sim.dt = 1.0  # Default, not saved in old files
        return sim
