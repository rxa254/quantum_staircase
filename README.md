# Quantum Staircase Tiling Generator
### Rana X Adhikari, 2025

[![CI](https://github.com/rxa254/quantum‑staircase/actions/workflows/ci.yml/badge.svg)](https://github.com/<YOUR‑ORG>/quantum‑staircase/actions/workflows/ci.yml)
[![Python 3.9‒3.11](https://img.shields.io/badge/python-3.9‒3.11-blue.svg)](https://www.python.org/)
[![License MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Generate large‑scale, high‑resolution wall panels (3 m × 3 m, ≥ 1 mm pixel pitch) for the four‑story spiral staircase in Caltech’s quantum‑precision building.  
The visual narrative evolves floor‑by‑floor—from **LIGO interferometry** to **emergent spacetime**.

<p align="center">
  <img alt="LIGO fringe demo" src="docs/img/demo_ligo.png"  width="32%">
  <img alt="Penrose demo"    src="docs/img/demo_penrose.png" width="32%">
</p>

---

## 1  Quick start (run straight from the repo)

```bash
git clone https://github.com/<YOUR‑ORG>/quantum‑staircase.git
cd quantum‑staircase
python -m venv .venv && source .venv/bin/activate   # optional isolation
pip install -r requirements.txt
```

Generate a sample panel:

```bash
python examples/generate_panel.py --theme ligo --outfile ligo_panel.png
```

Run the full test‑suite (geometry validation + export smoke test):

```bash
pytest -q
```

---

## 2  Repository layout
```
patterns/        Physics‑ & math‑inspired tile generators  
utils/           Geometry, validation & export helpers  
examples/        One‑shot demo scripts  
tests/           Pytest unit tests (run in CI)  
docs/img/        Thumbnails auto‑updated by CI  
.github/         Continuous‑integration config  
README.md        You’re here  
requirements.txt Runtime dependencies  
```

---

## 3  Public API cheatsheet

| Module | Helper | Purpose |
|--------|--------|---------|
| `quantum_staircase.patterns` | `list_themes()` | List available themes |
|  | `get_theme(name)` | Return generator callable |
|  | *per‑theme* `generate(size_m, res_mm)` | NumPy image array |
| `quantum_staircase.utils.geometry` | `angle(p0, p1, p2)` | Interior angle (deg) |
| `quantum_staircase.utils.validation` | `validate_polygons(polys)` | Detect overlaps / gaps |
| `quantum_staircase.utils.export` | `save_image(arr, path, size, res)` | Write PNG/SVG panel |
| **Demo CLI** | `python examples/generate_panel.py -h` | Usage help |

---

## 4  Examples

**Penrose panel**

```bash
python examples/generate_panel.py --theme penrose --outfile penrose.png
```

**Blend two themes**

```python
from quantum_staircase import patterns, utils
import numpy as np

size, res = 3.0, 1.0        # metres, millimetres
a = patterns.get_theme("ligo")(size, res)
b = patterns.get_theme("quantum_optics")(size, res)
blend = 0.5*a + 0.5*b
utils.export.save_image(blend, "blend.png", size, res)
```

---

## 5  Validation pipeline

GitHub Actions (`.github/workflows/ci.yml`) runs on every push:

1. Install dependencies  
2. Execute `pytest`  
3. If tests pass, regenerate thumbnails in **docs/img/** via  
   `scripts/update_thumbnails.py` (keeps README images current)

A green **CI** badge means geometry checks and exports pass on the latest commit.

---

## 6  Adding new patterns

1. Create `patterns/<name>.py` with  

   ```python
   def generate(panel_size_m: float, resolution_mm: float) -> np.ndarray:
       ...
   ```

2. Register it in `patterns/__init__.py`  
3. Add a unit test under `tests/` if geometry is non‑trivial

---

## 7  License  
[MIT](LICENSE)
