# Vnstock Pipeline - Chi Tiết Tasks & Builders

## Giới Thiệu

Chương này cung cấp chi tiết về các **tasks** (quy trình sẵn có) và **builders** (cách xây dựng custom pipeline) trong vnstock_pipeline. Tasks là các quy trình hoàn chỉnh lấy → xác thực → chuyển đổi → xuất dữ liệu, còn Builders là công cụ để tạo custom pipeline.

---

## I. TASKS (Quy Trình Sẵn Có)

### Task 1: OHLCV - Dữ Liệu Giá Hàng Ngày

**Mô tả**: Lấy dữ liệu OHLCV (mở, cao, thấp, đóng, khối lượng) lịch sử cho danh sách mã chứng khoán.

**Các lớp**:
- `OHLCVDailyFetcher`: Lấy dữ liệu từ `Quote` class với nguồn VCI
- `OHLCVDailyValidator`: Kiểm tra đủ cột (time, open, high, low, close, volume)
- `OHLCVDailyTransformer`: Xóa duplicate, format datetime
- `CSVExport`: Xuất CSV

**Output Structure**:

```
Columns: time, open, high, low, close, volume
Example (VCB):
        time   open   high    low  close   volume
0 2024-11-01  62.42  63.02  62.09  62.09  1732251
1 2024-11-02  62.09  62.92  61.95  62.42   892151
...
21 2024-12-02  63.02  63.15  62.36  62.56  1575332

Shape: (22, 6)
Data types:
time    datetime64[ns]
open             float64
high             float64
low              float64
close            float64
volume             int64
```

**Parameters**:

```python
run_task(
    tickers: list,              # ['VCB', 'ACB', 'HPG']
    start: str = "2024-01-01",  # Start date
    end: str = "2025-03-19",    # End date
    interval: str = "1D"        # 1D, 1W, 1M, 1H, 5m, 15m, 30m
)
```

**Ví dụ**:

```python
from vnstock_pipeline.tasks.ohlcv import run_task

# Lấy OHLCV cho VN30
from vnstock import Vnstock
stock = Vnstock().stock(symbol="VCB", source="VCI")
vn30 = stock.listing.symbols_by_group("VN30").tolist()

run_task(
    vn30,
    start="2024-01-01",
    end="2024-12-02",
    interval="1D"
)

print(f"✅ Data saved to ./data/ohlcv/")
print(f"   Files: {len(vn30)} CSV files")
```

**Output Location**: `./data/ohlcv/{ticker}.csv`

**Use Cases**:
- Phân tích kỹ thuật (technical analysis)
- Backtesting chiến lược giao dịch
- Dữ liệu huấn luyện mô hình (ML training)
- Khám phá mẫu giá (pattern recognition)

---

### Task 2: Báo Cáo Tài Chính

**Mô tả**: Thu thập dữ liệu báo cáo tài chính chi tiết từ vnstock_data (bao gồm Bảng cân đối kế toán, Kết quả kinh doanh, Lưu chuyển tiền tệ và Tỷ số tài chính).

**Các Loại Báo Cáo**:

| Báo Cáo                      | Tên Tiếng Việt     | Cột | Ví Dụ Chỉ Tiêu                       |
| ---------------------------- | ------------------ | --- | ------------------------------------ |
| **balance_sheet**            | Cân đối kế toán    | 94  | Tài sản, Nợ, Vốn chủ sở hữu          |
| **income_statement_year**    | KQKD năm           | 28  | Doanh thu, Chi phí, Lợi nhuận        |
| **income_statement_quarter** | KQKD quý           | 28  | Doanh thu quý, Lợi nhuận quý         |
| **cash_flow**                | Lưu chuyển tiền tệ | 56  | Tiền từ hoạt động, đầu tư, tài chính |
| **ratio**                    | Tỷ số tài chính    | 58  | P/E, ROA, ROE, Tỷ lệ nợ/vốn          |

**Cấu Trúc Dữ Liệu Trả Về (Output Structure)**:

```
Bảng cân đối kế toán (VD: VCB):
Kích thước: (8, 94)  # 8 năm, 94 chỉ tiêu
Các cột chính: ticker, Tổng tài sản, Tài sản ngắn hạn, ...

Kết quả kinh doanh năm (VD: VCB):
Kích thước: (8, 28)  # 8 năm
Các cột chính: ticker, Doanh thu thuần, Chi phí bán hàng, ...
```

