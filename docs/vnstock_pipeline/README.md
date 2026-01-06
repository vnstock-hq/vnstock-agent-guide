# Vnstock Pipeline - Hướng Dẫn Toàn Diện

Tài liệu chi tiết về thư viện **vnstock_pipeline** - công cụ xây dựng các đường ống xử lý dữ liệu chứng khoán theo mô hình **Fetcher → Validator → Transformer → Exporter**.

---

## 📑 Mục Lục

### [1. Tổng Quan Kiến Trúc](01-overview.md)
**Giới thiệu & cái nhìn tổng thể**

- 📋 Cấu trúc thư viện & các module
- 🔄 Luồng xử lý dữ liệu
- 📊 Các loại tác vụ sẵn có (OHLCV, Financial, Intraday, Price Board)
- 🎯 3 cấp độ sử dụng (đơn giản, lập lịch, tùy chỉnh)
- 🔧 Các ví dụ hoạt động
- ⚡ Tối ưu hóa & khắc phục sự cố

**Người dùng mới nên bắt đầu từ đây**

---

### [2. Chi Tiết Các Tác Vụ & Công Cụ Xây Dựng](02-tasks-and-builders.md)
**Tham khảo chi tiết về các tác vụ có sẵn**

#### Các Tác Vụ Sẵn Có (Quy Trình Hoàn Chỉnh)
- **OHLCV Daily** - Dữ liệu giá hàng ngày
  - Tham số: start, end, interval
  - Kết quả: DataFrame (22 dòng, 6 cột)
  - Ứng dụng: Phân tích kỹ thuật, kiểm tra chiến lược, huấn luyện mô hình học máy

- **Financial** - Báo cáo tài chính
  - 5 loại báo cáo: Bảng cân đối, Báo cáo thu nhập (năm/quý), Lưu chuyển tiền tệ, Tỷ số tài chính
  - Kết quả: Dictionary chứa 5 DataFrames với 8-94 cột
  - Ứng dụng: Phân tích tài chính, định giá, sàng lọc P/E

- **Intraday** - Dữ liệu trong phiên
  - Khung thời gian: 1m, 5m, 15m, 30m, 1h
  - Kết quả: Tương tự OHLCV nhưng nhiều dòng hơn
  - Ứng dụng: Giao dịch trong ngày, nhận dạng mẫu hình

- **Price Board** - Bảng giá thời gian thực
  - Chế độ: EOD (một lần), Live (cập nhật liên tục)
  - Kết quả: Thông tin giá trực tiếp từ VPS
  - Ứng dụng: Theo dõi danh mục, cảnh báo giá

#### Công Cụ Xây Dựng (Tùy Chỉnh)
- **Custom Fetcher** - Kế thừa từ VNFetcher, triển khai _vn_call()
- **Custom Validator** - Kiểm tra điều kiện kinh doanh
- **Custom Transformer** - Làm giàu dữ liệu với các chỉ báo
- **Custom Exporter** - Xuất vào CSV/Parquet/Database/Webhook

---

### [3. Xây Dựng Pipeline Tùy Chỉnh](03-custom-pipelines.md)
**Hướng dẫn tạo pipeline cho các bài toán thực tế**

#### Các Mẫu Fetcher
- Bộ bọc API đơn giản - Lấy dữ liệu từ API tùy chỉnh
- Dự phòng nhiều nguồn - Thử nhiều nguồn dữ liệu
- Bộ nhớ đệm với thời gian hết hạn - Cache thông minh với TTL

#### Các Mẫu Validator
- Xác thực logic - Kiểm tra logic dữ liệu
- Chấm điểm chất lượng dữ liệu - Tính điểm chất lượng 0-100

#### Các Mẫu Transformer
- **Làm giàu chỉ báo kỹ thuật** - Thêm 20+ chỉ báo kỹ thuật
- **Làm giàu dữ liệu cơ bản** - Kết hợp OHLCV + báo cáo tài chính
- **Chuẩn hóa** - Chuẩn hóa dữ liệu cho học máy

#### Các Mẫu Exporter
- **Xuất đa định dạng** - CSV + Parquet + JSON
- **Xuất vào cơ sở dữ liệu** - SQLite/DuckDB
- **Tích hợp Webhook** - Đẩy vào API từ xa

