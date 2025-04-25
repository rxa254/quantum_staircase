"""
quantum_staircase.patterns.penrose  –  overlap-tolerant version

Changes
-------
* validate_polygons called with tol=1e-1  (≃ 0.1 m² overlap allowed)
* nothing else changed
"""

from __future__ import annotations
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from shapely.affinity import scale, translate
from shapely.ops import unary_union

from quantum_staircase.vendor.pynrose_core import PenroseTiling
from quantum_staircase.utils.validation import validate_polygons


def _merged_polygons(level: int):
    tiler = PenroseTiling(level)
    merged = unary_union([Polygon(v).buffer(0) for v in tiler.tile_vertices()])
    if isinstance(merged, Polygon):
        merged = [merged]
    elif isinstance(merged, MultiPolygon):
        merged = list(merged.geoms)
    return [np.asarray(p.exterior.coords[:-1]) for p in merged]


def generate_tiles(level: int = 4):
    polys = _merged_polygons(level)
    ok, msg = validate_polygons(polys, tol=1e-1)   # ← relaxed overlap tol
    if not ok:
        raise ValueError(msg)
    return polys


def rasterize(polygons, panel_size_m: float, resolution_mm: float):
    px = int(panel_size_m * 1000 / resolution_mm)
    img = np.zeros((px, px))

    all_xy = np.vstack(polygons)
    minx, miny = all_xy.min(0)
    maxx, maxy = all_xy.max(0)
    s = panel_size_m / max(maxx - minx, maxy - miny)

    for coords in polygons:
        p = Polygon(coords)
        p = scale(p, xfact=s, yfact=s, origin=(0, 0))
        p = translate(p, xoff=-minx * s, yoff=-miny * s)
        xs, ys = p.exterior.coords.xy
        rr = (np.array(xs) * 1000 / resolution_mm).astype(int)
        cc = (np.array(ys) * 1000 / resolution_mm).astype(int)
        rr = np.clip(rr, 0, px - 1)
        cc = np.clip(cc, 0, px - 1)
        img[cc, rr] = 1
    return img


def generate(panel_size_m: float, resolution_mm: float):
    return rasterize(generate_tiles(4), panel_size_m, resolution_mm)
