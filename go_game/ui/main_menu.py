"""
Main menu screen – the first screen the user sees.

Features a decorative Go-themed background painted with QPainter,
title, subtitle, and navigation buttons.
"""

from __future__ import annotations

import math
import random
from typing import Optional

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import (
    QBrush,
    QColor,
    QLinearGradient,
    QPainter,
    QPen,
    QRadialGradient,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from . import theme


class MainMenuScreen(QWidget):
    """Main menu with decorative background and navigation buttons."""

    # Navigation signals
    new_game_clicked = Signal()
    load_game_clicked = Signal()
    tutorial_clicked = Signal()
    quit_clicked = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("mainMenu")
        # Pre-generate decorative stone positions for the background
        self._deco_stones = self._generate_deco_stones()
        self._build_ui()

    def _generate_deco_stones(self) -> list[dict]:
        """Generate random decorative stones for the background."""
        rng = random.Random(42)  # deterministic for consistency
        stones = []
        for _ in range(35):
            stones.append({
                "x": rng.uniform(0.0, 1.0),
                "y": rng.uniform(0.0, 1.0),
                "r": rng.uniform(0.012, 0.035),
                "black": rng.choice([True, False]),
                "alpha": rng.uniform(0.04, 0.12),
            })
        return stones

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Spacer top
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Centre column
        center = QVBoxLayout()
        center.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        center.setSpacing(18)

        # Buttons
        self._btn_new = QPushButton("Ván mới")
        self._btn_new.setStyleSheet(theme.menu_button_gold())
        self._btn_new.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_new.clicked.connect(self.new_game_clicked)

        self._btn_load = QPushButton("Tải ván")
        self._btn_load.setStyleSheet(theme.menu_button_outline())
        self._btn_load.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_load.clicked.connect(self.load_game_clicked)

        self._btn_tutorial = QPushButton("Hướng dẫn chơi")
        self._btn_tutorial.setStyleSheet(theme.menu_button_outline())
        self._btn_tutorial.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_tutorial.clicked.connect(self.tutorial_clicked)

        self._btn_quit = QPushButton("Thoát")
        self._btn_quit.setStyleSheet(theme.menu_button_danger())
        self._btn_quit.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_quit.clicked.connect(self.quit_clicked)

        for btn in [self._btn_new, self._btn_load, self._btn_tutorial, self._btn_quit]:
            center.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addLayout(center)

        # Spacer bottom
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    # -- painting (decorative background) -----------------------------------

    def paintEvent(self, event) -> None:  # type: ignore[override]
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        w, h = self.width(), self.height()

        # Background gradient
        grad = QLinearGradient(0, 0, w, h)
        grad.setColorAt(0.0, QColor(246, 248, 252))
        grad.setColorAt(0.5, QColor(233, 238, 247))
        grad.setColorAt(1.0, QColor(246, 248, 252))
        p.fillRect(self.rect(), grad)

        # Decorative grid lines (subtle)
        p.setPen(QPen(QColor(120, 130, 150, 25), 1))
        spacing = 40
        for i in range(0, max(w, h) + spacing, spacing):
            if i < w:
                p.drawLine(i, 0, i, h)
            if i < h:
                p.drawLine(0, i, w, i)

        # Decorative stones
        for s in self._deco_stones:
            cx = s["x"] * w
            cy = s["y"] * h
            r = s["r"] * min(w, h)
            alpha = int(s["alpha"] * 255)

            if s["black"]:
                color = QColor(80, 80, 90, alpha)
            else:
                color = QColor(240, 240, 235, alpha)

            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(color))
            p.drawEllipse(QPointF(cx, cy), r, r)

        # Title
        title_font = theme.font_title(42)
        p.setFont(title_font)
        p.setPen(QPen(theme.MENU_ACCENT))
        title_rect = QRectF(0, h * 0.12, w, 60)
        p.drawText(title_rect, Qt.AlignmentFlag.AlignCenter, "Cờ Vây")

        # Subtitle
        sub_font = theme.font_normal(16)
        p.setFont(sub_font)
        p.setPen(QPen(theme.MENU_TEXT_DIM))
        sub_rect = QRectF(0, h * 0.12 + 55, w, 30)
        p.drawText(sub_rect, Qt.AlignmentFlag.AlignCenter, "Trò chơi chiến thuật cổ xưa")

        # Version / footer
        footer_font = theme.font_normal(10)
        p.setFont(footer_font)
        p.setPen(QPen(QColor(120, 130, 145)))
        footer_rect = QRectF(0, h - 30, w, 20)
        p.drawText(footer_rect, Qt.AlignmentFlag.AlignCenter, "Cờ Vây  ·  Weiqi  ·  Baduk")

        p.end()
