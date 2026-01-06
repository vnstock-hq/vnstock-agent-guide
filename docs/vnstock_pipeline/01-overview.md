# Vnstock Pipeline - Thư Viện Xử Lý Dữ Liệu Pipeline

## Giới Thiệu

`vnstock_pipeline` là thư viện Python cung cấp một framework mạnh mẽ và linh hoạt để xây dựng các **quy trình xử lý dữ liệu** từ việc lấy (fetch), xác thực (validate), chuyển đổi (transform) cho đến xuất (export) dữ liệu thị trường chứng khoán Việt Nam. Thư viện được thiết kế theo kiến trúc **modular** (dạng plugin), cho phép bạn dễ dàng tùy biến hoặc mở rộng mà không cần sửa mã nguồn cốt lõi.

### Đặc Điểm Chính

- **Kiến trúc Modular**: Các thành phần (Fetcher, Validator, Transformer, Exporter) độc lập và có thể thay thế
- **Mẫu Tác Vụ**: Hàm sẵn sàng sử dụng cho các loại dữ liệu phổ biến (OHLCV, Financial, Intraday, Price Board)
- **Lập Lịch Linh Hoạt**: Scheduler tự động xử lý song song cho danh sách mã
- **Xử Lý Lỗi**: Logic thử lại, ghi nhật ký lỗi và báo cáo chi tiết
- **Streaming Thời Gian Thực**: Hỗ trợ WebSocket streaming dữ liệu với độ trễ thấp quy mô toàn thị trường mà không gặp giới hạn tốc độ API như kết nối thông qua REST API thông thường
- **Tùy Chọn Xuất**: CSV, DuckDB, Parquet, v.v.
- **Khả Năng Mở Rộng**: Dễ dàng thêm Fetcher, Processor hoặc Exporter tùy chỉnh

### Tại Sao Dùng Vnstock Pipeline?

1. **Tiết Kiệm Thời Gian**: Sẵn sàng sử dụng cho các tác vụ phổ biến
2. **Khả Năng Chịu Lỗi**: Tự động thử lại và xử lý lỗi
3. **Khả Năng Mở Rộng**: Xử lý song song cho 1600+ mã
4. **Tính Linh Hoạt**: Dễ tùy biến mà không cần tác động nhiều vào mã nguồn
5. **Sẵn Sàng Sản Xuất**: Ghi nhật ký, giám sát, báo cáo

---

## Cấu Trúc Package

```
vnstock_pipeline/
├── __init__.py
├── core/                    # Các class cốt lõi
│   ├── fetcher.py          # Base Fetcher class
│   ├── validator.py        # Base Validator class
│   ├── transformer.py      # Base Transformer class
│   ├── exporter.py         # Base Exporter class
│   ├── scheduler.py        # Scheduler để chạy pipeline
│   ├── data_manager.py     # Quản lý bộ nhớ đệm dữ liệu
│   └── flexible_exporter.py # Tùy chọn xuất linh hoạt
├── template/                # Các mẫu triển khai
│   └── vnstock.py          # VNFetcher, VNValidator, VNTransformer
├── tasks/                   # Các tác vụ có sẵn
│   ├── ohlcv.py           # Dữ liệu OHLCV hàng ngày
│   ├── financial.py        # Báo cáo tài chính
│   ├── intraday.py        # Dữ liệu trong phiên
│   └── price_board.py      # Dữ liệu bảng giá
├── schemas/                 # Schemas/xác thực dữ liệu
├── stream/                  # Streaming thời gian thực
│   ├── client.py           # WSSClient cho WebSocket
│   ├── processors.py       # Bộ xử lý dữ liệu
│   ├── processors_advanced.py
│   └── sources/            # Nguồn dữ liệu
├── utils/                   # Tiện ích
│   ├── logger.py           # Thiết lập ghi nhật ký
│   ├── env.py              # Cấu hình môi trường
│   ├── deduplication.py    # Loại bỏ trùng lặp
│   └── market_hours.py     # Thông tin giờ giao dịch
└── __pycache__/
```

