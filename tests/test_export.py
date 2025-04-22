from quantum_staircase.patterns import ligo
from quantum_staircase.utils.export import save_image
from pathlib import Path
import numpy as np

def test_export(tmp_path):
    arr = ligo.generate(0.1, 1)
    out = tmp_path / "panel.png"
    save_image(arr, out, 0.1, 1)
    assert out.exists() and out.stat().st_size > 0
