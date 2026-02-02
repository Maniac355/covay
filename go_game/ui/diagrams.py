"""
Go diagram widgets for tutorial illustrations.

These widgets draw Go board diagrams directly using QPainter,
eliminating the need for remote images and working offline.
"""

from __future__ import annotations

from typing import Optional, List, Tuple
from enum import Enum

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QRadialGradient, QLinearGradient
from PySide6.QtWidgets import QWidget, QSizePolicy


class Stone(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class GoDiagram(QWidget):
    """Base class for Go board diagram illustrations."""

    # Colors
    BOARD_COLOR = QColor(220, 179, 92)
    BOARD_DARK = QColor(200, 160, 75)
    GRID_COLOR = QColor(60, 45, 20)
    BLACK_STONE = QColor(25, 25, 25)
    BLACK_HIGHLIGHT = QColor(70, 70, 70)
    WHITE_STONE = QColor(245, 245, 240)
    WHITE_HIGHLIGHT = QColor(255, 255, 255)
    MARKER_BLACK = QColor(200, 200, 200)
    MARKER_WHITE = QColor(40, 40, 40)
    LIBERTY_COLOR = QColor(100, 180, 100, 180)
    CAPTURE_COLOR = QColor(220, 80, 80, 180)
    TERRITORY_BLACK = QColor(0, 0, 0, 100)
    TERRITORY_WHITE = QColor(255, 255, 255, 120)

    def __init__(
        self,
        grid_size: int = 5,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._grid_size = grid_size
        self._stones: List[Tuple[int, int, Stone]] = []
        self._markers: List[Tuple[int, int, str, QColor]] = []  # x, y, text, color
        self._liberties: List[Tuple[int, int]] = []
        self._captures: List[Tuple[int, int]] = []
        self._territory_black: List[Tuple[int, int]] = []
        self._territory_white: List[Tuple[int, int]] = []

        self.setMinimumSize(120, 120)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_stones(self, stones: List[Tuple[int, int, Stone]]) -> None:
        """Set stone positions: [(x, y, Stone), ...]"""
        self._stones = stones
        self.update()

    def set_markers(self, markers: List[Tuple[int, int, str, QColor]]) -> None:
        """Set markers: [(x, y, text, color), ...]"""
        self._markers = markers
        self.update()

    def set_liberties(self, liberties: List[Tuple[int, int]]) -> None:
        """Highlight liberty points."""
        self._liberties = liberties
        self.update()

    def set_captures(self, captures: List[Tuple[int, int]]) -> None:
        """Highlight capture points."""
        self._captures = captures
        self.update()

    def set_territory(
        self,
        black: List[Tuple[int, int]],
        white: List[Tuple[int, int]],
    ) -> None:
        """Set territory markers."""
        self._territory_black = black
        self._territory_white = white
        self.update()

    def paintEvent(self, event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate board dimensions
        size = min(self.width(), self.height())
        margin = size * 0.08
        board_size = size - 2 * margin
        cell_size = board_size / (self._grid_size - 1) if self._grid_size > 1 else board_size

        # Offset to center the board
        offset_x = (self.width() - size) / 2 + margin
        offset_y = (self.height() - size) / 2 + margin

        # Draw board background
        self._draw_board_bg(p, offset_x - margin, offset_y - margin, size)

        # Draw grid
        self._draw_grid(p, offset_x, offset_y, cell_size)

        # Draw territory
        self._draw_territory(p, offset_x, offset_y, cell_size)

        # Draw liberties
        self._draw_liberties(p, offset_x, offset_y, cell_size)

        # Draw captures
        self._draw_captures(p, offset_x, offset_y, cell_size)

        # Draw stones
        self._draw_stones(p, offset_x, offset_y, cell_size)

        # Draw markers
        self._draw_markers(p, offset_x, offset_y, cell_size)

        p.end()

    def _draw_board_bg(self, p: QPainter, x: float, y: float, size: float) -> None:
        """Draw wooden board background."""
        grad = QLinearGradient(x, y, x + size, y + size)
        grad.setColorAt(0.0, self.BOARD_COLOR)
        grad.setColorAt(0.5, self.BOARD_DARK)
        grad.setColorAt(1.0, self.BOARD_COLOR)
        p.fillRect(QRectF(x, y, size, size), grad)

    def _draw_grid(self, p: QPainter, ox: float, oy: float, cell: float) -> None:
        """Draw grid lines."""
        pen = QPen(self.GRID_COLOR, 1.2)
        p.setPen(pen)

        for i in range(self._grid_size):
            # Horizontal
            p.drawLine(
                QPointF(ox, oy + i * cell),
                QPointF(ox + (self._grid_size - 1) * cell, oy + i * cell),
            )
            # Vertical
            p.drawLine(
                QPointF(ox + i * cell, oy),
                QPointF(ox + i * cell, oy + (self._grid_size - 1) * cell),
            )

        # Draw hoshi (star points) for larger boards
        if self._grid_size >= 9:
            hoshi_r = cell * 0.12
            p.setBrush(QBrush(self.GRID_COLOR))
            p.setPen(Qt.PenStyle.NoPen)
            center = self._grid_size // 2
            for hx, hy in [(center, center)]:
                p.drawEllipse(
                    QPointF(ox + hx * cell, oy + hy * cell),
                    hoshi_r, hoshi_r,
                )

    def _draw_stone(
        self,
        p: QPainter,
        cx: float,
        cy: float,
        r: float,
        is_black: bool,
    ) -> None:
        """Draw a single stone with gradient."""
        if is_black:
            grad = QRadialGradient(cx - r * 0.3, cy - r * 0.3, r * 1.5)
            grad.setColorAt(0.0, self.BLACK_HIGHLIGHT)
            grad.setColorAt(1.0, self.BLACK_STONE)
        else:
            grad = QRadialGradient(cx - r * 0.3, cy - r * 0.3, r * 1.5)
            grad.setColorAt(0.0, self.WHITE_HIGHLIGHT)
            grad.setColorAt(0.8, self.WHITE_STONE)
            grad.setColorAt(1.0, QColor(210, 210, 205))

        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(grad))
        p.drawEllipse(QPointF(cx, cy), r, r)

        # Add subtle border for white stones
        if not is_black:
            p.setPen(QPen(QColor(180, 180, 175), 1))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawEllipse(QPointF(cx, cy), r, r)

    def _draw_stones(self, p: QPainter, ox: float, oy: float, cell: float) -> None:
        """Draw all stones."""
        r = cell * 0.42
        for x, y, stone in self._stones:
            if stone == Stone.EMPTY:
                continue
            cx = ox + x * cell
            cy = oy + y * cell
            self._draw_stone(p, cx, cy, r, stone == Stone.BLACK)

    def _draw_markers(self, p: QPainter, ox: float, oy: float, cell: float) -> None:
        """Draw text markers on the board."""
        from PySide6.QtGui import QFont
        font = QFont("Segoe UI", int(cell * 0.4))
        font.setBold(True)
        p.setFont(font)

        for x, y, text, color in self._markers:
            cx = ox + x * cell
            cy = oy + y * cell
            p.setPen(QPen(color))
            rect = QRectF(cx - cell / 2, cy - cell / 2, cell, cell)
            p.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

    def _draw_liberties(self, p: QPainter, ox: float, oy: float, cell: float) -> None:
        """Draw liberty markers."""
        r = cell * 0.25
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(self.LIBERTY_COLOR))
        for x, y in self._liberties:
            cx = ox + x * cell
            cy = oy + y * cell
            p.drawEllipse(QPointF(cx, cy), r, r)

    def _draw_captures(self, p: QPainter, ox: float, oy: float, cell: float) -> None:
        """Draw capture markers (X)."""
        r = cell * 0.3
        pen = QPen(self.CAPTURE_COLOR, 3)
        p.setPen(pen)
        for x, y in self._captures:
            cx = ox + x * cell
            cy = oy + y * cell
            p.drawLine(QPointF(cx - r, cy - r), QPointF(cx + r, cy + r))
            p.drawLine(QPointF(cx - r, cy + r), QPointF(cx + r, cy - r))

    def _draw_territory(self, p: QPainter, ox: float, oy: float, cell: float) -> None:
        """Draw territory markers."""
        r = cell * 0.2
        for x, y in self._territory_black:
            cx = ox + x * cell
            cy = oy + y * cell
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(self.TERRITORY_BLACK))
            p.drawRect(QRectF(cx - r, cy - r, r * 2, r * 2))

        for x, y in self._territory_white:
            cx = ox + x * cell
            cy = oy + y * cell
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(self.TERRITORY_WHITE))
            p.drawRect(QRectF(cx - r, cy - r, r * 2, r * 2))


