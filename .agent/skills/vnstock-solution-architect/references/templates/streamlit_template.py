# Vnstock Streamlit Dashboard Template
# Run with: streamlit run app.py
# Use this for: Interactive Dashboards, Sharing Tools, Monitoring

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Import Vnstock ecosystem
from vnstock import Listing, Quote 
from vnstock_ta import Indicator, Plotter, DataSource

# --- Page Config ---
st.set_page_config(
    page_title="Vnstock Pro Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar Controls ---
st.sidebar.title("Configuration")
symbol = st.sidebar.text_input("Stock Symbol", value="VCB").upper()
days_back = st.sidebar.slider("History (Days)", min_value=30, max_value=365*2, value=180)
resolution = st.sidebar.selectbox("Resolution", ["1D", "1H", "15m"], index=0)

st.sidebar.markdown("---")
st.sidebar.subheader("Indicators")
show_sma = st.sidebar.checkbox("Show SMA 20", value=True)
show_bbands = st.sidebar.checkbox("Show Bollinger Bands", value=False)
show_rsi = st.sidebar.checkbox("Show RSI", value=True)

# --- Data Loading (Cached) ---
@st.cache_data(ttl=600) # Cache for 10 minutes
def load_data(symbol, days, res):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    s_str = start_date.strftime("%Y-%m-%d")
    e_str = end_date.strftime("%Y-%m-%d")
    
    try:
        # Use vnstock_ta.DataSource for formatting
        ds = DataSource(symbol=symbol, start=s_str, end=e_str, interval=res, source='kbs')
        return ds.data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# --- Main App ---
st.title(f"📈 {symbol} Technical Analysis")

# Load Data
with st.spinner("Fetching market data..."):
    df = load_data(symbol, days_back, resolution)

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

# --- Charting (using vnstock_ta Plotter) ---
# vnstock_ta uses pyecharts which might need html embedding in streamlit, 
# OR we can use simple streamlit charts if pyecharts is complex.
# BUT Plotter is the "Power Tool". Let's assume user wants simple st charts for availability
# or we can extract data for graphs.

# For this template, we'll use Streamlit's native charts for reliability, 
# but calculating indicators with vnstock_ta.

indicator = Indicator(df)
chart_data = df[['close']].copy()

if show_sma:
    chart_data['SMA_20'] = indicator.sma(20)
if show_bbands:
    bb = indicator.bbands(20, 2.0)
    chart_data = chart_data.join(bb)

st.line_chart(chart_data)

if show_rsi:
    st.subheader("Relative Strength Index (14)")
    rsi_data = indicator.rsi(14)
    st.line_chart(rsi_data)

st.markdown("---")
st.caption("Powered by Vnstock Ecosystem")
