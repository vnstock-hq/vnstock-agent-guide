# Vnstock Pipeline - Xây Dựng Custom Pipelines

## Giới Thiệu

Chương này hướng dẫn xây dựng **custom pipelines** - các quy trình riêng biệt để giải quyết các bài toán thực tế như:
- Kết hợp dữ liệu từ nhiều sources
- Làm giàu dữ liệu OHLCV với chỉ báo kỹ thuật
- Xuất dữ liệu vào các định dạng khác nhau
- Tích hợp với hệ thống bên ngoài

---

## I. Kiến Trúc Tùy Chỉnh

### Luồng Xử Lý

```text
Dữ Liệu Đầu Vào (Danh sách mã) 
    ↓
Fetcher (Thu thập dữ liệu)
    ↓
Validator (Xác thực chất lượng)
    ↓
Transformer (Chuyển đổi & Cải thiện)
    ↓
Exporter (Lưu trữ và phân phối)
    ↓
Dữ Liệu Đầu Ra (Files/DB/API)
```

### Vai Trò Của Các Thành Phần

| Thành Phần      | Trách Nhiệm                           | Đầu Vào                   | Đầu Ra                       |
| --------------- | ------------------------------------- | ------------------------- | ---------------------------- |
| **Fetcher**     | Thu thập dữ liệu thô từ nguồn         | Mã chứng khoán, tham số   | DataFrame                    |
| **Validator**   | Kiểm tra chất lượng và tính toàn vẹn  | DataFrame                 | Boolean (Đạt/Không đạt)      |
| **Transformer** | Làm sạch, chuẩn hóa và tính toán thêm | DataFrame                 | DataFrame (Đã được làm giàu) |
| **Exporter**    | Lưu trữ hoặc xuất dữ liệu             | DataFrame, mã chứng khoán | File/Database/API            |

---

## II. Các Mẫu Thiết Kế Fetcher Tùy Chỉnh

### Mẫu 1: API Wrapper Đơn Giản

**Ứng dụng thực tế**: Thu thập dữ liệu từ các API công cộng hoặc hệ thống nội bộ.

```python
from vnstock_pipeline.template.vnstock import VNFetcher
import pandas as pd
import requests

class APIFetcher(VNFetcher):
    """Thu thập dữ liệu từ endpoint API tùy chỉnh"""
    
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
    
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        params = {
            "symbol": ticker,
            "from": kwargs.get("start", "2024-01-01"),
            "to": kwargs.get("end", "2024-12-02"),
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            df = pd.DataFrame(data['quotes'])
            
            # Chuẩn hóa tên cột
            df.rename(columns={
                'timestamp': 'time',
                'open_price': 'open',
                'high_price': 'high',
                'low_price': 'low',
                'close_price': 'close',
                'volume_traded': 'volume'
            }, inplace=True)
            
            return df
        
        except Exception as e:
            print(f"Lỗi khi thu thập {ticker}: {e}")
            return pd.DataFrame()
```

**Cách Sử Dụng**:

```python
fetcher = APIFetcher(
    api_url="https://api.example.com/stocks",
    api_key="your_api_key"
)
```

---

### Mẫu 2: Dự Phòng Đa Nguồn (Multi-Source Fallback)

**Ứng dụng thực tế**: Thử tự động lấy từ nguồn dự phòng nếu nguồn dữ liệu chính gặp sự cố.

```python
from vnstock_pipeline.template.vnstock import VNFetcher
from vnstock_data import Quote
import pandas as pd

class MultiSourceFetcher(VNFetcher):
    """Thử nhiều nguồn dữ liệu, sử dụng nguồn tốt nhất có sẵn"""
    
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        sources = ['vci', 'vnd', 'cafef']  # Thứ tự ưu tiên
        
        for source in sources:
            try:
                quote = Quote(source=source, symbol=ticker)
                df = quote.history(
                    start=kwargs.get("start", "2024-01-01"),
                    end=kwargs.get("end", "2024-12-02"),
                    interval=kwargs.get("interval", "1D")
                )
                
                if len(df) > 0:
                    df['source'] = source
                    print(f"✅ Đã lấy {ticker} từ nguồn {source}")
                    return df
            
            except Exception as e:
                print(f"⚠️ {ticker} lỗi với nguồn {source}: {e}")
                continue
        
        print(f"❌ {ticker} thất bại với tất cả các nguồn")
        return pd.DataFrame()
```

