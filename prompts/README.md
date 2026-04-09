# Reaction-Diffusion Pattern Prompting Guide

> **Purpose**: Use these templates to describe Gray-Scott / Pearson reaction-diffusion patterns accurately when prompting Midjourney, DALL-E, Gemini, Stable Diffusion, Flux, or any text-to-image system.
>
> **Machine-readable data**: See `pearson-type-prompts.json` for structured prompts and tags for all 19 pattern types.

---

## Table of Contents

1. [Why Standard Prompts Fall Short](#1-why-standard-prompts-fall-short)
2. [Core Vocabulary](#2-core-vocabulary)
3. [Master Prompt Templates](#3-master-prompt-templates)
4. [Per-Type Quick Reference](#4-per-type-quick-reference)
5. [Hybrid Pattern Descriptions](#5-hybrid-pattern-descriptions)
6. [Color and Material Control](#6-color-and-material-control)
7. [Midjourney-Specific Tips](#7-midjourney-specific-tips)
8. [DALL-E / GPT-Image Tips](#8-dall-e--gpt-image-tips)
9. [Stable Diffusion / Flux Tips](#9-stable-diffusion--flux-tips)
10. [Gemini Tips](#10-gemini-tips)
11. [Prompts That Don't Work (and Why)](#11-prompts-that-dont-work-and-why)
12. [Verification Checklist](#12-verification-checklist)

---

## 1. Why Standard Prompts Fall Short

Most AI image generators don't have deep knowledge of specific reaction-diffusion pattern types. A prompt like *"reaction diffusion pattern"* will produce something vaguely organic but almost never match a specific Pearson type.

**The problem**: AI models encode "reaction diffusion" as a visual category associated with vague organic textures — they don't reason about the parameter space.

**The solution**: Describe the *visual output* in physical and material terms the model understands, not the mathematical mechanism. Instead of "type δ Turing pattern", say "hexagonal array of dark spots on cream background, uniform spacing, cheetah-like, natural organic geometry."

---

## 2. Core Vocabulary

Use these validated terms when building prompts:

### Spatial Structure Terms
| Term | Use for |
|------|---------|
| `hexagonal spot array` | δ (Turing Spots), λ (Mitotic Hexagons) |
| `parallel worm-like stripes` | μ (Growing Worms), γ (Unstable Stripes) |
| `labyrinthine branching channels` | κ (Hedgerow Mazes) |
| `concentric ring pattern` | θ (Ring Growth Stripes) |
| `closed-cell foam topology` | ρ (Red Soap Bubbles), σ (Blue Soap Bubbles) |
| `rotating spiral waves` | ξ (Spirals) |
| `scattered isolated spots` | ν (Inert Solitons), ι (Molecular Negatons) |
| `chaotic waveforms` | α (Wavelet Chaos), β (Ocean Voids) |
| `mixed spot and stripe morphology` | η (Spots and Worms) |

### Material Associations (most effective in AI models)
| Material | Maps to |
|----------|---------|
| `cheetah fur pattern` | δ (Turing Spots) |
| `leopard skin` | δ, ζ |
| `giraffe flank` | η (Spots and Worms) |
| `zebra stripe` | μ (Growing Worms) |
| `fingerprint ridges` | γ (Unstable Stripes) |
| `soap bubble foam` | ρ, σ |
| `agate stone cross-section` | θ (Ring Growth) |
| `Belousov-Zhabotinsky reaction` | ξ (Spirals) |
| `brain coral surface` | κ (Mazes) |
| `honeycomb lattice` | λ (Mitotic Hexagons) |

### Process/Character Descriptors
| Descriptor | Meaning |
|-----------|---------|
| `emergent from uniform noise` | Turing instability origin |
| `self-organizing` | pattern arises without external structure |
| `biological patterning mechanism` | Turing/reaction-diffusion context |
| `frozen in time` | static pattern, not animated |
| `sustained oscillation` | dynamic, never-static |
| `autocatalytic` | the chemical creates more of itself |

---

## 3. Master Prompt Templates

### Template A: Static Pattern (for image generation)

```
[SPATIAL STRUCTURE], [SCALE DESCRIPTOR], [MATERIAL ASSOCIATION],
[COLOR PALETTE], [TEXTURE QUALITY], [CONTEXT/AESTHETIC]
```

**Example for δ (Turing Spots)**:
```
hexagonal array of dark spots on cream background, uniform spacing similar 
to cheetah fur patterning, natural biological organization, warm earth tones 
with high contrast spots, macro photography texture quality, 
organic Turing pattern aesthetic
```

### Template B: Dynamic/Animated Description

```
[MOTION DESCRIPTION], [SPATIAL ORGANIZATION], [MATERIAL FEEL],
[COLOR PALETTE], [ENERGY LEVEL], [ANIMATION LOOP CHARACTER]
```

**Example for ξ (Spirals)**:
```
rotating chemical spiral waves, large-scale Belousov-Zhabotinsky reaction pattern,
mesmerizing galaxy-like rotation, electric blue and deep violet color cycling,
continuously animated, hypnotic loop, scientific elegance
```

### Template C: Texture for 3D/Shader Use

```
seamless tiling texture, [PATTERN TYPE], [SCALE], 
[TECHNICAL QUALITY TERMS], [COLOR RANGE], suitable for PBR workflow,
albedo map, physically-based material
```

**Example for μ (Growing Worms)**:
```
seamless tiling texture, parallel organic stripe pattern similar to zebra stripes,
medium scale, high detail, grayscale, suitable for PBR displacement or normal map,
regular worm-like organic stripes, 4K texture quality
```

---

## 4. Per-Type Quick Reference

| Type | Name | Best Prompt Phrase | Notes |
|------|------|-------------------|-------|
| R | Uniform Red | `monochromatic flat red field, zero texture` | Not visually interesting — use for background |
| B | Uniform Blue | `flat deep blue field, uniform calm surface` | Same as R — use as void/background |
| α | Wavelet Chaos | `turbulent chemical wave interference, chaotic overlapping wavelets` | Always describe as dynamic/moving |
| β | Ocean Voids | `bioluminescent ocean with dark drifting voids, wave patterns` | Emphasize oceanic + void character |
| γ | Unstable Stripes | `fingerprint-like organic stripes constantly rearranging` | Emphasize *unstable*, not clean stripes |
| δ | Turing Spots | `hexagonal cheetah spot array, negative spots on light field, Turing pattern` | Most recognizable type |
| ε | Chaotic Mitosis | `dividing cells chaos, blobs splitting like amoeba` | Emphasize *splitting* and *chaos* |
| ζ | Stable Spots | `ordered cell colony, pulsing dot array, frog skin texture` | More regular than ε |
| η | Spots and Worms | `giraffe flank texture, mixed spots and worm-like stripes` | Two morphologies in one image |
| θ | Ring Growth | `concentric ring growth pattern, tree ring cross-section, agate stone` | Concentric is key |
| ι | Molecular Negatons | `dark spots sparse on bright field, molecular gas top-view` | Inverse polarity — dark on light |
| κ | Hedgerow Mazes | `branching dendritic maze channels, river delta aerial view` | Labyrinthine topology |
| λ | Mitotic Hexagons | `hexagonal honeycomb-organized spots, crystalline dot lattice` | Most ordered spot type |
| μ | Growing Worms | `parallel worm stripes, corduroy-like biological texture` | Parallel + long stripes |
| ν | Inert Solitons | `isolated glowing spots, sparse particle field on black background` | Sparse + starfield aesthetic |
| ξ | Spirals | `rotating BZ chemical spiral waves, galaxy-like spiral arms` | Always describe rotation |
| π | U-Skate World | `self-propelled localized chemical structures, autonomous moving patterns` | Moving + autonomous |
| ρ | Red Soap Bubbles | `red soap bubble cell foam, closed-cell organic structure` | Closed topology |
| σ | Blue Soap Bubbles | `blue cellular foam pattern, stained glass cell network` | Cool color + cellular |

---

## 5. Hybrid Pattern Descriptions

Real reaction-diffusion parameter space has smooth transitions between types. Here's how to describe blends:

### δ → λ (Spots becoming more hexagonal)
```
semi-ordered spot array, approximately hexagonal arrangement but with 
natural variance, biological dot patterning between random and crystalline,
like a leopard skin with unusually regular spot spacing
```

### γ → μ (Chaotic stripes becoming parallel)
```
organic stripe pattern transitioning from disordered fingerprint whorls 
to parallel aligned channels, biological fiber texture with partial 
directional organization, some grain boundaries remaining
```

### η blend (spots AND stripes in same image)
```
natural animal skin patterning where spots and stripes coexist in different 
regions, giraffe-like patchwork of circular spots merging into elongated 
worm-like stripes at transitions, rich mixed morphology texture
```

### α + ξ (chaos with spiral tendency)
```
turbulent chemical oscillation with nascent spiral structure trying to organize,
chaotic wavelet field with rotating tendencies, dynamic abstract texture 
between randomness and order
```

---

## 6. Color and Material Control

### Scientific Color Mappings

These prompts produce the "classic" reaction-diffusion color schemes:

```
# Grayscale (simplest)
"high-contrast black and white texture, pattern only, no color"

# Classic blue-red (Munafo scheme)
"deep navy to crimson gradient mapped to chemical concentration, 
blue regions high substrate, red regions high product"

# Inferno heatmap
"dark purple to orange to yellow inferno colormap, 
scientific heatmap visualization of chemical field"

# Turbo rainbow
"full-spectrum rainbow colormap mapped to concentration gradient,
scientific visualization, turbo colormap"
```

### Biological / Natural Palette Prompts

```
# Cheetah (δ type)
"warm cream and tan background with dark chocolate-brown spots, 
natural cheetah fur coloration"

# Ocean (β type)  
"deep ocean navy and electric teal blues, dark voids on bioluminescent field"

# Forest floor (κ maze type)
"dark forest green labyrinthine channels on warm tan sandy background,
moss and earth tones"

# Coral reef (η mixed type)
"warm ochre and terracotta with dark brown accents, 
tropical coral surface texture palette"
```

### Luminous / Glowing Aesthetic

For neon or dark-background renders:
```
"glowing neon [color] on pure black background, 
luminous chemical emission lines, dark field microscopy aesthetic,
bioluminescence"
```

---

## 7. Midjourney-Specific Tips

**Aspect ratio**: Use `--ar 1:1` for standard textures, `--ar 16:9` for background scenes.

**Style modifiers that work well**:
```
--style raw         # Less AI interpretation, closer to described pattern
--chaos 15-25       # Adds natural variation to spot/stripe placement
--stylize 50-150    # Controls artistic interpretation
```

**Effective suffix for static patterns**:
```
..., macro photograph, scientific photography, neutral background, 
perfectly tiled, --style raw --ar 1:1
```

**Effective suffix for dynamic/animated feel**:
```
..., digital art, flowing energy, abstract visualization, 
vibrant colors, --ar 16:9 --stylize 200
```

**What works best in Midjourney**: Material analogies. "Cheetah spots" produces better δ-type results than "hexagonal negative spot array on uniform field". Always anchor to a known material first, then modify.

---

## 8. DALL-E / GPT-Image Tips

DALL-E responds well to:
- **Role framing**: "A scientific visualization of..." or "A close-up photograph of..."
- **Physical anchors**: "The surface texture resembles..." 
- **Negation**: "no text, no labels, seamless, no grid lines"

**Example for θ (Ring Growth)**:
```
A close-up cross-section of an agate stone showing concentric mineral rings 
in warm amber and brown tones. The rings are slightly irregular, organic, 
formed by chemical diffusion. Scientific geology photography. No labels. 
Macro lens, neutral background.
```

---

## 9. Stable Diffusion / Flux Tips

**Useful LoRA/embedding search terms**:
- `reaction diffusion`, `Turing pattern`, `morphogenesis`, `cellular automaton`
- Model recommendations: Any model with strong texture capabilities (RealVisXL, SDXL-Turbo)

**Negative prompts** (add to all):
```
blurry, low quality, cartoon, anime, text, watermark, oversaturated, 
3D render, photorealistic human, border, frame
```

**CFG scale recommendations**:
- Static geometric patterns (δ, λ, μ): CFG 7–10
- Chaotic/organic patterns (α, ε, ξ): CFG 5–7 (allow more freedom)

---

## 10. Gemini Tips

Gemini (image generation via Imagen) responds best to:
- **Descriptive physical metaphors** over mathematical descriptions
- **Layered specificity**: Start general, add modifiers ("organic texture, specifically the hexagonal spot array found in cheetah fur, viewed as a macro photograph")
- **Context anchoring**: "In the style of scientific nature photography" or "as seen in a biology textbook illustration"

---

## 11. Prompts That Don't Work (and Why)

| Prompt | Problem | Better Alternative |
|--------|---------|-------------------|
| `"Gray-Scott type delta"` | Model has no learned encoding for this classification | `"hexagonal array of dark spots on light field, Turing pattern"` |
| `"reaction diffusion with F=0.030 k=0.055"` | Model doesn't understand parameter space | Describe the visual output instead |
| `"Turing instability pattern"` | Too technical, under-represented in training data | `"biological spot patterning, cheetah-like hexagonal dots"` |
| `"spatiotemporal chaos"` | Abstract mathematical term | `"turbulent chemical waves, constantly shifting, never settling"` |
| `"class 4 Wolfram complexity"` | Highly specific technical term | `"self-propelled autonomous particles, moving chemical structures"` |

---

## 12. Verification Checklist

When evaluating AI-generated results against a target Pearson type, check:

- [ ] **δ (Turing Spots)**: Are spots arranged in roughly hexagonal lattice? Are they *negative* (dark on light)? Regular spacing?
- [ ] **μ (Worms)**: Are stripes long and approximately parallel? No closed loops?
- [ ] **κ (Mazes)**: Are channels branching (dendritic), not closed loops? No isolated spots?
- [ ] **ρ/σ (Bubbles)**: Are regions fully enclosed (foam topology)? Is there a border network?
- [ ] **ξ (Spirals)**: Are spirals continuous arms, not concentric circles? Multiple rotating centers?
- [ ] **λ (Hexagons)**: Are spots in perfect hexagonal arrangement? Uniform size?

If the image doesn't pass the checklist, add more specific descriptors from the Core Vocabulary section and regenerate.