#### Ví Dụ Sản Phẩm
- Pipeline hoàn chỉnh đã kiểm chứng: Lấy VN100 → Làm giàu → Xuất
- Với xử lý lỗi, ghi nhật ký, kiểm thử

---

### [4. Xử Lý Dữ Liệu Thời Gian Thực](04-streaming.md)
**Nhận & xử lý dữ liệu streaming thời gian thực**

#### Streaming Cơ Bản
- Thiết lập kết nối WebSocket
- Xử lý thông điệp đơn giản
- Chuyển đổi sang DataFrame

#### Các Mẫu Nâng Cao
- **Streaming nhiều mã** - Lắng nghe nhiều mã cùng lúc
- **Chỉ báo thời gian thực** - Tính SMA, RSI, độ biến động trực tiếp
- **Hệ thống cảnh báo** - Cảnh báo khi giá phá ngưỡng, RSI cực đoan
- **Streaming bền vững** - Lưu dữ liệu streaming vào cơ sở dữ liệu

#### Ứng Dụng Hoàn Chỉnh
- Ứng dụng streaming sản xuất: Theo dõi VN30, tính chỉ báo, kích hoạt cảnh báo
- Khả năng kết nối lại, giới hạn tốc độ

---

### [5. Phương Pháp Tốt Nhất & Tối Ưu Hóa](05-best-practices.md)
**Hướng dẫn cho triển khai sản xuất**

#### Hiệu Suất
- Lấy dữ liệu song song (50+ workers)
- Xử lý theo lô (100 mã/lô)
- Bộ nhớ đệm tích cực (TTL 24h)
- Tối ưu hóa kiểu dữ liệu (giảm 75% bộ nhớ)
- Vector hóa (nhanh hơn 100 lần)

#### Xử Lý Lỗi
- Các mẫu try-catch toàn diện
- Xác thực ở mỗi bước
- Thử lại với lùi theo hàm mũ
- Ghi nhật ký lỗi vào CSV

#### Kiểm Thử
- Kiểm thử đơn vị (fetcher, validator, transformer, exporter)
- Kiểm thử tích hợp (đầu-cuối)
- Kiểm thử tải (10000+ dòng)

#### Triển Khai
- Container hóa Docker
- Lập lịch pipeline (hàng ngày lúc 16:30)
- Giám sát & kiểm tra sức khỏe
- Hướng dẫn khắc phục sự cố

#### Scheduler Configuration (v2.1.5)
- Tối ưu hóa max_workers, request_delay, rate_limit_wait
- Xử lý batch lớn (500+ tickers)
- Tránh rate limit hiệu quả

---

### [6. Tối Ưu Hóa Scheduler (v2.1.5)](06-scheduler-tuning.md)
**Hướng dẫn tối ưu hóa hiệu suất & xử lý rate limiting**

#### Các Tham Số Scheduler
- **max_workers** - Số luồng xử lý song song (1-10)
- **request_delay** - Độ trễ giữa requests (0.1-2.0s)
- **rate_limit_wait** - Thời gian chờ khi rate limit (30-120s)

#### Chiến Lược Cấu Hình
- Ít dữ liệu (< 50 tickers): `max_workers=3, request_delay=0.5, rate_limit_wait=35`
- Nhiều dữ liệu (100-300): `max_workers=2, request_delay=1.0, rate_limit_wait=40`
- Rất nhiều (500+): `max_workers=1, request_delay=2.0, rate_limit_wait=120`
- Tối ưu tốc độ: `max_workers=8, request_delay=0.1, rate_limit_wait=30`

#### Các Tính Năng Khác
- Xử lý batch lớn (500+ tickers)
- Override tham số tại runtime
- Debug & monitoring
- Troubleshooting rate limit & timeout

**Quan trọng cho tất cả users xử lý dữ liệu lớn**

---

### [5. Phương Pháp Tốt Nhất & Tối Ưu Hóa](05-best-practices.md)
**Hướng dẫn cho triển khai sản xuất**

