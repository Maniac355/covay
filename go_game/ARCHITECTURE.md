# Sơ đồ khối & workflow của game Cờ Vây

Tài liệu này mô tả kiến trúc tổng thể của dự án, các khối chức năng chính, vai trò của từng khối và luồng xử lý (workflow) giữa các khối.

## 1) Sơ đồ khối tổng quan

```
+------------------+
|      UI Layer    |
| (PySide6 Widgets)|
+--------+---------+
         |
         v
+------------------+
|   GameState API  |
|  (engine/state) |
+--------+---------+
         |
         v
+---------------------------+
|      Engine Layer         |
| board / rules / scoring   |
+--------+---------+---------+
         |         |
         v         v
+----------------+ +----------------+
|   History      | | Serialization  |
| (engine/history)| | (save/load)   |
+----------------+ +----------------+
```

### Ý nghĩa:
- **UI Layer**: Hiển thị giao diện, nhận input người chơi.
- **GameState API**: Cầu nối giữa UI và engine, quản lý trạng thái ván.
- **Engine Layer**: Luật chơi, logic bàn cờ, chấm điểm.
- **History**: Lưu snapshot để undo/redo.
- **Serialization**: Lưu/khôi phục trạng thái ván qua JSON.

## 2) Mô tả chi tiết từng khối

### 2.1 UI Layer (go_game/ui)
**Vai trò:**
- Hiển thị bàn cờ, nút thao tác, lịch sử nước đi, hộp thoại.
- Gửi sự kiện (đặt quân, bỏ lượt, undo/redo, lưu/tải) đến GameState.
- Đồng bộ UI với trạng thái hiện tại của game.

**Khối chính:**
- `main_window.py`: Điều hướng giữa các màn hình (menu, setup, tutorial, game).
- `game_screen.py`: Màn chơi chính, gắn board widget + panel thông tin.
- `board_widget.py`: Vẽ bàn cờ, quân cờ, nhận click/hover.
- `dialogs.py`: Hộp thoại ván mới, cài đặt, kết quả.
- `theme.py`: Quy định màu sắc, font, style tổng thể.

**Chi tiết kỹ thuật:**
- `BoardWidget` xử lý chuyển đổi toạ độ pixel ↔ grid, vẽ lưới, quân, ghost stone.
- `GameScreen` gọi `GameState.play()` hoặc `pass_turn()` để cập nhật game.
- `GameScreen` lắng nghe `stone_placed` và `dead_toggled` để xử lý.

### 2.2 GameState API (go_game/engine/state.py)
**Vai trò:**
- Lớp trung tâm quản lý trạng thái ván (turn, captures, ko, phase, history).
- Cung cấp API thống nhất để UI thao tác.

**Trách nhiệm:**
- **Play/Pass/Resign**: tiếp nhận hành động, gọi Rules để kiểm tra hợp lệ.
- **Undo/Redo**: quản lý snapshot qua `History`.
- **Scoring**: chuyển sang `SCORING` mode sau 2 pass, xác nhận điểm.
- **Serialization**: lưu/tải ván theo JSON.

**Chi tiết kỹ thuật:**
- `play()` gọi `Rules.apply_move()` để xác thực nước đi.
- `pass_turn()` tăng `consecutive_passes`, vào scoring nếu ≥2.
- `toggle_dead_group()` đánh dấu nhóm chết khi ở `SCORING`.

### 2.3 Board (go_game/engine/board.py)
**Vai trò:**
- Đại diện cho bàn cờ: kích thước, grid, các nhóm quân.

**Trách nhiệm:**
- `set/get`: đặt quân hoặc đọc trạng thái giao điểm.
- `neighbors()`: xác định hàng xóm.
- `get_group()`: lấy nhóm liên kết.
- `liberties()`: tính số khí.
- `get_territory()`: tính đất cho scoring.

**Chi tiết kỹ thuật:**
- Dùng flood-fill/DFS để tìm nhóm và khí.
- `position_hash()` hỗ trợ kiểm tra Ko (superko).

### 2.4 Rules (go_game/engine/rules.py)
**Vai trò:**
- Kiểm tra tính hợp lệ của nước đi.