**Cách Sử Dụng**:

```python
fetcher = MultiSourceFetcher()
df = fetcher._vn_call("VCB", start="2024-01-01", end="2024-12-02")
print(f"Nguồn sử dụng: {df['source'].iloc[0] if len(df) > 0 else 'Không có'}")
```

---

### Mẫu 3: Lưu Trữ Tạm Thời (Caching)

**Ứng dụng thực tế**: Tránh gọi API lặp lại không cần thiết để tăng tốc độ khởi chạy lại pipeline.

```python
from vnstock_pipeline.template.vnstock import VNFetcher
from vnstock_data import Quote
import pandas as pd
import pickle
import os
from datetime import datetime, timedelta

class CachedFetcher(VNFetcher):
    """Thu thập dữ liệu kèm bộ nhớ đệm cục bộ (tự động hết hạn)"""
    
    def __init__(self, cache_dir: str = "./cache", ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.ttl_hours = ttl_hours
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, ticker: str, start: str, end: str) -> str:
        filename = f"{ticker}_{start}_{end}.pkl"
        return os.path.join(self.cache_dir, filename)
    
    def _is_cache_valid(self, cache_path: str) -> bool:
        if not os.path.exists(cache_path):
            return False
        
        age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_path))
        return age < timedelta(hours=self.ttl_hours)
    
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        start = kwargs.get("start", "2024-01-01")
        end = kwargs.get("end", "2024-12-02")
        cache_path = self._get_cache_path(ticker, start, end)
        
        # Kiểm tra bộ nhớ đệm
        if self._is_cache_valid(cache_path):
            with open(cache_path, 'rb') as f:
                df = pickle.load(f)
                print(f"✅ Lấy {ticker} từ bộ nhớ đệm")
                return df
        
        # Tải dữ liệu mới
        try:
            quote = Quote(source="vci", symbol=ticker)
            df = quote.history(start=start, end=end, interval=kwargs.get("interval", "1D"))
            
            # Lưu vào đệm
            with open(cache_path, 'wb') as f:
                pickle.dump(df, f)
            
            print(f"✅ Đã tải mới {ticker}")
            return df
        
        except Exception as e:
            print(f"❌ Lỗi khi tải {ticker}: {e}")
            return pd.DataFrame()
```

**Cách Sử Dụng**:

```python
fetcher = CachedFetcher(cache_dir="./stock_cache", ttl_hours=12)

# Lần gọi đầu tiên: Sẽ tải mới từ API
df1 = fetcher._vn_call("VCB", start="2024-01-01", end="2024-12-02")

# Lần gọi thứ hai: Sẽ lấy thẳng từ bộ nhớ đệm (nhanh hơn)
df2 = fetcher._vn_call("VCB", start="2024-01-01", end="2024-12-02")

# Sau 12 tiếng: Sẽ hết hạn và bắt đầu tải mới lại
```

---

## III. Các Mẫu Thiết Kế Validator Tùy Chỉnh

### Mẫu 1: Xác Thực Theo Logic Nghiệp Vụ

**Ứng dụng thực tế**: Kiểm tra dữ liệu theo các điều kiện nghiệp vụ cụ thể.

```python
from vnstock_pipeline.template.vnstock import VNValidator
import pandas as pd

class BusinessValidator(VNValidator):
    """Xác thực dựa trên các quy tắc nghiệp vụ"""
    
    required_columns = ["time", "open", "high", "low", "close", "volume"]
    
    def validate(self, data: pd.DataFrame) -> bool:
        # Kiểm tra cơ bản
        if not super().validate(data):
            return False
        
        # Số lượng hàng tối thiểu
        if len(data) < 20:
            print("❌ Dữ liệu không đủ (< 20 dòng)")
            return False
        
        # Logic giá OHLC
        if (data['high'] < data['low']).any():
            print("❌ Lỗi: Giá cao nhất (High) < Giá thấp nhất (Low)")
            return False
        
        if (data['close'] > data['high']).any() or (data['close'] < data['low']).any():
            print("❌ Lỗi: Giá đóng cửa (Close) nằm ngoài khoảng High/Low")
            return False
        
        # Tính liên tục của giá
        price_gap = data['open'].diff().abs() / data['close'].shift(1)
        if (price_gap > 0.1).any():  # Nhảy giá 10%
            print("⚠️ Cảnh báo: Phát hiện khoảng trống giá (gap) lớn")
            # Có thể trả về False hoặc chỉ cảnh báo
        
        # Kiểm tra khối lượng
        if (data['volume'] <= 0).any():
            print("❌ Lỗi: Khối lượng giao dịch không hợp lệ (<= 0)")
            return False
        
        # Biến động bất thường (> 50%)
        max_move = (data['close'] - data['open']).abs() / data['open']
        if (max_move > 0.5).any():
            print("❌ Lỗi: Biến động giá bất thường (> 50%)")
            return False
        
        return True
```