**Tham Số Bắt Buộc và Tùy Chọn**:

```python
run_financial_task(
    tickers: list,                              # Danh sách mã, VD: ['VCB', 'ACB']
    max_workers: int = 3,                       # Số luồng xử lý song song
    request_delay: float = 0.5,                 # Độ trễ giữa mỗi request (giây)
    rate_limit_wait: float = 35.0,              # Thời gian chờ khi gặp Rate Limit (giây)
    balance_sheet_period: str = "year",         # "year" hoặc "quarter"
    income_statement_year_period: str = "year",
    income_statement_quarter_period: str = "quarter",
    cash_flow_period: str = "year",
    ratio_period: str = "year",
    lang: str = "vi",                           # "vi" hoặc "en"
    dropna: bool = True                         # Xóa hàng có dữ liệu trống
)
```

**Ví Dụ Sử Dụng**:

```python
from vnstock_pipeline.tasks.financial import run_financial_task
from vnstock_data import Listing

# Lấy danh sách VN100
listing = Listing(source="vci")
vn100 = listing.symbols_by_group("VN100").tolist()

# Thu thập dữ liệu báo cáo tài chính với cấu hình tối ưu
run_financial_task(
    vn100,
    max_workers=5,
    request_delay=0.2,
    rate_limit_wait=30.0,
    balance_sheet_period="year",
    income_statement_year_period="year",
    income_statement_quarter_period="quarter",
    cash_flow_period="year",
    ratio_period="year",
    lang="vi",
    dropna=True
)

print(f"✅ Đã lưu dữ liệu tài chính vào thư mục ./data/financial/")
```

**Đầu Ra (Output Location)**: 
```
./data/financial/
├── {ticker}_balance_sheet.csv
├── {ticker}_income_statement_year.csv
├── {ticker}_income_statement_quarter.csv
├── {ticker}_cash_flow.csv
└── {ticker}_ratio.csv
```

**Ứng Dụng Thực Tế (Use Cases)**:
- Phân tích tài chính chuyên sâu.
- Tính toán các chỉ số định giá P/E, ROE, ROA, v.v.
- Xây dựng mô hình định giá doanh nghiệp.
- Tìm kiếm cổ phiếu bị định giá thấp (undervalued) trên thị trường.

---

### Task 3: Dữ Liệu Khớp Lệnh

**Mô tả**: Thu thập toàn bộ lịch sử các lệnh khớp (tick data) trong phiên giao dịch của danh sách mã chứng khoán. Hỗ trợ cơ chế tải tĩnh một lần hoặc cập nhật liên tục (live mode) tích hợp cơ chế ghép dữ liệu thông minh (smart append).

**Chế Độ Tải Dữ Liệu (Modes)**:
- `EOD`: Tải toàn bộ dữ liệu lịch sử lệnh khớp tĩnh (thường dùng sau khi kết thúc phiên).
- `live`: Quét và tải dữ liệu mới liên tục định kỳ trong phiên giao dịch. Trình điều phối sẽ tự động kiểm tra giờ mở/đóng cửa thị trường để dừng lại khi không cần thiết.

**Tham Số Khởi Chạy**:
```python
run_intraday_task(
    tickers: list,              # ['VCB', 'ACB', 'HPG']
    mode: str = "live",         # "live" hoặc "EOD"
    interval: int = 60,         # (Chế độ live) Độ trễ giữa các chu kỳ cập nhật tính bằng giây
    page_size: int = 50000,     # Số lượng bản ghi tick data tối đa lấy từ API mỗi lần gọi
    backup: bool = True,        # Bật/tắt tự động sao lưu dữ liệu trong chế độ live
    max_backups: int = 2        # Số file sao lưu tối đa giữ lại cho mỗi mã
)
```

**Ví Dụ Sử Dụng**:

```python
from vnstock_pipeline.tasks.intraday import run_intraday_task

tickers = ['VCB', 'ACB', 'HPG']

# Tải dữ liệu liên tục trong phiên giao dịch
run_intraday_task(
    tickers,
    mode="live",
    interval=60,                # Quét dữ liệu mỗi 60 giây
    page_size=5000,             # Ở chế độ live chỉ cần page_size nhỏ để giảm tải API
    backup=True,
    max_backups=2
)

print(f"✅ Đã lưu dữ liệu Intraday vào thư mục ./data/intraday/")
```

