# Quote - Dữ Liệu Giá Lịch Sử, OHLCV, Intraday

## Giới Thiệu

Lớp `Quote` cung cấp dữ liệu giá cổ phiếu theo thời gian:

- **History**: Giá lịch sử OHLCV (Open, High, Low, Close, Volume) đã điều chỉnh theo ngày, tuần, tháng hoặc phút
- **Intraday**: Khớp lệnh chi tiết theo từng phút trong ngày
- **Price Depth**: Bước giá và khối lượng (dư mua, dư bán) tại các mức giá

### Ứng Dụng Phổ Biến

- **Phân tích kỹ thuật - Technical Analysis**: Vẽ biểu đồ kỹ thuật, tính indicator
- **Kiểm thử - Backtesting**: Kiểm tra chiến lược trên dữ liệu lịch sử
- **Theo dõi thời gian thực - Realtime Monitoring**: Theo dõi giá intraday
- **Phân tích thống kê - Statistical Analysis**: Tính volatility, correlation, etc.

## Khởi Tạo Đối tượng

```python
from vnstock_data import Quote

# Cách 1: Qua Adapter (cú pháp dễ nhớ)
quote = Quote(source="vci", symbol="VCB")

# Cách 2: Qua Adapter với VND (cú pháp dễ nhớ)
quote_vnd = Quote(source="vnd", symbol="VCB")

# Cách 3: Import trực tiếp từ nguồn (cố định, phải hiểu cấu trúc thư **viện**)
from vnstock_data.explorer.vci import Quote
quote = Quote(symbol="VCB")
```

### Tham Số Khởi Tạo

- `source` (str): Nguồn dữ liệu (`"vci"`, `"vnd"`, `"mas"`)
- `symbol` (str): Mã chứng khoán (ví dụ: `"VCB"`, `"VN30"`, `"VNINDEX"`). Mã có thể viết hoa hoặc thường.

### Các Mã Hỗ Trợ

**Cổ Phiếu**: Tất cả mã niêm yết tại HOSE, HNX, UPCOM (VD: `VCB`, `MSN`, `REE`)

**Chỉ Số**:
- `VNINDEX` - VN Index
- `HNXINDEX` - HNX Index
- `UPCOMINDEX` - Upcom Index
- `VN30`, `VN100`, `HNX30`, `VNSML`, `VNMID`, `VNALL`

**Chỉ Số Ngành**:
- `VNREAL` - Bất động sản
- `VNMAT` - Nguyên vật liệu
- `VNIT` - Công nghệ
- `VNHEAL` - Chăm sóc sức khỏe
- `VNFINSELECT`, `VNFIN` - Tài chính
- `VNENE` - Năng lượng
- `VNCONS`, `VNCOND` - Hàng tiêu dùng

## Phương Thức: history()

Lấy dữ liệu giá lịch sử OHLCV.

**Cú Pháp**
```python
df = quote.history(
    start="2024-01-01", 
    end="2024-12-31", 
    interval="1D"
)
```

**Tham Số**

| Tham Số | Kiểu | Mặc Định | Mô Tả |
|---|---|---|---|
| `start` | str | - | Ngày bắt đầu, định dạng `YYYY-MM-DD` |
| `end` | str | - | Ngày kết thúc, định dạng `YYYY-MM-DD` |
| `interval` | str | `"1D"` | Khung thời gian: `1m`, `5m`, `15m`, `30m`, `1H`, `1W`, `1M` |

**Interval Giới Hạn**

- Khung phút (`1m`...`30m`): Max 2 năm
- Khung ngày trở lên (`1D`...`1M`): dữ liệu đầy đủ kể từ 27/8/2000 với các mã REE, SAM

**Kiểu Dữ Liệu Trả Về**

```
DataFrame với các cột:
- time: Thời gian (datetime64)
- open: Giá mở cửa (float)
- high: Giá cao nhất (float)
- low: Giá thấp nhất (float)
- close: Giá đóng cửa (float)
- volume: Khối lượng (int)
```

**Ví Dụ**

