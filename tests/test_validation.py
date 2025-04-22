import numpy as np
from quantum_staircase.utils.validation import validate_polygons
from shapely.geometry import Polygon
def test_simple_square():
    polys = [Polygon([(0,0),(1,0),(1,1),(0,1)])]
    ok, _ = validate_polygons([np.array(p.exterior.coords[:-1]) for p in polys])
    assert ok
