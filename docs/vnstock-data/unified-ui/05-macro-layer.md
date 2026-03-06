# Layer 6: Macro Data (Dữ Liệu Vĩ Mô & Hàng Hóa)

## 📌 Tổng Quan

**Macro Layer** cung cấp dữ liệu **kinh tế vĩ mô, tiền tệ, hàng hóa** phục vụ cho:
- Phân tích tác động yếu tố kinh tế đến thị trường
- Trading danh sách hàng hóa (gold, oil, steel, etc.)
- Quản lý rủi ro tiền tệ, lãi suất
- Dự báo xu hướng kinh tế

## 🏗️ Cấu Trúc Domain

```python
Macro()
├── .economy()       # Dữ liệu kinh tế Việt Nam
├── .currency()      # Tỷ giá, lãi suất
└── .commodity()     # Giá hàng hóa
```

## 📋 Chi Tiết Các Domain

### 1. Economy Domain (Kinh Tế Việt Nam)

**Source:** MBK (mbk)  
**Registry Key:** `"macro.economy"`

#### Mô Tả

Dữ liệu kinh tế Việt Nam theo quý/năm: GDP, CPI, FDI, xuất nhập khẩu, v.v.

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `gdp()` | `start`, `end`, `period` | Tăng trưởng GDP | DataFrame |
| `cpi()` | `start`, `end`, `period` | Chỉ số giá tiêu dùng | DataFrame |
| `industry_prod()` | `start`, `end`, `period` | Sản xuất công nghiệp | DataFrame |
| `import_export()` | `start`, `end`, `period` | Xuất nhập khẩu | DataFrame |
| `retail()` | `start`, `end`, `period` | Bán lẻ | DataFrame |
| `fdi()` | `start`, `end`, `period` | Đầu tư trực tiếp nước ngoài | DataFrame |
| `money_supply()` | `start`, `end`, `period` | Cung tiền | DataFrame |
| `population_labor()` | `start`, `end`, `period` | Dân số & lao động | DataFrame |

**Parameters:**
- `start`: Mốc bắt đầu (ví dụ: "2020-01" hoặc "2020")
- `end`: Mốc kết thúc (ví dụ: "2026-03")
- `period`: "quarter" (mặc định) hoặc "month" hoặc "year"
- `length`: Số kỳ gần nhất (ví dụ: length=12 lấy 12 tháng gần nhất)

#### Ví Dụ

```python
from vnstock_data import Macro

mac = Macro()

# ===== GDP Growth (Tăng Trưởng GDP) =====
# GDP theo quý
df_gdp_q = mac.economy().gdp(
    start="2020-01",
    end="2026-03",
    period="quarter"
)
print(df_gdp_q[['report_time', 'gdp_growth']])
#      report_time  gdp_growth
# 0    2020Q1       3.5%
# 1    2020Q2       0.4%
# 2    2020Q3       2.4%

# GDP năm
df_gdp_y = mac.economy().gdp(period="year")
print(df_gdp_y[['report_time', 'gdp_growth']].tail(3))

# ===== CPI (Chỉ Số Giá) =====
# CPI theo tháng
df_cpi = mac.economy().cpi(period="month", length=24)  # 24 tháng gần nhất
print(df_cpi[['report_time', 'cpi_yoy', 'cpi_mom']])
#      report_time  cpi_yoy  cpi_mom
# 0    2024-03     2.50%    0.30%
# 1    2024-04     3.65%    0.45%

# ===== Industrial Production (Sản Xuất Công Nghiệp) =====
df_ind = mac.economy().industry_prod(period="month", length=12)
print(df_ind[['report_time', 'production_growth']])

# ===== Import-Export (Xuất Nhập Khẩu) =====
df_trade = mac.economy().import_export(period="month")
print(df_trade[['report_time', 'export', 'import', 'trade_balance']])
#      report_time    export    import  trade_balance
# 0    2026-02      3500.5    3200.3        +300.2

# ===== Retail Sales (Bán Lẻ) =====
df_retail = mac.economy().retail(period="month")
print(df_retail[['report_time', 'retail_sales']])

# ===== FDI (Đầu Tư Trực Tiếp) =====
df_fdi = mac.economy().fdi(period="month")
print(df_fdi[['report_time', 'fdi_registered', 'fdi_implemented']])

# ===== Money Supply (Cung Tiền) =====
df_money = mac.economy().money_supply(period="month")
print(df_money[['report_time', 'm0', 'm1', 'm2']])

# ===== Population & Labor (Dân Số & Lao Động) =====
df_labor = mac.economy().population_labor(period="year")
print(df_labor[['report_time', 'population', 'unemployment_rate']])
```

