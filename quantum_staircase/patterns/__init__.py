"""Pattern generators registry."""
from importlib import import_module

_THEMES = {
    "ligo": "ligo",
    "quantum_optics": "quantum_optics",
    "condensed_matter": "condensed_matter",
    "amo": "amo",
    "qec": "qec",
    "tensor": "tensor_networks",
    "penrose": "penrose",
}

def list_themes():
    return sorted(_THEMES.keys())

def get_theme(name):
    modname = _THEMES[name]
    mod = import_module(f"quantum_staircase.patterns.{modname}")
    return mod.generate