```python
from vnstock_data import Quote
import pandas as pd

quote = Quote(source="vci", symbol="VCB")

# Lấy dữ liệu 1 năm theo ngày
df = quote.history(start="2024-01-01", end="2024-12-31", interval="1D")
print(f"Lấy được {len(df)} dòng dữ liệu")
print(df.head())
#            time   open   high    low  close     volume
# 0  2024-01-02  70.5  71.2  70.3  70.8  1200000
# 1  2024-01-03  71.0  72.1  71.0  71.5  1500000

# Lấy dữ liệu intraday (phút)
df_intra = quote.history(start="2024-12-20", end="2024-12-20", interval="15m")

# Tính moving average
df['MA20'] = df['close'].rolling(20).mean()
df['MA50'] = df['close'].rolling(50).mean()

# Lấy close price gần nhất
latest_price = df['close'].iloc[-1]
print(f"Giá đóng cửa gần nhất: {latest_price}")
```

## Phương Thức: intraday()

Lấy dữ liệu khớp lệnh chi tiết trong ngày giao dịch gần nhất.

**Cú Pháp**
```python
df = quote.intraday()
```

**Tham Số**: Không có

**Kiểu Dữ Liệu Trả Về**

```
DataFrame với các cột:
- time: Thời gian khớp lệnh (datetime)
- price: Giá khớp lệnh (float)
- accumulated_val: Giá trị lũy tích (int)
- accumulated_vol: Khối lượng lũy tích (int)
- volume: Khối lượng giao dịch lần này (int)
- match_type: Loại khớp lệnh (str) - "Sell", "Buy", "ATO", "ATC"
```

**Ví Dụ**

```python
quote = Quote(source="vci", symbol="VCB")

# Lấy dữ liệu intraday hôm nay
df_intra = quote.intraday()

print(f"Số lệnh khớp hôm nay: {len(df_intra)}")
print(df_intra.head(20))
#                  time  price  accumulated_val accumulated_vol  volume match_type
# 0 2024-12-20 09:15:00  70.5      1317470000          20300   20300        ATO

# Lọc chỉ lệnh mua/bán
buy_orders = df_intra[df_intra['match_type'] == 'Buy']
sell_orders = df_intra[df_intra['match_type'] == 'Sell']

# Tính matching price
matching_price = df_intra['price'].iloc[-1]
print(f"Giá khớp lệnh gần nhất: {matching_price}")

# Tổng khối lượng giao dịch ngày hôm nay
total_vol = df_intra['volume'].sum()
print(f"Tổng khối lượng: {total_vol}")
```

## Phương Thức: price_depth()

Lấy bước giá (mức giá, khối lượng mua/bán) tại thời điểm hiện tại.

**Cú Pháp**
```python
df = quote.price_depth()
```

**Kiểu Dữ Liệu Trả Về**

```
DataFrame với các cột:
- price: Mức giá (float)
- volume: Tổng khối lượng (float)
- buy_volume: Khối lượng mua (float)
- sell_volume: Khối lượng bán (float)
- undefined_volume: Khối lượng chưa xác định (float)
```

**Ví Dụ**

```python
quote = Quote(source="vci", symbol="VCB")

df_depth = quote.price_depth()

print(df_depth.head(10))
#     price    volume  buy_volume  sell_volume  undefined_volume
# 0  62300.0    4900.0     4900.0         0.0              0.0
# 1  62200.0   10700.0     7100.0      3600.0              0.0

# Tính dư mua - dư bán
df_depth['balance'] = df_depth['buy_volume'] - df_depth['sell_volume']

# Lấy top bid/ask
print(f"Bid cao nhất (dư mua): {df_depth.iloc[0]['price']}")
print(f"Ask thấp nhất (dư bán): {df_depth.iloc[0]['price']}")

# Tính sự chênh lệch dư mua/bán
total_buy = df_depth['buy_volume'].sum()
total_sell = df_depth['sell_volume'].sum()
balance_pct = (total_buy - total_sell) / (total_buy + total_sell)
print(f"Balance %: {balance_pct*100:.2f}%")
```

## Ma Trận Nguồn Dữ Liệu Hỗ Trợ

| Phương Thức | VCI | VND | MAS |
|---|---|---|---|
| history | ✅ | ✅ | ✅ |
| intraday | ✅ | ✅ | ✅ |
| price_depth | ✅ | ❌ | ✅ |

