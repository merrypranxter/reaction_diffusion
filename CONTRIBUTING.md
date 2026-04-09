# Contributing

## Don't PR Garbage

This repo maintains strict quality standards. Before submitting:

1. **Test your parameters** — Run at least 10k steps to verify stability
2. **Benchmark if CPU-bound** — Include timing comparisons against NumPy baseline
3. **Shader validation** — Test on both NVIDIA and Intel GPUs
4. **Document the math** — Every equation needs a citation or derivation

## Code Style
- Python: Black formatter, 88 char line length
- GLSL: 4-space indents, explicit precision qualifiers
- Commit messages: Imperative mood, reference issue numbers

## What We Want
- New pattern type discoveries (rare but possible)
- Performance optimizations with measured speedups
- Additional model implementations (Schnakenberg, BZ Oregonator)
- Topological defect analysis tools
- WebGPU compute pipeline improvements

## What We Don't Want
- "Cleanups" that change formatting without functional improvement
- Untested shader "optimizations"
- Breaking changes to preset parameter values
- Dependencies without strong justification

## Architecture Decisions
- **Laplacian kernels**: 9-point weighted (Karl Sims) is default, 5-point available for compatibility
- **Boundary conditions**: Periodic (toroidal) everywhere — no plans for Dirichlet/Neumann
- **Color mapping**: Munafo's u/∂u approach preferred over simple grayscale

Questions? Open an issue with the `question` label.