**Ứng Dụng Thực Tế (Use Cases)**:
- Xây dựng chiến lược giao dịch trong ngày (Day trading).
- Phân tích khối lượng theo vùng giá (Volume Profile).
- Đào tạo mô hình phân tích hành vi khớp lệnh mua/bán chủ động.

---

### Task 4: Bảng Giá Trực Tuyến

**Mô tả**: Truy xuất thông tin bảng giá trực tuyến (bao gồm giá khớp lệnh hiện tại, khối lượng mua/bán tốt nhất và thay đổi giá) cho danh sách mã.

**Chế Độ Tải Dữ Liệu (Modes)**:
```python
mode = "eod"      # Lấy dữ liệu bảng giá cuối ngày một lần duy nhất
mode = "live"     # Cập nhật thông tin bảng giá định kỳ liên tục
```

**Cấu Trúc Cột Dữ Liệu (Output Columns)**:
```text
symbol, last_price, reference, bid_price, ask_price,
best_bid_volume, best_ask_volume, open, high, low,
close_price, total_volume, total_value, change_percent, update_unix, update_time
```

**Ví Dụ Sử Dụng**:

```python
from vnstock_pipeline.tasks.price_board import run_price_board

# Danh sách mã VN30
tickers = [
    'ACB', 'BCM', 'BID', 'BVH', 'CTG', 'FPT', 'GAS', 'GVR',
    'HDB', 'HPG', 'LPB', 'MBB', 'MSN', 'MWG', 'PLX', 'SAB',
    'SHB', 'SSB', 'SSI', 'STB', 'TCB', 'TPB', 'VCB', 'VHM',
    'VIB', 'VIC', 'VJC', 'VNM', 'VPB', 'VRE'
]

# Chế độ End of day
run_price_board(tickers, mode="eod")

# Hoặc chế độ cập nhật trực tuyến mỗi 60 giây
# run_price_board(tickers, interval=60, mode="live")
```

**Ứng Dụng Thực Tế (Use Cases)**:
- Theo dõi biến động giá trị danh mục đầu tư theo thời gian thực.
- Xây dựng hệ thống bảng điều khiển (Dashboard) cá nhân.
- Tích hợp với bot cảnh báo (Discord/Telegram) khi giá chạm ngưỡng thiết lập.

---

## II. BUILDERS (Xây Dựng Custom Pipeline)

Từ phiên bản v2.1.5, vnstock_pipeline cung cấp các tham số scheduler để tối ưu hóa tốc độ xử lý và tránh rate limiting.

### Các Tham Số Scheduler

| Tham Số             | Mặc Định | Phạm Vi | Mô Tả                                   |
| ------------------- | -------- | ------- | --------------------------------------- |
| **max_workers**     | 3        | 1-10    | Số luồng xử lý song song                |
| **request_delay**   | 0.5      | 0.1-2.0 | Delay giữa mỗi request (giây)           |
| **rate_limit_wait** | 35.0     | 30-120  | Thời gian chờ khi gặp rate limit (giây) |

### Cấu hình Tại Khởi Tạo Scheduler

```python
from vnstock_pipeline.core.scheduler import Scheduler
from vnstock_pipeline.tasks.financial import (
    FinancialFetcher, FinancialValidator, 
    FinancialTransformer, FinancialExporter
)

scheduler = Scheduler(
    FinancialFetcher(),
    FinancialValidator(),
    FinancialTransformer(),
    FinancialExporter(base_path="./data/financial"),
    retry_attempts=3,
    max_workers=3,              # (v2.1.5) Số workers
    request_delay=0.5,          # (v2.1.5) Delay giữa requests
    rate_limit_wait=35.0        # (v2.1.5) Chờ khi rate limit
)

scheduler.run(tickers)
```

### Override Tham Số Tại Thời Điểm Chạy

```python
# Override config mặc định của scheduler
scheduler.run(
    tickers,
    max_workers=5,              # Override: 5 workers
    request_delay=0.2,          # Override: 0.2s delay
    rate_limit_wait=40.0        # Override: 40s chờ
)
```

