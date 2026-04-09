# Coloring Strategies

## Munafo's Approach

Encode both $u$ and $\partial u/\partial t$ in single color:
- **Low u** → Blue (matches bromothymol blue pH indicator)
- **High u** → Red
- **Rate of change** → Brightness/saturation modulation

## Simple Mappings

### Grayscale on v
```glsl
float c = 1.0 - v;
gl_FragColor = vec4(c, c, c, 1.0);
```

### Two-Tone Chemical
```glsl
vec3 colorU = vec3(1.0); // White = pure U
vec3 colorV = vec3(0.0); // Black = pure V
vec3 color = mix(colorU, colorV, v);
```

### Psychedelic Ramp
```glsl
vec3 col;
col.r = sin(v * 6.28 * 2.0 + 0.0) * 0.5 + 0.5;
col.g = sin(v * 6.28 * 2.0 + 2.09) * 0.5 + 0.5;
col.b = sin(v * 6.28 * 2.0 + 4.18) * 0.5 + 0.5;
```

### Embossed 3D (Karl Sims)
Use gradient of v as surface normal for fake lighting.

## Multi-Channel Encoding

Store simulation state in RGBA:
- R: u concentration
- G: v concentration
- B: du/dt (for Munafo coloring)
- A: dv/dt or iteration count
