# 04. Phân Tích Xu Hướng & Keyword

Tài liệu này hướng dẫn sử dụng module phân tích xu hướng để tìm ra các chủ đề, keyword phổ biến từ tin tức.

---

## 1. TrendingAnalyzer - Khái Niệm

### TrendingAnalyzer Là Gì?

`TrendingAnalyzer` là công cụ phân tích dữ liệu tin tức để tìm ra:

1. **Từ khóa phổ biến** (keywords) - Từ/cụm từ xuất hiện nhiều
2. **Chủ đề xu hướng** (trending topics) - Các chủ đề được bàn luận
3. **Độ phổ biến của từ** - Tần suất từ xuất hiện

### Hoạt Động

```
Danh sách tin tức (DataFrame)
    ↓
Lấy nội dung từ các bài
    ↓
Chuẩn hóa text (thường dùng, xóa ký tự lạ)
    ↓
Tách từ (tokenization) & xóa từ không cần (stopwords)
    ↓
Đếm tần suất từ
    ↓
Xếp hạng & trả về kết quả
```

---

## 2. Khởi Tạo & Cơ Bản

### Import

```python
from vnstock_news import TrendingAnalyzer
import pandas as pd
```

### Khởi Tạo

```python
# Cách 1: Mặc định (Vietnamese)
analyzer = TrendingAnalyzer()

# Cách 2: Custom language & stopwords
analyzer = TrendingAnalyzer(
    language='vietnamese',
    min_frequency=2,          # Từ phải xuất hiện ít nhất 2 lần
    max_keywords=20,          # Trả về tối đa 20 từ
    min_word_length=2         # Từ phải có ít nhất 2 ký tự
)
```

**Parameters:**
- `language` (str): Ngôn ngữ ('vietnamese', 'english', ...)
- `min_frequency` (int): Từ phải xuất hiện ít nhất N lần để được coi là trending
- `max_keywords` (int): Trả về tối đa bao nhiêu keyword
- `min_word_length` (int): Từ phải dài tối thiểu bao nhiêu ký tự

---

## 3. Phương Thức Chính

### `extract_keywords(texts, top_n=20)`

Trích xuất keywords từ danh sách text.

```python
from vnstock_news import Crawler, TrendingAnalyzer

# Bước 1: Lấy tin tức
crawler = Crawler(site_name="cafef")
articles = crawler.get_articles_from_feed(limit_per_feed=30)

# Bước 2: Khởi tạo analyzer
analyzer = TrendingAnalyzer()

# Bước 3: Trích xuất keywords
# Dùng 'content' (nội dung đầy đủ) hoặc 'title' (tiêu đề)
keywords = analyzer.extract_keywords(
    texts=articles['title'].tolist(),
    top_n=20
)

print(keywords)
```

**Output:**
```
{'chứng khoán': 45, 'nhà đầu tư': 32, 'thị trường': 28, 'tăng': 25, ...}
```

**Parameters:**
- `texts` (list): Danh sách text cần phân tích
- `top_n` (int): Trả về top N keyword (default: 20)

**Returns:** Dict with format `{keyword: frequency}`

---

### `extract_topics(articles_df, content_column='content', top_n=20)`

Trích xuất topics từ DataFrame tin tức.

```python
from vnstock_news import Crawler, TrendingAnalyzer

crawler = Crawler(site_name="tuoitre")
articles = crawler.get_articles_from_feed(limit_per_feed=50)

analyzer = TrendingAnalyzer()

topics = analyzer.extract_topics(
    articles_df=articles,
    content_column='content',  # Cột chứa nội dung
    top_n=15
)

print(f"🔥 Top topics:")
for i, (topic, count) in enumerate(topics.items(), 1):
    print(f"{i}. {topic}: {count}")
```

**Output:**
```
🔥 Top topics:
1. chứng khoán: 45
2. nhà đầu tư: 32
3. thị trường: 28
4. tăng: 25
5. công ty: 22
```

---

### `get_trending(articles_df, time_window='24h', top_n=20)`

Lấy trending **trong khoảng thời gian cụ thể**.