**Trách nhiệm:**
- Xử lý bắt quân, ko, suicide.
- Trả về `MoveResult` (OK, OCCUPIED, KO, SUICIDE).

**Chi tiết kỹ thuật:**
- Tạo board mới nếu nước đi hợp lệ.
- Loại bỏ nhóm bị bắt.
- Kiểm tra ko dựa trên `ko_point` hoặc `position_hashes`.

### 2.5 Scoring (go_game/engine/scoring.py)
**Vai trò:**
- Tính điểm theo luật Nhật Bản hoặc Trung Quốc.

**Trách nhiệm:**
- `compute_score_japanese()` và `compute_score_chinese()`.
- Nhận vào `dead_stones` để loại quân chết.

**Chi tiết kỹ thuật:**
- Nhật: điểm = territory + captures + komi.
- Trung: điểm = stones + territory + komi.

### 2.6 History (go_game/engine/history.py)
**Vai trò:**
- Lưu snapshot trạng thái để undo/redo.

**Trách nhiệm:**
- `push()`: lưu snapshot mới.
- `undo()` / `redo()` trả lại snapshot tương ứng.

**Chi tiết kỹ thuật:**
- Snapshot chứa board copy + turn + captures + ko + move.

### 2.7 Serialization (go_game/engine/state.py)
**Vai trò:**
- Lưu và tải ván chơi dưới JSON.

**Trách nhiệm:**
- `to_dict()` → JSON.
- `from_dict()` → khôi phục state.

**Chi tiết kỹ thuật:**
- Lưu `grid`, `moves`, `captures`, `phase`, `dead_stones`, `final_score`.
- Tải có thể replay moves hoặc dựng lại từ grid nếu thiếu history.

## 3) Workflow chính của game

### 3.1 Luồng khi chơi một nước
1. Người chơi click vào bàn cờ (`BoardWidget`).
2. `GameScreen._on_stone_placed()` gọi `GameState.play(row, col)`.
3. `GameState` gọi `Rules.apply_move()`:
   - Kiểm tra occupied.
   - Kiểm tra capture.
   - Kiểm tra ko / suicide.
4. Nếu hợp lệ, cập nhật board + captures + turn + history.
5. UI cập nhật lại panel và board.

### 3.2 Luồng pass & scoring
1. Người chơi nhấn **Bỏ lượt**.
2. `GameState.pass_turn()` tăng `consecutive_passes`.
3. Nếu đủ 2 pass, `phase = SCORING`.
4. UI chuyển sang chế độ đánh dấu quân chết.

### 3.3 Luồng scoring
1. Người chơi click nhóm để đánh dấu dead.
2. `GameState.toggle_dead_group()` cập nhật `dead_stones`.
3. Khi nhấn **Xác nhận điểm**, gọi `GameState.confirm_score()`.
4. `scoring.py` tính điểm, trả kết quả.
5. UI hiển thị `ScoreDialog`.

### 3.4 Luồng undo/redo
1. Người chơi bấm **Hoàn tác**.
2. `GameState.undo()` lấy snapshot trước.
3. UI cập nhật lại board và thông tin.

### 3.5 Luồng save/load
1. Người chơi bấm **Lưu** → `GameState.save_json()`.
2. Người chơi bấm **Tải** → `GameState.load_json()`.
3. `from_dict()` khôi phục board + metadata.
4. UI cập nhật lại theo state mới.

## 4) Phụ thuộc giữa các khối

- `UI` phụ thuộc vào `GameState` để cập nhật trạng thái.
- `GameState` phụ thuộc vào `Board`, `Rules`, `History`, `Scoring`.
- `Rules` phụ thuộc vào `Board` để xác định nhóm, khí.
- `Scoring` phụ thuộc vào `Board` và trạng thái dead_stones.

## 5) Tổng kết

Kiến trúc được chia tầng rõ ràng:
- **UI** chỉ hiển thị và gửi sự kiện.
- **GameState** là trung tâm điều phối.
- **Engine** đảm nhiệm toàn bộ luật chơi, tính điểm.
- **History/Serialization** hỗ trợ undo/redo và lưu ván.

Cách tách khối này giúp dễ bảo trì, kiểm thử và mở rộng (ví dụ: thêm AI, thêm luật mới).
