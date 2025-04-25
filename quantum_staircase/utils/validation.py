"""
quantum_staircase.utils.validation  – relaxed version

Rules enforced
--------------
1.  No overlaps: if total-overlap area > *tol* the check fails.
2.  Gaps / whitespace are **allowed** (this is decorative wallpaper).
3.  Polygons that collapse to near-zero area are silently discarded.
"""

from __future__ import annotations

from typing import Iterable, Sequence, Tuple

from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union


def _clean(coords: Sequence[Tuple[float, float]], min_area: float):
    """Return a valid Shapely polygon, or None if it’s empty/tiny."""
    poly = Polygon(coords).buffer(0)
    if poly.is_empty or poly.area < min_area:
        return None
    return poly


def validate_polygons(
    polygons: Iterable[Sequence[Tuple[float, float]]],
    tol: float = 1e-8,
    min_area: float = 1e-10,
):
    cleaned = []
    for coords in polygons:
        poly = _clean(coords, min_area)
        if poly is not None:
            cleaned.append(poly)

    if not cleaned:
        return False, "No valid polygons remain after cleaning"

    union = unary_union(cleaned)
    if not isinstance(union, (Polygon, MultiPolygon)):
        return False, "Union result is not polygonal"

    sum_area = sum(p.area for p in cleaned)
    overlap_area = sum_area - union.area  # gaps OK; overlaps shrink union.area

    if overlap_area > tol:
        return False, f"Overlap area {overlap_area:.3e} exceeds tolerance"
    return True, "Geometry validated"
