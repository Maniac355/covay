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

BOARD_BG = QColor(220, 179, 92)          # warm wood
BOARD_BG_LIGHT = QColor(235, 200, 120)   # lighter wood for gradient
GRID_COLOR = QColor(60, 40, 20)          # dark brown grid lines
HOSHI_COLOR = QColor(60, 40, 20)

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

PANEL_BG = QColor(45, 45, 50)
PANEL_TEXT = QColor(230, 230, 230)
PANEL_ACCENT = QColor(100, 180, 255)

# ---------------------------------------------------------------------------
# Menu / setup colours
# ---------------------------------------------------------------------------

MENU_BG_DARK = QColor(28, 28, 35)
MENU_BG_MID = QColor(38, 38, 48)
MENU_ACCENT = QColor(200, 165, 80)        # gold
MENU_ACCENT_HOVER = QColor(230, 195, 100)
MENU_TEXT = QColor(230, 230, 230)
MENU_TEXT_DIM = QColor(150, 150, 160)
MENU_CARD_BG = QColor(48, 48, 58)
MENU_CARD_BORDER = QColor(70, 70, 85)
MENU_CARD_SELECTED = QColor(200, 165, 80)

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
    background-color: #1c1c23;
}
QWidget#central {
    background-color: #1c1c23;
}
QLabel {
    color: #e6e6e6;
    font-family: "Segoe UI";
    font-size: 12px;
    background: transparent;
}
QPushButton {
    background-color: #3a3a42;
    color: #e6e6e6;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 6px 14px;
    font-family: "Segoe UI";
    font-size: 12px;
    min-width: 70px;
}
QPushButton:hover {
    background-color: #4a4a55;
    border-color: #77a;
}
QPushButton:pressed {
    background-color: #555566;
}
QPushButton:disabled {
    background-color: #2a2a30;
    color: #666;
    border-color: #444;
}
QListWidget {
    background-color: #35353c;
    color: #e6e6e6;
    border: 1px solid #555;
    border-radius: 4px;
    font-family: "Consolas";
    font-size: 11px;
}
QListWidget::item:selected {
    background-color: #4a5a7a;
}
QGroupBox {
    color: #e6e6e6;
    border: 1px solid #555;
    border-radius: 4px;
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
    background-color: #3a3a42;
    color: #e6e6e6;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 4px 8px;
    font-family: "Segoe UI";
    font-size: 12px;
}
QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    border-color: #77a;
}
QComboBox QAbstractItemView {
    background-color: #3a3a42;
    color: #e6e6e6;
    selection-background-color: #4a5a7a;
    border: 1px solid #555;
}
QCheckBox {
    color: #e6e6e6;
    font-family: "Segoe UI";
    font-size: 12px;
    spacing: 6px;
}
QDialog {
    background-color: #2d2d32;
}
QStatusBar {
    background-color: #18181e;
    color: #aaa;
    font-size: 11px;
}
QScrollArea {
    border: none;
    background: transparent;
}
QScrollBar:vertical {
    background: #2a2a32;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #555;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #777;
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
        bg="#c8a550", fg="#1c1c23", border="#c8a550",
        font_size=15,
        hover_bg="#dab860", hover_border="#e6cc80",
        pressed_bg="#b09040",
    )


def menu_button_outline() -> str:
    return MENU_BUTTON_STYLE.format(
        bg="transparent", fg="#e6e6e6", border="#666",
        font_size=14,
        hover_bg="#35354040", hover_border="#c8a550",
        pressed_bg="#45455050",
    )


def menu_button_danger() -> str:
    return MENU_BUTTON_STYLE.format(
        bg="transparent", fg="#cc6666", border="#663333",
        font_size=14,
        hover_bg="#33222240", hover_border="#cc6666",
        pressed_bg="#44333350",
    )


CARD_STYLE_NORMAL = """
    background-color: #303038;
    border: 2px solid #50505a;
    border-radius: 10px;
"""

CARD_STYLE_SELECTED = """
    background-color: #3a3530;
    border: 2px solid #c8a550;
    border-radius: 10px;
"""

SETUP_START_BUTTON = """
QPushButton {
    background-color: #c8a550;
    color: #1c1c23;
    border: none;
    border-radius: 8px;
    padding: 14px 48px;
    font-family: "Segoe UI";
    font-size: 16px;
    font-weight: bold;
    min-width: 200px;
}
QPushButton:hover {
    background-color: #dab860;
}
QPushButton:pressed {
    background-color: #b09040;
}
"""

SETUP_BACK_BUTTON = """
QPushButton {
    background-color: transparent;
    color: #aaa;
    border: 1px solid #555;
    border-radius: 6px;
    padding: 8px 24px;
    font-family: "Segoe UI";
    font-size: 13px;
    min-width: 100px;
}
QPushButton:hover {
    color: #e6e6e6;
    border-color: #888;
    background-color: #ffffff10;
}
"""
