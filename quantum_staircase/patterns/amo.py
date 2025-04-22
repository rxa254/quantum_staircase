"""Circular AMO trap lattice pattern."""
import numpy as np

def generate(panel_size_m, resolution_mm):
    px = int(panel_size_m * 1000 / resolution_mm)
    center = px / 2
    yy, xx = np.indices((px, px))
    r = np.hypot(xx-center, yy-center)
    pattern = np.sin(r / 15) ** 2
    pattern = (pattern - pattern.min()) / (pattern.max() - pattern.min())
    return pattern
