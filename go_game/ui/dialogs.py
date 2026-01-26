"""
Dialogs for the Go game – New Game, Settings, Score Result.
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from ..engine.rules import KoRule
from ..engine.state import DEFAULT_KOMI, GameConfig, Ruleset
from . import theme


# ---------------------------------------------------------------------------
# New Game Dialog
# ---------------------------------------------------------------------------

class NewGameDialog(QDialog):
    """Dialog for starting a new game with chosen settings."""

    def __init__(self, current_config: Optional[GameConfig] = None, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("New Game")
        self.setMinimumWidth(340)
        self._config = current_config or GameConfig()
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        # Board size
        group_board = QGroupBox("Board")
        form_board = QFormLayout(group_board)
        self._size_combo = QComboBox()
        self._size_combo.addItems(["9 × 9", "13 × 13", "19 × 19"])
        size_map = {9: 0, 13: 1, 19: 2}
        self._size_combo.setCurrentIndex(size_map.get(self._config.board_size, 2))
        self._size_combo.currentIndexChanged.connect(self._on_size_changed)
        form_board.addRow("Board Size:", self._size_combo)
        layout.addWidget(group_board)

        # Rules
        group_rules = QGroupBox("Rules")
        form_rules = QFormLayout(group_rules)

        self._ruleset_combo = QComboBox()
        self._ruleset_combo.addItems(["Japanese (Territory)", "Chinese (Area)"])
        self._ruleset_combo.setCurrentIndex(0 if self._config.ruleset == Ruleset.JAPANESE else 1)
        form_rules.addRow("Ruleset:", self._ruleset_combo)

        self._komi_spin = QDoubleSpinBox()
        self._komi_spin.setRange(0.0, 99.5)
        self._komi_spin.setSingleStep(0.5)
        self._komi_spin.setDecimals(1)
        self._komi_spin.setValue(self._config.komi)
        form_rules.addRow("Komi:", self._komi_spin)

        self._ko_combo = QComboBox()
        self._ko_combo.addItems(["Simple Ko", "Positional Superko"])
        self._ko_combo.setCurrentIndex(0 if self._config.ko_rule == KoRule.SIMPLE else 1)
        form_rules.addRow("Ko Rule:", self._ko_combo)

        self._suicide_check = QCheckBox("Allow suicide moves")
        self._suicide_check.setChecked(self._config.allow_suicide)
        form_rules.addRow(self._suicide_check)

        layout.addWidget(group_rules)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _on_size_changed(self, index: int) -> None:
        sizes = [9, 13, 19]
        size = sizes[index]
        self._komi_spin.setValue(DEFAULT_KOMI.get(size, 6.5))

    def get_config(self) -> GameConfig:
        sizes = [9, 13, 19]
        size = sizes[self._size_combo.currentIndex()]
        ruleset = Ruleset.JAPANESE if self._ruleset_combo.currentIndex() == 0 else Ruleset.CHINESE
        ko_rule = KoRule.SIMPLE if self._ko_combo.currentIndex() == 0 else KoRule.POSITIONAL_SUPERKO
        return GameConfig(
            board_size=size,
            ruleset=ruleset,
            komi=self._komi_spin.value(),
            ko_rule=ko_rule,
            allow_suicide=self._suicide_check.isChecked(),
        )


# ---------------------------------------------------------------------------
# Settings Dialog (same fields but for mid-game display / reference)
# ---------------------------------------------------------------------------

class SettingsDialog(QDialog):
    """Shows current settings (read-only during a game)."""

    def __init__(self, config: GameConfig, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Game Settings")
        self.setMinimumWidth(300)
        self._config = config
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        form = QFormLayout()
        form.addRow("Board Size:", QLabel(f"{self._config.board_size} × {self._config.board_size}"))
        form.addRow("Ruleset:", QLabel(
            "Japanese (Territory)" if self._config.ruleset == Ruleset.JAPANESE else "Chinese (Area)"
        ))
        form.addRow("Komi:", QLabel(str(self._config.komi)))
        form.addRow("Ko Rule:", QLabel(
            "Simple Ko" if self._config.ko_rule == KoRule.SIMPLE else "Positional Superko"
        ))
        form.addRow("Allow Suicide:", QLabel("Yes" if self._config.allow_suicide else "No"))
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)


# ---------------------------------------------------------------------------
# Score Result Dialog
# ---------------------------------------------------------------------------

class ScoreDialog(QDialog):
    """Displays the final score breakdown."""

    def __init__(self, score: dict, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Game Result")
        self.setMinimumWidth(360)
        self._score = score
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        ruleset = self._score.get("ruleset", "")
        reason = self._score.get("reason", "")
        winner = self._score.get("winner", "?")
        margin = self._score.get("margin", 0)

        # Winner banner
        if reason == "Resignation":
            banner = f"{winner} wins by Resignation"
        elif winner == "Tie":
            banner = "Game is a Tie (Jigo)"
        else:
            banner = f"{winner} wins by {margin:.1f} points"

        lbl_banner = QLabel(banner)
        lbl_banner.setFont(theme.font_bold(16))
        lbl_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_banner)

        layout.addSpacing(10)

        # Details
        lbl_ruleset = QLabel(f"Ruleset: {ruleset}")
        lbl_ruleset.setFont(theme.font_normal(11))
        layout.addWidget(lbl_ruleset)

        layout.addSpacing(6)

        # Black breakdown
        b = self._score.get("black", {})
        layout.addWidget(QLabel(self._format_side("Black", b)))

        # White breakdown
        w = self._score.get("white", {})
        layout.addWidget(QLabel(self._format_side("White", w)))

        layout.addSpacing(10)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

    @staticmethod
    def _format_side(name: str, data: dict) -> str:
        parts = [f"  {name}:"]
        for key, val in data.items():
            if key == "total":
                continue
            parts.append(f"    {key.capitalize()}: {val}")
        total = data.get("total", "?")
        parts.append(f"    Total: {total}")
        return "\n".join(parts)


# ---------------------------------------------------------------------------
# Confirm dialog helper
# ---------------------------------------------------------------------------

def confirm_action(parent: QWidget, title: str, message: str) -> bool:
    reply = QMessageBox.question(
        parent, title, message,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No,
    )
    return reply == QMessageBox.StandardButton.Yes


# ---------------------------------------------------------------------------
# Invalid move notification
# ---------------------------------------------------------------------------

def show_invalid_move(parent: QWidget, reason: str) -> None:
    """Show a brief warning about an illegal move."""
    QMessageBox.warning(parent, "Invalid Move", reason)
