#!/usr/bin/env python3
"""
Performance profiling for reaction-diffusion implementations.
"""
import time
import argparse
import json
from pathlib import Path
from typing import Dict, List
import numpy as np
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.gray_scott import GrayScottNumpy
from core.parameters import DELTA


class Profiler:
    """Profile different implementations."""
    
    def __init__(self, sizes: List[int] = [128, 256, 512, 1024]):
        self.sizes = sizes
        self.results = {}
    
    def profile_numpy(self, size: int, n_steps: int = 100) -> Dict:
        """Profile NumPy implementation."""
        sim = GrayScottNumpy(size=size, **DELTA.with_diffusion())
        
        # Warmup
        sim.step(10)
        
        # Time it
        start = time.perf_counter()
        sim.step(n_steps)
        elapsed = time.perf_counter() - start
        
        return {
            "implementation": "numpy",
            "size": size,
            "steps": n_steps,
            "total_time": elapsed,
            "ms_per_step": elapsed * 1000 / n_steps,
            "cells_per_second": (size * size * n_steps) / elapsed
        }
    
    def profile_pytorch(self, size: int, n_steps: int = 100) -> Dict:
        """Profile PyTorch GPU implementation."""
        try:
            import torch
            from gpu.pytorch.gray_scott_torch import GrayScottTorch
            
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            sim = GrayScottTorch(width=size, height=size, device=device)
            
            # Warmup
            sim.step_n(10)
            
            # Synchronize before timing
            if device == 'cuda':
                torch.cuda.synchronize()
            
            start = time.perf_counter()
            sim.step_n(n_steps)
            
            if device == 'cuda':
                torch.cuda.synchronize()
            
            elapsed = time.perf_counter() - start
            
            return {
                "implementation": "pytorch",
                "device": device,
                "size": size,
                "steps": n_steps,
                "total_time": elapsed,
                "ms_per_step": elapsed * 1000 / n_steps,
                "cells_per_second": (size * size * n_steps) / elapsed
            }
        except ImportError:
            return {"error": "PyTorch not installed"}
    
    def profile_all(self) -> Dict:
        """Run full profiling suite."""
        implementations = [
            ("numpy", self.profile_numpy),
            ("pytorch", self.profile_pytorch),
        ]
        
        for name, profile_fn in implementations:
            self.results[name] = []
            for size in self.sizes:
                print(f"Profiling {name} at {size}x{size}...")
                result = profile_fn(size)
                self.results[name].append(result)
                if "error" not in result:
                    print(f"  {result['ms_per_step']:.3f} ms/step")
        
        return self.results
    
    def generate_report(self, output_path: Path):
        """Generate markdown report."""
        lines = [
            "# Performance Benchmark Results\n",
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            "## Summary\n\n",
            "| Implementation | Size | ms/step | Cells/second |\n",
            "|----------------|------|---------|--------------|\n"
        ]
        
        for impl_name, results in self.results.items():
            for r in results:
                if "error" not in r:
                    lines.append(
                        f"| {impl_name} | {r['size']}x{r['size']} | "
                        f"{r['ms_per_step']:.3f} | "
                        f"{r['cells_per_second']:.2e} |\n"
                    )
        
        # Speedup analysis
        lines.extend([
            "\n## GPU Speedup Analysis\n\n",
            "| Size | CPU (ms) | GPU (ms) | Speedup |\n",
            "|------|----------|----------|---------|\n"
        ])
        
        if "numpy" in self.results and "pytorch" in self.results:
            for cpu_r, gpu_r in zip(self.results["numpy"], self.results["pytorch"]):
                if "error" not in cpu_r and "error" not in gpu_r:
                    speedup = cpu_r["ms_per_step"] / gpu_r["ms_per_step"]
                    lines.append(
                        f"| {cpu_r['size']}x{cpu_r['size']} | "
                        f"{cpu_r['ms_per_step']:.3f} | "
                        f"{gpu_r['ms_per_step']:.3f} | "
                        f"{speedup:.1f}x |\n"
                    )
        
        output_path.write_text("".join(lines))
        print(f"Report saved to {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int, default=[128, 256, 512])
    parser.add_argument("--output", type=Path, default="benchmark_results.md")
    parser.add_argument("--json", type=Path, default=None)
    
    args = parser.parse_args()
    
    profiler = Profiler(sizes=args.sizes)
    results = profiler.profile_all()
    profiler.generate_report(args.output)
    
    if args.json:
        with open(args.json, 'w') as f:
            json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