---

## Quy Trình Cơ Bản (Luồng Xử Lý Dữ Liệu)

```
Dữ liệu thô
    │
    ▼
[Fetcher] ─► Lấy dữ liệu từ API/DB
    │
    ▼
[Validator] ─► Kiểm tra dữ liệu hợp lệ
    │
    ▼
[Transformer] ─► Chuyển đổi/làm sạch dữ liệu
    │
    ▼
[Exporter] ─► Lưu vào CSV/DB/Parquet
    │
    ▼
Dữ liệu có cấu trúc
```

**Scheduler** điều phối quá trình trên cho danh sách mã:
- Xử lý song song nếu mã > 10
- Tự động thử lại khi có lỗi
- Ghi nhật ký chi tiết
- Báo cáo tiến trình

---

## Các Loại Tác Vụ

### 1. OHLCV (Open, High, Low, Close, Volume) - Giá Hàng Ngày

**Mục đích**: Lấy dữ liệu OHLCV lịch sử cho danh sách mã

**Lớp chính**:
- `OHLCVDailyFetcher`: Lấy dữ liệu từ `vnstock_data.explorer.vci.Quote`
- `OHLCVDailyValidator`: Kiểm tra có đủ cột (time, open, high, low, close, volume)
- `OHLCVDailyTransformer`: Xóa trùng lặp, định dạng datetime
- `CSVExport`: Xuất ra CSV

**Kết quả**:
```
Columns: time, open, high, low, close, volume
Ví dụ:
        time   open   high    low  close   volume
0 2024-11-01  62.42  63.02  62.09  62.09  1732251
1 2024-11-02  62.09  62.92  61.95  62.42   892151
```

**Ví dụ**:
```python
from vnstock_pipeline.tasks.ohlcv import run_task

tickers = ['VCB', 'ACB', 'HPG']
run_task(tickers, start="2024-01-01", end="2024-12-02", interval="1D")
# Kết quả: ./data/ohlcv/VCB.csv, ./data/ohlcv/ACB.csv, ...
```

### 2. Financial - Báo Cáo Tài Chính

**Mục đích**: Lấy báo cáo tài chính (BCTC, KQKD, LCTT, Tỉ số)

**Loại báo cáo**:
- `balance_sheet`: Cân đối kế toán (94 cột)
- `income_statement_year`: KQKD năm (28 cột)
- `income_statement_quarter`: KQKD quý (28 cột)
- `cash_flow`: Lưu chuyển tiền tệ (56 cột)
- `ratio`: Tỉ số tài chính (58 cột)

**Kết quả**: Lưu riêng các báo cáo
```
./data/financial/VCB_balance_sheet.csv
./data/financial/VCB_income_statement_year.csv
./data/financial/VCB_cash_flow.csv
...
```

**Ví dụ**:
```python
from vnstock_pipeline.tasks.financial import run_financial_task

tickers = ['VCB', 'ACB']
run_financial_task(
    tickers,
    balance_sheet_period="year",
    income_statement_year_period="year",
    lang="vi",
    dropna=True
)
```

### 3. Intraday - Dữ Liệu Trong Phiên

**Mục đích**: Lấy dữ liệu giao dịch trong phiên (1 phút, 5 phút, 15 phút, 1 giờ)

**Kết quả**: Tương tự OHLCV nhưng với khung thời gian nhỏ hơn

### 4. Price Board - Bảng Giá Thời Gian Thực

**Mục đích**: Lấy thông tin giá trực tiếp

**Chế độ**:
- `eod`: Lấy một lần cuối ngày (End Of Day)
- `live`: Cập nhật liên tục trong phiên giao dịch

**Ví dụ**:
```python
from vnstock_pipeline.tasks.price_board import run_price_board

tickers = ['VCB', 'ACB', 'HPG']
run_price_board(tickers, interval=60, mode="eod")  # Cập nhật mỗi 60 giây
```

---

