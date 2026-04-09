#version 300 es
precision highp float;

// Munafo coloring: encodes u and du/dt
uniform sampler2D uState;
uniform sampler2D uPreviousState;  // For computing du/dt
uniform vec2 uResolution;
uniform float uDeltaT;

in vec2 vUv;
out vec4 fragColor;

vec3 hsl2rgb(float h, float s, float l) {
    vec3 rgb = clamp(abs(mod(h * 6.0 + vec3(0.0, 4.0, 2.0), 6.0) - 3.0) - 1.0, 0.0, 1.0);
    return l + s * (rgb - 0.5) * (1.0 - abs(2.0 * l - 1.0));
}

void main() {
    vec2 state = texture(uState, vUv).rg;
    vec2 prevState = texture(uPreviousState, vUv).rg;
    
    float u = state.r;
    float v = state.g;
    float du = (u - prevState.r) / uDeltaT;
    
    // Base color from u: blue (low) to red (high)
    vec3 color;
    color.r = u;
    color.b = 1.0 - u;
    color.g = 0.0;
    
    // Modulate brightness by rate of change
    float activity = abs(du) * 10.0;  // Scale factor
    color *= (0.5 + activity);
    
    // Or use du to shift hue
    // color = hsl2rgb(u * 0.7 + du * 0.1, 0.8, 0.5);
    
    fragColor = vec4(clamp(color, 0.0, 1.0), 1.0);
}
