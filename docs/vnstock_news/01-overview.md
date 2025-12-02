# Vnstock News - Hướng Dẫn Toàn Diện

## Giới Thiệu

**vnstock_news** là thư viện Python cung cấp khả năng thu thập tin tức từ các trang báo Việt Nam bằng hai phương pháp chính:

1. **RSS Feed Aggregation** - Kết nối trực tiếp đến các luồng RSS của báo
2. **Web Scraping via Sitemap** - Sử dụng sitemap (bản đồ chỉ mục web) để duyệt và lấy toàn bộ bài viết

### Đặc Điểm Chính

- **📰 Hỗ trợ 12+ trang báo**: VnExpress, Tuổi Trẻ, CafeF, VietStock, Báo Đầu Tư, VnEconomy, PLO, v.v.
- **🌐 Hai phương thức lấy dữ liệu**: RSS (cập nhật mới nhất) + Sitemap (lịch sử toàn bộ)
- **⚡ Hỗ trợ bất đồng bộ (async)**: Tải nhiều bài cùng lúc nhanh chóng
- **💾 Caching thông minh**: Lưu cache để tránh tải lại cùng một bài
- **🧹 Cleaning & Validation**: Tự động làm sạch, chuẩn hóa nội dung
- **📊 Phân tích xu hướng**: Tìm ra chủ đề/keyword phổ biến từ tin tức
- **🔄 Batch Processing**: Xử lý hàng loạt từ nhiều nguồn cùng lúc

**Tất cả các báo đều hỗ trợ cả RSS và Sitemap** vì đây là tiêu chuẩn web. vnstock_news cung cấp cấu hình sẵn cho 12+ báo phổ biến nhưng có thể tùy biến để làm việc với bất kỳ website/báo nào có nguồn RSS/sitemap để cung cấp bản đồ cho thuật toán đọc bài viết chi tiết.

### Cấu Trúc Package

```
vnstock_news/
├── __init__.py           # Khởi tạo, export main classes
├── main.py              # Module monitoring tin tức tự động
├── api/
│   └── enhanced.py      # EnhancedNewsCrawler - API cao cấp
├── core/                # Core modules
│   ├── base.py          # BaseParser - base class
│   ├── crawler.py       # Crawler - unified crawler
│   ├── batch.py         # BatchCrawler - đồng bộ batch
│   ├── rss.py           # RSS parser
│   ├── sitemap.py       # Sitemap parser
│   └── news.py          # News article parser
├── async_crawlers/      # Async implementations
│   └── async_batch.py   # AsyncBatchCrawler - bất đồng bộ batch
├── config/              # Cấu hình
│   ├── sites.py         # SITES_CONFIG - config cho tất cả báo
│   ├── sitemap_resolver.py  # Dynamic sitemap URL resolution
│   ├── dynamic_config.py    # Cấu hình động
│   ├── const.py         # Constants
│   └── vietnamese-stopwords.txt  # Vietnamese stopwords
├── trending/            # Phân tích xu hướng
│   └── analyzer.py      # TrendingAnalyzer
└── utils/               # Utilities
    ├── cache.py         # Caching system
    ├── cleaner.py       # ContentCleaner
    ├── validators.py    # Validation
    └── helpers.py       # Helper functions
```

---

## Các Loại Dữ Liệu Có Thể Lấy

### 1. **RSS Feed Data** (Tin Mới Nhất)

- ✅ Nhanh nhất, thường cập nhật hàng giờ
- ✅ Bài viết mới nhất từ báo
- ❌ Chỉ lấy được những bài mới trong vài ngày
- 💡 Dùng cho: Monitoring tin tức real-time, cập nhật hàng ngày

**Ví dụ**: RSS feed của VnExpress cập nhật tin mới nhất mỗi giờ

### 2. **Sitemap Data** (Lịch Sử - Năm nay, Năm ngoái)

- ✅ Lấy được toàn bộ bài viết có trong sitemap (thường là 1-2 năm gần nhất)
- ✅ Nhiều báo sắp xếp sitemap theo tháng/năm (ví dụ: `news-2024-12.xml`, `news-2025-01.xml`)
- ✅ Có thể lấy hàng ngàn bài cũ từ một nguồn
- ❌ Chậm hơn RSS, cần curl từng bài
- 💡 Dùng cho: Xây dựng database tin tức lịch sử, phân tích dài hạn

**Ví dụ**: Báo PLO có sitemap chia theo tháng `https://plo.vn/sitemaps/news-2024-12.xml`