---

### 2. Currency Domain (Tiền Tệ & Lãi Suất)

**Source:** MBK (mbk)  
**Registry Key:** `"macro.currency"`

#### Mô Tả

Tỷ giá hối đoái, lãi suất tiền tệ, chính sách tiền tệ.

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `exchange_rate()` | `start`, `end`, `period` | Tỷ giá hối đoái | DataFrame |
| `interest_rate()` | `start`, `end`, `period`, `format` | Lãi suất | DataFrame |

**Parameters:**
- `period`: "day" (mặc định), "month", "quarter"
- `format`: "pivot" (mặc định) hoặc "long"
- `length`: Số kỳ gần nhất

#### Ví Dụ

```python
from vnstock_data import Macro

mac = Macro()

# ===== Exchange Rate (Tỷ Giá Hối Đoái) =====
# Tỷ giá hàng ngày
df_exr = mac.currency().exchange_rate(
    start="2026-02-06",
    end="2026-03-06",
    period="day"
)
print(df_exr[['report_time', 'USD', 'EUR', 'JPY']])
#      report_time      USD      EUR      JPY
# 0    2026-02-06    24500    26800    165.5
# 1    2026-02-09    24510    26750    165.2

# Tỷ giá trung bình tháng
df_exr_m = mac.currency().exchange_rate(period="month", length=12)
print(df_exr_m[['report_time', 'USD', 'EUR']].tail())

# ===== Interest Rate (Lãi Suất) =====
# Lãi suất hàng ngày
df_ir = mac.currency().interest_rate(
    period="day",
    length=365  # 1 năm gần nhất
)
print(df_ir[['report_time', 'lending_rate', 'deposit_rate']])
#      report_time  lending_rate  deposit_rate
# 0    2025-03-06        4.50%         0.80%
# 1    2025-03-07        4.50%         0.85%

# Định dạng long (dễ phân tích hơn)
df_ir_long = mac.currency().interest_rate(period="month", format="long")
print(df_ir_long[['date', 'rate_type', 'rate_value']].head(10))
#             date     rate_type  rate_value
# 0    2025-01       lending    4.50%
# 1    2025-01       deposit    0.80%
```

---

### 3. Commodity Domain (Hàng Hóa)

**Source:** SPL (spl)  
**Registry Key:** `"macro.commodity"`

#### Mô Tả

Giá hàng hóa địa phương và quốc tế: vàng, dầu, thép, nông sản, v.v.

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `gold()` | `market`, `start`, `end` | Giá vàng | DataFrame |
| `gas()` | `market`, `start`, `end` | Giá xăng dầu | DataFrame |
| `oil_crude()` | `start`, `end` | Giá dầu thô | DataFrame |
| `coke()` | `start`, `end` | Giá coke (than cốc) | DataFrame |
| `steel()` | `market`, `start`, `end` | Giá thép | DataFrame |
| `iron_ore()` | `start`, `end` | Giá quặng sắt | DataFrame |
| `fertilizer_ure()` | `start`, `end` | Giá phân URE | DataFrame |
| `soybean()` | `start`, `end` | Giá đậu tương | DataFrame |
| `corn()` | `start`, `end` | Giá ngô | DataFrame |
| `sugar()` | `start`, `end` | Giá đường | DataFrame |
| `pork()` | `market`, `start`, `end` | Giá thịt lợn | DataFrame |

