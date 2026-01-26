"""
Game screen – the main gameplay view.

Contains the board widget, info panel, move history, and action buttons.
This is shown after the user starts or loads a game.
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QLinearGradient, QPainter
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..engine.board import Stone
from ..engine.rules import MoveResult
from ..engine.state import GameConfig, GamePhase, GameState, Ruleset
from .board_widget import BoardWidget
from .dialogs import (
    NewGameDialog,
    ScoreDialog,
    SettingsDialog,
    confirm_action,
    show_invalid_move,
)
from . import theme


class GameScreen(QWidget):
    """The main gameplay screen with board, info, and controls."""

    # Signal to navigate back to main menu
    back_to_menu = Signal()
    # Signal to navigate to setup (new game)
    new_game_requested = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._game: Optional[GameState] = None
        self._build_ui()

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def start_game(self, config: GameConfig) -> None:
        """Start a new game with the given configuration."""
        self._game = GameState(config)
        self._board_widget.set_game(self._game)
        self._update_ui()

    def load_game(self, game: GameState) -> None:
        """Load an existing game state."""
        self._game = game
        self._board_widget.set_game(self._game)
        self._update_ui()

    @property
    def game(self) -> Optional[GameState]:
        return self._game

    # -----------------------------------------------------------------------
    # UI construction
    # -----------------------------------------------------------------------

    def _build_ui(self) -> None:
        root = QHBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(10)

        # Left: Board
        self._board_widget = BoardWidget()
        self._board_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self._board_widget.stone_placed.connect(self._on_stone_placed)
        self._board_widget.dead_toggled.connect(self._on_dead_toggled)
        root.addWidget(self._board_widget, stretch=3)

        # Right: info panel
        right = QVBoxLayout()
        right.setSpacing(8)

        # -- Back to menu button (top) --
        self._btn_menu = QPushButton("Main Menu")
        self._btn_menu.setStyleSheet(theme.SETUP_BACK_BUTTON)
        self._btn_menu.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_menu.clicked.connect(self._on_back_to_menu)
        right.addWidget(self._btn_menu)

        right.addSpacing(4)

        # -- Turn / status --
        self._lbl_turn = QLabel("Black to play")
        self._lbl_turn.setFont(theme.font_bold(14))
        self._lbl_turn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right.addWidget(self._lbl_turn)

        # -- Info group --
        info_group = QGroupBox("Game Info")
        info_layout = QVBoxLayout(info_group)
        self._lbl_captures_b = QLabel("Black captures: 0")
        self._lbl_captures_w = QLabel("White captures: 0")
        self._lbl_komi = QLabel("Komi: 6.5")
        self._lbl_ruleset = QLabel("Ruleset: Japanese")
        self._lbl_move_num = QLabel("Move: 0")
        for lbl in [
            self._lbl_captures_b,
            self._lbl_captures_w,
            self._lbl_komi,
            self._lbl_ruleset,
            self._lbl_move_num,
        ]:
            lbl.setFont(theme.font_normal(11))
            info_layout.addWidget(lbl)
        right.addWidget(info_group)

        # -- History list --
        history_group = QGroupBox("Move History")
        history_layout = QVBoxLayout(history_group)
        self._move_list = QListWidget()
        self._move_list.setFont(theme.font_mono(10))
        history_layout.addWidget(self._move_list)
        right.addWidget(history_group, stretch=1)

        # -- Toolbar buttons --
        btn_group = QGroupBox("Actions")
        btn_layout = QVBoxLayout(btn_group)

        row1 = QHBoxLayout()
        self._btn_new = QPushButton("New Game")
        self._btn_pass = QPushButton("Pass")
        self._btn_resign = QPushButton("Resign")
        row1.addWidget(self._btn_new)
        row1.addWidget(self._btn_pass)
        row1.addWidget(self._btn_resign)
        btn_layout.addLayout(row1)

        row2 = QHBoxLayout()
        self._btn_undo = QPushButton("Undo")
        self._btn_redo = QPushButton("Redo")
        self._btn_settings = QPushButton("Settings")
        row2.addWidget(self._btn_undo)
        row2.addWidget(self._btn_redo)
        row2.addWidget(self._btn_settings)
        btn_layout.addLayout(row2)

        row3 = QHBoxLayout()
        self._btn_save = QPushButton("Save")
        self._btn_load = QPushButton("Load")
        row3.addWidget(self._btn_save)
        row3.addWidget(self._btn_load)
        btn_layout.addLayout(row3)

        # Scoring mode buttons (hidden until scoring phase)
        self._btn_confirm_score = QPushButton("Confirm Score")
        self._btn_confirm_score.setVisible(False)
        self._btn_confirm_score.setStyleSheet(
            "QPushButton { background-color: #c8a550; color: #1c1c23; font-weight: bold; }"
            "QPushButton:hover { background-color: #dab860; }"
        )
        self._btn_resume_play = QPushButton("Resume Play")
        self._btn_resume_play.setVisible(False)
        row4 = QHBoxLayout()
        row4.addWidget(self._btn_confirm_score)
        row4.addWidget(self._btn_resume_play)
        btn_layout.addLayout(row4)

        right.addWidget(btn_group)

        root.addLayout(right, stretch=1)

        # Connections
        self._btn_new.clicked.connect(self._on_new_game)
        self._btn_pass.clicked.connect(self._on_pass)
        self._btn_resign.clicked.connect(self._on_resign)
        self._btn_undo.clicked.connect(self._on_undo)
        self._btn_redo.clicked.connect(self._on_redo)
        self._btn_settings.clicked.connect(self._on_settings)
        self._btn_save.clicked.connect(self._on_save)
        self._btn_load.clicked.connect(self._on_load)
        self._btn_confirm_score.clicked.connect(self._on_confirm_score)
        self._btn_resume_play.clicked.connect(self._on_resume_play)

    # -----------------------------------------------------------------------
    # UI update
    # -----------------------------------------------------------------------

    def _update_ui(self) -> None:
        g = self._game
        if g is None:
            return

        # Turn label
        if g.phase == GamePhase.PLAYING:
            color_name = "Black" if g.current_turn == Stone.BLACK else "White"
            self._lbl_turn.setText(f"{color_name} to play")
            if g.current_turn == Stone.BLACK:
                self._lbl_turn.setStyleSheet(
                    "color: #ddd; background-color: #333; border-radius: 6px; padding: 6px;"
                )
            else:
                self._lbl_turn.setStyleSheet(
                    "color: #333; background-color: #e8e8e0; border-radius: 6px; padding: 6px;"
                )
        elif g.phase == GamePhase.SCORING:
            self._lbl_turn.setText("Scoring Mode\nClick groups to mark dead stones")
            self._lbl_turn.setStyleSheet(
                "color: #ffaa44; background-color: #3a3020; border-radius: 6px; padding: 6px;"
            )
        elif g.phase == GamePhase.FINISHED:
            winner = g.final_score.get("winner", "?") if g.final_score else "?"
            reason = g.final_score.get("reason", "") if g.final_score else ""
            if reason == "Resignation":
                self._lbl_turn.setText(f"Game Over\n{winner} wins by resignation")
            else:
                margin = g.final_score.get("margin", 0) if g.final_score else 0
                self._lbl_turn.setText(f"Game Over\n{winner} wins by {margin:.1f}")
            self._lbl_turn.setStyleSheet(
                "color: #66ccff; background-color: #1a2a3a; border-radius: 6px; padding: 6px;"
            )

        # Info
        self._lbl_captures_b.setText(f"Black captures: {g.captures[Stone.BLACK]}")
        self._lbl_captures_w.setText(f"White captures: {g.captures[Stone.WHITE]}")
        self._lbl_komi.setText(f"Komi: {g.config.komi}")
        self._lbl_ruleset.setText(
            f"Ruleset: {'Japanese' if g.config.ruleset == Ruleset.JAPANESE else 'Chinese'}"
        )
        self._lbl_move_num.setText(f"Move: {g.move_number}")

        # Move history
        self._move_list.clear()
        for m in g.move_list:
            self._move_list.addItem(
                f"{m.move_number:3d}. {m.coordinate_str(g.board.size)}"
            )
        if self._move_list.count() > 0:
            self._move_list.scrollToBottom()

        # Button states
        playing = g.phase == GamePhase.PLAYING
        self._btn_pass.setEnabled(playing)
        self._btn_resign.setEnabled(playing)
        self._btn_undo.setEnabled(g.history.can_undo() and g.phase != GamePhase.FINISHED)
        self._btn_redo.setEnabled(g.history.can_redo() and g.phase != GamePhase.FINISHED)

        scoring = g.phase == GamePhase.SCORING
        self._btn_confirm_score.setVisible(scoring)
        self._btn_resume_play.setVisible(scoring)

        self._board_widget.refresh()

    # -----------------------------------------------------------------------
    # Slots
    # -----------------------------------------------------------------------

    def _on_stone_placed(self, row: int, col: int) -> None:
        if self._game is None:
            return
        result = self._game.play(row, col)
        if result == MoveResult.OK:
            self._update_ui()
        elif result == MoveResult.OCCUPIED:
            show_invalid_move(self, "That intersection is already occupied.")
        elif result == MoveResult.KO:
            show_invalid_move(self, "Illegal move: Ko violation.\nYou must play elsewhere first.")
        elif result == MoveResult.SUICIDE:
            show_invalid_move(self, "Illegal move: Suicide is not allowed.\nYour stone would have no liberties.")

    def _on_dead_toggled(self, row: int, col: int) -> None:
        if self._game is None:
            return
        self._game.toggle_dead_group(row, col)
        self._update_ui()

    def _on_new_game(self) -> None:
        if self._game and self._game.phase == GamePhase.PLAYING and self._game.move_number > 0:
            if not confirm_action(self, "New Game", "Current game will be lost. Continue?"):
                return
        self.new_game_requested.emit()

    def _on_back_to_menu(self) -> None:
        if self._game and self._game.phase == GamePhase.PLAYING and self._game.move_number > 0:
            if not confirm_action(self, "Leave Game", "Current game will be lost. Return to menu?"):
                return
        self.back_to_menu.emit()

    def _on_pass(self) -> None:
        if self._game is None:
            return
        self._game.pass_turn()
        self._update_ui()

    def _on_resign(self) -> None:
        if self._game is None:
            return
        color_name = "Black" if self._game.current_turn == Stone.BLACK else "White"
        if not confirm_action(self, "Resign", f"{color_name} resigns. Are you sure?"):
            return
        self._game.resign()
        self._update_ui()
        if self._game.final_score:
            ScoreDialog(self._game.final_score, self).exec()

    def _on_undo(self) -> None:
        if self._game and self._game.undo():
            self._update_ui()

    def _on_redo(self) -> None:
        if self._game and self._game.redo():
            self._update_ui()

    def _on_settings(self) -> None:
        if self._game:
            SettingsDialog(self._game.config, self).exec()

    def _on_save(self) -> None:
        if self._game is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Game", "", "Go Game (*.json);;All Files (*)"
        )
        if path:
            try:
                self._game.save_json(path)
            except Exception as e:
                show_invalid_move(self, f"Save failed: {e}")

    def _on_load(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Game", "", "Go Game (*.json);;All Files (*)"
        )
        if path:
            try:
                self._game = GameState.load_json(path)
                self._board_widget.set_game(self._game)
                self._update_ui()
            except Exception as e:
                show_invalid_move(self, f"Load failed: {e}")

    def _on_confirm_score(self) -> None:
        if self._game is None:
            return
        result = self._game.confirm_score()
        self._update_ui()
        ScoreDialog(result, self).exec()

    def _on_resume_play(self) -> None:
        if self._game is None:
            return
        self._game.phase = GamePhase.PLAYING
        self._game.consecutive_passes = 0
        self._game.dead_stones.clear()
        self._update_ui()

    # -- background painting ------------------------------------------------

    def paintEvent(self, event) -> None:  # type: ignore[override]
        p = QPainter(self)
        w, h = self.width(), self.height()
        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0.0, QColor(28, 28, 35))
        grad.setColorAt(1.0, QColor(24, 24, 30))
        p.fillRect(self.rect(), grad)
        p.end()