**Tất cả các báo đều hỗ trợ cả RSS và Sitemap** vì đây là tiêu chuẩn web. Bạn có thể dùng RSS để lấy tin mới nhất hoặc Sitemap để lấy lịch sử.

### 3. **Dynamic Sitemap** (Sitemap Tự Động Cập Nhật)

- Một số báo như **PLO**, **Tuổi Trẻ** có sitemap thay đổi theo tháng/năm
- Thư viện tự động phát hiện tháng hiện tại và gọi đúng sitemap
- Ví dụ: Tháng 1/2025 → `news-2025-01.xml`

---

## Các Trang Báo Được Hỗ Trợ

| Tên Báo | Domain | RSS | Sitemap | Ghi Chú |
|---------|--------|-----|---------|---------|
| **VnExpress** | vnexpress.net | ✅ | ✅ | RSS cập nhật nhanh |
| **Tuổi Trẻ** | tuoitre.vn | ✅ | ✅ | Sitemap tháng/năm |
| **CafeF** | cafef.vn | ✅ | ✅ | Cả hai |
| **CafeBiz** | cafebiz.vn | ✅ | ✅ | Cả hai |
| **VietStock** | vietstock.vn | ✅ | ✅ | Cả hai |
| **VnEconomy** | vneconomy.vn | ✅ | ✅ | Sitemap XML |
| **Báo Đầu Tư** | baodautu.vn | ✅ | ✅ | Sitemap XML |
| **PLO** | plo.vn | ✅ | ✅ | Sitemap dynamic (tháng/năm) |
| **Báo Mới** | baomoi.com | ✅ | ✅ | Sitemap XML |
| **Thế Giới Tài Chính** | thesaigontimes.vn | ✅ | ✅ | Incremental sitemap |
| **Nhịp Cầu Đầu Tư** | nhipcaudautu.vn | ✅ | ✅ | Sitemap XML |
| **Công Thương** | congthuong.vn | ✅ | ✅ | Sitemap XML |

**Tất cả các báo đều hỗ trợ cả RSS và Sitemap** vì đây là tiêu chuẩn web. vnstock_news cung cấp cấu hình sẵn cho 12+ báo phổ biến nhưng có thể tùy biến để làm việc với bất kỳ website/báo nào có nguồn RSS/sitemap.

---

## Phương Thức Thu Thập Dữ Liệu

### 1. **RSS Parser** - Lấy từ RSS Feed

```python
from vnstock_news import Crawler

crawler = Crawler(site_name="vnexpress")
articles = crawler.get_articles_from_feed(limit_per_feed=20)
# Output: DataFrame với các bài từ RSS
```

**Ưu điểm**: Nhanh, dễ, cập nhật liên tục  
**Nhược điểm**: Chỉ lấy được bài mới nhất (thường 1-2 tuần)

### 2. **Sitemap Parser** - Lấy từ Sitemap XML

```python
from vnstock_news import Crawler

crawler = Crawler(site_name="cafef")
articles = crawler.get_articles_from_sitemap(limit=100)
# Output: DataFrame với 100 bài từ sitemap
```

**Ưu điểm**: Lấy được lịch sử nhiều tháng/năm  
**Nhược điểm**: Chậm hơn (phải duyệt từng bài)

**Tất cả các báo đều hỗ trợ cả RSS và Sitemap**. Bạn có thể chọn phương thức phù hợp với nhu cầu: RSS cho tin mới nhất, Sitemap cho lịch sử.

### 3. **Batch Crawler** - Lấy Hàng Loạt (Đồng Bộ)

```python
from vnstock_news import BatchCrawler

crawler = BatchCrawler(site_name="cafef", debug=False)
articles = crawler.fetch_articles(limit=500)
# Tải 500 bài, tự động lưu vào file
```

**Ưu điểm**: Đơn giản, có resume nếu bị lỗi  
**Nhược điểm**: Chậm vì chạy từng bài một

### 4. **Async Batch Crawler** - Lấy Hàng Loạt (Bất Đồng Bộ)

```python
import asyncio
from vnstock_news import AsyncBatchCrawler

async def main():
    crawler = AsyncBatchCrawler(site_name="cafef")
    articles = await crawler.fetch_articles_async(
        sources=["https://cafef.vn/latest-news-sitemap.xml"],
        top_n=500
    )

asyncio.run(main())
# Tải 500 bài nhanh hơn gấp 10 lần
```

