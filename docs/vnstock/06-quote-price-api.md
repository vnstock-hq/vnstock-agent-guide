# 04 - Quote & Price API - Giá Lịch Sử & Dữ Liệu Real-time

## 📖 Giới Thiệu

Quote API cung cấp các phương thức lấy dữ liệu giá chứng khoán, bao gồm:

- **Giá lịch sử (Historical Data)**: OHLCV data từ các khoảng thời gian khác nhau
- **Dữ liệu trong ngày (Intraday)**: Giá thực tế theo từng phút/giờ
- **Bảng giá realtime (Price Board)**: Giá mua/bán, khối lượng hiện tại
- **Độ sâu giá (Price Depth)**: Order book, mức bid/ask
- **Các chỉ số kỹ thuật**: Volume, Volatility, Moving Averages

### 🚀 Quick Start

```python
from vnstock import Quote
from vnstock.core.types import TimeFrame

quote = Quote(source="vci", symbol="VCI")

# Lấy giá hàng ngày - Dùng string format
df = quote.history(start="2024-01-01", end="2024-12-31", resolution="1D")

# Hoặc dùng TimeFrame enum
df = quote.history(start="2024-01-01", end="2024-12-31", resolution=TimeFrame.DAILY)

# TimeFrame options: "1m", "5m", "15m", "30m", "1H", "1D", "1W", "1M"
# Hoặc: TimeFrame.MINUTE_5, TimeFrame.HOUR_1, TimeFrame.DAILY, TimeFrame.WEEKLY, etc.
```

## 🏗️ Khởi Tạo

```python
from vnstock import Quote
from vnstock.core.types import TimeFrame, DataSource

# Khởi tạo Quote adapter
# Hỗ trợ: VCI (khuyến nghị), TCBS, MSN
quote = Quote(
    source="vci",           # Nguồn dữ liệu
    symbol="VCI",           # Mã chứng khoán
    random_agent=False,     # Sử dụng random user agent
    show_log=True           # Hiển thị log chi tiết
)

# Hoặc khởi tạo mà chưa chọn symbol
quote = Quote(source="vci", symbol="")

# Thay đổi symbol sau
quote.symbol = "ACB"
```

## 📊 Dữ Liệu OHLCV

OHLCV là viết tắt của:

- **O**pen (Giá mở): Giá đóng cửa hôm trước
- **H**igh (Giá cao): Giá cao nhất trong khoảng thời gian
- **L**ow (Giá thấp): Giá thấp nhất trong khoảng thời gian
- **C**lose (Giá đóng): Giá cuối cùng trong khoảng thời gian
- **V**olume (Khối lượng): Số lượng cổ phiếu giao dịch

```
Ví dụ:
         time   open   high    low  close     volume
0  2024-01-01  21.00  21.50  20.80  21.40   1234567
1  2024-01-02  21.40  21.80  21.10  21.50   2345678
2  2024-01-03  21.50  21.90  21.30  21.60   1567890
```

## 🔄 Các TimeFrame (Khung Thời Gian)

### Supported TimeFrames

vnstock 3.3.0 hỗ trợ **21 định dạng interval** khác nhau. Bạn có thể sử dụng:
1. **TimeFrame enum** - Kiểu an toàn, có autocompletion
2. **String format MT5** - Kiểu viết tắt phổ biến
3. **Alias names** - Các tên gọi khác (DAILY, WEEKLY, MONTHLY)

#### 1️⃣ Định Dạng Tiêu Chuẩn (9 định dạng)

