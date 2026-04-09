"""
Test Laplacian operator implementations.
"""
import numpy as np
import pytest
from core.laplacian import (
    laplacian_5point,
    laplacian_9point,
    laplacian_convolution,
    KERNEL_5POINT,
    KERNEL_9POINT
)


class TestLaplacianProperties:
    """Test mathematical properties of Laplacian operators."""
    
    def test_laplacian_of_constant_is_zero(self):
        """∇²(c) = 0 for constant c."""
        const = np.ones((64, 64))
        for lap_fn in [laplacian_5point, laplacian_9point]:
            result = lap_fn(const)
            assert np.allclose(result, 0, atol=1e-10)
    
    def test_laplacian_of_linear_is_zero(self):
        """∇²(ax + by) = 0 (linear function)."""
        x = np.linspace(0, 1, 64)
        y = np.linspace(0, 1, 64)
        X, Y = np.meshgrid(x, y)
        linear = 2*X + 3*Y
        
        # Note: discrete Laplacian has error for linear functions
        # due to discretization, but should be small
        result_5 = laplacian_5point(linear)
        result_9 = laplacian_9point(linear)
        
        assert np.abs(result_5).max() < 0.1
        assert np.abs(result_9).max() < 0.01  # 9-point more accurate
    
    def test_laplacian_of_quadratic(self):
        """∇²(x² + y²) = 4 (constant)."""
        x = np.linspace(-1, 1, 64)
        y = np.linspace(-1, 1, 64)
        X, Y = np.meshgrid(x, y)
        quadratic = X**2 + Y**2
        
        result = laplacian_9point(quadratic)
        # Interior should be approximately 4
        interior = result[10:-10, 10:-10]
        assert np.allclose(interior, 4.0, rtol=0.1)
    
    def test_kernel_sum_to_zero(self):
        """Laplacian kernels must sum to zero."""
        assert np.isclose(KERNEL_5POINT.sum(), 0)
        assert np.isclose(KERNEL_9POINT.sum(), 0)
    
    def test_rotational_symmetry_9point(self):
        """9-point kernel should be more isotropic than 5-point."""
        # Create circular pattern
        x = np.linspace(-1, 1, 64)
        X, Y = np.meshgrid(x, x)
        circle = (X**2 + Y**2 < 0.5).astype(float)
        
        lap_5 = laplacian_5point(circle)
        lap_9 = laplacian_9point(circle)
        
        # Measure anisotropy by comparing diagonal vs cardinal responses
        center = 32
        # 9-point should have more uniform response around circle
        angles = np.linspace(0, 2*np.pi, 16, endpoint=False)
        radius = 10
        samples_5 = []
        samples_9 = []
        for angle in angles:
            dx = int(radius * np.cos(angle))
            dy = int(radius * np.sin(angle))
            samples_5.append(lap_5[center+dy, center+dx])
            samples_9.append(lap_9[center+dy, center+dx])
        
        # Lower variance = more isotropic
        assert np.std(samples_9) < np.std(samples_5)


class TestLaplacianBoundaryConditions:
    """Test periodic boundary implementation."""
    
    def test_periodicity_horizontal(self):
        """Values should wrap horizontally."""
        field = np.random.random((32, 32))
        result = laplacian_9point(field)
        # Left and right edges should be consistent
        assert np.allclose(result[:, 0], result[:, -1], rtol=0.1)
    
    def test_periodicity_vertical(self):
        """Values should wrap vertically."""
        field = np.random.random((32, 32))
        result = laplacian_9point(field)
        # Top and bottom edges should be consistent
        assert np.allclose(result[0, :], result[-1, :], rtol=0.1)


class TestConvolutionEquivalence:
    """Test that convolution matches direct implementation."""
    
    def test_convolution_vs_direct_5point(self):
        field = np.random.random((64, 64))
        direct = laplacian_5point(field)
        conv = laplacian_convolution(field, KERNEL_5POINT)
        assert np.allclose(direct, conv, rtol=1e-5)
    
    def test_convolution_vs_direct_9point(self):
        field = np.random.random((64, 64))
        direct = laplacian_9point(field)
        conv = laplacian_convolution(field, KERNEL_9POINT)
        assert np.allclose(direct, conv, rtol=1e-5)
