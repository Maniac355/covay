"""
Visual theme constants for the Go game UI.

All colours, sizes, and style parameters are centralised here so that the
look-and-feel can be adjusted in one place.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QLinearGradient


# ---------------------------------------------------------------------------
# Spacing / layout
# ---------------------------------------------------------------------------

BASE_PADDING = 16
SECTION_SPACING = 24
ITEM_SPACING = 16
GROUPBOX_MARGIN = 12
GROUPBOX_SPACING = 8
TIGHT_SPACING = 8

PAGE_MARGIN = (40, 30, 40, 30)
CONTENT_MARGIN = (60, 30, 60, 40)
HEADER_HEIGHT = 60

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

PANEL_BG = QColor(42, 48, 60)
PANEL_TEXT = QColor(220, 225, 235)
PANEL_ACCENT = QColor(120, 165, 230)

# ---------------------------------------------------------------------------
# Menu / setup colours
# ---------------------------------------------------------------------------

MENU_BG_DARK = QColor(36, 40, 50)
MENU_BG_MID = QColor(44, 50, 62)
MENU_ACCENT = QColor(200, 160, 90)        # warm accent
MENU_ACCENT_HOVER = QColor(220, 180, 110)
MENU_TEXT = QColor(225, 230, 238)
MENU_TEXT_DIM = QColor(165, 175, 190)
MENU_CARD_BG = QColor(32, 36, 46)
MENU_CARD_BORDER = QColor(70, 78, 95)
MENU_CARD_SELECTED = QColor(210, 170, 100)
HEADER_BG = QColor(32, 36, 46)

# Background gradients
BACKGROUND_GRADIENT_START = QColor(28, 32, 40)
BACKGROUND_GRADIENT_MID = QColor(36, 42, 54)
BACKGROUND_GRADIENT_END = QColor(28, 32, 40)

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
QMainWindow {{
    background-color: #1f242c;
}}
QWidget#central {{
    background-color: #1f242c;
}}
QLabel {{
    color: #e4e8f1;
    font-family: "Segoe UI";
    font-size: 12px;
    background: transparent;
}}
QPushButton {{
    background-color: #2a303c;
    color: #e7ebf2;
    border: 1px solid #3d4554;
    border-radius: 12px;
    padding: 7px 16px;
    font-family: "Segoe UI";
    font-size: 12px;
    min-width: 70px;
}}
QPushButton:hover {{
    background-color: #333a48;
    border-color: #4a5366;
}}
QPushButton:pressed {{
    background-color: #242a36;
}}
QPushButton:disabled {{
    background-color: #2a2f3a;
    color: #8f98aa;
    border-color: #353d4b;
}}
QListWidget {{
    background-color: #262c38;
    color: #e4e8f1;
    border: 1px solid #3d4554;
    border-radius: 12px;
    font-family: "Consolas";
    font-size: 11px;
}}
QListWidget::item:selected {{
    background-color: #3a455a;
}}
QGroupBox {{
    color: #e4e8f1;
    border: 1px solid #3d4554;
    border-radius: 14px;
    margin-top: {TIGHT_SPACING}px;
    padding-top: {GROUPBOX_MARGIN}px;
    font-family: "Segoe UI";
    font-size: 12px;
    font-weight: bold;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
}}
QComboBox, QSpinBox, QDoubleSpinBox {{
    background-color: #262c38;
    color: #e4e8f1;
    border: 1px solid #3d4554;
    border-radius: 12px;
    padding: 4px 8px;
    font-family: "Segoe UI";
    font-size: 12px;
}}
QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {{
    border-color: #4a5366;
}}
QComboBox QAbstractItemView {{
    background-color: #262c38;
    color: #e4e8f1;
    selection-background-color: #3a455a;
    border: 1px solid #3d4554;
}}
QCheckBox {{
    color: #e4e8f1;
    font-family: "Segoe UI";
    font-size: 12px;
    spacing: 6px;
}}
QDialog {{
    background-color: #1f242c;
}}
QStatusBar {{
    background-color: #262c38;
    color: #b4bccb;
    font-size: 11px;
}}
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollBar:vertical {{
    background: #2a303c;
    width: 10px;
    border-radius: 6px;
}}
QScrollBar::handle:vertical {{
    background: #4a5366;
    border-radius: 6px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: #5a657a;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
""".format(
    TIGHT_SPACING=TIGHT_SPACING,
    GROUPBOX_MARGIN=GROUPBOX_MARGIN,
)

# ---------------------------------------------------------------------------
# Menu-specific button styles
# ---------------------------------------------------------------------------

MENU_BUTTON_STYLE = """
QPushButton {{
    background-color: {bg};
    color: {fg};
    border: 2px solid {border};
    border-radius: 12px;
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
        bg="#3a2f1f", fg="#f1d7a5", border="#5a4630",
        font_size=15,
        hover_bg="#4a3b26", hover_border="#6b5236",
        pressed_bg="#332818",
    )


def menu_button_outline() -> str:
    return MENU_BUTTON_STYLE.format(
        bg="#2a303c", fg="#e4e8f1", border="#3d4554",
        font_size=14,
        hover_bg="#333a48", hover_border="#4a5366",
        pressed_bg="#242a36",
    )


def menu_button_danger() -> str:
    return MENU_BUTTON_STYLE.format(
        bg="#3a2226", fg="#f0b0b0", border="#5a3138",
        font_size=14,
        hover_bg="#4a2b31", hover_border="#6b3b44",
        pressed_bg="#321c20",
    )


CARD_STYLE_NORMAL = """
    background-color: #262c38;
    border: 2px solid #3d4554;
    border-radius: 14px;
"""

CARD_STYLE_SELECTED = """
    background-color: #3a3122;
    border: 2px solid #7a5c38;
    border-radius: 14px;
"""

SETUP_START_BUTTON = """
QPushButton {
    background-color: #3a2f1f;
    color: #f1d7a5;
    border: 1px solid #5a4630;
    border-radius: 14px;
    padding: 14px 48px;
    font-family: "Segoe UI";
    font-size: 16px;
    font-weight: bold;
    min-width: 200px;
}
QPushButton:hover {
    background-color: #4a3b26;
    border-color: #6b5236;
}
QPushButton:pressed {
    background-color: #332818;
}
"""

SETUP_BACK_BUTTON = """
QPushButton {
    background-color: #2a303c;
    color: #cfd6e2;
    border: 1px solid #3d4554;
    border-radius: 12px;
    padding: 8px 24px;
    font-family: "Segoe UI";
    font-size: 13px;
    min-width: 100px;
}
QPushButton:hover {
    color: #e4e8f1;
    border-color: #4a5366;
    background-color: #333a48;
}
"""
