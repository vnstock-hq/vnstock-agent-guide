# 02. Các Loại Crawler & API

Tài liệu này mô tả chi tiết tất cả các crawler và cách sử dụng từng loại.

---

## 1. Crawler - Unified Interface

`Crawler` là lớp chính đơn giản nhất, hỗ trợ cả RSS và Sitemap.

### Khởi Tạo

```python
from vnstock_news import Crawler

# Cách 1: Dùng site_name (có sẵn config)
crawler = Crawler(site_name="cafef")

# Cách 2: Custom config cho site mới
custom_config = {
    "name": "My Custom News",
    "domain": "mynews.com",
    "rss": {
        "urls": ["https://mynews.com/feed.xml"]
    },
    "sitemap_url": "https://mynews.com/sitemap.xml"
}
crawler = Crawler(custom_config=custom_config)
```

### Các Phương Thức

#### `get_articles_from_feed(limit_per_feed=20, timeout=10)`

Lấy tin từ RSS feed.

```python
articles = crawler.get_articles_from_feed(limit_per_feed=10)
print(articles.head())
```

**Output:**
```
                              url                    title  publish_time
0  https://cafef.vn/investment/...  Thị trường chứng khoán...  2025-01-15
1  https://cafef.vn/investment/...  Nhà đầu tư tiếp tục...  2025-01-15
```

**Parameters:**
- `limit_per_feed` (int): Lấy tối đa bao nhiêu bài từ mỗi RSS feed
- `timeout` (int): Timeout cho mỗi request (giây)

**Returns:** `pd.DataFrame` với cột `[url, title, short_description, publish_time, author]`

---

#### `get_articles_from_sitemap(limit=100, start_date=None, end_date=None, timeout=10)`

Lấy tin từ XML sitemap.

```python
from datetime import datetime, timedelta

# Lấy 100 bài gần đây nhất
articles = crawler.get_articles_from_sitemap(limit=100)

# Lấy bài từ tháng 1/2025
articles = crawler.get_articles_from_sitemap(
    limit=200,
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 1, 31)
)

print(f"Lấy được {len(articles)} bài")
print(articles[['title', 'publish_time']].head())
```

**Output:**
```
                    title      publish_time
0  Chứng khoán tăng trưởng...  2025-01-15
1  Nhà đầu tư nước ngoài...  2025-01-14
```

**Parameters:**
- `limit` (int): Tối đa bao nhiêu URL từ sitemap
- `start_date` (datetime): Lọc bài từ ngày này trở đi
- `end_date` (datetime): Lọc bài đến ngày này
- `timeout` (int): Timeout

**Returns:** `pd.DataFrame`

---

## 2. RSS - RSS Feed Parser

Parser chuyên biệt cho RSS feed, trả về danh sách feed URLs với metadata.

### Khởi Tạo

```python
from vnstock_news import RSS

rss = RSS(site_name="vnexpress")
# hoặc
rss = RSS(feed_urls=["https://vnexpress.net/rss/tin-moi-nhat.rss"])
```

### Phương Thức

#### `get_all_articles(limit_per_feed=20)`

```python
articles = rss.get_all_articles(limit_per_feed=15)

print(articles.shape)  # (N, 5)
print(articles.columns)  # url, title, short_description, publish_time, author
```

---

## 3. Sitemap - XML Sitemap Parser

Parser chuyên biệt cho XML sitemap.

### Khởi Tạo

```python
from vnstock_news import Sitemap

sitemap = Sitemap(sitemap_url="https://cafef.vn/latest-news-sitemap.xml")
```

### Phương Thức

#### `get_urls(limit=None, start_date=None, end_date=None)`

Lấy URLs từ sitemap với bộ lọc ngày.

```python
from datetime import datetime

# Lấy 100 URL đầu tiên
urls = sitemap.get_urls(limit=100)

# Lấy URLs từ 1-31/1/2025
urls = sitemap.get_urls(
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 1, 31)
)

print(f"Lấy được {len(urls)} URLs")
for url in urls[:5]:
    print(url)
```

**Output:**
```
https://cafef.vn/investment/stock/top-10-co-phieu-tang-gia-tuan-qua...
https://cafef.vn/investment/stock/nha-dau-tu-nhat-phuc-tiet-lo...
```

---

## 4. News - Article Content Parser

Parse nội dung chi tiết của một bài viết.

### Khởi Tạo

```python
from vnstock_news import News

news_parser = News(site_name="cafef")
# hoặc dùng custom config
news_parser = News(config={
    "selectors": {
        "title": "h1.title",
        "content": "div.article-content",
        "author": "span.author-name"
    }
})
```

### Phương Thức

#### `parse(url)`

Parse nội dung từ một URL.

```python
url = "https://cafef.vn/investment/stock/tin-tuc..."
article = news_parser.parse(url)

print(article)
# {
#   'url': 'https://cafef.vn/...',
#   'title': 'Chứng khoán tăng 1%',
#   'content': 'Thị trường chứng khoán hôm nay...',
#   'publish_time': datetime(2025, 1, 15),
#   'author': 'Nguyễn Văn A'
# }
```

