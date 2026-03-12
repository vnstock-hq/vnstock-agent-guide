# Vnstock Streamlit Dashboard Template
# Run with: streamlit run app.py
# Use this for: Interactive Dashboards, Sharing Tools, Monitoring

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Import Vnstock ecosystem
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
    from vnstock_data import Market, Fundamental, Reference

from vnstock_ta import Indicator, Plotter

# --- Page Config ---
st.set_page_config(
    page_title="Vnstock Unified Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar Controls ---
st.sidebar.title("Configuration")
symbol = st.sidebar.text_input("Stock Symbol", value="TCB").upper()
days_back = st.sidebar.slider("History (Days)", min_value=30, max_value=365*2, value=180)

st.sidebar.markdown("---")
st.sidebar.subheader("Indicators")
show_sma = st.sidebar.checkbox("Show SMA 20", value=True)
show_bbands = st.sidebar.checkbox("Show Bollinger Bands", value=False)
show_rsi = st.sidebar.checkbox("Show RSI", value=True)

# --- Data Loading (Cached) ---
@st.cache_data(ttl=600) # Cache for 10 minutes
def load_data(symbol, days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    s_str = start_date.strftime("%Y-%m-%d")
    e_str = end_date.strftime("%Y-%m-%d")
    
    try:
        if HAS_VNSTOCK_DATA and VNSTOCK_DATA_VERSION >= '3.0.0':
            # Use Unified UI (Layer 2)
            mkt = Market()
            return mkt.equity(symbol).ohlcv(start=s_str, end=e_str)
        else:
            # Fallback for old version or free library
            from vnstock import Quote
            quote = Quote(symbol=symbol, source='kbs')
            return quote.history(start=s_str, end=e_str)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# --- Main App ---
st.title(f"📈 {symbol} Analysis Dashboard")
if HAS_VNSTOCK_DATA:
    st.info(f"Using vnstock_data v{VNSTOCK_DATA_VERSION} (Unified UI)")

# Load Data
with st.spinner("Fetching market data..."):
    df = load_data(symbol, days_back)

if df.empty:
    st.warning("No data found. Please check the symbol.")
    st.stop()

# --- Metrics Row ---
last_close = df['close'].iloc[-1]
prev_close = df['close'].iloc[-2]
change = last_close - prev_close
change_pct = (change / prev_close) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Last Price", f"{last_close:,.0f}", f"{change:,.0f} ({change_pct:.2f}%)")
col2.metric("Volume", f"{df['volume'].iloc[-1]:,.0f}")
col3.metric("High/Low", f"{df['high'].iloc[-1]:,.0f} / {df['low'].iloc[-1]:,.0f}")

# --- Charting ---
st.subheader("Technical Chart")

# Calculation
indicator = Indicator(df)
chart_data = df[['time', 'close']].copy()

if show_sma:
    chart_data['SMA_20'] = indicator.sma(20)

# Display (Simple Streamlit Chart or Plotter)
st.line_chart(chart_data.set_index('time'))

if show_rsi:
    st.subheader("Relative Strength Index (14)")
    rsi_data = indicator.rsi(14)
    st.line_chart(rsi_data)

# --- Fundamental Analysis (Unified UI) ---
if HAS_VNSTOCK_DATA and VNSTOCK_DATA_VERSION >= '3.0.0':
    with st.expander("Company Fundamentals (Layer 3)"):
        fun = Fundamental()
        ratios = fun.equity(symbol).ratio()
        st.dataframe(ratios.tail(10))

st.markdown("---")
st.caption("Powered by Vnstock Ecosystem | Unified Financial Data Platform")
