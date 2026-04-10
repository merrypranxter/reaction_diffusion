# WebGL Integration Guide

> **Audience**: JavaScript developers deploying Gray-Scott reaction-diffusion in browser environments.  
> **Coverage**: Full setup from scratch, ping-pong rendering, live controls, frame export, performance monitoring, and common pitfalls.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Canvas and Renderer Setup](#2-canvas-and-renderer-setup)
3. [Ping-Pong Texture Rendering](#3-ping-pong-texture-rendering)
4. [Seeding Initial Conditions](#4-seeding-initial-conditions)
5. [Simulation Loop](#5-simulation-loop)
6. [Real-Time Parameter Controls](#6-real-time-parameter-controls)
7. [Exporting Frames as Image or Video](#7-exporting-frames-as-image-or-video)
8. [Performance Monitoring](#8-performance-monitoring)
9. [Loading Pearson Presets](#9-loading-pearson-presets)
10. [Common Pitfalls and Fixes](#10-common-pitfalls-and-fixes)
11. [Minimal Standalone Example](#11-minimal-standalone-example)
12. [Deployment Notes](#12-deployment-notes)

---

## 1. Architecture Overview

Gray-Scott in WebGL requires a **render-to-texture loop** (ping-pong buffering) because each pixel's next state depends on its neighbors' current state — you cannot read and write the same texture simultaneously in a GPU shader.

```
┌──────────────────────────────────────────────────────────────┐
│  CPU: Initialize seed data (Float32Array)                     │
│       Upload to Texture A                                     │
└───────────────────────────────┬──────────────────────────────┘
                                │
              ┌─────────────────▼─────────────────┐
              │          SIMULATION LOOP           │
              │                                    │
              │  ┌──────────────┐                  │
              │  │  Texture A   │◄─────────────┐   │
              │  │ (read state) │              │   │
              │  └──────┬───────┘              │   │
              │         │                      │   │
              │  [sim shader: Gray-Scott step]  │   │
              │         │                      │   │
              │  ┌──────▼───────┐              │   │
              │  │  Texture B   │──────────────┘   │
              │  │ (write state)│  swap A↔B        │
              │  └──────┬───────┘                  │
              │         │ (after N steps)          │
              └─────────┼──────────────────────────┘
                        │
              ┌─────────▼───────────┐
              │  DISPLAY SHADER     │
              │  (colormap → screen)│
              └─────────────────────┘
```

**Key constraint**: Never render to the same texture you are reading from in the same draw call. Always alternate (A→B, then B→A, then A→B, ...).

---

## 2. Canvas and Renderer Setup

### With Three.js (recommended for most use cases)

```javascript
import * as THREE from 'three';

function setupRenderer(size = 512) {
    const renderer = new THREE.WebGLRenderer({ antialias: false });
    renderer.setSize(size, size);
    renderer.setPixelRatio(1);          // Always 1 for sim textures
    document.body.appendChild(renderer.domElement);
    
    // Check float texture support (required)
    const ext = renderer.extensions.get('OES_texture_float_linear');
    if (!ext) {
        console.warn('OES_texture_float_linear not available. Using nearest filtering.');
    }
    
    return renderer;
}
```

### Canvas Size Considerations

| Size | Use Case | Notes |
|------|----------|-------|
| 256² | Mobile, quick prototype | Fast but coarse patterns |
| 512² | Desktop interactive | Best balance of quality/speed |
| 1024² | High-detail display | May drop frames on integrated GPU |
| 2048²+ | Export/print renders | Use offline (non-realtime) loop |

### WebGL 2 vs WebGL 1

Three.js ≥ r125 defaults to WebGL 2 where available. For maximum compatibility:
```javascript
const renderer = new THREE.WebGLRenderer({
    antialias: false,
    powerPreference: 'high-performance'  // request discrete GPU on laptops
});
```

---

## 3. Ping-Pong Texture Rendering

The ping-pong system requires exactly two render targets of identical format.

```javascript
function createRenderTarget(size) {
    return new THREE.WebGLRenderTarget(size, size, {
        minFilter: THREE.NearestFilter,  // No interpolation — critical for accuracy
        magFilter: THREE.NearestFilter,
        format: THREE.RGBAFormat,
        type: THREE.FloatType,           // Full precision for chemical concentrations
        wrapS: THREE.RepeatWrapping,     // Toroidal boundary conditions
        wrapT: THREE.RepeatWrapping,
        depthBuffer: false,              // Optimization: no depth needed for 2D sim
        stencilBuffer: false
    });
}

// Create both targets
const targets = [createRenderTarget(SIZE), createRenderTarget(SIZE)];
let currentTarget = 0;  // Index of the current "read" target
```

**Swap pattern** (executed each simulation step):
```javascript
function simulationStep() {
    const readIdx  = currentTarget;
    const writeIdx = 1 - currentTarget;
    
    // Point sim shader at read texture
    simMaterial.uniforms.uState.value = targets[readIdx].texture;
    
    // Render into write target
    renderer.setRenderTarget(targets[writeIdx]);
    renderer.render(scene, camera);
    
    // Swap — the written result is now the new "current" state
    currentTarget = writeIdx;
}
```

**Why NearestFilter?** Linear interpolation between texels would blur the chemical field, causing nonphysical mixing of concentrations. Nearest-neighbor sampling preserves exact values at pixel centers.

---

## 4. Seeding Initial Conditions

The seed sets up the initial chemical state before simulation begins.

### Standard Center-Circle Seed

```javascript
function seedCenterCircle(size) {
    const data = new Float32Array(size * size * 4);
    
    // Initialize entire field: u=1, v=0 (uniform blue equilibrium)
    for (let i = 0; i < size * size; i++) {
        data[i * 4 + 0] = 1.0;  // U channel (red)
        data[i * 4 + 1] = 0.0;  // V channel (green)
        data[i * 4 + 2] = 0.0;  // unused
        data[i * 4 + 3] = 1.0;  // alpha
    }
    
    // Seed a circle with perturbation in the center
    const cx = size / 2, cy = size / 2, r = size / 10;
    for (let y = 0; y < size; y++) {
        for (let x = 0; x < size; x++) {
            if ((x - cx) ** 2 + (y - cy) ** 2 < r * r) {
                const idx = (y * size + x) * 4;
                data[idx + 0] = 0.5 + (Math.random() - 0.5) * 0.1;  // u
                data[idx + 1] = 0.25 + (Math.random() - 0.5) * 0.1; // v
            }
        }
    }
    
    return data;
}
```

### Scattered Noise Seed (faster emergence)

```javascript
function seedScatteredNoise(size, density = 0.02) {
    const data = new Float32Array(size * size * 4);
    for (let i = 0; i < size * size; i++) {
        data[i * 4 + 0] = 1.0;
        data[i * 4 + 3] = 1.0;
    }
    
    const nSeeds = Math.floor(size * size * density);
    for (let s = 0; s < nSeeds; s++) {
        const x = Math.floor(Math.random() * size);
        const y = Math.floor(Math.random() * size);
        const r = 2 + Math.floor(Math.random() * 3);
        for (let dy = -r; dy <= r; dy++) {
            for (let dx = -r; dx <= r; dx++) {
                if (dx * dx + dy * dy <= r * r) {
                    const px = (x + dx + size) % size;
                    const py = (y + dy + size) % size;
                    const idx = (py * size + px) * 4;
                    data[idx + 0] = 0.5;
                    data[idx + 1] = 0.25;
                }
            }
        }
    }
    return data;
}
```

### Uploading Seed to Both Targets

```javascript
function uploadSeed(renderer, scene, camera, targets, seedData, size) {
    const texture = new THREE.DataTexture(
        seedData, size, size, THREE.RGBAFormat, THREE.FloatType
    );
    texture.needsUpdate = true;
    
    // Use a simple pass-through shader to blit seed into both targets
    const blitMaterial = new THREE.MeshBasicMaterial({ map: texture });
    plane.material = blitMaterial;
    
    for (const target of targets) {
        renderer.setRenderTarget(target);
        renderer.render(scene, camera);
    }
    renderer.setRenderTarget(null);
    texture.dispose();
}
```

---

## 5. Simulation Loop

```javascript
let stepsPerFrame = 16;   // Tuneable: more = faster convergence, fewer = smoother animation
let iteration = 0;
let isRunning = true;

function animate() {
    if (!isRunning) return;
    requestAnimationFrame(animate);
    
    // Run N simulation steps
    for (let i = 0; i < stepsPerFrame; i++) {
        simulationStep();
        iteration++;
    }
    
    // Render to screen
    displayMaterial.uniforms.uState.value = targets[currentTarget].texture;
    plane.material = displayMaterial;
    renderer.setRenderTarget(null);
    renderer.render(scene, camera);
    
    // Update UI
    iterationDisplay.textContent = iteration;
}

animate();
```

**Pause/Resume**:
```javascript
function pause() { isRunning = false; }
function resume() { isRunning = true; animate(); }
```

---

## 6. Real-Time Parameter Controls

### Slider Binding

```javascript
function bindSlider(id, uniform, displayId, decimals = 3) {
    const slider = document.getElementById(id);
    const display = document.getElementById(displayId);
    
    slider.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        display.textContent = val.toFixed(decimals);
        simMaterial.uniforms[uniform].value = val;
        // Note: no simulation reset needed — parameters take effect immediately
    });
}

// Bind all parameters
bindSlider('feed',       'uFeedRate',    'feedVal');
bindSlider('kill',       'uKillRate',    'killVal');
bindSlider('diffU',      'uDiffusionU',  'diffUVal');
bindSlider('diffV',      'uDiffusionV',  'diffVVal');
bindSlider('dt',         'uDeltaT',      'dtVal',  2);
bindSlider('stepsFrame', 'stepsPerFrame', 'stepsVal', 0);  // not a shader uniform
```

### Preset Buttons

```javascript
const PRESETS = {
    "Turing Spots":    { F: 0.030, k: 0.055 },
    "Growing Worms":   { F: 0.046, k: 0.065 },
    "BZ Spirals":      { F: 0.010, k: 0.041 },
    "U-Skate World":   { F: 0.062, k: 0.061 },
    "Hedgerow Mazes":  { F: 0.050, k: 0.063 },
    "Mitotic Hexagons":{ F: 0.026, k: 0.061 },
};

Object.entries(PRESETS).forEach(([name, params]) => {
    const btn = document.createElement('button');
    btn.textContent = name;
    btn.addEventListener('click', () => {
        simMaterial.uniforms.uFeedRate.value = params.F;
        simMaterial.uniforms.uKillRate.value = params.k;
        // Update slider UI to match
        document.getElementById('feed').value = params.F;
        document.getElementById('kill').value = params.k;
        document.getElementById('feedVal').textContent = params.F.toFixed(3);
        document.getElementById('killVal').textContent = params.k.toFixed(3);
    });
    presetContainer.appendChild(btn);
});
```

### Color Scheme Selector

```javascript
const colorSchemes = {
    'grayscale': `
        void main() {
            float v = texture2D(uState, vUv).g;
            gl_FragColor = vec4(vec3(1.0 - v * 2.0), 1.0);
        }`,
    'twotone': `
        uniform vec3 uColorA;
        uniform vec3 uColorB;
        void main() {
            float v = texture2D(uState, vUv).g;
            gl_FragColor = vec4(mix(uColorA, uColorB, v * 3.0), 1.0);
        }`,
    // ... etc
};

function setColorScheme(name) {
    displayMaterial.fragmentShader = colorSchemes[name];
    displayMaterial.needsUpdate = true;
}
```

---

## 7. Exporting Frames as Image or Video

### Single Frame PNG Export

```javascript
function exportFrame(renderer, scene, camera, state, filename = 'rd-frame.png') {
    // Render at full resolution to a temporary larger canvas if needed
    renderer.setRenderTarget(null);
    
    // Ensure display render is current
    displayMaterial.uniforms.uState.value = state;
    plane.material = displayMaterial;
    renderer.render(scene, camera);
    
    renderer.domElement.toBlob((blob) => {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.click();
        URL.revokeObjectURL(url);
    }, 'image/png');
}
```

### High-Resolution Export

For print-quality exports at larger resolution than the simulation size:
```javascript
async function exportHighRes(size = 2048) {
    // Create temporary high-res renderer
    const exportRenderer = new THREE.WebGLRenderer({ preserveDrawingBuffer: true });
    exportRenderer.setSize(size, size);
    
    // Run sim at high res (or upscale display from existing state)
    // ... setup sim at size x size ...
    
    // Render final frame
    exportRenderer.render(scene, camera);
    exportRenderer.domElement.toBlob((blob) => {
        // ... download ...
    }, 'image/png');
    
    exportRenderer.dispose();
}
```

### Video Export (WebCodecs API)

```javascript
async function recordVideo(durationSeconds = 10, fps = 30) {
    const stream = renderer.domElement.captureStream(fps);
    const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'video/webm;codecs=vp9',
        videoBitsPerSecond: 8_000_000
    });
    
    const chunks = [];
    mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
    mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'video/webm' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `rd-pattern-${Date.now()}.webm`;
        link.click();
    };
    
    mediaRecorder.start();
    setTimeout(() => mediaRecorder.stop(), durationSeconds * 1000);
}
```

---

## 8. Performance Monitoring

### FPS Counter

```javascript
const fpsStats = {
    frames: 0,
    lastTime: performance.now(),
    fps: 0,
    
    update() {
        this.frames++;
        const now = performance.now();
        const elapsed = now - this.lastTime;
        if (elapsed >= 1000) {
            this.fps = Math.round(this.frames * 1000 / elapsed);
            this.frames = 0;
            this.lastTime = now;
        }
        return this.fps;
    }
};

// In animation loop:
fpsDisplay.textContent = fpsStats.update();
```

### GPU Memory Usage

WebGL doesn't expose direct memory usage, but you can estimate it:
```javascript
function estimateGPUMemoryMB(size, floatTextures = 2) {
    const bytesPerPixel = 4 * 4;  // RGBA * float32
    const bytes = size * size * bytesPerPixel * floatTextures;
    return (bytes / 1024 / 1024).toFixed(1);
}

console.log(`Estimated GPU VRAM: ${estimateGPUMemoryMB(512)} MB`);
// 512²: 8 MB, 1024²: 32 MB, 2048²: 128 MB
```

### Adaptive Quality

Drop resolution automatically if FPS falls below threshold:
```javascript
let currentSize = 512;

function adaptiveQuality(fps) {
    if (fps < 30 && currentSize > 256) {
        currentSize /= 2;
        resizeSimulation(currentSize);
        console.log(`Reduced to ${currentSize}² for performance`);
    } else if (fps > 55 && currentSize < 1024) {
        currentSize *= 2;
        resizeSimulation(currentSize);
        console.log(`Increased to ${currentSize}² for quality`);
    }
}
```

---

## 9. Loading Pearson Presets

```javascript
async function loadPearsonPresets() {
    const [types, metadata] = await Promise.all([
        fetch('/presets/pearson-types.json').then(r => r.json()),
        fetch('/presets/visual-metadata.json').then(r => r.json())
    ]);
    
    // Merge parameter data with visual metadata
    const presets = types.pearson_types.map(type => {
        const meta = metadata.types.find(m => m.type === type.type) || {};
        return { ...type, ...meta };
    });
    
    return presets;
}

// Build preset UI
const presets = await loadPearsonPresets();
presets.forEach(preset => {
    if (preset.visual_complexity > 0) {  // Skip trivial R and B
        createPresetCard(preset);
    }
});

function createPresetCard(preset) {
    const card = document.createElement('div');
    card.className = 'preset-card';
    card.innerHTML = `
        <strong>${preset.type}: ${preset.name}</strong>
        <small>F=${preset.F}, k=${preset.k}</small>
        <small>Complexity: ${(preset.visual_complexity * 100).toFixed(0)}%</small>
        <small>${preset.is_static ? 'Static' : 'Animated'}</small>
    `;
    card.addEventListener('click', () => {
        simMaterial.uniforms.uFeedRate.value = preset.F;
        simMaterial.uniforms.uKillRate.value = preset.k;
    });
    presetGrid.appendChild(card);
}
```

---

## 10. Common Pitfalls and Fixes

### ❌ Patterns Look Like Noise / NaN Artifacts

**Symptom**: Bright random pixels, checkerboard, or pure white/black after a few steps.  
**Cause**: Numerical instability from too-large `dt` or extreme F/k values.  
**Fix**: Reduce `dt` (try 0.5, then 0.25). Ensure F and k are in the valid range: F ∈ [0.01, 0.10], k ∈ [0.035, 0.070].

### ❌ Patterns Are Directionally Biased (Rectangular Artifacts)

**Symptom**: Spots or stripes strongly prefer horizontal/vertical alignment.  
**Cause**: Using the 5-point Laplacian (cardinal-only) instead of the 9-point.  
**Fix**: Ensure diagonal neighbors are included with weight 0.05 in the Laplacian.

### ❌ Same Parameters, Different Patterns Each Run

**Behavior**: This is *expected* — the random seed determines which specific spatial configuration emerges, not the Pearson type. The same F/k with a different seed will give the same *type* of pattern but different specific arrangement.  
**For reproducible results**: Use `Math.seedrandom()` or a fixed seed value for the noise generation.

### ❌ Boundary Edge Lines / Artificial Stripes at Edges

**Symptom**: Strong stripe or ring at canvas edges, pattern looks different near edges.  
**Cause**: Texture wrapping is `ClampToEdgeWrapping` instead of `RepeatWrapping`.  
**Fix**: Set both wrapS and wrapT to `THREE.RepeatWrapping` on the render target texture.

### ❌ Performance Drops After Changing Resolution

**Symptom**: Frame rate drops dramatically after calling resize.  
**Cause**: Old render targets not disposed — GPU memory leak.  
**Fix**: Always call `.dispose()` on old targets before creating new ones:
```javascript
function resizeSimulation(newSize) {
    targets.forEach(t => t.dispose());  // Free GPU memory
    targets = [createRenderTarget(newSize), createRenderTarget(newSize)];
    uploadSeed(renderer, scene, camera, targets, seedData, newSize);
}
```

### ❌ Float Textures Not Supported (Mobile)

**Symptom**: `OES_texture_float` extension not available; console error.  
**Fix**: Fall back to 8-bit textures with normalized values and a manual decode step in the shader. Performance will be slightly worse but it will work on all devices.
```javascript
// Detect support
const supportsFloat = renderer.extensions.get('OES_texture_float') !== null;
const textureType = supportsFloat ? THREE.FloatType : THREE.UnsignedByteType;
```

### ❌ Pattern Never Develops / Stays Uniform

**Symptom**: Field stays at U=1, V=0 forever.  
**Cause**: Seed was not properly uploaded, or both targets weren't initialized.  
**Fix**: Verify the seed upload blit renders into *both* targets (not just one). Check that `data[idx+1]` (V channel, green) has non-zero values at seed locations.

---

## 11. Minimal Standalone Example

A complete self-contained implementation (no build tools required) is in `examples/threejs-webgl/index.html`. To run it:

```bash
# Any static file server works — Python is simplest
python3 -m http.server 8000

# Then open:
# http://localhost:8000/examples/threejs-webgl/
```

The example demonstrates:
- Full ping-pong simulation loop
- Live F and k sliders
- Steps-per-frame control
- Reset and random seed buttons

---

## 12. Deployment Notes

### CORS and CDN Assets

The Three.js import map in the example uses `unpkg.com`. For production:
1. Download Three.js locally: `npm install three`
2. Bundle with Vite, Rollup, or webpack
3. Or use a pinned CDN version: `https://unpkg.com/three@0.160.0/build/three.module.js`

### HTTPS Requirement

WebGL float textures require a secure context on some browsers. Serve over HTTPS in production. For local development, `localhost` is always treated as secure.

### Mobile Considerations

- Reduce default resolution to 256² on mobile (detect via `navigator.maxTouchPoints > 0`)
- Prefer `mediump` precision in shaders
- Limit `stepsPerFrame` to 4–8 on mobile GPUs
- Test on Safari (iOS): WebGL 2 support varies by iOS version

### Embedding in iframes / React / Vue

The simulation is fully self-contained in a canvas element and can be wrapped in any component framework. For React:
```jsx
const SimCanvas = () => {
    const canvasRef = useRef(null);
    useEffect(() => {
        const sim = new GrayScottWebGL(canvasRef.current);
        return () => sim.dispose();  // Cleanup on unmount
    }, []);
    return <canvas ref={canvasRef} />;
};
```