**Parameters (cho gold, gas, steel, pork):**
- `market`: "VN" (Việt Nam) hoặc "GLOBAL" (quốc tế), mặc định = "VN"
- `start`, `end`: Khoảng thời gian lịch sử

#### Ví Dụ

```python
from vnstock_data import Macro
import pandas as pd

mac = Macro()

# ===== Gold (Vàng) =====
# Giá vàng trong nước (SJC)
df_gold_vn = mac.commodity().gold(market="VN")
print(df_gold_vn[['report_time', 'price']].tail())
#      report_time     price
# 0    2026-03-06  80050000  (VNĐ/lượng)
# 1    2026-03-05  79950000

# Giá vàng quốc tế (GC=F)
df_gold_global = mac.commodity().gold(market="GLOBAL")
print(df_gold_global[['report_time', 'price']])  # USD/troy oz

# ===== Gas / Petrol (Xăng Dầu) =====
# Giá xăng lẻ trong nước
df_gas_vn = mac.commodity().gas(market="VN")
print(df_gas_vn[['report_time', 'ron92_price', 'do_price']])

# Giá khí tự nhiên quốc tế
df_gas_global = mac.commodity().gas(market="GLOBAL")
print(df_gas_global[['report_time', 'price']])  # USD/MMBtu

# ===== Crude Oil (Dầu Thô) =====
# Giá dầu thô WTI & Brent
df_oil = mac.commodity().oil_crude()
print(df_oil[['report_time', 'brent', 'wti']])
#      report_time   brent    wti
# 0    2026-03-06   90.50  85.25

# ===== Coke (Than Cốc) =====
df_coke = mac.commodity().coke()
print(df_coke[['report_time', 'price']])

# ===== Steel (Thép) =====
# Thép trong nước
df_steel_vn = mac.commodity().steel(market="VN")
print(df_steel_vn[['report_time', 'price']])

# Thép quốc tế (HRC)
df_steel_global = mac.commodity().steel(market="GLOBAL")
print(df_steel_global[['report_time', 'price']])  # USD/tấn

# ===== Iron Ore (Quặng Sắt) =====
df_ore = mac.commodity().iron_ore()
print(df_ore[['report_time', 'price']])  # USD/tấn

# ===== Nông Sản (Crops) =====
# Giá đậu tương (Soybean)
df_soy = mac.commodity().soybean()
print(df_soy[['report_time', 'price']])  # USD/bushel

# Giá ngô (Corn)
df_corn = mac.commodity().corn()
print(df_corn[['report_time', 'price']])

# Giá đường (Sugar)
df_sugar = mac.commodity().sugar()
print(df_sugar[['report_time', 'price']])

# ===== Pork (Thịt Lợn) =====
# Giá lợn hơi Việt Nam (miền Bắc)
df_pork_vn = mac.commodity().pork(market="VN")
print(df_pork_vn[['report_time', 'price']])  # VNĐ/kg

# Giá lợn hơi Trung Quốc
df_pork_china = mac.commodity().pork(market="CHINA")
print(df_pork_china[['report_time', 'price']])
```

---

## 🔗 Registry Mapping