**Cách Sử Dụng**:

```python
validator = BusinessValidator()

# Good data
good_df = pd.DataFrame({
    'time': pd.date_range('2024-01-01', periods=50),
    'open': [62.0] * 50,
    'high': [63.0] * 50,
    'low': [61.0] * 50,
    'close': [62.5] * 50,
    'volume': [1000000] * 50
})
print(f"Good data valid: {validator.validate(good_df)}")  # True

# Bad data (high < low)
bad_df = good_df.copy()
bad_df.loc[0, 'high'] = 60.0
print(f"Bad data valid: {validator.validate(bad_df)}")  # False
```

---

### Mẫu 2: Chấm Điểm Chất Lượng Dữ Liệu (Quality Scoring)

**Ứng dụng thực tế**: Đánh giá và cho điểm chất lượng dữ liệu thay vì từ chối hoàn toàn.

```python
from vnstock_pipeline.template.vnstock import VNValidator
import pandas as pd

class QualityScorer(VNValidator):
    """Chấm điểm chất lượng dữ liệu từ 0-100"""
    
    required_columns = ["time", "open", "high", "low", "close", "volume"]
    
    def validate(self, data: pd.DataFrame) -> bool:
        # Accept if score >= threshold
        score = self.quality_score(data)
        print(f"Data quality score: {score}/100")
        return score >= 70
    
    def quality_score(self, data: pd.DataFrame) -> float:
        if len(data) == 0:
            return 0
        
        score = 100
        
        # Check required columns
        missing_cols = set(self.required_columns) - set(data.columns)
        if missing_cols:
            score -= 50
        
        # Check data completeness
        missing_pct = data.isnull().sum().sum() / (len(data) * len(data.columns)) * 100
        score -= missing_pct
        
        # Check OHLC logic
        bad_ohlc = (data['high'] < data['low']).sum()
        score -= bad_ohlc * 10
        
        # Check volume
        zero_volume = (data['volume'] <= 0).sum()
        score -= zero_volume * 5
        
        # Check time continuity
        if 'time' in data.columns:
            data_sorted = data.sort_values('time')
            gaps = data_sorted['time'].diff().dt.days
            # For daily data, expect gaps <= 3 (weekends/holidays)
            excessive_gaps = (gaps > 3).sum()
            score -= excessive_gaps * 2
        
        return max(0, score)
```

---

## IV. Các Mẫu Thiết Kế Transformer Tùy Chỉnh

### Mẫu 1: Tính Toán Chỉ Báo Kỹ Thuật (Technical Indicators)

**Ứng dụng thực tế**: Tính toán và bổ sung hơn 20 chỉ báo kỹ thuật vào dữ liệu giá OHLCV.

