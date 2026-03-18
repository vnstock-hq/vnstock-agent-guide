---
name: vnstock-news-crawler
description: End-to-end workflow to set up data extraction for supported news sites using `vnstock_news`. Selects optimal strategies (RSS vs Sitemap) based on timeframe and provides executable code.
version: 1.0.0
tags: [news, crawler, data, vnstock_news]
---

# `vnstock-news-crawler` Skill

## Persona Framing
> _"You are a meticulous Data Engineer. Your prime directive is to build robust, scalable news crawlers STRICTLY using the `vnstock_news` library. You MUST NEVER bypass `vnstock_news` to scrape directly with other tools on your own. You do not just create scripts; you ensure the scripts use the right extraction strategy (RSS vs Sitemap) that minimizes API failures and maximizes data freshness. If a site is difficult to parse natively, you MUST use `custom_config` inside `AsyncBatchCrawler` to extract the HTML contents natively within the library."_

## 1. Quick Reference Table

| Timeframe Request | Best Strategy | Recommended Tool | Command |
|-------------------|----------------|------------------|---------|
| Realtime / Today | **RSS** | `Crawler` | `crawler.get_articles_from_feed()` |
| 1 Week to 1 Month | **RSS / Sitemap** | `AsyncBatchCrawler`| `crawler.fetch_articles_async()` |
| 1 Year+ (History) | **Sitemap XML** | `AsyncBatchCrawler`| `crawler.fetch_articles_async()` |
| Custom Sites | **RSS / Sitemap** | `EnhancedNewsCrawler` | `fetch_articles_async()` |

---

## 2. Dependencies

This skill requires the following packages installed in the virtual environment (`.venv`):
- `vnstock_news` (Core library)
- `pandas` (Data manipulation)
- `aiohttp` / `asyncio` (Concurrent requests)

---

## 3. The Extraction Workflow

### Step 1: Context Gathering
Ask the user two critical questions if they haven't provided the info:
1. **Which news sites** are you targeting? (e.g., CafeF, TuoiTre, Custom URL).
2. **What timeframe** do you need? (e.g., Realtime updates, Last 30 days, 5 years historical).

**Exit Condition:** Do not proceed to generation until you know the exact site and the intended timeframe.

### Step 2: Source Analysis
Run the provided analyzer script to determine the exact URLs and the optimal extraction strategy. 
_The script automatically handles complex logic like TuoiTre's monthly dynamic sitemaps or VietStock's category RSS feeds._

```bash
# Run this script before generating any crawler code
python scripts/news_source_analyzer.py --site [SITE_NAME] --timeframe [TIMEFRAME]
```

**Valid arguments:**
- `--site`: `cafef`, `cafebiz`, `vietstock`, `vneconomy`, `plo`, `vnexpress`, `tuoitre`, `ktsg`, `ncdt`, `dddn`, `baodautu`
- `--timeframe`: `realtime`, `1d`, `7d`, `1m`, `3m`, `6m`, `1y`, `3y`, `5y`, `10y`, `all`

### Step 3: Code Generation
Use the snippet output by the analyzer script to generate the final crawler code for the user. **Ensure all imports are present.**

---

## 4. Code Blocks & Templates

### 📝 Template A: Realtime Updates (RSS Strategy)
Use this when the user demands up-to-the-minute news. 
**CRITICAL:** Do NOT use `custom_config` when initializing `Crawler(site_name="...")` unless you explicitly omit `site_name`.

```python
from vnstock_news import Crawler
import pandas as pd

# IMPORTANT: Passing site_name automatically loads predefined RSS/Sitemap configs
crawler = Crawler(site_name="cafebiz") 
articles = crawler.get_articles_from_feed(limit_per_feed=20)

df = pd.DataFrame(articles)
print(f"Extracted {len(df)} real-time articles")
```

### 📝 Template B: Historical Bulk Extraction (Sitemap Strategy)
Use when the user wants data spanning months or years. 

