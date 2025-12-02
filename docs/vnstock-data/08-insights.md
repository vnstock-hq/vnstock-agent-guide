# Insights / TopStock - Top Cổ Phiếu

Lớp `TopStock` cung cấp thông tin về các cổ phiếu hàng đầu theo các tiêu chí khác nhau.

## Khởi Tạo

```python
from vnstock_data import TopStock

# Khởi tạo cơ bản
insights = TopStock()

# Khởi tạo với random user agent
insights = TopStock(random_agent=True)

# Hiển thị debug logs
insights = TopStock(show_log=True)
```

### Tham Số Khởi Tạo

- `show_log` (bool, default=False): Hiển thị debug logs
- `random_agent` (bool, default=False): Sử dụng random user agent để tránh bị block

**Lưu ý**: Chỉ **VND** hỗ trợ TopStock.

## Phương Thức

### gainer() - Top Cổ Phiếu Tăng Giá

```python
# Lấy top 10 tăng giá VNINDEX (mặc định)
df = insights.gainer()

# Lấy top 5 tăng giá VNINDEX
df = insights.gainer(limit=5)

# Lấy top 10 tăng giá HNX
df = insights.gainer(index="HNX")
```

**Tham Số**:
- `index` (str, default="VNINDEX"): Chỉ số thị trường ("VNINDEX", "HNX", "VN30")
- `limit` (int, default=10): Số lượng cổ phiếu

**Trả về**: DataFrame với 15 cột (shape: limit, 15)
- Cột cơ bản: `symbol`, `index`, `last_price`, `last_updated`
- Cột giá: `price_change_1d`, `price_change_pct_1d`
- Cột khối lượng: `avg_volume_20d`, `volume_spike_20d_pct`, `total_volume_avg_20d`
- Cột giao dịch: `accumulated_value`, `deal_volume_spike_20d_pct`, `deal_volume_spike_5d_20d_pct`
- Cột 5 ngày: `deal_volume_sum_5d`, `deal_value_avg_5d`, `deal_volume_avg_5d`

**Ví dụ** (Top 3 tăng giá):
```
  symbol    index  last_price price_change_pct_1d  accumulated_value
0    ITD  VNINDEX        15.3                 6.99      3.704415e+09
1    VPS  VNINDEX        9.69                6.95      3.821120e+08
2    TLG  VNINDEX       63.40                6.91      9.460624e+10
```

### loser() - Top Cổ Phiếu Giảm Giá

```python
# Lấy top 10 giảm giá VNINDEX (mặc định)
df = insights.loser()

# Lấy top 5 giảm giá
df = insights.loser(limit=5)

# Lấy top 10 giảm giá HNX
df = insights.loser(index="HNX")
```

**Tham Số**:
- `index` (str, default="VNINDEX"): Chỉ số thị trường ("VNINDEX", "HNX", "VN30")
- `limit` (int, default=10): Số lượng cổ phiếu

**Trả về**: DataFrame với 15 cột (giống gainer())

**Ví dụ** (Top 3 giảm giá):
```
  symbol    index  last_price price_change_pct_1d  accumulated_value
0    RYG  VNINDEX       10.00                -5.00      1.234515e+09
1    CDC  VNINDEX       25.00                -4.51      7.285780e+09
2    ICT  VNINDEX       21.10                -3.71      2.442279e+11
```

### value() - Top Theo Giá Trị Giao Dịch

```python
# Lấy top 10 theo giá trị giao dịch (mặc định)
df = insights.value()

# Lấy top 5
df = insights.value(limit=5)

# Lấy top 10 của HNX
df = insights.value(index="HNX")
```

**Tham Số**:
- `index` (str, default="VNINDEX"): Chỉ số thị trường ("VNINDEX", "HNX", "VN30")
- `limit` (int, default=10): Số lượng cổ phiếu

**Trả về**: DataFrame với 15 cột (giống gainer())

**Ví dụ** (Top 3 giá trị giao dịch):
```
  symbol    index  last_price  accumulated_value
0    SSI  VNINDEX       32.20      5.011092e+11
1    VIX  VNINDEX       24.15      4.995282e+11
2    VIC  VNINDEX      270.00      4.805920e+11
```

### volume() - Top Theo Khối Lượng Đột Biến

```python
# Lấy top 10 theo khối lượng (mặc định)
df = insights.volume()

# Lấy top 5
df = insights.volume(limit=5)
```

**Tham Số**:
- `index` (str, default="VNINDEX"): Chỉ số thị trường ("VNINDEX", "HNX", "VN30")
- `limit` (int, default=10): Số lượng cổ phiếu

**Trả về**: DataFrame với 15 cột (giống gainer())

**Ví dụ** (Top 3 khối lượng đột biến):
```
  symbol    index  last_price  volume_spike_20d_pct
0    ITD  VNINDEX       15.30                  185.41
1    TLG  VNINDEX       63.40                  125.63
2    VPL  VNINDEX      103.90                  118.72
```

### deal() - Top Theo Giao Dịch Thỏa Thuận Đột Biến

```python
# Lấy top 10 theo giao dịch thỏa thuận (mặc định)
df = insights.deal()

# Lấy top 5
df = insights.deal(limit=5)
```

**Tham Số**:
- `index` (str, default="VNINDEX"): Chỉ số thị trường ("VNINDEX", "HNX", "VN30")
- `limit` (int, default=10): Số lượng cổ phiếu

**Trả về**: DataFrame với 15 cột (giống gainer())

**Ví dụ** (Top 3 giao dịch thỏa thuận):
```
  symbol    index  last_price  deal_volume_spike_20d_pct
0    BKG  VNINDEX        2.92                       22.50
1    NAB  VNINDEX       14.35                        2.69
2    CDC  VNINDEX       25.00                        6.24
```