```python
from vnstock_pipeline.template.vnstock import VNTransformer
import pandas as pd
import numpy as np

class TAEnrichedTransformer(VNTransformer):
    """Làm giàu dữ liệu bằng các chỉ báo kỹ thuật toàn diện"""
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(data)
        
        # Moving Averages
        df['sma5'] = df['close'].rolling(5).mean()
        df['sma10'] = df['close'].rolling(10).mean()
        df['sma20'] = df['close'].rolling(20).mean()
        df['sma50'] = df['close'].rolling(50).mean()
        df['ema12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['ema26'] = df['close'].ewm(span=26, adjust=False).mean()
        
        # Momentum
        df['roc'] = df['close'].pct_change(periods=12) * 100
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        
        # Bollinger Bands
        bb_ma = df['close'].rolling(20).mean()
        bb_std = df['close'].rolling(20).std()
        df['bb_upper'] = bb_ma + (bb_std * 2)
        df['bb_middle'] = bb_ma
        df['bb_lower'] = bb_ma - (bb_std * 2)
        df['bb_pct'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        # ATR (Average True Range)
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift()),
                abs(df['low'] - df['close'].shift())
            )
        )
        df['atr'] = df['tr'].rolling(14).mean()
        
        # Volatility
        df['volatility_daily'] = (df['high'] - df['low']) / df['open'] * 100
        df['volatility_10d'] = df['close'].pct_change().rolling(10).std() * 100
        df['volatility_30d'] = df['close'].pct_change().rolling(30).std() * 100
        
        # On-Balance Volume
        obv = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
        df['obv'] = obv
        df['obv_ema'] = obv.ewm(span=21, adjust=False).mean()
        
        return df
```

**Ví dụ cấu trúc đầu ra (Output Example)**:

```
DataFrame với columns:
time, open, high, low, close, volume,
sma5, sma10, sma20, sma50, ema12, ema26,
roc, rsi, macd, macd_signal, macd_hist,
bb_upper, bb_middle, bb_lower, bb_pct,
atr, volatility_daily, volatility_10d, volatility_30d,
obv, obv_ema

Tổng cộng: ~25 columns
```

---

### Mẫu 2: Kết Hợp Dữ Liệu Cơ Bản (Fundamental Data)

**Ứng dụng thực tế**: Kết hợp dữ liệu giá (OHLCV) với các chỉ số từ báo cáo tài chính.

```python
from vnstock_pipeline.template.vnstock import VNTransformer
from vnstock_data import Finance
import pandas as pd

class FundamentalEnrichedTransformer(VNTransformer):
    """Làm giàu dữ liệu OHLCV với các chỉ số tài chính"""
    
    def __init__(self, ticker: str):
        self.ticker = ticker
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(data)
        
        try:
            # Lấy dữ liệu tài chính mới nhất
            finance = Finance(symbol=self.ticker)
            balance = finance.balance_sheet()
            income = finance.income_statement()
            ratio = finance.ratio()
            
            if balance is not None and len(balance) > 0:
                latest_balance = balance.iloc[0]
                df['total_assets'] = latest_balance.get('Tổng tài sản', np.nan)
                df['total_equity'] = latest_balance.get('Tổng vốn chủ sở hữu', np.nan)
                df['total_debt'] = latest_balance.get('Tổng nợ', np.nan)
            
            if income is not None and len(income) > 0:
                latest_income = income.iloc[0]
                df['revenue'] = latest_income.get('Doanh thu thuần', np.nan)
                df['net_income'] = latest_income.get('Lợi nhuận ròng', np.nan)
            
            if ratio is not None and len(ratio) > 0:
                latest_ratio = ratio.iloc[0]
                df['pe_ratio'] = latest_ratio.get('P/E', np.nan)
                df['roe'] = latest_ratio.get('ROE', np.nan)
                df['roa'] = latest_ratio.get('ROA', np.nan)
                df['debt_equity'] = latest_ratio.get('Debt/Equity', np.nan)
            
            # Calculate derived metrics
            df['price_to_book'] = df['close'] * 1000000 / df['total_equity']  # Adjust units
            df['book_value_per_share'] = df['total_equity'] / 1000000
            
        except Exception as e:
            print(f"Warning: Could not fetch fundamentals for {self.ticker}: {e}")
        
        return df
```

---

### Mẫu 3: Chuẩn Hóa Dữ Liệu (Data Normalization)

**Ứng dụng thực tế**: Chuẩn hóa và đưa dữ liệu về cùng thang đo (scale) phục vụ huấn luyện mô hình Machine Learning.

