# Vnstock Pipeline - Best Practices & Optimization

## Giới Thiệu

Chương này cung cấp guidance cho:
- **Performance optimization**: Tăng tốc độ fetch & process
- **Error handling**: Quản lý lỗi gracefully
- **Testing & debugging**: Kiểm tra pipeline
- **Deployment**: Deploy lên production
- **Monitoring**: Track pipeline health

---

## I. Performance Optimization

### 1. Parallel Fetching

**Problem**: Fetch từng cổ phiếu tuần tự quá chậm
**Solution**: Fetch song song

```python
from vnstock_pipeline.core.scheduler import Scheduler

# Sequential (slow)
scheduler = Scheduler(fetcher, validator, transformer, exporter)
# Takes 50 tickers * 2 seconds = 100 seconds

# Parallel (fast)
scheduler.max_workers = 20
# Takes max(50 tickers / 20 workers) * 2 seconds = ~5 seconds
```

**Configuration**:

```python
scheduler = Scheduler(
    fetcher,
    validator,
    transformer,
    exporter,
    max_workers=50  # Adjust based on API limits
)

# Recommended:
# - Free API: 5-10 workers
# - Premium API: 20-50 workers
# - Local data: 100+ workers
```

---

### 2. Batch Processing

**Problem**: Processing 1000+ stocks in one go causes memory issues

**Solution**: Process in batches

```python
def batch_tickers(all_tickers, batch_size=100):
    """Process tickers in batches"""
    for i in range(0, len(all_tickers), batch_size):
        batch = all_tickers[i:i+batch_size]
        yield batch

scheduler = Scheduler(...)

all_tickers = get_vn_all()  # 3000+ stocks

for batch_num, batch in enumerate(batch_tickers(all_tickers, batch_size=100)):
    print(f"Processing batch {batch_num+1}: {batch[:3]}... ({len(batch)} stocks)")
    scheduler.run(batch)
    print(f"✅ Batch {batch_num+1} completed\n")

print(f"✅ All {len(all_tickers)} stocks processed!")
```

---

### 3. Caching Strategy

**Problem**: Re-fetching same data multiple times

**Solution**: Cache aggressively

```python
from vnstock_pipeline.template.vnstock import VNFetcher
from functools import lru_cache
import pickle
import os
from datetime import datetime, timedelta

class SmartCachedFetcher(VNFetcher):
    def __init__(self, cache_dir: str = "./cache", ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)
    
    def _cache_key(self, ticker: str, start: str, end: str, interval: str) -> str:
        return f"{ticker}_{start}_{end}_{interval}.pkl"
    
    def _is_cached(self, cache_path: str) -> bool:
        if not os.path.exists(cache_path):
            return False
        
        age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_path))
        return age < self.ttl
    
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        start = kwargs.get("start", "2024-01-01")
        end = kwargs.get("end", "2024-12-02")
        interval = kwargs.get("interval", "1D")
        
        cache_path = os.path.join(self.cache_dir, self._cache_key(ticker, start, end, interval))
        
        # Try cache first
        if self._is_cached(cache_path):
            with open(cache_path, 'rb') as f:
                print(f"📦 {ticker}: from cache")
                return pickle.load(f)
        
        # Fetch fresh
        from vnstock_data import Quote
        
        try:
            quote = Quote(source="vci", symbol=ticker)
            df = quote.history(start=start, end=end, interval=interval)
            
            # Cache for next time
            with open(cache_path, 'wb') as f:
                pickle.dump(df, f)
            
            print(f"📥 {ticker}: fetched & cached")
            return df
        
        except Exception as e:
            print(f"❌ {ticker}: fetch failed - {e}")
            return pd.DataFrame()

# Usage
fetcher = SmartCachedFetcher(ttl_hours=24)

# First run: fetch all, cache all (slow)
# Second run: use cache (fast)
```

---

### 4. Data Type Optimization

