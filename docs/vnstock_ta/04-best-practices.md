# Vnstock TA - Best Practices & Patterns

## Giới Thiệu

Chương này cung cấp các best practices, patterns phổ biến, và tips & tricks khi sử dụng vnstock_ta trong các tình huống thực tế.

---

## I. DATA PREPARATION - Chuẩn Bị Dữ Liệu

### 1. Đặt Đúng Format DataFrame

**Yêu cầu**:
- Index phải là `DatetimeIndex` với tên `'time'`
- Phải có cột: `'open'`, `'high'`, `'low'`, `'close'`, `'volume'`

**Ví dụ đúng**:

```python
from vnstock_data import Quote
from vnstock_ta import Indicator

# Lấy dữ liệu từ vnstock_data
quote = Quote(source="vnd", symbol="VCB")
df = quote.history(start="2024-09-01", end="2024-12-02", interval="1D")

# Đặt index là 'time'
df = df.set_index('time')

# Kiểm tra format
print(df.index)  # DatetimeIndex
print(df.columns)  # ['close', 'open', 'high', 'low', 'volume']

# Bây giờ có thể dùng với vnstock_ta
indicator = Indicator(data=df)
```

### 2. Xử Lý Dữ Liệu Thiếu

```python
# Kiểm tra NaN
print(df.isnull().sum())

# Loại bỏ NaN
df = df.dropna()

# Fill forward (fill từ trước)
df = df.fillna(method='ffill')

# Fill bằng giá trị cụ thể
df = df.fillna(df.mean())
```

### 3. Xử Lý Ngoại Lệ (Outliers)

```python
# Xóa outliers với IQR
Q1 = df['close'].quantile(0.25)
Q3 = df['close'].quantile(0.75)
IQR = Q3 - Q1
df = df[~((df['close'] < (Q1 - 1.5*IQR)) | (df['close'] > (Q3 + 1.5*IQR)))]
```

---

## II. INDICATOR COMBINATION - Kết Hợp Chỉ Báo

### 1. Trend Following (Theo Xu Hướng)

**Mục đích**: Xác định xu hướng và vào lệnh theo chiều xu hướng.

**Chỉ báo**:
- SMA/EMA: Xác định xu hướng
- ADX: Xác nhận cường độ
- SUPERTREND: Xác định điểm vào và stop loss

**Code**:

```python
from vnstock_data import Quote
from vnstock_ta import Indicator
import pandas as pd

quote = Quote(source="vnd", symbol="VCB")
df = quote.history(start="2024-09-01", end="2024-12-02", interval="1D")
df = df.set_index('time')

indicator = Indicator(data=df)

# Trend indicators
sma20 = indicator.sma(length=20)
sma50 = indicator.sma(length=50)
adx = indicator.adx(length=14)
supertrend = indicator.supertrend(length=10, multiplier=3)

# Tạo signal
df['SMA20'] = sma20
df['SMA50'] = sma50
df['ADX'] = adx['ADX_14']
df['ST'] = supertrend['SUPERT_10_3.0']
df['STd'] = supertrend['SUPERTd_10_3.0']

# Logic: Mua khi SMA20 > SMA50 và ADX > 25
df['Buy_Signal'] = (
    (df['SMA20'] > df['SMA50']) & 
    (df['ADX'] > 25) & 
    (df['STd'] == 1)
).astype(int)

# Bán: Khi divergence
df['Sell_Signal'] = (
    (df['SMA20'] < df['SMA50']) | 
    (df['STd'] == -1)
).astype(int)

print("Buy signals:", df['Buy_Signal'].sum())
print("Sell signals:", df['Sell_Signal'].sum())
```

### 2. Mean Reversion (Giao Dịch Quay Về Trung Bình)

**Mục đích**: Bắt cơ hội khi giá quay lại trung bình.

**Chỉ báo**:
- Bollinger Bands: Xác định quá mức
- RSI: Xác nhận overbought/oversold
- STOCH: Xác định entry point

**Code**:

