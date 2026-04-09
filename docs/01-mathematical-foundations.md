# Mathematical Foundations

## The Reaction-Diffusion Master Equations

All Turing pattern formation derives from coupled PDEs tracking chemical concentrations:

$$\frac{\partial u}{\partial t} = D_u \nabla^2 u + f(u,v)$$
$$\frac{\partial v}{\partial t} = D_v \nabla^2 v + g(u,v)$$

Where:
- $u(\mathbf{x}, t)$ — activator concentration
- $v(\mathbf{x}, t)$ — inhibitor concentration
- $D_u, D_v$ — diffusion coefficients
- $\nabla^2$ — Laplacian operator (spatial spreading)
- $f, g$ — nonlinear reaction kinetics

## Turing Instability Conditions

For spontaneous pattern formation from uniform state:

1. **Differential diffusion**: $D_v > D_u$ (inhibitor spreads faster)
2. **Local activation**: $\frac{\partial f}{\partial u} > 0$ near fixed point
3. **Long-range inhibition**: $\frac{\partial g}{\partial v} < 0$ with sufficient magnitude

The characteristic wavelength emerges from:

$$\lambda_c = 2\pi\sqrt{\frac{D_u D_v}{D_v f_u - D_u g_v}}$$

## Discrete Laplacian Operators

### 5-Point Stencil (Unweighted)
```
  0   1   0
  1  -4   1
  0   1   0
```

### 9-Point Weighted (Karl Sims)
```
0.05  0.20  0.05
0.20 -1.00  0.20
0.05  0.20  0.05
```

The 9-point version better approximates rotational symmetry and reduces grid anisotropy.

## Forward Euler Discretization

$$u^{n+1} = u^n + \Delta t \cdot \frac{\partial u}{\partial t}$$

**Stability constraint**: $\Delta t \leq \frac{(\Delta x)^2}{4D_{max}}$ for explicit schemes.

## References
- Turing (1952) — "The Chemical Basis of Morphogenesis"
- Murray (2003) — *Mathematical Biology*, 3rd Ed.