| TimeFrame Enum | String Format | Mô Tả |
|---|---|---|
| `TimeFrame.MINUTE_1` | `"1m"` | 1 phút |
| `TimeFrame.MINUTE_5` | `"5m"` | 5 phút |
| `TimeFrame.MINUTE_15` | `"15m"` | 15 phút |
| `TimeFrame.MINUTE_30` | `"30m"` | 30 phút |
| `TimeFrame.HOUR_1` | `"1H"` | 1 giờ |
| `TimeFrame.HOUR_4` | `"4h"` | 4 giờ |
| `TimeFrame.DAY_1` | `"1D"` | 1 ngày |
| `TimeFrame.WEEK_1` | `"1W"` | 1 tuần |
| `TimeFrame.MONTH_1` | `"1M"` | 1 tháng |

#### 2️⃣ Biến Thể Viết Thường (3 định dạng)

Hỗ trợ viết thường để tiện lợi và tương thích với các trading platform khác:

| String Format | Tương Đương | Mô Tả |
|---|---|---|
| `"1h"` | `"1H"` | 1 giờ (viết thường) |
| `"1d"` | `"1D"` | 1 ngày (viết thường) |
| `"1w"` | `"1W"` | 1 tuần (viết thường) |

#### 3️⃣ Alias Ký Tự Đơn (5 định dạng)

Các alias ngắn gọn để viết nhanh hơn, tương thích với các platform khác:

| String Format | Tên | Tương Đương |
|---|---|---|
| `"m"` | phút | `"1m"` |
| `"h"` | giờ | `"1H"` |
| `"d"` | ngày | `"1D"` |
| `"w"` | tuần | `"1W"` |
| `"M"` | tháng | `"1M"` |

#### 4️⃣ Tên Đầy Đủ Tiếng Anh (5 định dạng)

Các tên gọi đầy đủ để dễ đọc và tránh nhầm lẫn:

| String Format | Tương Đương | Mô Tả |
|---|---|---|
| `"minute"` | `"1m"` | 1 phút |
| `"hour"` | `"1H"` | 1 giờ |
| `"day"` | `"1D"` | 1 ngày |
| `"week"` | `"1W"` | 1 tuần |
| `"month"` | `"1M"` | 1 tháng |

### Cách Sử Dụng TimeFrame

#### 1️⃣ Dùng TimeFrame Enum (Recommended)
```python
from vnstock import Quote
from vnstock.core.types import TimeFrame

quote = Quote(source="vci", symbol="VCI")

# ✅ Cách này được khuyến nghị (có type hint & autocompletion)
df = quote.history(
    start="2024-01-01",
    end="2024-12-31",
    resolution=TimeFrame.DAILY
)
```

#### 2️⃣ Dùng String Format (Ngắn Gọn)
```python
# ✅ Cách này ngắn gọn, hỗ trợ tất cả 21 định dạng

# Định dạng tiêu chuẩn (9): "1m", "5m", "15m", "30m", "1H", "4h", "1D", "1W", "1M"
df = quote.history(start="2024-01-01", end="2024-12-31", resolution="1D")

# Viết thường (3): "1h", "1d", "1w" - tương thích với các platform khác
df = quote.history(start="2024-01-01", end="2024-12-31", resolution="1d")

# Alias ký tự đơn (5): "m", "h", "d", "w", "M" - viết nhanh
df = quote.history(start="2024-01-01", end="2024-12-31", resolution="d")

# Tên đầy đủ (5): "minute", "hour", "day", "week", "month" - dễ đọc
df = quote.history(start="2024-01-01", end="2024-12-31", resolution="day")
```

#### 3️⃣ Dùng Alias Names (TimeFrame Enum)
```python
# ✅ Dùng tên gọi thân thuộc
df_daily = quote.history(start="2024-01-01", end="2024-12-31", resolution=TimeFrame.DAILY)
df_weekly = quote.history(start="2023-01-01", end="2024-12-31", resolution=TimeFrame.WEEKLY)
df_monthly = quote.history(start="2020-01-01", end="2024-12-31", resolution=TimeFrame.MONTHLY)
```

### Khác Biệt Giữa TimeFrame

