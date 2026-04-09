# Repository Structure for GitHub Copilot

This document describes the intended repository structure for the Chemical Diffusion Reactions project. Use this as a guide when organizing files.

## Directory Structure

```
chemical-diffusion-reactions/
│
├── README.md                          # Project overview and quick start
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # Contribution guidelines
├── .gitignore                         # Git ignore patterns
├── pyproject.toml                     # Python package configuration
├── setup.py                           # Setup script with Cython extensions
├── Dockerfile                         # Docker build configuration
├── docker-compose.yml                 # Docker Compose services
├── Makefile                           # Build automation
│
├── .github/
│   └── workflows/
│       └── ci.yml                     # GitHub Actions CI/CD
│
├── docs/                              # Documentation (MkDocs)
│   ├── index.md
│   ├── 01-mathematical-foundations.md
│   ├── 02-gray-scott-deep-dive.md
│   ├── 03-pearson-classification.md
│   ├── 04-bifurcation-theory.md
│   ├── 05-topological-defects.md
│   ├── 06-implementation-patterns.md
│   ├── 07-coloring-strategies.md
│   ├── 08-spatial-parameter-sweeps.md
│   ├── 09-alternative-models.md
│   └── 10-blur-sharpen-equivalence.md
│
├── core/                              # Core Python module
│   ├── __init__.py
│   ├── gray_scott.py                  # Main Gray-Scott implementation
│   ├── parameters.py                  # Parameter definitions (Pearson types)
│   ├── laplacian.py                   # Laplacian operators
│   └── seeding.py                     # Initial condition generators
│
├── cpu/                               # CPU implementations
│   ├── __init__.py
│   ├── numpy_vectorized.py            # NumPy baseline
│   ├── cython_accelerated.pyx         # Cython extension
│   ├── fortran_backend.f90            # Fortran backend
│   └── benchmarks/
│       └── benchmark_results.md
│
├── gpu/                               # GPU implementations
│   ├── pytorch/
│   │   ├── gray_scott_torch.py        # PyTorch CUDA implementation
│   │   └── pearson_plot_gpu.py        # Spatial parameter sweeps
│   ├── webgpu/
│   │   ├── compute.wgsl               # WebGPU compute shader
│   │   └── pipeline.js                # WebGPU pipeline
│   └── benchmarks/
│       └── gpu_speedups.md
│
├── models/                            # Alternative reaction-diffusion models
│   ├── belousov_zhabotinsky.py        # BZ reaction (Oregonator)
│   ├── fitzHugh_nagumo.py             # FHN neural model
│   ├── cahn_hilliard.py               # Phase separation
│   └── schnakenberg.py                # Cross-diffusion model
│
├── shaders/                           # GLSL/WGSL shaders
│   ├── gray-scott-sim.frag            # Main simulation shader
│   ├── display-munafo.frag            # Munafo coloring shader
│   └── color-ramps.glsl               # Color mapping utilities
│
├── presets/                           # Parameter presets
│   ├── pearson-types.json             # All 17 Pearson types
│   └── named-behaviors.json           # Named presets (Mitosis, etc.)
│
├── tests/                             # Unit tests
│   ├── test_laplacian.py              # Laplacian operator tests
│   ├── test_convergence.py            # Stability tests
│   └── test_presets.py                # Preset validation
│
├── tools/                             # CLI utilities
│   ├── parameter_scanner.py           # Batch parameter rendering
│   ├── video_generator.py             # MP4/GIF generation
│   └── profiler.py                    # Performance profiling
│
└── examples/                          # Standalone examples
    └── threejs-webgl/
        └── index.html                 # Interactive WebGL demo
```

## File Naming Conventions

| Element | Pattern | Example |
|---------|---------|---------|
| Files | kebab-case | `gray-scott-sim.frag` |
| Classes | PascalCase | `GrayScottTorch` |
| Functions | snake_case | `compute_laplacian()` |
| Constants | UPPER_SNAKE | `KERNEL_9POINT` |
| Preset keys | lowercase | `"mitosis"`, `"u-skate-world"` |

## Key Dependencies

- **NumPy**: Core array operations
- **SciPy**: Convolution, FFT
- **PyTorch**: GPU acceleration
- **Cython**: CPU optimization
- **Pillow**: Image I/O
- **OpenCV**: Video generation
- **pytest**: Testing framework

## Build Commands

```bash
# Install with all dependencies
pip install -e ".[all]"

# Run tests
pytest tests/ -v --cov=core --cov=models

# Build Cython extensions
python setup.py build_ext --inplace

# Build Docker image
docker build -t cdr:latest .

# Run benchmarks
python -m tools.profiler --sizes 128 256 512 1024
```

## Notes for AI Assistants

1. **Laplacian kernels**: 9-point weighted (Karl Sims) is default
2. **Boundary conditions**: Periodic (toroidal) everywhere
3. **Color mapping**: Munafo's u/∂u approach preferred
4. **Seeding**: Use u≈0.5, v≈0.25 for center seed (not tiny noise)
5. **Stability**: dt ≤ 0.25 for explicit Euler with Du=1, Dv=0.5
