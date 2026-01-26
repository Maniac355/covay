"""
Move history and undo/redo support.

Stores complete game snapshots so that undo/redo is exact.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .board import Board, Point, Stone


# ---------------------------------------------------------------------------
# Move record
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MoveRecord:
    """One entry in the game history."""
    color: Stone
    point: Optional[Point]          # None = pass
    captured: frozenset[Point]      # stones captured by this move
    move_number: int

    def coordinate_str(self, board_size: int) -> str:
        """Human-readable coordinate like 'B D4' or 'W Pass'."""
        color_char = "B" if self.color == Stone.BLACK else "W"
        if self.point is None:
            return f"{color_char} Pass"
        row, col = self.point
        col_letter = chr(ord('A') + col + (1 if col >= 8 else 0))  # skip 'I'
        row_number = board_size - row
        return f"{color_char} {col_letter}{row_number}"


# ---------------------------------------------------------------------------
# Snapshot for undo/redo
# ---------------------------------------------------------------------------

@dataclass
class GameSnapshot:
    """Complete snapshot of the game state at one point in time."""
    board: Board
    current_turn: Stone
    captures_black: int
    captures_white: int
    ko_point: Optional[Point]
    position_hashes: set[int]
    consecutive_passes: int
    move: Optional[MoveRecord]      # the move that led to this state


# ---------------------------------------------------------------------------
# History manager
# ---------------------------------------------------------------------------

class History:
    """
    Manages the ordered list of game snapshots for undo/redo.

    `_snapshots[0]` is always the initial (empty-board) state.
    `_cursor` points to the current state index.
    """

    def __init__(self) -> None:
        self._snapshots: list[GameSnapshot] = []
        self._cursor: int = -1

    def push(self, snapshot: GameSnapshot) -> None:
        """Record a new state, discarding any redo history."""
        self._cursor += 1
        # Discard future snapshots
        self._snapshots = self._snapshots[: self._cursor]
        self._snapshots.append(snapshot)

    def can_undo(self) -> bool:
        return self._cursor > 0

    def can_redo(self) -> bool:
        return self._cursor < len(self._snapshots) - 1

    def undo(self) -> Optional[GameSnapshot]:
        if not self.can_undo():
            return None
        self._cursor -= 1
        return self._snapshots[self._cursor]

    def redo(self) -> Optional[GameSnapshot]:
        if not self.can_redo():
            return None
        self._cursor += 1
        return self._snapshots[self._cursor]

    @property
    def current(self) -> Optional[GameSnapshot]:
        if 0 <= self._cursor < len(self._snapshots):
            return self._snapshots[self._cursor]
        return None

    @property
    def move_list(self) -> list[MoveRecord]:
        """Return the list of moves up to the current cursor (excluding initial)."""
        moves: list[MoveRecord] = []
        for i in range(1, self._cursor + 1):
            snap = self._snapshots[i]
            if snap.move is not None:
                moves.append(snap.move)
        return moves

    @property
    def all_snapshots(self) -> list[GameSnapshot]:
        return self._snapshots[: self._cursor + 1]

    def clear(self) -> None:
        self._snapshots.clear()
        self._cursor = -1