**Ưu điểm**: Nhanh, concurrent requests  
**Nhược điểm**: Phức tạp hơn, cần async/await

### 5. **EnhancedNewsCrawler** - API Cao Cấp

```python
from vnstock_news import EnhancedNewsCrawler

crawler = EnhancedNewsCrawler(
    cache_enabled=True,
    cache_ttl=3600
)

articles = await crawler.fetch_articles_async(
    sources=["https://cafef.vn/latest-news-sitemap.xml"],
    site_name="cafef",
    max_articles=100,
    time_frame="7d",
    clean_content=True
)
# Đầy đủ tính năng: cache, cleaning, validation
```

---

## Output Data Structure

Tất cả phương thức đều trả về DataFrame với các cột sau:

| Cột | Kiểu | Mô Tả |
|-----|------|-------|
| `url` | string | URL bài viết |
| `title` | string | Tiêu đề |
| `short_description` | string | Tóm tắt ngắn/Sapo |
| `content` | string | Nội dung bài viết |
| `publish_time` | datetime | Thời gian đăng |
| `author` | string | Tác giả |
| `category` | string | Chuyên mục |
| `image_url` | string | URL hình ảnh (nếu có) |

### Ví dụ Output:

```
              url                   title  short_description  publish_time
0  https://cafef.vn/...  Thị trường chứng...  Dự báo tăng từ...  2025-01-15
1  https://cafef.vn/...  VN-Index chiếm...  Nhà đầu tư lo...  2025-01-14
```

---

## Cài Đặt & Import

### Cài Đặt Thư Viện

Các gói thư viện vnstock_data được cài đặt **chung** thông qua chương trình cài đặt của Vnstock. Để cài đặt và kích hoạt vnstock_data, vui lòng tham khảo hướng dẫn chi tiết tại:

**🔗 [Hướng Dẫn Cài Đặt Vnstock](https://vnstocks.com/onboard-member)**

Sau khi hoàn thành cài đặt, bạn có thể bắt đầu sử dụng các module trong vnstock_data ngay lập tức.

### Import

```python
# Cách 1: Import từ package chính
from vnstock_news import (
    Crawler,
    BatchCrawler,
    AsyncBatchCrawler,
    EnhancedNewsCrawler,
    SITES_CONFIG
)

# Cách 2: Import từ module riêng
from vnstock_news.core.crawler import Crawler
from vnstock_news.core.batch import BatchCrawler
from vnstock_news.api.enhanced import EnhancedNewsCrawler
from vnstock_news.config.sites import SITES_CONFIG
```

---

## Yêu Cầu & Giới Hạn

### Yêu Cầu Hệ Thống

- **Python**: 3.10+
- **Libraries**: requests, pandas, beautifulsoup4, feedparser, aiohttp

### Giới Hạn & Lưu Ý Quan Trọng

⚠️ **NGƯỜI DÙNG TỰ CHỊU TRÁCH NHIỆM** với các vấn đề sau:

1. **Bản Quyền & Thuê Bao**
   - Nội dung báo có liên quan đến vấn đề bản quyền khi sử dụng lại
   - Chỉ lấy để học tập, nghiên cứu cá nhân
   - Không lấy để tái xuất bản, thương mại hoá

2. **Rate Limiting & Block IP**
   - Tránh gửi quá nhiều request (mỗi báo có giới hạn)
   - Thêm delay giữa các request: `request_delay=2.0`
   - Lưu ý việc lạm dụng có thể bị chặn IP

3. **Terms of Service**
   - Đọc kỹ ToS của trang báo trước khi lấy dữ liệu
   - Một số báo cấm crawling trong ToS của họ

4. **Robot.txt & Sitemap.xml**
   - Hãy kiểm tra `/robots.txt` của báo
   - Sitemap thường được phép truy cập


**Hầu hết các báo đều hỗ trợ cả RSS và Sitemap** vì đây là tiêu chuẩn web. vnstock_news cung cấp cấu hình sẵn nhưng bạn có thể tùy biến cho bất kỳ website nào có RSS/sitemap.

---

## Cấu Trúc Tài Liệu

1. **01-overview.md** (Tệp này) - Giới thiệu, cấu trúc, cách sử dụng cơ bản
2. **02-crawlers.md** - Chi tiết các crawler (Crawler, Batch, Async, Enhanced)
3. **03-sitemap-rss-guide.md** - Hướng dẫn tìm và thiết lập Sitemap/RSS
4. **04-trending-analysis.md** - Phân tích xu hướng, keyword từ tin tức
5. **05-best-practices.md** - Best practices, tips, xử lý lỗi
6. **README.md** - Hướng dẫn tổng quan và navigation

---

## Quickstart - Bắt Đầu Nhanh

### Thu Thập Tin Từ RSS (Cách Nhanh Nhất)

```python
from vnstock_news import Crawler

# 1. Tạo crawler cho VnExpress
crawler = Crawler(site_name="vnexpress")

# 2. Lấy 10 bài mới nhất từ RSS
articles = crawler.get_articles_from_feed(limit_per_feed=10)

# 3. Lưu vào CSV
articles.to_csv("vnexpress_news.csv", index=False, encoding='utf-8-sig')

print(f"✅ Đã lấy {len(articles)} bài viết")
```

### Thu Thập Tin Từ Sitemap (Lấy Lịch Sử)

```python
from vnstock_news import BatchCrawler

# 1. Tạo batch crawler
crawler = BatchCrawler(
    site_name="cafef",
    request_delay=1.5  # Delay 1.5 giây giữa mỗi request
)

# 2. Lấy 100 bài từ sitemap
articles = crawler.fetch_articles(limit=100)

# 3. Lưu vào CSV
articles.to_csv("cafef_articles.csv", index=False)

print(f"✅ Đã lấy {len(articles)} bài viết từ {articles['publish_time'].min()} đến {articles['publish_time'].max()}")
```

### Lấy Từ Nhiều Báo Cùng Lúc (Nhanh)

```python
import asyncio
from vnstock_news import AsyncBatchCrawler, SITES_CONFIG

async def fetch_all():
    sites = ["cafef", "tuoitre", "vietstock"]
    all_articles = []
    
    for site_name in sites:
        crawler = AsyncBatchCrawler(site_name=site_name)
        config = SITES_CONFIG[site_name]
        
        # Lấy source (RSS hoặc Sitemap)
        if "rss" in config:
            sources = config["rss"]["urls"][:1]  # Lấy RSS đầu tiên
        else:
            sources = [config.get("sitemap_url")]
        
        print(f"📰 Đang lấy từ {site_name}...")
        articles = await crawler.fetch_articles_async(
            sources=sources,
            top_n=50
        )
        
        articles['source'] = site_name
        all_articles.append(articles)
    
    # Gộp tất cả
    result = pd.concat(all_articles, ignore_index=True)
    return result

# Chạy
articles = asyncio.run(fetch_all())
print(f"✅ Tổng cộng lấy được {len(articles)} bài")
```

---

## Tối Ưu Hóa & Tips

### 🚀 Tăng Tốc Độ

1. **Dùng AsyncBatchCrawler** - Nhanh gấp 5-10 lần
2. **Tăng concurrency** - Nhưng nhớ tránh block IP
3. **Bật cache** - Tránh lấy lại cùng một bài

### 🛡️ Tránh Bị Block

1. **Thêm delay** - `request_delay=2.0` giữa mỗi request
2. **Giới hạn concurrency** - `max_concurrency=3` để không quá tải
3. **Rotate user-agent** - Thay đổi User-Agent để không bị phát hiện
4. **Xác suất ngừng** - Nếu bị 403/429, dừng lại

### 💾 Quản Lý Bộ Nhớ

1. **Xử lý dữ liệu theo batch** - Không load hết vào RAM
2. **Xóa cache cũ** - Cache chỉ lưu N ngày gần nhất
3. **Lưu thường xuyên** - Tránh mất dữ liệu khi bị lỗi

---

## Các Lỗi Thường Gặp

| Lỗi | Nguyên Nhân | Giải Pháp |
|-----|-----------|---------|
| `ConnectionError` | Mất kết nối internet | Kiểm tra WiFi, thử lại |
| `HTTPError 429` | Quá nhiều request | Tăng `request_delay`, giảm `max_concurrency` |
| `HTTPError 403` | Bị block IP | Đợi vài giờ, dùng VPN |
| `Timeout Error` | Server chậm | Tăng timeout, thử lại |
| `Parsing Error` | Cấu trúc trang đã thay đổi | Báo lỗi tại GitHub, dùng custom_config |

---

## Tài Liệu Tham Khảo

- **Vnstock Official**: https://vnstocks.com/
- **GitHub**: https://github.com/vnstock-lab
- **Robots.txt Guide**: https://www.robotstxt.org/
- **Sitemap Protocol**: https://www.sitemaps.org/
- **RSS Standard**: https://www.rssboard.org/
