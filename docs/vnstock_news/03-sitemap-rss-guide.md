# 03. Hướng Dẫn Tìm & Thiết Lập Sitemap/RSS

Tài liệu này giúp bạn tìm sitemap và RSS feed của các trang báo, cũng như cách thiết lập crawler cho báo mới.

---

## 1. Sitemap - XML Bản Đồ Website

### Sitemap Là Gì?

Sitemap là tệp XML chứa danh sách tất cả URLs của website. Nó giúp máy tìm kiếm như Google, Bing (và chúng ta) biết được những trang nào tồn tại trên website. Biết được cấu trúc website giống như bạn có bản đồ thành phố khi đi du lịch.

**Định dạng sitemap:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://cafef.vn/article-1</loc>
    <lastmod>2025-01-15</lastmod>
  </url>
  <url>
    <loc>https://cafef.vn/article-2</loc>
    <lastmod>2025-01-14</lastmod>
  </url>
</urlset>
```

### Vị Trí Sitemap

Hầu hết các website đặt sitemap tại:
- `https://domain.com/sitemap.xml`
- `https://domain.com/sitemap_index.xml`
- `https://domain.com/news-sitemap.xml`
- `https://domain.com/sitemaps/...`

### Cách Tìm Sitemap

#### **Cách 1: robots.txt**

Hầu hết các website liệt kê sitemap trong `/robots.txt`:

```bash
# Mở trong trình duyệt hoặc terminal
curl https://cafef.vn/robots.txt
```

**Ví dụ output:**
```
User-agent: *
Allow: /
Disallow: /admin/
Sitemap: https://cafef.vn/latest-news-sitemap.xml
```

---

#### **Cách 2: Thử các URL phổ biến**

```bash
# Thử từng URL này
curl https://domain.com/sitemap.xml
curl https://domain.com/sitemap_index.xml
curl https://domain.com/news-sitemap.xml
curl https://domain.com/sitemaps/latest.xml
```

Nếu có kết quả XML → Đó là sitemap!

---

#### **Cách 3: Dùng công cụ online**

- https://www.xml-sitemaps.com/
- https://www.screaming-frog.com/seo-spider/
- https://ahrefs.com/sitemapapi

---

#### **Cách 4: Tìm kiếm Google với từ khóa sitemap**

Dùng Google để tìm sitemap của website:

**Tìm kiếm cơ bản:**
```
site:cafef.vn sitemap
```

**Tìm kiếm nâng cao:**
```
site:cafef.vn filetype:xml sitemap
```

**Tìm kiếm RSS:**
```
site:cafef.vn rss feed
```

**Ví dụ kết quả:**
- `https://cafef.vn/latest-news-sitemap.xml`
- `https://cafef.vn/rss.xml`

**Cách thực hiện:**
1. Mở Google.com
2. Nhập: `site:domain.com sitemap`
3. Nhấn Enter
4. Kiểm tra kết quả đầu tiên thường là sitemap chính

---

## 2. RSS Feed - Luồng Tin Tức

### RSS Là Gì?

RSS (Really Simple Syndication) là tệp text chứa danh sách các bài viết mới nhất của website, cập nhật tự động.

**Ví dụ RSS:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>VnExpress - Tin Tức Mới Nhất</title>
    <link>https://vnexpress.net</link>
    <item>
      <title>Chứng khoán tăng 1%</title>
      <link>https://vnexpress.net/article/1</link>
      <pubDate>Wed, 15 Jan 2025 10:30:00 GMT</pubDate>
      <description>Thị trường hôm nay...</description>
    </item>
  </channel>
</rss>
```

### Vị Trí RSS Feed

RSS feed thường tại:
- `https://domain.com/feed.xml`
- `https://domain.com/rss`
- `https://domain.com/category/feed`

---

### Cách Tìm RSS Feed

#### **Cách 1: Mã HTML của trang chủ**

```bash
# Tải HTML trang chủ
curl https://vnexpress.net | grep -i "rss\|feed"
```

Tìm tag như:
```html
<link rel="alternate" type="application/rss+xml" href="https://vnexpress.net/rss/tin-moi-nhat.rss">
```

---

#### **Cách 2: Thử các URL phổ biến**

```bash
curl https://domain.com/feed.xml
curl https://domain.com/feed.rss
curl https://domain.com/rss/feed
curl https://domain.com/category/feed.rss
```

---

#### **Cách 3: Sử dụng trình duyệt**