```python
indicator = Indicator(data=df)

# Mean reversion indicators
bbands = indicator.bbands(length=20, std=2)
rsi = indicator.rsi(length=14)
stoch = indicator.stoch(k=14, d=3, smooth_k=3)

df['BBL'] = bbands['BBL_20_2.0']
df['BBM'] = bbands['BBM_20_2.0']
df['BBU'] = bbands['BBU_20_2.0']
df['RSI'] = rsi
df['STOCHk'] = stoch['STOCHk_14_3_3']
df['STOCHd'] = stoch['STOCHd_14_3_3']

# Logic: Mua khi giá chạm BBL và RSI < 30
df['Buy_MR'] = (
    (df['close'] <= df['BBL']) & 
    (df['RSI'] < 30)
).astype(int)

# Bán: Khi giá trở lại BBM hoặc RSI > 70
df['Sell_MR'] = (
    (df['close'] >= df['BBM']) | 
    (df['RSI'] > 70)
).astype(int)

print("Mean reversion buys:", df['Buy_MR'].sum())
```

### 3. Momentum Trading (Giao Dịch Động Lực)

**Mục đích**: Bắt sóng khi động lực mạnh.

**Chỉ báo**:
- MACD: Golden cross/death cross
- ROC: Tốc độ thay đổi
- OBV: Xác nhận khối lượng

**Code**:

```python
indicator = Indicator(data=df)

# Momentum indicators
macd = indicator.macd(fast=12, slow=26, signal=9)
roc = indicator.roc(length=9)
obv = indicator.obv()

df['MACD'] = macd['MACD_12_26_9']
df['Signal'] = macd['MACDs_12_26_9']
df['Histogram'] = macd['MACDh_12_26_9']
df['ROC'] = roc
df['OBV'] = obv

# Logic: Mua khi MACD vượt Signal
df['MACD_Cross'] = (df['MACD'] > df['Signal']).astype(int)
df['MACD_Buy'] = (df['MACD_Cross'] != df['MACD_Cross'].shift(1)) & (df['MACD_Cross'] == 1)

# Xác nhận: ROC > 0 và OBV tăng
df['OBV_Trend'] = (df['OBV'] > df['OBV'].shift(1)).astype(int)
df['Buy_Momentum'] = (
    df['MACD_Buy'] & 
    (df['ROC'] > 0) & 
    (df['OBV_Trend'] == 1)
).astype(int)

print("Momentum buy signals:", df['Buy_Momentum'].sum())
```

### 4. Volatility-Based Trading (Giao Dịch Dựa Trên Biến Động)

**Mục đích**: Điều chỉnh strategy theo mức biến động.

**Chỉ báo**:
- ATR: Đo biến động
- Bollinger Bands: Dải biến động
- STDEV: Độ lệch chuẩn

**Code**:

```python
indicator = Indicator(data=df)

# Volatility indicators
atr = indicator.atr(length=14)
bbands = indicator.bbands(length=20, std=2)
stdev = indicator.stdev(length=14, ddof=1)

df['ATR'] = atr
df['BBB'] = bbands['BBB_20_2.0']  # Bandwidth
df['STDEV'] = stdev

# Xác định mức biến động
df['Volatility_Level'] = pd.cut(
    df['ATR'],
    bins=[0, df['ATR'].quantile(0.33), df['ATR'].quantile(0.67), float('inf')],
    labels=['Low', 'Medium', 'High']
)

# Điều chỉnh stop loss theo ATR
df['Stop_Loss'] = df['close'] - (df['ATR'] * 2)
df['Take_Profit'] = df['close'] + (df['ATR'] * 3)

print(df[['ATR', 'Volatility_Level', 'Stop_Loss', 'Take_Profit']].tail())
```

---

## III. BACKTEST PATTERNS - Pattern Backtesting

### 1. Simple Backtest Framework

