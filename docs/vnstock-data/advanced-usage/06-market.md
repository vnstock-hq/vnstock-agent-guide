# Market - Định Giá Thị Trường (P/E, P/B)

> ⚠️ **Lưu ý Deprecation**: Các phương thức `pe()`, `pb()`, và `evaluation()` trong lớp `Market` đã bị đánh dấu là **deprecated** và sẽ bị loại bỏ vào ngày **31/08/2026**. Vui lòng chuyển sang sử dụng lớp `Analytics().valuation()` (xem hướng dẫn chi tiết bên dưới).

Lớp `Market` cung cấp dữ liệu định giá thị trường theo thời gian.

## Khởi Tạo

```python
from vnstock_data import Market

# Khởi tạo cơ bản với VNINDEX
market = Market()

# Khởi tạo với HNX
market_hnx = Market(index="HNX")

# Khởi tạo với random user agent
market = Market(random_agent=True)
```

### Tham Số Khởi Tạo

- `index` (str, default="VNINDEX"): Chỉ số thị trường
  - `"VNINDEX"`: Chỉ số chính (HSX)
  - `"HNX"` hoặc `"HNXINDEX"`: Chỉ số phụ (HNX)
- `random_agent` (bool, default=False): Sử dụng random user agent để tránh bị block

**Lưu ý**: Chỉ **VND** hỗ trợ Market.

## Phương Thức

### pe() - P/E Ratio Theo Thời Gian (Deprecated)

```python
# Lấy P/E 5 năm (mặc định)
df = market.pe()

# Lấy P/E 1 năm
df = market.pe(duration="1Y")

# Lấy P/E 10 năm
df = market.pe(duration="10Y")
```

**Tham Số**:
- `duration` (str, default="5Y"): Khoảng thời gian lịch sử
  - `"1Y", "2Y", "3Y", "5Y", "10Y"`, v.v. Dữ liệu hiện tại có đến năm 2017.

**Trả về**: DataFrame với 1 cột (shape: N, 1)
- `pe`: float64 - P/E ratio của thị trường (VNINDEX)
- Index: `reportDate` (datetime)

**Ví dụ** (5 ngày gần nhất):
```
            pe
reportDate              
2025-11-25  14.492048
2025-11-26  14.649851
2025-11-27  14.676644
2025-11-28  14.716241
2025-12-01  15.157115
```

### pb() - P/B Ratio Theo Thời Gian (Deprecated)

```python
# Lấy P/B 5 năm (mặc định)
df = market.pb()

# Lấy P/B 1 năm
df = market.pb(duration="1Y")

# Lấy P/B 10 năm
df = market.pb(duration="10Y")
```

**Tham Số**:
- `duration` (str, default="5Y"): Khoảng thời gian lịch sử
  - `"1Y", "2Y", "3Y", "5Y", "10Y", "15Y"`, v.v.

**Trả về**: DataFrame với 1 cột (shape: N, 1)
- `pb`: float64 - P/B ratio của thị trường (VNINDEX)
- Index: `reportDate` (datetime)

**Ví dụ** (5 ngày gần nhất):
```
            pb
reportDate      
2025-11-25  2.014220
2025-11-26  2.038516
2025-11-27  2.043279
2025-11-28  2.051375
2025-12-01  2.064346
```

### evaluation() - Lịch Sử Định Giá (Deprecated)

```python
# Lấy cả P/E và P/B 5 năm (mặc định)
df = market.evaluation()

# Lấy cả P/E và P/B 3 năm
df = market.evaluation(duration="3Y")

# Lấy cả P/E và P/B 10 năm
df = market.evaluation(duration="10Y")
```

**Tham Số**:
- `duration` (str, default="5Y"): Khoảng thời gian lịch sử
  - `"1Y", "2Y", "3Y", "5Y", "10Y", "15Y"`, v.v.

**Trả về**: DataFrame với 2 cột (shape: N, 2)
- `pe`: float64 - P/E ratio của thị trường
- `pb`: float64 - P/B ratio của thị trường
- Index: `reportDate` (datetime)

**Ví dụ** (5 ngày gần nhất):
```
                   pe        pb
reportDate                     
2025-11-25  14.492048  2.014220
2025-11-26  14.649851  2.038516
2025-11-27  14.676644  2.043279
2025-11-28  14.716241  2.051375
2025-12-01  15.157115  2.064346
```

## Ví Dụ

```python
from vnstock_data import Market
import matplotlib.pyplot as plt

market = Market()

# Lấy P/E 10 năm
pe_data = market.pe(duration="10Y")
print(f"P/E hiện tại: {pe_data['pe'].iloc[-1]:.2f}")
print(f"P/E trung bình: {pe_data['pe'].mean():.2f}")

# Lấy P/B 10 năm
pb_data = market.pb(duration="10Y")
print(f"\nP/B hiện tại: {pb_data['pb'].iloc[-1]:.2f}")

# Vẽ biểu đồ
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(pe_data.index, pe_data['pe'], label='P/E')
plt.title('P/E Thị Trường')
plt.xlabel('Thời gian')
plt.ylabel('P/E Ratio')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(pb_data.index, pb_data['pb'], label='P/B', color='orange')
plt.title('P/B Thị Trường')
plt.xlabel('Thời gian')
plt.ylabel('P/B Ratio')
plt.legend()
plt.tight_layout()
plt.show()
```

## Phân Tích Ví Dụ

