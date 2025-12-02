# 05. Best Practices & Tips

Tài liệu này tổng hợp các kỹ thuật tốt nhất để sử dụng vnstock_news hiệu quả và an toàn.

---

## 1. Chiến Lược Thu Thập Dữ Liệu

### Chọn Phương Thức Phù Hợp

| Mục Tiêu | Phương Thức | Ưu Điểm | Nhược Điểm |
|----------|-------------|---------|-----------|
| Cập nhật hàng ngày | RSS | Nhanh, cập nhật tự động | Chỉ bài mới |
| Xây dựng database | Sitemap batch | Lấy lịch sử, đầy đủ | Chậm, phức tạp |
| Real-time monitoring | Async batch | Nhanh, concurrent | Phức tạp |
| Sản xuất hàng ngày | Scheduler + RSS | Tự động, tin tươi | Cần thiết lập |

---

### Ví Dụ 1: Daily Update (RSS + Scheduler)

```python
# daily_update.py
from vnstock_news import Crawler
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
from datetime import datetime
import os

scheduler = BackgroundScheduler()

def update_news_daily():
    """Cập nhật tin hàng ngày"""
    
    print(f"⏰ Update at {datetime.now()}")
    
    sites = ["cafef", "tuoitre", "vietstock"]
    all_articles = []
    
    for site_name in sites:
        try:
            crawler = Crawler(site_name=site_name)
            articles = crawler.get_articles_from_feed(limit_per_feed=20)
            articles['source'] = site_name
            all_articles.append(articles)
            print(f"✅ {site_name}: {len(articles)} articles")
        except Exception as e:
            print(f"❌ {site_name}: {e}")
    
    if all_articles:
        result = pd.concat(all_articles, ignore_index=True)
        
        # Lưu vào file theo ngày
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"news_updates/{date_str}.csv"
        
        os.makedirs("news_updates", exist_ok=True)
        result.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"💾 Saved to {filename}")

# Lên lịch chạy mỗi ngày lúc 8:00 AM
scheduler.add_job(update_news_daily, 'cron', hour=8, minute=0)
scheduler.start()

# Chạy trong nền
try:
    print("📰 News update scheduler started...")
    while True:
        import time
        time.sleep(1)
except KeyboardInterrupt:
    scheduler.shutdown()
```

**Chạy:**
```bash
python daily_update.py
```

---

### Ví Dụ 2: Build Historical Database (Sitemap)

```python
# build_database.py
from vnstock_news import AsyncBatchCrawler, SITES_CONFIG
from datetime import datetime, timedelta
import asyncio
import pandas as pd

async def build_database():
    """Xây dựng database tin tức từ 3 tháng gần đây"""
    
    sites = ["cafef", "tuoitre", "vietstock"]
    all_articles = []
    
    for site_name in sites:
        print(f"⏳ Building {site_name}...")
        
        crawler = AsyncBatchCrawler(
            site_name=site_name,
            max_concurrency=5,
            request_delay=1.0
        )
        
        try:
            articles = await crawler.fetch_articles_async(
                site_name=site_name,
                max_articles=1000  # Lấy tối đa 1000 bài
            )
            articles['source'] = site_name
            all_articles.append(articles)
            
            print(f"✅ {site_name}: {len(articles)} articles")
            print(f"   Date range: {articles['publish_time'].min()} to {articles['publish_time'].max()}")
            
        except Exception as e:
            print(f"❌ {site_name}: {e}")
    
    if all_articles:
        result = pd.concat(all_articles, ignore_index=True)
        
        # Xóa duplicate
        result = result.drop_duplicates(subset=['url'])
        
        # Lưu
        result.to_csv("news_database_3months.csv", index=False, encoding='utf-8-sig')
        
        print(f"\n✅ Database built: {len(result)} articles")
        print(f"   Date range: {result['publish_time'].min()} to {result['publish_time'].max()}")
        print(f"   Sources: {result['source'].value_counts().to_dict()}")

# Chạy
asyncio.run(build_database())
```

