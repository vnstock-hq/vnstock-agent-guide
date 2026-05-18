# Vnstock Pipeline - Dữ Liệu Thời Gian Thực (Streaming)

## Giới Thiệu

Chương này giới thiệu tổng quan tính năng **real-time streaming** của `vnstock_pipeline` nhằm:
- Nhận cập nhật giá thời gian thực từ WebSocket mà không phải gọi API liên tục gây nghẽn kết nối.
- Quản lý phiên giao dịch tự động (ví dụ: nghỉ trưa, kết nối lại).
- Tự động phân giải các mã phái sinh sang định dạng chuẩn KRX.
- Xử lý dữ liệu luồng (in-stream) mạnh mẽ qua kiến trúc Processors.

> [!IMPORTANT]
> **Yêu cầu gói tài trợ (Sponsor)**
> Gói `vnstock_pipeline` (bao gồm tính năng streaming) chỉ dành riêng cho người dùng tham gia tài trợ hệ sinh thái mức **Golden** hoặc **Diamond**.

---

## 🎁 Tải Bộ Code Mẫu Độc Quyền

Vì Streaming là một tính năng phức tạp đòi hỏi tổ chức mã nguồn tốt, tài liệu này đi kèm với một bộ mã nguồn minh họa (**Streaming Examples**) rất chi tiết. **Bộ code này không được chia sẻ công khai trên GitHub.**

> [!TIP]
> **Tải bộ code mẫu:** Vui lòng đăng nhập vào tài khoản trên Vnstocks và truy cập link sau:
> [Tải xuống tại mục Exclusive Files](https://vnstocks.com/account?section=packages&tab=exclusive-files)
>
> Tải file ZIP về máy, giải nén. Toàn bộ kịch bản được nhắc đến dưới đây đều nằm trong thư mục giải nén này.

---

### Cấu Trúc Thư Mục Bộ Mã Nguồn (`streaming_examples`)

Sau khi giải nén, bộ mã nguồn sẽ có cấu trúc như sau:

```text
streaming_examples/
├── 01_basic/
│   ├── 01_console_streaming.py         # Kết nối WSSClient và in giá ra Terminal
│   └── 02_custom_processor.py          # Hướng dẫn tạo Processor xử lý logic riêng
├── 02_redis_pubsub/
│   ├── 01_publisher.py                 # Nhận dữ liệu WSS và đẩy (publish) vào Redis
│   └── 02_consumer.py                  # Chạy độc lập, lấy dữ liệu từ Redis xử lý
├── 03_websocket_relay/
│   └── 01_relay_server.py              # Server trung chuyển WebSocket cục bộ
├── 04_advanced_use_cases/
│   ├── 01_rsi_alert.py                 # Tính RSI real-time bằng vnstock_ta
│   ├── 02_macd_crossover.py            # Bắt tín hiệu giao cắt MACD thời gian thực
│   ├── 03_volume_spike.py              # Theo dõi khối lượng đột biến
│   └── 04_discord_webhook_alert.py     # Đẩy tín hiệu cảnh báo lên nhóm Discord
└── docs/
    ├── streaming_guide.md              # Hướng dẫn chi tiết
    └── streaming_use_cases.md          # Các phân tích kịch bản ứng dụng
```

---

## Các Kịch Bản Sử Dụng Khuyến Nghị

Thay vì tự viết lại toàn bộ boilerplate code, hãy trực tiếp sử dụng các script đã đóng gói sẵn trong thư mục `streaming_examples`.

### I. Streaming Cơ Bản (`01_basic`)

Dành cho người mới làm quen với luồng dữ liệu WebSocket:
- **`01_console_streaming.py`**: Trình diễn cách kết nối `WSSClient`, đăng ký các mã cổ phiếu/phái sinh (như `VN30F1M`), và theo dõi dữ liệu trả về liên tục (tick-by-tick).
- **`02_custom_processor.py`**: Minh họa cách kế thừa class `DataProcessor` của Vnstock, cho phép bạn tự định nghĩa logic lọc (filter) hoặc lưu trữ dữ liệu (lưu CSV, DuckDB) khi có tín hiệu mới đến.

### II. Xây Dựng Hệ Thống Phân Tán với Redis (`02_redis_pubsub`)

Với hệ thống giao dịch tự động, việc tách biệt luồng kết nối mạng và luồng tính toán là bắt buộc để tránh trễ gói tin.
- **`01_publisher.py`**: Thiết lập một `RedisPubSubProcessor`. Nhiệm vụ duy nhất của nó là nhận dữ liệu thô và đẩy (broadcast) vào bộ nhớ Redis.
- **`02_consumer.py`**: Có thể chạy nhiều tiến trình consumer cùng lúc trên các máy khác nhau để tính toán các logic phức tạp.

> [!NOTE]
> Bạn cần khởi chạy Redis Server trước (VD bằng Docker: `docker run -p 6379:6379 -d redis`) và cài đặt thư viện `pip install redis` để sử dụng cụm kịch bản này.

### III. Hệ Thống Trung Chuyển Nội Bộ (`03_websocket_relay`)

Dành cho hệ thống muốn phát triển Dashboard trên nền tảng Web Frontend (React/Vue) hoặc ứng dụng Mobile. Script **`01_relay_server.py`** sẽ nhận dữ liệu từ máy chủ Vnstock và mở một cổng WebSocket cục bộ, cho phép hàng trăm client nội bộ khác kết nối vào mà không ảnh hưởng giới hạn kết nối của tài khoản chính.

### IV. Giao Dịch Thuật Toán & Cảnh Báo (`04_advanced_use_cases`)

Đây là nhóm kịch bản mạnh mẽ nhất, kết hợp sức mạnh của `vnstock_pipeline` và thư viện phân tích kỹ thuật `vnstock_ta`:
- **Quét đột biến**: Các file `01_rsi_alert.py`, `02_macd_crossover.py`, và `03_volume_spike.py` chứa logic cấu trúc bộ đệm giá (Buffer Queue) để tính toán các tín hiệu mua/bán trong thời gian thực.
- **Gửi thông báo**: Script `04_discord_webhook_alert.py` hướng dẫn cách bọc các lời gọi mạng (network calls) vào các `asyncio.Task` phi đồng bộ, giúp bạn gửi tin nhắn cảnh báo lên kênh Discord mà không làm nghẽn luồng đọc giá chính.

---

## Lưu Ý Quan Trọng Khi Phát Triển Hệ Thống Streaming

1. **Khống Chế Bộ Nhớ (Memory Management)**: Khi tính toán chỉ báo kỹ thuật thời gian thực, luôn sử dụng các cấu trúc dữ liệu có giới hạn vòng (như `collections.deque(maxlen=N)` trong Python). Tuyệt đối không dùng mảng List tiêu chuẩn, vì điều này sẽ gây tràn bộ nhớ RAM (OOM) sau nhiều giờ chạy liên tục trên VPS.
2. **Luồng Không Đợi (Non-blocking I/O)**: Mọi tác vụ tốn thời gian như ghi vào Database ổ cứng hay gọi API mạng Webhook bên trong hàm `process()` đều phải được thực thi dưới dạng Async Tasks (`asyncio.create_task()`). Việc để block luồng thực thi chính dù chỉ vài phần mười giây cũng có thể khiến WSSClient rớt kết nối.
