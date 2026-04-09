# Pearson Classification — All 17 Types

Extended classification from Pearson (1993) 14 types + Munafo (2009+) additions.

## Wolfram Complexity Classes

| Class | Behavior | Gray-Scott Types |
|-------|----------|------------------|
| 1 | Uniform steady state | R, B |
| 2 | Periodic/structured | ι, ν |
| 2-a | Structured with spatial complexity | δ, θ, κ, λ, μ, ρ, σ |
| 3 | Chaotic/aperiodic | α, β, γ, ε, ζ, η, ξ |
| 4 | Complex localized structures | **π** |

## The Complete Taxonomy

### Class 1: Trivial States

**R (Uniform Red)**
- F=0.014, k=0.057
- All U consumed, V dominates
- No pattern formation

**B (Uniform Blue)**
- F=0.050, k=0.059
- U dominates, V eliminated
- No pattern formation

### Class 3: Chaotic Dynamics

**α — Wavelet Chaos**
- F=0.010, k=0.047
- Fledgling spirals, wavelets grow and annihilate
- Continuous spatiotemporal chaos

**β — Ocean Voids**
- F=0.014, k=0.039
- Waves on blue background, red voids open/fill periodically

**γ — Unstable Stripes**
- F=0.022, k=0.051
- Wormlike stripes, endless grain boundary events
- Never reaches steady state

**ε — Chaotic Mitosis**
- F=0.018, k=0.055
- Spots split via mitosis, rings grow until contact
- Overcrowding causes die-outs

**ζ — Stable Chaotic Spots**
- F=0.022, k=0.061
- Like ε but more symmetrical, less volatile

**η — Spots and Worms**
- F=0.034, k=0.063
- Mixed morphology, eventually reaches steady state

**ξ — Spirals**
- F=0.010, k=0.041
- Large sustained spirals (BZ-like)
- Requires large domain or spirals die out

### Class 2-a: Structured Complexity

**δ — Turing Spots (Classic)**
- F=0.030, k=0.055
- True Turing patterns: hexagonal negative spots
- Stable grain boundaries

**θ — Ring Growth Stripes**
- F=0.030, k=0.057
- Blue spots → concentric rings → stripes
- Final connected network

**κ — Hedgerow Mazes**
- F=0.050, k=0.063
- Stripes meander, form disconnected mazes

**λ — Mitotic Hexagons**
- F=0.026, k=0.061
- Solitons divide, arrange into hexagonal grid
- Then stops (steady state)

**μ — Growing Worms**
- F=0.046, k=0.065
- Stripes grow from ends, reorganize to parallel

**ρ — Red Soap Bubbles**
- F=0.090, k=0.059
- Closed red regions bordered by stripes
- Surface tension dynamics (smaller shrink, larger grow)

**σ — Blue Soap Bubbles**
- F=0.090, k=0.057
- Like ρ with colors reversed

### Class 2: Molecular

**ι — Molecular Negatons**
- F=0.046, k=0.0594
- Negative spots with molecule-like binding
- Solitary negatons not viable

**ν — Inert Solitons**
- F=0.054, k=0.067
- Non-mitotic, drift apart exponentially slowly
- Steady state requires astronomical time

### Class 4: The Holy Grail

**π — U-Skate World**
- F=0.062, k=0.061 (or 0.0609 for precise U-skate)
- **Only Gray-Scott type reaching Wolfram Class 4**
- Stable moving localized patterns
- Negative stripes, loops, spots with oscillating interactions
- Computational complexity rivaling Rule 110

## Parameter Map Visualization

```
F ↑
0.10│ R (trivial red)                 │
0.08│                                 │
    │     ╔═══╗ ← Saddle-node boundary│
0.06│   ╔╝ π ╚╗ U-Skate World (Class 4)│
    │ ╔╝CHAOS ╚╗                      │
0.04│╔╝ α β ╚╗                        │
    │╔╝ γ ε ζ ╚╗                      │
0.02│╚╗ δ θ κ ╔╝                      │
    │ ║ λ μ ρ σ ║                      │
0.01│ ║ ξ (spirals) ║                  │
    └┴────────────────┴──→ k
      0.03    0.05    0.07
```

## Alternate Presets

Many types have multiple valid (F,k) pairs producing similar behavior. See `presets/pearson-types.json` for complete list.