---

## 2. Rate Limiting & Tránh Block IP

### Chiến Lược 1: Thêm Delay

```python
from vnstock_news import BatchCrawler
import time

crawler = BatchCrawler(
    site_name="cafef",
    request_delay=2.0,  # Delay 2 giây giữa mỗi request
    timeout=30
)

articles = crawler.fetch_articles(limit=500)
```

**Hướng dẫn:**
- `request_delay=0.5`: Nhanh nhất, rủi ro block
- `request_delay=1.0`: Cân bằng
- `request_delay=2.0`: An toàn, chập nhận chậm
- `request_delay=5.0`: Rất an toàn, rất chậm

---

### Chiến Lược 2: Giảm Concurrency

```python
import asyncio
from vnstock_news import AsyncBatchCrawler

async def safe_fetch():
    crawler = AsyncBatchCrawler(
        site_name="cafef",
        max_concurrency=2,    # Chỉ 2 requests cùng lúc
        request_delay=1.0
    )
    
    articles = await crawler.fetch_articles_async(
        site_name="cafef",
        max_articles=500
    )
    
    return articles

articles = asyncio.run(safe_fetch())
```

---

### Chiến Lược 3: Xử Lý Rate Limit

```python
from vnstock_news import BatchCrawler
from requests.exceptions import HTTPError
import time

def fetch_with_retry(site_name, limit):
    """Fetch với xử lý rate limit"""
    
    crawler = BatchCrawler(
        site_name=site_name,
        request_delay=1.5,
        timeout=30
    )
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            articles = crawler.fetch_articles(limit=limit)
            return articles
            
        except HTTPError as e:
            if e.response.status_code == 429:  # Rate limit
                retry_count += 1
                wait_time = 3600 * retry_count  # Chờ 1h, 2h, 3h
                print(f"⚠️ Rate limited, waiting {wait_time}s before retry {retry_count}...")
                time.sleep(wait_time)
            else:
                raise
    
    raise Exception(f"Failed after {max_retries} retries")

# Sử dụng
articles = fetch_with_retry("cafef", limit=500)
```

---

### Chiến Lược 4: Kiểm Tra Robots.txt

```python
import requests
from urllib.parse import urljoin

def check_robots_txt(domain):
    """Kiểm tra robots.txt"""
    
    try:
        robots_url = urljoin(domain, '/robots.txt')
        resp = requests.get(robots_url, timeout=10)
        
        rules = {
            'disallow': [],
            'crawl_delay': None
        }
        
        for line in resp.text.split('\n'):
            line = line.strip()
            
            if line.lower().startswith('disallow:'):
                path = line.split(':', 1)[1].strip()
                rules['disallow'].append(path)
            
            elif line.lower().startswith('crawl-delay:'):
                delay = float(line.split(':', 1)[1].strip())
                rules['crawl_delay'] = delay
        
        print(f"Robots.txt of {domain}:")
        print(f"  Disallow: {rules['disallow']}")
        print(f"  Crawl-delay: {rules['crawl_delay']}")
        
        return rules
        
    except Exception as e:
        print(f"Cannot fetch robots.txt: {e}")
        return None

# Sử dụng
rules = check_robots_txt("https://cafef.vn")
```

---

## 3. Caching & Performance

### Bật Caching

```python
from vnstock_news import EnhancedNewsCrawler
import asyncio

async def fetch_with_cache():
    crawler = EnhancedNewsCrawler(
        cache_enabled=True,
        cache_ttl=7200,           # Cache 2 giờ
        cache_dir="./news_cache"  # Thư mục cache
    )
    
    # Lần đầu: tải từ web, lưu cache
    articles1 = await crawler.fetch_articles_async(
        sources=["https://cafef.vn/latest-news-sitemap.xml"],
        site_name="cafef",
        max_articles=100
    )
    
    # Lần thứ 2 (trong 2 giờ): tải từ cache, nhanh hơn
    articles2 = await crawler.fetch_articles_async(
        sources=["https://cafef.vn/latest-news-sitemap.xml"],
        site_name="cafef",
        max_articles=100
    )
    
    return articles2

articles = asyncio.run(fetch_with_cache())
```