```python
from vnstock_data import Quote
from vnstock_ta import Indicator
import pandas as pd

def backtest_sma_crossover(symbol, start, end, sma_short=20, sma_long=50):
    """
    Backtest SMA Crossover Strategy
    
    Logic:
    - Mua: SMA20 vượt SMA50 từ dưới lên
    - Bán: SMA20 xuyên SMA50 từ trên xuống
    """
    
    # Lấy dữ liệu
    quote = Quote(source="vnd", symbol=symbol)
    df = quote.history(start=start, end=end, interval="1D")
    df = df.set_index('time')
    
    # Tính chỉ báo
    indicator = Indicator(data=df)
    sma_s = indicator.sma(length=sma_short)
    sma_l = indicator.sma(length=sma_long)
    
    df['SMA_Short'] = sma_s
    df['SMA_Long'] = sma_l
    
    # Tín hiệu
    df['Signal'] = 0
    df.loc[df['SMA_Short'] > df['SMA_Long'], 'Signal'] = 1  # Bullish
    df.loc[df['SMA_Short'] < df['SMA_Long'], 'Signal'] = -1  # Bearish
    
    # Tìm crossover
    df['Position'] = df['Signal'].diff()  # 2 = buy signal, -2 = sell signal
    
    # Tính toán P&L
    trades = []
    entry_price = None
    entry_date = None
    
    for idx, row in df.iterrows():
        if row['Position'] == 2:  # Buy
            entry_price = row['close']
            entry_date = idx
        elif row['Position'] == -2:  # Sell
            if entry_price:
                pnl = (row['close'] - entry_price) / entry_price * 100
                trades.append({
                    'entry_date': entry_date,
                    'entry_price': entry_price,
                    'exit_date': idx,
                    'exit_price': row['close'],
                    'pnl_pct': pnl
                })
                entry_price = None
                entry_date = None
    
    # Kết quả
    trades_df = pd.DataFrame(trades)
    if len(trades_df) > 0:
        win_rate = (trades_df['pnl_pct'] > 0).sum() / len(trades_df) * 100
        avg_pnl = trades_df['pnl_pct'].mean()
        total_pnl = trades_df['pnl_pct'].sum()
        
        print(f"Total trades: {len(trades_df)}")
        print(f"Win rate: {win_rate:.2f}%")
        print(f"Avg PnL: {avg_pnl:.2f}%")
        print(f"Total PnL: {total_pnl:.2f}%")
    else:
        print("No trades generated")
    
    return trades_df

# Chạy backtest
trades = backtest_sma_crossover('VCB', '2024-01-01', '2024-12-02', sma_short=20, sma_long=50)
```

### 2. Backtest với Stop Loss & Take Profit

```python
def backtest_with_sl_tp(symbol, start, end, atr_multiplier_sl=2, atr_multiplier_tp=3):
    """Backtest với ATR-based Stop Loss & Take Profit"""
    
    quote = Quote(source="vnd", symbol=symbol)
    df = quote.history(start=start, end=end, interval="1D")
    df = df.set_index('time')
    
    indicator = Indicator(data=df)
    rsi = indicator.rsi(length=14)
    atr = indicator.atr(length=14)
    
    df['RSI'] = rsi
    df['ATR'] = atr
    
    # Trading logic
    trades = []
    position = None
    
    for idx in range(len(df)):
        row = df.iloc[idx]
        
        # Entry: RSI < 30 (oversold)
        if position is None and row['RSI'] < 30:
            position = {
                'entry_idx': idx,
                'entry_price': row['close'],
                'entry_date': row.name,
                'stop_loss': row['close'] - (row['ATR'] * atr_multiplier_sl),
                'take_profit': row['close'] + (row['ATR'] * atr_multiplier_tp)
            }
        
        # Exit: SL hoặc TP
        elif position is not None:
            row_curr = df.iloc[idx]
            
            # Hit SL
            if row_curr['low'] <= position['stop_loss']:
                pnl = (position['stop_loss'] - position['entry_price']) / position['entry_price'] * 100
                trades.append({
                    'entry_date': position['entry_date'],
                    'entry_price': position['entry_price'],
                    'exit_date': row.name,
                    'exit_price': position['stop_loss'],
                    'pnl_pct': pnl,
                    'exit_reason': 'SL'
                })
                position = None
            
            # Hit TP
            elif row_curr['high'] >= position['take_profit']:
                pnl = (position['take_profit'] - position['entry_price']) / position['entry_price'] * 100
                trades.append({
                    'entry_date': position['entry_date'],
                    'entry_price': position['entry_price'],
                    'exit_date': row.name,
                    'exit_price': position['take_profit'],
                    'pnl_pct': pnl,
                    'exit_reason': 'TP'
                })
                position = None
    
    trades_df = pd.DataFrame(trades)
    
    if len(trades_df) > 0:
        print(f"Total trades: {len(trades_df)}")
        print(f"Win rate: {(trades_df['pnl_pct'] > 0).sum() / len(trades_df) * 100:.2f}%")
        print(f"Avg win: {trades_df[trades_df['pnl_pct'] > 0]['pnl_pct'].mean():.2f}%")
        print(f"Avg loss: {trades_df[trades_df['pnl_pct'] < 0]['pnl_pct'].mean():.2f}%")
        print(f"Total PnL: {trades_df['pnl_pct'].sum():.2f}%")
    
    return trades_df

# Chạy backtest
trades = backtest_with_sl_tp('VCB', '2024-01-01', '2024-12-02', atr_multiplier_sl=2, atr_multiplier_tp=3)
```

