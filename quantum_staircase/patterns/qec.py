"""Surface code checkerboard."""
import numpy as np

def generate(panel_size_m, resolution_mm):
    px = int(panel_size_m * 1000 / resolution_mm)
    xx, yy = np.indices((px, px))
    pattern = ((xx//20 + yy//20) % 2).astype(float)
    return pattern
