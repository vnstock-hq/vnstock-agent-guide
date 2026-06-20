#!/usr/bin/env python3
# 0 16 * * 1-5 ~/.venv/bin/python /path/to/vnstock_pipeline/job_examples/sync_market_data.py --group HOSE --mode daily
import os
import argparse
import logging
import subprocess
import sys
from datetime import datetime
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"sync_market_data_{datetime.now().strftime('%Y%m%d')}.log")
    ]
)
logger = logging.getLogger("MarketDataSync")

def run_command(cmd_list, env):
    """Run a subprocess command and log output."""
    cmd_str = ' '.join(cmd_list)
    logger.info(f"🚀 Started: {cmd_str}")
    
    start_time = time.time()
    try:
        # Run command and capture output
        result = subprocess.run(
            cmd_list,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=True
        )
        elapsed = time.time() - start_time
        logger.info(f"✅ Success ({elapsed:.1f}s): {cmd_str}")
        return True
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time
        logger.error(f"❌ Failed ({elapsed:.1f}s): {cmd_str}")
        logger.error(f"Exit code: {e.returncode}")
        logger.error(f"Output:\n{e.output}")
        return False
    except Exception as e:
        logger.exception(f"💥 Critical error running {cmd_str}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Comprehensive Market Data Sync Orchestrator")
    parser.add_argument("--group", type=str, default="HOSE", help="Stock universe group (e.g., HOSE, HNX, UPCOM, VN30, VN100)")
    parser.add_argument("--mode", type=str, default="daily", choices=["init", "daily", "eod", "live"], help="Time window mode")
    parser.add_argument("--skip-reference", action="store_true", help="Skip reference data update")
    parser.add_argument("--skip-news", action="store_true", help="Skip news data update")
    parser.add_argument("--stop-on-error", action="store_true", help="Stop execution if any task fails")
    
    args = parser.parse_args()
    
    # Define tasks to run
    tasks = []
    
    # Get the current Python interpreter (respects active virtual environment)
    python_cmd = sys.executable

    if not args.skip_reference:
        tasks.append([python_cmd, "-m", "vnstock_pipeline.cli", "run", "reference"])
        
    # Core ticker tasks
    ticker_tasks = [
        [python_cmd, "-m", "vnstock_pipeline.cli", "run", "session-stats", "--group", args.group, "--mode", args.mode],
        [python_cmd, "-m", "vnstock_pipeline.cli", "run", "ohlcv", "--group", args.group, "--mode", args.mode],
        [python_cmd, "-m", "vnstock_pipeline.cli", "run", "trades", "--group", args.group, "--mode", args.mode],
        [python_cmd, "-m", "vnstock_pipeline.cli", "run", "financial", "--group", args.group],
        [python_cmd, "-m", "vnstock_pipeline.cli", "run", "company", "--group", args.group],
        [python_cmd, "-m", "vnstock_pipeline.cli", "run", "events", "--mode", args.mode],
        [python_cmd, "-m", "vnstock_pipeline.cli", "run", "quote", "--group", args.group]
    ]
    tasks.extend(ticker_tasks)
    
    if not args.skip_news:
        tasks.append([python_cmd, "-m", "vnstock_pipeline.cli", "run", "news", "--limit", "10"])

    # Setup environment
    env = os.environ.copy()
    
    logger.info("=" * 60)
    logger.info(f"Starting Market Data Sync Pipeline")
    logger.info(f"Group: {args.group} | Mode: {args.mode}")
    logger.info(f"Total tasks: {len(tasks)}")
    logger.info("=" * 60)
    
    overall_start = time.time()
    failed_tasks = []

    for idx, cmd in enumerate(tasks, 1):
        logger.info(f"--- Task {idx}/{len(tasks)} ---")
        success = run_command(cmd, env)
        
        if not success:
            failed_tasks.append(' '.join(cmd))
            if args.stop_on_error:
                logger.error("🛑 Stopping execution due to --stop-on-error flag.")
                break
            else:
                logger.warning("⚠️ Task failed, but continuing to next task...")
                
    overall_elapsed = time.time() - overall_start
    logger.info("=" * 60)
    logger.info(f"Pipeline Completed in {overall_elapsed:.1f}s")
    
    if failed_tasks:
        logger.warning(f"⚠️ {len(failed_tasks)} tasks failed:")
        for ft in failed_tasks:
            logger.warning(f"  - {ft}")
        sys.exit(1)
    else:
        logger.info("✅ All tasks executed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
