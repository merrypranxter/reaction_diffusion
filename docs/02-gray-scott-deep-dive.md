# Gray-Scott Model — Deep Dive

## The Chemistry

Two irreversible reactions:
$$U + 2V \rightarrow 3V \quad \text{(autocatalytic)}$$
$$V \rightarrow P \quad \text{(decay to inert product)}$$

The $uv^2$ term derives from mass action kinetics: rate proportional to $[U]^1[V]^2$.

## The Equations

$$\frac{\partial u}{\partial t} = D_u \nabla^2 u - uv^2 + F(1-u)$$
$$\frac{\partial v}{\partial t} = D_v \nabla^2 v + uv^2 - (F+k)v$$

### Term Breakdown

| Term | Equation | Physical Meaning |
|------|----------|------------------|
| $D_u \nabla^2 u$ | u-equation | U diffuses (spreads) |
| $-uv^2$ | both | U consumed, V produced (autocatalysis) |
| $+F(1-u)$ | u-equation | U replenished toward 1.0 at rate F |
| $-(F+k)v$ | v-equation | V removed at combined rate (F+k) |

## Parameter Space

### Feed Rate F (0.01 – 0.10)
Controls membrane permeability / replenishment rate of U.

### Kill Rate k (0.03 – 0.07)
Controls decay rate of V to inert product P.

### Diffusion Ratio D = D_v/D_u

| D Value | Behavior |
|---------|----------|
| 0.5 | Standard, rich pattern space |
| < 1 | Reduced patterned regions |
| > 1 | More patterns, more stationary |

VisualPDE uses D=2 (different formulation where D_v appears explicitly).

## Discretization

```python
# Forward Euler, explicit
u_next = u + dt * (Du * laplacian(u) - u*v*v + F*(1-u))
v_next = v + dt * (Dv * laplacian(v) + u*v*v - (F+k)*v)
```

## Initialization Strategy

Critical insight from Frankfurt analysis: **finite-amplitude perturbations required**.

```python
# Background state
u = np.ones((n, n))  # U = 1 everywhere
v = np.zeros((n, n))  # V = 0 everywhere

# Seed region (must be substantial, not tiny noise)
center = (n//2, n//2)
radius = n // 10
u[center] = 0.5  # Deplete U
v[center] = 0.25  # Inject V
```

Different seeding reveals different pattern types — this is not classical Turing instability but **subcritical/excitable dynamics**.

## Key References
* Gray & Scott (1984) — Original CSTR model
* Pearson (1993) — Classification of 14 types
* Munafo (2009-2014) — Extended to 17 types, U-Skate World
* ITP Frankfurt — Bifurcation analysis, pattern mechanism
