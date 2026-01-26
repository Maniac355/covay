"""
Scoring for Go – Japanese (Territory) and Chinese (Area) rules.

Both functions accept:
    state      – a GameState (provides board, captures, etc.)
    dead_mask  – set of Points that have been marked as dead stones
    komi       – the komi value (compensation for White)

Both return a ScoreBreakdown dict with detailed information.
"""

from __future__ import annotations

from typing import Any, Set

from .board import Board, Point, Stone


# ---------------------------------------------------------------------------
# Helper: build a "clean" board with dead stones removed
# ---------------------------------------------------------------------------

def _board_without_dead(board: Board, dead_mask: Set[Point]) -> Board:
    """Return a copy of the board with dead stones removed."""
    clean = board.copy()
    for r, c in dead_mask:
        clean.set(r, c, Stone.EMPTY)
    return clean


def _count_stones(board: Board, color: Stone) -> int:
    """Count stones of a given color on the board."""
    count = 0
    for r in range(board.size):
        for c in range(board.size):
            if board.get(r, c) == color:
                count += 1
    return count


def _count_dead_by_color(
    board: Board, dead_mask: Set[Point]
) -> dict[Stone, int]:
    """Count dead stones per color."""
    counts: dict[Stone, int] = {Stone.BLACK: 0, Stone.WHITE: 0}
    for r, c in dead_mask:
        color = board.get(r, c)
        if color in counts:
            counts[color] += 1
    return counts


# ---------------------------------------------------------------------------
# Japanese scoring (Territory)
# ---------------------------------------------------------------------------

def compute_score_japanese(
    state: Any,  # GameState – avoid circular import
    dead_mask: Set[Point],
    komi: float,
) -> dict[str, Any]:
    """
    Japanese rules scoring.

    Score = Territory + Captures + Dead opponent stones + Komi (for White)

    Territory is counted on the board *after* removing dead stones.
    Dead stones of color X are added to the opponent's capture count.
    """
    board: Board = state.board
    clean = _board_without_dead(board, dead_mask)
    territory = clean.get_territory()

    dead_counts = _count_dead_by_color(board, dead_mask)

    black_territory = len(territory[Stone.BLACK])
    white_territory = len(territory[Stone.WHITE])

    black_captures = state.captures[Stone.BLACK] + dead_counts[Stone.WHITE]
    white_captures = state.captures[Stone.WHITE] + dead_counts[Stone.BLACK]

    black_score = black_territory + black_captures
    white_score = white_territory + white_captures + komi

    if black_score > white_score:
        winner = "Black"
    elif white_score > black_score:
        winner = "White"
    else:
        winner = "Tie"

    return {
        "ruleset": "Japanese",
        "black": {
            "territory": black_territory,
            "captures": black_captures,
            "total": black_score,
        },
        "white": {
            "territory": white_territory,
            "captures": white_captures,
            "komi": komi,
            "total": white_score,
        },
        "winner": winner,
        "margin": abs(black_score - white_score),
        "reason": "Score",
    }


# ---------------------------------------------------------------------------
# Chinese scoring (Area)
# ---------------------------------------------------------------------------

def compute_score_chinese(
    state: Any,  # GameState
    dead_mask: Set[Point],
    komi: float,
) -> dict[str, Any]:
    """
    Chinese rules scoring.

    Score = Stones on board + Territory + Komi (for White)

    Counted on the board *after* removing dead stones.
    Dead stones of one color are effectively counted for the opponent's
    territory (since the clean board shows those as empty, and if surrounded
    by one color they become that color's territory).
    """
    board: Board = state.board
    clean = _board_without_dead(board, dead_mask)
    territory = clean.get_territory()

    black_stones = _count_stones(clean, Stone.BLACK)
    white_stones = _count_stones(clean, Stone.WHITE)

    black_territory = len(territory[Stone.BLACK])
    white_territory = len(territory[Stone.WHITE])

    black_score = float(black_stones + black_territory)
    white_score = float(white_stones + white_territory) + komi

    if black_score > white_score:
        winner = "Black"
    elif white_score > black_score:
        winner = "White"
    else:
        winner = "Tie"

    return {
        "ruleset": "Chinese",
        "black": {
            "stones": black_stones,
            "territory": black_territory,
            "total": black_score,
        },
        "white": {
            "stones": white_stones,
            "territory": white_territory,
            "komi": komi,
            "total": white_score,
        },
        "winner": winner,
        "margin": abs(black_score - white_score),
        "reason": "Score",
    }