# ---------------------------------------------------------------------------
# Pre-configured diagrams for tutorial
# ---------------------------------------------------------------------------

def create_stones_diagram() -> GoDiagram:
    """Diagram showing black and white stones on a board."""
    d = GoDiagram(grid_size=5)
    d.set_stones([
        (1, 1, Stone.BLACK),
        (2, 1, Stone.BLACK),
        (3, 2, Stone.WHITE),
        (2, 2, Stone.WHITE),
        (1, 3, Stone.BLACK),
        (3, 3, Stone.BLACK),
        (2, 3, Stone.WHITE),
    ])
    return d


def create_liberties_diagram() -> GoDiagram:
    """Diagram showing liberties of a stone."""
    d = GoDiagram(grid_size=5)
    d.set_stones([
        (2, 2, Stone.BLACK),
    ])
    d.set_liberties([
        (1, 2), (3, 2), (2, 1), (2, 3),  # 4 liberties
    ])
    d.set_markers([
        (1, 2, "1", QColor(255, 255, 255)),
        (3, 2, "2", QColor(255, 255, 255)),
        (2, 1, "3", QColor(255, 255, 255)),
        (2, 3, "4", QColor(255, 255, 255)),
    ])
    return d


def create_capture_diagram() -> GoDiagram:
    """Diagram showing a capture situation."""
    d = GoDiagram(grid_size=5)
    d.set_stones([
        # White stone about to be captured
        (2, 2, Stone.WHITE),
        # Black stones surrounding
        (1, 2, Stone.BLACK),
        (3, 2, Stone.BLACK),
        (2, 1, Stone.BLACK),
    ])
    # Show the capture point
    d.set_captures([(2, 3)])
    d.set_markers([
        (2, 3, "X", QColor(220, 80, 80)),
    ])
    return d


