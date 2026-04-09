#version 300 es
precision highp float;

uniform sampler2D uState;
uniform vec2 uResolution;
uniform float uFeedRate;      // F
uniform float uKillRate;      // k
uniform float uDiffusionU;    // Du (typically 1.0)
uniform float uDiffusionV;    // Dv (typically 0.5)
uniform float uDeltaT;        // dt (typically 1.0)

in vec2 vUv;
out vec4 fragColor;

// Karl Sims weighted 9-point Laplacian
vec2 laplacian(sampler2D tex, vec2 uv, vec2 texel) {
    vec2 sum = vec2(0.0);
    
    // Cardinal neighbors (weight 0.2)
    sum += texture(tex, uv + vec2(-1.0, 0.0) * texel).rg * 0.2;
    sum += texture(tex, uv + vec2( 1.0, 0.0) * texel).rg * 0.2;
    sum += texture(tex, uv + vec2( 0.0, -1.0) * texel).rg * 0.2;
    sum += texture(tex, uv + vec2( 0.0,  1.0) * texel).rg * 0.2;
    
    // Diagonal neighbors (weight 0.05)
    sum += texture(tex, uv + vec2(-1.0, -1.0) * texel).rg * 0.05;
    sum += texture(tex, uv + vec2( 1.0, -1.0) * texel).rg * 0.05;
    sum += texture(tex, uv + vec2(-1.0,  1.0) * texel).rg * 0.05;
    sum += texture(tex, uv + vec2( 1.0,  1.0) * texel).rg * 0.05;
    
    // Center (weight -1.0)
    sum -= texture(tex, uv).rg;
    
    return sum;
}

void main() {
    vec2 texel = 1.0 / uResolution;
    vec2 state = texture(uState, vUv).rg;
    
    float u = state.r;
    float v = state.g;
    
    vec2 lap = laplacian(uState, vUv, texel);
    
    float reaction = u * v * v;
    
    float du = uDiffusionU * lap.r - reaction + uFeedRate * (1.0 - u);
    float dv = uDiffusionV * lap.g + reaction - (uFeedRate + uKillRate) * v;
    
    float newU = u + uDeltaT * du;
    float newV = v + uDeltaT * dv;
    
    // Clamp to valid range
    fragColor = vec4(
        clamp(newU, 0.0, 1.0),
        clamp(newV, 0.0, 1.0),
        0.0,
        1.0
    );
}
