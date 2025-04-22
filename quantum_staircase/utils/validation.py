"""
quantum_staircase.utils.validation
==================================

Geometry‑validation helpers for tiling generators.

Public API
----------
validate_polygons(polygons, tol=1e-9)
    • polygons : Iterable[np.ndarray | Sequence[(x, y)]]
        Each item is an ordered list/array of vertex coordinates.
    • Returns  (ok: bool, msg: str)

The routine:

1. Cleans every polygon with `buffer(0)` to remove self‑intersections.
2. Verifies each cleaned polygon is valid and non‑empty.
3. Ensures the union of all polygons has the same area as the
   individual‑area sum (detects overlaps or gaps).
"""

from __future__ import annotations

from typing import Iterable, Sequence, Tuple

from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union


def _clean_polygon(coords: Sequence[Tuple[float, float]]) -> Polygon:
    """
    Return a topologically valid version of the polygon defined by *coords*.
    Uses `buffer(0)`; raises ValueError if the result is empty or invalid.
    """
    poly = Polygon(coords).buffer(0)
    if poly.is_empty:
        raise ValueError("Polygon collapsed to empty after cleaning")
    if not poly.is_valid:
        raise ValueError("Polygon is invalid after cleaning")
    return poly


def validate_polygons(
    polygons: Iterable[Sequence[Tuple[float, float]]], tol: float = 1e-9
) -> Tuple[bool, str]:
    """
    Validate a collection of polygons.

    Parameters
    ----------
    polygons
        Iterable of vertex sequences. Each sequence is converted to a Shapely
        polygon, cleaned, and checked.
    tol
        Absolute area tolerance for the union-area consistency check.

    Returns
    -------
    (ok, msg)
        ok  : True  → all tests passed
              False → first test that failed
        msg : Diagnostic message
    """
    cleaned = []
    try:
        for coords in polygons:
            cleaned.append(_clean_polygon(coords))
    except ValueError as exc:
        return False, str(exc)

    union = unary_union(cleaned)
    if not isinstance(union, (Polygon, MultiPolygon)):
        return False, "Union result is not polygonal"

    area_sum = sum(p.area for p in cleaned)
    if abs(union.area - area_sum) > tol:
        return False, "Overlap or gaps detected"

    return True, "Geometry validated"
