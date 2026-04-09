# Blur-Sharpen Equivalence (Werth 2015)

## The Discovery

Repeated Gaussian Blur + Unsharp Mask = Turing patterns

This is mathematically equivalent to reaction-diffusion.

## The Technique

1. Start with grayscale image (noise works)
2. Gaussian Blur (σ_blur ≈ 5px)
3. Unsharp Mask (amount=100%, σ_sharpen ≈ 10px)
4. Repeat 150× iterations

## The Math

**Blur**: Convolution with Gaussian = diffusion
$$I_{blur} = G_{\sigma_{blur}} \star I_0$$

**Unsharp Mask**:
$$mask = I_{blur} - G_{\sigma_{usm}} \star I_{blur}$$
$$I_1 = I_{blur} + mask = 2G_{\sigma_{blur}} \star I_0 - G_{\sigma_{ub}} \star I_0$$

Where $\sigma_{ub} = \sqrt{\sigma_{usm}^2 + \sigma_{blur}^2}$

**Result**: Difference of Gaussians (DoG) convolution
$$I_1 = (2G_{\sigma_{blur}} - G_{\sigma_{ub}}) \star I_0$$

## Mexican Hat Kernel

DoG has characteristic shape:
- **Positive center** (short-range activation)
- **Negative surround** (long-range inhibition)

Exactly the Turing requirement.

## Parameters

| Parameter | Effect |
|-----------|--------|
| σ_blur | Activation range |
| σ_sharpen | Inhibition range (must be > σ_blur) |
| Sharpen amount | Reaction strength |

## Multi-Scale Patterns

Jonathan McCabe (Bridges 2010): Multiple DoG scales simultaneously for richer patterns.

## GLSL Implementation

See `shaders/glsl/experimental/multi-scale.frag`
