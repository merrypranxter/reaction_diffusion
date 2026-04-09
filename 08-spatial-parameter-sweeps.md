# Spatial Parameter Sweeps (Pearson Plots)

## The Technique

Map F and k to spatial axes within single simulation:

$$k(x) = k_{min} + \frac{x}{width}(k_{max} - k_{min})$$
$$F(y) = F_{min} + \frac{y}{height}(F_{max} - F_{min})$$

## Standard Ranges

- k: 0.03 → 0.07 (X-axis)
- F: 0.00 → 0.08 (Y-axis)

## Rescaled Plot (VisualPDE)

Nonlinear rescaling to focus on crescent:
```glsl
float kNorm = uv.x * uv.x; // Quadratic: more resolution at low k
float FNorm = uv.y;        // Linear F
float F = mix(0.0, 0.08, FNorm);
float k = mix(0.03, 0.07, kNorm);
```

## Seeding Strategy

Scatter 50+ small seeds across domain — different regions need different seeding to trigger patterns.

## GPU Implementation

F and k as 2D tensors (texture lookups):
```python
# PyTorch: spatially varying parameters
F_map = torch.linspace(0.0, 0.08, height).view(-1, 1).expand(height, width)
k_map = torch.linspace(0.03, 0.07, width).view(1, -1).expand(height, width)
```

## Output

Single image showing all 17 pattern types simultaneously — invaluable for navigation and education.
