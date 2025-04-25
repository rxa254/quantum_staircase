from hypothesis import given, settings
import hypothesis.strategies as st
from quantum_staircase.patterns import penrose
from quantum_staircase.utils.validation import validate_polygons


@settings(max_examples=20, deadline=None)   # ← disable 200 ms deadline
@given(level=st.integers(min_value=1, max_value=6))
def test_penrose_any_level(level):
    polys = penrose.generate_tiles(level=level)
    ok, _ = validate_polygons(polys, tol=1e-1)
    assert ok
