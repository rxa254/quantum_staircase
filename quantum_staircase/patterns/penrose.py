"""Penrose P3 rhombus tiling via inflation/deflation.

Returns high‑resolution raster image for now. For tile geometry,
the validation utilities can use the polygon list from `tiles`.
"""
import numpy as np
from math import cos, sin, pi
from shapely.geometry import Polygon
from quantum_staircase.utils.validation import validate_polygons

tau = (1 + 5 ** 0.5) / 2  # golden ratio

def inflate_rhomb(rhomb):
    """Inflation rules for thick/thin rhombs. Each rhomb is (coords, type)."""
    coords, kind = rhomb
    A, B, C, D = coords
    if kind == "thick":
        P = A + (B - A) / tau
        Q = B + (C - B) / tau
        return [
            (np.array([A, P, D, P]), "thick"),
            (np.array([P, B, Q, P]), "thin"),
            (np.array([D, P, Q, C]), "thick"),
        ]
    else:  # thin
        P = B + (A - B) / tau
        return [
            (np.array([P, A, D, P]), "thin"),
            (np.array([B, C, D, P]), "thick"),
        ]

def make_seed():
    """Seed: star of 10 rhombs."""
    rhombs = []
    for k in range(10):
        angle = k * pi / 5
        rot = np.array([[cos(angle), -sin(angle)], [sin(angle), cos(angle)]])
        A = rot @ np.array([0, 0])
        B = rot @ np.array([1, 0])
        C = rot @ np.array([1 + cos(pi/5), sin(pi/5)])
        D = rot @ np.array([cos(pi/5), sin(pi/5)])
        rhombs.append((np.array([A, B, C, D]), "thick"))
    return rhombs

def generate_tiles(level=4):
    tiles = make_seed()
    for _ in range(level):
        new_tiles = []
        for t in tiles:
            new_tiles.extend(inflate_rhomb(t))
        tiles = new_tiles
    polygons = [coords for coords, _ in tiles]
    ok, msg = validate_polygons(polygons)
    if not ok:
        raise ValueError(f"Validation failed: {msg}")
    return polygons

def rasterize(polygons, panel_size_m, resolution_mm):
    px = int(panel_size_m * 1000 / resolution_mm)
    img = np.zeros((px, px))
    from shapely.affinity import scale, translate
    # scale to fit
    all_coords = np.vstack(polygons)
    minx, miny = all_coords.min(0)
    maxx, maxy = all_coords.max(0)
    s = panel_size_m / max(maxx - minx, maxy - miny)
    for poly in polygons:
        p = Polygon(poly)
        p = scale(p, xfact=s, yfact=s, origin=(0, 0))
        p = translate(p, xoff=-minx*s, yoff=-miny*s)
        xs, ys = p.exterior.coords.xy
        rr = (np.array(xs) * 1000 / resolution_mm).astype(int)
        cc = (np.array(ys) * 1000 / resolution_mm).astype(int)
        rr = np.clip(rr, 0, px-1)
        cc = np.clip(cc, 0, px-1)
        img[cc, rr] = 1
    return img

def generate(panel_size_m, resolution_mm):
    polys = generate_tiles(level=4)
    return rasterize(polys, panel_size_m, resolution_mm)