### Cấu hình Qua Hàm Task

```python
from vnstock_pipeline.tasks.financial import run_financial_task

tickers = ["VCB", "ACB", "HPG", "FPT"]

# Cấu hình nhanh
run_financial_task(
    tickers,
    max_workers=5,              # 5 workers song song
    request_delay=0.2,          # 0.2s delay
    rate_limit_wait=30.0,       # 30s chờ
)

# Cấu hình an toàn
run_financial_task(
    tickers,
    max_workers=1,              # Tuần tự
    request_delay=1.0,          # 1s delay
    rate_limit_wait=60.0,       # 60s chờ
)
```

### Hướng Dẫn Lựa Chọn Cấu Hình

**Xử lý ít dữ liệu (< 50 tickers)**:
```python
max_workers=3, request_delay=0.5, rate_limit_wait=35.0
```

**Xử lý nhiều dữ liệu (100+ tickers)**:
```python
max_workers=2, request_delay=1.0, rate_limit_wait=60.0
```

**Xử lý rất nhiều dữ liệu (500+ tickers)**:
```python
max_workers=1, request_delay=2.0, rate_limit_wait=120.0
```

**Tối ưu cho tốc độ (với rủi ro cao hơn)**:
```python
max_workers=8, request_delay=0.1, rate_limit_wait=30.0
```

---

## III. BUILDERS (Xây Dựng Custom Pipeline)

### Builder 1: Simple Custom Fetcher

**Mục đích**: Fetch dữ liệu từ API riêng hoặc nguồn khác

**Các bước**:

1. **Inherit từ VNFetcher**

```python
from vnstock_pipeline.template.vnstock import VNFetcher
import pandas as pd

class MyFetcher(VNFetcher):
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        # Lấy dữ liệu
        from vnstock_data import Quote
        quote = Quote(source="vci", symbol=ticker)
        df = quote.history(
            start=kwargs.get("start", "2024-01-01"),
            end=kwargs.get("end", "2024-12-02"),
            interval=kwargs.get("interval", "1D")
        )
        return df
```

2. **Implement _vn_call method**

- Tham số bắt buộc: `ticker` (str)
- Tham số tùy chọn: `**kwargs` (dict)
- Return: `pd.DataFrame`

3. **Error handling**

```python
class RobustFetcher(VNFetcher):
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        try:
            # Fetch logic
            data = fetch_data(ticker)
            return data
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            # Return empty DataFrame để validator xử lý
            return pd.DataFrame()
```

---

### Builder 2: Custom Validator

**Mục đích**: Xác thực dữ liệu theo tiêu chí riêng

**Các bước**:

1. **Inherit từ VNValidator**

```python
from vnstock_pipeline.template.vnstock import VNValidator
import pandas as pd

class MyValidator(VNValidator):
    required_columns = ["time", "close", "volume"]
    
    def validate(self, data: pd.DataFrame) -> bool:
        # Kiểm tra base
        if not super().validate(data):
            return False
        
        # Kiểm tra tùy chỉnh
        if len(data) == 0:
            return False
        
        if (data['close'] <= 0).any():
            return False
        
        if (data['volume'] < 0).any():
            return False
        
        return True
```

2. **Validate conditions**

```python
class StrictValidator(VNValidator):
    required_columns = ["time", "open", "high", "low", "close", "volume"]
    
    def validate(self, data: pd.DataFrame) -> bool:
        if not super().validate(data):
            return False
        
        # OHLC logic
        if (data['high'] < data['low']).any():
            return False
        
        if (data['close'] > data['high']).any() or (data['close'] < data['low']).any():
            return False
        
        # No extreme price movements
        max_change = data['close'].pct_change().abs().max()
        if max_change > 0.5:  # > 50% in one day
            return False
        
        return True
```

---

### Builder 3: Custom Transformer

**Mục đích**: Làm sạch, chuyển đổi, enrich dữ liệu

**Ví dụ 1: Add Technical Indicators**

```python
from vnstock_pipeline.template.vnstock import VNTransformer
import pandas as pd

class EnrichedTransformer(VNTransformer):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(data)
        
        # Add SMA
        df['sma20'] = df['close'].rolling(20).mean()
        df['sma50'] = df['close'].rolling(50).mean()
        
        # Add RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Add MACD
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        
        return df
```

