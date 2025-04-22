"""Hyperbolic tiling approximated pattern for tensor networks."""
import numpy as np

def generate(panel_size_m, resolution_mm):
    px = int(panel_size_m * 1000 / resolution_mm)
    xx, yy = np.indices((px, px))
    r = np.hypot(xx - px/2, yy - px/2)
    pattern = np.sin(np.log1p(r))**2
    pattern = (pattern - pattern.min()) / (pattern.max() - pattern.min())
    return pattern