---

### Xóa Cache Cũ

```python
import os
from pathlib import Path
from datetime import datetime, timedelta

def clean_old_cache(cache_dir="./news_cache", days=7):
    """Xóa cache cũ hơn N ngày"""
    
    cutoff_time = datetime.now() - timedelta(days=days)
    deleted_count = 0
    
    for file_path in Path(cache_dir).iterdir():
        if file_path.is_file():
            file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            if file_time < cutoff_time:
                file_path.unlink()
                deleted_count += 1
                print(f"🗑️ Deleted: {file_path.name}")
    
    print(f"✅ Cleaned {deleted_count} cache files")

# Chạy hàng ngày
clean_old_cache(cache_dir="./news_cache", days=7)
```

---

## 4. Error Handling & Resumption

### Xử Lý Lỗi Cơ Bản

```python
from vnstock_news import Crawler
from requests.exceptions import (
    RequestException, Timeout, ConnectionError
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_safely(site_name, method='feed'):
    """Fetch với xử lý lỗi"""
    
    try:
        crawler = Crawler(site_name=site_name)
        
        if method == 'feed':
            articles = crawler.get_articles_from_feed(limit_per_feed=20)
        elif method == 'sitemap':
            articles = crawler.get_articles_from_sitemap(limit=100)
        
        logger.info(f"✅ {site_name}: {len(articles)} articles")
        return articles
        
    except ConnectionError:
        logger.error(f"❌ Connection error for {site_name}")
        return None
    
    except Timeout:
        logger.error(f"❌ Timeout for {site_name}")
        return None
    
    except Exception as e:
        logger.error(f"❌ Unexpected error for {site_name}: {e}")
        return None

# Sử dụng
for site in ["cafef", "tuoitre", "vietstock"]:
    articles = fetch_safely(site)
    if articles is not None:
        articles.to_csv(f"{site}_articles.csv", index=False)
```

---

### Resume Từ Nơi Dừng

```python
from vnstock_news import BatchCrawler
import pandas as pd
import os

def fetch_with_resume(site_name, limit=1000):
    """Fetch từ sitemap, có khả năng resume"""
    
    # Kiểm tra progress file
    progress_file = f"progress_{site_name}.txt"
    start_index = 0
    
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            start_index = int(f.read().strip())
        print(f"📌 Resuming from index {start_index}")
    
    # Tạo crawler
    crawler = BatchCrawler(
        site_name=site_name,
        request_delay=1.5
    )
    
    all_articles = []
    
    # Load existing data nếu có
    output_file = f"{site_name}_articles.csv"
    if os.path.exists(output_file):
        all_articles = [pd.read_csv(output_file)]
    
    try:
        # Fetch từ start_index
        new_articles = crawler.fetch_articles(limit=limit)
        all_articles.append(new_articles)
        
        # Gộp và lưu
        result = pd.concat(all_articles, ignore_index=True)
        result = result.drop_duplicates(subset=['url'])
        result.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        # Update progress
        with open(progress_file, 'w') as f:
            f.write(str(start_index + len(new_articles)))
        
        print(f"✅ Fetched {len(new_articles)} new articles")
        print(f"📊 Total: {len(result)} articles")
        
    except KeyboardInterrupt:
        print("⚠️ Interrupted by user")
        # Progress đã lưu, có thể resume lại
    
    except Exception as e:
        print(f"❌ Error: {e}")

# Sử dụng
fetch_with_resume("cafef", limit=2000)
```

---

## 5. Deduplication & Data Cleaning