```python
import asyncio
from vnstock_news import AsyncBatchCrawler
import pandas as pd

async def fetch_historical():
    # max_concurrency should be between 2-5 to prevent rate limits
    crawler = AsyncBatchCrawler(site_name="tuoitre", max_concurrency=3)
    
    # ⚠️ CRITICAL: The `sources` array MUST be an array of absolute URLs, NOT site names.
    sources = [
        "https://tuoitre.vn/StaticSitemaps/sitemaps-2023-1.xml",
        "https://tuoitre.vn/StaticSitemaps/sitemaps-2023-2.xml"
    ]
    
    articles = await crawler.fetch_articles_async(
        sources=sources,
        top_n=500, # Limit per feed to avoid OOM
        within="1y"
    )
    return articles

if __name__ == "__main__":
    df = asyncio.run(fetch_historical())
    print(df.head())
```

```
---

### 📝 Template C: Custom Site with Content Filtering (No category in URL)
Use when the site is not natively supported and its sitemap URLs are flat (e.g., `...post123.html`), requiring you to fetch the articles first and filter by keywords in their content.

```python
import asyncio
import pandas as pd
from vnstock_news import AsyncBatchCrawler

custom_config = {
    "name": "Custom Site",
    "domain": "customsite.vn",
    "sitemap": {
        "pattern_type": "monthly",
        "base_url": "https://customsite.vn/sitemaps/news",
        "format": "-{year}-{month}",
        "extension": "xml"
    },
    "config": {
        "title_selector": {"tag": "h1", "class": "title"},
        "content_selector": {"tag": "div", "class": "article-body"}
    }
}

async def fetch_filtered_news():
    # ⚠️ CRITICAL: site_name MUST be omitted when using custom_config
    crawler = AsyncBatchCrawler(custom_config=custom_config, max_concurrency=5)
    
    # Generate explicit sitemap URL matching the pattern
    sitemap_url = "https://customsite.vn/sitemaps/news-2026-3.xml"
    
    df = await crawler.fetch_articles_async(
        sources=[sitemap_url],
        top_n=50,
        within="1d"
    )
    
    if not df.empty and 'markdown_content' in df.columns:
        # Filter natively extracted markdown content
        df_filtered = df[df['markdown_content'].str.contains('keyword1|keyword2', case=False, na=False)]
        return df_filtered
    return pd.DataFrame()

if __name__ == "__main__":
    df = asyncio.run(fetch_filtered_news())
    print(f"Extracted {len(df)} filtered articles")
```

---

## 5. Anti-Patterns (Avoid at all costs!)

- ⛔ **NEVER bypass vnstock_news internals.**
  Do not use bare `requests` + `BeautifulSoup` or any other manually. If a site's URLs lack category metadata, extract the URLs using the Sitemap approach and let `AsyncBatchCrawler(custom_config=...)` fetch the `markdown_content`. Then, filter the resulting DataFrame using Pandas string matching (e.g. `df['markdown_content'].str.contains(...)`).

- ⛔ **NEVER pass `site_name` string into `sources`.**  
  _Bad_: `AsyncBatchCrawler(..).fetch_articles_async(sources=["cafef"])`  
  _Good_: `AsyncBatchCrawler(..).fetch_articles_async(sources=["https://cafef.vn/sitemap.xml"])`

- ⛔ **NEVER assume a site has an RSS feed.**  
  CafeF, for example, defaults to Sitemap only. Always run the analyzer script to confirm capabilities.

- ⛔ **NEVER fetch full sitemap content without `top_n` limits during tests.**  
  Testing scripts should always impose `limit_per_feed=5` or `top_n=5` to prevent IP bans.

- ⛔ **NEVER nest `rss_urls` inside an `rss: { urls: ... }` dictionary in custom configs.**  
  The Crawler actively looks for the top-level keys: `rss_urls` and `config`.

---

## 6. QA Protocol (Required)

After generating the script for the user, you MUST verify it before presenting:
1. Did you run the `news_source_analyzer.py` analyzer script? 
2. Does the script instantiate the Crawler correctly?
3. If using `AsyncBatchCrawler`, are the passed `sources` absolute valid URLs (starting with `http`)?
4. Run the script with a `top_n=2` limit to confirm it extracts at least one row without exceptions.

*Assume the generated code has problems. Your job is to find them before the user does.*