# quantum_staircase/utils/svg_export.py
"""
Vector (SVG) exporter for the Quantum Staircase project.

Every pattern generator already returns either
* NumPy bitmap arrays (0‒1 float), or
* lists of polygons (Penrose).

This module converts those outputs into **pure vector SVG** so the artwork
remains crisp at any zoom level.

Requirements
------------
pip install svgwrite numpy matplotlib

Public helpers
--------------
save_svg(arr_or_polys, outfile, panel_size_m, resolution_mm, cmap="viridis")

* If *arr_or_polys* is a NumPy 2-D array   → draws coloured rects
* If it is a list of polygons (Nx2 ndarray) → draws filled paths
"""

from __future__ import annotations

from typing import Sequence, Union

import numpy as np
import svgwrite
from matplotlib import cm


def _rgba(color):
    r, g, b, a = color
    return f"rgba({int(r*255)},{int(g*255)},{int(b*255)},{a:.3f})"


def _export_bitmap(arr: np.ndarray, dwg, size_px, cmap):
    h, w = arr.shape
    colormap = cm.get_cmap(cmap)
    pixel_w = size_px[0] / w
    pixel_h = size_px[1] / h
    for y in range(h):
        for x in range(w):
            c = colormap(arr[y, x])
            dwg.add(
                dwg.rect(
                    insert=(x * pixel_w, size_px[1] - (y + 1) * pixel_h),
                    size=(pixel_w, pixel_h),
                    fill=_rgba(c),
                    stroke="none",
                )
            )


def _export_polygons(polys: Sequence[np.ndarray], dwg, scale, cmap):
    colormap = cm.get_cmap(cmap)
    for i, poly in enumerate(polys):
        color = _rgba(colormap(i / len(polys)))
        path_data = [(poly[0][0] * scale, poly[0][1] * scale)]
        for x, y in poly[1:]:
            path_data.append((x * scale, y * scale))
        dwg.add(
            dwg.polygon(
                points=path_data,
                fill=color,
                stroke="none",
            )
        )


def save_svg(
    data: Union[np.ndarray, Sequence[np.ndarray]],
    outfile,
    panel_size_m: float,
    resolution_mm: float,
    cmap: str = "viridis",
):
    """
    Parameters
    ----------
    data           NumPy bitmap or list of polygons
    outfile        Path ending in .svg
    panel_size_m   Physical size (square panels assumed)
    resolution_mm  mm per unit in *data* (for bitmap only)
    cmap           Matplotlib colormap name
    """
    px = int(panel_size_m * 1000 / resolution_mm)
    dwg = svgwrite.Drawing(outfile, size=(f"{panel_size_m}m", f"{panel_size_m}m"))
    if isinstance(data, np.ndarray):
        _export_bitmap(data, dwg, (panel_size_m, panel_size_m), cmap)
    else:  # assume polygons
        # scale coordinates so max extent fits panel_size_m
        all_xy = np.vstack(data)
        minx, miny = all_xy.min(0)
        maxx, maxy = all_xy.max(0)
        scale = panel_size_m / max(maxx - minx, maxy - miny)
        _export_polygons(data, dwg, scale, cmap)
    dwg.save()