```python
from vnstock_data import Market
import pandas as pd

market = Market()
pe_data = market.pe(duration="10Y")

# Tính percentile
pe_data['percentile'] = pe_data['pe'].rank(pct=True) * 100

# Kiểm tra đắt hay rẻ
current_pe = pe_data['pe'].iloc[-1]
avg_pe = pe_data['pe'].mean()

if current_pe < avg_pe * 0.8:
    print("📈 Thị trường đang rẻ (Undervalued)")
elif current_pe > avg_pe * 1.2:
    print("📉 Thị trường đang đắt (Overvalued)")
else:
    print("➡️ Thị trường ở mức trung bình")

print(f"\nP/E hiện tại: {current_pe:.2f}")
print(f"P/E trung bình: {avg_pe:.2f}")
print(f"P/E thấp nhất: {pe_data['pe'].min():.2f}")
print(f"P/E cao nhất: {pe_data['pe'].max():.2f}")
```

## Use Case

- **Định giá thị trường**: So sánh với giá trị lịch sử để quyết định vào/ra
- **Phân tích macro**: Kết hợp với kinh tế vĩ mô để dự báo
- **Quản lý danh mục**: Điều chỉnh allocation dựa trên P/E, P/B
- **So sánh sàn**: Phân tích sự khác biệt định giá giữa VNINDEX và HNX

## Ví Dụ Advanced - So Sánh VNINDEX và HNX

```python
from vnstock_data import Market
import numpy as np

# So sánh giữa VNINDEX và HNX
market_vnindex = Market(index="VNINDEX")
market_hnx = Market(index="HNX")

pe_vnindex = market_vnindex.pe(duration="5Y")
pe_hnx = market_hnx.pe(duration="5Y")

print("P/E trung bình 5 năm:")
print(f"VNINDEX: {pe_vnindex['pe'].mean():.2f}")
print(f"HNX: {pe_hnx['pe'].mean():.2f}")

# Phân tích độ biến động
pe_volatility = pe_vnindex['pe'].std()
print(f"\nĐộ biến động P/E: {pe_volatility:.2f}")

# Tìm thời kỳ thị trường rẻ nhất
min_pe_date = pe_vnindex['pe'].idxmin()
min_pe = pe_vnindex['pe'].min()
print(f"\nThị trường rẻ nhất: {min_pe_date.date()} (P/E = {min_pe:.2f})")

# Tìm thời kỳ thị trường đắt nhất
max_pe_date = pe_vnindex['pe'].idxmax()
max_pe = pe_vnindex['pe'].max()
print(f"Thị trường đắt nhất: {max_pe_date.date()} (P/E = {max_pe:.2f})")
```

## Dữ Liệu Crypto

Ngoài dữ liệu chứng khoán, lớp `Market` cũng cung cấp phương thức truy cập dữ liệu thị trường tiền mã hóa (Crypto). Dữ liệu này hỗ trợ lấy thông tin lịch sử giá (OHLCV), sổ lệnh (order book) và lịch sử giao dịch thời gian thực.

### Khởi Tạo

Sử dụng phương thức `crypto()` của `Market` với mã giao dịch tương ứng:

```python
from vnstock_data import Market

mkt = Market()
crypto = mkt.crypto("BTCUSDT")  # Nhập mã giao dịch, ví dụ: BTCUSDT, ETHUSDT
```

### Các Phương Thức Chính

Các phương thức được thiết kế chuẩn hoá và trả về `pandas.DataFrame`.

#### `ohlcv()` - Lịch Sử Giá (Bars)

```python
# Lấy dữ liệu nến theo khung thời gian
df = crypto.ohlcv(interval="1d", limit=500)
```

**Tham Số**:
- `interval` (str): Khung thời gian (`"1s"`, `"1m"` đến `"30m"`, `"1h"` đến `"12h"`, `"1d"`, `"3d"`, `"1w"`, `"1M"`). Default: `"1d"`
- `limit` (int): Số nến hiển thị. Default: `500`
- `start_time`, `end_time` (int, tuỳ chọn): Bộ lọc Unix timestamp (mili-giây).

**Trả về**: DataFrame `[time, open, high, low, close, volume]`

#### `trades()` - Lịch Sử Khớp Lệnh (Time & Sales)

```python
# Lịch sử khớp lệnh chi tiết (raw)
df_raw = crypto.trades(limit=500, mode="raw")

# Lịch sử khớp lệnh tổng hợp các lệnh cùng loại (aggregate)
df_agg = crypto.trades(limit=500, mode="aggregate")
```

**Tham Số**:
- `limit` (int): Số lượng lệnh hiển thị. Default: `500`
- `mode` (str): Chế độ `"raw"` hoặc `"aggregate"`. Default: `"raw"`
- `start_time`, `end_time` (int, tuỳ chọn): Dùng cho mode `aggregate` (mili-giây).

**Trả về**: DataFrame `[time, price, volume, side, match_type, id]`

#### `order_book()` - Sổ Lệnh (Market Depth)

```python
# Xem các mức giá đặt mua/bán (Bid/Ask) tốt nhất
df = crypto.order_book(limit=10)
```

**Tham Số**:
- `limit` (int): Số cấp giá (1, 5, 10, 20, 50, 100...). Default: `10`

**Trả về**: DataFrame `[bid_price, bid_vol, ask_price, ask_vol, ...]`

#### Dữ Liệu Tức Thời (Real-time Snapshots)

```python
# Xem thống kê trong 24 giờ qua (Giá mở, đỉnh, đáy, khối lượng)
df_quote = crypto.quote()

# Xem giá tham chiếu và tính toán
df_ref = crypto.reference_price()

# Xem giá khớp lệnh tại thời điểm hiện tại (nhẹ, tải nhanh)
df_last = crypto.last_price()
```