1. Vào trang web
2. Bấm **Ctrl+U** để xem source
3. Tìm keyword `rss`, `feed`, `xmlns` trong `<head>`

---

## 3. Các Báo Việt Nam - Sitemap & RSS

Bảng dưới đây liệt kê sitemap và RSS của các báo chính:

| Báo | Domain | Sitemap | RSS |
|-----|--------|---------|-----|
| **VnExpress** | vnexpress.net | request bằng curl hoặc Python sẽ thấy, thường bị website chuyển hướng khi mở trên trình duyệt | ✅ [tin-moi-nhat](https://vnexpress.net/rss/tin-moi-nhat.rss) |
| **Tuổi Trẻ** | tuoitre.vn | ✅ [news-sitemap](https://tuoitre.vn/news-sitemap.xml) | ✅ [feed.rss](https://tuoitre.vn/feed.rss) |
| **CafeF** | cafef.vn | ✅ [latest-news-sitemap](https://cafef.vn/latest-news-sitemap.xml) | ✅ [RSS](https://cafef.vn/rss.xml) |
| **CafeBiz** | cafebiz.vn | ✅ [sitemap](https://cafebiz.vn/sitemap.xml) | ✅ [RSS feeds](https://cafebiz.vn/rss/) |
| **VietStock** | vietstock.vn | ✅ [news-sitemap](https://vietstock.vn/news-sitemap.xml) | ✅ [RSS](https://vietstock.vn/rss/) |
| **VnEconomy** | vneconomy.vn | ✅ [latest-news](https://vneconomy.vn/latest-news.xml) | ✅ |
| **Báo Đầu Tư** | baodautu.vn | ✅ [sitemap](https://baodautu.vn/sitemap.xml) | ✅ |
| **PLO** | plo.vn | ✅ [monthly](https://plo.vn/sitemaps/news-{year}-{month}.xml) | ✅ |
| **Báo Mới** | baomoi.com | ✅ [sitemap](https://baomoi.com/sitemap.xml) | ✅ |
| **Thế Giới Tài Chính** | thesaigontimes.vn | ✅ [incremental](https://thesaigontimes.vn/sitemaps/) | ✅ |
| **Nhịp Cầu Đầu Tư** | nhipcaudautu.vn | ✅ [sitemap](https://nhipcaudautu.vn/sitemap.xml) | ✅ |
| **Công Thương** | congthuong.vn | ✅ [sitemap](https://congthuong.vn/sitemap.xml) | ✅ |

---

## 4. Sitemap Động (Dynamic)

Một số báo sắp xếp sitemap theo **tháng/năm**, không có sitemap chung duy nhất.

### Ví Dụ: PLO - Sitemap Tháng/Năm

PLO lưu trữ sitemap theo tháng:

```
https://plo.vn/sitemaps/news-2025-01.xml  (Tháng 1/2025)
https://plo.vn/sitemaps/news-2025-02.xml  (Tháng 2/2025)
https://plo.vn/sitemaps/news-2024-12.xml  (Tháng 12/2024)
https://plo.vn/sitemaps/news-2024-11.xml  (Tháng 11/2024)
```

**Cách thêm vào vnstock_news:**

```python
from vnstock_news import Crawler, SITES_CONFIG

# Nếu chưa có trong config, thêm thủ công
custom_plo_config = {
    "name": "Báo PLO",
    "domain": "plo.vn",
    "sitemap": {
        "pattern_type": "monthly",  # ← Key: "monthly"
        "base_url": "https://plo.vn/sitemaps/news",
        "format": "{base_url}-{year}-{month:02d}.xml"
    }
}

crawler = Crawler(custom_config=custom_plo_config)

# Crawler sẽ tự động tạo URL cho tháng hiện tại
articles = crawler.get_articles_from_sitemap(limit=100)
```

---

### Ví Dụ: Thế Giới Tài Chính - Incremental Sitemap

Thế Giới Tài Chính sử dụng "incremental sitemaps" - danh sách sitemaps cập nhật từng ngày:

```
https://thesaigontimes.vn/sitemaps/news-1.xml   (Ngày 1)
https://thesaigontimes.vn/sitemaps/news-2.xml   (Ngày 2)
https://thesaigontimes.vn/sitemaps/news-3.xml   (Ngày 3)
... cứ tiếp tục
```

**Cách cấu hình:**

```python
custom_ktsg_config = {
    "name": "Thế Giới Tài Chính",
    "domain": "thesaigontimes.vn",
    "sitemap": {
        "pattern_type": "incremental",  # ← Key: "incremental"
        "base_url": "https://thesaigontimes.vn/sitemaps/news",
        "index_url": "https://thesaigontimes.vn/sitemaps/",
        "format": "{base_url}-{index}.xml"
    }
}

crawler = Crawler(custom_config=custom_ktsg_config)
articles = crawler.get_articles_from_sitemap(limit=100)
```

---

## 5. Thêm Báo Mới - Custom Configuration

Nếu trang báo chưa được hỗ trợ, thêm configuration thủ công:

### **Nếu báo có RSS:**

```python
from vnstock_news import Crawler

custom_config = {
    "name": "Báo XYZ",
    "domain": "baoxyz.vn",
    "rss": {
        "urls": [
            "https://baoxyz.vn/feed.rss",
            "https://baoxyz.vn/category/business/feed.rss"
        ]
    }
}

crawler = Crawler(custom_config=custom_config)
articles = crawler.get_articles_from_feed(limit=20)
```

---

### **Nếu báo có Sitemap:**

```python
from vnstock_news import Crawler

custom_config = {
    "name": "Báo XYZ",
    "domain": "baoxyz.vn",
    "sitemap_url": "https://baoxyz.vn/sitemap.xml",
    "config": {
        "selectors": {
            "title": "h1.title",              # CSS selector cho tiêu đề
            "short_description": "p.summary", # CSS selector cho sapo
            "content": "div.article-body",    # CSS selector cho nội dung
            "publish_time": "span.date",      # CSS selector cho ngày
            "author": "span.author"           # CSS selector cho tác giả
        }
    }
}

crawler = Crawler(custom_config=custom_config)
articles = crawler.get_articles_from_sitemap(limit=100)
```

---

### **Nếu báo có Dynamic Sitemap (theo tháng):**

```python
from vnstock_news import Crawler

custom_config = {
    "name": "Báo XYZ",
    "domain": "baoxyz.vn",
    "sitemap": {
        "pattern_type": "monthly",
        "base_url": "https://baoxyz.vn/sitemaps/news",
        "format": "{base_url}-{year}-{month:02d}.xml"
        # Format: 2025-01, 2025-02, v.v.
    }
}

crawler = Crawler(custom_config=custom_config)
articles = crawler.get_articles_from_sitemap(limit=100)
```

---

## 6. Kiểm Tra Sitemap/RSS Trước Khi Dùng

### **Kiểm Tra Sitemap**

```bash
# Linux/Mac
curl -I https://cafef.vn/latest-news-sitemap.xml

# Xem nội dung đầu tiên
curl https://cafef.vn/latest-news-sitemap.xml | head -50
```

**Output tốt:**
```
HTTP/1.1 200 OK
Content-Type: application/xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
```

**Output tệ:**
```
HTTP/1.1 404 Not Found
```

---

### **Kiểm Tra RSS**

```bash
curl https://vnexpress.net/rss/tin-moi-nhat.rss | head -50
```

**Output tốt:**
```
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>VnExpress</title>
```

---

## 7. Cập Nhật SITES_CONFIG

Nếu bạn tìm được sitemap/RSS mới, báo cáo lên GitHub:

```python
# Gửi PR với cấu hình mới
SITES_CONFIG["my_news"] = {
    "name": "Báo Mới",
    "domain": "mynews.vn",
    "rss": {
        "urls": ["https://mynews.vn/feed.rss"]
    },
    "sitemap_url": "https://mynews.vn/sitemap.xml"
}
```

---

## 8. Lưu Ý Quan Trọng - Legal & Ethical

⚠️ **NGƯỜI DÙNG TỰ CHỊU TRÁCH NHIỆM** với các vấn đề sau:

### **1. Robots.txt & Các Quy Tắc Crawling**

Trước khi crawl, kiểm tra `/robots.txt`:

```bash
curl https://domain.com/robots.txt
```

**Ví dụ:**
```
User-agent: *
Allow: /           # ← Cho phép crawl
Disallow: /admin/  # ← Cấm crawl /admin/

# Đối với Googlebot
User-agent: Googlebot
Allow: /
Crawl-delay: 1     # ← Delay 1 giây

# Đối với crawler khác
User-agent: *
Crawl-delay: 5
```

**Tuân thủ:**
- Kiểm tra `Disallow` - không crawl những URL bị cấm
- Tuân thủ `Crawl-delay` - thêm delay giữa requests
- User-agent: Cho báo cáo bạn là ai (`Mozilla/5.0` hoặc tên riêng)

### **2. Rate Limiting - Tránh Overload Server**

```python
from vnstock_news import BatchCrawler

# ❌ Sai - 10 requests/giây → Block IP
crawler = BatchCrawler(site_name="cafef", request_delay=0.0)

# ✅ Đúng - 1 request/2 giây → An toàn
crawler = BatchCrawler(site_name="cafef", request_delay=2.0)
```

**Khuyến cáo:**
- Thêm delay 1-2 giây giữa mỗi request
- Không crawl trong giờ cao điểm
- Giảm concurrency nếu bị 429 (Rate Limit)

### **3. Bản Quyền & Terms of Service**

- Nội dung báo có **bản quyền** ©
- **Chỉ dùng để học tập, nghiên cứu cá nhân**
- **Không tái xuất bản, không mua bán**
- Đọc kỹ ToS của báo trước dùng

### **4. Block IP & VPN**

Nếu bị block:
```
HTTP 403 Forbidden
hoặc
HTTP 429 Too Many Requests
```

**Giải pháp:**
- Dừng crawl 1-2 giờ, sau đó thử lại
- Dùng VPN (nếu hợp pháp)
- Giảm request rate

### **5. Privacy & Dữ Liệu Cá Nhân**

- Không crawl thông tin cá nhân (email, số điện thoại)
- Tuân thủ GDPR/luật pháp địa phương

---

## 9. Ví Dụ Thực Tế

### Lấy Sitemap Của CafeF

```python
from vnstock_news import Crawler
from datetime import datetime

crawler = Crawler(site_name="cafef")

# Lấy 200 bài từ 1-31/1/2025
articles = crawler.get_articles_from_sitemap(
    limit=200,
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 1, 31)
)

print(f"✅ Lấy {len(articles)} bài từ tháng 1/2025")
print(articles[['title', 'publish_time']].head())

articles.to_csv("cafef_january_2025.csv", index=False)
```

---

### Lấy RSS + Sitemap Cùng Lúc

```python
from vnstock_news import Crawler
import pandas as pd

crawler = Crawler(site_name="tuoitre")

# Lấy RSS (mới nhất)
rss_articles = crawler.get_articles_from_feed(limit_per_feed=30)

# Lấy Sitemap (lịch sử)
sitemap_articles = crawler.get_articles_from_sitemap(limit=100)

# Gộp, loại bỏ duplicate
all_articles = pd.concat([rss_articles, sitemap_articles], ignore_index=True)
all_articles = all_articles.drop_duplicates(subset=['url'])

print(f"✅ Tổng {len(all_articles)} bài (RSS + Sitemap)")
```

---

### Tìm Sitemap Tự Động

```python
import requests
from urllib.parse import urljoin
from xml.etree import ElementTree as ET

def find_sitemaps(domain):
    """Tìm sitemaps của một domain"""
    sitemaps = []
    
    # Cách 1: Kiểm tra robots.txt
    try:
        robots_url = f"{domain}/robots.txt"
        resp = requests.get(robots_url, timeout=5)
        for line in resp.text.split('\n'):
            if line.lower().startswith('sitemap:'):
                sitemap_url = line.split(':', 1)[1].strip()
                sitemaps.append(sitemap_url)
    except:
        pass
    
    # Cách 2: Thử các URLs phổ biến
    common_sitemaps = [
        '/sitemap.xml',
        '/sitemap_index.xml',
        '/news-sitemap.xml',
        '/sitemaps/news.xml',
    ]
    
    for path in common_sitemaps:
        try:
            url = urljoin(domain, path)
            resp = requests.head(url, timeout=5)
            if resp.status_code == 200:
                sitemaps.append(url)
        except:
            pass
    
    return list(set(sitemaps))

# Sử dụng
sitemaps = find_sitemaps("https://cafef.vn")
for sitemap in sitemaps:
    print(f"✅ Tìm được: {sitemap}")
```

---

## Tổng Kết

| Cần | Cách Tìm |
|-----|---------|
| Tìm Sitemap | Kiểm tra robots.txt, hoặc thử `/sitemap.xml` |
| Tìm RSS | Xem source HTML, hoặc thử `/feed.rss` |
| Báo chưa hỗ trợ | Thêm custom_config với sitemap_url hoặc RSS |
| Dynamic sitemap | Dùng `pattern_type: "monthly"` hoặc `"incremental"` |
| An toàn crawling | Tuân thủ robots.txt, thêm delay, rate limit |
