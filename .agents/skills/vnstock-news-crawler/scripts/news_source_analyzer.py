import argparse
import sys
import datetime
import json
from dateutil.relativedelta import relativedelta

try:
    from vnstock_news.config.sites import SITES_CONFIG, SUPPORTED_SITES
except ImportError:
    print("CRITICAL: vnstock_news is not installed or accessible in this environment.")
    sys.exit(1)

def generate_dynamic_sitemap_urls(site_config, months_back):
    sitemap_rules = site_config.get('sitemap')
    if not sitemap_rules:
        return []
    
    base_url = sitemap_rules.get('base_url')
    fmt = sitemap_rules.get('format')
    ext = sitemap_rules.get('extension')
    pattern = sitemap_rules.get('pattern_type')
    
    urls = []
    
    if pattern == 'monthly':
        today = datetime.date.today()
        for i in range(months_back):
            m_date = today - relativedelta(months=i)
            # Formatting year and month according to {year}-{month} or {month:02d}
            date_str = fmt.format(year=m_date.year, month=m_date.month)
            urls.append(f"{base_url}{date_str}.{ext}")
    elif pattern == 'incremental':
        # Assume incremental gives last X pages
        for i in range(1, min(months_back * 2, 50)): # rough estimate
            urls.append(f"{base_url}{i}.{ext}")
            
    return urls

def analyze(site, timeframe):
    if site not in SUPPORTED_SITES:
        print(f"Warning: {site} is not natively supported. Assuming it relies heavily on custom config.")
        return
        
    config = SITES_CONFIG[site]
    has_rss = 'rss' in config
    has_sitemap = 'sitemap_url' in config or 'sitemap' in config
    
    print(f"--- Analysis for {site} ---")
    print(f"Capabilities: RSS={'Yes' if has_rss else 'No'}, Sitemap={'Yes' if has_sitemap else 'No'}")
    
    strategy = "sitemap" # default to sitemap
    if timeframe in ['realtime', '1d', '7d'] and has_rss:
        strategy = "rss"
        
    print(f"\nRecommended Strategy: {strategy.upper()}")
    
    sources = []
    if strategy == "rss":
        sources = config['rss']['urls']
        print(f"Use the following RSS URLs:")
        for s in sources:
            print(f" - {s}")
            
        print("\n[Snippet to copy-paste]")
        print("```python")
        print("from vnstock_news import Crawler")
        print("import pandas as pd\n")
        print(f"crawler = Crawler(site_name=\"{site}\")")
        print(f"articles = crawler.get_articles_from_feed(limit_per_feed=50)")
        print("df = pd.DataFrame(articles)")
        print("print(f\"Extracted {len(df)} articles\")")
        print("```")
        
    else:
        # Sitemap logic
        if 'sitemap_url' in config:
            sources = [config['sitemap_url']]
        elif 'sitemap' in config:
            # Dynamic sitemap calculation
            months = 1
            if timeframe == '1m': months = 1
            elif timeframe == '3m': months = 3
            elif timeframe == '6m': months = 6
            elif timeframe == '1y': months = 12
            elif timeframe == '3y': months = 36
            elif timeframe == '5y': months = 60
            elif timeframe == '10y': months = 120
            elif timeframe == 'all': months = 180 # capped reasonably
            
            sources = generate_dynamic_sitemap_urls(config, months)
            
        print(f"Use the following {len(sources)} Sitemap URLs:")
        for s in sources[:5]:
            print(f" - {s}")
        if len(sources) > 5:
            print(f" - ... and {len(sources)-5} more.")
            
        print("\n[Snippet to copy-paste]")
        print("```python")
        print("import asyncio")
        print("from vnstock_news import AsyncBatchCrawler")
        print("import pandas as pd")
        print("\nasync def fetch_historical():")
        print(f"    crawler = AsyncBatchCrawler(site_name=\"{site}\", max_concurrency=3)")
        print(f"    sources = {json.dumps(sources, indent=4)}")
        print("    articles = await crawler.fetch_articles_async(")
        print("        sources=sources,")
        print("        top_n=1000  # Adjust as needed")
        print("    )")
        print("    return articles")
        print("\ndf = asyncio.run(fetch_historical())")
        print("print(f\"Extracted {len(df)} historical articles\")")
        print("```")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vnstock News Source Analyzer")
    parser.add_argument('--site', type=str, required=True, help=f"Target site: {SUPPORTED_SITES}")
    parser.add_argument('--timeframe', type=str, choices=['realtime', '1d', '7d', '1m', '3m', '6m', '1y', '3y', '5y', '10y', 'all'], default='1m')
    args = parser.parse_args()
    analyze(args.site, args.timeframe)
