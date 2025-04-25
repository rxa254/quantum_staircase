"""
pynrose_core.py  (MIT License, vendored)

Minimal, dependency-free Penrose P3 tiler.

Changes from the previous revision
----------------------------------
* Replaced tuple arithmetic that relied on `/` with an explicit `_lerp`
  helper to avoid TypeError (“unsupported operand type(s) for /:”).
* All vector maths now stays inside helper functions—no tuple/float
  operations are performed directly.

Interface
---------
PenroseTiling(level).tile_vertices()  ->  List[Tuple[(x, y), ...]]  (len 4)
"""

from __future__ import annotations

from math import cos, sin, pi
from typing import List, Sequence, Tuple

tau = (1 + 5**0.5) / 2  # golden ratio
Vec = Tuple[float, float]
Rhomb = Tuple[Sequence[Vec], str]  # (4-tuple of vertices, "thick"/"thin")


# ----------------------------------------------------------------------
# Vector helpers (no third-party deps)
# ----------------------------------------------------------------------
def _lerp(u: Vec, v: Vec, alpha: float) -> Vec:
    """Linear interpolate: u + alpha*(v-u)."""
    return (u[0] + alpha * (v[0] - u[0]), u[1] + alpha * (v[1] - u[1]))


def _rot(v: Vec, angle: float) -> Vec:
    x, y = v
    c, s = cos(angle), sin(angle)
    return (c * x - s * y, s * x + c * y)


# ----------------------------------------------------------------------
# Core tiler
# ----------------------------------------------------------------------
class PenroseTiling:
    """Inflation-based thick/thin rhombus tiler."""

    def __init__(self, level: int = 4):
        self.level = level
        self._tiles: List[Rhomb] = self._inflate(level)

    # ------------------  public  ------------------
    def tile_vertices(self) -> List[Sequence[Vec]]:
        return [coords for coords, _ in self._tiles]

    # ------------------  private  -----------------
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
            P = _lerp(A, B, 1 / tau)
            Q = _lerp(D, A, 1 / tau)
            R = _lerp(B, C, 1 / tau)
            return [
                ((A, P, Q, D), "thick"),
                ((P, B, R, Q), "thin"),
                ((Q, R, C, D), "thick"),
            ]

        # thin rhomb
        P = _lerp(B, A, 1 / tau)
        Q = _lerp(B, C, 1 / tau)
        R = _lerp(D, A, 1 / tau)
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