---

## IV. PARAMETER OPTIMIZATION - Tối Ưu Hóa Tham Số

### 1. Grid Search cho SMA Crossover

```python
def optimize_sma(symbol, start, end):
    """Tìm kỳ SMA tốt nhất"""
    
    quote = Quote(source="vnd", symbol=symbol)
    df = quote.history(start=start, end=end, interval="1D")
    df = df.set_index('time')
    
    results = []
    
    # Grid search
    for short in [5, 10, 15, 20, 25]:
        for long in [50, 100, 150, 200]:
            if short >= long:
                continue
            
            indicator = Indicator(data=df)
            sma_s = indicator.sma(length=short)
            sma_l = indicator.sma(length=long)
            
            df[f'SMA_{short}'] = sma_s
            df[f'SMA_{long}'] = sma_l
            
            # Tính signals
            df['Signal'] = (df[f'SMA_{short}'] > df[f'SMA_{long}']).astype(int)
            
            # Đếm crossovers
            crossovers = df['Signal'].diff().abs().sum()
            
            # Tính return
            df['Returns'] = df['close'].pct_change()
            df['Strategy_Returns'] = df['Signal'].shift(1) * df['Returns']
            total_return = (1 + df['Strategy_Returns']).prod() - 1
            
            results.append({
                'short': short,
                'long': long,
                'crossovers': crossovers,
                'total_return': total_return * 100,
                'return_per_trade': (total_return / crossovers * 100) if crossovers > 0 else 0
            })
    
    results_df = pd.DataFrame(results).sort_values('total_return', ascending=False)
    print(results_df.head(10))
    
    return results_df

# Chạy optimization
best_params = optimize_sma('VCB', '2024-01-01', '2024-12-02')
```

---

## V. REAL-TIME MONITORING - Giám Sát Real-Time

### 1. Daily Alert System

```python
def generate_daily_alerts(symbol):
    """Tạo alert hàng ngày"""
    
    quote = Quote(source="vnd", symbol=symbol)
    df = quote.history(start="2024-11-01", end="2024-12-02", interval="1D")
    df = df.set_index('time')
    
    # Lấy dữ liệu mới nhất
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    indicator = Indicator(data=df)
    rsi = indicator.rsi(length=14)
    macd = indicator.macd(fast=12, slow=26, signal=9)
    supertrend = indicator.supertrend(length=10, multiplier=3)
    
    alerts = []
    
    # Alert 1: RSI < 30 (Oversold)
    if rsi.iloc[-1] < 30:
        alerts.append({
            'time': latest.name,
            'symbol': symbol,
            'type': 'OVERSOLD',
            'indicator': 'RSI',
            'value': rsi.iloc[-1],
            'message': f'{symbol}: RSI = {rsi.iloc[-1]:.2f} (Oversold)'
        })
    
    # Alert 2: MACD Crossover
    if (macd['MACD_12_26_9'].iloc[-2] < macd['MACDs_12_26_9'].iloc[-2] and 
        macd['MACD_12_26_9'].iloc[-1] > macd['MACDs_12_26_9'].iloc[-1]):
        alerts.append({
            'time': latest.name,
            'symbol': symbol,
            'type': 'BUY',
            'indicator': 'MACD',
            'value': macd['MACD_12_26_9'].iloc[-1],
            'message': f'{symbol}: MACD Golden Cross'
        })
    
    # Alert 3: Supertrend Reversal
    if (supertrend['SUPERTd_10_3.0'].iloc[-2] == -1 and 
        supertrend['SUPERTd_10_3.0'].iloc[-1] == 1):
        alerts.append({
            'time': latest.name,
            'symbol': symbol,
            'type': 'REVERSAL',
            'indicator': 'SUPERTREND',
            'value': supertrend['SUPERT_10_3.0'].iloc[-1],
            'message': f'{symbol}: Supertrend Up Signal'
        })
    
    return pd.DataFrame(alerts)

# Tạo alert
alerts = generate_daily_alerts('VCB')
print(alerts)
```