## Ví Dụ Thực Tế

### Ví Dụ 1: Backtest Strategy Đơn Giản

```python
from vnstock_data import Quote
import pandas as pd

quote = Quote(source="vci", symbol="VCB")
df = quote.history(start="2023-01-01", end="2024-12-31", interval="1D")
df = df.set_index('time') # Đặt time làm index, tạo time series

# Tính SMA20, SMA50
df['SMA20'] = df['close'].rolling(20).mean()
df['SMA50'] = df['close'].rolling(50).mean()

# Tín hiệu: Golden Cross
df['signal'] = 0
df.loc[df['SMA20'] > df['SMA50'], 'signal'] = 1
df.loc[df['SMA20'] <= df['SMA50'], 'signal'] = -1

# Tính return
df['returns'] = df['close'].pct_change()
df['strategy_returns'] = df['signal'].shift(1) * df['returns']

# Tính cumulative return
df['cumulative_return'] = (1 + df['strategy_returns']).cumprod()

print(f"Final return: {(df['cumulative_return'].iloc[-1] - 1) * 100:.2f}%")
```

### Ví Dụ 2: Tìm Support/Resistance

```python
from vnstock_data import Quote

quote = Quote(source="vci", symbol="VCB")
df = quote.history(start="2024-01-01", end="2024-12-31", interval="1D")
df = df.set_index('time')  # Đặt time làm index

# Năm ngoài
year_high = df['high'].max()
year_low = df['low'].min()
year_close = df['close'].iloc[-1]

print(f"Năm ngoài cao nhất: {year_high}")
print(f"Năm ngoài thấp nhất: {year_low}")
print(f"Giá đóng cửa năm ngoài: {year_close}")
print(f"Năm ngoài range: {year_high - year_low}")

# Tính % từ low -> high
pct_from_low = (year_close - year_low) / (year_high - year_low) * 100
print(f"% từ low tới close: {pct_from_low:.2f}%")
```

### Ví Dụ 3: Tính Volatility

```python
from vnstock_data import Quote
import numpy as np

quote = Quote(source="vci", symbol="VCB")
df = quote.history(start="2024-01-01", end="2024-12-31", interval="1D")
df = df.set_index('time')  # Đặt time làm index

# Tính daily return
df['returns'] = df['close'].pct_change()

# Tính volatility (annualized)
daily_vol = df['returns'].std()
annual_vol = daily_vol * np.sqrt(252)  # 252 trading days per year

print(f"Daily volatility: {daily_vol*100:.2f}%")
print(f"Annual volatility: {annual_vol*100:.2f}%")

# Tính rolling volatility
df['vol_20'] = df['returns'].rolling(20).std() * np.sqrt(252)
print(df[['close', 'vol_20']].tail(10))
```

### Ví Dụ 4: Phân Tích Intraday

```python
from vnstock_data import Quote
import pandas as pd

quote = Quote(source="vci", symbol="VCB")
df_intra = quote.intraday()

if not df_intra.empty:
    # Giá mở cửa
    opening_price = df_intra['price'].iloc[0]
    
    # Giá cao/thấp nhất trong ngày
    high = df_intra['price'].max()
    low = df_intra['price'].min()
    
    # Giá đóng cửa
    closing_price = df_intra['price'].iloc[-1]
    
    # Tổng khối lượng
    total_volume = df_intra['volume'].sum()
    
    print(f"Open: {opening_price}")
    print(f"High: {high}")
    print(f"Low: {low}")
    print(f"Close: {closing_price}")
    print(f"Volume: {total_volume}")
    print(f"Change: {(closing_price - opening_price)/opening_price*100:.2f}%")
```

## Bí quyết & Thực hành tốt

### Tip 1: Kiểm Tra Độ Đủ Dữ Liệu

```python
from vnstock_data import Quote
import pandas as pd

quote = Quote(source="vci", symbol="VCB")
df = quote.history(start="2020-01-01", end="2024-12-31", interval="1D")

# Kiểm tra số dòng
print(f"Số ngày giao dịch: {len(df)}")

# Kiểm tra missing data
print(f"Missing values: {df.isnull().sum().sum()}")

# Kiểm tra cột có đủ không
required_cols = ['open', 'high', 'low', 'close', 'volume']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    print(f"Thiếu cột: {missing_cols}")
```