**Problem**: DataFrame uses too much memory

**Solution**: Use appropriate data types

```python
import pandas as pd
import numpy as np

def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Reduce memory by optimizing data types"""
    
    for col in df.columns:
        col_type = df[col].dtype
        
        # Object -> category if unique values < 50
        if col_type == 'object':
            num_unique = len(df[col].unique())
            if num_unique < 50:
                df[col] = df[col].astype('category')
        
        # int64 -> smaller int if possible
        elif col_type == 'int64':
            if df[col].min() >= -2147483648 and df[col].max() <= 2147483647:
                df[col] = df[col].astype('int32')
            elif df[col].min() >= 0 and df[col].max() <= 4294967295:
                df[col] = df[col].astype('uint32')
        
        # float64 -> float32 if precision ok
        elif col_type == 'float64':
            df[col] = df[col].astype('float32')
    
    return df

# Before: 1000 rows × 10 columns = ~80KB
# After:  1000 rows × 10 columns = ~20KB (75% reduction!)

class OptimizedTransformer(VNTransformer):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(data)
        return optimize_dtypes(df)
```

---

### 5. Vectorization Over Loops

**Problem**: Slow Python loops in transformers

**Solution**: Use pandas/numpy vectorization

```python
# ❌ Slow (loop)
def slow_rsi(prices):
    rsi_values = []
    for i in range(len(prices)):
        if i < 14:
            rsi_values.append(np.nan)
        else:
            window = prices[i-14:i]
            # ... complex calculation
            rsi_values.append(rsi)
    return rsi_values

# ✅ Fast (vectorized)
def fast_rsi(prices):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Benchmark:
# slow_rsi: 10000 rows = 500ms
# fast_rsi: 10000 rows = 5ms (100x faster!)
```

---

## II. Error Handling

### 1. Comprehensive Try-Catch

```python
from vnstock_pipeline.template.vnstock import VNFetcher
import logging

logger = logging.getLogger(__name__)

class RobustFetcher(VNFetcher):
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        try:
            from vnstock_data import Quote
            
            quote = Quote(source="vci", symbol=ticker)
            df = quote.history(
                start=kwargs.get("start", "2024-01-01"),
                end=kwargs.get("end", "2024-12-02"),
                interval=kwargs.get("interval", "1D")
            )
            
            if df is None or len(df) == 0:
                logger.warning(f"{ticker}: Empty response")
                return pd.DataFrame()
            
            return df
        
        except ConnectionError as e:
            logger.error(f"{ticker}: Connection failed - {e}")
            # Might retry from scheduler
            return pd.DataFrame()
        
        except ValueError as e:
            logger.error(f"{ticker}: Invalid parameter - {e}")
            # Don't retry, data issue
            return pd.DataFrame()
        
        except Exception as e:
            logger.error(f"{ticker}: Unexpected error - {type(e).__name__}: {e}")
            # Log with full traceback
            logger.exception(f"Traceback for {ticker}:")
            return pd.DataFrame()
```

### 2. Validation at Each Step

```python
from vnstock_pipeline.template.vnstock import VNValidator

class StrictValidator(VNValidator):
    required_columns = ["time", "open", "high", "low", "close", "volume"]
    
    def validate(self, data: pd.DataFrame) -> bool:
        issues = []
        
        # Step 1: Existence check
        if data is None:
            issues.append("Data is None")
            return False
        
        # Step 2: Shape check
        if len(data) == 0:
            issues.append("Empty DataFrame")
            return False
        
        # Step 3: Column check
        missing = set(self.required_columns) - set(data.columns)
        if missing:
            issues.append(f"Missing columns: {missing}")
            return False
        
        # Step 4: Data type check
        for col in self.required_columns:
            if col == 'time' and not pd.api.types.is_datetime64_any_dtype(data[col]):
                issues.append(f"{col} is not datetime")
                return False
            elif col != 'time' and col != 'volume':
                if not pd.api.types.is_numeric_dtype(data[col]):
                    issues.append(f"{col} is not numeric")
                    return False
        
        # Step 5: Value range check
        if (data['close'] <= 0).any():
            issues.append("Non-positive close prices")
            return False
        
        if (data['volume'] < 0).any():
            issues.append("Negative volumes")
            return False
        
        # Step 6: Logic check
        if (data['high'] < data['low']).any():
            issues.append("High < Low")
            return False
        
        if issues:
            for issue in issues:
                logger.warning(f"Validation issue: {issue}")
            return False
        
        return True
```

