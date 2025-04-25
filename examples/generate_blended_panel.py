#!/usr/bin/env python
"""
examples/generate_blended_panel.py
----------------------------------

Create a *rectangular* blended panel – perfect for a 3 m × 20 m wall.

Default: blend themes **horizontally** in the order given, so the pattern
evolves left→right across 20 m while the 3 m height stays constant.

Usage:

    python examples/generate_blended_panel.py \
            --themes ligo quantum_optics penrose \
            --width-m 20 --height-m 3 \
            --outfile wall_3x20.png \
            --blend-fraction 0.10

Arguments
---------
--themes            list of themes in left→right order
--width-m           total wall width  (default 3.0)
--height-m          total wall height (default 3.0)
--resolution-mm     pixel pitch (default 1.0 mm)
--blend-fraction    fraction of slice width used for cross-fade (0–0.5)

The script works for any rectangle; set width < height to blend vertically.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from quantum_staircase import patterns, utils


# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------
def cosine_mix(a: np.ndarray, b: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Cosine-smoothed blend between two same-shape arrays along x-axis."""
    weight = (1 - np.cos(np.pi * w)) / 2  # smoothstep
    return (1 - weight) * a + weight * b


def build_panel(width_m, height_m, res_mm, theme_names, blend_frac, axis="x"):
    """
    axis = 'x' → blend left→right slices
    axis = 'y' → blend bottom→top slices
    """
    px_w = int(width_m * 1000 / res_mm)
    px_h = int(height_m * 1000 / res_mm)

    n = len(theme_names)
    slice_px = (px_w if axis == "x" else px_h) // n
    blend_px = int(blend_frac * slice_px)

    # generate full-size arrays for each theme
    theme_imgs = {
        name: patterns.get_theme(name)(max(width_m, height_m), res_mm)
        for name in theme_names
    }

    panel = np.zeros((px_h, px_w))

    for i, name in enumerate(theme_names):
        if axis == "x":
            x0, x1 = i * slice_px, (i + 1) * slice_px
            panel[:, x0:x1] = theme_imgs[name][:px_h, x0:x1]
        else:  # vertical blend
            y0, y1 = i * slice_px, (i + 1) * slice_px
            panel[y0:y1, :] = theme_imgs[name][y0:y1, :px_w]

    # blend interfaces
    for i in range(n - 1):
        if axis == "x":
            x_mid = (i + 1) * slice_px
            x0, x1 = x_mid - blend_px, x_mid + blend_px
            w = np.linspace(0, 1, x1 - x0)
            panel[:, x0:x1] = cosine_mix(
                theme_imgs[theme_names[i]][:px_h, x0:x1],
                theme_imgs[theme_names[i + 1]][:px_h, x0:x1],
                w,
            )
        else:
            y_mid = (i + 1) * slice_px
            y0, y1 = y_mid - blend_px, y_mid + blend_px
            w = np.linspace(0, 1, y1 - y0)[:, None]
            panel[y0:y1, :] = cosine_mix(
                theme_imgs[theme_names[i]][y0:y1, :px_w],
                theme_imgs[theme_names[i + 1]][y0:y1, :px_w],
                w,
            )

    return np.clip(panel, 0, 1)


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Generate blended wall panel")
    parser.add_argument(
        "--themes",
        nargs="+",
        default=["ligo", "quantum_optics", "penrose"],
        help="Theme names in blend order",
    )
    parser.add_argument("--width-m", type=float, default=3.0, help="Wall width (m)")
    parser.add_argument("--height-m", type=float, default=3.0, help="Wall height (m)")
    parser.add_argument("--resolution-mm", type=float, default=1.0, help="Pixel pitch")
    parser.add_argument(
        "--blend-fraction",
        type=float,
        default=0.15,
        help="Fraction of slice dimension used for blending (0–0.5)",
    )
    parser.add_argument(
        "--axis",
        choices=["x", "y"],
        default="x",
        help="Blend direction: x = left→right, y = bottom→top",
    )
    parser.add_argument("--outfile", required=True, help="Output PNG/SVG")
    args = parser.parse_args()

    panel = build_panel(
        args.width_m,
        args.height_m,
        args.resolution_mm,
        args.themes,
        args.blend_fraction,
        axis=args.axis,
    )
    utils.export.save_image(
        panel, Path(args.outfile), args.width_m, args.resolution_mm
    )
    print(f"Saved {args.outfile}")


if __name__ == "__main__":
    main()
