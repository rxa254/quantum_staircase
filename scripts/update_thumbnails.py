#!/usr/bin/env python
"""
scripts/update_thumbnails.py
============================

Re-build README thumbnails:

* docs/img/demo_ligo.png
* docs/img/demo_penrose.png

Run locally with:
    python scripts/update_thumbnails.py

The CI workflow calls this after tests pass so the badge images always
reflect the current rendering code.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from quantum_staircase.patterns import ligo, penrose
from quantum_staircase.utils.export import save_image

# ----------------------------------------------------------------------
# config
# ----------------------------------------------------------------------
DOC_IMG = Path("docs") / "img"
DOC_IMG.mkdir(parents=True, exist_ok=True)

PANEL_SIZE_M = 0.3      # tiny thumbnail panel (0.3 m → 300 px at 1 mm)
RES_MM = 1.0            # 1 mm/pixel


# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------
def _thumbnail(theme_func, outfile: Path):
    arr = theme_func(PANEL_SIZE_M, RES_MM)
    # enhance contrast for small images
    arr = (arr - arr.min()) / (arr.max() - arr.min() + 1e-12)
    save_image(arr, outfile, PANEL_SIZE_M, RES_MM)
    print(f"wrote {outfile}")


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
if __name__ == "__main__":
    _thumbnail(ligo.generate, DOC_IMG / "demo_ligo.png")
    _thumbnail(penrose.generate, DOC_IMG / "demo_penrose.png")
