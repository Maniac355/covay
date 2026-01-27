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
            "QFrame { background-color: #ffffff; border-radius: 12px; border: 1px solid #e1e6f0; }"
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
        lbl_body.setStyleSheet("color: #566070; line-height: 1.5;")
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
            "QFrame { background-color: #f3f6fb; border-radius: 10px; border: 1px solid #e1e6f0; }"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)

        lbl = QLabel(text)
        lbl.setFont(theme.font_mono(11))
        lbl.setStyleSheet("color: #6f7a8a;")
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
        header.setStyleSheet("background-color: #eef2f8;")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(20, 0, 20, 0)

        self._btn_back = QPushButton("Về menu")
        self._btn_back.setStyleSheet(theme.SETUP_BACK_BUTTON)
        self._btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_back.clicked.connect(self.back_clicked)
        h_layout.addWidget(self._btn_back)

        lbl_title = QLabel("Hướng dẫn chơi Cờ Vây")
        lbl_title.setFont(theme.font_bold(18))
        lbl_title.setStyleSheet("color: #b98f4f;")
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
            "Cờ Vây là gì?",
            "Cờ Vây (còn gọi là <b>Weiqi</b> hoặc <b>Baduk</b>) là trò chơi chiến thuật "
            "dành cho hai người. Trò chơi có nguồn gốc từ Trung Quốc cách đây hơn 4.000 năm "
            "và là một trong những trò chơi cổ nhất vẫn còn được chơi đến nay.<br><br>"
            "Mục tiêu rất đơn giản: <b>kiểm soát nhiều đất hơn</b> đối thủ bằng cách "
            "đặt quân lên các giao điểm của bàn cờ.",
        ))

        content_layout.addWidget(_Section(
            "Luật cơ bản",
            "<b>1. Bàn cờ:</b> Cờ Vây chơi trên lưới các giao điểm. Kích thước chuẩn là "
            "9×9 (người mới), 13×13 (trung cấp) và 19×19 (tiêu chuẩn).<br><br>"
            "<b>2. Quân:</b> Đen đi trước. Hai bên lần lượt đặt một quân mỗi lượt vào "
            "giao điểm trống.<br><br>"
            "<b>3. Khí:</b> Mỗi quân (hoặc nhóm quân liên thông) có các <i>khí</i> — "
            "các giao điểm trống kề trực tiếp (trên, dưới, trái, phải). Quân ở giữa có 4 khí; "
            "ở cạnh có 3; ở góc có 2.<br><br>"
            "<b>4. Đã đặt thì không di chuyển.</b> Quân chỉ bị lấy khỏi bàn khi bị bắt.",
            "#78a6d8",
        ))

        content_layout.addWidget(_Diagram(
            "  Ví dụ về khí:\n\n"
            "    . . . . .        . = ô trống\n"
            "    . . L . .        X = quân Đen\n"
            "    . L X L .        L = khí của X\n"
            "    . . L . .\n"
            "    . . . . .\n\n"
            "  Quân đơn này có 4 khí."
        ))

        content_layout.addWidget(_Section(
            "Bắt quân",
            "Khi một quân hoặc nhóm quân cùng màu <b>hết khí</b>, "
            "chúng sẽ bị <b>bắt</b> và lấy khỏi bàn.<br><br>"
            "Bạn bắt quân đối thủ bằng cách lấp nốt khí cuối cùng của họ. "
            "Việc bắt diễn ra ngay sau khi bạn đặt quân.<br><br>"
            "<b>Lưu ý:</b> Nếu nước đi của bạn đồng thời làm đối thủ hết khí "
            "và nhóm của bạn cũng hết khí, quân đối thủ sẽ bị bắt trước, "
            "từ đó nhóm của bạn có thể được thêm khí. Đây KHÔNG phải tự sát — "
            "đó là một nước bắt hợp lệ.",
            "#e38b6f",
        ))

        content_layout.addWidget(_Diagram(
            "  Ví dụ bắt quân:\n\n"
            "    Trước:           Sau khi Đen đi A:\n"
            "    . X . .          . X . .\n"
            "    X O A .    →     X . X .\n"
            "    . X . .          . X . .\n\n"
            "  O = quân Trắng còn 1 khí tại A.\n"
            "  Đen đi A → Trắng bị bắt và lấy khỏi bàn."
        ))

        content_layout.addWidget(_Section(
            "Luật Ko",
            "Tình huống <b>ko</b> xảy ra khi một quân bị bắt và đối thủ có thể bắt lại ngay, "
            "tạo ra vòng lặp vô hạn.<br><br>"
            "<b>Ko đơn giản:</b> Bạn không được bắt lại ngay quân vừa bị bắt. "
            "Bạn phải đi chỗ khác trước (đòn 'đe doạ ko'), rồi mới có thể bắt lại ở lượt sau.<br><br>"
            "<b>Siêu Ko theo vị trí:</b> Luật chặt hơn, không cho phép bất kỳ thế cờ nào "
            "lặp lại. Luật này xử lý cả những tình huống ko phức tạp.",
            "#b58ad6",
        ))

        content_layout.addWidget(_Diagram(
            "  Ví dụ ko:\n\n"
            "    . X O .          . X O .\n"
            "    X O . O    →     X . X O     Đen bắt O\n"
            "    . X O .          . X O .     tại (1,1)\n\n"
            "  Trắng KHÔNG được đi ngay vào\n"
            "  vị trí vừa bị bắt. Phải đi chỗ khác trước."
        ))

        content_layout.addWidget(_Section(
            "Tự sát",
            "Một <b>nước tự sát</b> là khi bạn đặt quân khiến quân (hoặc nhóm) của bạn "
            "hết khí mà không bắt được quân đối thủ.<br><br>"
            "Mặc định, tự sát <b>bị cấm</b>. Một số luật cho phép — "
            "bạn có thể bật/tắt trong phần cài đặt.",
            "#e3779a",
        ))

        content_layout.addWidget(_Section(
            "Bỏ lượt và kết thúc ván",
            "Bạn có thể <b>bỏ lượt</b> thay vì đặt quân. "
            "Khi cả hai bên bỏ lượt liên tiếp, ván sẽ chuyển sang "
            "<b>Chế độ tính điểm</b>.<br><br>"
            "Trong chế độ tính điểm, hai bên thống nhất quân nào là 'chết' "
            "(sẽ bị bắt chắc chắn). Nhấn vào nhóm quân để đánh dấu sống/chết, "
            "sau đó xác nhận để tính điểm cuối.",
            "#75bfa6",
        ))

        content_layout.addWidget(_Section(
            "Tính điểm: Luật Nhật Bản (Tính đất)",
            "Theo luật Nhật Bản, điểm của bạn gồm:<br><br>"
            "<table style='color:#566070;'>"
            "<tr><td style='padding-right:20px;'><b>Đất</b></td>"
            "<td>Các giao điểm trống được bao quanh <i>chỉ</i> bởi quân của bạn</td></tr>"
            "<tr><td><b>+ Bắt quân</b></td>"
            "<td>Số quân đối thủ bị bạn bắt trong ván</td></tr>"
            "<tr><td><b>+ Quân chết</b></td>"
            "<td>Quân chết của đối thủ (thống nhất khi tính điểm) được tính như bắt quân</td></tr>"
            "<tr><td><b>+ Komi</b></td>"
            "<td>Trắng nhận komi (bù cho việc đi sau)</td></tr>"
            "</table><br>"
            "<b>Komi mặc định:</b> 19×19 → 6.5 · 13×13 → 5.5 · 9×9 → 3.5<br><br>"
            "Nửa điểm (0.5) của komi giúp tránh hòa.",
            "#d9b05c",
        ))

        content_layout.addWidget(_Diagram(
            "  Ví dụ tính điểm Nhật (9x9):\n\n"
            "  Komi = 3.5 (cho Trắng)\n\n"
            "  Đen: 20 đất + 4 bắt quân      = 24.0\n"
            "  Trắng: 18 đất + 2 bắt quân + 3.5 = 23.5\n\n"
            "  → Đen thắng 0.5 điểm"
        ))

        content_layout.addWidget(_Section(
            "Tính điểm: Luật Trung Quốc (Tính diện tích)",
            "Theo luật Trung Quốc, điểm của bạn gồm:<br><br>"
            "<table style='color:#566070;'>"
            "<tr><td style='padding-right:20px;'><b>Quân trên bàn</b></td>"
            "<td>Số quân còn lại của bạn trên bàn</td></tr>"
            "<tr><td><b>+ Đất</b></td>"
            "<td>Các giao điểm trống được bao quanh bởi quân của bạn</td></tr>"
            "<tr><td><b>+ Komi</b></td>"
            "<td>Trắng nhận komi</td></tr>"
            "</table><br>"
            "Lưu ý: Bắt quân KHÔNG được tính riêng trong luật Trung Quốc, "
            "vì quân bị bắt sẽ làm giảm số quân trên bàn của đối thủ.",
            "#6aa9e0",
        ))

        content_layout.addWidget(_Diagram(
            "  Ví dụ tính điểm Trung Quốc (9x9):\n\n"
            "  Komi = 3.5 (cho Trắng)\n\n"
            "  Đen: 30 quân + 10 đất      = 40.0\n"
            "  Trắng: 25 quân + 12 đất + 3.5 = 40.5\n\n"
            "  → Trắng thắng 0.5 điểm"
        ))

        content_layout.addWidget(_Section(
            "Nhật Bản vs Trung Quốc: Khi nào khác biệt?",
            "Trong đa số ván thông thường, hai cách tính điểm cho ra <b>cùng người thắng</b>. "
            "Sự khác biệt chỉ xuất hiện ở một số tình huống đặc biệt:<br><br>"
            "• Luật Nhật: bạn mất điểm khi tự đi vào đất của mình (điền dame / phòng thủ). "
            "Luật Trung Quốc thì không.<br>"
            "• Luật Trung Quốc khuyến khích điền dame, vì quân trên bàn cũng tính điểm.<br>"
            "• Luật Trung Quốc dễ kiểm tra và ít tranh cãi hơn.<br>"
            "• Luật Nhật là truyền thống trong thi đấu chuyên nghiệp ở Nhật và Hàn.",
            "#9aa663",
        ))

        content_layout.addWidget(_Section(
            "Mẹo cho người mới",
            "• <b>Bắt đầu với 9×9</b> để nắm cơ bản trước khi lên 19×19.<br>"
            "• <b>Đừng cố bắt mọi thứ.</b> Hãy tập trung xây đất.<br>"
            "• <b>Kết nối các quân</b> để tạo nhóm mạnh.<br>"
            "• <b>Giữ nhóm sống</b> — một nhóm cần hai 'mắt' (khí bên trong) để an toàn lâu dài.<br>"
            "• <b>Đừng ngại bỏ lượt.</b> Nếu không có nước đi hữu ích, hãy bỏ lượt.<br>"
            "• <b>Chúc vui!</b> Cờ Vây là hành trình — bạn sẽ tiến bộ sau mỗi ván.",
            "#7fbfa1",
        ))

        content_layout.addSpacing(30)

        scroll.setWidget(content)
        outer.addWidget(scroll)

    # -- background painting ------------------------------------------------

    def paintEvent(self, event) -> None:  # type: ignore[override]
        p = QPainter(self)
        w, h = self.width(), self.height()
        grad = QLinearGradient(0, 0, w, h)
        grad.setColorAt(0.0, QColor(246, 248, 252))
        grad.setColorAt(1.0, QColor(235, 239, 247))
        p.fillRect(self.rect(), grad)
        p.end()
