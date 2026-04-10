# Three.js WebGL Gray-Scott Demo

> Interactive browser-based reaction-diffusion simulation using Three.js and WebGL. No build step required — runs directly from a static file server.

## Quick Start

```bash
# From the repository root:
python3 -m http.server 8000

# Then open in your browser:
http://localhost:8000/examples/threejs-webgl/
```

Any static file server works:
- `npx serve .` (Node.js)
- `php -S localhost:8000` (PHP)
- VS Code Live Server extension
- Any web hosting (GitHub Pages, Netlify, etc.)

## What You'll See

A real-time Gray-Scott reaction-diffusion simulation running at 512×512 pixels, with live controls:

| Control | Description | Default |
|---------|-------------|---------|
| **Feed (F)** | Feed rate — controls pattern type along the F-axis of Pearson space | 0.054 |
| **Kill (k)** | Kill rate — controls pattern type along the k-axis of Pearson space | 0.062 |
| **Steps/Frame** | Simulation steps run per animation frame | 16 |
| **Reset** | Reinitialize with the default center-circle seed | — |
| **Random Seed** | Reinitialize with a new random seed | — |

## Exploring Pearson Pattern Types

Navigate to these (F, k) values to see each named pattern type:

| Pattern | F | k | What to look for |
|---------|---|---|-----------------|
| Wavelet Chaos (α) | 0.010 | 0.047 | Turbulent overlapping waves |
| Ocean Voids (β) | 0.014 | 0.039 | Blue waves with dark drifting holes |
| Unstable Stripes (γ) | 0.022 | 0.051 | Fingerprint-like stripes rearranging |
| **Turing Spots (δ)** | **0.030** | **0.055** | Hexagonal cheetah-like spots |
| Chaotic Mitosis (ε) | 0.018 | 0.055 | Blobs dividing like cells |
| BZ Spirals (ξ) | 0.010 | 0.041 | Rotating chemical spirals |
| Hedgerow Mazes (κ) | 0.050 | 0.063 | Branching dendritic channels |
| Mitotic Hexagons (λ) | 0.026 | 0.061 | Honeycomb-ordered spots |
| Growing Worms (μ) | 0.046 | 0.065 | Parallel worm stripes |
| **U-Skate World (π)** | **0.062** | **0.061** | Moving autonomous structures |
| Red Soap Bubbles (ρ) | 0.090 | 0.059 | Cellular foam with warm tones |

**Tip**: Increase Steps/Frame to 32–50 for faster emergence. Static patterns (δ, λ, θ) take 2000–5000 iterations to fully develop.

## Technical Details

### Architecture

```
┌─────────────────────────────────────────┐
│  GrayScottWebGL class                   │
│  ├── Two WebGLRenderTarget (ping-pong)  │
│  ├── Simulation ShaderMaterial          │
│  │   └── Karl Sims 9-point Laplacian   │
│  └── Display ShaderMaterial            │
│      └── V-channel grayscale mapping   │
└─────────────────────────────────────────┘
```

### Ping-Pong Rendering

The simulation uses two render targets that alternate:
1. Read from Target A → compute new state → write to Target B
2. Read from Target B → compute new state → write to Target A
3. Repeat

This ensures each pixel's computation uses consistent neighbor values from the same timestep.

### Shader Details

**Simulation fragment shader** (embedded in `index.html`):
- Implements the Gray-Scott equations: `du/dt = Du·∇²u − u·v² + F·(1−u)`
- Uses Karl Sims' 9-point Laplacian (cardinal weight 0.2, diagonal weight 0.05)
- State stored in `.rg` channels: red=U, green=V
- Toroidal (periodic) boundary conditions via `RepeatWrapping`

**Display fragment shader** (also embedded):
- Maps V concentration to grayscale: `color = vec3(1.0 - v * 2.0)`
- Light areas = low V, dark areas = high V

### Float Texture Precision

Uses `THREE.FloatType` (full 32-bit float precision) for chemical concentrations. This is required for numerical stability at low F and k values. Falls back gracefully if only half-float is available.

## Extending This Demo

### Change the Color Scheme

Replace the display shader's `fragmentShader` string:

```javascript
// Inferno colormap (dark to bright)
fragmentShader: `
    precision highp float;
    uniform sampler2D uState;
    varying vec2 vUv;
    void main() {
        float v = texture2D(uState, vUv).g;
        vec3 c0 = vec3(0.0, 0.001, -0.019);
        vec3 c1 = vec3(0.107, 0.564, 3.933);
        vec3 c2 = vec3(11.6, -3.97, -15.94);
        gl_FragColor = vec4(clamp(c0 + v*(c1 + v*c2), 0.0, 1.0), 1.0);
    }
`
```

### Export a Frame

```javascript
// Paste in browser console while simulation is running:
sim.renderer.domElement.toBlob(blob => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'rd-frame.png';
    a.click();
}, 'image/png');
```

### Load from JSON Preset

```javascript
// Load Pearson types from the presets file
fetch('/presets/pearson-types.json')
    .then(r => r.json())
    .then(data => {
        const delta = data.pearson_types.find(t => t.type === 'δ');
        sim.setParams({ F: delta.F, k: delta.k });
    });
```

### Run at Higher Resolution

Change `this.size = 512` to `this.size = 1024` in the `GrayScottWebGL` constructor. Note this is 4× slower — reduce `stepsPerFrame` accordingly.

## Browser Compatibility

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome 90+ | ✅ Full | Best performance |
| Firefox 89+ | ✅ Full | |
| Safari 15+ | ✅ Full | WebGL 2 from iOS 15 |
| Safari 14 | ⚠️ Partial | WebGL 1 only, slightly slower |
| Mobile Chrome | ✅ Works | Reduce to 256² for smooth 30fps |
| Mobile Safari | ✅ Works | Same as Safari desktop |

## Related Files

- `shaders/gray-scott-sim.frag` — Production standalone simulation shader
- `shaders/display-munafo.frag` — Advanced display with du/dt activity mapping
- `shaders/color-ramps.glsl` — Reusable colormap functions
- `docs/11-shader-library-guide.md` — Complete GLSL documentation
- `docs/12-webgl-integration.md` — Full WebGL integration guide
- `presets/pearson-types.json` — All 19 Pearson type parameters
- `presets/visual-descriptions.json` — Visual character descriptions for AI prompting
- `prompts/pearson-type-prompts.json` — AI image generation prompts per type
