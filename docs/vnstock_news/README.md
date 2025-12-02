# VnStock News - Hướng Dẫn Chi Tiết

**vnstock_news** là thư viện Python cung cấp khả năng thu thập, xử lý và phân tích tin tức từ các trang báo Việt Nam. Thư viện cung cấp cấu hình sẵn cho **12+ trang báo** phổ biến nhưng có thể tùy biến để làm việc với **bất kỳ website/báo nào** có nguồn RSS/sitemap để cung cấp danh sách cho thuật toán đọc bài viết chi tiết.

## 📚 Danh Sách Tài Liệu

Hướng dẫn được chia thành các phần:

### 1. **[01-overview.md](./01-overview.md)** - Giới Thiệu & Bắt Đầu
- ❓ vnstock_news là gì?
- 📰 Những báo nào được hỗ trợ
- 🔄 Phương thức thu thập dữ liệu (RSS vs Sitemap)
- 📊 Cấu trúc dữ liệu output
- ⚡ Quickstart 3 ví dụ

**Cho ai?** Người mới bắt đầu, muốn hiểu cơ bản

---

### 2. **[02-crawlers.md](./02-crawlers.md)** - Chi Tiết Các Crawler
- 📖 7 loại crawler khác nhau
- 🔧 Các method và parameter của từng loại
- 💻 Ví dụ code chi tiết
- 📊 Bảng so sánh tốc độ/tính năng
- ⚠️ Xử lý lỗi

**Cho ai?** Developer muốn dùng API chi tiết

---

### 3. **[03-sitemap-rss-guide.md](./03-sitemap-rss-guide.md)** - Tìm & Thiết Lập Sitemap/RSS
- 🔍 Cách tìm sitemap của báo
- 📡 Cách tìm RSS feed
- 📋 Danh sách 12+ báo với sitemap/RSS
- 🎯 Sitemap động (tháng/năm)
- ➕ Thêm báo mới
- ⚖️ Lưu ý pháp lý (robots.txt, rate limiting, copyright)

**Cho ai?** Muốn tìm sitemap/RSS, thêm báo mới

---

### 4. **[04-trending-analysis.md](./04-trending-analysis.md)** - Phân Tích Xu Hướng
- 🔥 TrendingAnalyzer - công cụ phân tích keyword
- 🔍 Extract keywords phổ biến
- 📈 Phân tích trending theo thời gian
- 📊 So sánh giữa các báo
- 📉 Visualization & export

**Cho ai?** Phân tích dữ liệu, journalist, marketer

---

### 5. **[05-best-practices.md](./05-best-practices.md)** - Best Practices & Tips
- 🎯 Chiến lược thu thập dữ liệu
- ⚡ Rate limiting & tránh block IP
- 💾 Caching & performance
- 🛡️ Error handling & resume
- 🧹 Deduplication & cleaning
- 🕐 Timezone handling
- 🚀 Production deployment

**Cho ai?** Production use, muốn optimize performance

---

## 🚀 Quickstart - Bắt Đầu Nhanh

### Ví Dụ 1: Lấy 20 Bài Mới Từ VnExpress (30 giây)
```python
from vnstock_news import Crawler

crawler = Crawler(site_name="vnexpress")
articles = crawler.get_articles_from_feed(limit_per_feed=20)

print(f"✅ Lấy {len(articles)} bài")
print(articles[['title', 'publish_time']].head())
```

### Ví Dụ 2: Lấy 100 Bài Lịch Sử Từ CafeF (1 phút)
```python
from vnstock_news import BatchCrawler

crawler = BatchCrawler(site_name="cafef", request_delay=1.0)
articles = crawler.fetch_articles(limit=100)

print(f"✅ Lấy {len(articles)} bài từ {articles['publish_time'].min()}")
articles.to_csv("cafef_articles.csv", index=False)
```

### Ví Dụ 3: Tìm Trending Keywords (1 phút)
```python
from vnstock_news import Crawler, TrendingAnalyzer

crawler = Crawler(site_name="cafef")
articles = crawler.get_articles_from_feed(limit_per_feed=50)

analyzer = TrendingAnalyzer()
keywords = analyzer.extract_keywords(articles['title'].tolist(), top_n=10)

for keyword, count in keywords.items():
    print(f"{keyword}: {count}")
```

---

## 📊 Các Báo Được Hỗ Trợ (12+ báo)