```python
from vnstock import Quote
from vnstock.core.types import TimeFrame

quote = Quote(source="vci", symbol="VCI")

# 1 Phút - Giá cập nhật mỗi 1 phút
df_1m = quote.history(
    start="2024-12-02",
    end="2024-12-03",
    resolution="1m"  # hoặc "m" (alias)
)
print(f"1-minute data: {len(df_1m)} rows")  # ~1440 rows (24*60)

# 5 Phút - Giá cập nhật mỗi 5 phút
df_5m = quote.history(
    start="2024-12-02",
    end="2024-12-03",
    resolution="5m"  # hoặc "minute" (full name)
)
print(f"5-minute data: {len(df_5m)} rows")  # ~288 rows (24*12)

# 1 Giờ - Giá cập nhật mỗi 1 giờ
df_1h = quote.history(
    start="2024-12-02",
    end="2024-12-03",
    resolution="1H"  # hoặc "1h", "h" (alias), "hour" (full name)
)
print(f"1-hour data: {len(df_1h)} rows")  # ~24 rows

# 4 Giờ - Giá cập nhật mỗi 4 giờ
df_4h = quote.history(
    start="2024-12-02",
    end="2024-12-31",
    resolution="4h"
)
print(f"4-hour data: {len(df_4h)} rows")  # ~180 rows (30 days)

# 1 Ngày - Giá hàng ngày
df_daily = quote.history(
    start="2024-01-01",
    end="2024-12-31",
    resolution="1D"  # hoặc "1d", "d" (alias), "day" (full name)
)
print(f"Daily data: {len(df_daily)} rows")  # ~250 rows (trading days)

# 1 Tuần - Giá hàng tuần
df_weekly = quote.history(
    start="2023-01-01",
    end="2024-12-31",
    resolution="1W"  # hoặc "1w", "w" (alias), "week" (full name)
)
print(f"Weekly data: {len(df_weekly)} rows")  # ~100 rows

# 1 Tháng - Giá hàng tháng
df_monthly = quote.history(
    start="2020-01-01",
    end="2024-12-31",
    resolution="1M"  # hoặc "M" (alias), "month" (full name)
)
print(f"Monthly data: {len(df_monthly)} rows")  # ~60 rows
```

### Provider Support

Không phải tất cả providers đều hỗ trợ tất cả timeframes:

| TimeFrame | VCI | TCBS | MSN |
|---|:---:|:---:|:---:|
| 1m, 5m, 15m, 30m | ✅ | ❌ | ❌ |
| 1H, 4h | ✅ | ❌ | ❌ |
| 1D (Daily) | ✅ | ✅ | ✅ |
| 1W (Weekly) | ✅ | ✅ | ❌ |
| 1M (Monthly) | ✅ | ✅ | ❌ |

**Note**: VCI được khuyến nghị vì hỗ trợ đầy đủ nhất.



## 📈 Phương Thức Chính

### 1. history() - Giá Lịch Sử

Lấy dữ liệu giá lịch sử theo khoảng thời gian.

**Parameters:**

```
- start (str): Ngày bắt đầu (YYYY-MM-DD)
- end (str): Ngày kết thúc (YYYY-MM-DD)
- resolution (str|TimeFrame): Khung thời gian (hỗ trợ 21 định dạng)
  
  Định dạng tiêu chuẩn (9): "1m", "5m", "15m", "30m", "1H", "4h", "1D", "1W", "1M"
  Viết thường (3): "1h", "1d", "1w" - tương thích với platform khác
  Alias ký tự đơn (5): "m", "h", "d", "w", "M" - viết nhanh
  Tên đầy đủ (5): "minute", "hour", "day", "week", "month" - dễ đọc
  
  TimeFrame enum: TimeFrame.MINUTE_1, TimeFrame.MINUTE_5, TimeFrame.MINUTE_15,
                  TimeFrame.MINUTE_30, TimeFrame.HOUR_1, TimeFrame.HOUR_4,
                  TimeFrame.DAY_1, TimeFrame.WEEK_1, TimeFrame.MONTH_1
  
  Alias enum: TimeFrame.DAILY, TimeFrame.WEEKLY, TimeFrame.MONTHLY
  
  Default: "1D" (hàng ngày)
  
Provider support:
  ├─ VCI: ✅ Tất cả 21 định dạng
  ├─ TCBS: ✅ (1D, 1W, 1M)
  └─ MSN: ✅ (1D chủ yếu)
```

