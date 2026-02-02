"""
Tutorial / How-to-Play screen.

A scrollable guide explaining Go rules, capturing, ko, and scoring
for both Japanese and Chinese rulesets.
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, Signal, QUrl
from PySide6.QtGui import QLinearGradient, QPainter, QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
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
        lbl_title.setFont(theme.font_bold(16))
        lbl_title.setStyleSheet(f"color: {accent_color};")
        layout.addWidget(lbl_title)

        lbl_body = QLabel(body)
        lbl_body.setFont(theme.font_normal(13))
        lbl_body.setWordWrap(True)
        lbl_body.setStyleSheet("color: #c9d1de; line-height: 1.5;")
        lbl_body.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(lbl_body)


# ---------------------------------------------------------------------------
# Illustration widgets
# ---------------------------------------------------------------------------

class _RemoteImage(QLabel):
    """Loads a remote image and scales it to fit the card width."""

    def __init__(
        self,
        image_url: str,
        alt_text: str,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._image_url = image_url
        self._alt_text = alt_text
        self._pixmap: Optional[QPixmap] = None
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumHeight(160)
        self.setWordWrap(True)
        self.setStyleSheet(
            "QLabel { background-color: #1f2430; border-radius: 8px; padding: 6px; }"
            "QLabel { color: #9aa3b2; font-size: 12px; }"
        )
        self.setText(f"{alt_text}\n(đang tải hình...)")

        self._network = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(self._image_url))
        request.setRawHeader(b"User-Agent", b"Covay-Go-Guide/1.0")
        reply = self._network.get(request)
        reply.finished.connect(lambda: self._handle_reply(reply))

    def _handle_reply(self, reply) -> None:
        if reply.error():
            self.setText(f"{self._alt_text}\n(Không tải được hình.)")
            reply.deleteLater()
            return

        data = reply.readAll()
        pixmap = QPixmap()
        if not pixmap.loadFromData(data):
            self.setText(f"{self._alt_text}\n(Không đọc được hình.)")
            reply.deleteLater()
            return

        self._pixmap = pixmap
        self._update_scaled_pixmap()
        reply.deleteLater()

    def _update_scaled_pixmap(self) -> None:
        if not self._pixmap:
            return
        target_width = max(1, self.width() - 12)
        scaled = self._pixmap.scaledToWidth(
            target_width,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(scaled)

    def resizeEvent(self, event) -> None:  # type: ignore[override]
        super().resizeEvent(event)
        if self._pixmap:
            self._update_scaled_pixmap()


class _Illustration(QFrame):
    """Visual card with a title, remote image, and caption."""

    def __init__(
        self,
        title: str,
        image_url: str,
        caption: str,
        parent: Optional[QWidget] = None,
    ) -> None:
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
        lbl_title.setFont(theme.font_bold(13))
        lbl_title.setStyleSheet("color: #b8c0cf;")
        layout.addWidget(lbl_title)

        img = _RemoteImage(image_url, title)
        layout.addWidget(img)

        lbl_caption = QLabel(caption)
        lbl_caption.setTextFormat(Qt.TextFormat.RichText)
        lbl_caption.setStyleSheet("color: #c9d1de; line-height: 1.5; font-size: 13px;")
        lbl_caption.setWordWrap(True)
        layout.addWidget(lbl_caption)


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
        # Image sources from Wikimedia Commons (verified working URLs)
        image_sources = {
            "stones": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Go_stones_on_goban.jpg",
            "liberties": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Go_Stone_Liberties.svg",
            "capture": "https://upload.wikimedia.org/wikipedia/commons/5/5d/Go_capture.svg",
            "ko": "https://upload.wikimedia.org/wikipedia/commons/6/63/Ko_%28go%29.svg",
            "suicide": "https://upload.wikimedia.org/wikipedia/commons/4/40/Go_adjacent_stones.svg",
            "turns": "https://upload.wikimedia.org/wikipedia/commons/2/21/Go_board_19x19.png",
            "japanese_scoring": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Go_scoring_territory.svg",
            "chinese_scoring": "https://upload.wikimedia.org/wikipedia/commons/7/7a/Go_scoring_area.svg",
        }

        content_layout.addWidget(_SectionRow(
            _Section(
                "Cờ Vây là gì?",
                "Cờ Vây (còn gọi là <b>Weiqi</b> ở Trung Quốc, <b>Baduk</b> ở Hàn Quốc, "
                "<b>Go</b> ở Nhật Bản) là trò chơi chiến thuật dành cho hai người.<br><br>"
                "Trò chơi có nguồn gốc từ Trung Quốc cách đây hơn <b>4.000 năm</b> "
                "và là một trong những trò chơi cổ nhất vẫn còn được chơi đến nay.<br><br>"
                "Mục tiêu: <b>kiểm soát nhiều đất hơn</b> đối thủ bằng cách "
                "đặt quân lên các giao điểm của bàn cờ và bao vây lãnh thổ.",
            ),
            _Illustration(
                "Bàn cờ và quân cờ",
                image_sources["stones"],
                "Bàn cờ Vây truyền thống (Goban) với quân <b>Đen</b> và <b>Trắng</b>.",
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
                image_sources["liberties"],
                "Các điểm được đánh dấu là <b>khí</b> của quân cờ (trên, dưới, trái, phải).",
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
                image_sources["capture"],
                "Khi đặt quân lấp hết khí cuối cùng, quân đối thủ bị <b>bắt</b> và loại khỏi bàn.",
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
                "Tình huống Ko",
                image_sources["ko"],
                "Sau khi bắt 1 quân, đối thủ <b>không được bắt lại ngay</b> — phải đi chỗ khác trước.",
            ),
        ))

        content_layout.addWidget(_SectionRow(
            _Section(
                "Tự sát",
                "Một <b>nước tự sát</b> là khi bạn đặt quân khiến quân (hoặc nhóm) của bạn "
                "hết khí mà không bắt được quân đối thủ.<br><br>"
                "<b>Ví dụ:</b> Nếu Trắng bị bao vây bởi Đen và chỉ còn một ô trống bên trong, "
                "Đen không thể đặt quân vào ô đó (vì sẽ tự hết khí ngay lập tức).<br><br>"
                "<b>Ngoại lệ:</b> Nếu nước đi đó bắt được quân đối thủ, thì KHÔNG phải tự sát — "
                "quân đối thủ bị bắt trước, tạo khí cho quân vừa đặt.<br><br>"
                "Mặc định, tự sát <b>bị cấm</b>. Một số luật (như New Zealand, Ing) cho phép — "
                "bạn có thể bật/tắt trong phần cài đặt.",
                "#e3779a",
            ),
            _Illustration(
                "Ví dụ tự sát",
                image_sources["suicide"],
                "Nước đi được đánh dấu X là <b>tự sát</b> — quân đặt vào sẽ hết khí ngay.",
            ),
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
                "Ván cờ kết thúc",
                image_sources["turns"],
                "Ván cờ kết thúc khi cả hai bên <b>bỏ lượt liên tiếp</b> — bắt đầu tính điểm.",
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
                "Tính điểm Nhật Bản",
                image_sources["japanese_scoring"],
                "Điểm = <b>Đất bao vây</b> + Quân bắt được + Komi (cho Trắng).",
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
                "Tính điểm Trung Quốc",
                image_sources["chinese_scoring"],
                "Điểm = <b>Quân trên bàn</b> + Đất bao vây + Komi (cho Trắng).",
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
