"""
Game setup screen – configure board size, ruleset, komi, and advanced options
before starting a new game.

Uses visual "cards" for board size and ruleset selection.
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPen
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from ..engine.rules import KoRule
from ..engine.state import DEFAULT_KOMI, GameConfig, Ruleset
from . import theme


# ---------------------------------------------------------------------------
# Selectable card widget
# ---------------------------------------------------------------------------

class _SelectCard(QFrame):
    """A clickable card widget for option selection."""

    clicked = Signal()

    def __init__(
        self,
        title: str,
        description: str,
        icon_text: str = "",
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.setFixedSize(180, 150)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._selected = False
        self._title = title
        self._desc = description
        self._icon = icon_text
        self._build_ui()
        self._apply_style()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        if self._icon:
            lbl_icon = QLabel(self._icon)
            lbl_icon.setFont(theme.font_bold(28))
            lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_icon.setStyleSheet("color: #b98f4f;")
            layout.addWidget(lbl_icon)

        lbl_title = QLabel(self._title)
        lbl_title.setFont(theme.font_bold(14))
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet("color: #3a3f49;")
        layout.addWidget(lbl_title)

        lbl_desc = QLabel(self._desc)
        lbl_desc.setFont(theme.font_normal(10))
        lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("color: #7a828f;")
        layout.addWidget(lbl_desc)

        layout.addStretch()

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        self._selected = value
        self._apply_style()

    def _apply_style(self) -> None:
        if self._selected:
            self.setStyleSheet(theme.CARD_STYLE_SELECTED)
        else:
            self.setStyleSheet(theme.CARD_STYLE_NORMAL)

    def mousePressEvent(self, event) -> None:  # type: ignore[override]
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


# ---------------------------------------------------------------------------
# Card group (radio-style)
# ---------------------------------------------------------------------------

class _CardGroup:
    """Manages mutual exclusion among a set of _SelectCard widgets."""

    def __init__(self) -> None:
        self._cards: list[_SelectCard] = []
        self._selected_index: int = 0

    def add(self, card: _SelectCard) -> int:
        idx = len(self._cards)
        self._cards.append(card)
        card.clicked.connect(lambda i=idx: self.select(i))
        return idx

    def select(self, index: int) -> None:
        for i, c in enumerate(self._cards):
            c.selected = (i == index)
        self._selected_index = index

    @property
    def selected_index(self) -> int:
        return self._selected_index


# ---------------------------------------------------------------------------
# Game Setup Screen
# ---------------------------------------------------------------------------

class GameSetupScreen(QWidget):
    """Full-screen game configuration before starting."""

    start_game = Signal(object)   # emits GameConfig
    back_clicked = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._size_group = _CardGroup()
        self._rule_group = _CardGroup()
        self._build_ui()
        # Set defaults
        self._size_group.select(2)  # 19x19
        self._rule_group.select(0)  # Japanese
        self._on_size_changed()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(40, 30, 40, 30)
        outer.setSpacing(0)

        # Header
        header = QHBoxLayout()
        self._btn_back = QPushButton("Quay lại")
        self._btn_back.setStyleSheet(theme.SETUP_BACK_BUTTON)
        self._btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_back.clicked.connect(self.back_clicked)
        header.addWidget(self._btn_back)
        header.addStretch()
        lbl_title = QLabel("Ván mới")
        lbl_title.setFont(theme.font_bold(22))
        lbl_title.setStyleSheet("color: #b98f4f;")
        header.addWidget(lbl_title)
        header.addStretch()
        # Invisible spacer to balance the back button
        spacer_btn = QPushButton("")
        spacer_btn.setFixedWidth(80)
        spacer_btn.setStyleSheet("border:none; background:transparent;")
        header.addWidget(spacer_btn)
        outer.addLayout(header)

        outer.addSpacing(24)

        # -- Board size section --
        lbl_size = QLabel("Kích thước bàn cờ")
        lbl_size.setFont(theme.font_bold(15))
        lbl_size.setStyleSheet("color: #3a3f49;")
        outer.addWidget(lbl_size)
        outer.addSpacing(10)

        size_row = QHBoxLayout()
        size_row.setSpacing(16)

        size_row.addStretch()
        card_9 = _SelectCard("9 × 9", "Ván nhanh\n~15 phút", "9")
        card_13 = _SelectCard("13 × 13", "Ván trung bình\n~30 phút", "13")
        card_19 = _SelectCard("19 × 19", "Ván tiêu chuẩn\n~60+ phút", "19")

        for card in [card_9, card_13, card_19]:
            self._size_group.add(card)
            size_row.addWidget(card)
            card.clicked.connect(self._on_size_changed)

        size_row.addStretch()
        outer.addLayout(size_row)

        outer.addSpacing(24)

        # -- Ruleset section --
        lbl_rules = QLabel("Luật chơi")
        lbl_rules.setFont(theme.font_bold(15))
        lbl_rules.setStyleSheet("color: #3a3f49;")
        outer.addWidget(lbl_rules)
        outer.addSpacing(10)

        rule_row = QHBoxLayout()
        rule_row.setSpacing(16)

        rule_row.addStretch()
        card_jp = _SelectCard(
            "Nhật Bản",
            "Tính đất\nCó tính bắt quân",
            "JP",
        )
        card_cn = _SelectCard(
            "Trung Quốc",
            "Tính diện tích\nQuân + Đất",
            "CN",
        )

        for card in [card_jp, card_cn]:
            self._rule_group.add(card)
            rule_row.addWidget(card)

        rule_row.addStretch()
        outer.addLayout(rule_row)

        outer.addSpacing(24)

        # -- Komi & advanced --
        detail_row = QHBoxLayout()
        detail_row.setSpacing(30)

        # Komi
        komi_col = QVBoxLayout()
        lbl_komi = QLabel("Komi (bù điểm cho Trắng)")
        lbl_komi.setFont(theme.font_bold(12))
        lbl_komi.setStyleSheet("color: #6f7786;")
        komi_col.addWidget(lbl_komi)
        self._komi_spin = QDoubleSpinBox()
        self._komi_spin.setRange(0.0, 99.5)
        self._komi_spin.setSingleStep(0.5)
        self._komi_spin.setDecimals(1)
        self._komi_spin.setValue(6.5)
        self._komi_spin.setFixedWidth(120)
        komi_col.addWidget(self._komi_spin)
        detail_row.addLayout(komi_col)

        # Ko rule
        ko_col = QVBoxLayout()
        lbl_ko = QLabel("Luật Ko")
        lbl_ko.setFont(theme.font_bold(12))
        lbl_ko.setStyleSheet("color: #6f7786;")
        ko_col.addWidget(lbl_ko)
        self._ko_combo = QComboBox()
        self._ko_combo.addItems(["Ko đơn giản", "Siêu Ko theo vị trí"])
        self._ko_combo.setFixedWidth(200)
        ko_col.addWidget(self._ko_combo)
        detail_row.addLayout(ko_col)

        # Suicide
        suicide_col = QVBoxLayout()
        lbl_sui = QLabel("Nâng cao")
        lbl_sui.setFont(theme.font_bold(12))
        lbl_sui.setStyleSheet("color: #6f7786;")
        suicide_col.addWidget(lbl_sui)
        self._suicide_check = QCheckBox("Cho phép nước đi tự sát")
        suicide_col.addWidget(self._suicide_check)
        detail_row.addLayout(suicide_col)
        detail_row.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        outer.addLayout(detail_row)

        outer.addStretch()

        # -- Start button --
        bottom = QHBoxLayout()
        bottom.addStretch()
        self._btn_start = QPushButton("Bắt đầu ván")
        self._btn_start.setStyleSheet(theme.SETUP_START_BUTTON)
        self._btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_start.clicked.connect(self._on_start)
        bottom.addWidget(self._btn_start)
        bottom.addStretch()
        outer.addLayout(bottom)

    # -- slots --------------------------------------------------------------

    def _on_size_changed(self) -> None:
        sizes = [9, 13, 19]
        size = sizes[self._size_group.selected_index]
        self._komi_spin.setValue(DEFAULT_KOMI.get(size, 6.5))

    def _on_start(self) -> None:
        sizes = [9, 13, 19]
        size = sizes[self._size_group.selected_index]
        ruleset = Ruleset.JAPANESE if self._rule_group.selected_index == 0 else Ruleset.CHINESE
        ko_rule = KoRule.SIMPLE if self._ko_combo.currentIndex() == 0 else KoRule.POSITIONAL_SUPERKO

        config = GameConfig(
            board_size=size,
            ruleset=ruleset,
            komi=self._komi_spin.value(),
            ko_rule=ko_rule,
            allow_suicide=self._suicide_check.isChecked(),
        )
        self.start_game.emit(config)

    # -- background painting ------------------------------------------------

    def paintEvent(self, event) -> None:  # type: ignore[override]
        p = QPainter(self)
        w, h = self.width(), self.height()
        grad = QLinearGradient(0, 0, w, h)
        grad.setColorAt(0.0, QColor(246, 248, 252))
        grad.setColorAt(1.0, QColor(233, 238, 247))
        p.fillRect(self.rect(), grad)
        p.end()
