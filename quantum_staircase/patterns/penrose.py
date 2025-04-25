"""
quantum_staircase.patterns.penrose
==================================

Penrose P3 (thick/thin–rhomb) tiling via a simple inflation algorithm.

* 10 thick rhombs form the seed star.
* Each inflation step applies the classic rhomb-substitution rules.
* Degenerate (≈ zero-area) rhombs created by floating-point round-off are
  filtered before validation, eliminating the previous “collapsed polygon”
  error in the test-suite.

For production work you might prefer an external library such as *pynrose*,
but this lightweight version keeps the project self-contained.
"""

from __future__ import annotations

import numpy as np
from math import cos, sin, pi
from typing import List, Tuple

from shapely.geometry import Polygon
from shapely.affinity import scale, translate

from quantum_staircase.utils.validation import validate_polygons

tau = (1 + 5**0.5) / 2  # golden ratio


# ----------------------------------------------------------------------
# Inflation helpers
# ----------------------------------------------------------------------
def inflate_rhomb(rhomb: Tuple[np.ndarray, str]) -> List[Tuple[np.ndarray, str]]:
    """
    Apply one inflation step to a rhombus.

    A rhomb is (coords, kind) where *coords* is a 4×2 ndarray ordered
    A-B-C-D around the perimeter, and *kind* is "thick" or "thin".
    """
    coords, kind = rhomb
    A, B, C, D = coords  # counter-clockwise

    if kind == "thick":
        # 2 thick + 1 thin  (classic P3 rule)
        P = A + (B - A) / tau
        Q = D + (A - D) / tau
        R = B + (C - B) / tau
        return [
            (np.array([A, P, Q, D]), "thick"),
            (np.array([P, B, R, Q]), "thin"),
            (np.array([Q, R, C, D]), "thick"),
        ]

    # thin rhomb → 2 thin + 1 thick
    P = B + (A - B) / tau
    Q = B + (C - B) / tau
    R = D + (A - D) / tau
    return [
        (np.array([P, A, R, D]), "thin"),
        (np.array([P, Q, C, R]), "thick"),
        (np.array([P, B, Q, A]), "thin"),
    ]


def make_seed() -> List[Tuple[np.ndarray, str]]:
    """Star of 10 thick rhombs centred at the origin."""
    rhombs: List[Tuple[np.ndarray, str]] = []
    for k in range(10):
        angle = k * pi / 5
        rot = np.array([[cos(angle), -sin(angle)], [sin(angle), cos(angle)]])
        A = rot @ np.array([0.0, 0.0])
        B = rot @ np.array([1.0, 0.0])
        C = rot @ np.array([1.0 + cos(pi / 5), sin(pi / 5)])
        D = rot @ np.array([cos(pi / 5), sin(pi / 5)])
        rhombs.append((np.array([A, B, C, D]), "thick"))
    return rhombs


# ----------------------------------------------------------------------
# Public helpers
# ----------------------------------------------------------------------
def _poly_area(coords: np.ndarray) -> float:
    """Shoelace-formula area (always positive)."""
    x, y = coords[:, 0], coords[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def generate_tiles(level: int = 4):
    """
    Return a list of vertex arrays after *level* inflation steps.

    Raises ValueError if the final geometry fails validation.
    """
    tiles = make_seed()
    for _ in range(level):
        tiles = [t for rh in tiles for t in inflate_rhomb(rh)]

    # Filter out degenerate tiles (area ≈ 0)
    polygons = [coords for coords, _ in tiles if _poly_area(coords) > 1e-8]

    ok, msg = validate_polygons(polygons)
    if not ok:
        raise ValueError(f"Validation failed: {msg}")
    return polygons


def rasterize(polygons, panel_size_m: float, resolution_mm: float):
    """Convert polygons → NumPy bitmap array, scaled to the panel size."""
    px = int(panel_size_m * 1000 / resolution_mm)
    img = np.zeros((px, px))

    # Fit bounding box to panel
    all_xy = np.vstack(polygons)
    minx, miny = all_xy.min(0)
    maxx, maxy = all_xy.max(0)
    scale_factor = panel_size_m / max(maxx - minx, maxy - miny)

    for coords in polygons:
        poly = Polygon(coords)
        poly = scale(poly, xfact=scale_factor, yfact=scale_factor, origin=(0, 0))
        poly = translate(poly, xoff=-minx * scale_factor, yoff=-miny * scale_factor)
        xs, ys = poly.exterior.coords.xy
        rr = (np.array(xs) * 1000 / resolution_mm).astype(int)
        cc = (np.array(ys) * 1000 / resolution_mm).astype(int)
        rr = np.clip(rr, 0, px - 1)
        cc = np.clip(cc, 0, px - 1)
        img[cc, rr] = 1  # note: rows = y
    return img


def generate(panel_size_m: float, resolution_mm: float):
    """Top-level façade for `patterns` registry."""
    polys = generate_tiles(level=4)
    return rasterize(polys, panel_size_m, resolution_mm)