### Loại Bỏ Bài Trùng

```python
import pandas as pd

def deduplicate_articles(df):
    """Loại bỏ bài trùng"""
    
    before = len(df)
    
    # Cách 1: Drop duplicate URLs
    df = df.drop_duplicates(subset=['url'])
    
    # Cách 2: Drop duplicate titles (nếu tiêu đề giống hệt)
    df = df.drop_duplicates(subset=['title'])
    
    after = len(df)
    
    print(f"✅ Removed {before - after} duplicates")
    print(f"📊 Remaining: {after} articles")
    
    return df

# Sử dụng
articles = pd.read_csv("all_articles.csv")
articles = deduplicate_articles(articles)
articles.to_csv("all_articles_dedup.csv", index=False)
```

---

### Làm Sạch Nội Dung

```python
import re
import pandas as pd

def clean_content(text):
    """Làm sạch nội dung"""
    
    if pd.isna(text):
        return ""
    
    # Xóa HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Xóa các ký tự đặc biệt không cần thiết
    text = re.sub(r'[\n\r\t]+', ' ', text)
    
    # Xóa khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Xóa các emoji
    text = re.sub(r'[^\w\s\u0100-\uFFFF.,!?;:\'-]', '', text)
    
    return text

def clean_articles(df):
    """Làm sạch toàn bộ DataFrame"""
    
    for col in ['title', 'short_description', 'content']:
        if col in df.columns:
            df[col] = df[col].apply(clean_content)
    
    return df

# Sử dụng
articles = pd.read_csv("raw_articles.csv")
articles = clean_articles(articles)
articles.to_csv("clean_articles.csv", index=False)
```

---

## 6. Timezone Handling

### Chuẩn Hóa Timezone

```python
import pandas as pd
from datetime import datetime
import pytz

def normalize_timezone(df, target_tz='Asia/Ho_Chi_Minh'):
    """Chuẩn hóa timezone"""
    
    # Convert sang datetime
    df['publish_time'] = pd.to_datetime(df['publish_time'])
    
    # Đặt timezone nếu chưa có
    if df['publish_time'].dt.tz is None:
        df['publish_time'] = df['publish_time'].dt.tz_localize('UTC')
    
    # Convert sang target timezone
    df['publish_time'] = df['publish_time'].dt.tz_convert(target_tz)
    
    return df

# Sử dụng
articles = pd.read_csv("articles.csv")
articles = normalize_timezone(articles, target_tz='Asia/Ho_Chi_Minh')
print(articles['publish_time'].head())
```

**Output:**
```
0   2025-01-15 10:30:00+07:00
1   2025-01-15 09:15:00+07:00
```

---

## 7. Production Deployment

### Ví Dụ: News Aggregator Service