```python
from vnstock_pipeline.template.vnstock import VNTransformer
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd

class NormalizedTransformer(VNTransformer):
    """Chuẩn hóa dữ liệu cho các mô hình Machine Learning"""
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(data)
        
        # Xác định các cột dạng số cần chuẩn hóa
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        exclude = ['volume']  # Bỏ qua cột khối lượng
        cols_to_normalize = [c for c in numeric_cols if c not in exclude]
        
        # Áp dụng StandardScaler cho các chỉ báo
        scaler = StandardScaler()
        df[cols_to_normalize] = scaler.fit_transform(df[cols_to_normalize])
        
        # Áp dụng MinMaxScaler cho các mức giá (khoảng 0-1)
        minmax = MinMaxScaler()
        df[['open', 'high', 'low', 'close']] = minmax.fit_transform(df[['open', 'high', 'low', 'close']])
        
        return df
```

---

## V. Các Mẫu Thiết Kế Exporter Tùy Chỉnh

### Mẫu 1: Xuất Đa Định Dạng (Multi-Format)

**Ứng dụng thực tế**: Lưu cùng lúc vào các định dạng CSV, Parquet và JSON.

```python
from vnstock_pipeline.core.exporter import Exporter
import pandas as pd
import os
import json

class MultiFormatExporter(Exporter):
    """Export to multiple formats"""
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        for fmt in ['csv', 'parquet', 'json']:
            os.makedirs(f"{base_path}/{fmt}", exist_ok=True)
    
    def export(self, data, ticker: str, **kwargs):
        # CSV
        csv_path = os.path.join(self.base_path, "csv", f"{ticker}.csv")
        data.to_csv(csv_path, index=False)
        
        # Parquet
        parquet_path = os.path.join(self.base_path, "parquet", f"{ticker}.parquet")
        data.to_parquet(parquet_path, index=False, compression='snappy')
        
        # JSON
        json_path = os.path.join(self.base_path, "json", f"{ticker}.json")
        data_dict = {
            'ticker': ticker,
            'rows': len(data),
            'columns': list(data.columns),
            'records': data.to_dict('records')
        }
        with open(json_path, 'w') as f:
            json.dump(data_dict, f, default=str, indent=2)
        
        print(f"✅ {ticker}: CSV + Parquet + JSON saved")
    
    def preview(self, ticker: str, n: int = 5, **kwargs):
        csv_path = os.path.join(self.base_path, "csv", f"{ticker}.csv")
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path).head(n)
        return None
```

---

### Mẫu 2: Xuất Ra Cơ Sở Dữ Liệu (Database Export)

**Ứng dụng thực tế**: Lưu trực tiếp vào SQLite hoặc DuckDB để tối ưu tốc độ truy vấn SQL.

```python
from vnstock_pipeline.core.exporter import Exporter
import duckdb
import pandas as pd

class DuckDBExporter(Exporter):
    """Export to DuckDB for efficient querying"""
    
    def __init__(self, db_path: str = "stocks.duckdb"):
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
    
    def export(self, data, ticker: str, **kwargs):
        # Create table or append to existing
        table_name = f"stock_{ticker}".lower()
        
        try:
            self.conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} AS
                SELECT * FROM data WHERE 1=0
            """)
        except:
            pass
        
        # Insert data
        self.conn.from_df(data).insert_into(table_name)
        print(f"✅ {ticker}: Inserted into {table_name}")
    
    def query(self, ticker: str, query: str):
        """Query data directly"""
        table_name = f"stock_{ticker}".lower()
        return self.conn.execute(
            f"SELECT * FROM {table_name} WHERE {query}"
        ).df()
    
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

# Usage
exporter = DuckDBExporter("stocks.duckdb")

# Export
for ticker in ['VCB', 'ACB']:
    df = fetch_data(ticker)
    exporter.export(df, ticker)

# Query
recent_vcb = exporter.query("vcb", "time > '2024-12-01'")
high_volume = exporter.query("vcb", "volume > 10000000")
```

---

### Mẫu 3: Tích Hợp Webhook

**Ứng dụng thực tế**: Gửi thông báo hoặc đẩy dữ liệu theo từng lô (batch) lên các hệ thống từ xa như API server, Discord, hoặc Telegram.

