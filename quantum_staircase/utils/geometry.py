"""Basic geometric helpers; avoids heavy dependencies when possible."""
import numpy as np
from math import atan2, degrees

def angle(p0, p1, p2):
    """Return angle (deg) p0‑p1‑p2."""
    a = np.array(p0) - np.array(p1)
    b = np.array(p2) - np.array(p1)
    return degrees(np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))))