**Return:**

```
pd.DataFrame with columns:
  - time: datetime
  - open: float (giá mở)
  - high: float (giá cao)
  - low: float (giá thấp)
  - close: float (giá đóng)
  - volume: int (khối lượng)
  - value: float (optional, giá trị giao dịch)
```

**Ví dụ:**

```python
import pandas as pd
from vnstock import Quote
from vnstock.core.types import TimeFrame

quote = Quote(source="vci", symbol="VCI")

# 1. Giá hàng ngày - Dùng TimeFrame enum
df = quote.history(
    start="2024-01-01",
    end="2024-12-31",
    resolution=TimeFrame.DAILY  # Hoặc "1D"
)
print(df.head())
# Output:
#                 time   open   high    low  close    volume
# 0  2024-01-01 00:00  21.00  21.50  20.80  21.40   1234567
# 1  2024-01-02 00:00  21.40  21.80  21.10  21.50   2345678

# 1b. Giá hàng ngày - Dùng string format MT5
df = quote.history(
    start="2024-01-01",
    end="2024-12-31",
    resolution="1D"  # hoặc "1d" (case-insensitive)
)

# 2. Giá 5 phút trong 1 ngày
df = quote.history(
    start="2024-12-02",
    end="2024-12-02",
    resolution="5m"  # hoặc TimeFrame.MINUTE_5
)
print(f"5-minute bars: {len(df)}")

# 3. Giá hàng tuần trong năm ngoái
df = quote.history(
    start="2023-01-01",
    end="2024-12-31",
    resolution="1W"  # hoặc TimeFrame.WEEKLY
)
print(f"Weekly bars: {len(df)}")

# 4. Giá từ đầu năm đến nay
import datetime
today = datetime.date.today().isoformat()
df = quote.history(
    start="2024-01-01",
    end=today,
    resolution="1D"
)
print(f"YTD bars: {len(df)}")

# 5. Giá 1 giờ - Trading intraday
df = quote.history(
    start="2024-12-02",
    end="2024-12-03",
    resolution="1H"  # hoặc "1h"
)
print(f"Hourly bars: {len(df)}")

# 6. Giá hàng tháng - Long-term analysis
df = quote.history(
    start="2020-01-01",
    end="2024-12-31",
    resolution=TimeFrame.MONTHLY
)
print(f"Monthly bars: {len(df)}")
```

### 2. intraday() - Dữ Liệu Trong Ngày

Lấy dữ liệu giao dịch trong ngày (real-time hoặc gần real-time).

**Parameters:**

```
- page_size (int): Số bản ghi để lấy (default: 100)
- page (int): Số trang (default: 1)
```

**Ví dụ:**

```python
# Lấy 100 bản ghi trong ngày
df = quote.intraday(page_size=100)
print(df.head())
# Output:
#                   time   open   high    low  close  volume
# 0  2024-12-03 15:30  21.45  21.55  21.40  21.50  50000
# 1  2024-12-03 15:29  21.40  21.50  21.35  21.45  45000
# 2  2024-12-03 15:28  21.35  21.45  21.30  21.40  55000

# Lấy nhiều hơn
df = quote.intraday(page_size=500, page=1)
print(f"Total intraday records: {len(df)}")

# Lấy các trang khác
page1 = quote.intraday(page_size=100, page=1)
page2 = quote.intraday(page_size=100, page=2)
```