**Ví dụ 2: Add Derived Columns**

```python
class DerivedTransformer(VNTransformer):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(data)
        
        # Price changes
        df['change'] = df['close'] - df['open']
        df['change_pct'] = (df['close'] - df['close'].shift(1)) / df['close'].shift(1) * 100
        
        # Volatility
        df['volatility_daily'] = (df['high'] - df['low']) / df['open'] * 100
        df['volatility_30d'] = df['change_pct'].rolling(30).std()
        
        # Volume analysis
        df['avg_volume_20d'] = df['volume'].rolling(20).mean()
        df['volume_spike'] = df['volume'] / df['avg_volume_20d']
        
        return df
```

---

### Builder 4: Custom Exporter

**Mục đích**: Lưu dữ liệu vào các định dạng khác nhau

**Ví dụ 1: CSV + Parquet**

```python
from vnstock_pipeline.core.exporter import Exporter
import pandas as pd
import os

class DualExporter(Exporter):
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(f"{base_path}/csv", exist_ok=True)
        os.makedirs(f"{base_path}/parquet", exist_ok=True)
    
    def export(self, data, ticker: str, **kwargs):
        # Save CSV
        csv_path = os.path.join(self.base_path, "csv", f"{ticker}.csv")
        data.to_csv(csv_path, index=False)
        
        # Save Parquet
        parquet_path = os.path.join(self.base_path, "parquet", f"{ticker}.parquet")
        data.to_parquet(parquet_path, index=False)
        
        print(f"✅ {ticker}: CSV + Parquet saved")
    
    def preview(self, ticker: str, n: int = 5, **kwargs):
        csv_path = os.path.join(self.base_path, "csv", f"{ticker}.csv")
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path).head(n)
        return None
```

**Ví dụ 2: Database (SQLite/DuckDB)**

```python
import sqlite3

class SQLiteExporter(Exporter):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
    
    def export(self, data, ticker: str, **kwargs):
        # Create table if not exists
        table_name = f"stock_{ticker}"
        data.to_sql(table_name, self.conn, if_exists='replace', index=False)
        self.conn.commit()
        print(f"✅ {ticker}: Saved to SQLite table {table_name}")
    
    def preview(self, ticker: str, n: int = 5, **kwargs):
        table_name = f"stock_{ticker}"
        query = f"SELECT * FROM {table_name} LIMIT {n}"
        return pd.read_sql(query, self.conn)
    
    def __del__(self):
        if self.conn:
            self.conn.close()
```

**Ví dụ 3: Webhook (Forward to API)**

```python
import requests
import json

class WebhookExporter(Exporter):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def export(self, data, ticker: str, **kwargs):
        # Convert to dict
        payload = {
            "ticker": ticker,
            "count": len(data),
            "latest": data.iloc[-1].to_dict() if len(data) > 0 else None
        }
        
        # Send to webhook
        response = requests.post(
            self.webhook_url,
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✅ {ticker}: Sent to webhook")
        else:
            print(f"❌ {ticker}: Webhook failed ({response.status_code})")
    
    def preview(self, ticker: str, n: int = 5, **kwargs):
        return None
```

---

## III. Advanced Patterns

### Pattern 1: Multi-Source Fetching

```python
from vnstock_pipeline.template.vnstock import VNFetcher
import pandas as pd

class MultiSourceFetcher(VNFetcher):
    """Fetch từ nhiều nguồn, lấy source tốt nhất"""
    
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        sources = ['vci', 'vnd', 'cafef']
        
        for source in sources:
            try:
                from vnstock_data import Quote
                quote = Quote(source=source, symbol=ticker)
                df = quote.history(
                    start=kwargs.get("start", "2024-01-01"),
                    end=kwargs.get("end", "2024-12-02"),
                    interval=kwargs.get("interval", "1D")
                )
                
                if len(df) > 0:
                    df['source'] = source
                    return df
            except:
                continue
        
        # Fallback: empty DataFrame
        return pd.DataFrame()
```

### Pattern 2: Caching Layer

