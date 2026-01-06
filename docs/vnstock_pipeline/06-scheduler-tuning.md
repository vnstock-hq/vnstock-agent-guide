# Vnstock Pipeline - Scheduler Performance Tuning (v2.1.5)

Scheduler trong vnstock_pipeline v2.1.5 cho phép tối ưu hóa hiệu suất và xử lý rate limiting một cách thông minh.

---

## I. Các Tham Số Scheduler

### 1. max_workers - Số Luồng Xử Lý

**Tác dụng**: Kiểm soát số request được gửi đồng thời.

| Giá Trị | Tốc Độ      | Rủi Ro   | Sử Dụng Khi                        |
| ------- | ----------- | -------- | ---------------------------------- |
| 1       | Chậm        | Rất thấp | Xử lý 500+ tickers hoặc API strict |
| 2-3     | Bình thường | Thấp     | Cấu hình mặc định, an toàn         |
| 5-8     | Nhanh       | Cao      | Xử lý < 50 tickers, API tolerant   |
| 10+     | Rất nhanh   | Rất cao  | Chỉ khi API cho phép               |

**Ví dụ**:

```python
# Tuần tự (an toàn nhất)
scheduler = Scheduler(..., max_workers=1)

# Chuẩn
scheduler = Scheduler(..., max_workers=3)

# Nhanh (rủi ro cao)
scheduler = Scheduler(..., max_workers=10)
```

### 2. request_delay - Độ Trễ Giữa Requests

**Tác dụng**: Thêm delay giữa các request để tránh bị rate limit.

| Giá Trị  | Thích Hợp Cho                |
| -------- | ---------------------------- |
| 0.1-0.3s | Ít dữ liệu (<20 tickers)     |
| 0.5-1.0s | Bình thường (50-200 tickers) |
| 1.0-2.0s | Nhiều dữ liệu (200+ tickers) |

**Ví dụ**:

```python
# Delay ngắn
scheduler = Scheduler(..., request_delay=0.1)

# Delay chuẩn
scheduler = Scheduler(..., request_delay=0.5)

# Delay dài
scheduler = Scheduler(..., request_delay=2.0)
```

### 3. rate_limit_wait - Thời Gian Chờ Khi Rate Limit

**Tác dụng**: Thời gian chờ trước khi retry khi API trả về rate limit (429).

| Giá Trị     | Ghi Chú                         |
| ----------- | ------------------------------- |
| 30 giây     | Tối thiểu (yêu cầu của API VCI) |
| 35-60 giây  | Khuyến nghị                     |
| 60-120 giây | Rất an toàn                     |

**Ví dụ**:

```python
# Tối thiểu (API VCI yêu cầu)
scheduler = Scheduler(..., rate_limit_wait=30.0)

# Chuẩn
scheduler = Scheduler(..., rate_limit_wait=35.0)

# An toàn
scheduler = Scheduler(..., rate_limit_wait=60.0)
```

---

## II. Chiến Lược Cấu Hình Cho Các Tình Huống

### Tình Huống A: Xử Lý Ít Dữ Liệu (< 50 tickers)

```python
from vnstock_pipeline.core.scheduler import Scheduler
from vnstock_pipeline.tasks.financial import (
    FinancialFetcher, FinancialValidator, 
    FinancialTransformer, FinancialExporter
)

tickers = ['VCB', 'ACB', 'HPG', 'FPT']

scheduler = Scheduler(
    FinancialFetcher(),
    FinancialValidator(),
    FinancialTransformer(),
    FinancialExporter(base_path="./data/financial"),
    max_workers=3,
    request_delay=0.5,
    rate_limit_wait=35.0
)

scheduler.run(tickers)
```

**Đặc điểm**:

- ✅ Nhanh (xử lý ~ 5-10 phút)
- ✅ An toàn (ít bị rate limit)
- ✅ Cân bằng tốt

### Tình Huống B: Xử Lý Nhiều Dữ Liệu (100-200 tickers)

```python
scheduler = Scheduler(
    FinancialFetcher(),
    FinancialValidator(),
    FinancialTransformer(),
    FinancialExporter(base_path="./data/financial"),
    max_workers=2,
    request_delay=1.0,
    rate_limit_wait=40.0
)

scheduler.run(tickers)
```

**Đặc điểm**:

- ✅ Tránh rate limit hiệu quả
- ✅ Xử lý nhanh (30-45 phút)
- ✅ Độ tin cậy cao

### Tình Huống C: Xử Lý Rất Nhiều Dữ Liệu (500+ tickers)

```python
scheduler = Scheduler(
    FinancialFetcher(),
    FinancialValidator(),
    FinancialTransformer(),
    FinancialExporter(base_path="./data/financial"),
    max_workers=1,
    request_delay=2.0,
    rate_limit_wait=120.0
)

scheduler.run(tickers)
```

**Đặc điểm**:

- ✅ An toàn nhất (tuần tự)
- ✅ Không bị rate limit
- ⚠️ Chậm (2-4 giờ cho 500 tickers)

### Tình Huống D: Tối Ưu Tốc Độ (với rủi ro cao)

```python
scheduler = Scheduler(
    FinancialFetcher(),
    FinancialValidator(),
    FinancialTransformer(),
    FinancialExporter(base_path="./data/financial"),
    max_workers=8,
    request_delay=0.1,
    rate_limit_wait=30.0
)

scheduler.run(tickers)
```