### foreign_buy() - Top Nước Ngoài Mua Ròng

```python
# Lấy top 10 mua ròng hôm nay (mặc định)
df = insights.foreign_buy()

# Lấy top 5
df = insights.foreign_buy(limit=5)

# Lấy top 10 của ngày cụ thể
df = insights.foreign_buy(date="2025-11-30")
```

**Tham Số**:
- `date` (str, optional): Ngày giao dịch (format: "YYYY-MM-DD"). Nếu không cung cấp, sử dụng ngày hôm nay
- `limit` (int, default=10): Số lượng cổ phiếu

**Trả về**: DataFrame với 3 cột (shape: limit, 3)
- `symbol`: str - Mã cổ phiếu
- `date`: str - Ngày giao dịch (YYYY-MM-DD)
- `net_value`: float64 - Giá trị mua ròng (VND)

**Ví dụ** (Top 3 mua ròng):
```
  symbol        date     net_value
0    VJC  2025-12-02  1.326863e+11
1    VIC  2025-12-02  9.060632e+10
2    TCB  2025-12-02  6.987791e+10
```

### foreign_sell() - Top Nước Ngoài Bán Ròng

```python
# Lấy top 10 bán ròng hôm nay (mặc định)
df = insights.foreign_sell()

# Lấy top 5
df = insights.foreign_sell(limit=5)

# Lấy top 10 của ngày cụ thể
df = insights.foreign_sell(date="2025-11-30")
```

**Tham Số**:
- `date` (str, optional): Ngày giao dịch (format: "YYYY-MM-DD"). Nếu không cung cấp, sử dụng ngày hôm nay
- `limit` (int, default=10): Số lượng cổ phiếu

**Trả về**: DataFrame với 3 cột (shape: limit, 3)
- `symbol`: str - Mã cổ phiếu
- `date`: str - Ngày giao dịch (YYYY-MM-DD)
- `net_value`: float64 - Giá trị bán ròng (VND - âm)

**Ví dụ** (Top 3 bán ròng):
```
  symbol        date     net_value
0    VPI  2025-12-02 -5.005783e+10
1    VIX  2025-12-02 -4.019161e+10
2    VRE  2025-12-02 -4.015856e+10
```

## Ví Dụ

```python
from vnstock_data import TopStock

insights = TopStock()

# Top tăng giá
gainers = insights.gainer(limit=5)
print("Top 5 cổ phiếu tăng giá:")
print(gainers[['symbol', 'price_change_pct_1d', 'accumulated_value']].to_string())

# Top giảm giá
losers = insights.loser(limit=5)
print("\nTop 5 cổ phiếu giảm giá:")
print(losers[['symbol', 'price_change_pct_1d', 'accumulated_value']].to_string())

# Top giá trị giao dịch
top_value = insights.value(limit=5)
print("\nTop 5 cổ phiếu theo giá trị giao dịch:")
print(top_value[['symbol', 'accumulated_value']].to_string())

# Top khối lượng
top_volume = insights.volume(limit=5)
print("\nTop 5 cổ phiếu theo khối lượng đột biến:")
print(top_volume[['symbol', 'volume_spike_20d_pct']].to_string())

# Khối ngoại mua ròng
foreign_buy = insights.foreign_buy(limit=5)
print("\nTop 5 cổ phiếu NĐTNN mua ròng:")
print(foreign_buy.to_string())
```

## Phân Tích Ví Dụ

```python
from vnstock_data import TopStock
import pandas as pd

insights = TopStock()

# Lấy dữ liệu
gainers = insights.gainer(limit=20)
losers = insights.loser(limit=20)
foreign_buy = insights.foreign_buy(limit=20)

# Tìm giao lộ: tăng giá + nước ngoài mua
gaining_symbols = set(gainers['symbol'])
foreign_buying_symbols = set(foreign_buy['symbol'])
intersection = gaining_symbols & foreign_buying_symbols

print(f"Cổ phiếu vừa tăng giá vừa NĐTNN mua ròng ({len(intersection)} cổ):")
for symbol in sorted(intersection):
    gainer_pct = gainers[gainers['symbol'] == symbol]['price_change_pct_1d'].values[0]
    foreign_buy_val = foreign_buy[foreign_buy['symbol'] == symbol]['net_value'].values[0]
    print(f"  {symbol}: +{gainer_pct:.2f}% | Mua ròng: {foreign_buy_val:.2e}")

# Phân tích flow nước ngoài
print(f"\nTop 5 NĐTNN mua ròng:")
print(foreign_buy[['symbol', 'net_value']].head(5).to_string(index=False))

print(f"\nTop 5 NĐTNN bán ròng:")
top_sell = insights.foreign_sell(limit=5)
print(top_sell[['symbol', 'net_value']].to_string(index=False))

# Tìm cơ hội: giảm giá nhưng nước ngoài vẫn mua
losing_symbols = set(losers['symbol'])
potential_opportunities = foreign_buying_symbols - losing_symbols

print(f"\nCổ phiếu NĐTNN mua không xuất hiện trong top giảm:")
print(f"Số lượng: {len(potential_opportunities)}")
print(f"Ví dụ: {list(potential_opportunities)[:5]}")
```


**Lưu ý**: Chỉ VND hỗ trợ TopStock.

## Ứng Dụng

- **Tìm cơ hội**: Phát hiện cổ phiếu tăng giá, khối ngoại mua
- **Theo dõi dòng tiền**: Xem khối ngoại đang mua/bán cổ phiếu nào
- **Phân tích thị trường**: Hiểu tâm lý thị trường qua top tăng/giảm giá.
- **Cảnh báo**: Theo dõi nếu cổ phiếu quan tâm xuất hiện trong top
