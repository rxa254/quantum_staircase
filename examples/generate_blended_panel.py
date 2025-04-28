#!/usr/bin/env python
"""
examples/generate_blended_panel.py
==================================

Generate a *single* wall-panel image whose pattern morphs smoothly through
multiple physics themes.

• Works out of the box with **PNG or SVG**:
      --outfile wall.svg   → vector, infinite zoom
      --outfile wall.png   → raster bitmap

• Blending direction:
      --axis y   (default)  bottom → top
      --axis x              left   → right

• Size and resolution are independent:
      --width-m  3   --height-m 20 --resolution-mm 1

-------------------------------------------------------------------------------
USAGE EXAMPLE  (vertical gradient for a 3×20 m wall)
-------------------------------------------------------------------------------
PYTHONPATH=. python examples/generate_blended_panel.py \
        --themes ligo quantum_optics amo qec tensor penrose \
        --width-m 3 --height-m 20 \
        --axis y \
        --blend-fraction 0.12 \
        --resolution-mm 1 \
        --outfile wall_3x20.svg
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

import numpy as np

from quantum_staircase import patterns
from quantum_staircase.utils import svg_export, export


# ──────────────────────────────────────────────────────────────────────────────
# core math helpers
# ──────────────────────────────────────────────────────────────────────────────
def _cos_blend(a: np.ndarray, b: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Cosine-smoothed blend between two arrays along the blending axis."""
    weight = (1 - np.cos(np.pi * w)) / 2  # 0→1
    return (1 - weight) * a + weight * b


def _generate_theme_image(name: str, size_m: float, res_mm: float) -> np.ndarray:
    """Call the theme’s generator at the requested physical resolution."""
    gen = patterns.get_theme(name)
    return gen(size_m, res_mm)


# ──────────────────────────────────────────────────────────────────────────────
# panel assembly
# ──────────────────────────────────────────────────────────────────────────────
def build_panel(
    width_m: float,
    height_m: float,
    res_mm: float,
    theme_names: List[str],
    blend_frac: float,
    axis: str = "y",
) -> np.ndarray:
    """
    Return a NumPy image array with smooth transitions.

    axis = 'y' → vertical morph; 'x' → horizontal.
    """
    px_w = int(width_m * 1000 / res_mm)
    px_h = int(height_m * 1000 / res_mm)
    n = len(theme_names)
    slice_px = (px_h if axis == "y" else px_w) // n
    blend_px = max(1, int(blend_frac * slice_px))

    # Pre-render each theme over the *entire* canvas so colours match in blends
    theme_img = {
        t: _generate_theme_image(t, max(width_m, height_m), res_mm)[:px_h, :px_w]
        for t in theme_names
    }

    panel = np.zeros((px_h, px_w))

    # Paste core slices
    for i, t in enumerate(theme_names):
        if axis == "y":
            y0, y1 = i * slice_px, (i + 1) * slice_px
            panel[y0:y1, :] = theme_img[t][y0:y1, :]
        else:
            x0, x1 = i * slice_px, (i + 1) * slice_px
            panel[:, x0:x1] = theme_img[t][:, x0:x1]

    # Blend interfaces
    for i in range(n - 1):
        tA, tB = theme_names[i], theme_names[i + 1]
        if axis == "y":
            y_mid = (i + 1) * slice_px
            y0, y1 = y_mid - blend_px, y_mid + blend_px
            w = np.linspace(0, 1, y1 - y0)[:, None]
            panel[y0:y1, :] = _cos_blend(theme_img[tA][y0:y1, :], theme_img[tB][y0:y1, :], w)
        else:
            x_mid = (i + 1) * slice_px
            x0, x1 = x_mid - blend_px, x_mid + blend_px
            w = np.linspace(0, 1, x1 - x0)
            panel[:, x0:x1] = _cos_blend(theme_img[tA][:, x0:x1], theme_img[tB][:, x0:x1], w)

    return np.clip(panel, 0, 1)


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="Generate a blended wall panel")
    p.add_argument("--themes", nargs="+", required=True, help="Theme names in order")
    p.add_argument("--width-m", type=float, required=True, help="Panel width  (m)")
    p.add_argument("--height-m", type=float, required=True, help="Panel height (m)")
    p.add_argument("--axis", choices=["x", "y"], default="y", help="Blend direction")
    p.add_argument("--blend-fraction", type=float, default=0.12, help="0–0.5")
    p.add_argument("--resolution-mm", type=float, default=1.0, help="Pixel pitch")
    p.add_argument("--outfile", required=True, help="PNG or SVG file")
    args = p.parse_args()

    wall = build_panel(
        args.width_m,
        args.height_m,
        args.resolution_mm,
        args.themes,
        args.blend_fraction,
        axis=args.axis,
    )

    out_path = Path(args.outfile)
    if out_path.suffix.lower() == ".svg":
        svg_export.save_svg(
            wall, out_path, panel_size_m=args.width_m, resolution_mm=args.resolution_mm
        )
    else:
        export.save_image(
            wall, out_path, size_m=args.width_m, res_mm=args.resolution_mm
        )
    print(f"Saved {out_path.resolve()}")


if __name__ == "__main__":
    main()
