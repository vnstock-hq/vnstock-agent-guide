# Vnstock Pipeline - Xây Dựng Custom Pipelines

## Giới Thiệu

Chương này hướng dẫn xây dựng **custom pipelines** - các quy trình riêng biệt để giải quyết các bài toán thực tế như:
- Kết hợp dữ liệu từ nhiều sources
- Làm giàu dữ liệu OHLCV với chỉ báo kỹ thuật
- Xuất dữ liệu vào các định dạng khác nhau
- Tích hợp với hệ thống bên ngoài

---

## I. Kiến Trúc Custom Pipeline

### Luồng Xử Lý

```
Input (Tickers) 
    ↓
Fetcher (Lấy dữ liệu)
    ↓
Validator (Kiểm tra dữ liệu)
    ↓
Transformer (Chuyển đổi & Làm giàu)
    ↓
Exporter (Lưu dữ liệu)
    ↓
Output (Files/DB/API)
```

### Component Responsibilities

| Component | Trách Nhiệm | Input | Output |
|-----------|------------|-------|--------|
| **Fetcher** | Lấy raw data từ source | Ticker, params | DataFrame |
| **Validator** | Kiểm tra data quality | DataFrame | bool (pass/fail) |
| **Transformer** | Làm sạch, enrich, tính toán | DataFrame | DataFrame (enriched) |
| **Exporter** | Lưu data | DataFrame, ticker | File/DB/API |

---

## II. Custom Fetcher Patterns

### Pattern 1: Simple API Wrapper

**Use case**: Fetch từ API công khai hoặc proprietary

```python
from vnstock_pipeline.template.vnstock import VNFetcher
import pandas as pd
import requests

class APIFetcher(VNFetcher):
    """Fetch from custom API endpoint"""
    
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
            
            # Normalize columns
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
            print(f"Error fetching {ticker}: {e}")
            return pd.DataFrame()
```

**Usage**:

```python
fetcher = APIFetcher(
    api_url="https://api.example.com/stocks",
    api_key="your_api_key"
)
```

---

### Pattern 2: Multi-Source Fallback

**Use case**: Retry với sources khác nếu source chính thất bại

```python
from vnstock_pipeline.template.vnstock import VNFetcher
from vnstock_data import Quote
import pandas as pd

class MultiSourceFetcher(VNFetcher):
    """Try multiple sources, use best available"""
    
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        sources = ['vci', 'vnd', 'cafef']  # Priority order
        
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
                    print(f"✅ {ticker} from {source}")
                    return df
            
            except Exception as e:
                print(f"⚠️ {ticker} failed with {source}: {e}")
                continue
        
        print(f"❌ {ticker} failed all sources")
        return pd.DataFrame()
```

**Usage**:

```python
fetcher = MultiSourceFetcher()
df = fetcher._vn_call("VCB", start="2024-01-01", end="2024-12-02")
print(f"Source: {df['source'].iloc[0] if len(df) > 0 else 'None'}")
```

---

### Pattern 3: Caching with Expiration

**Use case**: Avoid redundant API calls, speed up re-runs

```python
from vnstock_pipeline.template.vnstock import VNFetcher
from vnstock_data import Quote
import pandas as pd
import pickle
import os
from datetime import datetime, timedelta

class CachedFetcher(VNFetcher):
    """Fetch with local cache, automatic expiration"""
    
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
        
        # Check cache
        if self._is_cache_valid(cache_path):
            with open(cache_path, 'rb') as f:
                df = pickle.load(f)
                print(f"✅ {ticker} from cache")
                return df
        
        # Fetch fresh
        try:
            quote = Quote(source="vci", symbol=ticker)
            df = quote.history(start=start, end=end, interval=kwargs.get("interval", "1D"))
            
            # Save cache
            with open(cache_path, 'wb') as f:
                pickle.dump(df, f)
            
            print(f"✅ {ticker} freshly fetched")
            return df
        
        except Exception as e:
            print(f"❌ Error fetching {ticker}: {e}")
            return pd.DataFrame()
```

**Usage**:

```python
fetcher = CachedFetcher(cache_dir="./stock_cache", ttl_hours=12)

# First call: fetch fresh
df1 = fetcher._vn_call("VCB", start="2024-01-01", end="2024-12-02")

# Second call: from cache
df2 = fetcher._vn_call("VCB", start="2024-01-01", end="2024-12-02")

# After 12 hours: fetch fresh again
```

---

## III. Custom Validator Patterns

### Pattern 1: Business Logic Validation

**Use case**: Kiểm tra điều kiện kinh doanh cụ thể

```python
from vnstock_pipeline.template.vnstock import VNValidator
import pandas as pd

class BusinessValidator(VNValidator):
    """Validate against business rules"""
    
    required_columns = ["time", "open", "high", "low", "close", "volume"]
    
    def validate(self, data: pd.DataFrame) -> bool:
        # Base checks
        if not super().validate(data):
            return False
        
        # Minimum rows
        if len(data) < 20:
            print("❌ Insufficient data (< 20 rows)")
            return False
        
        # OHLC logic
        if (data['high'] < data['low']).any():
            print("❌ High < Low detected")
            return False
        
        if (data['close'] > data['high']).any() or (data['close'] < data['low']).any():
            print("❌ Close outside High/Low range")
            return False
        
        # Price continuity
        price_gap = data['open'].diff().abs() / data['close'].shift(1)
        if (price_gap > 0.1).any():  # 10% gap
            print("⚠️ Large price gap detected")
            # Could return False or just warn
        
        # Volume checks
        if (data['volume'] <= 0).any():
            print("❌ Non-positive volume")
            return False
        
        # Extreme movements (> 50%)
        max_move = (data['close'] - data['open']).abs() / data['open']
        if (max_move > 0.5).any():
            print("❌ Extreme price movement (> 50%)")
            return False
        
        return True
```

**Usage**:

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

### Pattern 2: Data Quality Scoring

**Use case**: Score data quality thay vì reject outright

```python
from vnstock_pipeline.template.vnstock import VNValidator
import pandas as pd

class QualityScorer(VNValidator):
    """Score data quality 0-100"""
    
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

## IV. Custom Transformer Patterns

### Pattern 1: Technical Indicators Enrichment

**Use case**: Thêm 20+ indicators vào dữ liệu OHLCV

```python
from vnstock_pipeline.template.vnstock import VNTransformer
import pandas as pd
import numpy as np

class TAEnrichedTransformer(VNTransformer):
    """Enrich with comprehensive technical indicators"""
    
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

**Output example**:

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

### Pattern 2: Fundamental Data Enrichment

**Use case**: Kết hợp OHLCV + báo cáo tài chính

```python
from vnstock_pipeline.template.vnstock import VNTransformer
from vnstock_data import Finance
import pandas as pd

class FundamentalEnrichedTransformer(VNTransformer):
    """Enrich OHLCV with financial indicators"""
    
    def __init__(self, ticker: str):
        self.ticker = ticker
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(data)
        
        try:
            # Fetch latest financial data
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

### Pattern 3: Data Normalization

**Use case**: Chuẩn hóa dữ liệu cho machine learning

```python
from vnstock_pipeline.template.vnstock import VNTransformer
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd

class NormalizedTransformer(VNTransformer):
    """Normalize data for ML models"""
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(data)
        
        # Identify numeric columns to normalize
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        exclude = ['volume']  # Don't normalize volume
        cols_to_normalize = [c for c in numeric_cols if c not in exclude]
        
        # StandardScaler for indicators
        scaler = StandardScaler()
        df[cols_to_normalize] = scaler.fit_transform(df[cols_to_normalize])
        
        # MinMaxScaler for prices (0-1 range)
        minmax = MinMaxScaler()
        df[['open', 'high', 'low', 'close']] = minmax.fit_transform(df[['open', 'high', 'low', 'close']])
        
        return df
```

---

## V. Custom Exporter Patterns

### Pattern 1: Multi-Format Export

**Use case**: Lưu vào CSV + Parquet + JSON

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

### Pattern 2: Database Export

**Use case**: Lưu vào SQLite/DuckDB cho querying

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

### Pattern 3: Webhook Integration

**Use case**: Push data vào remote API/webhook

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

## VI. Complete Production Example

```python
"""
Production pipeline: Fetch VN100 stocks, enrich with indicators, export
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

## VII. Testing Custom Pipelines

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