```python
from datetime import datetime
from vnstock_news import Crawler, TrendingAnalyzer

crawler = Crawler(site_name="cafef")
articles = crawler.get_articles_from_sitemap(limit=500)

analyzer = TrendingAnalyzer()

# Lấy trending từ 7 ngày gần đây
trending = analyzer.get_trending(
    articles_df=articles,
    time_window='7d',  # '24h', '7d', '30d', '90d'
    top_n=25
)

print("📊 Trending last 7 days:")
for keyword, stats in trending.items():
    print(f"{keyword}: {stats['count']} occurrences")
```

**Output:**
```
📊 Trending last 7 days:
chứng khoán: {'count': 45, 'first_mention': 2025-01-15, 'last_mention': 2025-01-22}
nhà đầu tư: {'count': 32, ...}
```

**Parameters:**
- `articles_df` (DataFrame): DataFrame chứa tin tức (phải có cột 'publish_time')
- `time_window` (str): Khoảng thời gian ('24h', '7d', '30d', '90d')
- `top_n` (int): Top N keywords

---

### `analyze_sentiment(texts)`

Phân tích cảm xúc (Positive/Negative) trong text.

```python
analyzer = TrendingAnalyzer()

texts = [
    "Chứng khoán tăng mạnh hôm nay",  # Tích cực
    "Thị trường suy thoái, nhà đầu tư lo lắng",  # Tiêu cực
]

sentiments = analyzer.analyze_sentiment(texts)

print(sentiments)
# [{'text': '...', 'sentiment': 'positive', 'score': 0.85},
#  {'text': '...', 'sentiment': 'negative', 'score': -0.72}]
```

---

## 4. Ví Dụ Thực Tế

### Ví Dụ 1: Tìm Keyword Phổ Biến Hôm Nay

```python
from vnstock_news import Crawler, TrendingAnalyzer
import pandas as pd

# Bước 1: Lấy tin mới nhất
crawler = Crawler(site_name="cafef")
articles = crawler.get_articles_from_feed(limit_per_feed=50)

print(f"📰 Lấy {len(articles)} bài viết")

# Bước 2: Phân tích
analyzer = TrendingAnalyzer(min_frequency=2)
keywords = analyzer.extract_keywords(
    texts=articles['title'].tolist(),
    top_n=20
)

# Bước 3: Hiển thị
print("\n🔥 Các từ khóa hôm nay:\n")
for i, (keyword, count) in enumerate(keywords.items(), 1):
    print(f"{i:2d}. {keyword:20s} - {count:3d} lần")

# Bước 4: Lưu
result_df = pd.DataFrame(
    [{'keyword': k, 'frequency': v} for k, v in keywords.items()]
)
result_df.to_csv("trending_keywords.csv", index=False)
```

**Output:**
```
📰 Lấy 47 bài viết

🔥 Các từ khóa hôm nay:

 1. chứng khoán       -  45 lần
 2. nhà đầu tư        -  32 lần
 3. thị trường        -  28 lần
 4. tăng              -  25 lần
 5. giá cổ phiếu      -  20 lần
 ...
```

---

### Ví Dụ 2: So Sánh Trending Giữa 2 Báo

```python
from vnstock_news import Crawler, TrendingAnalyzer
import pandas as pd

analyzer = TrendingAnalyzer()

# Lấy từ CafeF
cafef_crawler = Crawler(site_name="cafef")
cafef_articles = cafef_crawler.get_articles_from_feed(limit_per_feed=30)
cafef_keywords = analyzer.extract_keywords(cafef_articles['title'].tolist(), top_n=10)

# Lấy từ VietStock
vietstock_crawler = Crawler(site_name="vietstock")
vietstock_articles = vietstock_crawler.get_articles_from_feed(limit_per_feed=30)
vietstock_keywords = analyzer.extract_keywords(vietstock_articles['title'].tolist(), top_n=10)

# So sánh
print("CafeF Top 10:")
for i, (k, v) in enumerate(list(cafef_keywords.items())[:10], 1):
    print(f"  {i}. {k}: {v}")

print("\nVietStock Top 10:")
for i, (k, v) in enumerate(list(vietstock_keywords.items())[:10], 1):
    print(f"  {i}. {k}: {v}")

# Keywords chỉ có ở CafeF
cafef_only = set(cafef_keywords.keys()) - set(vietstock_keywords.keys())
print(f"\nChỉ CafeF bàn luận: {cafef_only}")
```