## Cách Sử Dụng Chi Tiết

### Cấp độ 1: Sử Dụng Tác Vụ Có Sẵn (Đơn Giản)

```python
from vnstock_pipeline.tasks.ohlcv import run_task

# Lấy OHLCV cho 3 mã
tickers = ['VCB', 'ACB', 'HPG']
run_task(
    tickers,
    start="2024-01-01",
    end="2024-12-02",
    interval="1D"
)
# Kết quả: ./data/ohlcv/VCB.csv, etc.
```

**Ưu điểm**:
- ✅ Nhanh, không cần cấu hình
- ✅ Tất cả xử lý tự động

**Nhược điểm**:
- ❌ Cấu hình cố định
- ❌ Khó tùy biến

### Cấp độ 2: Tùy Biến Với Scheduler (Trung Bình)

```python
from vnstock_pipeline.core.scheduler import Scheduler
from vnstock_pipeline.tasks.ohlcv import OHLCVDailyFetcher, OHLCVDailyValidator, OHLCVDailyTransformer
from vnstock_pipeline.core.exporter import CSVExport

tickers = ['VCB', 'ACB', 'HPG']

# Tạo các thành phần
fetcher = OHLCVDailyFetcher()
validator = OHLCVDailyValidator()
transformer = OHLCVDailyTransformer()
exporter = CSVExport(base_path="./my_data/ohlcv")

# Tạo scheduler
scheduler = Scheduler(
    fetcher,
    validator,
    transformer,
    exporter,
    retry_attempts=3,
    backoff_factor=2.0,
    max_workers=3,           # (v2.1.5) Số luồng xử lý song song
    request_delay=0.5,       # (v2.1.5) Delay giữa requests (giây)
    rate_limit_wait=35.0     # (v2.1.5) Thời gian chờ khi gặp rate limit (giây)
)

# Chạy
scheduler.run(
    tickers,
    fetcher_kwargs={"start": "2024-01-01", "end": "2024-12-02"}
)

# Hoặc override tại thời điểm chạy
scheduler.run(
    tickers,
    fetcher_kwargs={"start": "2024-01-01", "end": "2024-12-02"},
    max_workers=5,           # Override scheduler config
    request_delay=0.3,
    rate_limit_wait=40.0
)
```

**Ưu điểm**:
- ✅ Kiểm soát chi tiết
- ✅ Có thể cấu hình từng thành phần

**Nhược điểm**:
- ❌ Mã phức tạp hơn

### Cấp độ 3: Tạo Tác Vụ Tùy Chỉnh (Nâng Cao)

```python
from vnstock_pipeline.template.vnstock import VNFetcher, VNValidator, VNTransformer
from vnstock_pipeline.core.scheduler import Scheduler
from vnstock_pipeline.core.exporter import Exporter
import pandas as pd

# 1. Fetcher tùy chỉnh
class MyCustomFetcher(VNFetcher):
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        # Lấy dữ liệu từ API/DB riêng
        from vnstock_data import Quote
        quote = Quote(source="vci", symbol=ticker)
        df = quote.history(start="2024-01-01", end="2024-12-02", interval="1D")
        # Thêm cột tùy chỉnh
        df['source'] = 'custom'
        return df

# 2. Validator tùy chỉnh
class MyCustomValidator(VNValidator):
    required_columns = ["time", "close", "source"]

    def validate(self, data: pd.DataFrame) -> bool:
        if not super().validate(data):
            return False
        # Thêm logic kiểm tra tùy chỉnh
        if (data['close'] < 0).any():
            return False
        return True

# 3. Transformer tùy chỉnh
class MyCustomTransformer(VNTransformer):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(data)
        # Thêm cột tính toán
        df['change_pct'] = df['close'].pct_change() * 100
        return df

# 4. Exporter tùy chỉnh
class MyCustomExporter(Exporter):
    def export(self, data, ticker: str, **kwargs):
        # Lưu vào DB hoặc webhook
        print(f"Đang xuất {ticker} với {len(data)} dòng")
        data.to_csv(f"./data/{ticker}.csv", index=False)

# 5. Chạy
tickers = ['VCB', 'ACB']
scheduler = Scheduler(
    MyCustomFetcher(),
    MyCustomValidator(),
    MyCustomTransformer(),
    MyCustomExporter()
)
scheduler.run(tickers)
```