### Tip 2: Đặt Datetime Index Cho Phân Tích Timeseries

```python
from vnstock_data import Quote

quote = Quote(source="vci", symbol="VCB")
df = quote.history(start="2024-01-01", end="2024-12-31", interval="1D")

# Đặt cột time làm index để tạo timeseries
df = df.set_index('time')

# Giờ có thể sử dụng các method timeseries
print(df.index)  # DatetimeIndex

# Lọc theo tháng
df_2024_12 = df.loc['2024-12']
print(f"Dữ liệu tháng 12/2024: {len(df_2024_12)} ngày")

# Resample thành weekly
df_weekly = df.resample('W').agg({
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum'
})

# Tính return hàng tuần
df_weekly['weekly_return'] = df_weekly['close'].pct_change()

print(df_weekly[['close', 'weekly_return']].tail())
```

**Lưu ý quan trọng**: Luôn đặt `time` làm index trước khi thực hiện các thao tác phân tích kỹ thuật như tính moving averages, resampling, hoặc các indicator phức tạp. Điều này giúp pandas hiểu đây là dữ liệu timeseries và thực hiện các phép toán chính xác.

### Tip 3: Cache Dữ Liệu Để Tăng Tốc

```python
from vnstock_data import Quote
import pickle

quote = Quote(source="vci", symbol="VCB")

# Lần đầu: lấy từ API
df = quote.history(start="2024-01-01", end="2024-12-31", interval="1D")
df.to_csv('vcb_2024.csv', index=False)

# Lần tiếp theo: đọc từ file
import pandas as pd
df = pd.read_csv('vcb_2024.csv')
df['time'] = pd.to_datetime(df['time'])
```

### Tip 4: So Sánh Nhiều Nguồn Dữ Liệu

```python
from vnstock_data import Quote
import pandas as pd

# Lấy từ VCI
quote_vci = Quote(source="vci", symbol="VCB")
df_vci = quote_vci.history(start="2024-12-01", end="2024-12-31", interval="1D")

# Lấy từ VND
quote_vnd = Quote(source="vnd", symbol="VCB")
df_vnd = quote_vnd.history(start="2024-12-01", end="2024-12-31", interval="1D")

# So sánh close price
comparison = pd.DataFrame({
    'VCI': df_vci.set_index('time')['close'],
    'VND': df_vnd.set_index('time')['close']
})

print(comparison.head())

# Tính hiệu giữa 2 nguồn
comparison['diff_pct'] = abs(comparison['VCI'] - comparison['VND']) / comparison['VCI'] * 100
print(f"Trung bình chênh lệch: {comparison['diff_pct'].mean():.2f}%")
```

## Sai Lầm Cần Tránh

### 1: Quên Chuyển Đổi Ngày Sang Định Dạng ISO (YYYY-MM-DD)

**Sai**:
```python
df = quote.history(start="01/01/2024", end="31/12/2024")  # Sai format!
```

**Đúng**:
```python
df = quote.history(start="2024-01-01", end="2024-12-31")  # YYYY-MM-DD
```

### 2: Kỳ Vọng Dữ Liệu Quá Dài ở Khung Thời Gian Phút

**Sai**:
```python
# Yêu cầu 5 năm dữ liệu phút
df = quote.history(start="2019-01-01", end="2024-12-31", interval="1m")
```

**Đúng**:
```python
# Max 2 năm cho interval phút
df = quote.history(start="2022-01-01", end="2024-12-31", interval="1m")
```

### 3: Không Kiểm Tra Kết Quả Trống

**Sai**:
```python
df = quote.history(start="2100-01-01", end="2100-12-31")  # Dữ liệu tương lai
df['MA20'] = df['close'].rolling(20).mean()  # Error vì empty
```

**Đúng**:
```python
df = quote.history(start="2024-01-01", end="2024-12-31")
if df.empty:
    print("Không có dữ liệu!")
else:
    df['MA20'] = df['close'].rolling(20).mean()
```
