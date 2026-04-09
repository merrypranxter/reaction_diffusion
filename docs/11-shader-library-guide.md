# GLSL Shader Library Guide

> **Audience**: WebGL/GLSL developers integrating Gray-Scott reaction-diffusion into real-time rendering pipelines.  
> **Coverage**: Every shader in `shaders/`, the math behind each choice, performance guidance, and extension patterns.

---

## Table of Contents

1. [Shader Overview](#1-shader-overview)
2. [The Gray-Scott Fragment Shader (`gray-scott-sim.frag`)](#2-the-gray-scott-fragment-shader)
   - [Uniform Reference](#21-uniform-reference)
   - [The Karl Sims 9-Point Laplacian](#22-the-karl-sims-9-point-laplacian)
   - [Reaction Step](#23-reaction-step)
   - [Stability Constraints](#24-stability-constraints)
3. [Color Ramp Library (`color-ramps.glsl`)](#3-color-ramp-library)
   - [Turbo Colormap](#31-turbo-colormap)
   - [Inferno Colormap](#32-inferno-colormap)
   - [Reaction-Diffusion Two-Tone](#33-reaction-diffusion-two-tone)
   - [Psychedelic Cycling](#34-psychedelic-cycling)
4. [Munafo Display Shader (`display-munafo.frag`)](#4-munafo-display-shader)
5. [Boundary Conditions](#5-boundary-conditions)
6. [Performance Optimization Patterns](#6-performance-optimization-patterns)
7. [Swapping Color Mapping Shaders](#7-swapping-color-mapping-shaders)
8. [Extending the Library](#8-extending-the-library)

---

## 1. Shader Overview

The shader pipeline has two stages:

```
CPU seed data  →  [Simulation Shader]  →  ping-pong texture  →  [Display Shader]  →  screen
                  gray-scott-sim.frag        (loop N times)       display-munafo.frag
```

- **Simulation shader** (`gray-scott-sim.frag`): Reads current state from a float texture, computes one Gray-Scott timestep, writes new state. Run in a render-to-texture loop (ping-pong).
- **Display shader** (`display-munafo.frag` or custom): Reads the final state texture and converts chemical concentrations to visible RGB colors.

The two stages are deliberately separate so you can swap display shaders without touching simulation logic.

---

## 2. The Gray-Scott Fragment Shader

**File**: `shaders/gray-scott-sim.frag`

This is the heart of the system. One call per pixel, one Gray-Scott timestep per call.

### 2.1 Uniform Reference

| Uniform | Type | Typical Value | Description |
|---------|------|--------------|-------------|
| `uState` | `sampler2D` | — | Current state texture. Red channel = U concentration, Green channel = V concentration. |
| `uResolution` | `vec2` | `(512.0, 512.0)` | Texture dimensions in pixels. Used to convert UV coordinates to texel offsets. |
| `uFeedRate` | `float` | `0.030–0.090` | Feed rate `F`. Controls how fast the substrate U is replenished. |
| `uKillRate` | `float` | `0.039–0.067` | Kill rate `k`. Controls how fast the product V is removed. |
| `uDiffusionU` | `float` | `1.0` | Diffusion coefficient for U. Almost always 1.0 — defines the unit of diffusion. |
| `uDiffusionV` | `float` | `0.5` | Diffusion coefficient for V. Standard Gray-Scott uses Du/Dv = 2:1. |
| `uDeltaT` | `float` | `1.0` | Timestep size. Reduce for stability at extreme parameters. |

**Why these specific uniforms?**  
F and k are the two degrees of freedom that determine which Pearson type emerges — they're the axes of Munafo's parameter map. Du and Dv set the diffusion ratio; the 2:1 convention (Du=1, Dv=0.5) matches Pearson's original 1993 paper. dt=1.0 is at the stability edge for the standard parameter range.

### 2.2 The Karl Sims 9-Point Laplacian

```glsl
vec2 laplacian(sampler2D tex, vec2 uv, vec2 texel) {
    vec2 sum = vec2(0.0);
    
    // Cardinal neighbors (weight 0.2)
    sum += texture(tex, uv + vec2(-1.0,  0.0) * texel).rg * 0.2;
    sum += texture(tex, uv + vec2( 1.0,  0.0) * texel).rg * 0.2;
    sum += texture(tex, uv + vec2( 0.0, -1.0) * texel).rg * 0.2;
    sum += texture(tex, uv + vec2( 0.0,  1.0) * texel).rg * 0.2;
    
    // Diagonal neighbors (weight 0.05)
    sum += texture(tex, uv + vec2(-1.0, -1.0) * texel).rg * 0.05;
    sum += texture(tex, uv + vec2( 1.0, -1.0) * texel).rg * 0.05;
    sum += texture(tex, uv + vec2(-1.0,  1.0) * texel).rg * 0.05;
    sum += texture(tex, uv + vec2( 1.0,  1.0) * texel).rg * 0.05;
    
    // Center (weight -1.0)
    sum -= texture(tex, uv).rg;
    
    return sum;
}
```

**Why 9 points?** The standard 5-point Laplacian (cardinal neighbors only) introduces directional artifacts — patterns elongate along axis directions. The 9-point stencil adds diagonal contributions that produce more isotropic (direction-independent) diffusion.

**Why these specific weights?** The weights sum to zero (−1.0 + 4×0.2 + 4×0.05 = 0) — this is a property of all correct discrete Laplacian stencils. The 4:1 ratio between cardinal (0.2) and diagonal (0.05) weights follows the standard D2Q9 lattice Boltzmann weighting, which Sims adopted for reaction-diffusion because it produces near-perfect circular diffusion fronts.

**Weight derivation** (for the curious):
- For a 2D isotropic discrete Laplacian: cardinal weight = `4/(h²·(4+4·ω))`, diagonal weight = `ω·(cardinal)`
- With ω = 0.25 (the Sims choice) and h=1: cardinal = 0.2, diagonal = 0.05 ✓

**Simultaneous computation of U and V**: The `.rg` swizzle reads both channels at once, allowing a single texture sample to update both chemicals. This halves the texture bandwidth compared to two separate passes.

### 2.3 Reaction Step

```glsl
float reaction = u * v * v;    // autocatalytic: U + 2V → 3V

float du = uDiffusionU * lap.r - reaction + uFeedRate * (1.0 - u);
float dv = uDiffusionV * lap.g + reaction - (uFeedRate + uKillRate) * v;
```

This is the Gray-Scott model verbatim:

```
∂u/∂t = Du·∇²u  −  u·v²  +  F·(1−u)
∂v/∂t = Dv·∇²v  +  u·v²  −  (F+k)·v
```

- `u·v²`: Autocatalytic reaction. V catalyzes its own production from U. The squared term creates the non-linear threshold behavior responsible for pattern formation.
- `F·(1−u)`: Feed term. Restores U toward 1.0 at rate F. If u=1, no feed; if u=0, maximum feed.
- `(F+k)·v`: Kill term. Removes V. The combined rate (F+k) ensures V is destroyed at least as fast as it's created in the uniform state.

### 2.4 Stability Constraints

The explicit Euler integration scheme is conditionally stable. Instability manifests as values escaping [0,1] or NaN propagation — hence the `clamp()` at the end.

**Maximum stable dt** is governed by the CFL condition:
```
dt_max ≈ 1 / (2 * Du * (4 * 0.2 + 4 * 0.05))   ≈  1 / (2 * 1.0 * 1.0)  ≈  0.5–1.0
```

**In practice:**
- `dt = 1.0` is stable for the standard Pearson parameters (F: 0.01–0.09, k: 0.04–0.07)
- `dt = 0.5` is safe for all parameters, including edge cases
- `dt > 1.0` produces instability, visible as bright noise or checkerboard artifacts
- `dt < 0.5` gives smoother, slower convergence — useful for ultra-high-detail renders

**Rule of thumb**: If you see pixel-level noise after 10 iterations, halve dt first.

---

## 3. Color Ramp Library

**File**: `shaders/color-ramps.glsl`

A library of reusable colormap functions. Include in display shaders with `#include` or copy-paste (WebGL doesn't have native includes — use string concatenation or a preprocessor).

### 3.1 Turbo Colormap

```glsl
vec3 turbo(float t)
```

Google's Turbo colormap — perceptually linear, rainbow-like but with uniform luminance gradient. Excellent for visualizing the full range of V concentrations in complex patterns (spiral types, chaotic types).

**Best for**: α (Wavelet Chaos), β (Ocean Voids), ξ (Spirals), π (U-Skate World)  
**Mapping**: Pass V concentration directly: `turbo(texture(uState, vUv).g)`

### 3.2 Inferno Colormap

```glsl
vec3 inferno(float t)
```

Black → purple → orange → yellow. Perceptually uniform, dark-to-light. Great for scientific visualization or dark-themed generative art.

**Best for**: ε (Chaotic Mitosis), ζ (Stable Spots), any dark-background aesthetic  
**Mapping**: `inferno(v)` where `v = texture(uState, vUv).g`

### 3.3 Reaction-Diffusion Two-Tone

```glsl
vec3 rd_twotone(float v, vec3 colorA, vec3 colorB)
```

Simple linear interpolation between two colors. The workhorse for biological pattern aesthetics.

**Examples**:
```glsl
// Cheetah spots (delta type)
rd_twotone(v, vec3(0.91, 0.83, 0.63), vec3(0.1, 0.06, 0.0))

// Zebra stripes (mu type)
rd_twotone(v, vec3(1.0), vec3(0.0))

// Ocean (beta type)
rd_twotone(v, vec3(0.0, 0.05, 0.2), vec3(0.0, 0.4, 1.0))
```

### 3.4 Psychedelic Cycling

```glsl
vec3 rd_psychedelic(float v, float time)
```

Cycles hue with time, creating animated color flow even on static patterns. The `time` uniform is incremented each frame.

**Best for**: Adding motion to otherwise-static patterns (δ, λ, θ), looping animations, music visualizer aesthetics.

```glsl
// In display shader with time uniform:
uniform float uTime;
// ...
vec3 col = rd_psychedelic(texture(uState, vUv).g, uTime * 0.5);
```

---

## 4. Munafo Display Shader

**File**: `shaders/display-munafo.frag`

Robert Munafo's coloring scheme, which encodes both the current state and the rate of change (activity) in the display. This requires two state textures: current and previous.

**How it works**:
1. Read current U (concentration) → controls hue (blue=low, red=high)
2. Compute `du/dt = (u_current - u_previous) / dt` → controls brightness
3. Multiply color by `(0.5 + |du/dt| * 10)` — active regions light up

**The result**: Static regions appear at half-brightness; active fronts (wavefronts, splitting events, spiral tips) blaze at full brightness. This is the classic "glowing wavefront" look.

**Shader requirements**: Needs a third uniform `uPreviousState` pointing to the render target from two frames ago (not the immediate previous — the current ping-pong write target is the immediate previous, you need the one before that).

**Alternative**: Comment out the brightness modulation and uncomment the HSL line for a smooth hue-mapped version.

---

## 5. Boundary Conditions

All shaders in this library use **periodic (toroidal) boundary conditions** via WebGL texture wrapping:

```javascript
// Three.js / WebGL texture setup
texture.wrapS = THREE.RepeatWrapping;   // horizontal wrap
texture.wrapT = THREE.RepeatWrapping;   // vertical wrap
```

This means:
- Left edge wraps to right edge
- Top edge wraps to bottom edge
- The domain is topologically a torus

**Why toroidal?**  
Boundary artifacts (fixed-value or zero-flux boundaries) create artificial stripe/spot nucleation at edges that dominates the pattern. Toroidal conditions let patterns form freely and are much more representative of "infinite" chemistry.

**To implement non-periodic boundaries** (fixed-value walls):
1. Change texture wrapping to `ClampToEdgeWrapping`
2. Add edge masking in the sim shader:
```glsl
// In gray-scott-sim.frag, before the final write:
vec2 edgeDist = min(vUv, 1.0 - vUv);
float isBorder = step(1.5 / uResolution.x, edgeDist.x) * 
                 step(1.5 / uResolution.y, edgeDist.y);
fragColor = mix(vec4(1.0, 0.0, 0.0, 1.0), fragColor, isBorder);
```

---

## 6. Performance Optimization Patterns

### 6.1 Reduced Precision

For faster mobile/embedded rendering, downgrade to `mediump`:
```glsl
precision mediump float;  // instead of highp
```

**Trade-off**: Slight visible artifacts in some parameter regimes. Test δ (Turing Spots) first — it's the most sensitive to precision loss.

### 6.2 Texture Format Optimization

Float textures (default) give full precision. For a 2× memory/bandwidth gain:
```javascript
// Use half-float (16-bit) textures
type: THREE.HalfFloatType   // instead of THREE.FloatType
```

**Trade-off**: Values outside [0,1] can lose precision. Monitor with the clamp behavior — if patterns look blocky, switch back to FloatType.

### 6.3 Multiple Steps Per Frame

The biggest performance gain: run N simulation steps before each display render.
```javascript
// In animation loop — balance visual smoothness vs compute cost
for (let i = 0; i < stepsPerFrame; i++) {
    sim.step();   // render-to-texture
}
sim.render();     // display once
```

Typical values: 8–32 steps/frame. Higher values = faster pattern development, but individual events (splits, wavefronts) may be skipped visually.

### 6.4 Resolution Scaling

Resolution scaling has an O(N²) effect on computation:

| Resolution | Relative cost |
|-----------|--------------|
| 256² | 1× |
| 512² | 4× |
| 1024² | 16× |
| 2048² | 64× |

For interactive use: 512². For export/print renders: 2048–4096².

### 6.5 Texture Caching

If you are switching between presets frequently, cache textures rather than destroying and recreating render targets:
```javascript
// Pre-allocate a pool of render targets
const targetPool = Array.from({length: 4}, () => createRenderTarget(size));
// Swap from pool instead of creating new
```

---

## 7. Swapping Color Mapping Shaders

The simulation shader and display shader are independent — swap the display shader at any time without resetting the simulation.

**Pattern**:
```javascript
// After creating simMaterial (simulation):
const displayMaterials = {
    munafo: createMunafoMaterial(),
    turbo: createTurboMaterial(),
    twotone: createTwotoneMaterial(colorA, colorB),
    psychedelic: createPsychedelicMaterial()
};

let activeDisplay = 'turbo';

function render() {
    // ... simulation steps ...
    
    // Swap display shader based on user preference
    const mat = displayMaterials[activeDisplay];
    mat.uniforms.uState.value = targets[currentTarget].texture;
    plane.material = mat;
    renderer.setRenderTarget(null);
    renderer.render(scene, camera);
}
```

**Real-time colormap swap**: Update the display material without recreating it by modifying uniforms:
```javascript
// For two-tone: update color uniforms live
displayMaterial.uniforms.uColorA.value = new THREE.Color(hex1);
displayMaterial.uniforms.uColorB.value = new THREE.Color(hex2);
```

---

## 8. Extending the Library

### 8.1 Adding a New Colormap

Add a new function to `color-ramps.glsl`:
```glsl
// Example: leopard skin colormap
vec3 leopard(float t) {
    vec3 bg = vec3(0.85, 0.72, 0.40);   // tawny background
    vec3 spot = vec3(0.15, 0.08, 0.0);  // dark brown spots
    float edge = smoothstep(0.15, 0.35, t);
    return mix(bg, spot, edge);
}
```

### 8.2 Adding a Three-Chemical System

The current shader packs U and V in `.rg`. To add a third chemical W:
1. Pack U in `.r`, V in `.g`, W in `.b`
2. Add a third laplacian call for `.b` channel
3. Add W's equation in the reaction step

```glsl
// Three-component Laplacian in gray-scott-sim.frag
vec3 lap = laplacian3(uState, vUv, texel);  // returns .rgb
float w = state.b;
float dw = uDiffusionW * lap.b + ...; // Lengyel-Epstein or custom
```

### 8.3 Parameter Animation

Animate F and k over time by binding to time-varying uniforms:
```javascript
// Slow parameter drift through Pearson space
const t = performance.now() * 0.0001;
simMaterial.uniforms.uFeedRate.value = 0.030 + 0.020 * Math.sin(t);
simMaterial.uniforms.uKillRate.value = 0.055 + 0.010 * Math.sin(t * 1.3);
```

This creates smooth transitions between Pearson types — watch the spots morph into stripes and back.

### 8.4 Multi-Scale Laplacian

For smoother, larger-scale patterns, use a larger stencil (5×5 instead of 3×3):
```glsl
// 25-point Laplacian for larger diffusion scale
vec2 laplacian5x5(sampler2D tex, vec2 uv, vec2 texel) {
    vec2 sum = vec2(0.0);
    // ... 24 neighbor samples with appropriate weights ...
    sum -= texture(tex, uv).rg * weightCenter;
    return sum;
}
```

This increases the characteristic wavelength of patterns, useful for lower-resolution canvases or stylized renders.