### 3. Retry with Exponential Backoff

```python
from time import sleep
import random

class RetryableFetcher(VNFetcher):
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        max_retries = 3
        base_wait = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                # ... fetch logic
                return fetch_data(ticker)
            
            except ConnectionError:
                if attempt < max_retries - 1:
                    # Exponential backoff + jitter
                    wait_time = base_wait * (2 ** attempt) + random.uniform(0, 1)
                    logger.info(f"{ticker}: Retry attempt {attempt + 1}, waiting {wait_time:.1f}s")
                    sleep(wait_time)
                else:
                    logger.error(f"{ticker}: Failed after {max_retries} attempts")
                    return pd.DataFrame()
            
            except Exception as e:
                logger.error(f"{ticker}: Unexpected error - {e}")
                return pd.DataFrame()
```

### 4. Error Logging

```python
import logging
from datetime import datetime
import csv

class ErrorLogger:
    def __init__(self, log_file: str = "pipeline_errors.csv"):
        self.log_file = log_file
        self.errors = []
    
    def log_error(self, ticker: str, step: str, error: Exception, **kwargs):
        """Log error to CSV"""
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'ticker': ticker,
            'step': step,
            'error_type': type(error).__name__,
            'error_message': str(error),
            **kwargs
        }
        
        self.errors.append(error_record)
        
        # Write immediately
        with open(self.log_file, 'a', newline='') as f:
            if not self.errors:  # First write, add header
                writer = csv.DictWriter(f, fieldnames=error_record.keys())
                writer.writeheader()
            else:
                writer = csv.DictWriter(f, fieldnames=self.errors[0].keys())
            
            writer.writerow(error_record)

# Usage in scheduler
error_logger = ErrorLogger()

try:
    df = fetcher._vn_call(ticker, **kwargs)
except Exception as e:
    error_logger.log_error(ticker, "fetch", e, source="vci")

# Later: analyze errors
df_errors = pd.read_csv("pipeline_errors.csv")
print(f"Total errors: {len(df_errors)}")
print(f"By ticker: {df_errors.groupby('ticker').size()}")
print(f"By type: {df_errors.groupby('error_type').size()}")
```

---

## III. Testing

### 1. Unit Tests