---

### Ví Dụ 3: Trending Theo Thời Gian (Time Series)

```python
from vnstock_news import Crawler, TrendingAnalyzer
from datetime import datetime, timedelta
import pandas as pd

crawler = Crawler(site_name="cafef")

# Lấy tin từ 30 ngày gần đây
articles = crawler.get_articles_from_sitemap(limit=1000)

analyzer = TrendingAnalyzer()

# Phân tích từng tuần
trending_by_week = {}

for i in range(4):  # 4 tuần
    start_date = datetime.now() - timedelta(days=7*(i+1))
    end_date = datetime.now() - timedelta(days=7*i)
    
    # Lọc bài trong khoảng thời gian
    week_articles = articles[
        (articles['publish_time'] >= start_date) & 
        (articles['publish_time'] < end_date)
    ]
    
    if len(week_articles) > 0:
        keywords = analyzer.extract_keywords(
            week_articles['title'].tolist(),
            top_n=5
        )
        
        week_name = f"Week {4-i} ({start_date.strftime('%d/%m')} - {end_date.strftime('%d/%m')})"
        trending_by_week[week_name] = keywords

# Hiển thị
for week, keywords in trending_by_week.items():
    print(f"\n{week}:")
    for k, v in keywords.items():
        print(f"  - {k}: {v}")
```

**Output:**
```
Week 1 (08/01 - 15/01):
  - chứng khoán: 45
  - nhà đầu tư: 32

Week 2 (01/01 - 08/01):
  - lạm phát: 28
  - lãi suất: 25
```

---

### Ví Dụ 4: Real-time Monitoring Với vnstock_news Main

```python
# main.py có script news_monitor sẵn
from vnstock_news.main import news_monitor

# Hoặc sử dụng trực tiếp:
from vnstock_news import Crawler, TrendingAnalyzer
import asyncio
from datetime import datetime

async def monitor_news():
    """Monitor tin tức theo thời gian thực"""
    
    sites = ["cafef", "tuoitre", "vietstock"]
    
    crawler = Crawler()
    analyzer = TrendingAnalyzer()
    
    article_history = []
    
    while True:
        print(f"\n{'='*60}")
        print(f"📰 Monitoring at {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}")
        
        for site_name in sites:
            try:
                c = Crawler(site_name=site_name)
                articles = c.get_articles_from_feed(limit_per_feed=20)
                
                keywords = analyzer.extract_keywords(
                    articles['title'].tolist(),
                    top_n=5
                )
                
                print(f"\n📊 {site_name.upper()}:")
                for keyword, count in keywords.items():
                    print(f"  {keyword}: {count}")
                
                article_history.extend(articles.to_dict('records'))
                
            except Exception as e:
                print(f"❌ Error fetching {site_name}: {e}")
        
        # Tổng thể trending
        if len(article_history) > 0:
            print(f"\n🔥 OVERALL TRENDING (từ {len(article_history)} bài):")
            all_titles = [a['title'] for a in article_history]
            overall_keywords = analyzer.extract_keywords(all_titles, top_n=10)
            
            for i, (keyword, count) in enumerate(overall_keywords.items(), 1):
                print(f"  {i}. {keyword}: {count}")
        
        # Chờ 60 phút rồi lặp lại
        print("\n⏳ Chờ 1 giờ...")
        await asyncio.sleep(3600)

# Chạy
asyncio.run(monitor_news())
```

---

## 5. Tối Ưu Hóa Kết Quả

### Loại Bỏ Từ Không Cần

Một số từ không mang ý nghĩa (stopwords) nên loại bỏ:

