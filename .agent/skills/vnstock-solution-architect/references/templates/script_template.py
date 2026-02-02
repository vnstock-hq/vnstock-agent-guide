# Vnstock Automation Script Template
# Use this for: Daily Crawling, Scheduled Tasks, Data Pipelines
# Run with: python script.py

import os
import time
import logging
from datetime import datetime
import pandas as pd

# Vnstock Ecosystem
from vnstock import Listing
from vnstock_pipeline.tasks.ohlcv import run_task as run_ohlcv
from vnstock_news import BatchCrawler

# --- 1. Setup Logging ---
# Professional logging is crucial for automation
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
        # Get list of symbols
        listing = Listing(source='VCI')
        symbols = listing.symbols_by_group(group=SYMBOLS_GROUP).tolist()
        logger.info(f"Targeting {len(symbols)} symbols from {SYMBOLS_GROUP}")
        
        # Use Pipeline for robust fetching (Handles retries/errors)
        run_ohlcv(
            symbols, 
            start=datetime.now().replace(month=1, day=1).strftime("%Y-%m-%d"), # YTD
            end=datetime.now().strftime("%Y-%m-%d"),
            interval="1D"
        )
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
    logger.info("=== Automation Started ===")
    start_time = time.time()
    
    ensure_directories()
    
    step_1_update_market_data()
    step_2_fetch_news()
    
    duration = time.time() - start_time
    logger.info(f"=== Automation Finished in {duration:.2f} seconds ===")

if __name__ == "__main__":
    main()
