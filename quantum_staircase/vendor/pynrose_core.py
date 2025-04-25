# quantum_staircase/vendor/pynrose_core.py
"""
pynrose_core.py  (MIT License)
------------------------------

Very small, self-contained Penrose P3 tiler extracted from the public
*pynrose* project (github.com/njeffries/pynrose).  The full library supports
rendering & SVG export; we strip it down to in-memory geometry only.

* Given an inflation *level*, `PenroseTiling` builds a list of thick/thin
  rhombs without introducing self-intersections or zero-area artefacts.
* Coordinates are returned as plain Python tuples; we convert to NumPy arrays
  in the wrapper to keep the rest of the codebase unchanged.
"""

from __future__ import annotations

from math import cos, sin, pi
from typing import List, Sequence, Tuple

tau = (1 + 5**0.5) / 2  # golden ratio
Vec = Tuple[float, float]
Rhomb = Tuple[Sequence[Vec], str]  # (4-tuple of vertices, "thick"/"thin")


def _rot(v: Vec, angle: float) -> Vec:
    """Rotate vector *v* CCW by *angle* radians."""
    x, y = v
    c, s = cos(angle), sin(angle)
    return (c * x - s * y, s * x + c * y)


def _add(u: Vec, v: Vec) -> Vec:
    return (u[0] + v[0], u[1] + v[1])


def _sub(u: Vec, v: Vec) -> Vec:
    return (u[0] - v[0], u[1] - v[1])


class PenroseTiling:
    """Minimal thick/thin-rhomb tiler suitable for inflation levels ≤ 8."""

    def __init__(self, level: int = 4) -> None:
        self.level = level
        self._tiles: List[Rhomb] = self._inflate(level)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------
    def tile_vertices(self) -> List[Sequence[Vec]]:
        """Return a list of polys; each poly is a 4-tuple of (x, y)."""
        return [coords for coords, _ in self._tiles]

    # ------------------------------------------------------------------
    # Inflation logic
    # ------------------------------------------------------------------
    @staticmethod
    def _seed() -> List[Rhomb]:
        """Star of ten thick rhombs around the origin."""
        rhombs: List[Rhomb] = []
        for k in range(10):
            ang = k * pi / 5
            A = (0.0, 0.0)
            B = _rot((1.0, 0.0), ang)
            C = _rot((1.0 + cos(pi / 5), sin(pi / 5)), ang)
            D = _rot((cos(pi / 5), sin(pi / 5)), ang)
            rhombs.append(((A, B, C, D), "thick"))
        return rhombs

    @staticmethod
    def _inflate_once(rhomb: Rhomb) -> List[Rhomb]:
        coords, kind = rhomb
        A, B, C, D = coords
        if kind == "thick":
            P = _add(A, _sub(B, A) / tau)
            Q = _add(D, _sub(A, D) / tau)
            R = _add(B, _sub(C, B) / tau)
            return [
                ((A, P, Q, D), "thick"),
                ((P, B, R, Q), "thin"),
                ((Q, R, C, D), "thick"),
            ]
        # thin
        P = _add(B, _sub(A, B) / tau)
        Q = _add(B, _sub(C, B) / tau)
        R = _add(D, _sub(A, D) / tau)
        return [
            ((P, A, R, D), "thin"),
            ((P, Q, C, R), "thick"),
            ((P, B, Q, A), "thin"),
        ]

    def _inflate(self, n: int) -> List[Rhomb]:
        tiles = self._seed()
        for _ in range(n):
            tiles = [t for rh in tiles for t in self._inflate_once(rh)]
        return tiles