#### Hiệu Suất
- Lấy dữ liệu song song (50+ workers)
- Xử lý theo lô (100 mã/lô)
- Bộ nhớ đệm tích cực (TTL 24h)
- Tối ưu hóa kiểu dữ liệu (giảm 75% bộ nhớ)
- Vector hóa (nhanh hơn 100 lần)

#### Xử Lý Lỗi
- Các mẫu try-catch toàn diện
- Xác thực ở mỗi bước
- Thử lại với lùi theo hàm mũ
- Ghi nhật ký lỗi vào CSV

#### Kiểm Thử
- Kiểm thử đơn vị (fetcher, validator, transformer, exporter)
- Kiểm thử tích hợp (đầu-cuối)
- Kiểm thử tải (10000+ dòng)

#### Triển Khai
- Container hóa Docker
- Lập lịch pipeline (hàng ngày lúc 16:30)
- Giám sát & kiểm tra sức khỏe
- Hướng dẫn khắc phục sự cố

---

## 🚀 Bắt Đầu Nhanh

### Cài Đặt

```bash
pip install vnstock>=3.2.0
```

### Cách Sử Dụng Cơ Bản (3 dòng)

```python
from vnstock_pipeline.tasks.ohlcv import run_task

run_task(['VCB', 'ACB', 'HPG'], start="2024-01-01", end="2024-12-02")
print("✅ Dữ liệu đã lưu vào ./data/ohlcv/")
```

### Cấu Trúc Kết Quả

```
./data/ohlcv/
├── VCB.csv  (22 dòng × 6 cột: time, open, high, low, close, volume)
├── ACB.csv
└── HPG.csv
```

---

## 📊 Tổng Quan Kiến Trúc

```
┌─────────────────────────────────────────────────────────┐
│                    LUỒNG PIPELINE                        │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Đầu vào (Danh sách mã)                                  │
│      ↓                                                    │
│  ┌──────────────────────────────────────────────────┐   │
│  │ FETCHER (Lấy dữ liệu từ nguồn)                   │   │
│  │ - VCI Quote API                                   │   │
│  │ - Bộ bọc API tùy chỉnh                            │   │
│  │ - Dự phòng nhiều nguồn                            │   │
│  └──────────────────────────────────────────────────┘   │
│      ↓                                                    │
│  ┌──────────────────────────────────────────────────┐   │
│  │ VALIDATOR (Kiểm tra chất lượng dữ liệu)          │   │
│  │ - Các cột bắt buộc                                │   │
│  │ - Logic OHLC                                      │   │
│  │ - Quy tắc kinh doanh                              │   │
│  └──────────────────────────────────────────────────┘   │
│      ↓                                                    │
│  ┌──────────────────────────────────────────────────┐   │
│  │ TRANSFORMER (Xử lý & làm giàu dữ liệu)           │   │
│  │ - Làm sạch & loại trùng lặp                       │   │
│  │ - Chỉ báo kỹ thuật (SMA, RSI, MACD)               │   │
│  │ - Các cột phái sinh                               │   │
│  └──────────────────────────────────────────────────┘   │
│      ↓                                                    │
│  ┌──────────────────────────────────────────────────┐   │
│  │ EXPORTER (Lưu dữ liệu)                           │   │
│  │ - CSV / Parquet                                   │   │
│  │ - SQLite / DuckDB                                 │   │
│  │ - Webhook API                                     │   │
│  └──────────────────────────────────────────────────┘   │
│      ↓                                                    │
│  Đầu ra (Tệp / Cơ sở dữ liệu)                           │
│                                                           │
└─────────────────────────────────────────────────────────┘

SCHEDULER (Điều phối)
- Xử lý song song (ThreadPoolExecutor)
- Logic thử lại (lùi theo hàm mũ)
- Theo dõi tiến trình (tqdm)
- Báo cáo lỗi
```

---

## 🎯 Các Khái Niệm Chính

### 1. Fetcher
**Lấy dữ liệu từ nguồn (API, cơ sở dữ liệu, tệp)**

```python
class VNFetcher(ABC):
    @abc.abstractmethod
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        """Ghi đè phương thức này để lấy dữ liệu"""
        pass
```