```python
MACRO_SOURCES = {
    "macro.economy": {
        "gdp": ("mbk", "macro", "Macro", "gdp"),
        "cpi": ("mbk", "macro", "Macro", "cpi"),
        "industry_prod": ("mbk", "macro", "Macro", "industry_prod"),
        "import_export": ("mbk", "macro", "Macro", "import_export"),
        "retail": ("mbk", "macro", "Macro", "retail"),
        "fdi": ("mbk", "macro", "Macro", "fdi"),
        "money_supply": ("mbk", "macro", "Macro", "money_supply"),
        "population_labor": ("mbk", "macro", "Macro", "population_labor"),
    },
    "macro.currency": {
        "exchange_rate": ("mbk", "macro", "Macro", "exchange_rate"),
        "interest_rate": ("mbk", "macro", "Macro", "interest_rate"),
    },
    "macro.commodity": {
        "gold_vn": ("spl", "commodity", "CommodityPrice", "gold_vn"),
        "gold_global": ("spl", "commodity", "CommodityPrice", "gold_global"),
        "gas_vn": ("spl", "commodity", "CommodityPrice", "gas_vn"),
        "gas_natural": ("spl", "commodity", "CommodityPrice", "gas_natural"),
        "oil_crude": ("spl", "commodity", "CommodityPrice", "oil_crude"),
        "coke": ("spl", "commodity", "CommodityPrice", "coke"),
        "steel_d10": ("spl", "commodity", "CommodityPrice", "steel_d10"),
        "steel_hrc": ("spl", "commodity", "CommodityPrice", "steel_hrc"),
        "iron_ore": ("spl", "commodity", "CommodityPrice", "iron_ore"),
        "fertilizer_ure": ("spl", "commodity", "CommodityPrice", "fertilizer_ure"),
        "soybean": ("spl", "commodity", "CommodityPrice", "soybean"),
        "corn": ("spl", "commodity", "CommodityPrice", "corn"),
        "sugar": ("spl", "commodity", "CommodityPrice", "sugar"),
        "pork_vn": ("spl", "commodity", "CommodityPrice", "pork_north_vn"),
        "pork_china": ("spl", "commodity", "CommodityPrice", "pork_china"),
    }
}
```

---

## 💡 Best Practices

### 1. Phân Tích Tác Động Vĩ Mô

```python
from vnstock_data import Macro, Market
import pandas as pd

mac = Macro()
mkt = Market()

# Lấy dữ liệu GDP & CPI
gdp = mac.economy().gdp(period="quarter", length=8)  # 2 năm gần nhất
cpi = mac.economy().cpi(period="quarter", length=8)

# Lấy giá chỉ số thị trường
vnindex = mkt.index.quote("VNINDEX")

# Phân tích tương quan
print("Xu hướng kinh tế:")
print(f"GDP growth: {gdp['gdp_growth'].iloc[-1]}")
print(f"CPI (YoY): {cpi['cpi_yoy'].iloc[-1]}")
print(f"VNIndex: {vnindex['close'].values[0]:.0f}")
```

### 2. Theo Dõi Tỷ Giá & Lãi Suất

```python
from vnstock_data import Macro

mac = Macro()

# Tỷ giá USD/VND
exr = mac.currency().exchange_rate(period="day", length=90)
print("Tỷ giá USD/VND - 3 tháng gần nhất:")
print(exr[['report_time', 'USD']].tail(10))

# Thay đổi tỷ giá
exr['USD_change'] = exr['USD'].pct_change() * 100
strengthening = (exr['USD_change'] > 0).sum()
weakening = (exr['USD_change'] < 0).sum()
print(f"USD tăng giá: {strengthening} ngày, USD giảm giá: {weakening} ngày")

# Lãi suất
ir = mac.currency().interest_rate(period="month", length=12)
print("Xu hướng lãi suất:")
print(ir[['report_time', 'lending_rate']].tail(5))

if ir['lending_rate'].iloc[-1] > ir['lending_rate'].iloc[-2]:
    print("⬆️ Lãi suất tăng")
else:
    print("⬇️ Lãi suất giảm")
```

### 3. Phân Tích Giá Hàng Hóa

```python
from vnstock_data import Macro

mac = Macro()

# Giá vàng Việt Nam
gold_vn = mac.commodity().gold(market="VN", length=90)
gold_vn['Price_MA20'] = gold_vn['price'].rolling(20).mean()

print("Giá vàng SJC (3 tháng gần nhất):")
print(gold_vn[['report_time', 'price', 'Price_MA20']].tail(5))

# Tín hiệu
if gold_vn['price'].iloc[-1] > gold_vn['Price_MA20'].iloc[-1]:
    print("✓ Giá vàng phá vỡ MA20 (khả năng tăng tiếp)")
else:
    print("✗ Giá vàng dưới MA20 (khả năng giảm tiếp)")

# Giá dầu
oil = mac.commodity().oil_crude(length=90)
print("\nGiá dầu WTI (3 tháng gần nhất):")
print(oil[['report_time', 'wti']].tail(5))

# Volatility
oil_volatility = oil['wti'].std()
print(f"Volatility: {oil_volatility:.2f} USD/barrel")
```