---

## 5. BatchCrawler - Batch Processing (Đồng Bộ)

Lấy hàng loạt bài từ một trang báo, với hỗ trợ resume nếu bị lỗi.

### Khởi Tạo

```python
from vnstock_news import BatchCrawler

crawler = BatchCrawler(
    site_name="cafef",
    request_delay=1.5,      # Delay 1.5s giữa mỗi request
    timeout=30,             # Timeout 30s
    output_dir="./data",    # Lưu kết quả vào thư mục này
    debug=False             # Tắt debug output
)
```

### Phương Thức

#### `fetch_articles(limit=100, use_rss=True, use_sitemap=True, output_file=None)`

Tải bài viết theo batch.

```python
# Tải 100 bài mới nhất (dùng RSS trước)
articles = crawler.fetch_articles(limit=100)

# Tải 500 bài từ sitemap
articles = crawler.fetch_articles(
    limit=500,
    use_rss=False,
    use_sitemap=True,
    output_file="articles_batch.csv"
)

print(f"✅ Lấy được {len(articles)} bài")
print(articles.info())
```

**Parameters:**
- `limit` (int): Tối đa bao nhiêu bài
- `use_rss` (bool): Dùng RSS trước hay không
- `use_sitemap` (bool): Dùng sitemap hay không
- `output_file` (str): Lưu vào file nào (nếu None thì dùng default)

**Returns:** `pd.DataFrame`

---

#### `fetch_articles_batch(batch_size=10, max_workers=2)`

Lấy từng batch nhỏ.

```python
# Lấy theo batch 50 bài, 2 workers
batches = crawler.fetch_articles_batch(
    batch_size=50,
    max_workers=2
)

for i, batch in enumerate(batches):
    print(f"Batch {i}: {len(batch)} bài")
    batch.to_csv(f"batch_{i}.csv", index=False)
```

---

## 6. AsyncBatchCrawler - Batch Processing (Bất Đồng Bộ)

Lấy hàng loạt bài **nhanh hơn gấp 5-10 lần** bằng concurrent requests.

### Khởi Tạo

```python
from vnstock_news import AsyncBatchCrawler

crawler = AsyncBatchCrawler(
    site_name="cafef",
    max_concurrency=5,      # Tối đa 5 requests cùng lúc
    request_delay=0.5,      # Delay giữa requests (để tránh block)
    timeout=30
)
```

### Phương Thức

#### `fetch_articles_async(sources=None, top_n=100, site_name=None)`

```python
import asyncio

async def main():
    crawler = AsyncBatchCrawler(site_name="cafef")
    
    articles = await crawler.fetch_articles_async(
        top_n=200,  # Lấy 200 bài
        site_name="cafef"
    )
    
    print(f"✅ Lấy được {len(articles)} bài trong {articles['publish_time'].max() - articles['publish_time'].min()}")
    return articles

# Chạy
articles = asyncio.run(main())
articles.to_csv("cafef_async.csv", index=False)
```

**Output:**
```
✅ Lấy được 187 bài trong 45 days, 12:34:56
```

---

#### `fetch_articles_concurrently(urls, max_concurrency=5)`

Lấy content chi tiết từ danh sách URLs nhanh chóng.

```python
import asyncio

async def main():
    urls = [
        "https://cafef.vn/article1",
        "https://cafef.vn/article2",
        # ... nhiều URLs khác
    ]
    
    crawler = AsyncBatchCrawler(site_name="cafef")
    articles = await crawler.fetch_articles_concurrently(
        urls=urls,
        max_concurrency=10  # 10 requests cùng lúc
    )
    
    return articles

articles = asyncio.run(main())
```

---

## 7. EnhancedNewsCrawler - Advanced API

API cao cấp với đầy đủ tính năng: caching, validation, content cleaning.

### Khởi Tạo

```python
from vnstock_news import EnhancedNewsCrawler

crawler = EnhancedNewsCrawler(
    cache_enabled=True,           # Bật caching
    cache_ttl=7200,               # Cache 2 giờ
    cache_dir="./cache",          # Thư mục cache
    max_retries=3,                # Retry 3 lần nếu lỗi
    timeout=30,
    user_agent=None               # Tự động rotate user-agent
)
```

### Phương Thức

#### `fetch_articles_async(sources, site_name, max_articles=100, time_frame="24h", clean_content=True)`

Lấy bài với đầy đủ tính năng.

```python
import asyncio

async def main():
    crawler = EnhancedNewsCrawler(cache_enabled=True)
    
    articles = await crawler.fetch_articles_async(
        sources=["https://cafef.vn/latest-news-sitemap.xml"],
        site_name="cafef",
        max_articles=100,
        time_frame="7d",           # Lấy bài từ 7 ngày gần đây
        clean_content=True         # Xóa HTML, chuẩn hóa nội dung
    )
    
    print(f"✅ Lấy {len(articles)} bài từ cache/web")
    return articles

articles = asyncio.run(main())
```

