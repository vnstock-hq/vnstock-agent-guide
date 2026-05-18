# Hướng Dẫn Nâng Cấp WebSocket Streaming Data (Migration Guide)

Tài liệu này cung cấp hướng dẫn nâng cấp (migration) dành cho người dùng đang sử dụng thư viện `vnstock_pipeline` phiên bản cũ từ 2.2.1 trở về trước, nhằm chuyển đổi sang cấu trúc dữ liệu mới tương thích với `vnstock_data` UI và chuẩn quốc tế (FIX/Bloomberg-aligned).

---

## 1. Mục Tiêu Nâng Cấp

Cấu trúc dữ liệu trả về từ WebSocket feed trước đây (Legacy) có một số hạn chế về tính đồng nhất (naming conventions). Bản nâng cấp này giải quyết:
- Đồng nhất tất cả các key về dạng `snake_case` chuẩn.
- Loại bỏ các field viết tắt khó hiểu, chuẩn hóa hậu tố giá (`_price`), khối lượng (`_volume`) và giá trị (`_value`).
- Sổ lệnh (Board) được gộp tự động và phân loại mức giá theo bên Mua (`bid`) và Bán (`ask`).
- Đảm bảo tương thích hoàn toàn 100% với lớp giao diện `vnstock_data` và các agent phân tích tự động.

---

## 2. Các Thay Đổi Chính (Changelog)

### A. Naming Parameters cho Processors
Hai Data Processor chính là `CSVProcessor` và `DuckDBProcessor` nay hỗ trợ thêm tham số `naming`.
Tham số này xác định định dạng schema dữ liệu đầu ra:
- `naming="legacy"` (Mặc định): Giữ nguyên định dạng cũ, đảm bảo **100% backward compatibility** cho code đang chạy của bạn.
- `naming="standard"`: Áp dụng định dạng schema tiêu chuẩn mới.

### B. StandardizedProcessor Wrapper
Giới thiệu class `StandardizedProcessor`. Đây là một wrapper (lớp bọc) linh hoạt cho phép biến đổi dữ liệu sang chuẩn mới trước khi đưa vào bất kỳ Data Processor hiện có nào.

### C. Logic Chuẩn Hóa Sổ Lệnh (Order Book)
Các sự kiện Sổ lệnh (`board`, `boardps`) giờ đây được tách biệt tự động:
- Thay vì `price_1` + `side=B`, dữ liệu sẽ được ánh xạ thành `bid_price_1`.
- Thay vì `volume_2` + `side=S`, dữ liệu sẽ được ánh xạ thành `ask_vol_2`.
- Lược bỏ các trường cờ báo dư thừa như `flag_N` hay `event_type`.

---

## 3. Lộ Trình Nâng Cấp (Migration Path)

Chúng tôi thiết kế lộ trình nâng cấp để không làm gián đoạn trải nghiệm của người dùng. Tùy thuộc vào nhu cầu, bạn có thể chọn 1 trong các tùy chọn sau:

### Tùy Chọn 0: Giữ Nguyên Hiện Trạng (Không Cần Sửa Code)
Bạn không cần thay đổi bất kỳ dòng code nào. Hệ thống mặc định tiếp tục lưu trữ theo cấu trúc cũ.
```python
from vnstock_pipeline.stream import CSVProcessor
# Code cũ vẫn hoạt động hoàn hảo, mặc định là naming="legacy"
client.add_processor(CSVProcessor("data/{event_type}_%Y-%m-%d.csv"))
```

### Tùy Chọn 1: Sử dụng Wrapper (Khuyến Nghị cho Custom Processors)
Nếu bạn đang dùng một Processor tự viết (Custom Processor) hoặc không muốn thay đổi tham số khởi tạo của Processor hiện tại, hãy dùng `StandardizedProcessor` để bọc nó lại.
```python
from vnstock_pipeline.stream import StandardizedProcessor, CSVProcessor

# 1. Khởi tạo processor như cũ
csv = CSVProcessor("data/{event_type}_%Y-%m-%d.csv")

# 2. Bọc processor bằng StandardizedProcessor
client.add_processor(StandardizedProcessor(csv))
```

### Tùy Chọn 2: Sử Dụng Naming Parameter (Tối Ưu Nhất)
Đây là cách ngắn gọn và chính thức để sử dụng chuẩn mới. Chỉ cần truyền thêm `naming="standard"` khi khởi tạo `CSVProcessor` hoặc `DuckDBProcessor`.
```python
from vnstock_pipeline.stream import CSVProcessor

# Truyền thêm tham số naming
client.add_processor(CSVProcessor(
    "data/{event_type}_%Y-%m-%d.csv",
    naming="standard"  # Kích hoạt output chuẩn FIX/Bloomberg
))
```

---

## 4. Kiểm Tra Sau Khi Nâng Cấp

Sau khi chuyển đổi sang `naming="standard"`, bạn cần cập nhật các script đọc/xử lý dữ liệu CSV hoặc DuckDB của mình để khớp với tên cột mới.

**Ví dụ một số thay đổi thường gặp:**
- Thay vì đọc cột `timestamp`, hãy đọc cột `time`.
- Thay vì đọc `last_price` và `last_volume`, hãy dùng `price` và `volume`.
- Thay vì đọc `stock_id`, hãy dùng `id`.
- Với sổ lệnh cổ phiếu, sử dụng thẳng `bid_price_1`, `ask_price_1` thay vì phải tự lọc giá trị theo cột `side` và `price_1`.

Để tham khảo chi tiết toàn bộ các field bị thay đổi trong từng Event Type, vui lòng xem tài liệu:
👉 **[Standard Schema Reference](./07-streaming-data-schemas.md)**
