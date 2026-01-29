# Tổng quan chức năng, ứng dụng của game Cờ Vây

Tài liệu này mô tả chi tiết các chức năng chính, ứng dụng/giá trị sử dụng của game, các luật được hỗ trợ (ví dụ: Luật Nhật Bản), cùng ý tưởng thiết kế UI.

## 1) Mục tiêu & ứng dụng

Game Cờ Vây trong dự án này được thiết kế để:

- **Giải trí**: cho phép người chơi đánh Cờ Vây trực tiếp trên máy tính.
- **Học tập**: cung cấp các chế độ luật, scoring, và hiển thị lịch sử nước đi để học chiến thuật.
- **Thực hành luật**: mô phỏng các luật phổ biến (Nhật Bản, Trung Quốc), ko, suicide, và scoring mode chuẩn.

## 2) Danh sách chức năng chính

### 2.1 Chơi ván mới
- Chọn kích thước bàn (9×9, 13×13, 19×19).
- Chọn luật chơi (Nhật Bản / Trung Quốc).
- Thiết lập komi.
- Chọn luật Ko (Ko đơn giản / Siêu Ko theo vị trí).
- Cho phép hoặc không cho phép nước đi tự sát.

### 2.2 Đặt quân & luật hợp lệ
- Click lên bàn để đặt quân ở giao điểm hợp lệ.
- Tự động bắt quân khi nhóm hết khí.
- Chặn nước đi vi phạm Ko hoặc tự sát (nếu không cho phép).

### 2.3 Bỏ lượt & kết thúc ván
- Cho phép người chơi bỏ lượt.
- Khi hai lượt liên tiếp bỏ, game vào chế độ tính điểm (Scoring Mode).

### 2.4 Chế độ tính điểm (Scoring Mode)
- Người chơi đánh dấu các nhóm quân chết.
- Hệ thống tính điểm theo luật đã chọn.
- Hiển thị bảng kết quả chi tiết, gồm: đất, quân, bắt quân, komi.

### 2.5 Undo/Redo
- Hoàn tác hoặc làm lại nhiều bước nhờ hệ thống snapshot.

### 2.6 Lưu/Tải ván
- Lưu ván chơi dưới dạng JSON (gồm toàn bộ lịch sử và trạng thái).
- Tải ván chơi để tiếp tục hoặc xem lại.

### 2.7 Lịch sử nước đi
- Hiển thị danh sách nước đi theo tọa độ chuẩn (A1, B2…).

### 2.8 Xin thua
- Người chơi có thể xin thua, ván kết thúc ngay.

## 3) Luật chơi được hỗ trợ

### 3.1 Luật Nhật Bản (Territory Scoring)
- **Cách tính điểm:**
  - Điểm = *đất bao quanh* + *số quân bắt* + *komi*.
- **Ý nghĩa:**
  - Ưu tiên việc kiểm soát đất và bắt quân đối thủ.

### 3.2 Luật Trung Quốc (Area Scoring)
- **Cách tính điểm:**
  - Điểm = *số quân trên bàn* + *đất bao quanh* + *komi*.
- **Ý nghĩa:**
  - Mỗi quân còn sống trên bàn đều có giá trị điểm.

### 3.3 Luật Ko
- **Ko đơn giản:**
  - Không được ngay lập tức lặp lại một tình huống bắt quân y hệt ở lượt kế tiếp.
- **Siêu Ko theo vị trí:**
  - Không được lặp lại bất kỳ trạng thái bàn cờ nào đã xuất hiện trước đó.

### 3.4 Luật tự sát (Suicide)
- **Cho phép hoặc không cho phép:**
  - Nếu không cho phép, nước đi tự sát bị chặn.
  - Nếu cho phép, quân có thể tự đặt vào thế không còn khí (ít dùng trong thực tế).

## 4) Thiết kế UI & ý tưởng trải nghiệm

### 4.1 Tư duy thiết kế
- **Đơn giản – rõ ràng – tập trung vào bàn cờ**.
- UI tập trung vào trải nghiệm người chơi, giảm nhiễu.
- Màu sắc ấm áp, dễ nhìn, gợi cảm giác bàn cờ gỗ.

### 4.2 Bố cục UI
- **Khu vực trái:** Bàn cờ lớn chiếm ưu tiên diện tích.
- **Khu vực phải:** Panel thông tin (lượt đi, captures, komi, luật).
- **Dưới panel:** Lịch sử nước đi.
- **Nhóm nút thao tác:** gom chức năng vào các nhóm nút trực quan.

### 4.3 Các yếu tố UI nổi bật
- **Ghost Stone**: hiển thị quân mờ khi hover.
- **Marker nước đi cuối**: đánh dấu nước đi mới nhất.
- **Chế độ Scoring**: overlay hiển thị quân chết và đất được tính điểm.

### 4.4 Màu sắc & phong cách
- **Bàn cờ**: gradient màu gỗ ấm.
- **Quân đen/trắng**: có highlight và shadow nhẹ để tạo chiều sâu.
- **Button**: bo tròn, màu nhạt, hover rõ ràng để tạo cảm giác mềm mại.

## 5) Định hướng mở rộng

- **AI đối thủ**: thêm engine AI để chơi với máy.
- **Chế độ học**: gợi ý nước đi, phân tích chiến thuật.
- **Replay/Review**: phát lại ván và chú thích nước đi.
- **Online Multiplayer**: chơi qua mạng.

---

Tài liệu này giúp nắm nhanh các chức năng, luật hỗ trợ, và tư duy thiết kế UI của game Cờ Vây trong dự án.