### 3. price_depth() - Độ Sâu Giá (Order Book)

Lấy thông tin độ sâu giá (Bid/Ask levels).

**Ví dụ:**

```python
# Lấy order book
depth = quote.price_depth()
print(depth)
# Output:
# {
#     'bid': [
#         {'price': 21.40, 'volume': 50000, 'count': 10},
#         {'price': 21.39, 'volume': 45000, 'count': 8},
#         ...
#     ],
#     'ask': [
#         {'price': 21.41, 'volume': 60000, 'count': 12},
#         {'price': 21.42, 'volume': 55000, 'count': 9},
#         ...
#     ],
#     'last_price': 21.40,
#     'timestamp': '2024-12-03 15:30:00'
# }

# Phân tích order book
best_bid = depth['bid'][0]
best_ask = depth['ask'][0]
spread = best_ask['price'] - best_bid['price']

print(f"Best Bid: {best_bid['price']} x {best_bid['volume']}")
print(f"Best Ask: {best_ask['price']} x {best_ask['volume']}")
print(f"Spread: {spread}")
```

### 4. price_board() - Bảng Giá Realtime

Lấy bảng giá realtime cho một hoặc nhiều chứng khoán.

**Ví dụ:**

```python
# Bảng giá cho một chứng khoán
board = quote.price_board()
print(board)
# Output:
# {
#     'symbol': 'VCI',
#     'price': 21.40,
#     'bid': 21.40,
#     'ask': 21.41,
#     'bid_volume': 50000,
#     'ask_volume': 60000,
#     'volume': 1000000,
#     'value': 21400000,
#     'change': 0.40,
#     'change_percent': 1.90,
#     'open': 21.00,
#     'high': 21.90,
#     'low': 20.80,
#     'timestamp': '2024-12-03 15:30:00'
# }

# Hoặc trả về DataFrame nếu multiple symbols
symbols = ['VCI', 'ACB', 'BID']
board = quote.price_board(symbols=symbols)
print(board)
```

## 🔍 Phân Tích & Xử Lý Dữ Liệu

### Ví dụ 1: Tính Toán Chỉ Số Cơ Bản

```python
from vnstock import Quote
from vnstock.core.types import TimeFrame
import pandas as pd

quote = Quote(source="vci", symbol="VCI")

# Lấy dữ liệu
df = quote.history(
    start="2024-01-01",
    end="2024-12-31",
    resolution=TimeFrame.DAILY
)

# 1. Tính Returns (Lợi suất)
df['daily_return'] = df['close'].pct_change()
df['cumulative_return'] = (1 + df['daily_return']).cumprod() - 1

print("Daily Returns:")
print(df[['close', 'daily_return', 'cumulative_return']].head(10))

# 2. Tính Volatility (Biến động)
volatility = df['daily_return'].std()
annualized_vol = volatility * (252 ** 0.5)
print(f"\nDaily Volatility: {volatility:.4f}")
print(f"Annualized Volatility: {annualized_vol:.4f}")

# 3. Min/Max Price
print(f"\nMin Price: {df['low'].min()}")
print(f"Max Price: {df['high'].max()}")

# 4. Average Volume
avg_volume = df['volume'].mean()
print(f"Average Volume: {avg_volume:,.0f}")
```

### Ví dụ 2: Moving Averages