| # | Báo | Domain | RSS | Sitemap | Ghi Chú |
|---|-----|--------|-----|---------|---------|
| 1 | **VnExpress** | vnexpress.net | ✅ | ✅ | RSS cập nhật nhanh |
| 2 | **Tuổi Trẻ** | tuoitre.vn | ✅ | ✅ | Sitemap tháng/năm |
| 3 | **CafeF** | cafef.vn | ✅ | ✅ | Cả hai |
| 4 | **CafeBiz** | cafebiz.vn | ✅ | ✅ | Cả hai |
| 5 | **VietStock** | vietstock.vn | ✅ | ✅ | Cả hai |
| 6 | **VnEconomy** | vneconomy.vn | ✅ | ✅ | Sitemap XML |
| 7 | **Báo Đầu Tư** | baodautu.vn | ✅ | ✅ | Sitemap XML |
| 8 | **PLO** | plo.vn | ✅ | ✅ | Sitemap dynamic (tháng/năm) |
| 9 | **Báo Mới** | baomoi.com | ✅ | ✅ | Sitemap XML |
| 10 | **Thế Giới Tài Chính** | thesaigontimes.vn | ✅ | ✅ | Incremental sitemap |
| 11 | **Nhịp Cầu Đầu Tư** | nhipcaudautu.vn | ✅ | ✅ | Sitemap XML |
| 12 | **Công Thương** | congthuong.vn | ✅ | ✅ | Sitemap XML |

**Tất cả các báo đều hỗ trợ cả RSS và Sitemap** vì đây là tiêu chuẩn web. vnstock_news cung cấp cấu hình sẵn cho 12+ báo phổ biến nhưng có thể tùy biến để làm việc với bất kỳ website/báo nào có nguồn RSS/sitemap.

