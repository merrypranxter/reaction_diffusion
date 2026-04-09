/**
 * WebGPU compute pipeline for Gray-Scott reaction-diffusion
 * Modern alternative to WebGL with better performance
 */
class GrayScottWebGPU {
    constructor(canvas) {
        this.canvas = canvas;
        this.device = null;
        this.context = null;
        this.pipeline = null;
        this.bindGroupLayout = null;
        this.uniformBuffer = null;
        
        // Simulation state
        this.width = 512;
        this.height = 512;
        this.params = {
            Du: 1.0,
            Dv: 0.5,
            F: 0.0545,
            k: 0.062,
            dt: 1.0,
            width: this.width,
            height: this.height
        };
        
        // Ping-pong textures
        this.textures = [];
        this.currentTexture = 0;
    }
    
    async init() {
        if (!navigator.gpu) {
            throw new Error('WebGPU not supported');
        }
        
        const adapter = await navigator.gpu.requestAdapter({
            powerPreference: 'high-performance'
        });
        if (!adapter) {
            throw new Error('Failed to get WebGPU adapter');
        }
        
        this.device = await adapter.requestDevice();
        this.context = this.canvas.getContext('webgpu');
        const canvasFormat = navigator.gpu.getPreferredCanvasFormat();
        this.context.configure({
            device: this.device,
            format: canvasFormat,
            alphaMode: 'premultiplied'
        });
        
        await this.createResources();
        await this.createPipeline();
    }
    
    async createResources() {
        const textureDescriptor = {
            size: [this.width, this.height],
            format: 'rg32float',
            usage: GPUTextureUsage.STORAGE_BINDING |
                   GPUTextureUsage.TEXTURE_BINDING |
                   GPUTextureUsage.COPY_DST
        };
        
        // Create ping-pong pairs for U and V
        for (let i = 0; i < 2; i++) {
            this.textures.push({
                u: this.device.createTexture(textureDescriptor),
                v: this.device.createTexture(textureDescriptor)
            });
        }
        
        // Initialize with seed
        await this.initializeSeed();
        
        // Uniform buffer
        this.uniformBuffer = this.device.createBuffer({
            size: 32,  // 8 floats * 4 bytes
            usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST
        });
        this.updateUniforms();
    }
    
    async initializeSeed() {
        // Create center seed
        const uData = new Float32Array(this.width * this.height).fill(1.0);
        const vData = new Float32Array(this.width * this.height).fill(0.0);
        
        const cx = Math.floor(this.width / 2);
        const cy = Math.floor(this.height / 2);
        const r = Math.floor(this.width / 10);
        
        for (let y = cy - r; y < cy + r; y++) {
            for (let x = cx - r; x < cx + r; x++) {
                if ((x-cx)**2 + (y-cy)**2 < r**2) {
                    const idx = y * this.width + x;
                    uData[idx] = 0.5;
                    vData[idx] = 0.25;
                }
            }
        }
        
        // Upload to textures
        for (const texSet of this.textures) {
            this.device.queue.writeTexture(
                { texture: texSet.u },
                uData.buffer,
                { bytesPerRow: this.width * 8 },
                [this.width, this.height]
            );
            this.device.queue.writeTexture(
                { texture: texSet.v },
                vData.buffer,
                { bytesPerRow: this.width * 8 },
                [this.width, this.height]
            );
        }
    }
    
    updateUniforms() {
        const uniformData = new Float32Array([
            this.params.Du,
            this.params.Dv,
            this.params.F,
            this.params.k,
            this.params.dt,
            this.params.width,
            this.params.height,
            0  // padding
        ]);
        this.device.queue.writeBuffer(this.uniformBuffer, 0, uniformData);
    }
    
    async createPipeline() {
        // Load WGSL shader
        const response = await fetch('compute.wgsl');
        const shaderCode = await response.text();
        
        const shaderModule = this.device.createShaderModule({
            code: shaderCode
        });
        
        this.bindGroupLayout = this.device.createBindGroupLayout({
            entries: [
                { binding: 0, visibility: GPUShaderStage.COMPUTE, storageTexture: { access: 'read-only', format: 'rg32float' } },
                { binding: 1, visibility: GPUShaderStage.COMPUTE, storageTexture: { access: 'read-only', format: 'rg32float' } },
                { binding: 2, visibility: GPUShaderStage.COMPUTE, storageTexture: { access: 'write-only', format: 'rg32float' } },
                { binding: 3, visibility: GPUShaderStage.COMPUTE, storageTexture: { access: 'write-only', format: 'rg32float' } },
                { binding: 4, visibility: GPUShaderStage.COMPUTE, buffer: { type: 'uniform' } }
            ]
        });
        
        const pipelineLayout = this.device.createPipelineLayout({
            bindGroupLayouts: [this.bindGroupLayout]
        });
        
        this.pipeline = this.device.createComputePipeline({
            layout: pipelineLayout,
            compute: {
                module: shaderModule,
                entryPoint: 'main'
            }
        });
    }
    
    createBindGroup(readIdx, writeIdx) {
        return this.device.createBindGroup({
            layout: this.bindGroupLayout,
            entries: [
                { binding: 0, resource: this.textures[readIdx].u.createView() },
                { binding: 1, resource: this.textures[readIdx].v.createView() },
                { binding: 2, resource: this.textures[writeIdx].u.createView() },
                { binding: 3, resource: this.textures[writeIdx].v.createView() },
                { binding: 4, resource: { buffer: this.uniformBuffer } }
            ]
        });
    }
    
    step() {
        const readIdx = this.currentTexture;
        const writeIdx = 1 - this.currentTexture;
        
        const bindGroup = this.createBindGroup(readIdx, writeIdx);
        
        const commandEncoder = this.device.createCommandEncoder();
        const passEncoder = commandEncoder.beginComputePass();
        passEncoder.setPipeline(this.pipeline);
        passEncoder.setBindGroup(0, bindGroup);
        passEncoder.dispatchWorkgroups(
            Math.ceil(this.width / 8),
            Math.ceil(this.height / 8)
        );
        passEncoder.end();
        
        this.device.queue.submit([commandEncoder.finish()]);
        this.currentTexture = writeIdx;
    }
    
    setParams(newParams) {
        Object.assign(this.params, newParams);
        this.updateUniforms();
    }
}

export { GrayScottWebGPU };
