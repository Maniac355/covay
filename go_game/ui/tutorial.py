"""
Tutorial / How-to-Play screen.

A scrollable guide explaining Go rules, capturing, ko, and scoring
for both Japanese and Chinese rulesets.
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QLinearGradient, QPainter
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from . import theme


# ---------------------------------------------------------------------------
# Section widget
# ---------------------------------------------------------------------------

class _Section(QFrame):
    """A styled section card for the tutorial."""

    def __init__(
        self,
        title: str,
        body: str,
        accent_color: str = "#c8a550",
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            "QFrame { background-color: #2a2a34; border-radius: 10px; }"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        lbl_title = QLabel(title)
        lbl_title.setFont(theme.font_bold(15))
        lbl_title.setStyleSheet(f"color: {accent_color};")
        layout.addWidget(lbl_title)

        lbl_body = QLabel(body)
        lbl_body.setFont(theme.font_normal(12))
        lbl_body.setWordWrap(True)
        lbl_body.setStyleSheet("color: #ccc; line-height: 1.5;")
        lbl_body.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(lbl_body)


# ---------------------------------------------------------------------------
# Diagram widget (text-based board illustration)
# ---------------------------------------------------------------------------

class _Diagram(QFrame):
    """A monospaced diagram block."""

    def __init__(self, text: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            "QFrame { background-color: #1e1e26; border-radius: 8px; }"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)

        lbl = QLabel(text)
        lbl.setFont(theme.font_mono(11))
        lbl.setStyleSheet("color: #b0b080;")
        layout.addWidget(lbl)


# ---------------------------------------------------------------------------
# Tutorial Screen
# ---------------------------------------------------------------------------

class TutorialScreen(QWidget):
    """Scrollable how-to-play guide."""

    back_clicked = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # Header bar
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet("background-color: #22222a;")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(20, 0, 20, 0)

        self._btn_back = QPushButton("Back to Menu")
        self._btn_back.setStyleSheet(theme.SETUP_BACK_BUTTON)
        self._btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_back.clicked.connect(self.back_clicked)
        h_layout.addWidget(self._btn_back)

        lbl_title = QLabel("How to Play Go")
        lbl_title.setFont(theme.font_bold(18))
        lbl_title.setStyleSheet("color: #c8a550;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_layout.addWidget(lbl_title, stretch=1)

        # balance spacer
        spacer = QWidget()
        spacer.setFixedWidth(120)
        h_layout.addWidget(spacer)

        outer.addWidget(header)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(60, 30, 60, 40)
        content_layout.setSpacing(20)

        # -- Sections --

        content_layout.addWidget(_Section(
            "What is Go?",
            "Go (also called <b>Cờ Vây</b>, Weiqi, or Baduk) is a strategic board game "
            "for two players. It originated in China over 4,000 years ago and is one of "
            "the oldest games still played today.<br><br>"
            "The goal is simple: <b>control more territory</b> than your opponent by "
            "placing stones on the intersections of a grid.",
        ))

        content_layout.addWidget(_Section(
            "Basic Rules",
            "<b>1. The Board:</b> Go is played on a grid of intersections. Standard sizes "
            "are 9×9 (beginner), 13×13 (intermediate), and 19×19 (standard).<br><br>"
            "<b>2. Stones:</b> Black plays first. Players alternate placing one stone per "
            "turn on an empty intersection.<br><br>"
            "<b>3. Liberties:</b> Each stone (or connected group of stones) has "
            "<i>liberties</i> — the empty intersections directly adjacent to it "
            "(up, down, left, right). A stone in the center has 4 liberties; on the edge, 3; "
            "in the corner, 2.<br><br>"
            "<b>4. Once placed, stones never move.</b> They can only be removed by capture.",
            "#66aaff",
        ))

        content_layout.addWidget(_Diagram(
            "  Liberties example:\n\n"
            "    . . . . .        . = empty\n"
            "    . . L . .        X = Black stone\n"
            "    . L X L .        L = liberty of X\n"
            "    . . L . .\n"
            "    . . . . .\n\n"
            "  This single stone has 4 liberties."
        ))

        content_layout.addWidget(_Section(
            "Capturing Stones",
            "When a stone or connected group of same-colour stones has <b>zero liberties</b>, "
            "it is <b>captured</b> and removed from the board.<br><br>"
            "You capture opponent stones by filling their last liberty. "
            "Captures happen immediately when you place your stone.<br><br>"
            "<b>Important:</b> If your move simultaneously removes the last liberty of an "
            "opponent group AND your own group, the opponent's stones are captured first, "
            "which may give your group liberties. This is NOT suicide — it is a legal capture.",
            "#ff8866",
        ))

        content_layout.addWidget(_Diagram(
            "  Capture example:\n\n"
            "    Before:          After Black plays A:\n"
            "    . X . .          . X . .\n"
            "    X O A .    →     X . X .\n"
            "    . X . .          . X . .\n\n"
            "  O = White stone with one liberty at A.\n"
            "  Black plays A → White captured and removed."
        ))

        content_layout.addWidget(_Section(
            "Ko Rule",
            "A <b>ko</b> situation occurs when a single stone is captured and the opponent "
            "could immediately recapture, creating an infinite loop.<br><br>"
            "<b>Simple Ko:</b> You cannot immediately recapture the stone that was just taken. "
            "You must play elsewhere first (a 'ko threat'), then you may recapture on your "
            "next turn.<br><br>"
            "<b>Positional Superko:</b> A stricter rule that prevents ANY board position from "
            "repeating. This handles complex ko situations as well.",
            "#cc88ff",
        ))

        content_layout.addWidget(_Diagram(
            "  Ko example:\n\n"
            "    . X O .          . X O .\n"
            "    X O . O    →     X . X O     Black captures O\n"
            "    . X O .          . X O .     at (1,1)\n\n"
            "  White CANNOT immediately play back at the\n"
            "  captured position. Must play elsewhere first."
        ))

        content_layout.addWidget(_Section(
            "Suicide",
            "A <b>suicide move</b> is one where your stone (or group) would have zero "
            "liberties after placement, without capturing any opponent stones.<br><br>"
            "By default, suicide is <b>forbidden</b> (you cannot make such a move). "
            "Some rulesets allow it — you can toggle this in game settings.",
            "#ff6699",
        ))

        content_layout.addWidget(_Section(
            "Passing and End of Game",
            "You may <b>pass</b> your turn instead of placing a stone. "
            "When both players pass consecutively, the game enters "
            "<b>Scoring Mode</b>.<br><br>"
            "In Scoring Mode, players agree on which stones are 'dead' (will inevitably "
            "be captured). Click on stone groups to mark them as dead/alive. Then confirm "
            "to calculate the final score.",
            "#66ccaa",
        ))

        content_layout.addWidget(_Section(
            "Scoring: Japanese Rules (Territory)",
            "Under Japanese rules, your score consists of:<br><br>"
            "<table style='color:#ccc;'>"
            "<tr><td style='padding-right:20px;'><b>Territory</b></td>"
            "<td>Empty intersections surrounded <i>only</i> by your stones</td></tr>"
            "<tr><td><b>+ Captures</b></td>"
            "<td>Number of opponent stones you captured during the game</td></tr>"
            "<tr><td><b>+ Dead stones</b></td>"
            "<td>Opponent's dead stones (agreed upon in scoring) count as captures</td></tr>"
            "<tr><td><b>+ Komi</b></td>"
            "<td>White receives komi (compensation for going second)</td></tr>"
            "</table><br>"
            "<b>Default komi:</b> 19×19 → 6.5 · 13×13 → 5.5 · 9×9 → 3.5<br><br>"
            "The half-point (0.5) in komi ensures there is no tie.",
            "#ffbb44",
        ))

        content_layout.addWidget(_Diagram(
            "  Japanese scoring example (9x9):\n\n"
            "  Komi = 3.5 (for White)\n\n"
            "  Black: 20 territory + 4 captures      = 24.0\n"
            "  White: 18 territory + 2 captures + 3.5 = 23.5\n\n"
            "  → Black wins by 0.5 points"
        ))

        content_layout.addWidget(_Section(
            "Scoring: Chinese Rules (Area)",
            "Under Chinese rules, your score consists of:<br><br>"
            "<table style='color:#ccc;'>"
            "<tr><td style='padding-right:20px;'><b>Stones on board</b></td>"
            "<td>Number of your stones remaining on the board</td></tr>"
            "<tr><td><b>+ Territory</b></td>"
            "<td>Empty intersections surrounded only by your stones</td></tr>"
            "<tr><td><b>+ Komi</b></td>"
            "<td>White receives komi</td></tr>"
            "</table><br>"
            "Note: Captures are NOT counted separately in Chinese rules, because captured "
            "stones reduce the opponent's stones on the board.",
            "#44bbff",
        ))

        content_layout.addWidget(_Diagram(
            "  Chinese scoring example (9x9):\n\n"
            "  Komi = 3.5 (for White)\n\n"
            "  Black: 30 stones + 10 territory      = 40.0\n"
            "  White: 25 stones + 12 territory + 3.5 = 40.5\n\n"
            "  → White wins by 0.5 points"
        ))

        content_layout.addWidget(_Section(
            "Japanese vs Chinese: When Does It Matter?",
            "In most normal games, both scoring methods give the <b>same winner</b>. "
            "The difference arises in edge cases:<br><br>"
            "• In Japanese rules, you lose a point for each stone you place in your own "
            "territory (filling dame / defensive moves). In Chinese rules, you don't.<br>"
            "• Chinese rules encourage filling dame (neutral points), since your stones on "
            "the board count toward your score.<br>"
            "• Chinese rules are simpler to verify and less dispute-prone.<br>"
            "• Japanese rules are traditional in professional play in Japan and Korea.",
            "#aabb66",
        ))

        content_layout.addWidget(_Section(
            "Tips for Beginners",
            "• <b>Start with 9×9</b> to learn the basics before moving to 19×19.<br>"
            "• <b>Don't try to capture everything.</b> Focus on building territory.<br>"
            "• <b>Connect your stones</b> to form strong groups.<br>"
            "• <b>Keep your groups alive</b> — a group needs two 'eyes' (internal liberties) "
            "to be permanently safe.<br>"
            "• <b>Don't be afraid to pass.</b> If you can't find a useful move, pass.<br>"
            "• <b>Have fun!</b> Go is a journey — you'll improve with every game.",
            "#88ddaa",
        ))

        content_layout.addSpacing(30)

        scroll.setWidget(content)
        outer.addWidget(scroll)

    # -- background painting ------------------------------------------------

    def paintEvent(self, event) -> None:  # type: ignore[override]
        p = QPainter(self)
        w, h = self.width(), self.height()
        grad = QLinearGradient(0, 0, w, h)
        grad.setColorAt(0.0, QColor(24, 24, 32))
        grad.setColorAt(1.0, QColor(30, 30, 40))
        p.fillRect(self.rect(), grad)
        p.end()