```python
import unittest
import pandas as pd
import numpy as np
from datetime import datetime

class TestPipeline(unittest.TestCase):
    
    def setUp(self):
        """Create sample data"""
        self.valid_df = pd.DataFrame({
            'time': pd.date_range('2024-01-01', periods=100),
            'open': np.random.uniform(60, 65, 100),
            'high': np.random.uniform(65, 70, 100),
            'low': np.random.uniform(55, 60, 100),
            'close': np.random.uniform(60, 65, 100),
            'volume': np.random.randint(1000000, 10000000, 100)
        })
    
    def test_fetcher_output_structure(self):
        """Test fetcher returns proper structure"""
        fetcher = SmartCachedFetcher()
        df = fetcher._vn_call("VCB", start="2024-01-01", end="2024-12-02")
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
        self.assertIn('close', df.columns)
    
    def test_validator_accepts_valid(self):
        """Test validator accepts valid data"""
        validator = StrictValidator()
        self.assertTrue(validator.validate(self.valid_df))
    
    def test_validator_rejects_empty(self):
        """Test validator rejects empty data"""
        validator = StrictValidator()
        empty_df = pd.DataFrame()
        self.assertFalse(validator.validate(empty_df))
    
    def test_validator_rejects_bad_ohlc(self):
        """Test validator rejects bad OHLC logic"""
        validator = StrictValidator()
        bad_df = self.valid_df.copy()
        bad_df.loc[0, 'high'] = 50  # High < Low
        self.assertFalse(validator.validate(bad_df))
    
    def test_transformer_adds_indicators(self):
        """Test transformer adds indicators"""
        transformer = OptimizedTransformer()
        result = transformer.transform(self.valid_df)
        
        self.assertIn('sma20', result.columns)
        self.assertIn('rsi', result.columns)
        self.assertIn('macd', result.columns)
    
    def test_exporter_creates_file(self):
        """Test exporter creates file"""
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = ProductionExporter(tmpdir)
            exporter.export(self.valid_df, "TEST")
            
            csv_file = os.path.join(tmpdir, "csv", "TEST.csv")
            self.assertTrue(os.path.exists(csv_file))

if __name__ == '__main__':
    unittest.main()
```

### 2. Integration Tests

```python
class TestPipelineIntegration(unittest.TestCase):
    
    def test_full_pipeline(self):
        """Test entire pipeline end-to-end"""
        from vnstock_pipeline.core.scheduler import Scheduler
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            scheduler = Scheduler(
                SmartCachedFetcher(),
                StrictValidator(),
                OptimizedTransformer(),
                ProductionExporter(tmpdir)
            )
            
            # Run on single stock
            scheduler.run(['VCB'])
            
            # Verify output
            import os
            csv_file = os.path.join(tmpdir, "csv", "VCB.csv")
            self.assertTrue(os.path.exists(csv_file))
            
            # Verify data
            df = pd.read_csv(csv_file)
            self.assertGreater(len(df), 0)
            self.assertIn('sma20', df.columns)
```

### 3. Load Tests

```python
import time

class TestPerformance(unittest.TestCase):
    
    def test_fetch_speed(self):
        """Test fetch speed acceptable"""
        fetcher = SmartCachedFetcher()
        
        start = time.time()
        df = fetcher._vn_call("VCB", start="2024-01-01", end="2024-12-02")
        elapsed = time.time() - start
        
        self.assertLess(elapsed, 2.0)  # Should complete within 2 seconds
    
    def test_transform_speed(self):
        """Test transform speed on large data"""
        transformer = OptimizedTransformer()
        
        # Create large DataFrame
        large_df = pd.DataFrame({
            'time': pd.date_range('2020-01-01', periods=10000),
            'open': np.random.uniform(50, 100, 10000),
            'high': np.random.uniform(100, 110, 10000),
            'low': np.random.uniform(40, 50, 10000),
            'close': np.random.uniform(50, 100, 10000),
            'volume': np.random.randint(1000000, 100000000, 10000)
        })
        
        start = time.time()
        result = transformer.transform(large_df)
        elapsed = time.time() - start
        
        self.assertLess(elapsed, 1.0)  # Should complete within 1 second
```

---

## IV. Deployment

### 1. Docker Container

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy code
COPY vnstock_pipeline/ ./vnstock_pipeline/
COPY pipeline_script.py .

# Create data directory
RUN mkdir -p /app/data