```python
# news_service.py
from vnstock_news import AsyncBatchCrawler, TrendingAnalyzer
from vnstock_news.api.enhanced import EnhancedNewsCrawler
import asyncio
import pandas as pd
from datetime import datetime
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsAggregatorService:
    """Service để tập hợp tin tức từ nhiều báo"""
    
    def __init__(self, output_dir="./news_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.sites = ["cafef", "tuoitre", "vietstock"]
        self.analyzer = TrendingAnalyzer()
    
    async def fetch_all_news(self):
        """Lấy tin từ tất cả báo"""
        
        logger.info("Starting news fetch...")
        all_articles = []
        
        for site_name in self.sites:
            try:
                logger.info(f"Fetching from {site_name}...")
                
                crawler = AsyncBatchCrawler(
                    site_name=site_name,
                    max_concurrency=3,
                    request_delay=1.0
                )
                
                articles = await crawler.fetch_articles_async(
                    site_name=site_name,
                    max_articles=100
                )
                
                articles['source'] = site_name
                all_articles.append(articles)
                
                logger.info(f"✅ {site_name}: {len(articles)} articles")
                
            except Exception as e:
                logger.error(f"❌ {site_name}: {e}")
        
        if not all_articles:
            logger.error("No articles fetched")
            return None
        
        # Gộp
        result = pd.concat(all_articles, ignore_index=True)
        result = result.drop_duplicates(subset=['url'])
        
        logger.info(f"📊 Total: {len(result)} articles from {len(self.sites)} sources")
        
        return result
    
    async def analyze_trending(self, articles):
        """Phân tích trending"""
        
        logger.info("Analyzing trending keywords...")
        
        if articles is None or len(articles) == 0:
            logger.warning("No articles to analyze")
            return None
        
        keywords = self.analyzer.extract_keywords(
            articles['title'].tolist(),
            top_n=20
        )
        
        return keywords
    
    async def save_results(self, articles, keywords):
        """Lưu kết quả"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Lưu articles
        articles_file = self.output_dir / f"articles_{timestamp}.csv"
        articles.to_csv(articles_file, index=False, encoding='utf-8-sig')
        logger.info(f"📁 Saved articles to {articles_file}")
        
        # Lưu keywords
        keywords_df = pd.DataFrame([
            {'keyword': k, 'frequency': v}
            for k, v in keywords.items()
        ])
        keywords_file = self.output_dir / f"keywords_{timestamp}.csv"
        keywords_df.to_csv(keywords_file, index=False)
        logger.info(f"📁 Saved keywords to {keywords_file}")
    
    async def run(self):
        """Chạy service"""
        
        try:
            articles = await self.fetch_all_news()
            
            if articles is not None:
                keywords = await self.analyze_trending(articles)
                
                if keywords is not None:
                    await self.save_results(articles, keywords)
                    
                    logger.info("✅ Service completed successfully")
                    return True
        
        except Exception as e:
            logger.error(f"❌ Service failed: {e}")
            return False

# Chạy
if __name__ == "__main__":
    service = NewsAggregatorService()
    success = asyncio.run(service.run())
    
    exit(0 if success else 1)
```

**Chạy:**
```bash
python news_service.py
```

---

### Chạy Định Kỳ (Cron Job)

```bash
# Crontab: Chạy mỗi ngày lúc 8:00 AM
0 8 * * * cd /path/to/project && python news_service.py >> logs/news_service.log 2>&1
```

---

## 8. Monitoring & Logging

### Setup Logging

```python
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(log_dir="./logs"):
    """Setup logging"""
    
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger("vnstock_news")
    logger.setLevel(logging.DEBUG)
    
    # File handler
    fh = RotatingFileHandler(
        os.path.join(log_dir, "vnstock_news.log"),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    fh.setLevel(logging.DEBUG)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

# Sử dụng
logger = setup_logging()
logger.info("Starting news crawler...")
logger.error("Error occurred!")
```

---

## 9. Checklist - Trước Khi Deploy

- [ ] Test với dữ liệu thực
- [ ] Kiểm tra error handling
- [ ] Cấu hình request_delay phù hợp
- [ ] Kiểm tra robots.txt
- [ ] Bật caching
- [ ] Setup logging
- [ ] Chuẩn bị deduplication
- [ ] Test resume/retry logic
- [ ] Kiểm tra timezone
- [ ] Có backup strategy
- [ ] Có monitoring
- [ ] Có alert nếu lỗi

---

## Tổng Kết

**Best Practices:**
1. ✅ Chọn phương thức phù hợp (RSS/Sitemap/Batch)
2. ✅ Tuân thủ rate limiting (request_delay, concurrency)
3. ✅ Bật caching để tiết kiệm bandwidth
4. ✅ Xử lý lỗi & có khả năng resume
5. ✅ Loại bỏ duplicate & làm sạch dữ liệu
6. ✅ Setup logging & monitoring
7. ✅ Kiểm tra robots.txt & ToS
8. ✅ Deploy với scheduler (cron, APScheduler)
9. ✅ Test kỹ trước production
