"""
Cahn-Hilliard equation for phase separation and coarsening.
"""
import numpy as np
from scipy.fft import fft2, ifft2, fftfreq


class CahnHilliard:
    """
    Cahn-Hilliard equation:
        ∂φ/∂t = ∇²(μ) = ∇²(dF/dφ)
    
    where F is free energy functional.
    Uses spectral method for efficiency.
    """
    
    def __init__(
        self,
        size: int = 256,
        M: float = 1.0,  # Mobility
        gamma: float = 0.5,  # Interface energy coefficient
        dt: float = 0.01
    ):
        self.size = size
        self.M = M
        self.gamma = gamma
        self.dt = dt
        
        # Initialize with random mixture
        self.phi = np.random.random((size, size)) * 0.1 + 0.45  # Near 0.5
        
        # Spectral setup
        self._setup_spectral()
    
    def _setup_spectral(self):
        """Initialize FFT operators."""
        # Wavenumbers
        kx = 2 * np.pi * fftfreq(self.size)
        ky = 2 * np.pi * fftfreq(self.size)
        self.KX, self.KY = np.meshgrid(kx, ky)
        self.K2 = self.KX**2 + self.KY**2  # Laplacian in Fourier space
        self.K4 = self.K2**2
        
        # Denominator for implicit scheme
        self.denom = 1 + self.dt * self.M * self.gamma * self.K4
    
    def _chemical_potential(self, phi: np.ndarray) -> np.ndarray:
        """μ = dF/dφ = φ³ - φ - γ∇²φ."""
        # Double-well potential derivative: φ³ - φ
        bulk = phi**3 - phi
        # Interface term
        lap_phi = ifft2(-self.K2 * fft2(phi)).real
        return bulk - self.gamma * lap_phi
    
    def step(self) -> np.ndarray:
        """Spectral integration step."""
        # Fourier transform
        phi_hat = fft2(self.phi)
        
        # Chemical potential
        mu = self._chemical_potential(self.phi)
        mu_hat = fft2(mu)
        
        # Update in Fourier space (semi-implicit)
        phi_hat = (phi_hat - self.dt * self.M * self.K2 * mu_hat) / self.denom
        
        # Inverse transform
        self.phi = ifft2(phi_hat).real
        return self.phi
    
    def get_phase_field(self) -> np.ndarray:
        """Return phase field for visualization."""
        return ((self.phi + 1) / 2 * 255).astype(np.uint8)
    
    def get_interface(self) -> np.ndarray:
        """Return interface locations (gradient magnitude)."""
        grad_x = np.roll(self.phi, -1, axis=1) - np.roll(self.phi, 1, axis=1)
        grad_y = np.roll(self.phi, -1, axis=0) - np.roll(self.phi, 1, axis=0)
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        return (magnitude / np.max(magnitude) * 255).astype(np.uint8)


class CahnHilliardWithNoise(CahnHilliard):
    """
    Cahn-Hilliard with thermal noise (Cahn-Hilliard-Cook).
    """
    
    def __init__(self, *args, temperature: float = 0.01, **kwargs):
        super().__init__(*args, **kwargs)
        self.temperature = temperature
    
    def step(self) -> np.ndarray:
        """Add thermal fluctuation."""
        # Deterministic step
        phi_hat = fft2(self.phi)
        mu = self._chemical_potential(self.phi)
        mu_hat = fft2(mu)
        
        # Add noise in Fourier space
        noise_hat = fft2(np.random.normal(0, self.temperature, self.phi.shape))
        phi_hat = (phi_hat - self.dt * self.M * self.K2 * mu_hat +
                   np.sqrt(self.dt) * noise_hat) / self.denom
        
        self.phi = ifft2(phi_hat).real
        return self.phi
