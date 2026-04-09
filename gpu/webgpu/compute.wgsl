// WebGPU compute shader for Gray-Scott reaction-diffusion
// Uses storage textures for ping-pong rendering

@group(0) @binding(0) var uCurrent: texture_storage_2d<rg32float, read>;
@group(0) @binding(1) var vCurrent: texture_storage_2d<rg32float, read>;
@group(0) @binding(2) var uNext: texture_storage_2d<rg32float, write>;
@group(0) @binding(3) var vNext: texture_storage_2d<rg32float, write>;
@group(0) @binding(4) var<uniform> params: SimulationParams;

struct SimulationParams {
    Du: f32,
    Dv: f32,
    F: f32,
    k: f32,
    dt: f32,
    width: u32,
    height: u32,
};

// 9-point weighted Laplacian
fn laplacianU(x: u32, y: u32) -> f32 {
    let w = params.width;
    let h = params.height;
    
    // Helper to sample with periodic BC
    let sample = |dx: i32, dy: i32| -> f32 {
        let sx = u32((i32(x) + dx + i32(w)) % i32(w));
        let sy = u32((i32(y) + dy + i32(h)) % i32(h));
        return textureLoad(uCurrent, vec2<u32>(sx, sy)).r;
    };
    
    return
        0.05 * sample(-1, -1) + 0.20 * sample(0, -1) + 0.05 * sample(1, -1) +
        0.20 * sample(-1, 0)  - 1.00 * sample(0, 0)  + 0.20 * sample(1, 0) +
        0.05 * sample(-1, 1)  + 0.20 * sample(0, 1)  + 0.05 * sample(1, 1);
}

fn laplacianV(x: u32, y: u32) -> f32 {
    let w = params.width;
    let h = params.height;
    
    let sample = |dx: i32, dy: i32| -> f32 {
        let sx = u32((i32(x) + dx + i32(w)) % i32(w));
        let sy = u32((i32(y) + dy + i32(h)) % i32(h));
        return textureLoad(vCurrent, vec2<u32>(sx, sy)).r;
    };
    
    return
        0.05 * sample(-1, -1) + 0.20 * sample(0, -1) + 0.05 * sample(1, -1) +
        0.20 * sample(-1, 0)  - 1.00 * sample(0, 0)  + 0.20 * sample(1, 0) +
        0.05 * sample(-1, 1)  + 0.20 * sample(0, 1)  + 0.05 * sample(1, 1);
}

@compute @workgroup_size(8, 8)
fn main(@builtin(global_invocation_id) global_id: vec3<u32>) {
    let x = global_id.x;
    let y = global_id.y;
    
    if (x >= params.width || y >= params.height) {
        return;
    }
    
    let u = textureLoad(uCurrent, vec2<u32>(x, y)).r;
    let v = textureLoad(vCurrent, vec2<u32>(x, y)).r;
    
    let Lu = laplacianU(x, y);
    let Lv = laplacianV(x, y);
    
    let reaction = u * v * v;
    
    let newU = u + params.dt * (params.Du * Lu - reaction + params.F * (1.0 - u));
    let newV = v + params.dt * (params.Dv * Lv + reaction - (params.F + params.k) * v);
    
    textureStore(uNext, vec2<u32>(x, y), vec4<f32>(clamp(newU, 0.0, 1.0), 0.0, 0.0, 1.0));
    textureStore(vNext, vec2<u32>(x, y), vec4<f32>(clamp(newV, 0.0, 1.0), 0.0, 0.0, 1.0));
}