**Đặc điểm**:

- ⚠️ Nhanh nhất (3-5 phút)
- ⚠️ Rủi ro cao bị rate limit
- ⚠️ Chỉ dùng với API tolerant

---

## III. Override Tham Số Tại Thời Điểm Chạy

Bạn có thể thay đổi tham số mà không cần khởi tạo lại scheduler:

```python
scheduler = Scheduler(..., max_workers=3)

# Override để chạy nhanh hơn
scheduler.run(
    tickers,
    max_workers=5,
    request_delay=0.2,
    rate_limit_wait=35.0
)

# Override để chạy an toàn hơn
scheduler.run(
    other_tickers,
    max_workers=1,
    request_delay=1.5,
    rate_limit_wait=60.0
)
```

---

## IV. Xử Lý Batch Lớn

Khi xử lý 500+ tickers, chia thành batches để tránh bị block:

```python
import time
from vnstock_pipeline.core.scheduler import Scheduler

def batch_process(all_tickers, batch_size=50):
    scheduler = Scheduler(
        FinancialFetcher(),
        FinancialValidator(),
        FinancialTransformer(),
        FinancialExporter(base_path="./data/financial"),
        max_workers=1,
        request_delay=2.0,
        rate_limit_wait=120.0
    )
    
    total_batches = (len(all_tickers) - 1) // batch_size + 1
    
    for i in range(0, len(all_tickers), batch_size):
        batch = all_tickers[i:i+batch_size]
        batch_num = i // batch_size + 1
        
        print(f"Processing batch {batch_num}/{total_batches}")
        print(f"Tickers: {batch}")
        
        scheduler.run(batch)
        
        # Wait giữa batches để API phục hồi
        if i + batch_size < len(all_tickers):
            print(f"Waiting 60s before next batch...")
            time.sleep(60)
    
    print("✅ All batches completed!")

# Usage
all_tickers = ["ACB", "VCB", "HPG", ...]  # 500+ tickers
batch_process(all_tickers, batch_size=50)
```

**Lợi ích**:

- Tránh bị API block hoàn toàn
- Có thể monitor progress dễ hơn
- Nếu lỗi, chỉ cần rerun batch đó

---

## V. Công Thức Tính Tham Số

Nếu bạn biết API có bao nhiêu requests/second:

```
Giả sử API cho phép 1 request/second (RPS)

max_workers = min(3, RPS)
request_delay = 1 / (max_workers * RPS)
rate_limit_wait = 30 + (wait_time_from_API_header if available)

Ví dụ nếu API cho 2 RPS:
max_workers = 2
request_delay = 1 / (2 * 2) = 0.25 giây
rate_limit_wait = 30 giây
```

---

## VI. Debug Và Monitoring

### Enable Debug Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

scheduler = Scheduler(...)
scheduler.run(tickers)
```

### Capture Statistics

```python
class MonitoredScheduler(Scheduler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.success_count = 0
        self.failure_count = 0
        self.rate_limit_count = 0
    
    def run(self, tickers, **kwargs):
        # Your monitoring logic
        super().run(tickers, **kwargs)
        
        print(f"✅ Success: {self.success_count}")
        print(f"❌ Failed: {self.failure_count}")
        print(f"⏸️  Rate Limited: {self.rate_limit_count}")
```

### Test Performance

```python
import time

tickers = ['VCB', 'ACB', 'HPG', 'FPT', 'VNM']

scheduler = Scheduler(..., max_workers=3)

start = time.time()
scheduler.run(tickers)
elapsed = time.time() - start

print(f"Processed {len(tickers)} tickers in {elapsed:.2f}s")
print(f"Average: {elapsed/len(tickers):.2f}s per ticker")
```

---

## VII. Troubleshooting

### Gặp Rate Limit Thường Xuyên

**Giải pháp**:

```python
# Tăng delay và giảm workers
scheduler = Scheduler(
    ...,
    max_workers=1,
    request_delay=2.0,
    rate_limit_wait=60.0
)
```

### Xử Lý Quá Chậm

**Giải pháp**:

```python
# Tăng workers và giảm delay (nếu API cho phép)
scheduler = Scheduler(
    ...,
    max_workers=5,
    request_delay=0.3,
    rate_limit_wait=35.0
)
```

### Timeout Errors

**Giải pháp**:

```python
# Retry thêm lần
scheduler = Scheduler(
    ...,
    retry_attempts=5,  # Tăng từ 3 lên 5
    backoff_factor=2.0
)
```

---

## VIII. Best Practices

1. **Bắt đầu an toàn**: Dùng `max_workers=1` rồi tăng dần
2. **Monitor logs**: Kiểm tra rate limit warnings
3. **Test trước**: Thử với 5-10 tickers trước
4. **Batch large jobs**: Chia 500+ tickers thành 50-100 batches
5. **Ghi nhật ký**: Lưu logs để debug sau này
6. **Respect API**: Luôn để `rate_limit_wait >= 30`

---

## IX. Khuyến Nghị

| Dataset Size | max_workers | request_delay | rate_limit_wait |
| ------------ | ----------- | ------------- | --------------- |
| < 20         | 3-5         | 0.3-0.5       | 30              |
| 20-100       | 3           | 0.5           | 35              |
| 100-300      | 2           | 1.0           | 40              |
| 300+         | 1           | 2.0           | 60              |

---