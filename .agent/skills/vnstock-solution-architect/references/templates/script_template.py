# Vnstock Automation Script Template
# Use this for: Daily Crawling, Scheduled Tasks, Data Pipelines
# Run with: python script.py

import os
import time
import logging
from datetime import datetime
import pandas as pd

# Vnstock Ecosystem
def get_vnstock_data_version():
    try:
        import vnstock_data
        return getattr(vnstock_data, "__version__", "2.0.0")
    except ImportError:
        try:
            from importlib.metadata import version
            return version("vnstock_data")
        except:
            return "0.0.0"

VNSTOCK_DATA_VERSION = get_vnstock_data_version()
HAS_VNSTOCK_DATA = VNSTOCK_DATA_VERSION != "0.0.0"

if HAS_VNSTOCK_DATA and VNSTOCK_DATA_VERSION >= '3.0.0':
    from vnstock_data import Market, Reference, Fundamental, show_api
else:
    # Use fallback or legacy imports if needed
    pass

from vnstock_news import BatchCrawler

# --- 1. Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("VnstockBot")

# --- 2. Configuration ---
DATA_DIR = "./data_warehouse"
SYMBOLS_GROUP = "VN30"
NEWS_SITE = "cafef"
NEWS_LIMIT = 50

def ensure_directories():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "market"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "news"), exist_ok=True)

def step_1_update_market_data():
    logger.info(">>> STEP 1: Updating Market Data")
    try:
        if HAS_VNSTOCK_DATA and VNSTOCK_DATA_VERSION >= '3.0.0':
            # Use Unified UI (Layer 1 & 2)
            ref = Reference()
            mkt = Market()
            
            symbols = ref.equity.list()['symbol'].head(30).tolist() # Example: Get first 30 symbols
            logger.info(f"Targeting {len(symbols)} symbols using Unified UI")
            
            for symbol in symbols:
                df = mkt.equity(symbol).ohlcv(
                    start=datetime.now().replace(month=1, day=1).strftime("%Y-%m-%d"),
                    end=datetime.now().strftime("%Y-%m-%d")
                )
                if not df.empty:
                    filename = os.path.join(DATA_DIR, "market", f"{symbol}.csv")
                    df.to_csv(filename, index=False)
        else:
            # Legacy Path
            logger.warning("Using legacy vnstock library or older vnstock_data version")
            # Implement legacy fetching if needed
            
        logger.info("Market data update complete.")
        
    except Exception as e:
        logger.error(f"Failed in Step 1: {e}")

def step_2_fetch_news():
    logger.info(">>> STEP 2: Fetching Latest News")
    try:
        crawler = BatchCrawler(site_name=NEWS_SITE)
        articles = crawler.fetch_articles(limit=NEWS_LIMIT)
        
        filename = os.path.join(DATA_DIR, "news", f"news_{datetime.now().strftime('%Y%m%d')}.csv")
        articles.to_csv(filename, index=False)
        logger.info(f"Saved {len(articles)} articles to {filename}")
        
    except Exception as e:
        logger.error(f"Failed in Step 2: {e}")

def main():
    logger.info(f"=== Automation Started (vnstock_data: {VNSTOCK_DATA_VERSION if HAS_VNSTOCK_DATA else 'N/A'}) ===")
    start_time = time.time()
    
    ensure_directories()
    
    step_1_update_market_data()
    step_2_fetch_news()
    
    duration = time.time() - start_time
    logger.info(f"=== Automation Finished in {duration:.2f} seconds ===")

if __name__ == "__main__":
    main()