# Run pipeline
CMD ["python", "pipeline_script.py"]
```

**requirements.txt**:
```
vnstock>=3.2.0
pandas>=1.3.0
numpy>=1.20.0
requests>=2.27.0
websocket-client>=1.0.0
```

**Build & Run**:
```bash
docker build -t vnstock-pipeline:latest .
docker run -v $(pwd)/data:/app/data vnstock-pipeline:latest
```

### 2. Scheduled Pipeline

```python
# pipeline_script.py
import schedule
import time
import logging
from datetime import datetime
from vnstock_pipeline.core.scheduler import Scheduler
# ... imports

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def run_daily_pipeline():
    """Run pipeline daily"""
    logger.info("Starting daily pipeline")
    
    scheduler = Scheduler(
        SmartCachedFetcher(),
        StrictValidator(),
        OptimizedTransformer(),
        ProductionExporter("./data")
    )
    
    all_tickers = get_vn_all()
    
    for batch_num, batch in enumerate(batch_tickers(all_tickers, 100)):
        try:
            scheduler.run(batch)
            logger.info(f"Completed batch {batch_num+1}")
        except Exception as e:
            logger.error(f"Batch {batch_num+1} failed: {e}")
    
    logger.info("Pipeline completed")

# Schedule
schedule.every().day.at("16:30").do(run_daily_pipeline)

# Run scheduler
if __name__ == "__main__":
    logger.info("Pipeline scheduler started")
    
    while True:
        schedule.run_pending()
        time.sleep(60)
```

### 3. Monitoring

```python
import psutil
import logging

class PipelineMonitor:
    def __init__(self):
        self.start_time = None
        self.start_memory = None
    
    def start(self):
        self.start_time = time.time()
        self.start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    
    def log_stats(self):
        elapsed = time.time() - self.start_time
        current_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_used = current_memory - self.start_memory
        
        logger.info(f"Elapsed: {elapsed:.1f}s | Memory used: {memory_used:.1f}MB")
    
    def end(self):
        elapsed = time.time() - self.start_time
        current_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_used = current_memory - self.start_memory
        
        logger.info(f"✅ Pipeline completed in {elapsed:.1f}s using {memory_used:.1f}MB")

# Usage
monitor = PipelineMonitor()
monitor.start()

# ... run pipeline ...

monitor.log_stats()  # Check during execution
monitor.end()       # Final summary
```

---

## V. Troubleshooting

### 1. Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **Timeout** | API slow or network issue | Increase timeout, add retries |
| **Memory error** | Too many workers / large data | Reduce workers, process in batches |
| **Missing data** | Ticker not exist or no data | Validate ticker, check date range |
| **Validation fail** | Bad data quality | Check validator rules, inspect source |
| **Export fail** | Disk full or permission | Check disk space, verify paths |

### 2. Debugging

```python
# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Inspect at each step
class DebugTransformer(VNTransformer):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        logger.debug(f"Input shape: {data.shape}")
        logger.debug(f"Input columns: {list(data.columns)}")
        logger.debug(f"First row: {data.iloc[0].to_dict()}")
        
        df = super().transform(data)
        
        logger.debug(f"Output shape: {df.shape}")
        logger.debug(f"Output columns: {list(df.columns)}")
        
        return df
```

### 3. Health Check

```python
class HealthCheck:
    @staticmethod
    def check_data_freshness(df: pd.DataFrame) -> bool:
        """Check if data is recent"""
        from datetime import datetime, timedelta
        
        latest_time = df['time'].max()
        age = datetime.now() - latest_time.to_pydatetime()
        
        # Data should be from today or yesterday
        return age < timedelta(days=2)
    
    @staticmethod
    def check_data_continuity(df: pd.DataFrame) -> bool:
        """Check for gaps in data"""
        df_sorted = df.sort_values('time')
        gaps = df_sorted['time'].diff().dt.days
        
        # For daily data, allow gaps <= 3 (weekends/holidays)
        return (gaps <= 3).all()
    
    @staticmethod
    def check_all(df: pd.DataFrame) -> dict:
        return {
            'freshness': HealthCheck.check_data_freshness(df),
            'continuity': HealthCheck.check_data_continuity(df),
            'rows': len(df),
            'latest_date': df['time'].max()
        }

# Usage
health = HealthCheck.check_all(df)
if health['freshness'] and health['continuity']:
    print("✅ Data health check passed")
else:
    print(f"⚠️ Health issues: {health}")
```