```python
from vnstock_pipeline.core.exporter import Exporter
import requests
import json

class WebhookExporter(Exporter):
    """Push data to webhook endpoint"""
    
    def __init__(self, webhook_url: str, batch_size: int = 100):
        self.webhook_url = webhook_url
        self.batch_size = batch_size
    
    def export(self, data, ticker: str, **kwargs):
        # Send in batches
        for i in range(0, len(data), self.batch_size):
            batch = data.iloc[i:i+self.batch_size]
            
            payload = {
                "ticker": ticker,
                "timestamp": datetime.now().isoformat(),
                "count": len(batch),
                "data": batch.to_dict('records')
            }
            
            try:
                response = requests.post(
                    self.webhook_url,
                    json=payload,
                    timeout=10,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    print(f"✅ {ticker}: Batch {i//self.batch_size + 1} sent")
                else:
                    print(f"⚠️ {ticker}: HTTP {response.status_code}")
            
            except Exception as e:
                print(f"❌ {ticker}: Webhook failed - {e}")
    
    def preview(self, ticker: str, n: int = 5, **kwargs):
        # No preview for webhook
        return None
```

---

## VI. Ví Dụ Cấu Trúc Pipeline Hoàn Chỉnh (Production-Ready)

```python
"""
Pipeline hoàn chỉnh: Tải VN100, làm giàu dữ liệu kỹ thuật, và xuất ra Parquet/CSV.
"""

from vnstock_pipeline.core.scheduler import Scheduler
from vnstock_pipeline.template.vnstock import VNFetcher, VNValidator, VNTransformer
from vnstock_pipeline.core.exporter import Exporter
from vnstock_data import Quote, Finance
import pandas as pd
import numpy as np
import logging
from datetime import datetime

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============= FETCHER =============
class ProductionFetcher(VNFetcher):
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        try:
            quote = Quote(source="vci", symbol=ticker)
            df = quote.history(
                start=kwargs.get("start", "2024-01-01"),
                end=kwargs.get("end", "2024-12-02"),
                interval=kwargs.get("interval", "1D")
            )
            logger.info(f"✅ Fetched {len(df)} rows for {ticker}")
            return df
        except Exception as e:
            logger.error(f"❌ Fetch failed for {ticker}: {e}")
            return pd.DataFrame()

# ============= VALIDATOR =============
class ProductionValidator(VNValidator):
    required_columns = ["time", "open", "high", "low", "close", "volume"]
    
    def validate(self, data: pd.DataFrame) -> bool:
        if not super().validate(data):
            return False
        
        # Min rows
        if len(data) < 20:
            return False
        
        # OHLC checks
        if (data['high'] < data['low']).any():
            return False
        
        # Volume checks
        if (data['volume'] <= 0).any():
            return False
        
        return True

# ============= TRANSFORMER =============
class ProductionTransformer(VNTransformer):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(data)
        
        # Moving Averages
        df['sma20'] = df['close'].rolling(20).mean()
        df['sma50'] = df['close'].rolling(50).mean()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        
        # Volatility
        df['volatility_30d'] = df['close'].pct_change().rolling(30).std() * 100
        
        # Price change
        df['change_pct'] = df['close'].pct_change() * 100
        
        logger.info(f"Enriched {len(df)} rows with indicators")
        return df

# ============= EXPORTER =============
class ProductionExporter(Exporter):
    def __init__(self, base_path: str):
        self.base_path = base_path
        import os
        os.makedirs(f"{base_path}/csv", exist_ok=True)
        os.makedirs(f"{base_path}/parquet", exist_ok=True)
    
    def export(self, data, ticker: str, **kwargs):
        import os
        
        # CSV
        csv_path = os.path.join(self.base_path, "csv", f"{ticker}.csv")
        data.to_csv(csv_path, index=False)
        
        # Parquet
        parquet_path = os.path.join(self.base_path, "parquet", f"{ticker}.parquet")
        data.to_parquet(parquet_path, index=False, compression='snappy')
        
        logger.info(f"✅ Exported {ticker}")
    
    def preview(self, ticker: str, n: int = 5, **kwargs):
        import os
        csv_path = os.path.join(self.base_path, "csv", f"{ticker}.csv")
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path).head(n)
        return None

# ============= RUN PIPELINE =============
if __name__ == "__main__":
    # Get VN100 tickers
    from vnstock import Vnstock
    stock = Vnstock().stock(symbol="VCB", source="VCI")
    tickers = stock.listing.symbols_by_group("VN100").tolist()
    
    # Create scheduler
    scheduler = Scheduler(
        ProductionFetcher(),
        ProductionValidator(),
        ProductionTransformer(),
        ProductionExporter("./vn100_enriched"),
        retry_attempts=3,
        backoff_factor=2.0
    )
    
    # Run
    logger.info(f"Starting pipeline for {len(tickers)} tickers")
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

## VII. Mẫu Thiết Kế Processor Tùy Chỉnh (Dữ Liệu Streaming)

**Ứng dụng thực tế**: Xử lý dữ liệu thời gian thực từ luồng WebSocket (Streaming) bằng cách tạo các Processor kế thừa từ `DataProcessor`. Khác với quy trình tĩnh ở trên, `DataProcessor` xử lý từng gói tin (tick) bất đồng bộ (async) ngay khi chúng vừa đến hệ thống.

```python
from vnstock_pipeline.stream import DataProcessor
import logging

