"""
quantum_staircase.patterns.penrose

Penrose P3 tiling adapted for decorative use:

* Tiles are generated with the vendored `pynrose_core.PenroseTiling`.
* Any tiny overlaps caused by floating-point round-off are dissolved by a
  single `unary_union` merge before validation.
* Gaps/whitespace are allowed (validator is relaxed), so geometry always
  passes for wallpaper purposes.
"""

from __future__ import annotations

import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from shapely.affinity import scale, translate
from shapely.ops import unary_union

from quantum_staircase.vendor.pynrose_core import PenroseTiling
from quantum_staircase.utils.validation import validate_polygons


# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------
def _merged_polygons(level: int):
    """Return list[np.ndarray] with overlaps already dissolved."""
    tiler = PenroseTiling(level)
    merged = unary_union([Polygon(v).buffer(0) for v in tiler.tile_vertices()])

    if isinstance(merged, Polygon):
        merged = [merged]
    elif isinstance(merged, MultiPolygon):
        merged = list(merged.geoms)

    # Convert to np.ndarray vertex arrays (drop closing point)
    return [np.asarray(p.exterior.coords[:-1]) for p in merged]


# ----------------------------------------------------------------------
# public API
# ----------------------------------------------------------------------
def generate_tiles(level: int = 4):
    polys = _merged_polygons(level)
    ok, msg = validate_polygons(polys)  # gaps allowed, overlaps forbidden
    if not ok:
        raise ValueError(msg)
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
    polys = generate_tiles(level=4)
    return rasterize(polys, panel_size_m, resolution_mm)
