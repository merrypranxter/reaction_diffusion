#!/usr/bin/env python3
"""
Batch-render parameter space for Gray-Scott.
Generate images/videos across F/k ranges.
"""
import argparse
import numpy as np
from pathlib import Path
from tqdm import tqdm
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.gray_scott import GrayScottNumpy
from core.parameters import ALL_PEARSON_TYPES


def render_type_grid(output_dir: Path, size: int = 256, steps: int = 5000):
    """Render image for each Pearson type."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for ptype in tqdm(ALL_PEARSON_TYPES, desc="Rendering types"):
        sim = GrayScottNumpy(size=size, **ptype.with_diffusion())
        sim.run(steps)
        filename = f"{ptype.symbol}_{ptype.name.replace(' ', '_')}.png"
        sim.save_image(output_dir / filename)
        print(f"Saved {filename}")


def render_parameter_sweep(
    output_dir: Path,
    F_range: tuple = (0.01, 0.08),
    k_range: tuple = (0.03, 0.07),
    n_F: int = 20,
    n_k: int = 20,
    size: int = 128,
    steps: int = 3000
):
    """Render grid of (F, k) combinations."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    F_vals = np.linspace(F_range[0], F_range[1], n_F)
    k_vals = np.linspace(k_range[0], k_range[1], n_k)
    
    for F in tqdm(F_vals, desc="F values"):
        for k in k_vals:
            sim = GrayScottNumpy(size=size, F=F, k=k)
            sim.run(steps)
            filename = f"F{F:.4f}_k{k:.4f}.png"
            sim.save_image(output_dir / filename)


def main():
    parser = argparse.ArgumentParser(description="Gray-Scott parameter scanner")
    parser.add_argument("command", choices=["types", "sweep"])
    parser.add_argument("-o", "--output", default="renders")
    parser.add_argument("--size", type=int, default=256)
    parser.add_argument("--steps", type=int, default=5000)
    
    args = parser.parse_args()
    output = Path(args.output)
    
    if args.command == "types":
        render_type_grid(output, args.size, args.steps)
    elif args.command == "sweep":
        render_parameter_sweep(output, size=args.size, steps=args.steps)


if __name__ == "__main__":
    main()
