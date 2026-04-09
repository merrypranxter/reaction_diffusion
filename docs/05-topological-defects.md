# Topological Defects — The Anatomy of Pattern Failure

Real reaction-diffusion patterns contain structural "glitches" where geometry accommodates stress. These are essential for realistic rendering.

## Defect Types

### 1. Stripe Terminations (Phase Slips)
Single stripe abruptly ends.

**Visual**: T-junction, wedge deleted from barcode
**Mathematics**: Local wavelength jump in Swift-Hohenberg analysis
**Cause**: Parameter gradient sweeping system across stripe-spot boundary

### 2. Y-Splits (Triradius Junctions)
Single stripe bifurcates into two.

**Visual**: 3-way stitch, "bifurcation scar"
**Mathematics**: Curvature stress relief — stripe splits to accommodate geometric tension
**Cause**: Curvature in coordinate grid or inhomogeneous parameter sweep

### 3. Grain-Boundary Seams (Zipper Lines)
Two "continents" of stripes with different orientations collide.

**Visual**: Serrated, zipper-like wall of mismatching phase lines
**Mathematics**: Dislocation arrays where orientations cannot merge smoothly
**Cause**: Domain collision during pattern evolution

### 4. Coarsening Trenches (Annihilation Trenches)
Broad "healed" belts where smaller defects were consumed.

**Visual**: Smoother lane with fading stitch marks
**Mathematics**: Energy minimization — smaller domains shrink, larger grow (Cahn-Hilliard-like coarsening)
**Cause**: Late-stage pattern evolution, defect annihilation

### 5. Phase Singularities (Vortex Cores)
In BZ/excitable media: core of rotating spiral.

**Visual**: Point where phase undefined, concentration spins endlessly around it
**Mathematics**: Topological charge ±1, cannot be removed by continuous deformation

## Swift-Hohenberg Equation

Often used to analyze defect structure:

$$\frac{\partial u}{\partial t} = ru - (1 + \nabla^2)^2 u + u^3$$

Captures pattern formation with explicit control of wavelength and defect dynamics.

## GLSL: Intentional Defect Injection

```glsl
// Add noise to parameters for natural-looking defects
float F = uFeedRate + 0.001 * hash(uv * 123.45);
float k = uKillRate + 0.001 * hash(uv * 543.21);
```

Or spatially varying parameters to force defects:
```glsl
// Gradient across domain creates Y-splits
float F = mix(0.030, 0.034, uv.x); // δ to η transition
```

## Shader Render Tags
* "Swift-Hohenberg barcode break"
* "Triradius bifurcation scar"
* "Serrated phase-mismatch wall"
* "Defect annihilation trench"
