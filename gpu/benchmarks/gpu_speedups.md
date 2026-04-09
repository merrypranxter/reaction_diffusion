# GPU Benchmark Results

Source: Nils Olovsson (2023)
Hardware: NVIDIA RTX 2070 vs 6-core Intel CPU
Method: PyTorch conv2d for Laplacian

## Speedup Factors

| Grid Size | Speedup |
|-----------|---------|
| 500 × 500 | 2× |
| 1000 × 1000 | 25× |
| 2000 × 2000 | **40×** |

## Key Implementation Details

- **Laplacian**: `torch.nn.functional.conv2d` with 3×3 kernel
- **dt**: 0.125 (smaller than CPU implementations for stability)
- **Kernel**: Karl Sims weighted 9-point
- **Padding**: `'same'` handles boundaries automatically

## Memory Usage

Approximate VRAM requirements:
- 512×512: ~50 MB
- 1024×1024: ~200 MB
- 2048×2048: ~800 MB

## Spatial Parameter Variation

F and k can be 2D tensors (textures) for Pearson plots:
```python
F_map = torch.linspace(0.0, 0.08, height).view(-1, 1).expand(height, width)
k_map = torch.linspace(0.03, 0.07, width).view(1, -1).expand(height, width)
```

This allows full parameter space exploration in single simulation.
