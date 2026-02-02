# Vnstock Analysis Notebook Template
# Use this for: Prototyping, Ad-hoc Analysis, Visualizing Data

# %% [markdown]
# # Market Analysis with Vnstock
# 1. Setup Environment
# 2. Fetch Data
# 3. Apply Technical Analysis
# 4. Visualize

# %%
# 1. Imports
import pandas as pd
from vnstock import Listing, Quote  # Base data
from vnstock_ta import Indicator, Plotter, DataSource # TA tools (Paid)

# Optional: Supress warnings
import warnings
warnings.filterwarnings('ignore')

print("Libraries imported successfully!")

# %%
# 2. Configuration
SYMBOL = 'VCB'
START_DATE = '2024-01-01'
END_DATE = '2024-12-31'
INTERVAL = '1D'
SOURCE = 'VCI' # Recommended source

# %%
# 3. Fetch Data
# We use vnstock_ta.DataSource for convenience as it formats the index correctly
print(f"Fetching data for {SYMBOL}...")

try:
    ds = DataSource(symbol=SYMBOL, start=START_DATE, end=END_DATE, interval=INTERVAL, source='kbs')
    df = ds.data
    
    if df.empty:
        print("⚠️ No data found! Check symbol or date range.")
    else:
        print(f"✅ Loaded {len(df)} bars.")
        display(df.tail())
except Exception as e:
    print(f"❌ Error fetching data: {e}")

# %%
# 4. Calculate Indicators (using vnstock_ta)
if not df.empty:
    indicator = Indicator(df)
    
    # Calculate SMA and RSI
    df['SMA_20'] = indicator.sma(length=20)
    df['RSI_14'] = indicator.rsi(length=14)
    
    # MACD
    macd_df = indicator.macd(fast=12, slow=26, signal=9)
    # Join MACD back to main df
    df = df.join(macd_df)
    
    display(df[['close', 'SMA_20', 'RSI_14']].tail())

# %%
# 5. Visualization (Interactive)
if not df.empty:
    plotter = Plotter(df, theme='light', watermark=True)
    
    # Create a chart with SMA and Bollinger Bands
    # Note: methods in Plotter return the chart object
    plotter.candlestick(title=f"{SYMBOL} Technical Chart")
    plotter.sma(20, color='blue', legend=True)
    plotter.bbands(20, 2.0)
    
    # Create a separate RSI chart
    plotter.rsi(14)

    # Render is automatic in Notebooks usually, or use .render_notebook()
    print("Charts generated.")
