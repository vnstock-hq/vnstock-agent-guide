# Vnstock Analysis Notebook Template
# Use this for: Prototyping, Ad-hoc Analysis, Visualizing Data

# %% [markdown]
# # Market Analysis with Vnstock (Unified UI)
# 1. API Discovery & Configuration
# 2. Fetch Data (Unified UI)
# 3. Apply Technical Analysis
# 4. Visualize

# %%
# 1. Imports
import pandas as pd
from vnstock_data import Market, Fundamental, Reference, show_api, show_doc # Unified UI (Sponsored)
from vnstock_ta import Indicator, Plotter # TA tools (Sponsored)

# Optional: Supress warnings
import warnings
warnings.filterwarnings('ignore')

print("Libraries imported successfully!")

# %%
# 2. API Discovery (Mandatory for Research)
# Run this to see the available layers and methods
show_api()

# If you need details on a specific method:
# show_doc(Market.equity)

# %%
# 3. Configuration
SYMBOL = 'VCB'
START_DATE = '2024-01-01'
END_DATE = '2024-12-31'

# %%
# 4. Fetch Data (Unified UI Chaining)
print(f"Fetching data for {SYMBOL}...")

try:
    # Layer 2: Market Data
    mkt = Market()
    df = mkt.equity(SYMBOL).ohlcv(start=SYMBOL, end=END_DATE) # Chaining API
    
    # Layer 3: Fundamental Data (Optional example)
    # fun = Fundamental()
    # stats = fun.equity(SYMBOL).ratio()
    
    if df.empty:
        print("⚠️ No data found! Check symbol or date range.")
    else:
        print(f"✅ Loaded {len(df)} bars.")
        display(df.tail())
except Exception as e:
    print(f"❌ Error fetching data: {e}")

# %%
# 5. Calculate Indicators (using vnstock_ta)
if not df.empty:
    indicator = Indicator(df)
    
    # Calculate SMA and RSI
    df['SMA_20'] = indicator.sma(length=20)
    df['RSI_14'] = indicator.rsi(length=14)
    
    display(df[['time', 'close', 'SMA_20', 'RSI_14']].tail())

# %%
# 6. Visualization (Interactive)
if not df.empty:
    plotter = Plotter(df, theme='light', watermark=True)
    
    # Create a chart with SMA and Bollinger Bands
    plotter.candlestick(title=f"{SYMBOL} Technical Chart")
    plotter.sma(20, color='blue', legend=True)
    plotter.bbands(20, 2.0)
    
    # Create a separate RSI chart
    plotter.rsi(14)

    print("Charts generated.")
