#version 300 es
precision highp float;

// Reusable color mapping functions

// Turbo colormap (Google)
vec3 turbo(float t) {
    const vec3 kRedVec4 = vec3(0.13572138, 4.61539260, -42.66032258);
    const vec3 kGreenVec4 = vec3(0.09140261, 2.19418839, 4.84296658);
    const vec3 kBlueVec4 = vec3(0.10667330, 12.64194608, -60.58204836);
    const vec2 kRedVec2 = vec2(86.60572483, -18.19145175);
    const vec2 kGreenVec2 = vec2(-13.19531455, 2.19399915);
    const vec2 kBlueVec2 = vec2(12.56896911, -1.91060217);
    
    t = clamp(t, 0.0, 1.0);
    vec4 v4 = vec4(1.0, t, t * t, t * t * t);
    vec2 v2 = v4.zw * v4.z;
    
    return vec3(
        dot(v4, vec4(kRedVec4, 1.0)) + dot(v2, kRedVec2),
        dot(v4, vec4(kGreenVec4, 1.0)) + dot(v2, kGreenVec2),
        dot(v4, vec4(kBlueVec4, 1.0)) + dot(v2, kBlueVec2)
    );
}

// Inferno colormap
vec3 inferno(float t) {
    t = clamp(t, 0.0, 1.0);
    vec3 c0 = vec3(0.0002189403691192265, 0.001651004631001012, -0.01948089843709184);
    vec3 c1 = vec3(0.1065134194856116, 0.5639564367884091, 3.932712388889277);
    vec3 c2 = vec3(11.60249308247187, -3.972853965665698, -15.9423941062914);
    return c0 + t * (c1 + t * c2);
}

// Two-tone for reaction-diffusion
vec3 rd_twotone(float v, vec3 colorA, vec3 colorB) {
    return mix(colorA, colorB, v);
}

// Psychedelic cycling
vec3 rd_psychedelic(float v, float time) {
    return vec3(
        sin(v * 6.28318 + time) * 0.5 + 0.5,
        sin(v * 6.28318 + time + 2.0944) * 0.5 + 0.5,
        sin(v * 6.28318 + time + 4.18879) * 0.5 + 0.5
    );
}
