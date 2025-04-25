# quantum_staircase/patterns/penrose.py
"""
Wrapper around the vendorised *pynrose_core* tiler so the rest of the project
keeps the same `generate(panel_size_m, resolution_mm)` façade.
"""

from __future__ import annotations

import numpy as np
from shapely.geometry import Polygon
from shapely.affinity import scale, translate

from quantum_staircase.vendor.pynrose_core import PenroseTiling
from quantum_staircase.utils.validation import validate_polygons


# ----------------------------------------------------------------------
# Geometry helpers
# ----------------------------------------------------------------------
def _np_polygons(level: int):
    """Return list[np.ndarray] for the given inflation level."""
    tiler = PenroseTiling(level)
    return [np.asarray(v) for v in tiler.tile_vertices()]


# ----------------------------------------------------------------------
# Public helpers
# ----------------------------------------------------------------------
def generate_tiles(level: int = 4):
    polys = _np_polygons(level)
    ok, msg = validate_polygons(polys)
    if not ok:
        raise ValueError(f"Penrose geometry failed validation: {msg}")
    return polys


def rasterize(polygons, panel_size_m: float, resolution_mm: float):
    px = int(panel_size_m * 1000 / resolution_mm)
    img = np.zeros((px, px))

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
        img[cc, rr] = 1
    return img


def generate(panel_size_m: float, resolution_mm: float):
    """Entry-point used by `patterns.__init__` registry."""
    polys = generate_tiles(level=4)
    return rasterize(polys, panel_size_m, resolution_mm)