Kết quả: `pd.DataFrame` với các cột tùy loại dữ liệu

---

### 2. Validator
**Kiểm tra chất lượng & tính đầy đủ của dữ liệu**

```python
class VNValidator(ABC):
    required_columns = [...]  # Định nghĩa các cột bắt buộc

    def validate(self, data: pd.DataFrame) -> bool:
        """Trả về True nếu dữ liệu hợp lệ"""
        pass
```

Kết quả: `bool` (đạt/không đạt)

---

### 3. Transformer
**Chuyển đổi, làm sạch, làm giàu dữ liệu**

```python
class VNTransformer(ABC):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        - Loại bỏ trùng lặp
        - Chuyển đổi kiểu dữ liệu
        - Thêm các chỉ báo
        - Sắp xếp theo thời gian
        """
        pass
```

Kết quả: `pd.DataFrame` (đã làm giàu)

---

### 4. Exporter
**Lưu dữ liệu vào các định dạng khác nhau**

```python
class Exporter(ABC):
    def export(self, data: pd.DataFrame, ticker: str, **kwargs):
        """Lưu dữ liệu - CSV, cơ sở dữ liệu, API, v.v."""
        pass
```

Kết quả: Tệp / Bản ghi cơ sở dữ liệu

---

### 5. Scheduler
**Điều phối Fetcher → Validator → Transformer → Exporter**

```python
scheduler = Scheduler(
    fetcher, validator, transformer, exporter,
    max_workers=50,        # Số workers song song
    retry_attempts=3,      # Số lần thử lại
    backoff_factor=2.0     # Hệ số lùi theo hàm mũ
)

scheduler.run(['VCB', 'ACB', 'HPG', ...])
```

Tính năng:
- ✅ Xử lý song song cho 10+ mã
- ✅ Tự động thử lại với lùi theo hàm mũ
- ✅ Thanh tiến trình (tqdm)
- ✅ Báo cáo lỗi vào CSV
- ✅ Ghi nhật ký chi tiết

---

## 📈 Thông Số Hiệu Suất

| Thao tác | Thời gian | Bộ nhớ |
|-----------|------|--------|
| Lấy 1 OHLCV | 1-2s | ~1MB |
| Lấy 50 OHLCV (song song) | 2-5s | ~50MB |
| Lấy 50 OHLCV (tuần tự) | 50-100s | ~50MB |
| Chuyển đổi 1000 dòng | <100ms | ~5MB |
| Xuất 50 CSV | <1s | ~10MB |
| **Tổng (VN100)** | **~3-5 phút** | **~500MB** |

**Mẹo tối ưu hóa:**
- Sử dụng `SmartCachedFetcher` để tránh lấy lại dữ liệu
- Xử lý theo lô 50-100 mã
- Sử dụng 20-50 workers (tùy giới hạn API)
- Tối ưu hóa kiểu dữ liệu (giảm 75% bộ nhớ)
- Sử dụng các thao tác vector hóa (nhanh hơn 100 lần)

---

## 💡 Các Trường Hợp Sử Dụng Phổ Biến

### Trường Hợp 1: Thu Thập Dữ Liệu Hàng Ngày

```python
# Lấy dữ liệu VN100 hàng ngày lúc 16:30
import schedule

def daily_collection():
    scheduler = Scheduler(...)
    vn100 = get_vn100_tickers()
    scheduler.run(vn100)

schedule.every().day.at("16:30").do(daily_collection)
```

