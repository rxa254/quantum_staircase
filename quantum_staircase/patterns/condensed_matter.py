"""Hexagonal lattice pattern inspired by 2D materials."""
import numpy as np

def generate(panel_size_m, resolution_mm):
    px = int(panel_size_m * 1000 / resolution_mm)
    xx, yy = np.meshgrid(np.arange(px), np.arange(px))
    pattern = ((xx + yy) % 6 < 3).astype(float)
    return pattern