---

## Scheduler - Điều Phối Xử Lý

### Tính Năng Chính

```python
scheduler = Scheduler(
    fetcher,
    validator,
    transformer,
    exporter,
    retry_attempts=3,        # Thử lại 3 lần nếu lỗi
    backoff_factor=2.0       # Chờ 2s, 4s, 8s giữa các lần thử
)
```

### Xử Lý Song Song

- **Nếu mã ≤ 10**: Xử lý tuần tự
- **Nếu mã > 10**: Xử lý song song với ThreadPoolExecutor + báo cáo tiến trình

### Báo Cáo & Ghi Nhật Ký

```
Đang xử lý 100 mã...
[████████████████████] 100/100 [00:45<00:00, 2.22 mã/s]

=== Báo Cáo ===
Tổng số mã: 100
Thành công: 98
Thất bại: 2
Thời gian: 45.2 giây
Tốc độ: 2.22 mã/giây

Lỗi được lưu tại: ./data/errors.csv
```

---

## Ví Dụ Hoàn Chỉnh

### Ví Dụ 1: Lấy OHLCV cho VN30

```python
from vnstock_pipeline.tasks.ohlcv import run_task
from vnstock import Vnstock

# Lấy danh sách VN30
stock = Vnstock().stock(symbol="VCB", source="VCI")
vn30 = stock.listing.symbols_by_group("VN30").tolist()

print(f"Đang lấy dữ liệu cho {len(vn30)} cổ phiếu VN30...")

# Chạy tác vụ
run_task(
    vn30,
    start="2023-01-01",
    end="2024-12-02",
    interval="1D"
)

print(f"✅ Hoàn thành! Kiểm tra tại ./data/ohlcv/")
```

### Ví Dụ 2: Lấy Báo Cáo Tài Chính

```python
from vnstock_pipeline.tasks.financial import run_financial_task
from vnstock import Vnstock

# Lấy VN100
stock = Vnstock().stock(symbol="VCB", source="VCI")
vn100 = stock.listing.symbols_by_group("VN100").tolist()

# Lấy dữ liệu tài chính
run_financial_task(
    vn100,
    balance_sheet_period="year",
    income_statement_year_period="year",
    income_statement_quarter_period="quarter",
    cash_flow_period="year",
    ratio_period="year",
    lang="vi",
    dropna=True
)

print(f"✅ Hoàn thành! Kiểm tra tại ./data/financial/")
```

### Ví Dụ 3: Pipeline Tùy Chỉnh (OHLCV + Xử Lý Tùy Chỉnh)

```python
from vnstock_pipeline.core.scheduler import Scheduler
from vnstock_pipeline.tasks.ohlcv import OHLCVDailyFetcher, OHLCVDailyValidator, OHLCVDailyTransformer
from vnstock_pipeline.core.exporter import Exporter
import pandas as pd
import os

# Transformer tùy chỉnh: Thêm moving average
class EnrichedTransformer(OHLCVDailyTransformer):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(data)
        # Thêm SMA20, SMA50
        df['sma20'] = df['close'].rolling(20).mean()
        df['sma50'] = df['close'].rolling(50).mean()
        return df

# Exporter tùy chỉnh: Lưu CSV + Parquet
class DualExporter(Exporter):
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
        os.makedirs(f"{base_path}/parquet", exist_ok=True)

    def export(self, data, ticker: str, **kwargs):
        # CSV
        csv_path = os.path.join(self.base_path, f"{ticker}.csv")
        data.to_csv(csv_path, index=False)

        # Parquet
        parquet_path = os.path.join(self.base_path, "parquet", f"{ticker}.parquet")
        data.to_parquet(parquet_path, index=False)

        print(f"✅ {ticker}: Đã lưu vào CSV và Parquet")

    def preview(self, ticker: str, n: int = 5, **kwargs):
        csv_path = os.path.join(self.base_path, f"{ticker}.csv")
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path).head(n)
        return None

# Chạy
tickers = ['VCB', 'ACB', 'HPG']
scheduler = Scheduler(
    OHLCVDailyFetcher(),
    OHLCVDailyValidator(),
    EnrichedTransformer(),
    DualExporter("./enriched_data")
)

scheduler.run(
    tickers,
    fetcher_kwargs={
        "start": "2024-01-01",
        "end": "2024-12-02"
    }
)
```