```python
import pandas as pd
from vnstock import Quote
from vnstock.core.types import TimeFrame

quote = Quote(source="vci", symbol="VCI")
df = quote.history(
    start="2024-01-01",
    end="2024-12-31",
    resolution=TimeFrame.DAILY
)

# 1. Simple Moving Average (SMA)
df['SMA_20'] = df['close'].rolling(window=20).mean()  # 20-day SMA
df['SMA_50'] = df['close'].rolling(window=50).mean()  # 50-day SMA
df['SMA_200'] = df['close'].rolling(window=200).mean()  # 200-day SMA

print(df[['close', 'SMA_20', 'SMA_50', 'SMA_200']].tail(10))

# 2. Exponential Moving Average (EMA)
df['EMA_12'] = df['close'].ewm(span=12).mean()
df['EMA_26'] = df['close'].ewm(span=26).mean()

print(df[['close', 'EMA_12', 'EMA_26']].tail(10))

# 3. MACD (Moving Average Convergence Divergence)
df['MACD'] = df['EMA_12'] - df['EMA_26']
df['Signal'] = df['MACD'].ewm(span=9).mean()
df['Histogram'] = df['MACD'] - df['Signal']

print(df[['MACD', 'Signal', 'Histogram']].tail(10))
```

### Ví dụ 3: Support & Resistance Levels

```python
from vnstock import Quote
from vnstock.core.types import TimeFrame
import pandas as pd

quote = Quote(source="vci", symbol="VCI")
df = quote.history(
    start="2024-01-01",
    end="2024-12-31",
    resolution=TimeFrame.DAILY
)

# 1. Tính Pivots
HIGH = df['high'].max()
LOW = df['low'].min()
CLOSE = df['close'].iloc[-1]

PIVOT = (HIGH + LOW + CLOSE) / 3
R1 = (2 * PIVOT) - LOW
R2 = PIVOT + (HIGH - LOW)
S1 = (2 * PIVOT) - HIGH
S2 = PIVOT - (HIGH - LOW)

print(f"Resistance 2: {R2:.2f}")
print(f"Resistance 1: {R1:.2f}")
print(f"Pivot: {PIVOT:.2f}")
print(f"Support 1: {S1:.2f}")
print(f"Support 2: {S2:.2f}")

# 2. Rolling High/Low (52-week range)
df['52W_High'] = df['high'].rolling(window=252).max()  # 252 trading days ≈ 1 year
df['52W_Low'] = df['low'].rolling(window=252).min()

print(f"\n52-Week High: {df['52W_High'].iloc[-1]:.2f}")
print(f"52-Week Low: {df['52W_Low'].iloc[-1]:.2f}")
```

### Ví dụ 4: Tìm Breakout/Breakdown

```python
from vnstock import Quote
from vnstock.core.types import TimeFrame
import pandas as pd

quote = Quote(source="vci", symbol="VCI")
df = quote.history(
    start="2024-01-01",
    end="2024-12-31",
    resolution=TimeFrame.DAILY
)

# 1. Breakout (vượt qua Resistance)
resistance_20d = df['high'].rolling(window=20).max()
df['Breakout'] = df['close'] > resistance_20d.shift(1)

breakouts = df[df['Breakout']]
print(f"Breakouts found: {len(breakouts)}")
print(breakouts[['close', 'high']].head())

# 2. Breakdown (thủng Support)
support_20d = df['low'].rolling(window=20).min()
df['Breakdown'] = df['close'] < support_20d.shift(1)

breakdowns = df[df['Breakdown']]
print(f"\nBreakdowns found: {len(breakdowns)}")
print(breakdowns[['close', 'low']].head())
```

### Ví dụ 5: Phân Tích Xu Hướng (Trend Analysis)

```python
from vnstock import Quote
from vnstock.core.types import TimeFrame
import pandas as pd
import numpy as np

quote = Quote(source="vci", symbol="VCI")
df = quote.history(
    start="2024-01-01",
    end="2024-12-31",
    resolution=TimeFrame.DAILY
)

# 1. Uptrend/Downtrend
df['HH'] = df['high'].rolling(window=20).apply(lambda x: x.argmax() == len(x) - 1)  # Higher High
df['LL'] = df['low'].rolling(window=20).apply(lambda x: x.argmin() == len(x) - 1)   # Lower Low

# 2. RSI (Relative Strength Index)
def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    seed = deltas[:period+1]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100. / (1. + rs)
    
    for i in range(period, len(prices)):
        delta = deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
        
        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)
    
    return rsi

df['RSI'] = calculate_rsi(df['close'].values)

# RSI > 70: Overbought, RSI < 30: Oversold
overbought = df[df['RSI'] > 70]
oversold = df[df['RSI'] < 30]

print(f"Overbought days: {len(overbought)}")
print(f"Oversold days: {len(oversold)}")
print(df[['close', 'RSI']].tail(10))
```

