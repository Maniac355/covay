"""
Tutorial / How-to-Play screen.

A scrollable guide explaining Go rules, capturing, ko, and scoring
for both Japanese and Chinese rulesets.
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QLinearGradient, QPainter
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
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
            "QFrame { background-color: #242a36; border-radius: 12px; border: 1px solid #3d4554; }"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            theme.BASE_PADDING,
            theme.BASE_PADDING,
            theme.BASE_PADDING,
            theme.BASE_PADDING,
        )
        layout.setSpacing(theme.TIGHT_SPACING)

        lbl_title = QLabel(title)
        lbl_title.setFont(theme.font_bold(15))
        lbl_title.setStyleSheet(f"color: {accent_color};")
        layout.addWidget(lbl_title)

        lbl_body = QLabel(body)
        lbl_body.setFont(theme.font_normal(12))
        lbl_body.setWordWrap(True)
        lbl_body.setStyleSheet("color: #c9d1de; line-height: 1.5;")
        lbl_body.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(lbl_body)


# ---------------------------------------------------------------------------
# Illustration widgets
# ---------------------------------------------------------------------------

class _Illustration(QFrame):
    """Visual card with a title and rich-text diagram."""

    def __init__(self, title: str, body: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            "QFrame { background-color: #2a303c; border-radius: 12px; border: 1px solid #3d4554; }"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            theme.BASE_PADDING,
            theme.BASE_PADDING,
            theme.BASE_PADDING,
            theme.BASE_PADDING,
        )
        layout.setSpacing(theme.TIGHT_SPACING)

        lbl_title = QLabel(title)
        lbl_title.setFont(theme.font_bold(12))
        lbl_title.setStyleSheet("color: #b8c0cf;")
        layout.addWidget(lbl_title)

        lbl_body = QLabel(body)
        lbl_body.setTextFormat(Qt.TextFormat.RichText)
        lbl_body.setStyleSheet("color: #c9d1de; line-height: 1.5; font-size: 13px;")
        lbl_body.setWordWrap(True)
        layout.addWidget(lbl_body)


class _SectionRow(QWidget):
    """Row combining a section description and an illustration."""

    def __init__(
        self,
        section: _Section,
        illustration: Optional[QWidget] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(theme.ITEM_SPACING)
        layout.addWidget(section, stretch=3)
        if illustration is not None:
            layout.addWidget(illustration, stretch=2)


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
        header.setFixedHeight(theme.HEADER_HEIGHT)
        header.setStyleSheet(f"background-color: {theme.HEADER_BG.name()};")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(
            theme.BASE_PADDING,
            0,
            theme.BASE_PADDING,
            0,
        )

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
        content_layout.setContentsMargins(*theme.CONTENT_MARGIN)
        content_layout.setSpacing(theme.SECTION_SPACING)

        # -- Sections --

        content_layout.addWidget(_SectionRow(
            _Section(
                "Cờ Vây là gì?",
                "Cờ Vây (còn gọi là <b>Weiqi</b> hoặc <b>Baduk</b>) là trò chơi chiến thuật "
                "dành cho hai người. Trò chơi có nguồn gốc từ Trung Quốc cách đây hơn 4.000 năm "
                "và là một trong những trò chơi cổ nhất vẫn còn được chơi đến nay.<br><br>"
                "Mục tiêu rất đơn giản: <b>kiểm soát nhiều đất hơn</b> đối thủ bằng cách "
                "đặt quân lên các giao điểm của bàn cờ.",
            ),
            _Illustration(
                "Ký hiệu quân cờ",
                "<div style='font-family: \"Segoe UI\"; font-size: 14px; color:#c9d1de;'>"
                "<b style='color:#111;'>●</b> Quân Đen &nbsp;&nbsp; "
                "<span style='color:#ffffff; text-shadow: 0 0 1px #3f4755; "
                "border: 1px solid #6b7485; border-radius: 50%; padding: 1px 3px;'>○</span> "
                "Quân Trắng &nbsp;&nbsp; <b style='color:#c2c7d1;'>●</b> Đánh dấu khí &nbsp;&nbsp; "
                "<b style='color:#8c95a4;'>·</b> Giao điểm trống<br><br>"
                "<span style='font-size: 20px; color:#111;'>● ● ● ●</span>"
                "&nbsp;&nbsp;"
                "<span style='font-size: 20px; color:#ffffff; text-shadow: 0 0 1px #3f4755; "
                "border: 1px solid #6b7485; border-radius: 50%; padding: 1px 3px;'>○ ○ ○</span>"
                "</div>",
            ),
        ))

        content_layout.addWidget(_SectionRow(
            _Section(
                "Luật cơ bản",
                "<b>1. Bàn cờ:</b> Cờ Vây chơi trên lưới các giao điểm. Kích thước chuẩn là "
                "9×9 (người mới), 13×13 (trung cấp) và 19×19 (tiêu chuẩn).<br><br>"
                "<b>2. Quân Đen/Trắng:</b> Đen đi trước. Hai bên lần lượt đặt 1 quân mỗi lượt "
                "vào giao điểm trống; đã đặt thì không di chuyển quân nữa.<br><br>"
                "<b>3. Khí:</b> Mỗi quân (hoặc nhóm quân liên thông) có các <i>khí</i> — "
                "giao điểm trống kề trực tiếp (trên, dưới, trái, phải). Quân ở giữa có 4 khí; "
                "ở cạnh có 3; ở góc có 2.<br><br>"
                "<b>4. Mục tiêu:</b> Đen và Trắng đều cố gắng kiểm soát nhiều đất hơn đối thủ.",
                "#78a6d8",
            ),
            _Illustration(
                "Ví dụ về khí",
                "<div style='color:#c9d1de;'>"
                "<pre style='font-family: Consolas; font-size: 13px; line-height: 1.5; margin: 0;'>"
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#9aa3b2;'>·</span>\n"
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#c2c7d1;'>●</span> "
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#9aa3b2;'>·</span>\n"
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#c2c7d1;'>●</span> "
                "<span style='color:#111;'>●</span> "
                "<span style='color:#c2c7d1;'>●</span> "
                "<span style='color:#9aa3b2;'>·</span>\n"
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#c2c7d1;'>●</span> "
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#9aa3b2;'>·</span>\n"
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#9aa3b2;'>·</span>"
                "</pre>"
                "<div style='margin-top: 6px;'>"
                "<span style='color:#9aa3b2;'>·</span> ô trống &nbsp; "
                "<span style='color:#c2c7d1;'>●</span> khí &nbsp; "
                "<span style='color:#111;'>●</span> quân Đen"
                "</div>"
                "<div style='margin-top: 6px; font-weight: 600;'>Quân đơn có 4 khí.</div>"
                "</div>",
            ),
        ))

        content_layout.addWidget(_SectionRow(
            _Section(
                "Bắt quân",
                "Khi một quân hoặc nhóm quân cùng màu <b>hết khí</b>, "
                "chúng sẽ bị <b>bắt</b> và lấy khỏi bàn.<br><br>"
                "Đen bắt quân Trắng (hoặc ngược lại) bằng cách lấp nốt khí cuối cùng "
                "của nhóm đối thủ. Việc bắt diễn ra ngay sau khi bạn đặt quân.<br><br>"
                "<b>Lưu ý:</b> Nếu nước đi của bạn đồng thời làm đối thủ hết khí "
                "và nhóm của bạn cũng hết khí, quân đối thủ sẽ bị bắt trước, "
                "từ đó nhóm của bạn có thể được thêm khí. Đây KHÔNG phải tự sát — "
                "đó là một nước bắt hợp lệ.",
                "#e38b6f",
            ),
            _Illustration(
                "Ví dụ bắt quân",
                "<div style='color:#c9d1de;'>"
                "<div style='display:flex; justify-content: space-between; font-weight:600;'>"
                "<span>Trước</span><span>Sau khi Đen đi A</span></div>"
                "<pre style='font-family: Consolas; font-size: 13px; line-height: 1.5; margin: 6px 0 0;'>"
                "<span style='color:#9aa3b2;'>·</span> <span style='color:#111;'>●</span> "
                "<span style='color:#9aa3b2;'>·</span> <span style='color:#9aa3b2;'>·</span>"
                "    "
                "<span style='color:#9aa3b2;'>·</span> <span style='color:#111;'>●</span> "
                "<span style='color:#9aa3b2;'>·</span> <span style='color:#9aa3b2;'>·</span>\n"
                "<span style='color:#111;'>●</span> "
                "<span style='color:#ffffff; text-shadow: 0 0 1px #3f4755; border: 1px solid #6b7485; border-radius: 50%; padding: 0 2px;'>○</span> "
                "<span style='color:#a06c2c;'>A</span> <span style='color:#9aa3b2;'>·</span>"
                "  →  "
                "<span style='color:#111;'>●</span> <span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#111;'>●</span> <span style='color:#9aa3b2;'>·</span>\n"
                "<span style='color:#9aa3b2;'>·</span> <span style='color:#111;'>●</span> "
                "<span style='color:#9aa3b2;'>·</span> <span style='color:#9aa3b2;'>·</span>"
                "    "
                "<span style='color:#9aa3b2;'>·</span> <span style='color:#111;'>●</span> "
                "<span style='color:#9aa3b2;'>·</span> <span style='color:#9aa3b2;'>·</span>"
                "</pre>"
                "<div style='margin-top: 6px; font-weight: 600;'>Trắng hết khí nên bị bắt.</div>"
                "</div>",
            ),
        ))

        content_layout.addWidget(_SectionRow(
            _Section(
                "Luật Ko",
                "Tình huống <b>ko</b> xảy ra khi một quân bị bắt và đối thủ có thể bắt lại ngay, "
                "tạo ra vòng lặp vô hạn giữa Đen và Trắng.<br><br>"
                "<b>Ko đơn giản:</b> Bạn không được bắt lại ngay quân vừa bị bắt. "
                "Bạn phải đi chỗ khác trước (đòn 'đe doạ ko'), rồi mới có thể bắt lại ở lượt sau.<br><br>"
                "<b>Siêu Ko theo vị trí:</b> Luật chặt hơn, không cho phép bất kỳ thế cờ nào "
                "lặp lại. Luật này xử lý cả những tình huống ko phức tạp.",
                "#b58ad6",
            ),
            _Illustration(
                "Vòng lặp ko",
                "<div style='color:#c9d1de;'>"
                "<div style='display:flex; justify-content: space-between; font-weight:600;'>"
                "<span>Trước</span><span>Sau khi Đen bắt</span></div>"
                "<pre style='font-family: Consolas; font-size: 13px; line-height: 1.5; margin: 6px 0 0;'>"
                "<span style='color:#9aa3b2;'>·</span> <span style='color:#111;'>●</span> "
                "<span style='color:#ffffff; text-shadow: 0 0 1px #3f4755; border: 1px solid #6b7485; border-radius: 50%; padding: 0 2px;'>○</span> "
                "<span style='color:#9aa3b2;'>·</span>"
                "    "
                "<span style='color:#9aa3b2;'>·</span> <span style='color:#111;'>●</span> "
                "<span style='color:#ffffff; text-shadow: 0 0 1px #3f4755; border: 1px solid #6b7485; border-radius: 50%; padding: 0 2px;'>○</span> "
                "<span style='color:#9aa3b2;'>·</span>\n"
                "<span style='color:#111;'>●</span> "
                "<span style='color:#ffffff; text-shadow: 0 0 1px #3f4755; border: 1px solid #6b7485; border-radius: 50%; padding: 0 2px;'>○</span> "
                "<span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#ffffff; text-shadow: 0 0 1px #3f4755; border: 1px solid #6b7485; border-radius: 50%; padding: 0 2px;'>○</span>"
                "  →  "
                "<span style='color:#111;'>●</span> <span style='color:#9aa3b2;'>·</span> "
                "<span style='color:#111;'>●</span> "
                "<span style='color:#ffffff; text-shadow: 0 0 1px #3f4755; border: 1px solid #6b7485; border-radius: 50%; padding: 0 2px;'>○</span>\n"
                "<span style='color:#9aa3b2;'>·</span> <span style='color:#111;'>●</span> "
                "<span style='color:#ffffff; text-shadow: 0 0 1px #3f4755; border: 1px solid #6b7485; border-radius: 50%; padding: 0 2px;'>○</span> "
                "<span style='color:#9aa3b2;'>·</span>"
                "    "
                "<span style='color:#9aa3b2;'>·</span> <span style='color:#111;'>●</span> "
                "<span style='color:#ffffff; text-shadow: 0 0 1px #3f4755; border: 1px solid #6b7485; border-radius: 50%; padding: 0 2px;'>○</span> "
                "<span style='color:#9aa3b2;'>·</span>"
                "</pre>"
                "<div style='margin-top: 6px; font-weight: 600;'>Trắng không được bắt lại ngay.</div>"
                "</div>",
            ),
        ))

        content_layout.addWidget(_Section(
            "Tự sát",
            "Một <b>nước tự sát</b> là khi bạn đặt quân khiến quân (hoặc nhóm) của bạn "
            "hết khí mà không bắt được quân đối thủ.<br><br>"
            "Mặc định, tự sát <b>bị cấm</b>. Một số luật cho phép — "
            "bạn có thể bật/tắt trong phần cài đặt.",
            "#e3779a",
        ))

        content_layout.addWidget(_SectionRow(
            _Section(
                "Bỏ lượt và kết thúc ván",
                "Đen hoặc Trắng có thể <b>bỏ lượt</b> thay vì đặt quân. "
                "Khi cả hai bên bỏ lượt liên tiếp, ván sẽ chuyển sang "
                "<b>Chế độ tính điểm</b>.<br><br>"
                "Trong chế độ tính điểm, hai bên thống nhất quân nào là 'chết' "
                "(sẽ bị bắt chắc chắn). Nhấn vào nhóm quân để đánh dấu sống/chết, "
                "sau đó xác nhận để tính điểm cuối.",
                "#75bfa6",
            ),
            _Illustration(
                "Chuỗi lượt",
                "<div style='font-family: \"Segoe UI\"; font-size: 12px;'>"
                "<span style='color:#1b1b1b;'>●</span> Đen đi &nbsp;→&nbsp; "
                "<span style='color:#ffffff; text-shadow: 0 0 1px #3f4755; border: 1px solid #6b7485; border-radius: 50%; padding: 0 2px;'>○</span> Trắng đi "
                "&nbsp;→&nbsp; <b>Bỏ lượt</b> × 2<br><br>"
                "<span style='color:#7b8393;'>Ván chuyển sang tính điểm.</span>"
                "</div>",
            ),
        ))

        content_layout.addWidget(_SectionRow(
            _Section(
                "Tính điểm: Luật Nhật Bản (Tính đất)",
                "Theo luật Nhật Bản, điểm của bạn gồm:<br><br>"
                "<table style='color:#c9d1de;'>"
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
                "Nửa điểm (0.5) của komi giúp tránh hòa. "
                "Đen và Trắng đều cộng phần điểm của mình theo cách trên.",
                "#d9b05c",
            ),
            _Illustration(
                "Ví dụ tính điểm Nhật",
                "<div style='font-family: \"Consolas\"; font-size: 12px;'>"
                "<b>Komi:</b> 3.5 (Trắng)<br>"
                "<span style='color:#1b1b1b;'>●</span> Đen: 20 đất + 4 bắt = 24.0<br>"
                "<span style='color:#ffffff; text-shadow: 0 0 1px #3f4755; border: 1px solid #6b7485; border-radius: 50%; padding: 0 2px;'>○</span> "
                "Trắng: 18 đất + 2 bắt + 3.5 = 23.5<br><br>"
                "<b>Đen thắng 0.5</b>"
                "</div>",
            ),
        ))

        content_layout.addWidget(_SectionRow(
            _Section(
                "Tính điểm: Luật Trung Quốc (Tính diện tích)",
                "Theo luật Trung Quốc, điểm của bạn gồm:<br><br>"
                "<table style='color:#c9d1de;'>"
                "<tr><td style='padding-right:20px;'><b>Quân trên bàn</b></td>"
                "<td>Số quân còn lại của bạn trên bàn</td></tr>"
                "<tr><td><b>+ Đất</b></td>"
                "<td>Các giao điểm trống được bao quanh bởi quân của bạn</td></tr>"
                "<tr><td><b>+ Komi</b></td>"
                "<td>Trắng nhận komi</td></tr>"
                "</table><br>"
                "Lưu ý: Bắt quân KHÔNG được tính riêng trong luật Trung Quốc, "
                "vì quân bị bắt sẽ làm giảm số quân trên bàn của đối thủ. "
                "Đen và Trắng đều cộng điểm theo cách này.",
                "#6aa9e0",
            ),
            _Illustration(
                "Ví dụ tính điểm Trung Quốc",
                "<div style='font-family: \"Consolas\"; font-size: 12px;'>"
                "<b>Komi:</b> 3.5 (Trắng)<br>"
                "<span style='color:#1b1b1b;'>●</span> Đen: 30 quân + 10 đất = 40.0<br>"
                "<span style='color:#ffffff; text-shadow: 0 0 1px #3f4755; border: 1px solid #6b7485; border-radius: 50%; padding: 0 2px;'>○</span> "
                "Trắng: 25 quân + 12 đất + 3.5 = 40.5<br><br>"
                "<b>Trắng thắng 0.5</b>"
                "</div>",
            ),
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

        content_layout.addSpacing(theme.SECTION_SPACING)

        scroll.setWidget(content)
        outer.addWidget(scroll)

    # -- background painting ------------------------------------------------

    def paintEvent(self, event) -> None:  # type: ignore[override]
        p = QPainter(self)
        w, h = self.width(), self.height()
        grad = QLinearGradient(0, 0, w, h)
        grad.setColorAt(0.0, theme.BACKGROUND_GRADIENT_START)
        grad.setColorAt(1.0, theme.BACKGROUND_GRADIENT_MID)
        p.fillRect(self.rect(), grad)
        p.end()
