# Bifurcation Theory — Why Patterns Form Where They Do

Source: ITP Frankfurt / Goethe University (Claudius Gros group)

## Non-Diffusive Analysis (Well-Mixed ODE)

Strip diffusion terms to analyze fixed points:

$$\frac{du}{dt} = -uv^2 + F(1-u)$$
$$\frac{dv}{dt} = +uv^2 - (F+k)v$$

## Fixed Points

### Trivial Fixed Point (Always Exists)
$$(u_0^*, v_0^*) = (1, 0)$$

Jacobian eigenvalues: $-F$ and $-(F+k)$ — **always stable**.

### Non-Trivial Fixed Points (Conditional)

Exist only when: $F > 4(F+k)^2$

$$u^* = \frac{1 \pm \sqrt{1 - 4(F+k)^2/F}}{2}$$
$$v^* = \frac{1 \mp \sqrt{1 - 4(F+k)^2/F}}{2(F+k)}$$

Two fixed points appear simultaneously at the **saddle-node bifurcation**.

## The Two Critical Boundaries

### Boundary 1: Saddle-Node Bifurcation
$$F = 4(F+k)^2$$

Or as quadratic in F:
$$4F^2 + (8k-1)F + 4k^2 = 0$$

Non-trivial fixed points appear (upper branch) or disappear (lower branch).

### Boundary 2: Hopf Bifurcation
$$(F+k)^2 = F\sqrt{k}$$

Where stable fixed point becomes **unstable focus** — oscillatory dynamics begin.

## Parameter Space Regimes

**Outside both boundaries:**
→ Only trivial (1,0) fixed point exists
→ Far from boundaries: uniform steady state (boring)
→ Near saddle-node: patterns possible with sufficient seeding

**Between boundaries (saddle-node crossed, Hopf not):**
→ Three fixed points exist
→ Non-trivial FP2 is stable node/focus
→ Bistability: homogeneous state AND patterns coexist
→ Spatial fronts propagate between regions

**Inside both boundaries:**
→ FP2 is unstable focus (oscillatory)
→ Spatiotemporal chaos: α, β, ξ types

## Why NOT Classical Turing Instability

At trivial fixed point $(1,0)$, Jacobian is:
$$J_0 = \begin{bmatrix} -F & 0 \\ 0 & -(F+k) \end{bmatrix}$$

**Diagonal with negative eigenvalues** — no off-diagonal coupling. Diffusion cannot destabilize this.

Instead: **subcritical/excitable instability** — finite-amplitude perturbations trigger self-sustaining patterns. This is why seeding strategy matters critically.

## Phase Space Structure

The U-V plane reveals:
- **Isoclines**: du/dt=0 (green) and dv/dt=0 (red) curves
- **Attractor distribution**: Patterned states cluster at specific (u,v) values
- **Transient dynamics**: Watch distribution bifurcate from point to manifold

## Python: Compute Boundaries

```python
import numpy as np
from scipy.optimize import brentq

def saddle_node_boundary(k_vals):
    """Upper and lower F branches for saddle-node curve."""
    F_vals = []
    for k in k_vals:
        a, b, c = 4, 8*k - 1, 4*k**2
        disc = b**2 - 4*a*c
        if disc >= 0:
            F1 = (-b + np.sqrt(disc)) / (2*a)
            F2 = (-b - np.sqrt(disc)) / (2*a)
            F_vals.append((max(F1, F2), min(F1, F2)))
        else:
            F_vals.append((np.nan, np.nan))
    return np.array(F_vals)

def hopf_boundary(k_vals):
    """F values at Hopf bifurcation."""
    F_vals = []
    for k in k_vals:
        try:
            F = brentq(lambda F: (F+k)**2 - F*np.sqrt(k), 1e-6, 0.2)
            F_vals.append(F)
        except ValueError:
            F_vals.append(np.nan)
    return np.array(F_vals)
```

## Implications for Implementation

1. **Seeding amplitude**: Use u≈0.5, v≈0.25, not tiny noise
2. **Parameter sensitivity**: Crescent region is exquisitely sensitive
3. **Bistability**: Can have pattern and uniform state coexisting
4. **Oscillation**: Inside both boundaries = genuine temporal chaos
