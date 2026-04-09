"""
Initial condition generators for Gray-Scott simulations.
"""
import numpy as np
from typing import Tuple, Optional


def seed_uniform(size: int, u_fill: float = 1.0, v_fill: float = 0.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Uniform initial condition.
    
    Args:
        size: Grid dimension (size x size)
        u_fill: U concentration everywhere
        v_fill: V concentration everywhere
        
    Returns:
        (u, v) arrays both shape (size, size)
    """
    u = np.full((size, size), u_fill, dtype=np.float32)
    v = np.full((size, size), v_fill, dtype=np.float32)
    return u, v


def seed_center_square(
    size: int,
    u_background: float = 1.0,
    v_background: float = 0.0,
    u_seed: float = 0.5,
    v_seed: float = 0.25,
    seed_size: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Classic Pearson seeding: square region at center.
    
    Args:
        size: Grid dimension
        u_background: U outside seed
        v_background: V outside seed
        u_seed: U inside seed
        v_seed: V inside seed
        seed_size: Half-width of seed (default: size//10)
        
    Returns:
        (u, v) arrays
    """
    u, v = seed_uniform(size, u_background, v_background)
    if seed_size is None:
        seed_size = size // 10
    center = size // 2
    start = center - seed_size
    end = center + seed_size
    u[start:end, start:end] = u_seed
    v[start:end, start:end] = v_seed
    return u, v


def seed_center_circle(
    size: int,
    u_background: float = 1.0,
    v_background: float = 0.0,
    u_seed: float = 0.5,
    v_seed: float = 0.25,
    radius: Optional[int] = None,
    noise: float = 0.01
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Circular seed with optional symmetry-breaking noise.
    
    Args:
        size: Grid dimension
        u_background: U outside seed
        v_background: V outside seed
        u_seed: U inside seed
        v_seed: V inside seed
        radius: Circle radius (default: size//10)
        noise: Amplitude of random perturbation
        
    Returns:
        (u, v) arrays
    """
    u, v = seed_uniform(size, u_background, v_background)
    if radius is None:
        radius = size // 10
    center = size // 2
    y, x = np.ogrid[:size, :size]
    mask = (x - center)**2 + (y - center)**2 <= radius**2
    u[mask] = u_seed + noise * (np.random.random(mask.sum()) - 0.5)
    v[mask] = v_seed + noise * (np.random.random(mask.sum()) - 0.5)
    return u, v


def seed_scattered(
    size: int,
    n_seeds: int = 50,
    seed_radius: int = 5,
    u_background: float = 1.0,
    v_background: float = 0.0,
    u_seed: float = 0.5,
    v_seed: float = 0.25
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Multiple scattered seeds — for Pearson plots or complex initial states.
    
    Args:
        size: Grid dimension
        n_seeds: Number of seed regions
        seed_radius: Radius of each seed
        u_background: U outside seeds
        v_background: V outside seeds
        u_seed: U inside seeds
        v_seed: V inside seeds
        
    Returns:
        (u, v) arrays
    """
    u, v = seed_uniform(size, u_background, v_background)
    for _ in range(n_seeds):
        cx = np.random.randint(0, size)
        cy = np.random.randint(0, size)
        y, x = np.ogrid[:size, :size]
        mask = (x - cx)**2 + (y - cy)**2 <= seed_radius**2
        u[mask] = u_seed + np.random.random() * 0.02 - 0.01
        v[mask] = v_seed + np.random.random() * 0.01 - 0.005
    return u, v


def seed_from_image(
    image: np.ndarray,
    u_channel: int = 0,
    v_channel: Optional[int] = None,
    invert: bool = False
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Initialize from image brightness.
    
    Args:
        image: 2D or 3D array (H, W) or (H, W, C)
        u_channel: Which channel for U (or 0 for grayscale)
        v_channel: Which channel for V (None = 1-U)
        invert: Invert brightness
        
    Returns:
        (u, v) arrays
    """
    if image.ndim == 3:
        u = image[:, :, u_channel].astype(np.float32) / 255.0
    else:
        u = image.astype(np.float32) / 255.0
    if invert:
        u = 1.0 - u
    if v_channel is not None and image.ndim == 3:
        v = image[:, :, v_channel].astype(np.float32) / 255.0
        if invert:
            v = 1.0 - v
    else:
        v = 1.0 - u
    return u, v
