"""Generate sinusoidal interference fringes reminiscent of LIGO arm cavity."""
import numpy as np

def generate(panel_size_m, resolution_mm):
    px = int(panel_size_m * 1000 / resolution_mm)
    x = np.linspace(0, 10*np.pi, px)
    y = np.linspace(0, 10*np.pi, px)
    xx, yy = np.meshgrid(x, y)
    pattern = 0.5 * (1 + np.cos(xx + yy))
    return pattern