```python
from vnstock_pipeline.template.vnstock import VNFetcher
import pickle
import os

class CachedFetcher(VNFetcher):
    """Fetch with local cache"""
    
    def __init__(self, cache_dir: str = "./cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, ticker: str, start: str, end: str) -> str:
        filename = f"{ticker}_{start}_{end}.pkl"
        return os.path.join(self.cache_dir, filename)
    
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        start = kwargs.get("start", "2024-01-01")
        end = kwargs.get("end", "2024-12-02")
        cache_path = self._get_cache_path(ticker, start, end)
        
        # Check cache
        if os.path.exists(cache_path):
            print(f"Loading {ticker} from cache...")
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        
        # Fetch and cache
        from vnstock_data import Quote
        quote = Quote(source="vci", symbol=ticker)
        df = quote.history(start=start, end=end, interval=kwargs.get("interval", "1D"))
        
        # Save cache
        with open(cache_path, 'wb') as f:
            pickle.dump(df, f)
        
        return df
```

---

## IV. Complete Example: Production Pipeline

```python
from vnstock_pipeline.core.scheduler import Scheduler
from vnstock_pipeline.template.vnstock import VNFetcher, VNValidator, VNTransformer
from vnstock_pipeline.core.exporter import Exporter
import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Custom Fetcher with retry
class RobustFetcher(VNFetcher):
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        from vnstock_data import Quote
        quote = Quote(source="vnd", symbol=ticker)
        df = quote.history(
            start=kwargs.get("start", "2024-01-01"),
            end=kwargs.get("end", "2024-12-02"),
            interval=kwargs.get("interval", "1D")
        )
        logger.info(f"Fetched {len(df)} rows for {ticker}")
        return df

# 2. Strict Validator
class StrictValidator(VNValidator):
    required_columns = ["time", "open", "high", "low", "close", "volume"]
    
    def validate(self, data: pd.DataFrame) -> bool:
        if not super().validate(data):
            return False
        
        if len(data) < 10:  # Need at least 10 rows
            return False
        
        if (data['high'] < data['low']).any():
            return False
        
        return True

# 3. Enriched Transformer
class EnrichedTransformer(VNTransformer):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(data)
        
        # Add indicators
        df['sma20'] = df['close'].rolling(20).mean()
        df['sma50'] = df['close'].rolling(50).mean()
        df['volatility_30d'] = df['close'].pct_change().rolling(30).std()
        df['change_pct'] = df['close'].pct_change() * 100
        
        logger.info(f"Enriched data with {len(df)} rows")
        return df

# 4. Dual Exporter
class ProductionExporter(Exporter):
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(f"{base_path}/csv", exist_ok=True)
        os.makedirs(f"{base_path}/parquet", exist_ok=True)
    
    def export(self, data, ticker: str, **kwargs):
        # CSV
        csv_path = os.path.join(self.base_path, "csv", f"{ticker}.csv")
        data.to_csv(csv_path, index=False)
        
        # Parquet
        parquet_path = os.path.join(self.base_path, "parquet", f"{ticker}.parquet")
        data.to_parquet(parquet_path, index=False)
        
        logger.info(f"Exported {ticker} to CSV + Parquet")
    
    def preview(self, ticker: str, n: int = 5, **kwargs):
        csv_path = os.path.join(self.base_path, "csv", f"{ticker}.csv")
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path).head(n)
        return None

# 5. Run Pipeline
if __name__ == "__main__":
    tickers = ['VCB', 'ACB', 'HPG', 'FPT', 'GAS']
    
    scheduler = Scheduler(
        RobustFetcher(),
        StrictValidator(),
        EnrichedTransformer(),
        ProductionExporter("./production_data"),
        retry_attempts=3,
        backoff_factor=2.0
    )
    
    scheduler.run(
        tickers,
        fetcher_kwargs={
            "start": "2024-01-01",
            "end": "2024-12-02",
            "interval": "1D"
        }
    )
    
    logger.info("✅ Pipeline completed!")
```

---

## V. Performance Tips

### 1. Batch Processing

```python
def batch_process(all_tickers, batch_size=50):
    for i in range(0, len(all_tickers), batch_size):
        batch = all_tickers[i:i+batch_size]
        scheduler.run(batch)
        print(f"Completed batch {i//batch_size + 1}")
```

### 2. Parallel Workers

```python
scheduler = Scheduler(...)
scheduler.max_workers = 20  # Adjust based on API limits
```

### 3. Caching

```python
# Use cached fetcher to avoid re-fetching
fetcher = CachedFetcher()
```

