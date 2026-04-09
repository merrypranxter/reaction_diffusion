# Alternative Reaction-Diffusion Models

## Belousov-Zhabotinsky (BZ) Reaction

**Type**: Excitable oscillator (not static Turing)
**Behavior**: Target patterns, spiral waves, 3D scroll waves
**Math**: Oregonator model (simplified)

```python
# Three-variable Oregonator
epsilon * dx/dt = x + y - q*x**2 - x*y
dy/dt = -y + 2*f*z - x*y
dz/dt = x - z
```

**Key feature**: Refractory period — waves annihilate on collision, creating "collision scars"

## Schnakenberg Model

**Type**: Cross-diffusion
**Behavior**: Shape-shifting grids — stripes snap into hexagons/rhombuses
**Math**: Cross-diffusion terms where ∇u drives v-flux and vice versa

## FitzHugh-Nagumo

**Origin**: Neural action potentials
**Behavior**: Pulsing capillaries, synaptic flashes traveling networks
**Use**: Biological neural tissue simulation

## Cahn-Hilliard

**Type**: Phase separation (not Turing)
**Math**:
$$\frac{∂ϕ}{∂t}=∇⋅\left(M∇μ\right), μ=\frac{δF}{δϕ}$$

**Behavior**: Spinodal decomposition, coarsening — "oil and water" separation
**Visual**: Marbled blobs that slowly coarsen, sharp interfaces

## Gray-Scott Extensions

### Porous Medium
Replace $∇^{2}u$ with $∇^{2}\left(u^{m}\right)$, m>1
**Effect**: Sharper edges, more geometric patterns

### Anisotropic Diffusion
Direction-dependent diffusion rates
**Effect**: Oriented stripes, flow-aligned patterns

### Flow Fields
Add advection: $v⋅∇u$
**Effect**: Dynamic flowing patterns, transport by velocity field
