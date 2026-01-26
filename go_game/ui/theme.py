"""
Visual theme constants for the Go game UI.

All colours, sizes, and style parameters are centralised here so that the
look-and-feel can be adjusted in one place.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QLinearGradient


# ---------------------------------------------------------------------------
# Board colours
# ---------------------------------------------------------------------------

BOARD_BG = QColor(230, 196, 120)          # warm wood
BOARD_BG_LIGHT = QColor(244, 222, 170)   # lighter wood for gradient
GRID_COLOR = QColor(80, 55, 30)          # softened brown grid lines
HOSHI_COLOR = QColor(80, 55, 30)

# ---------------------------------------------------------------------------
# Stone colours
# ---------------------------------------------------------------------------

BLACK_STONE = QColor(20, 20, 20)
BLACK_STONE_HIGHLIGHT = QColor(60, 60, 60)
WHITE_STONE = QColor(245, 245, 240)
WHITE_STONE_HIGHLIGHT = QColor(255, 255, 255)

# Shadow
STONE_SHADOW = QColor(0, 0, 0, 60)
STONE_SHADOW_OFFSET = 2  # pixels

# ---------------------------------------------------------------------------
# Ghost (hover preview)
# ---------------------------------------------------------------------------

GHOST_OPACITY = 0.45  # 40-60 %

# ---------------------------------------------------------------------------
# Last move marker
# ---------------------------------------------------------------------------

LAST_MOVE_MARKER_BLACK = QColor(200, 200, 200)  # light dot on black stone
LAST_MOVE_MARKER_WHITE = QColor(40, 40, 40)      # dark dot on white stone

# ---------------------------------------------------------------------------
# Scoring mode overlay
# ---------------------------------------------------------------------------

DEAD_STONE_OVERLAY = QColor(255, 0, 0, 120)   # translucent red
TERRITORY_BLACK = QColor(0, 0, 0, 80)
TERRITORY_WHITE = QColor(255, 255, 255, 80)

# ---------------------------------------------------------------------------
# Info panel
# ---------------------------------------------------------------------------

PANEL_BG = QColor(245, 247, 252)
PANEL_TEXT = QColor(45, 50, 60)
PANEL_ACCENT = QColor(90, 140, 220)

# ---------------------------------------------------------------------------
# Menu / setup colours
# ---------------------------------------------------------------------------

MENU_BG_DARK = QColor(245, 247, 252)
MENU_BG_MID = QColor(232, 237, 246)
MENU_ACCENT = QColor(170, 130, 60)        # warm accent
MENU_ACCENT_HOVER = QColor(190, 150, 80)
MENU_TEXT = QColor(50, 55, 65)
MENU_TEXT_DIM = QColor(110, 120, 135)
MENU_CARD_BG = QColor(255, 255, 255)
MENU_CARD_BORDER = QColor(210, 218, 230)
MENU_CARD_SELECTED = QColor(180, 140, 70)

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------

def font_normal(size: int = 12) -> QFont:
    f = QFont("Segoe UI", size)
    f.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
    return f


def font_bold(size: int = 12) -> QFont:
    f = font_normal(size)
    f.setBold(True)
    return f


def font_mono(size: int = 11) -> QFont:
    f = QFont("Consolas", size)
    return f


def font_title(size: int = 36) -> QFont:
    f = QFont("Georgia", size)
    f.setBold(True)
    return f


# ---------------------------------------------------------------------------
# Board gradient helper
# ---------------------------------------------------------------------------

def board_gradient(width: float, height: float) -> QLinearGradient:
    """Create a warm wood gradient for the board background."""
    grad = QLinearGradient(0, 0, width, height)
    grad.setColorAt(0.0, BOARD_BG_LIGHT)
    grad.setColorAt(0.5, BOARD_BG)
    grad.setColorAt(1.0, BOARD_BG_LIGHT)
    return grad


# ---------------------------------------------------------------------------
# Style sheet for the application
# ---------------------------------------------------------------------------

APP_STYLESHEET = """
QMainWindow {
    background-color: #f4f6fb;
}
QWidget#central {
    background-color: #f4f6fb;
}
QLabel {
    color: #2f3440;
    font-family: "Segoe UI";
    font-size: 12px;
    background: transparent;
}
QPushButton {
    background-color: #ffffff;
    color: #2f3440;
    border: 1px solid #d6dbe6;
    border-radius: 8px;
    padding: 7px 16px;
    font-family: "Segoe UI";
    font-size: 12px;
    min-width: 70px;
}
QPushButton:hover {
    background-color: #eef1f8;
    border-color: #bfc8d8;
}
QPushButton:pressed {
    background-color: #e2e7f1;
}
QPushButton:disabled {
    background-color: #f1f3f8;
    color: #9aa3b2;
    border-color: #e0e4ee;
}
QListWidget {
    background-color: #ffffff;
    color: #2f3440;
    border: 1px solid #d6dbe6;
    border-radius: 8px;
    font-family: "Consolas";
    font-size: 11px;
}
QListWidget::item:selected {
    background-color: #e4ecfb;
}
QGroupBox {
    color: #2f3440;
    border: 1px solid #d6dbe6;
    border-radius: 10px;
    margin-top: 8px;
    padding-top: 12px;
    font-family: "Segoe UI";
    font-size: 12px;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
}
QComboBox, QSpinBox, QDoubleSpinBox {
    background-color: #ffffff;
    color: #2f3440;
    border: 1px solid #d6dbe6;
    border-radius: 8px;
    padding: 4px 8px;
    font-family: "Segoe UI";
    font-size: 12px;
}
QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    border-color: #bfc8d8;
}
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #2f3440;
    selection-background-color: #e4ecfb;
    border: 1px solid #d6dbe6;
}
QCheckBox {
    color: #2f3440;
    font-family: "Segoe UI";
    font-size: 12px;
    spacing: 6px;
}
QDialog {
    background-color: #f8f9fc;
}
QStatusBar {
    background-color: #eef1f7;
    color: #6b7485;
    font-size: 11px;
}
QScrollArea {
    border: none;
    background: transparent;
}
QScrollBar:vertical {
    background: #edf0f6;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #c9d2e2;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #b7c1d4;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

# ---------------------------------------------------------------------------
# Menu-specific button styles
# ---------------------------------------------------------------------------

MENU_BUTTON_STYLE = """
QPushButton {{
    background-color: {bg};
    color: {fg};
    border: 2px solid {border};
    border-radius: 8px;
    padding: 14px 32px;
    font-family: "Segoe UI";
    font-size: {font_size}px;
    font-weight: bold;
    min-width: 220px;
}}
QPushButton:hover {{
    background-color: {hover_bg};
    border-color: {hover_border};
}}
QPushButton:pressed {{
    background-color: {pressed_bg};
}}
"""


def menu_button_gold() -> str:
    return MENU_BUTTON_STYLE.format(
        bg="#e9d7b5", fg="#503a1f", border="#e0cca3",
        font_size=15,
        hover_bg="#f2e3c9", hover_border="#d4be94",
        pressed_bg="#dcc8a2",
    )


def menu_button_outline() -> str:
    return MENU_BUTTON_STYLE.format(
        bg="#ffffff", fg="#39404d", border="#d6dbe6",
        font_size=14,
        hover_bg="#edf1f7", hover_border="#c9d2e2",
        pressed_bg="#e2e7f1",
    )


def menu_button_danger() -> str:
    return MENU_BUTTON_STYLE.format(
        bg="#fff5f5", fg="#b45555", border="#e8c9c9",
        font_size=14,
        hover_bg="#ffe6e6", hover_border="#d9a5a5",
        pressed_bg="#f5dada",
    )


CARD_STYLE_NORMAL = """
    background-color: #ffffff;
    border: 2px solid #d6dbe6;
    border-radius: 12px;
"""

CARD_STYLE_SELECTED = """
    background-color: #f6efe3;
    border: 2px solid #d9c09a;
    border-radius: 12px;
"""

SETUP_START_BUTTON = """
QPushButton {
    background-color: #e9d7b5;
    color: #503a1f;
    border: none;
    border-radius: 10px;
    padding: 14px 48px;
    font-family: "Segoe UI";
    font-size: 16px;
    font-weight: bold;
    min-width: 200px;
}
QPushButton:hover {
    background-color: #f2e3c9;
}
QPushButton:pressed {
    background-color: #dcc8a2;
}
"""

SETUP_BACK_BUTTON = """
QPushButton {
    background-color: #ffffff;
    color: #6b7485;
    border: 1px solid #d6dbe6;
    border-radius: 8px;
    padding: 8px 24px;
    font-family: "Segoe UI";
    font-size: 13px;
    min-width: 100px;
}
QPushButton:hover {
    color: #3a4150;
    border-color: #c6cddb;
    background-color: #f2f4f9;
}
"""
