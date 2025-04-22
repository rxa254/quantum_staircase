"""Wigner‑function style pattern for a squeezed state slice."""
import numpy as np

def generate(panel_size_m, resolution_mm):
    px = int(panel_size_m * 1000 / resolution_mm)
    x = np.linspace(-3, 3, px)
    y = np.linspace(-3, 3, px)
    xx, yy = np.meshgrid(x, y)
    r = 0.8  # squeeze parameter
    pattern = np.exp(- (xx**2 * np.exp(2*r) + yy**2 * np.exp(-2*r)))
    pattern = (pattern - pattern.min()) / (pattern.max() - pattern.min())
    return pattern
