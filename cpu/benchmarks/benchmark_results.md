# CPU Benchmark Results

Hardware: Intel Core i7-9700K @ 3.6GHz, 32GB RAM
Grid: 300 × 300
Parameters: Du=0.1, Dv=0.05, F=0.0545, k=0.062

## Results

| Implementation | Time per Step | Relative Speed |
|----------------|---------------|----------------|
| NumPy Vectorized | 1.27 ms | 1.0× (baseline) |
| Cython (typed loops) | 780 μs | 1.6× |
| Fortran f2py | 214 μs | **5.9×** |

## Key Insights

1. **NumPy overhead**: Vectorized operations have significant temporary array creation overhead
2. **Cython improvement**: Typed memoryviews eliminate Python overhead in inner loops
3. **Fortran dominance**: Native compilation with explicit loops maximizes cache efficiency

## Scaling Behavior

All implementations scale as O(n²) with grid size, but constant factors differ significantly.
For production CPU work, Fortran via f2py is recommended. For prototyping, NumPy is sufficient.
