#!/usr/bin/env python3
"""
Generate video from Gray-Scott simulation.
"""
import argparse
import numpy as np
from pathlib import Path
import cv2
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.gray_scott import GrayScottNumpy


def generate_video(
    output_path: Path,
    F: float = 0.0545,
    k: float = 0.062,
    size: int = 512,
    fps: int = 30,
    duration: float = 10.0,
    steps_per_frame: int = 20
):
    """Generate MP4 video of simulation evolution."""
    total_frames = int(fps * duration)
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (size, size), isColor=False)
    
    sim = GrayScottNumpy(size=size, F=F, k=k)
    
    for frame in range(total_frames):
        sim.step(steps_per_frame)
        
        # Get image and write
        img = sim.to_image("v")
        # Convert to BGR for OpenCV
        img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        writer.write(img_bgr)
        
        if frame % 30 == 0:
            print(f"Frame {frame}/{total_frames}")
    
    writer.release()
    print(f"Saved {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--F", type=float, default=0.0545)
    parser.add_argument("--k", type=float, default=0.062)
    parser.add_argument("--size", type=int, default=512)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--duration", type=float, default=10.0)
    
    args = parser.parse_args()
    generate_video(**vars(args))


if __name__ == "__main__":
    main()
