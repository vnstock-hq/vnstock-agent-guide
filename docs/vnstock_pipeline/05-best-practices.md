# Kinh Nghiệm Thực Tiễn (Best Practices)

## Giới Thiệu

Tài liệu này tổng hợp các kinh nghiệm quan trọng để tối ưu hóa hiệu suất (Performance), triển khai (Deployment) và gỡ lỗi (Troubleshooting) khi vận hành `vnstock_pipeline` trong môi trường triển khai thực tế. 

---

## I. Tối Ưu Hiệu Suất Tải Dữ Liệu (Performance Optimization)

Để tăng tốc độ tải dữ liệu cho hàng ngàn mã cổ phiếu mà không bị chặn (Rate Limit), bạn cần cấu hình `Scheduler` hợp lý thay vì chạy vòng lặp tuần tự.

### Cấu hình `Scheduler` Tiêu Chuẩn

```python
from vnstock_pipeline.core.scheduler import Scheduler

scheduler = Scheduler(
    fetcher, validator, transformer, exporter,
    max_workers=3,          # Số luồng chạy song song
    request_delay=0.5,      # Thời gian nghỉ giữa mỗi request (giây)
    rate_limit_wait=30.0,   # Thời gian chờ nếu bị chặn Rate Limit (giây)
    retry_attempts=3        # Số lần thử lại tối đa
)
```

**Khuyến nghị theo quy mô dữ liệu**:

- **Danh mục nhỏ (< 50 mã)**: `max_workers=5`, `request_delay=0.2`.
- **Danh mục lớn (VN100, HNX30)**: `max_workers=3`, `request_delay=0.5`.
- **Toàn thị trường (1000+ mã)**: Chạy theo Batch, `max_workers=2`, `request_delay=1.0`. Tránh nhồi toàn bộ danh sách vào một lần chạy.

> [!WARNING]
>
> Đừng đặt `max_workers` quá cao (ví dụ: > 10) nếu bạn không sử dụng proxy, vì hệ thống nguồn sẽ ngay lập tức chặn địa chỉ IP của bạn.

---

## II. Triển Khai Lịch Trình Tự Động (Deployment & Scheduling)

Hệ thống Pipeline cần được tự động hóa chạy hằng ngày sau giờ giao dịch. Bạn có thể dùng thư viện `schedule` kết hợp với Docker để triển khai.

### Thiết lập Lịch Trình (Cron/Schedule)

```python
import schedule
import time
import logging

logging.basicConfig(level=logging.INFO)

def run_daily_pipeline():
    logging.info("Bắt đầu cập nhật dữ liệu EOD...")
    # Khởi tạo và chạy Scheduler tại đây
    # scheduler.run(tickers)
    logging.info("Hoàn tất cập nhật.")

# Lên lịch chạy vào 15:30 chiều mỗi ngày (Sau giờ đóng cửa chứng khoán VN)
schedule.every().day.at("15:30").do(run_daily_pipeline)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
```

> [!TIP]
>
> Bọc ứng dụng của bạn bằng Docker Container và chạy nền bằng `docker-compose` để đảm bảo hệ thống tự khởi động lại khi Server reboot.

---

## III. Gỡ Lỗi & Xử Lý Sự Cố (Troubleshooting)

| Vấn Đề Gặp Phải                       | Nguyên Nhân Phổ Biến                        | Giải Pháp Khắc Phục                                             |
| ------------------------------------- | ------------------------------------------- | --------------------------------------------------------------- |
| **Lỗi Timeout liên tục**              | Mạng không ổn định hoặc API nguồn quá tải.  | Tăng `retry_attempts=5` và cấu hình `backoff_factor=2.0`.       |
| **HTTP 429 Too Many Requests**        | Tần suất gọi API quá cao.                   | Giảm `max_workers`, tăng `request_delay` (VD: > 1.0 giây).      |
| **Out of Memory (OOM)**               | Xử lý mảng dữ liệu quá lớn cùng lúc.        | Chia danh sách mã chứng khoán thành nhiều batch (100 mã/batch). |
| **Dữ liệu trả về bị rỗng**            | Nguồn dữ liệu (Source) gặp sự cố mạng tĩnh. | Áp dụng Mẫu Dự phòng Đa Nguồn (Multi-Source Fallback) ở Bài 03. |
| **Lỗi cấp quyền (Permission Denied)** | Thiếu quyền ghi file hoặc Database.         | Kiểm tra quyền (chmod) thư mục `/data` và đường dẫn tuyệt đối.  |

---

## IV. Tiện Ích Kiểm Tra Dữ Liệu Nhanh (Data Inspection CLI)

Khi vận hành hệ thống, việc kiểm tra nhanh dữ liệu đầu ra (file Parquet, CSV) trên môi trường Server CLI là rất cần thiết. `vnstock_pipeline` cung cấp sẵn công cụ kiểm tra (CLI Tool) để không phải viết code Pandas đọc file thủ công.

**Cú pháp chung:**

```bash
python -m vnstock_pipeline.cli <command> <file_path> [options]
```

**Các lệnh hỗ trợ:**

1. **Xem tổng quan thông tin file (Inspect)**
   Cung cấp cấu trúc schema, số lượng dòng/cột, dung lượng file, bộ nhớ sử dụng, khoảng thời gian (date range), và 5 dòng dữ liệu mẫu đầu tiên.

   ```bash
   python -m vnstock_pipeline.cli inspect data/ohlcv/ACB.parquet
   ```
1. **Xem dữ liệu mẫu (Head / Tail)**
   Xem N dòng đầu hoặc cuối của file (mặc định 10 dòng).

   ```bash
   python -m vnstock_pipeline.cli head data/ohlcv/ACB.csv --rows 20
   python -m vnstock_pipeline.cli tail data/ohlcv/ACB.parquet --rows 5
   ```
1. **Xem thống kê mô tả (Stats)**
   Thống kê mô tả (Count, Mean, Std, Min, Max) và tỷ lệ lấp đầy (phát hiện các cột chứa giá trị `NaN`), rất hữu ích để audit chất lượng dữ liệu.

   ```bash
   python -m vnstock_pipeline.cli stats data/ohlcv/ACB.parquet
   ```
1. **Truy vấn nhanh theo điều kiện (Query)**
   Hỗ trợ lọc/truy vấn trực tiếp bằng biểu thức SQL (tốc độ xử lý cực nhanh trên định dạng Parquet nhờ DuckDB).

   ```bash
   python -m vnstock_pipeline.cli query data/ohlcv/ACB.parquet "close > 50"
   ```
1. **Xem cấu trúc Schema**
   Chỉ hiển thị danh sách tên cột, kiểu dữ liệu, số dòng và tỷ lệ điền dữ liệu (fill rate).

   ```bash
   python -m vnstock_pipeline.cli schema data/ohlcv/ACB.parquet
   ```