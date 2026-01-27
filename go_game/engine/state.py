"""
Game state management.

`GameState` is the central object that ties Board, Rules, and History
together.  The UI interacts exclusively with this object.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional

from .board import Board, Point, Stone
from .history import GameSnapshot, History, MoveRecord
from .rules import KoRule, MoveResult, RuleSettings, Rules


# ---------------------------------------------------------------------------
# Ruleset (scoring flavour)
# ---------------------------------------------------------------------------

class Ruleset(Enum):
    JAPANESE = auto()
    CHINESE = auto()


# ---------------------------------------------------------------------------
# Default komi per board size
# ---------------------------------------------------------------------------

DEFAULT_KOMI: dict[int, float] = {
    9: 3.5,
    13: 5.5,
    19: 6.5,
}


# ---------------------------------------------------------------------------
# Game phase
# ---------------------------------------------------------------------------

class GamePhase(Enum):
    PLAYING = auto()
    SCORING = auto()
    FINISHED = auto()


# ---------------------------------------------------------------------------
# Game configuration
# ---------------------------------------------------------------------------

@dataclass
class GameConfig:
    board_size: int = 19
    ruleset: Ruleset = Ruleset.JAPANESE
    komi: float = 6.5
    ko_rule: KoRule = KoRule.SIMPLE
    allow_suicide: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "board_size": self.board_size,
            "ruleset": self.ruleset.name,
            "komi": self.komi,
            "ko_rule": self.ko_rule.name,
            "allow_suicide": self.allow_suicide,
        }

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "GameConfig":
        return GameConfig(
            board_size=d.get("board_size", 19),
            ruleset=Ruleset[d.get("ruleset", Ruleset.JAPANESE.name)],
            komi=d.get("komi", 6.5),
            ko_rule=KoRule[d.get("ko_rule", KoRule.SIMPLE.name)],
            allow_suicide=d.get("allow_suicide", False),
        )


# ---------------------------------------------------------------------------
# Game state
# ---------------------------------------------------------------------------

class GameState:
    """
    High-level game state.  Provides the public API that the UI consumes.
    """

    def __init__(self, config: Optional[GameConfig] = None) -> None:
        self.config = config or GameConfig()
        self.board = Board(self.config.board_size)
        self.current_turn: Stone = Stone.BLACK
        self.captures: dict[Stone, int] = {Stone.BLACK: 0, Stone.WHITE: 0}
        self.ko_point: Optional[Point] = None
        self.position_hashes: set[int] = {self.board.position_hash()}
        self.consecutive_passes: int = 0
        self.phase: GamePhase = GamePhase.PLAYING
        self.move_number: int = 0

        # Dead-stone mask for scoring mode (set of points marked dead)
        self.dead_stones: set[Point] = set()

        # Winner / score results (set after scoring)
        self.final_score: Optional[dict[str, Any]] = None

        # History
        self.history = History()
        self._rule_settings = RuleSettings(
            ko_rule=self.config.ko_rule,
            allow_suicide=self.config.allow_suicide,
        )
        # Push initial state
        self._push_snapshot(move=None)

    # -- snapshot helpers ---------------------------------------------------

    def _make_snapshot(self, move: Optional[MoveRecord]) -> GameSnapshot:
        return GameSnapshot(
            board=self.board.copy(),
            current_turn=self.current_turn,
            captures_black=self.captures[Stone.BLACK],
            captures_white=self.captures[Stone.WHITE],
            ko_point=self.ko_point,
            position_hashes=set(self.position_hashes),
            consecutive_passes=self.consecutive_passes,
            move=move,
        )

    def _push_snapshot(self, move: Optional[MoveRecord]) -> None:
        self.history.push(self._make_snapshot(move))

    def _restore_snapshot(self, snap: GameSnapshot) -> None:
        self.board = snap.board.copy()
        self.current_turn = snap.current_turn
        self.captures[Stone.BLACK] = snap.captures_black
        self.captures[Stone.WHITE] = snap.captures_white
        self.ko_point = snap.ko_point
        self.position_hashes = set(snap.position_hashes)
        self.consecutive_passes = snap.consecutive_passes

    # -- public API: play ---------------------------------------------------

    def play(self, row: int, col: int) -> MoveResult:
        """
        Attempt to place a stone at (row, col) for the current player.
        Returns the MoveResult.
        """
        if self.phase != GamePhase.PLAYING:
            return MoveResult.OCCUPIED  # can't play in scoring/finished

        result, new_board, new_ko, captured = Rules.apply_move(
            self.board,
            row,
            col,
            self.current_turn,
            self._rule_settings,
            self.ko_point,
            self.position_hashes if self.config.ko_rule == KoRule.POSITIONAL_SUPERKO else None,
        )

        if result != MoveResult.OK:
            return result

        assert new_board is not None

        # Apply
        self.move_number += 1
        move_record = MoveRecord(
            color=self.current_turn,
            point=(row, col),
            captured=captured,
            move_number=self.move_number,
        )
        self.captures[self.current_turn] += len(captured)
        self.board = new_board
        self.ko_point = new_ko
        self.position_hashes.add(self.board.position_hash())
        self.consecutive_passes = 0
        self.current_turn = self.current_turn.opponent()

        self._push_snapshot(move_record)
        return MoveResult.OK

    # -- public API: pass ---------------------------------------------------

    def pass_turn(self) -> None:
        """Current player passes."""
        if self.phase != GamePhase.PLAYING:
            return

        self.move_number += 1
        move_record = MoveRecord(
            color=self.current_turn,
            point=None,
            captured=frozenset(),
            move_number=self.move_number,
        )
        self.consecutive_passes += 1
        self.ko_point = None
        self.current_turn = self.current_turn.opponent()
        self._push_snapshot(move_record)

        if self.consecutive_passes >= 2:
            self.phase = GamePhase.SCORING

    # -- public API: resign -------------------------------------------------

    def resign(self) -> Stone:
        """Current player resigns.  Returns the winner."""
        winner = self.current_turn.opponent()
        self.phase = GamePhase.FINISHED
        self.final_score = {
            "winner": "Black" if winner == Stone.BLACK else "White",
            "reason": "Resignation",
        }
        return winner

    # -- public API: undo / redo --------------------------------------------

    def undo(self) -> bool:
        if self.phase == GamePhase.FINISHED:
            return False
        snap = self.history.undo()
        if snap is None:
            return False
        self._restore_snapshot(snap)
        self.phase = GamePhase.PLAYING
        self.dead_stones.clear()
        # Adjust move_number
        self.move_number = max(0, self.move_number - 1)
        return True

    def redo(self) -> bool:
        if self.phase == GamePhase.FINISHED:
            return False
        snap = self.history.redo()
        if snap is None:
            return False
        self._restore_snapshot(snap)
        self.move_number += 1
        return True

    # -- scoring mode -------------------------------------------------------

    def toggle_dead_group(self, row: int, col: int) -> None:
        """Toggle the dead/alive status of the group at (row, col)."""
        if self.phase != GamePhase.SCORING:
            return
        stone = self.board.get(row, col)
        if stone == Stone.EMPTY:
            return
        group = self.board.get_group(row, col)
        # Toggle: if any stone of the group is already dead, mark all alive;
        # otherwise mark all dead.
        if group & self.dead_stones:
            self.dead_stones -= group
        else:
            self.dead_stones |= group

    def confirm_score(self) -> dict[str, Any]:
        """Finalize scoring and set phase to FINISHED."""
        from .scoring import compute_score_chinese, compute_score_japanese

        dead_mask = self.dead_stones
        if self.config.ruleset == Ruleset.JAPANESE:
            result = compute_score_japanese(self, dead_mask, self.config.komi)
        else:
            result = compute_score_chinese(self, dead_mask, self.config.komi)

        self.final_score = result
        self.phase = GamePhase.FINISHED
        return result

    # -- move list (for display) --------------------------------------------

    @property
    def move_list(self) -> list[MoveRecord]:
        return self.history.move_list

    # -- serialization (save / load) ----------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Serialize the game state to a JSON-compatible dict."""
        grid: list[list[int]] = []
        for r in range(self.board.size):
            row_data: list[int] = []
            for c in range(self.board.size):
                row_data.append(int(self.board.get(r, c)))
            grid.append(row_data)

        moves: list[dict[str, Any]] = []
        for m in self.move_list:
            moves.append({
                "color": int(m.color),
                "point": list(m.point) if m.point else None,
                "captured": [list(p) for p in m.captured],
                "move_number": m.move_number,
            })

        return {
            "config": self.config.to_dict(),
            "grid": grid,
            "current_turn": int(self.current_turn),
            "captures_black": self.captures[Stone.BLACK],
            "captures_white": self.captures[Stone.WHITE],
            "ko_point": list(self.ko_point) if self.ko_point else None,
            "consecutive_passes": self.consecutive_passes,
            "move_number": self.move_number,
            "phase": self.phase.name,
            "dead_stones": [list(p) for p in sorted(self.dead_stones)],
            "final_score": self.final_score,
            "moves": moves,
        }

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "GameState":
        """Reconstruct a GameState from a dict (as returned by to_dict)."""
        config = GameConfig.from_dict(d.get("config", {}))
        state = GameState(config)
        moves = d.get("moves", [])
        if moves:
            # Replay moves
            for m in moves:
                color = Stone(m["color"])
                # Ensure it's the right turn
                if state.current_turn != color:
                    state.current_turn = color
                if m["point"] is None:
                    state.pass_turn()
                else:
                    row, col = m["point"]
                    result = state.play(row, col)
                    if result != MoveResult.OK:
                        # Fallback: force-place (shouldn't happen with valid saves)
                        state.board.set(row, col, color)
                        state.current_turn = color.opponent()
                        state.move_number += 1
        elif "grid" in d:
            grid = d["grid"]
            size = len(grid)
            state.board = Board(size)
            for r, row in enumerate(grid):
                for c, val in enumerate(row):
                    state.board.set(r, c, Stone(val))
            state.position_hashes = {state.board.position_hash()}
            state.history.clear()
            state._push_snapshot(move=None)
        if "captures_black" in d:
            state.captures[Stone.BLACK] = d["captures_black"]
        if "captures_white" in d:
            state.captures[Stone.WHITE] = d["captures_white"]
        if "ko_point" in d:
            state.ko_point = tuple(d["ko_point"]) if d["ko_point"] else None
        if "current_turn" in d:
            state.current_turn = Stone(d["current_turn"])
        state.consecutive_passes = d.get("consecutive_passes", state.consecutive_passes)
        state.move_number = d.get("move_number", state.move_number)
        if "phase" in d:
            try:
                state.phase = GamePhase[d["phase"]]
            except KeyError:
                pass
        dead_stones = d.get("dead_stones", [])
        state.dead_stones = {tuple(p) for p in dead_stones}
        if "final_score" in d:
            state.final_score = d["final_score"]
        return state

    def save_json(self, filepath: str) -> None:
        """Save game state to a JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @staticmethod
    def load_json(filepath: str) -> "GameState":
        """Load game state from a JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            d = json.load(f)
        return GameState.from_dict(d)