class CustomSignalProcessor(DataProcessor):
    """Custom processor để lọc và tính toán tín hiệu kỹ thuật real-time"""
    
    def __init__(self, symbol: str, buffer_size: int = 100):
        super().__init__()
        self.symbol = symbol
        self.prices = []
        self.buffer_size = buffer_size
        
    async def process(self, data: dict) -> None:
        # 1. Định tuyến sự kiện thông minh (từ vnstock_pipeline v2+)
        event_type = data.get("event_type") or data.get("data_type") or ""
        if event_type not in ["stockps", "board"]:
            return
            
        # 2. Lọc mã chứng khoán (nhận diện cả mã KRX tự động convert)
        if data.get("krx_symbol", data.get("symbol")) != self.symbol:
            return
            
        # 3. Trích xuất giá và lưu buffer
        price = float(data.get("price") or data.get("last_price") or 0)
        if not price:
            return
            
        self.prices.append(price)
        if len(self.prices) > self.buffer_size:
            self.prices.pop(0)
        
        # 4. Tính toán và Cảnh báo (ví dụ với vnstock_ta)
        if len(self.prices) >= 20:
            # import pandas as pd
            # from vnstock_ta.indicators.trend import TrendIndicator
            # Xây dựng tín hiệu cảnh báo tại đây...
            pass
```

**Cách Sử Dụng** (Tích hợp với `WSSClient`):

```python
import asyncio
from vnstock_pipeline.stream import WSSClient

async def main():
    client = WSSClient(enable_session_manager=True)
    client.subscribe_symbols(["VN30F1M"])
    
    # Gắn Custom Processor vào luồng Streaming Pipeline
    client.add_processor(CustomSignalProcessor(symbol="VN30F1M"))
    
    await client.connect()
```

---

## VIII. Kịch Bản Kiểm Thử (Testing Custom Pipelines)

```python
import unittest
import pandas as pd
import numpy as np

class TestCustomPipeline(unittest.TestCase):
    
    def setUp(self):
        # Create sample data
        self.valid_data = pd.DataFrame({
            'time': pd.date_range('2024-01-01', periods=50),
            'open': np.random.uniform(60, 65, 50),
            'high': np.random.uniform(63, 67, 50),
            'low': np.random.uniform(58, 62, 50),
            'close': np.random.uniform(60, 65, 50),
            'volume': np.random.randint(1000000, 10000000, 50)
        })
        
        # Ensure OHLC logic
        self.valid_data['low'] = self.valid_data[['open', 'high', 'low', 'close']].min(axis=1)
        self.valid_data['high'] = self.valid_data[['open', 'high', 'low', 'close']].max(axis=1)
    
    def test_fetcher(self):
        fetcher = ProductionFetcher()
        df = fetcher._vn_call("VCB", start="2024-01-01", end="2024-12-02")
        self.assertGreater(len(df), 0)
        self.assertIn('close', df.columns)
    
    def test_validator(self):
        validator = ProductionValidator()
        self.assertTrue(validator.validate(self.valid_data))
    
    def test_transformer(self):
        transformer = ProductionTransformer()
        result = transformer.transform(self.valid_data)
        self.assertIn('sma20', result.columns)
        self.assertIn('rsi', result.columns)
        self.assertIn('macd', result.columns)

if __name__ == '__main__':
    unittest.main()
```