**Muốn thêm báo mới?** → Xem [03-sitemap-rss-guide.md](./03-sitemap-rss-guide.md#5-thêm-báo-mới---custom-configuration)

---

## 🔍 Phương Thức Thu Thập Dữ Liệu

### RSS Feed - Tin Mới Nhất
- ✅ **Tốc độ**: Nhanh (< 10 giây)
- ✅ **Cập nhật**: Thường xuyên (hàng giờ)
- ✅ **Dữ liệu**: Bài mới nhất từ báo
- ❌ **Lịch sử**: Chỉ 1-2 tuần gần đây

**Dùng cho:** Monitoring tin tươi, cập nhật hàng ngày

**Code:**
```python
crawler = Crawler(site_name="vnexpress")
articles = crawler.get_articles_from_feed(limit_per_feed=20)
```

---

### Sitemap - Lịch Sử Lâu Dài
- ✅ **Tốc độ**: Chậm hơn (10-60 phút)
- ✅ **Dữ liệu**: Lịch sử 1-2 năm
- ✅ **Lượng**: Có thể lấy hàng ngàn bài
- ❌ **Thời gian**: Cần chờ lâu hơn

**Dùng cho:** Xây dựng database lịch sử, phân tích

**Code:**
```python
crawler = Crawler(site_name="cafef")
articles = crawler.get_articles_from_sitemap(limit=500)
```

---

### Batch Crawler - Lấy Hàng Loạt (Đồng Bộ)
- ✅ **Đơn giản**: Dùng dễ nhất
- ✅ **Resume**: Có thể tiếp tục nếu bị lỗi
- ❌ **Tốc độ**: Lấy từng bài một

**Dùng cho:** Xây dựng database, người mới

**Code:**
```python
crawler = BatchCrawler(site_name="cafef")
articles = crawler.fetch_articles(limit=500)
```

---

### AsyncBatchCrawler - Lấy Hàng Loạt (Bất Đồng Bộ)
- ✅ **Tốc độ**: Nhanh gấp 5-10 lần
- ✅ **Concurrent**: Lấy nhiều bài cùng lúc
- ❌ **Phức tạp**: Code async/await

**Dùng cho:** Production, cần tốc độ cao

**Code:**
```python
import asyncio
from vnstock_news import AsyncBatchCrawler

async def fetch():
    crawler = AsyncBatchCrawler(site_name="cafef")
    return await crawler.fetch_articles_async(
        site_name="cafef", max_articles=1000
    )

articles = asyncio.run(fetch())
```

---

### EnhancedNewsCrawler - Đầy Đủ Tính Năng
- ✅ **Caching**: Lưu cache tránh lấy lại
- ✅ **Cleaning**: Tự động làm sạch nội dung
- ✅ **Validation**: Kiểm tra dữ liệu
- ✅ **Retry**: Retry tự động nếu lỗi

**Dùng cho:** Production, cần đầy đủ tính năng

**Code:**
```python
from vnstock_news import EnhancedNewsCrawler

async def fetch():
    crawler = EnhancedNewsCrawler(cache_enabled=True)
    return await crawler.fetch_articles_async(
        sources=["https://cafef.vn/latest-news-sitemap.xml"],
        site_name="cafef",
        max_articles=100,
        clean_content=True
    )

articles = asyncio.run(fetch())
```

---

## 📊 Output Data Structure

Tất cả phương thức đều trả về **pandas DataFrame** với các cột:

| Cột | Kiểu | Ví Dụ |
|-----|------|-------|
| `url` | string | `https://cafef.vn/article/...` |
| `title` | string | `Chứng khoán tăng 1%` |
| `short_description` | string | `Thị trường hôm nay tăng...` |
| `content` | string | `Nội dung bài viết đầy đủ...` |
| `publish_time` | datetime | `2025-01-15 10:30:00` |
| `author` | string | `Nguyễn Văn A` |
| `category` | string | `Tài Chính` |
| `source` | string | `cafef` |

**Ví dụ:**
```python
articles.head()
#                             url                   title publish_time
# 0  https://cafef.vn/...  Thị trường chứng...  2025-01-15
# 1  https://cafef.vn/...  Nhà đầu tư lo...  2025-01-14
```

---

## 💡 Các Trường Hợp Sử Dụng

### 📈 Nhà Phân Tích Tài Chính
```python
# Lấy tin từ 3 tháng, phân tích trending keyword
from vnstock_news import AsyncBatchCrawler, TrendingAnalyzer

async def analyze():
    crawler = AsyncBatchCrawler(site_name="cafef")
    articles = await crawler.fetch_articles_async(
        site_name="cafef", max_articles=5000
    )
    
    analyzer = TrendingAnalyzer()
    keywords = analyzer.extract_keywords(articles['content'].tolist(), top_n=50)
    
    return keywords

keywords = asyncio.run(analyze())
```

---

### 📰 Journalist / Content Creator
```python
# Monitoring tin mới nhất, kiểm tra trending hàng ngày
from vnstock_news import Crawler
import schedule
import time

def check_trending():
    crawler = Crawler(site_name="tuoitre")
    articles = crawler.get_articles_from_feed(limit_per_feed=30)
    
    print(f"📰 Tin mới: {len(articles)} bài")
    print(articles[['title', 'publish_time']].head(10))

# Chạy mỗi 1 giờ
schedule.every(1).hours.do(check_trending)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

### 🤖 Data Scientist / ML Engineer
```python
# Xây dựng dataset tin tức để training model
from vnstock_news import AsyncBatchCrawler
import pandas as pd

async def build_dataset():
    all_articles = []
    
    sites = ["cafef", "tuoitre", "vietstock", "vnexpress"]
    
    for site in sites:
        crawler = AsyncBatchCrawler(site_name=site)
        articles = await crawler.fetch_articles_async(
            site_name=site, max_articles=2000
        )
        articles['source'] = site
        all_articles.append(articles)
    
    dataset = pd.concat(all_articles)
    dataset.to_csv("news_dataset_10k.csv", index=False)
    
    return dataset

dataset = asyncio.run(build_dataset())
```

---

### 🔍 Market Researcher
```python
# Theo dõi topic cụ thể, phân tích tần suất mention
from vnstock_news import Crawler, TrendingAnalyzer

crawler = Crawler(site_name="cafef")
articles = crawler.get_articles_from_sitemap(limit=1000)

# Lọc bài đề cập đến "FED" hoặc "lãi suất"
filtered = articles[
    (articles['title'].str.contains('FED|lãi suất', case=False, na=False))
]

print(f"Found {len(filtered)} articles mentioning FED or interest rates")
print(f"Date range: {filtered['publish_time'].min()} to {filtered['publish_time'].max()}")
```

---

## 🛡️ Lưu Ý Quan Trọng - Legal & Ethical

⚠️ **NGƯỜI DÙNG TỰ CHỊU TRÁCH NHIỆM** với các vấn đề sau:

### 1️⃣ Bản Quyền
- Nội dung báo có **bản quyền** ©
- **Chỉ dùng để học tập, nghiên cứu cá nhân**
- **Không tái xuất bản, không bán, không thương mại hóa**

### 2️⃣ Terms of Service
- Đọc kỹ ToS của trang báo trước crawling
- Một số báo cấm crawling trong ToS
- Tuân thủ các quy định của báo

### 3️⃣ Robots.txt & Rate Limiting
- Kiểm tra `/robots.txt` trước crawl
- Tuân thủ `Crawl-delay` (nếu có)
- Không crawl các path bị `Disallow`
- Thêm delay 1-2 giây giữa mỗi request

### 4️⃣ Block IP & Rate Limit
- Nếu bị 429 (Too Many Requests) → Dừng lại 1-2 giờ
- Nếu bị 403 (Forbidden) → IP bị block, dùng VPN
- Giảm concurrency / tăng request_delay

### 5️⃣ Privacy & GDPR
- Không crawl thông tin cá nhân (email, số điện thoại)
- Tuân thủ luật GDPR và privacy địa phương

**Xem chi tiết:** [03-sitemap-rss-guide.md - Section 8](./03-sitemap-rss-guide.md#8-lưu-ý-quan-trọng---legal--ethical)

---

## ❓ FAQ

### Q: Báo mới không có trong danh sách, thêm như thế nào?
**A:** Xem [03-sitemap-rss-guide.md - Section 5](./03-sitemap-rss-guide.md#5-thêm-báo-mới---custom-configuration)

---

### Q: Bị block IP, phải làm gì?
**A:** 
1. Dừng crawl ngay lập tức
2. Đợi 1-2 giờ
3. Tăng `request_delay` lên 3-5 giây
4. Giảm `max_concurrency` xuống 2-3
5. Dùng VPN (nếu cần)
6. Xem [05-best-practices.md - Section 2](./05-best-practices.md#2-rate-limiting--tránh-block-ip)

---

### Q: Lấy toàn bộ lịch sử (1-2 năm) từ một báo mất bao lâu?
**A:** 
- **AsyncBatchCrawler** (nhanh): 10-30 phút
- **BatchCrawler** (chậm): 1-2 giờ
- Phụ thuộc vào số lượng bài + request_delay

---

### Q: Cache hoạt động như thế nào?
**A:**
- Cache lưu URL đã fetch
- Nếu fetch lại URL trong TTL (time-to-live), lấy từ cache
- TTL mặc định: 2 giờ
- Tiết kiệm bandwidth 30-50%

---

### Q: Dữ liệu output có HTML hay đã làm sạch?
**A:** 
- Mặc định: Có HTML
- Dùng `EnhancedNewsCrawler` với `clean_content=True` để xóa HTML
- Hoặc tự làm sạch xem [05-best-practices.md - Section 5](./05-best-practices.md#5-deduplication--data-cleaning)

---

### Q: Có hỗ trợ tiếng Anh không?
**A:** vnstock_news tối ưu cho **tiếng Việt**. TrendingAnalyzer có `language='english'` nhưng chỉ là basic.

---

## 📞 Support & Contribution

- 🐛 **Bug Report**: https://github.com/vnstock-lab/vnstock/issues
- 💡 **Feature Request**: https://github.com/vnstock-lab/vnstock/discussions
- 📧 **Email**: support@vnstock.com

---

## 📚 Tài Liệu Liên Quan

- **Vnstock Official Docs**: https://vnstocks.com/
- **GitHub Repository**: https://github.com/vnstock-lab/vnstock
- **Sitemap Protocol**: https://www.sitemaps.org/
- **RSS Standard**: https://www.rssboard.org/
- **Robots.txt Guide**: https://www.robotstxt.org/

---

## 📋 Roadmap

- [ ] Support RSS 2.0 full features
- [ ] Add more Vietnamese news sites (20+)
- [ ] Sentiment analysis cho tiếng Việt
- [ ] NER (Named Entity Recognition) để extract entities
- [ ] Database backend support (PostgreSQL, MongoDB)
- [ ] Web UI dashboard
- [ ] API server

---

## 📄 License

vnstock_news là một phần của **vnstock** - công cụ phân tích thị trường chứng khoán Việt Nam.

**License**: MIT

---

## 🙏 Cảm Ơn

Cảm ơn bạn đã sử dụng vnstock_news. Vui lòng tuân thủ các quy tắc pháp lý và đạo đức trong quá trình sử dụng.

Happy analyzing! 📊
