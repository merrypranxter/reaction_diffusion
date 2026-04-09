# CHEMICAL DIFFUSION REACTIONS
> Reaction-diffusion pattern generation for biological morphogenesis, generative art, and computational design.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![WebGL 2.0](https://img.shields.io/badge/WebGL-2.0-red.svg)](https://get.webgl.org/webgl2/)

## What This Is
A comprehensive toolkit for simulating reaction-diffusion systems, with particular depth on the **Gray-Scott model**. Includes CPU (NumPy/Cython/Fortran) and GPU (PyTorch/WebGL/WebGPU) implementations, 17 classified pattern types, bifurcation analysis, and topological defect modeling.

**Key Features:**
- **17 Pearson Pattern Types** — from uniform states (R, B) to computational complexity (π/U-Skate World)
- **Bifurcation Theory** — saddle-node and Hopf boundary analysis
- **GPU Acceleration** — 40× speedup at 2K² resolution via PyTorch conv2d
- **WebGL Shaders** — production-ready GLSL for browser deployment
- **Blur-Sharpen Equivalence** — Werth's Difference-of-Gaussians method

## Quick Start
### Python (CPU)
```python
from core.gray_scott import GrayScottNumpy
from presets.pearson_types import DELTA

sim = GrayScottNumpy(size=256, **DELTA.to_dict())
for _ in range(1000):
    sim.step()
sim.save_image("turing_spots.png")
```

### Python (GPU)
```python
from gpu.pytorch.gray_scott_torch import GrayScottTorch

sim = GrayScottTorch(width=1024, height=1024, device='cuda')
for _ in range(1000):
    sim.step(F=0.0545, k=0.062)
```

### Browser (WebGL)
Open examples/threejs-webgl/index.html — interactive F/k sliders with live shader preview.

## Pattern Gallery
| Type | Name | F | k | Visual |
| --- | --- | --- | --- | --- |
| δ | Turing Spots | 0.030 | 0.055 | Hexagonal lattice |
| π | U-Skate World | 0.062 | 0.061 | Moving localized structures |
| ξ | Spirals | 0.010 | 0.041 | BZ-like rotating waves |
| ρ | Red Soap Bubbles | 0.090 | 0.059 | Surface tension networks |

## Repo Structure
```
core/      # Shared mathematics
cpu/       # NumPy, Cython, Fortran implementations
gpu/       # PyTorch, WebGL, WebGPU implementations
shaders/   # Raw GLSL/WGSL library
presets/   # Machine-readable parameter sets
docs/      # Comprehensive theory documentation
notebooks/ # Interactive Jupyter exploration
tools/     # CLI utilities for batch processing
```

## References
* Pearson (1993) — "Complex Patterns in a Simple System"
* Munafo (2009+) — Extended classification, U-Skate World discovery
* Karl Sims — [Reaction-Diffusion Tutorial](https://www.karlsims.com/rd.html)
* Werth (2015) — Blur-Sharpen Turing equivalence (Bridges)
* Olovsson (2023) — PyTorch GPU implementation

## License
MIT — See <LICENSE> for details.
