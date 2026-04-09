"""
Laplacian operator implementations for reaction-diffusion.
"""
import numpy as np
from typing import Tuple

# 5-point unweighted stencil (fast, compatible)
KERNEL_5POINT = np.array([
    [0, 1, 0],
    [1, -4, 1],
    [0, 1, 0]
], dtype=np.float32)

# 9-point weighted (Karl Sims) — better isotropy
KERNEL_9POINT = np.array([
    [0.05, 0.20, 0.05],
    [0.20, -1.00, 0.20],
    [0.05, 0.20, 0.05]
], dtype=np.float32)

# 9-point unweighted (alternative isotropic)
KERNEL_9POINT_UNWEIGHTED = np.array([
    [1, 1, 1],
    [1, -8, 1],
    [1, 1, 1]
], dtype=np.float32) / 8.0


def laplacian_5point(field: np.ndarray) -> np.ndarray:
    """
    Compute Laplacian using 5-point stencil.
    Assumes periodic boundary conditions (wrap-around).
    
    Args:
        field: 2D array of shape (n, n)
        
    Returns:
        Laplacian of same shape (n, n)
    """
    n = field.shape[0]
    result = np.zeros_like(field)
    
    # Interior points
    result[1:-1, 1:-1] = (
        field[:-2, 1:-1] +   # up
        field[2:, 1:-1] +    # down
        field[1:-1, :-2] +   # left
        field[1:-1, 2:] -    # right
        4 * field[1:-1, 1:-1]  # center
    )
    
    # Periodic boundaries
    result[0, :] = field[-1, :] + field[1, :] + field[0, -1] + field[0, 1] - 4*field[0, :]
    result[-1, :] = field[-2, :] + field[0, :] + field[-1, -1] + field[-1, 1] - 4*field[-1, :]
    result[:, 0] = field[-1, 0] + field[1, 0] + field[:, -1] + field[:, 1] - 4*field[:, 0]
    result[:, -1] = field[-1, -1] + field[1, -1] + field[:, -2] + field[:, 0] - 4*field[:, -1]
    
    return result


def laplacian_9point(field: np.ndarray, weighted: bool = True) -> np.ndarray:
    """
    Compute Laplacian using 9-point stencil.
    
    Args:
        field: 2D array
        weighted: Use Karl Sims weights (True) or unweighted (False)
        
    Returns:
        Laplacian of same shape
    """
    kernel = KERNEL_9POINT if weighted else KERNEL_9POINT_UNWEIGHTED
    # Use convolution for cleaner implementation
    from scipy.ndimage import convolve
    return convolve(field, kernel, mode='wrap')


def laplacian_convolution(field: np.ndarray, kernel: np.ndarray = None) -> np.ndarray:
    """
    Generic convolution-based Laplacian with periodic BC.
    
    Args:
        field: 2D array
        kernel: Convolution kernel (default: 9-point weighted)
        
    Returns:
        Laplacian of same shape
    """
    if kernel is None:
        kernel = KERNEL_9POINT
    from scipy.ndimage import convolve
    return convolve(field, kernel, mode='wrap')
