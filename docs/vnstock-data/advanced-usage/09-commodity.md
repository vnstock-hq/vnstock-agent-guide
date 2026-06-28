# Commodity - Giá Hàng Hóa

Lớp `CommodityPrice` cung cấp dữ liệu giá hàng hóa (vàng, dầu, khí, sắt, nông sản, v.v.).

## Khởi Tạo

```python
from vnstock_data import CommodityPrice

# Khởi tạo cơ bản
commodity = CommodityPrice()

# Khởi tạo với ngày bắt đầu/kết thúc mặc định
commodity = CommodityPrice(start="2024-01-01", end="2025-12-31")

# Hiển thị debug logs
commodity = CommodityPrice(show_log=True)
```

### Tham Số Khởi Tạo

- `start` (str, optional): Ngày bắt đầu mặc định (format: "YYYY-MM-DD")
- `end` (str, optional): Ngày kết thúc mặc định (format: "YYYY-MM-DD")
- `length` (str|int, optional): Khoảng thời gian mặc định lấy dữ liệu. Mặc định là `1Y` (1 năm gần nhất tính từ ngày hnay). Xem chi tiết cấu trúc tại [README.md](../README.md#tham-số-thời-gian-tương-đối-length).
- `show_log` (bool, default=False): Bật log debug

**Lưu ý**: Chỉ **SPL** hỗ trợ Commodity.

## Phương Thức

### Vàng

```python
# Vàng Việt Nam (mua/bán) - 3 tháng gần nhất
df = commodity.gold_vn(length="3M")

# Vàng thế giới - 100 nến
df = commodity.gold_global(length="100b")
```

**Trả về**: 
- `gold_vn()`: DataFrame với cột `buy`, `sell` (float64)
- `gold_global()`: DataFrame với cột `open`, `high`, `low`, `close`, `volume`

**Ví dụ - Vàng VN** (3 dòng gần nhất):
```
                 buy      sell
time                          
2025-11-28  152200.0  154200.0
2025-11-29  152900.0  154900.0
2025-12-02  152600.0  154600.0
```

### Năng Lượng

```python
# Xăng/dầu Việt Nam - mặc định 1 năm
df = commodity.gas_vn()

# Dầu thô thế giới - 3 tháng
df = commodity.oil_crude(length="3M")

# Khí thiên nhiên - 30 ngày
df = commodity.gas_natural(length="30D")
```

**Trả về**:
- `gas_vn()`: DataFrame với cột `ron95`, `ron92`, `oil_do`
- `oil_crude()`: DataFrame với cột `open`, `high`, `low`, `close`, `volume`
- `gas_natural()`: DataFrame với cột `open`, `high`, `low`, `close`, `volume`

**Ví dụ - Dầu thô** (3 dòng gần nhất):
```
             open   high    low  close    volume
time                                            
2025-11-27  58.58  59.64  58.27  58.55  139202.0
2025-12-01  58.96  59.97  58.83  59.32  211462.0
2025-12-02  59.52  59.67  59.33  59.46    6724.0
```

### Kim Loại

```python
# Than cốc
df = commodity.coke()

# Thép D10 Việt Nam - 3 tháng
df = commodity.steel_d10(length="3M")

# Quặng sắt thế giới
df = commodity.iron_ore()

# Thép HRC thế giới
df = commodity.steel_hrc()
```

**Trả về**: DataFrame với cột `open`, `high`, `low`, `close`, `volume` (float64)

**Ví dụ - Thép HRC** (3 dòng gần nhất):
```
             open   high    low  close  volume
time                                          
2025-11-26  890.0  907.0  890.0  904.0    68.0
2025-11-27  908.0  908.0  904.0  908.0     1.0
2025-12-01  905.0  905.0  899.0  903.0    44.0
```

### Nông Sản

```python
# Phân bón Urê (Mặc định 1Y)
df = commodity.fertilizer_ure()

# Đậu nành
df = commodity.soybean(length="3Y")

# Ngô
df = commodity.corn()

# Đường
df = commodity.sugar()

# Lợn (heo) miền Bắc Việt Nam
df = commodity.pork_north_vn(length="100b")

# Lợn (heo) Trung Quốc
df = commodity.pork_china()
```

**Tham Số Chung Của Các Hàm**:
- `start` (str, optional): Ngày bắt đầu (format: "YYYY-MM-DD")
- `end` (str, optional): Ngày kết thúc (format: "YYYY-MM-DD")
- `length` (str|int, optional): Khoảng thời gian tương đối (VD: `"30D"`, `"3M"`, `"1Y"` hoặc `"100b"`). Xem [Định dạng length](../README.md#tham-số-thời-gian-tương-đối-length).

*Lưu ý*: Với mỗi method, nếu các đối số khởi tạo này bỏ trống, cấu hình khởi tạo của chính class `CommodityPrice` (Mặc định `1Y`) sẽ được áp dụng.

**Trả về**: DataFrame với cột OHLCV (`open`, `high`, `low`, `close`, `volume` - float64)

**Ví dụ - Lợn miền Bắc VN** (3 dòng gần nhất):
```
              close
time               
2025-11-16  48100.0
2025-11-23  52100.0
2025-11-30  54400.0
```

## Ví Dụ

```python
from vnstock_data import CommodityPrice
import matplotlib.pyplot as plt

commodity = CommodityPrice()

# Lấy giá vàng 30 ngày qua
gold_vn = commodity.gold_vn(length="30D")
print("Giá vàng Việt Nam gần đây:")
print(f"Giá mua hiện tại: {gold_vn['buy'].iloc[-1]:,.0f} VND/chỉ")
print(f"Giá bán hiện tại: {gold_vn['sell'].iloc[-1]:,.0f} VND/chỉ")

# Lấy giá dầu 1 năm
oil = commodity.oil_crude()
print(f"\nGiá dầu thô gần đây:")
print(f"Giá close: {oil['close'].iloc[-1]:.2f} USD/barrel")

# Lấy giá thép 6 tháng
steel = commodity.steel_hrc(length="6M")
print(f"\nGiá thép HRC gần đây:")
print(f"Giá close: {steel['close'].iloc[-1]:,.0f} USD/tấn")

# Lấy giá lợn mốc 1 năm
pork = commodity.pork_north_vn()
print(f"\nGiá lợn Bắc Việt Nam gần đây:")
print(f"Giá close: {pork['close'].iloc[-1]:,.0f} VND/kg")

# Vẽ biểu đồ giá vàng
plt.figure(figsize=(12, 4))
plt.plot(gold_vn.index, gold_vn['close'], label='Vàng VN')
plt.title('Giá Vàng Việt Nam')
plt.xlabel('Thời gian')
plt.ylabel('Giá (VND)')
plt.legend()
plt.grid(True)
plt.show()
```

## Phân Tích Ví Dụ

```python
from vnstock_data import CommodityPrice
import pandas as pd

commodity = CommodityPrice()

# Phân tích giá vàng
gold = commodity.gold_vn(start="2024-01-01", end="2025-12-31")

# Tính moving average
gold['MA30'] = gold['close'].rolling(30).mean()

# Tìm support/resistance
price_high = gold['close'].max()
price_low = gold['close'].min()
price_current = gold['close'].iloc[-1]

print(f"Giá vàng cao nhất: {price_high:,.0f} VND")
print(f"Giá vàng thấp nhất: {price_low:,.0f} VND")
print(f"Giá vàng hiện tại: {price_current:,.0f} VND")

# Tính % từ low
pct_from_low = (price_current - price_low) / (price_high - price_low) * 100
print(f"% từ low tới current: {pct_from_low:.1f}%")

# Phân tích dầu
oil = commodity.oil_crude(start="2024-01-01", end="2025-12-31")
oil_ma20 = oil['close'].rolling(20).mean()

print(f"\nGiá dầu thô:")
print(f"Giá hiện tại: ${oil['close'].iloc[-1]:.2f}")
print(f"MA20: ${oil_ma20.iloc[-1]:.2f}")

if oil['close'].iloc[-1] > oil_ma20.iloc[-1]:
    print("📈 Giá dầu trên đường MA20 (uptrend)")
else:
    print("📉 Giá dầu dưới đường MA20 (downtrend)")
```

## Ứng Dụng

- **Phân tích ngành**: Vàng ↑ → cổ phiếu vàng ↑
- **Lạm phát**: Dầu/khí ↑ → lạm phát ↑
- **Nông sản**: Giá lợn → ngành thức ăn chăn nuôi
- **Ngành công nghiệp**: Giá thép → ngành xây dựng, cơ khí