---

## Streaming Thời Gian Thực (Nâng Cao)

### Streaming WebSocket từ VPS

```python
from vnstock_pipeline.stream import WSSClient

async def main():
    client = WSSClient()

    # Subscribe đến các mã
    client.subscribe_symbols(['VCB', 'ACB', 'HPG'])

    # Thêm bộ xử lý để xử lý dữ liệu thời gian thực
    from vnstock_pipeline.stream.processors import CSVProcessor
    client.add_processor(CSVProcessor("./realtime_data.csv"))

    # Kết nối
    await client.connect()

# Chạy
import asyncio
asyncio.run(main())
```

---

## Lưu Ý Quan Trọng

### 1. Index vs Regular Columns

Một số exporter yêu cầu index:
```python
# ❌ Sai: Index là range
df.to_csv("data.csv")  # DataFrame với RangeIndex

# ✅ Đúng: Không có index
df.to_csv("data.csv", index=False)
```

### 2. Xử Lý DateTime

```python
# ❌ Sai: Chuỗi ngày
df['time'] = "2024-01-01"

# ✅ Đúng: pd.Timestamp hoặc datetime
df['time'] = pd.to_datetime("2024-01-01")
```

### 3. Xử Lý Lỗi

```python
# ❌ Sai: Bỏ qua lỗi im lặng
try:
    data = fetch_data()
except:
    pass

# ✅ Đúng: Ghi nhật ký và thử lại
try:
    data = fetch_data()
except Exception as e:
    logger.error(f"Lấy dữ liệu thất bại: {e}")
    # Logic thử lại
```

---

## Tối Ưu Hóa Hiệu Suất

### 1. Xử Lý Song Song

```python
# Tự động: nếu > 10 mã
scheduler.run(100_tickers)  # Tự động song song

# Thủ công: Điều chỉnh số worker
scheduler.max_workers = 20
```

### 2. Bộ Nhớ Đệm

```python
from vnstock_pipeline.core.data_manager import DataManager

manager = DataManager(cache_dir="./cache")
data = manager.get_or_fetch(ticker, fetch_func)
```

### 3. Xử Lý Theo Lô

```python
# Lấy dữ liệu theo lô 50 mã
tickers = ['VCB', 'ACB', ...] * 50

scheduler.run(tickers[0:50])
scheduler.run(tickers[50:100])
scheduler.run(tickers[100:150])
```

---

## Khắc Phục Sự Cố

### Lỗi: "Index must be DatetimeIndex"

```python
# ❌ Sai
df.index

# ✅ Đúng
df = df.set_index('time')
df.index = pd.to_datetime(df.index)
```

### Lỗi: "Missing required columns"

```python
# Kiểm tra các cột bắt buộc
print(df.columns)

# Thêm nếu thiếu
if 'volume' not in df.columns:
    df['volume'] = 0
```

### Lỗi: "Connection refused"

```python
# Kiểm tra kết nối internet
# Kiểm tra API endpoint có khả dụng không
# Thử lại nếu tạm thời
```

---

## Tài Liệu Tham Khảo

- **Vnstock**: https://vnstocks.com/
- **Pandas**: https://pandas.pydata.org/
- **Async**: https://docs.python.org/3/library/asyncio.html