## 💾 Lưu & Load Dữ Liệu

### Ví dụ 1: Export CSV

```python
from vnstock import Quote
from vnstock.core.types import TimeFrame

quote = Quote(source="vci", symbol="VCI")
df = quote.history(
    start="2024-01-01",
    end="2024-12-31",
    resolution=TimeFrame.DAILY
)

# Export CSV
df.to_csv('vci_daily.csv', index=False)
print("✅ Exported to vci_daily.csv")

# Load lại
import pandas as pd
df_loaded = pd.read_csv('vci_daily.csv')
print(df_loaded.head())
```

### Ví dụ 2: Export Excel

```python
# Export Excel
df.to_excel('vci_daily.xlsx', index=False)
print("✅ Exported to vci_daily.xlsx")

# Với multiple sheets
with pd.ExcelWriter('vci_analysis.xlsx') as writer:
    df.to_excel(writer, sheet_name='OHLCV', index=False)
    df[['close', 'SMA_20', 'SMA_50']].to_excel(writer, sheet_name='MAs', index=False)
```

### Ví dụ 3: Caching

```python
import pickle
import os
from vnstock import Quote
from vnstock.core.types import TimeFrame

quote = Quote(source="vci", symbol="VCI")
CACHE_FILE = f'cache/vci_2024.pkl'

# Load hoặc fetch
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'rb') as f:
        df = pickle.load(f)
    print("✅ Loaded from cache")
else:
    df = quote.history(
        start="2024-01-01",
        end="2024-12-31",
        resolution=TimeFrame.DAILY
    )
    os.makedirs('cache', exist_ok=True)
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(df, f)
    print("✅ Cached for next time")

print(df.head())
```

## ❌ Các Lỗi Thường Gặp

### Lỗi 1: Invalid Date Format

```python
# ❌ Sai
df = quote.history(start="01/01/2024", end="31/12/2024")

# ✅ Đúng
df = quote.history(start="2024-01-01", end="2024-12-31")
```

### Lỗi 2: Start Date > End Date

```python
# ❌ Sai
df = quote.history(start="2024-12-31", end="2024-01-01")

# ✅ Đúng
df = quote.history(start="2024-01-01", end="2024-12-31")
```

### Lỗi 3: Invalid TimeFrame

```python
# ❌ Sai
df = quote.history(resolution="2D")  # 2D không hỗ trợ

# ✅ Đúng
df = quote.history(resolution="1D")  # hoặc "1W", "1M"
```

### Lỗi 4: Empty DataFrame

```python
# ❌ Kiểm tra không đúng
if df.empty:
    print("No data!")

# ✅ Kiểm tra đúng
if df is None or len(df) == 0:
    print("No data!")

# ✅ Hoặc
if df.shape[0] == 0:
    print("No data!")
```

## 📚 Bước Tiếp Theo

1. [02-Installation](02-installation.md) - Cài đặt
2. [01-Overview](01-overview.md) - Tổng quan
3. [03-Listing API](03-listing-api.md) - Danh sách chứng khoán
4. ✅ **04-Quote & Price** - Bạn đã ở đây
5. [05-Financial API](05-financial-api.md) - Dữ liệu tài chính
6. [06-Connector Guide](06-connector-guide.md) - API bên ngoài
7. [07-Best Practices](07-best-practices.md) - Mẹo & kinh nghiệm

---

**Last Updated**: 2024-12-03  
**Version**: 3.3.0  
**Status**: Actively Maintained