```python
analyzer = TrendingAnalyzer(
    min_frequency=3,      # Loại bỏ từ xuất hiện < 3 lần
    min_word_length=3,    # Loại bỏ từ < 3 ký tự
    language='vietnamese'
)

# Dùng custom stopwords
from vnstock_news import TrendingAnalyzer

custom_stopwords = ['là', 'và', 'của', 'bị', 'được', 'có', 'cái', 'này', 'đó']

analyzer = TrendingAnalyzer(
    custom_stopwords=custom_stopwords
)
```

### Chuẩn Hóa Text

```python
def preprocess_text(text):
    """Chuẩn hóa text"""
    # Chuyển thành chữ thường
    text = text.lower()
    
    # Xóa dấu ngoặc, ký tự đặc biệt
    import re
    text = re.sub(r'[^a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ\s]', '', text)
    
    # Xóa khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# Sử dụng
articles['title_clean'] = articles['title'].apply(preprocess_text)
keywords = analyzer.extract_keywords(articles['title_clean'].tolist())
```

---

## 6. Xuất Kết Quả

### Export CSV

```python
from vnstock_news import TrendingAnalyzer
import pandas as pd

keywords = {
    'chứng khoán': 45,
    'nhà đầu tư': 32,
    'thị trường': 28
}

# Chuyển sang DataFrame
df = pd.DataFrame([
    {'keyword': k, 'frequency': v, 'percentage': v/sum(keywords.values())*100}
    for k, v in keywords.items()
])

df = df.sort_values('frequency', ascending=False)

# Lưu
df.to_csv('keywords.csv', index=False, encoding='utf-8-sig')

print(df)
```

**Output CSV:**
```
keyword,frequency,percentage
chứng khoán,45,42.86
nhà đầu tư,32,30.48
thị trường,28,26.67
```

---

### Visualize với Matplotlib

```python
import matplotlib.pyplot as plt
from vnstock_news import TrendingAnalyzer

keywords = analyzer.extract_keywords(articles['title'].tolist(), top_n=10)

# Vẽ biểu đồ
plt.figure(figsize=(12, 6))
plt.barh(list(keywords.keys()), list(keywords.values()), color='steelblue')
plt.xlabel('Frequency')
plt.title('Trending Keywords')
plt.tight_layout()
plt.savefig('keywords.png', dpi=100)
plt.show()
```

---

## 7. Best Practices

| ✅ Nên Làm | ❌ Không Nên |
|-----------|-------------|
| Phân tích từ nội dung đầy đủ (content) | Chỉ phân tích tiêu đề (có thể thiếu ngữ cảnh) |
| Loại bỏ stopwords | Giữ tất cả các từ |
| Chuẩn hóa text trước phân tích | Dùng text thô |
| Lọc theo thời gian trước phân tích | Phân tích tất cả cùng lúc |
| Đặt min_frequency phù hợp | Đặt quá cao hoặc quá thấp |
| Kết hợp nhiều nguồn tin | Chỉ dùng 1 báo |

---

## 8. Troubleshooting

| Vấn đề | Nguyên Nhân | Giải Pháp |
|-------|-----------|---------|
| Keyword không hợp lý | Stopwords không đủ | Thêm custom stopwords |
| Quá nhiều keyword tầm thường | min_frequency quá thấp | Tăng min_frequency |
| Thiếu keyword quan trọng | min_frequency quá cao | Giảm min_frequency |
| Lỗi tiếng Việt | Encoding sai | Dùng utf-8, gọi preprocess_text() |
| Chậm | Phân tích quá nhiều text | Giảm số lượng text, dùng parallel processing |

---

## Tổng Kết

**TrendingAnalyzer** giúp bạn:
- ✅ Tìm keyword phổ biến từ tin tức
- ✅ Phát hiện xu hướng theo thời gian
- ✅ So sánh trending giữa các báo
- ✅ Monitor tin tức real-time
- ✅ Phân tích cảm xúc

**Workflow cơ bản:**
```python
1. Lấy tin → Crawler.get_articles_from_feed()
2. Phân tích → TrendingAnalyzer.extract_keywords()
3. Lưu kết quả → DataFrame.to_csv()
4. Visualize → Matplotlib/Pandas plot
```