👉 Xem: [01-overview.md](01-overview.md#example-simple-task-with-scheduler)

---

### Trường Hợp 2: Pipeline Phân Tích Kỹ Thuật

```python
# Lấy OHLCV + tính 20+ chỉ báo + xuất
transformer = TAEnrichedTransformer()  # Thêm SMA, RSI, MACD, BBands, ATR, OBV, v.v.
scheduler = Scheduler(fetcher, validator, transformer, exporter)
scheduler.run(['VCB', 'ACB', ...])
```

👉 Xem: [03-custom-pipelines.md](03-custom-pipelines.md#pattern-1-technical-indicators-enrichment)

---

### Trường Hợp 3: Phân Tích Tài Chính

```python
# Lấy bảng cân đối + báo cáo thu nhập + tỷ số
from vnstock_pipeline.tasks.financial import run_financial_task

run_financial_task(
    ['VCB', 'ACB', 'HPG'],
    balance_sheet_period="year",
    income_statement_year_period="year",
    income_statement_quarter_period="quarter"
)
```

👉 Xem: [02-tasks-and-builders.md](02-tasks-and-builders.md#task-2-financial---báo-cáo-tài-chính)

---

### Trường Hợp 4: Theo Dõi Thời Gian Thực

```python
# Theo dõi giá VN30, tính RSI, kích hoạt cảnh báo
streamer = MultiSymbolStreamer(['VCB', 'ACB', 'HPG', ...])
alert_mgr = StreamAlertManager()
alert_mgr.add_rsi_alert("VCB", 70, "above")  # Quá mua
alert_mgr.add_price_alert("VCB", 65, "above")  # Ngưỡng giá

asyncio.run(streamer.start_all(url))
```

👉 Xem: [04-streaming.md](04-streaming.md#pattern-2-real-time-indicators)

---

## 🔧 Hướng Dẫn Tham Chiếu API Nhanh

### Scheduler

```python
scheduler = Scheduler(
    fetcher,              # Đối tượng VNFetcher
    validator,            # Đối tượng VNValidator
    transformer,          # Đối tượng VNTransformer
    exporter,             # Đối tượng Exporter
    max_workers=20,       # Số workers song song
    retry_attempts=3,     # Số lần thử lại
    backoff_factor=2.0    # Hệ số lùi theo hàm mũ
)

scheduler.run(
    tickers=['VCB', 'ACB'],
    fetcher_kwargs={
        "start": "2024-01-01",
        "end": "2024-12-02",
        "interval": "1D"
    }
)
```

### Tác Vụ OHLCV

```python
from vnstock_pipeline.tasks.ohlcv import run_task

run_task(
    tickers=['VCB', 'ACB', 'HPG'],
    start="2024-01-01",
    end="2024-12-02",
    interval="1D"  # 1D, 1W, 1M, 1h, 5m, 15m, 30m
)
```

### Tác Vụ Tài Chính

```python
from vnstock_pipeline.tasks.financial import run_financial_task

run_financial_task(
    tickers=['VCB', 'ACB'],
    balance_sheet_period="year",       # "year" hoặc "quarter"
    income_statement_year_period="year",
    income_statement_quarter_period="quarter",
    cash_flow_period="year",
    ratio_period="year",
    lang="vi",                          # "vi" hoặc "en"
    dropna=True                         # Loại bỏ các dòng có NaN
)
```

---

## 🧪 Kiểm Thử & Xác Thực

### Chạy Kiểm Thử Đơn Vị

```python
import unittest

# Kiểm thử fetcher
class TestFetcher(unittest.TestCase):
    def test_fetch_vcb(self):
        fetcher = SmartCachedFetcher()
        df = fetcher._vn_call("VCB")
        self.assertGreater(len(df), 0)

# Kiểm thử validator
class TestValidator(unittest.TestCase):
    def test_reject_empty(self):
        validator = StrictValidator()
        self.assertFalse(validator.validate(pd.DataFrame()))

# Chạy
if __name__ == '__main__':
    unittest.main()
```

👉 Xem: [05-best-practices.md](05-best-practices.md#iii-testing)

---

## 📚 Cấu Trúc Tài Liệu

```
docs/vnstock_pipeline/
├── 01-overview.md              ← Bắt đầu từ đây (Tổng quan)
├── 02-tasks-and-builders.md    ← Tham chiếu tác vụ & ví dụ
├── 03-custom-pipelines.md      ← Các mẫu nâng cao
├── 04-streaming.md             ← Dữ liệu thời gian thực
├── 05-best-practices.md        ← Hiệu suất & triển khai
├── README.md                   ← Tệp này (Điều hướng nhanh)
└── examples/
    ├── simple/
    ├── builder/
    └── streaming/
```

---

## 🎓 Lộ Trình Học Tập

**Cấp độ 1 - Người mới bắt đầu** (30 phút)
1. Đọc: [01-overview.md](01-overview.md) - Hiểu kiến trúc & luồng xử lý
2. Thử: `run_task(['VCB'], start="2024-01-01", end="2024-12-02")`
3. Kiểm tra: Xem tệp CSV đầu ra

**Cấp độ 2 - Trung cấp** (1 giờ)
1. Đọc: [02-tasks-and-builders.md](02-tasks-and-builders.md) - Chi tiết 4 tác vụ
2. Thử: Xây dựng fetcher, validator, transformer tùy chỉnh
3. Thực hành: Xử lý các mã VN100 với Scheduler

**Cấp độ 3 - Nâng cao** (2 giờ)
1. Đọc: [03-custom-pipelines.md](03-custom-pipelines.md) - Các mẫu sản xuất
2. Thử: Làm giàu tài chính, dự phòng nhiều nguồn
3. Xây dựng: Pipeline hoàn chỉnh với các chỉ báo

**Cấp độ 4 - Chuyên gia** (2+ giờ)
1. Đọc: [04-streaming.md](04-streaming.md) & [05-best-practices.md](05-best-practices.md)
2. Thử: Theo dõi thời gian thực với cảnh báo
3. Triển khai: Container Docker, lập lịch pipeline
4. Giám sát: Kiểm tra sức khỏe, xử lý lỗi

---

## ❓ Câu Hỏi Thường Gặp

**H: Có cần phải triển khai tất cả 4 thành phần (Fetcher, Validator, Transformer, Exporter) không?**

Đ: Không! Có thể sử dụng `run_task()` cho các tác vụ có sẵn (OHLCV, Financial), hoặc chỉ ghi đè các thành phần cần thiết.

---

**H: Làm thế nào để tăng tốc độ lấy dữ liệu?**

Đ:
1. Sử dụng `SmartCachedFetcher` (bộ nhớ đệm 24h)
2. Tăng `max_workers` (ví dụ: 50)
3. Xử lý theo lô (100 mã/lô)
4. Xác nhận giới hạn API (qps, max_concurrent)

---

**H: Nên sử dụng máy chủ nào để chạy pipeline?**

Đ:
- **Cục bộ**: Máy tính cá nhân (tốc độ tùy cấu hình)
- **Đám mây**: AWS/GCP/Azure VMs (có thể mở rộng)
- **Docker**: Container hóa (di động & tái tạo được)
- **Lập lịch**: Cron + systemd (máy chủ Linux)

---

**H: Làm thế nào để xuất vào cơ sở dữ liệu thay vì CSV?**

Đ: Sử dụng Exporter tùy chỉnh:
```python
from vnstock_pipeline.core.exporter import Exporter

class DatabaseExporter(Exporter):
    def export(self, data, ticker, **kwargs):
        # Ghi vào SQLite/PostgreSQL/v.v.
        pass
```

👉 Xem: [03-custom-pipelines.md](03-custom-pipelines.md#pattern-2-database-export)

---

**H: Có hỗ trợ streaming thời gian thực không?**

Đ: Có! Sử dụng streaming WebSocket:
```python
streamer = MultiSymbolStreamer(['VCB', 'ACB', ...])
asyncio.run(streamer.start_all("wss://stream.example.com"))
```

👉 Xem: [04-streaming.md](04-streaming.md)

---

## 📞 Hỗ Trợ & Đóng Góp

- 📖 Tài liệu: Tham khảo các tệp .md
- 🐛 Vấn đề: Báo cáo qua GitHub
- 💬 Thảo luận: Thảo luận qua GitHub Discussions
- 📝 Đóng góp: Gửi pull request

---

## 📝 Giấy Phép

vnstock_pipeline là một phần của hệ sinh thái Vnstock.

---

## 🔗 Tài Liệu Liên Quan

- **vnstock_data**: [Tài liệu vnstock_data](../../vnstock-data/)
- **vnstock_ta**: [Tài liệu vnstock_ta](../vnstock-ta/)
- **vnstock_news**: [Tài liệu vnstock_news](../vnstock-news/)

---

**Cập nhật lần cuối**: Tháng 12 năm 2024
**Phiên bản**: 1.0