### 4. Dashboard Vĩ Mô

```python
from vnstock_data import Macro
import pandas as pd

mac = Macro()

# Tổng hợp chỉ số vĩ mô hiện tại
print("=== MACRO DASHBOARD ===")
print()

# Kinh tế
gdp = mac.economy().gdp(period="quarter", length=1)
cpi = mac.economy().cpi(period="month", length=1)
fdi = mac.economy().fdi(period="month", length=1)

print("📊 ECONOMY:")
print(f"  GDP Growth: {gdp['gdp_growth'].iloc[-1]}")
print(f"  CPI (YoY): {cpi['cpi_yoy'].iloc[-1]}")
print(f"  FDI Capital: ${fdi['fdi_registered'].iloc[-1]:.0f}M")

# Tiền tệ
exr = mac.currency().exchange_rate(period="day", length=1)
ir = mac.currency().interest_rate(period="day", length=1)

print("\n💱 CURRENCY & RATES:")
print(f"  USD/VND: {exr['USD'].iloc[-1]:,.0f}")
print(f"  Lending Rate: {ir['lending_rate'].iloc[-1]}")
print(f"  Deposit Rate: {ir['deposit_rate'].iloc[-1]}")

# Hàng hóa
gold = mac.commodity().gold(market="VN", length=1)
oil = mac.commodity().oil_crude(length=1)

print("\n⛽ COMMODITIES:")
print(f"  Gold (SJC): {gold['price'].iloc[-1]:,.0f} VNĐ/lượng")
print(f"  Crude Oil (WTI): ${oil['wti'].iloc[-1]:.2f}/barrel")

print("\n" + "="*30)
```

---

## ⚠️ Lưu Ý Quan Trọng

### 1. **Backward Compatibility (Tương Thích Ngược)**

**DEPRECATED** (sẽ xóa sau 31/8/2026):
```python
# ❌ CÓ HÌNH SắU LE - Sẽ bị xóa
m = Macro()
df = m.interest_rate(length=90)  # ⚠️ Warning
```

**RECOMMENDED** (Dùng từ bây giờ):
```python
# ✅ CHÍNH THỨC
df = Macro().currency().interest_rate(length=90)
```

Tất cả legacy methods sẽ hiển thị **deprecation warning bằng tiếng Việt + Anh**:
```
[DEPRECATED] Macro.interest_rate() sẽ bị xóa sau ngày 31/8/2026. 
Vui lòng sử dụng Macro().currency().interest_rate() thay thế. | 
Macro.interest_rate() is deprecated and will be removed after 31/8/2026. 
Please use Macro().currency().interest_rate() instead.
```

### 2. **Độ Trễ Dữ Liệu**
- GDP, CPI: Công bố quý/tháng, có độ trễ 1-2 tuần
- Tỷ giá: Cập nhật hằng ngày, có thể bị delay 1-2 giờ
- Giá hàng hóa: Cập nhật hằng ngày, realtime hoặc T+1

### 3. **Đơn Vị Tiền Tệ**
- Tỷ giá: Nghìn VNĐ (ví dụ: 24.5 = 24,500 VNĐ)
- Vàng: VNĐ/lượng
- Dầu/Quặng: USD/barrel hoặc USD/tấn
- Nông sản: USD/bushel hoặc USD/tấn

### 4. **Chỉ Số & Phần Trăm**
- GDP Growth, CPI: Phần trăm YoY hoặc QoQ
- Lãi suất: Phần trăm năm (%/năm)
- Tỷ lệ: 0-100 (không phải 0-1)

---

## 🚦 Next Steps

- **Market Layer**: Để liên kết dữ liệu vĩ mô với thị trường chứng khoán
- **Fundamental Layer**: Để phân tích tác động của kinh tế đến các công ty
- **Insights Layer**: Để xem phân tích chuyên sâu tích hợp yếu tố vĩ mô
