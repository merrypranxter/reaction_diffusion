"""
Spatial parameter sweeps on GPU — generate full Pearson classification in one run.
"""
import torch
import numpy as np
from .gray_scott_torch import GrayScottTorch


class PearsonPlotGPU(GrayScottTorch):
    """
    Gray-Scott with spatially varying F and k parameters.
    Generates full parameter space map in single simulation.
    """
    
    def __init__(
        self,
        width: int = 1024,
        height: int = 1024,
        F_range: tuple = (0.0, 0.08),
        k_range: tuple = (0.03, 0.07),
        **kwargs
    ):
        """
        Initialize with parameter maps.
        
        Args:
            width: Grid width (maps to k axis)
            height: Grid height (maps to F axis)
            F_range: (min, max) feed rate
            k_range: (min, max) kill rate
        """
        super().__init__(width=width, height=height, **kwargs)
        self.F_range = F_range
        self.k_range = k_range
        
        # Create parameter maps
        # F varies on Y axis (rows), k varies on X axis (columns)
        F_vals = torch.linspace(F_range[0], F_range[1], height, device=self.device)
        k_vals = torch.linspace(k_range[0], k_range[1], width, device=self.device)
        
        self.F_map = F_vals.view(-1, 1).expand(height, width)
        self.k_map = k_vals.view(1, -1).expand(height, width)
        
        # Add batch/channel dims for broadcasting
        self.F_map = self.F_map.unsqueeze(0).unsqueeze(0)  # (1, 1, H, W)
        self.k_map = self.k_map.unsqueeze(0).unsqueeze(0)
    
    def step(self) -> tuple:
        """Step with spatial parameters."""
        return super().step(F=self.F_map, k=self.k_map)
    
    def get_parameter_at(self, x: int, y: int) -> tuple:
        """Get (F, k) at specific pixel."""
        F_val = self.F_map[0, 0, y, x].item()
        k_val = self.k_map[0, 0, y, x].item()
        return F_val, k_val
    
    def identify_pattern_region(self, x: int, y: int) -> str:
        """
        Rough identification of pattern type at location.
        (Requires analysis of local state)
        """
        # Extract local region
        region_size = 50
        x_start = max(0, x - region_size//2)
        x_end = min(self.width, x + region_size//2)
        y_start = max(0, y - region_size//2)
        y_end = min(self.height, y + region_size//2)
        
        local_B = self.B[0, 0, y_start:y_end, x_start:x_end]
        
        # Simple statistics for classification
        mean_B = local_B.mean().item()
        std_B = local_B.std().item()
        
        # Heuristic classification
        if std_B < 0.1:
            return "uniform"
        elif mean_B > 0.5:
            return "red_dominant"
        else:
            return "patterned"
