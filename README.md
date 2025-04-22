# Quantum Staircase Tiling Generator

Generate large‑scale, high‑resolution wall panels (3 m × 3 m, ≥ 1 mm pixel pitch) for the four‑story spiral staircase in the Caltech quantum‑precision building.  
The visual narrative evolves floor‑by‑floor—from **LIGO interferometry** to **emergent spacetime**.

---

## 1  Quick start (run straight from the repo)

```bash
git clone <this‑repo‑url> quantum‑staircase
cd quantum‑staircase
python -m venv .venv && source .venv/bin/activate   # optional isolation
pip install -r requirements.txt
```

### Demo panel

```bash
python examples/generate_panel.py --theme ligo --outfile ligo_panel.png
```

### Full test‑suite

```bash
pytest -q
```

---

## 2  Repository layout
```
patterns/        Physics + mathematical tile generators
utils/           Geometry, validation & export helpers
examples/        One‑shot demo scripts
tests/           Pytest unit tests
.github/         Continuous‑integration config
README.md        You’re here
requirements.txt Runtime deps
```

---

## 3  Public API cheatsheet

| Module | Helper | Purpose |
|--------|--------|---------|
| `quantum_staircase.patterns` | `list_themes()` | List available themes |
| | `get_theme(theme)` | Return generator callable |
| | _per‑theme_ `generate()` | NumPy array image |
| `quantum_staircase.utils.geometry` | `angle(p0,p1,p2)` | Interior angle (deg) |
| `quantum_staircase.utils.validation` | `validate_polygons(polys)` | Overlap / gap check |
| `quantum_staircase.utils.export` | `save_image(arr,path,size,res)` | Save PNG/SVG panel |
| **Demo CLI** | `python examples/generate_panel.py -h` | Usage help |

---

## 4  Examples

* **Penrose panel**

  ```bash
  python examples/generate_panel.py --theme penrose --outfile penrose.png
  ```

* **Blend two themes**

  ```python
  from quantum_staircase import patterns, utils
  import numpy as np
  size, res = 3.0, 1.0
  a = patterns.get_theme("ligo")(size, res)
  b = patterns.get_theme("quantum_optics")(size, res)
  blend = 0.5*a + 0.5*b
  utils.export.save_image(blend, "blend.png", size, res)
  ```

---

## 5  Validation pipeline

On every push GitHub Actions executes:

1. Unit tests (`pytest`)
2. Geometry checks on Penrose tiling
3. Export smoke‑test

All must pass before merge.

---

## 6  Adding new patterns

1. Create `patterns/<name>.py` with `generate(size_m, res_mm) -> np.ndarray`
2. Register in `patterns/__init__.py`
3. Add a unit test if geometry is non‑trivial

---

## 7  License  
MIT — see `LICENSE`.