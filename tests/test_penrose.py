# tests/test_penrose.py
from hypothesis import given, settings
import hypothesis.strategies as st

from quantum_staircase.patterns import penrose
from quantum_staircase.utils.validation import validate_polygons


@settings(max_examples=30)
@given(level=st.integers(min_value=1, max_value=6))
def test_penrose_any_level(level):
    """
    Property-based: for inflation levels 1-6 the geometry is always valid.
    """
    polys = penrose.generate_tiles(level=level)
    ok, _ = validate_polygons(polys)
    assert ok
