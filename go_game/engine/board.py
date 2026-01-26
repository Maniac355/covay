"""
Board representation for the Go game.

Handles the grid, stone placement, group detection, and liberty counting.
Uses integer constants for cell states: EMPTY=0, BLACK=1, WHITE=2.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from enum import IntEnum
from typing import FrozenSet, Iterator, Set, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

class Stone(IntEnum):
    """Cell state on the board."""
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def opponent(self) -> "Stone":
        if self == Stone.BLACK:
            return Stone.WHITE
        if self == Stone.WHITE:
            return Stone.BLACK
        return Stone.EMPTY


Point = Tuple[int, int]  # (row, col), 0-indexed


# ---------------------------------------------------------------------------
# Hoshi (star point) positions
# ---------------------------------------------------------------------------

HOSHI_POSITIONS: dict[int, list[Point]] = {
    9: [
        (2, 2), (2, 6),
        (4, 4),
        (6, 2), (6, 6),
    ],
    13: [
        (3, 3), (3, 6), (3, 9),
        (6, 3), (6, 6), (6, 9),
        (9, 3), (9, 6), (9, 9),
    ],
    19: [
        (3, 3), (3, 9), (3, 15),
        (9, 3), (9, 9), (9, 15),
        (15, 3), (15, 9), (15, 15),
    ],
}


# ---------------------------------------------------------------------------
# Board
# ---------------------------------------------------------------------------

class Board:
    """
    Low-level board representation.

    Stores the grid as a flat list (row-major).  Provides helpers for
    neighbour lookup, group (connected-component) detection and liberty
    counting.
    """

    __slots__ = ("size", "_grid")

    def __init__(self, size: int = 19) -> None:
        assert size in (9, 13, 19), f"Unsupported board size: {size}"
        self.size: int = size
        self._grid: list[int] = [Stone.EMPTY] * (size * size)

    # -- copy ---------------------------------------------------------------

    def copy(self) -> "Board":
        b = Board.__new__(Board)
        b.size = self.size
        b._grid = self._grid[:]
        return b

    # -- index helpers ------------------------------------------------------

    def _idx(self, row: int, col: int) -> int:
        return row * self.size + col

    def on_board(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size

    # -- get / set ----------------------------------------------------------

    def get(self, row: int, col: int) -> Stone:
        return Stone(self._grid[self._idx(row, col)])

    def set(self, row: int, col: int, stone: Stone) -> None:
        self._grid[self._idx(row, col)] = int(stone)

    # -- neighbours ---------------------------------------------------------

    def neighbors(self, row: int, col: int) -> Iterator[Point]:
        """Yield orthogonally adjacent points that are on the board."""
        if row > 0:
            yield (row - 1, col)
        if row < self.size - 1:
            yield (row + 1, col)
        if col > 0:
            yield (row, col - 1)
        if col < self.size - 1:
            yield (row, col + 1)

    # -- group (connected component) ----------------------------------------

    def get_group(self, row: int, col: int) -> FrozenSet[Point]:
        """Return all points connected to (row, col) with the same colour."""
        color = self.get(row, col)
        if color == Stone.EMPTY:
            return frozenset()
        visited: Set[Point] = set()
        stack: list[Point] = [(row, col)]
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            if self.get(r, c) != color:
                continue
            visited.add((r, c))
            for nr, nc in self.neighbors(r, c):
                if (nr, nc) not in visited:
                    stack.append((nr, nc))
        return frozenset(visited)

    def get_group_and_liberties(
        self, row: int, col: int
    ) -> tuple[FrozenSet[Point], FrozenSet[Point]]:
        """Return (group, liberties) for the stone at (row, col)."""
        color = self.get(row, col)
        if color == Stone.EMPTY:
            return frozenset(), frozenset()
        group: Set[Point] = set()
        liberties: Set[Point] = set()
        stack: list[Point] = [(row, col)]
        while stack:
            r, c = stack.pop()
            if (r, c) in group:
                continue
            if self.get(r, c) != color:
                continue
            group.add((r, c))
            for nr, nc in self.neighbors(r, c):
                cell = self.get(nr, nc)
                if cell == Stone.EMPTY:
                    liberties.add((nr, nc))
                elif cell == color and (nr, nc) not in group:
                    stack.append((nr, nc))
        return frozenset(group), frozenset(liberties)

    def liberties(self, row: int, col: int) -> int:
        """Return the number of liberties for the group at (row, col)."""
        _, libs = self.get_group_and_liberties(row, col)
        return len(libs)

    # -- remove group -------------------------------------------------------

    def remove_group(self, group: FrozenSet[Point]) -> None:
        """Remove all stones in *group* from the board."""
        for r, c in group:
            self.set(r, c, Stone.EMPTY)

    # -- hash for superko ---------------------------------------------------

    def position_hash(self) -> int:
        """Zobrist-style hash of the full board position."""
        return hash(tuple(self._grid))

    # -- empty points -------------------------------------------------------

    def empty_points(self) -> Iterator[Point]:
        for r in range(self.size):
            for c in range(self.size):
                if self.get(r, c) == Stone.EMPTY:
                    yield (r, c)

    # -- all groups ---------------------------------------------------------

    def all_groups(self) -> list[tuple[Stone, FrozenSet[Point]]]:
        """Return a list of (color, group) for every group on the board."""
        visited: Set[Point] = set()
        groups: list[tuple[Stone, FrozenSet[Point]]] = []
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) in visited:
                    continue
                color = self.get(r, c)
                if color == Stone.EMPTY:
                    continue
                grp = self.get_group(r, c)
                visited |= grp
                groups.append((color, grp))
        return groups

    # -- territory detection ------------------------------------------------

    def get_territory(
        self,
    ) -> dict[Stone, set[Point]]:
        """
        Flood-fill empty regions.  A region belongs to a colour if it is
        bordered **only** by that colour (or the edge).  Neutral regions
        (bordered by both) belong to EMPTY.
        """
        visited: Set[Point] = set()
        territory: dict[Stone, set[Point]] = {
            Stone.BLACK: set(),
            Stone.WHITE: set(),
            Stone.EMPTY: set(),
        }
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) in visited or self.get(r, c) != Stone.EMPTY:
                    continue
                region: set[Point] = set()
                borders: set[Stone] = set()
                stack: list[Point] = [(r, c)]
                while stack:
                    pr, pc = stack.pop()
                    if (pr, pc) in region:
                        continue
                    cell = self.get(pr, pc)
                    if cell != Stone.EMPTY:
                        borders.add(cell)
                        continue
                    region.add((pr, pc))
                    for nr, nc in self.neighbors(pr, pc):
                        if (nr, nc) not in region:
                            stack.append((nr, nc))
                visited |= region
                if borders == {Stone.BLACK}:
                    territory[Stone.BLACK] |= region
                elif borders == {Stone.WHITE}:
                    territory[Stone.WHITE] |= region
                else:
                    territory[Stone.EMPTY] |= region
        return territory

    # -- hoshi positions for this board size --------------------------------

    def hoshi_points(self) -> list[Point]:
        return HOSHI_POSITIONS.get(self.size, [])

    # -- string representation (for debugging) ------------------------------

    def __str__(self) -> str:
        symbols = {Stone.EMPTY: ".", Stone.BLACK: "X", Stone.WHITE: "O"}
        rows: list[str] = []
        for r in range(self.size):
            row = " ".join(symbols[self.get(r, c)] for c in range(self.size))
            rows.append(f"{r:2d} {row}")
        header = "   " + " ".join(f"{c}" for c in range(self.size))
        return header + "\n" + "\n".join(rows)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return NotImplemented
        return self.size == other.size and self._grid == other._grid

    def __hash__(self) -> int:
        return self.position_hash()
