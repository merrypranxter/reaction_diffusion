"""
Test numerical stability and convergence.
"""
import numpy as np
import pytest
from core.gray_scott import GrayScottNumpy
from core.parameters import DELTA, R, B


class TestStability:
    """Test numerical stability criteria."""
    
    def test_explicit_euler_stability_limit(self):
        """Test that dt <= dx^2 / 4D for stability."""
        # With Du=1, Dv=0.5, dx=1, stability requires dt <= 0.25
        # But weighted kernel allows larger dt due to implicit smoothing
        sim = GrayScottNumpy(size=64, dt=1.0, **DELTA.with_diffusion())
        
        # Should not explode immediately
        for _ in range(100):
            sim.step()
        
        assert np.all(np.isfinite(sim.u))
        assert np.all(np.isfinite(sim.v))
        assert np.all(sim.u >= 0) and np.all(sim.u <= 1)
        assert np.all(sim.v >= 0) and np.all(sim.v <= 1)
    
    def test_mass_conservation_approximate(self):
        """Total mass should be approximately conserved."""
        sim = GrayScottNumpy(size=64, **DELTA.with_diffusion())
        initial_mass = sim.u.sum() + sim.v.sum()
        
        for _ in range(100):
            sim.step()
        
        final_mass = sim.u.sum() + sim.v.sum()
        # Not exact due to feed/kill, but shouldn't drift wildly
        assert abs(final_mass - initial_mass) / initial_mass < 0.5
    
    def test_clamping_enforces_bounds(self):
        """Values should stay in [0, 1] due to clamping."""
        sim = GrayScottNumpy(size=64, **DELTA.with_diffusion())
        
        # Force extreme values
        sim.u[32, 32] = 100
        sim.v[32, 32] = -50
        sim.step()
        
        assert np.all(sim.u >= 0) and np.all(sim.u <= 1)
        assert np.all(sim.v >= 0) and np.all(sim.v <= 1)


class TestPatternFormation:
    """Test that patterns actually form."""
    
    def test_delta_forms_turing_spots(self):
        """Delta type should form hexagonal spot pattern."""
        sim = GrayScottNumpy(size=128, **DELTA.with_diffusion())
        
        # Run to steady state
        sim.run(5000)
        
        # Should have variation (not uniform)
        assert sim.v.std() > 0.1
        
        # Should have multiple spots
        from scipy.ndimage import label
        spots, n_spots = label(sim.v > 0.5)
        assert n_spots > 5
    
    def test_r_converges_to_uniform(self):
        """R type should converge to uniform red state."""
        sim = GrayScottNumpy(size=64, **R.with_diffusion())
        sim.run(2000)
        
        # Should be nearly uniform
        assert sim.v.std() < 0.05
        assert sim.v.mean() > 0.8  # High V (red state)
    
    def test_b_converges_to_uniform(self):
        """B type should converge to uniform blue state."""
        sim = GrayScottNumpy(size=64, **B.with_diffusion())
        sim.run(2000)
        
        # Should be nearly uniform
        assert sim.v.std() < 0.05
        assert sim.v.mean() < 0.1  # Low V (blue state)


class TestConvergenceRate:
    """Test how quickly simulations converge."""
    
    def test_convergence_measured_by_variance(self):
        """Track variance over time as convergence metric."""
        sim = GrayScottNumpy(size=64, **DELTA.with_diffusion())
        
        variances = []
        for i in range(100):
            sim.step(50)
            variances.append(sim.v.var())
        
        # Variance should stabilize (not keep growing)
        late_var = np.mean(variances[-10:])
        early_var = np.mean(variances[10:20])
        assert abs(late_var - early_var) / early_var < 0.5
