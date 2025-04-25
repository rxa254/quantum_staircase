# Quantum Staircase Tiling Generator

[![CI](https://github.com/rxa254/quantum-staircase/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/rxa254/quantum-staircase/actions/workflows/ci.yml)
[![Python 3.9–3.11](https://img.shields.io/badge/python-3.9‒3.11-blue.svg)](https://www.python.org/)  
[![License MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Generate large-scale, physics-inspired wall panels (3 m × 3 m, ≥ 1 mm pixel pitch) for Caltech’s four-story quantum staircase. Themes evolve from **LIGO interferometry** to **emergent spacetime**.

<p align="center">
  <img src="docs/img/demo_ligo.png"  alt="LIGO fringe thumbnail"   width="32%">
  <img src="docs/img/demo_penrose.png" alt="Penrose tiling thumbnail" width="32%">
</p>

---

## 1 Quick start

    git clone https://github.com/rxa254/quantum-staircase.git
    cd quantum-staircase
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    python examples/generate_panel.py --theme ligo --outfile ligo_panel.png
    pytest -q

---

## 2 Repository layout

    patterns/     physics & math pattern generators
    utils/        geometry, validation, export helpers
    vendor/       vendored deps (pynrose_core)
    examples/     one-shot demo scripts
    tests/        pytest unit tests
    scripts/      update_thumbnails.py
    docs/img/     thumbnails for this README
    .github/      CI workflow
    README.md     you’re here
    requirements.txt

---

## 3 Public API snapshot

| Module | Key helpers | Purpose |
|--------|-------------|---------|
| `quantum_staircase.patterns` | `list_themes()` · `get_theme()` | Discover generators |
| theme modules | `generate(size_m, res_mm)` | Return NumPy image |
| `utils.validation` | `validate_polygons()` | Forbid overlaps (gaps OK) |
| `utils.export` | `save_image()` | Write PNG/SVG panel |

---

## 4 Examples

*Penrose panel*

    python examples/generate_panel.py --theme penrose --outfile penrose.png

*Blend two themes*

    from quantum_staircase import patterns, utils
    import numpy as np

    size, res = 3.0, 1.0
    a = patterns.get_theme("ligo")(size, res)
    b = patterns.get_theme("quantum_optics")(size, res)
    utils.export.save_image(0.5*a + 0.5*b, "blend.png", size, res)

---

## 5 CI pipeline

* Install deps → run `pytest`  
* Rebuild README thumbnails via `scripts/update_thumbnails.py`; upload as artifacts if changed.

---

## 6 Adding a new pattern

1. Create `patterns/<name>.py` containing:

       def generate(panel_size_m: float, resolution_mm: float):
           ...

2. Register it in `patterns/__init__.py`.  
3. Add a unit test under `tests/`.

---

## 7 License

[MIT](LICENSE)
