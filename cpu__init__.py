"""
CPU implementations of Gray-Scott reaction-diffusion.
"""
from .numpy_vectorized import GrayScottNumpy as NumpyImpl

try:
    from .cython_accelerated import GrayScottCython as CythonImpl
except ImportError:
    CythonImpl = None

__all__ = ['NumpyImpl', 'CythonImpl']