---

## VI. COMMON MISTAKES - Những Lỗi Phổ Biến

### ❌ Lỗi 1: Forget to set index as datetime

```python
# ❌ Sai
indicator = Indicator(data=df)  # df có RangeIndex

# ✅ Đúng
df = df.set_index('time')
indicator = Indicator(data=df)
```

### ❌ Lỗi 2: Using different data sources for same indicators

```python
# ❌ Sai: Mix data từ 2 nguồn khác
quote_vci = Quote(source="vci", symbol="VCB")
quote_vnd = Quote(source="vnd", symbol="VCB")
df_vci = quote_vci.history(...)
df_vnd = quote_vnd.history(...)
# Kết hợp df_vci và df_vnd -> kết quả không nhất quán

# ✅ Đúng: Dùng một nguồn
quote = Quote(source="vnd", symbol="VCB")
df = quote.history(...)
```

### ❌ Lỗi 3: Ignoring NaN values

```python
# ❌ Sai: Không xử lý NaN
sma = indicator.sma(length=20)
print((sma > df['close']).sum())  # Kết quả không chính xác vì có NaN

# ✅ Đúng: Drop NaN
print((sma.dropna() > df['close'].dropna()).sum())
```

### ❌ Lỗi 4: Over-optimization

```python
# ❌ Sai: Tối ưu dữ liệu lịch sử
# Test trên năm 2024, params tối ưu cho năm 2024
# Nhưng year 2025 kết quả tệ

# ✅ Đúng: Out-of-sample test
# Tối ưu trên 2024-01 to 2024-08
# Test trên 2024-09 to 2024-12
```

### ❌ Lỗi 5: Relying on single indicator

```python
# ❌ Sai: Chỉ dùng RSI
if rsi > 70:
    sell()

# ✅ Đúng: Kết hợp nhiều chỉ báo
if rsi > 70 and macd < signal and supertrend == -1:
    sell()
```

---

## VII. TIPS & TRICKS

### 1. Tính toán lỗi một lần

```python
# ❌ Inefficient: Tính nhiều lần
for i in range(100):
    rsi = indicator.rsi(length=14)

# ✅ Efficient: Tính một lần, reuse
rsi = indicator.rsi(length=14)
for i in range(100):
    use(rsi)
```

### 2. Lưu kết quả giữa các lần chạy

```python
import pickle

# Lưu
indicator_results = {
    'sma': indicator.sma(length=20),
    'rsi': indicator.rsi(length=14),
    'macd': indicator.macd()
}
with open('indicators.pkl', 'wb') as f:
    pickle.dump(indicator_results, f)

# Load
with open('indicators.pkl', 'rb') as f:
    results = pickle.load(f)
```

### 3. Kết hợp với pandas operations

```python
# Tích hợp kết quả vào DataFrame
df['SMA20'] = indicator.sma(length=20)
df['SMA50'] = indicator.sma(length=50)
df['SMA_Signal'] = (df['SMA20'] > df['SMA50']).astype(int)

# Dễ dàng phân tích
print(df[df['SMA_Signal'] == 1])
```

---

## VIII. PERFORMANCE BENCHMARKS

Thời gian tính toán cho 1000 bars dữ liệu:

| Chỉ báo | Thời gian | Ghi chú |
|---------|-----------|---------|
| SMA | < 1ms | Rất nhanh |
| EMA | < 1ms | Rất nhanh |
| RSI | 2-3ms | Nhanh |
| MACD | 2-3ms | Nhanh |
| BBANDS | 3-5ms | Trung bình |
| ATR | 5-10ms | Trung bình |
| SUPERTREND | 10-20ms | Chậm hơn |

---

## IX. Tài Liệu Tham Khảo

- **vnstock_data**: https://vnstocks.com/
- **pandas-ta**: https://github.com/twopirllc/pandas-ta
- **TradingView**: https://www.tradingview.com/education/
- **Investopedia**: https://www.investopedia.com/
