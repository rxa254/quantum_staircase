"""Geometry validation of tilings."""
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

def validate_polygons(polygons, tol=1e-9):
    """Return (bool ok, str message). Checks:
    * no overlaps
    * fully closed polygons
    * coverage (union area equals sum areas)
    """
    polys = [Polygon(p) for p in polygons]
    for p in polys:
        if not p.is_valid:
            return False, "Invalid polygon detected"
    union = unary_union(polys)
    if not isinstance(union, (Polygon, MultiPolygon)):
        return False, "Union not polygonal"
    area_sum = sum(p.area for p in polys)
    if abs(union.area - area_sum) > tol:
        return False, "Overlap or gaps detected"
    return True, "Geometry validated"
