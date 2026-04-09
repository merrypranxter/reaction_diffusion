# Implementation Patterns

## CPU Implementations

### NumPy Vectorized (Baseline)
- 5-point unweighted Laplacian
- 1.27 ms/step at 300×300
- Best for: Prototyping, parameter exploration

### Cython (Typed Loops)
- Memoryviews, explicit indexing
- 780 μs/step at 300×300 (1.6× speedup)
- Best for: Production CPU code

### Fortran f2py
- Explicit loops, optimized compilation
- 214 μs/step at 300×300 (5.9× speedup)
- Best for: Maximum CPU performance

## GPU Implementations

### PyTorch (Recommended)
- Laplacian = conv2d with 3×3 kernel
- 40× speedup at 2000×2000 (RTX 2070)
- F and k as tensors for spatial variation
- Best for: Research, batch processing, Pearson plots

### WebGL (Browser)
- Ping-pong FBO architecture
- 16-60 FPS at 512×512 depending on steps/frame
- Best for: Interactive demos, deployment

### WebGPU (Future)
- Compute shaders, better performance than WebGL
- Best for: Next-gen browser applications

## Laplacian Kernel Variants

| Variant | Kernel | Use Case |
|---------|--------|----------|
| 5-point | `[[0,1,0],[1,-4,1],[0,1,0]]` | Fast, compatible |
| 9-point weighted | `[[0.05,0.2,0.05],[0.2,-1,0.2],[0.05,0.2,0.05]]` | Default, isotropic |
| 9-point unweighted | `[[1,1,1],[1,-8,1],[1,1,1]]/8` | Alternative isotropic |

## Stability Considerations

Explicit Euler requires:
$$\Delta t \leq \frac{(\Delta x)^2}{4D_{max}}$$

For Du=1.0, Dv=0.5, dx=1.0: dt ≤ 0.25 (but 1.0 often stable with weighted kernel due to implicit smoothing).

## Multi-Step Rendering

Run 10-20 simulation steps per frame for visible evolution:
```javascript
function render() {
    for (let i = 0; i < 20; i++) {
        // Bind FBO, run simulation shader
        simulate();
    }
    // Display result
    draw();
    requestAnimationFrame(render);
}
```
