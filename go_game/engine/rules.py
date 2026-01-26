"""
Rules engine for Go.

Handles move validation, captures, ko detection, and suicide rules.
This module is pure logic with no UI dependency.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import FrozenSet, Optional, Set

from .board import Board, Point, Stone


# ---------------------------------------------------------------------------
# Ko type / Move result enums
# ---------------------------------------------------------------------------

class KoRule(Enum):
    SIMPLE = auto()
    POSITIONAL_SUPERKO = auto()


class MoveResult(Enum):
    OK = auto()
    OCCUPIED = auto()
    KO = auto()
    SUICIDE = auto()


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

@dataclass
class RuleSettings:
    """Per-game rule settings."""
    ko_rule: KoRule = KoRule.SIMPLE
    allow_suicide: bool = False


# ---------------------------------------------------------------------------
# Rules engine (stateless helpers)
# ---------------------------------------------------------------------------

class Rules:
    """
    Stateless helper that validates moves and applies them to a board copy.

    All public methods receive the data they need and return results without
    mutating the input board.
    """

    @staticmethod
    def apply_move(
        board: Board,
        row: int,
        col: int,
        color: Stone,
        settings: RuleSettings,
        ko_point: Optional[Point] = None,
        position_history: Optional[Set[int]] = None,
    ) -> tuple[MoveResult, Optional[Board], Optional[Point], FrozenSet[Point]]:
        """
        Try to apply a move.

        Returns
        -------
        result : MoveResult
        new_board : Board or None (None if illegal)
        new_ko_point : Point or None
        captured : frozenset of captured points (empty if none)
        """
        # 1. Occupied?
        if board.get(row, col) != Stone.EMPTY:
            return MoveResult.OCCUPIED, None, None, frozenset()

        # 2. Place stone on a copy
        new_board = board.copy()
        new_board.set(row, col, color)

        # 3. Capture opponent groups with 0 liberties
        opponent = color.opponent()
        captured: set[Point] = set()
        for nr, nc in new_board.neighbors(row, col):
            if new_board.get(nr, nc) == opponent:
                grp, libs = new_board.get_group_and_liberties(nr, nc)
                if len(libs) == 0:
                    captured |= grp
                    new_board.remove_group(grp)

        captured_frozen = frozenset(captured)

        # 4. Check suicide
        _, own_libs = new_board.get_group_and_liberties(row, col)
        if len(own_libs) == 0 and len(captured) == 0:
            if not settings.allow_suicide:
                return MoveResult.SUICIDE, None, None, frozenset()
            # Suicide is allowed – remove own group
            own_group = new_board.get_group(row, col)
            new_board.remove_group(own_group)
            # Captured stones in suicide = own group
            captured_frozen = frozenset(own_group)

        # 5. Ko check
        new_ko: Optional[Point] = None

        if settings.ko_rule == KoRule.SIMPLE:
            # Simple ko: if exactly one stone captured and move is single
            # stone, the recapture point is ko-banned next turn.
            if len(captured) == 1:
                cap_pt = next(iter(captured))
                # Check if the capturing stone is alone (group size 1) and
                # has exactly 0 liberties if opponent replays there.
                grp_now = new_board.get_group(row, col)
                _, libs_now = new_board.get_group_and_liberties(row, col)
                if len(grp_now) == 1 and len(libs_now) == 1:
                    new_ko = cap_pt

            if ko_point is not None and (row, col) == ko_point:
                return MoveResult.KO, None, None, frozenset()

        elif settings.ko_rule == KoRule.POSITIONAL_SUPERKO:
            if position_history is not None:
                h = new_board.position_hash()
                if h in position_history:
                    return MoveResult.KO, None, None, frozenset()

        return MoveResult.OK, new_board, new_ko, captured_frozen

    @staticmethod
    def has_legal_move(
        board: Board,
        color: Stone,
        settings: RuleSettings,
        ko_point: Optional[Point] = None,
        position_history: Optional[Set[int]] = None,
    ) -> bool:
        """Return True if *color* has at least one legal move."""
        for r, c in board.empty_points():
            result, *_ = Rules.apply_move(
                board, r, c, color, settings, ko_point, position_history
            )
            if result == MoveResult.OK:
                return True
        return False