def create_ko_diagram() -> GoDiagram:
    """Diagram showing a ko situation."""
    d = GoDiagram(grid_size=5)
    d.set_stones([
        # Ko shape
        (1, 2, Stone.BLACK),
        (2, 1, Stone.BLACK),
        (2, 3, Stone.BLACK),
        (3, 2, Stone.WHITE),
        (3, 1, Stone.WHITE),
        (3, 3, Stone.WHITE),
        (4, 2, Stone.WHITE),
    ])
    # Ko point
    d.set_captures([(2, 2)])
    d.set_markers([
        (2, 2, "Ko", QColor(220, 100, 100)),
    ])
    return d


def create_suicide_diagram() -> GoDiagram:
    """Diagram showing an illegal suicide move."""
    d = GoDiagram(grid_size=5)
    d.set_stones([
        # Surrounding black stones
        (1, 2, Stone.BLACK),
        (3, 2, Stone.BLACK),
        (2, 1, Stone.BLACK),
        (2, 3, Stone.BLACK),
    ])
    # Illegal move point
    d.set_captures([(2, 2)])
    d.set_markers([
        (2, 2, "X", QColor(220, 80, 80)),
    ])
    return d


def create_game_end_diagram() -> GoDiagram:
    """Diagram showing an end-game position."""
    d = GoDiagram(grid_size=7)
    d.set_stones([
        # Black territory (left side)
        (0, 1, Stone.BLACK),
        (0, 2, Stone.BLACK),
        (0, 3, Stone.BLACK),
        (1, 0, Stone.BLACK),
        (1, 4, Stone.BLACK),
        (2, 1, Stone.BLACK),
        (2, 2, Stone.BLACK),
        (2, 3, Stone.BLACK),
        # White territory (right side)
        (4, 1, Stone.WHITE),
        (4, 2, Stone.WHITE),
        (4, 3, Stone.WHITE),
        (5, 0, Stone.WHITE),
        (5, 4, Stone.WHITE),
        (6, 1, Stone.WHITE),
        (6, 2, Stone.WHITE),
        (6, 3, Stone.WHITE),
    ])
    d.set_territory(
        black=[(0, 0), (1, 1), (1, 2), (1, 3)],
        white=[(6, 0), (5, 1), (5, 2), (5, 3)],
    )
    return d


def create_japanese_scoring_diagram() -> GoDiagram:
    """Diagram showing Japanese territory scoring."""
    d = GoDiagram(grid_size=7)
    d.set_stones([
        # Black group
        (0, 3, Stone.BLACK),
        (1, 3, Stone.BLACK),
        (2, 3, Stone.BLACK),
        (2, 2, Stone.BLACK),
        (2, 1, Stone.BLACK),
        (2, 0, Stone.BLACK),
        # White group
        (4, 3, Stone.WHITE),
        (4, 2, Stone.WHITE),
        (4, 1, Stone.WHITE),
        (4, 0, Stone.WHITE),
        (5, 3, Stone.WHITE),
        (6, 3, Stone.WHITE),
    ])
    # Territory markers
    d.set_territory(
        black=[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
        white=[(5, 0), (5, 1), (5, 2), (6, 0), (6, 1), (6, 2)],
    )
    return d


def create_chinese_scoring_diagram() -> GoDiagram:
    """Diagram showing Chinese area scoring."""
    d = GoDiagram(grid_size=7)
    d.set_stones([
        # Black group (area = stones + territory)
        (0, 3, Stone.BLACK),
        (1, 3, Stone.BLACK),
        (2, 3, Stone.BLACK),
        (2, 2, Stone.BLACK),
        (2, 1, Stone.BLACK),
        (2, 0, Stone.BLACK),
        # White group
        (4, 3, Stone.WHITE),
        (4, 2, Stone.WHITE),
        (4, 1, Stone.WHITE),
        (4, 0, Stone.WHITE),
        (5, 3, Stone.WHITE),
        (6, 3, Stone.WHITE),
    ])
    # Territory + stones = area
    d.set_territory(
        black=[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
        white=[(5, 0), (5, 1), (5, 2), (6, 0), (6, 1), (6, 2)],
    )
    return d