**Features:**
- ✅ **Caching**: Lưu cache tránh lấy lại
- ✅ **Validation**: Kiểm tra dữ liệu hợp lệ
- ✅ **Content Cleaning**: Tự động xóa HTML, ký tự lạ
- ✅ **Retries**: Retry tự động nếu lỗi
- ✅ **Time Filtering**: Lọc theo khoảng thời gian

**Parameters:**
- `sources` (list): Danh sách URLs của sitemap/RSS
- `site_name` (str): Tên trang báo
- `max_articles` (int): Tối đa bao nhiêu bài
- `time_frame` (str): Khoảng thời gian ("24h", "7d", "30d", "all")
- `clean_content` (bool): Làm sạch content hay không

**Returns:** `pd.DataFrame`

---

## So Sánh Các Crawler

| Tiêu Chí | Crawler | RSS | Sitemap | BatchCrawler | AsyncBatchCrawler | Enhanced |
|---------|---------|-----|---------|--------------|-------------------|----------|
| **Tốc độ** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Dữ liệu lịch sử** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Đơn giản** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Caching** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Content Cleaning** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Async** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Resume Support** | ❌ | ❌ | ❌ | ✅ | ⚠️ | ✅ |

---

## Ví Dụ Thực Tế

### Ví Dụ 1: Lấy Nhanh 20 Bài Mới Từ VnExpress

```python
from vnstock_news import Crawler

crawler = Crawler(site_name="vnexpress")
articles = crawler.get_articles_from_feed(limit_per_feed=20)

print(f"✅ Lấy {len(articles)} bài")
print(articles[['title', 'publish_time']].head())
```

### Ví Dụ 2: Lấy 500 Bài Lịch Sử Từ CafeF

```python
from vnstock_news import BatchCrawler

crawler = BatchCrawler(
    site_name="cafef",
    request_delay=1.0
)

articles = crawler.fetch_articles(limit=500)
articles.to_csv("cafef_500_articles.csv", index=False)

print(f"✅ Lấy {len(articles)} bài")
print(f"Từ {articles['publish_time'].min()} đến {articles['publish_time'].max()}")
```

### Ví Dụ 3: Lấy Từ 3 Báo Cùng Lúc (Nhanh)

```python
import asyncio
from vnstock_news import AsyncBatchCrawler, SITES_CONFIG
import pandas as pd

async def fetch_all_sites():
    sites = ["cafef", "tuoitre", "vietstock"]
    all_articles = []
    
    for site_name in sites:
        crawler = AsyncBatchCrawler(
            site_name=site_name,
            max_concurrency=5
        )
        
        print(f"⏳ Đang lấy từ {site_name}...")
        articles = await crawler.fetch_articles_async(
            site_name=site_name,
            max_articles=100
        )
        articles['source'] = site_name
        all_articles.append(articles)
    
    result = pd.concat(all_articles, ignore_index=True)
    return result

articles = asyncio.run(fetch_all_sites())
articles.to_csv("all_sites_articles.csv", index=False)

print(f"✅ Tổng {len(articles)} bài từ {articles['source'].nunique()} báo")
print(articles['source'].value_counts())
```

---

## Xử Lý Lỗi

### Retry Tự Động

```python
from vnstock_news import EnhancedNewsCrawler
import asyncio

crawler = EnhancedNewsCrawler(
    max_retries=3,  # Retry 3 lần
    timeout=30
)

async def safe_fetch():
    try:
        articles = await crawler.fetch_articles_async(
            sources=["https://cafef.vn/latest-news-sitemap.xml"],
            site_name="cafef",
            max_articles=100
        )
        return articles
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return None

articles = asyncio.run(safe_fetch())
```

### Xử Lý Rate Limiting

```python
from vnstock_news import BatchCrawler
import time

crawler = BatchCrawler(
    site_name="cafef",
    request_delay=2.0,  # Delay 2 giây
    timeout=60
)

try:
    articles = crawler.fetch_articles(limit=1000)
except Exception as e:
    if "429" in str(e):
        print("⚠️ Bị rate limit, đợi 1 giờ...")
        time.sleep(3600)
        # Retry
        articles = crawler.fetch_articles(limit=1000)
```

---

## Tips Tối Ưu

1. **Chọn crawler đúng**:
   - Chỉ cần tin mới → `Crawler.get_articles_from_feed()`
   - Cần lịch sử → `BatchCrawler.fetch_articles()`
   - Cần nhanh + lịch sử → `AsyncBatchCrawler`
   - Cần cache + validation → `EnhancedNewsCrawler`

2. **Điều chỉnh request_delay**:
   - Tăng delay nếu bị 429 (rate limit)
   - Giảm delay nếu mạng nhanh

3. **Sử dụng cache**:
   - Tiết kiệm bandwidth
   - Tăng tốc độ
   - Tránh load server

4. **Batch processing**:
   - Xử lý dữ liệu theo batch nhỏ
   - Lưu thường xuyên
   - Tránh mất dữ liệu
