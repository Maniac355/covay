"""
Board widget – renders the Go board using QPainter.

Handles:
  - Grid drawing with coordinate labels
  - Hoshi (star) points
  - Stones with shadow and anti-aliasing
  - Ghost stone on hover
  - Last-move marker
  - Scoring-mode overlays (dead stones, territory)
  - Mouse interaction (click to play, hover preview)
"""

from __future__ import annotations

import math
from typing import Optional

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import (
    QBrush,
    QColor,
    QLinearGradient,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPen,
    QRadialGradient,
)
from PySide6.QtWidgets import QWidget

from ..engine.board import Stone, Point
from ..engine.state import GamePhase, GameState
from . import theme


class BoardWidget(QWidget):
    """Custom widget that draws the Go board and handles interaction."""

    # Signals
    stone_placed = Signal(int, int)   # row, col
    dead_toggled = Signal(int, int)   # row, col (scoring mode)

    # Board padding (fraction of cell size)
    _PADDING_CELLS = 1.5

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setMinimumSize(400, 400)

        self._game: Optional[GameState] = None
        self._hover_point: Optional[Point] = None
        self._last_move_point: Optional[Point] = None

    # -- public API ---------------------------------------------------------

    def set_game(self, game: GameState) -> None:
        self._game = game
        self._hover_point = None
        self._update_last_move()
        self.update()

    def refresh(self) -> None:
        self._update_last_move()
        self.update()

    # -- internal -----------------------------------------------------------

    def _update_last_move(self) -> None:
        if self._game is None:
            self._last_move_point = None
            return
        moves = self._game.move_list
        self._last_move_point = None
        for m in reversed(moves):
            if m.point is not None:
                self._last_move_point = m.point
                break

    @property
    def _board_size(self) -> int:
        return self._game.board.size if self._game else 19

    def _cell_size(self) -> float:
        """Pixel size of one grid cell."""
        n = self._board_size
        pad = self._PADDING_CELLS * 2
        available = min(self.width(), self.height())
        return available / (n - 1 + pad)

    def _origin(self) -> QPointF:
        """Top-left grid intersection in widget coordinates."""
        cs = self._cell_size()
        pad = self._PADDING_CELLS * cs
        # Centre the board
        total = (self._board_size - 1) * cs + 2 * pad
        ox = (self.width() - total) / 2 + pad
        oy = (self.height() - total) / 2 + pad
        return QPointF(ox, oy)

    def _grid_to_pixel(self, row: int, col: int) -> QPointF:
        o = self._origin()
        cs = self._cell_size()
        return QPointF(o.x() + col * cs, o.y() + row * cs)

    def _pixel_to_grid(self, x: float, y: float) -> Optional[Point]:
        o = self._origin()
        cs = self._cell_size()
        col = round((x - o.x()) / cs)
        row = round((y - o.y()) / cs)
        n = self._board_size
        if 0 <= row < n and 0 <= col < n:
            # Check distance from intersection
            px = o.x() + col * cs
            py = o.y() + row * cs
            dist = math.hypot(x - px, y - py)
            if dist < cs * 0.45:
                return (row, col)
        return None

    # -- painting -----------------------------------------------------------

    def paintEvent(self, event) -> None:  # type: ignore[override]
        if self._game is None:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        self._draw_background(painter)
        self._draw_grid(painter)
        self._draw_hoshi(painter)
        self._draw_coordinates(painter)
        self._draw_stones(painter)
        self._draw_last_move_marker(painter)
        self._draw_ghost(painter)

        if self._game.phase == GamePhase.SCORING:
            self._draw_scoring_overlay(painter)

        painter.end()

    def _draw_background(self, p: QPainter) -> None:
        grad = theme.board_gradient(self.width(), self.height())
        p.fillRect(self.rect(), grad)

    def _draw_grid(self, p: QPainter) -> None:
        n = self._board_size
        cs = self._cell_size()
        o = self._origin()

        pen = QPen(theme.GRID_COLOR, max(1.0, cs * 0.025))
        p.setPen(pen)

        for i in range(n):
            # Horizontal
            y = o.y() + i * cs
            p.drawLine(QPointF(o.x(), y), QPointF(o.x() + (n - 1) * cs, y))
            # Vertical
            x = o.x() + i * cs
            p.drawLine(QPointF(x, o.y()), QPointF(x, o.y() + (n - 1) * cs))

    def _draw_hoshi(self, p: QPainter) -> None:
        cs = self._cell_size()
        radius = max(2.5, cs * 0.1)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(theme.HOSHI_COLOR))

        for r, c in self._game.board.hoshi_points():
            pt = self._grid_to_pixel(r, c)
            p.drawEllipse(pt, radius, radius)

    def _draw_coordinates(self, p: QPainter) -> None:
        n = self._board_size
        cs = self._cell_size()
        o = self._origin()
        offset = cs * 0.75

        font = theme.font_normal(max(8, int(cs * 0.32)))
        p.setFont(font)
        p.setPen(QPen(QColor(80, 50, 20)))

        for c in range(n):
            letter = chr(ord('A') + c + (1 if c >= 8 else 0))
            x = o.x() + c * cs
            # Top
            p.drawText(
                QRectF(x - cs / 2, o.y() - offset - cs * 0.3, cs, cs * 0.4),
                Qt.AlignmentFlag.AlignCenter,
                letter,
            )
            # Bottom
            p.drawText(
                QRectF(x - cs / 2, o.y() + (n - 1) * cs + offset - cs * 0.1, cs, cs * 0.4),
                Qt.AlignmentFlag.AlignCenter,
                letter,
            )

        for r in range(n):
            number = str(n - r)
            y = o.y() + r * cs
            # Left
            p.drawText(
                QRectF(o.x() - offset - cs * 0.5, y - cs * 0.2, cs * 0.6, cs * 0.4),
                Qt.AlignmentFlag.AlignCenter,
                number,
            )
            # Right
            p.drawText(
                QRectF(o.x() + (n - 1) * cs + offset - cs * 0.1, y - cs * 0.2, cs * 0.6, cs * 0.4),
                Qt.AlignmentFlag.AlignCenter,
                number,
            )

    def _draw_stone(
        self, p: QPainter, row: int, col: int, color: Stone, opacity: float = 1.0
    ) -> None:
        cs = self._cell_size()
        radius = cs * 0.44
        center = self._grid_to_pixel(row, col)

        p.setOpacity(opacity)

        # Shadow
        if opacity > 0.8:
            shadow_center = QPointF(
                center.x() + theme.STONE_SHADOW_OFFSET,
                center.y() + theme.STONE_SHADOW_OFFSET,
            )
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(theme.STONE_SHADOW))
            p.drawEllipse(shadow_center, radius, radius)

        # Stone with gradient
        if color == Stone.BLACK:
            grad = QRadialGradient(
                center.x() - radius * 0.3,
                center.y() - radius * 0.3,
                radius * 1.8,
            )
            grad.setColorAt(0.0, theme.BLACK_STONE_HIGHLIGHT)
            grad.setColorAt(1.0, theme.BLACK_STONE)
        else:
            grad = QRadialGradient(
                center.x() - radius * 0.3,
                center.y() - radius * 0.3,
                radius * 1.8,
            )
            grad.setColorAt(0.0, theme.WHITE_STONE_HIGHLIGHT)
            grad.setColorAt(1.0, theme.WHITE_STONE)

        p.setPen(QPen(QColor(30, 30, 30, int(180 * opacity)), max(0.5, cs * 0.015)))
        p.setBrush(QBrush(grad))
        p.drawEllipse(center, radius, radius)

        p.setOpacity(1.0)

    def _draw_stones(self, p: QPainter) -> None:
        board = self._game.board
        for r in range(board.size):
            for c in range(board.size):
                stone = board.get(r, c)
                if stone != Stone.EMPTY:
                    self._draw_stone(p, r, c, stone)

    def _draw_last_move_marker(self, p: QPainter) -> None:
        if self._last_move_point is None:
            return
        r, c = self._last_move_point
        stone = self._game.board.get(r, c)
        if stone == Stone.EMPTY:
            return

        cs = self._cell_size()
        center = self._grid_to_pixel(r, c)
        marker_radius = cs * 0.12

        marker_color = (
            theme.LAST_MOVE_MARKER_BLACK
            if stone == Stone.BLACK
            else theme.LAST_MOVE_MARKER_WHITE
        )
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(marker_color))
        p.drawEllipse(center, marker_radius, marker_radius)

    def _draw_ghost(self, p: QPainter) -> None:
        if self._game is None or self._game.phase != GamePhase.PLAYING:
            return
        if self._hover_point is None:
            return
        r, c = self._hover_point
        if self._game.board.get(r, c) != Stone.EMPTY:
            return
        self._draw_stone(p, r, c, self._game.current_turn, opacity=theme.GHOST_OPACITY)

    def _draw_scoring_overlay(self, p: QPainter) -> None:
        """Draw dead stone markers and territory indicators."""
        board = self._game.board
        dead = self._game.dead_stones
        cs = self._cell_size()

        # Mark dead stones with an X
        for r, c in dead:
            center = self._grid_to_pixel(r, c)
            radius = cs * 0.25
            p.setPen(QPen(QColor(255, 50, 50), max(1.5, cs * 0.06)))
            p.drawLine(
                QPointF(center.x() - radius, center.y() - radius),
                QPointF(center.x() + radius, center.y() + radius),
            )
            p.drawLine(
                QPointF(center.x() + radius, center.y() - radius),
                QPointF(center.x() - radius, center.y() + radius),
            )

        # Territory overlay
        # Build a clean board (without dead) and compute territory
        from ..engine.board import Board
        clean = board.copy()
        for r, c in dead:
            clean.set(r, c, Stone.EMPTY)
        territory = clean.get_territory()

        sq_size = cs * 0.22
        for color, pts in territory.items():
            if color == Stone.EMPTY:
                continue
            fill = theme.TERRITORY_BLACK if color == Stone.BLACK else theme.TERRITORY_WHITE
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(fill))
            for r, c in pts:
                center = self._grid_to_pixel(r, c)
                p.drawRect(QRectF(
                    center.x() - sq_size,
                    center.y() - sq_size,
                    sq_size * 2,
                    sq_size * 2,
                ))

    # -- mouse events -------------------------------------------------------

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = event.position()
        pt = self._pixel_to_grid(pos.x(), pos.y())
        if pt != self._hover_point:
            self._hover_point = pt
            self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return
        pos = event.position()
        pt = self._pixel_to_grid(pos.x(), pos.y())
        if pt is None:
            return

        if self._game is None:
            return

        r, c = pt
        if self._game.phase == GamePhase.PLAYING:
            self.stone_placed.emit(r, c)
        elif self._game.phase == GamePhase.SCORING:
            self.dead_toggled.emit(r, c)

    def leaveEvent(self, event) -> None:  # type: ignore[override]
        self._hover_point = None
        self.update()

    # -- sizing -------------------------------------------------------------

    def sizeHint(self):  # type: ignore[override]
        return self.minimumSize()

    def heightForWidth(self, w: int) -> int:
        return w
