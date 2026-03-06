# Unified UI - Giao Diện Hợp Nhất (Unified Financial Data Platform)

Thư mục `vnstock_data` cung cấp một cấu trúc giao diện cấp cao gom nhóm tất cả các tính năng dữ liệu thành từng **domain ngữ nghĩa** để dễ dàng tra cứu và gọi.

Các lớp dữ liệu được phân chia thành **5 trụ cột chính**: `Reference`, `Market`, `Fundamental`, `Insights`, và `Macro`.

---

## 📚 Tổng Quan Kiến Trúc

### Các Domain Chính (5 Cột Sống)

| Domain | Mô Tả | Mục Đích | Layer |
|--------|-------|---------|-------|
| **Reference** | Dữ liệu tham chiếu | Thông tin công ty, chỉ số, danh sách | Layer 1 |
| **Market** | Dữ liệu giao dịch | Giá, thanh khoản, khối lượng | Layer 2 |
| **Fundamental** | Dữ liệu cơ bản | BCTC, tỷ số, phân tích | Layer 3 |
| **Insights** | Phân tích chuyên sâu | Xếp hạng, định giá, khuyến nghị | Layer 4 |
| **Macro** | Dữ liệu vĩ mô | Kinh tế, tiền tệ, hàng hóa | Layer 5 |

### Cấu Trúc Phân Cấp

```
vnstock_data
├── Reference (Layer 1)
│   ├── .company()          # Thông tin công ty
│   ├── .equity()           # Danh sách cổ phiếu
│   ├── .index()            # Danh sách chỉ số
│   ├── .industry()         # Ngành kinh tế
│   ├── .fund()             # Quỹ đầu tư
│   └── .derivatives()      # Chứng chỉ phái sinh
│       ├── .warrant()      # Chứng quyền (nested)
│       └── .futures()      # Hợp đồng tương lai (nested)
│
├── Market (Layer 2)
│   ├── .equity()           # Thị trường cổ phiếu
│   ├── .index()            # Thị trường chỉ số
│   ├── .fund()             # Thị trường quỹ
│   └── .derivatives()      # Thị trường phái sinh
│       ├── .warrant()      # Thị trường chứng quyền (nested)
│       └── .futures()      # Thị trường tương lai (nested)
│
├── Fundamental (Layer 3)
│   └── .equity             # Báo cáo tài chính
│
├── Macro (Layer 4)
│   ├── .economy()          # Dữ liệu kinh tế
│   ├── .currency()         # Tỷ giá & Lãi suất
│   └── .commodity()        # Hàng hóa
│
│
└── Insights (Layer 5)
│   ├── .ranking            # Xếp hạng
│   ├── .valuation          # Định giá
│   └── .screener           # Lọc chứng khoán
```

---

## 🚀 Khởi Tạo & Cách Sử Dụng

### Import

```python
from vnstock_data import Reference, Market, Fundamental, Insights, Macro
```

### Khởi Tạo

```python
ref = Reference()
mkt = Market()
fun = Fundamental()
ins = Insights()
mac = Macro()
```

### Gọi Dữ Liệu (Chaining API)

```python
# Reference: Lấy thông tin công ty
df_company = ref.company("TCB").profile()

# Market: Lấy lịch sử giá
df_history = mkt.equity("VIC").ohlcv(
    start="2026-02-06", 
    end="2026-03-06"
)

# Fundamental: Lấy báo cáo tài chính
df_income = fun.equity.income_statement("HPG", period="Y")

# Insights: Lấy top gainer
df_gainers = ins.ranking.gainer()

# Macro: Lấy dữ liệu kinh tế
df_gdp = mac.economy().gdp(period="quarter")
df_interest = mac.currency().interest_rate(length=90)
df_gold = mac.commodity().gold(market="VN")
```

---

## 🎯 Quick Start - Ví Dụ Đầy Đủ

```python
from vnstock_data import Reference, Market, Fundamental, Insights, Macro

# Reference: Lấy danh sách công ty, chỉ số, chứng chỉ
ref = Reference()
companies = ref.company("TCB").profile()
equity_list = ref.equity().list()

# Derivatives (nested under Reference)
warrant = ref.derivatives().warrant("CACB2511").profile()
futures = ref.derivatives().futures("VN30F2503").profile()

# Market: Lấy giá, khối lượng, lịch sử giao dịch
mkt = Market()
price_history = mkt.equity("VIC").ohlcv(start="2026-02-06", end="2026-03-06")
quote = mkt.equity("VIC").quote()

# Derivatives market (nested under Market)
warrant_price = mkt.derivatives().warrant("CACB2511").ohlcv()
futures_price = mkt.derivatives().futures("VN30F2503").quote()

# Fundamental: Báo cáo tài chính, tỷ số
fun = Fundamental()
income = fun.equity.income_statement("HPG", period="Y")
ratio = fun.equity.ratio("TCB")

# Insights: Xếp hạng, định giá, khuyến nghị
ins = Insights()
gainers = ins.ranking.gainer()
valuation = ins.valuation.evaluation()

# Macro: Kinh tế, tiền tệ, hàng hóa
mac = Macro()
gdp = mac.economy().gdp(period="quarter")
exchange = mac.currency().exchange_rate()
gold = mac.commodity().gold(market="VN")
```

---

## 📖 Tài Liệu Chi Tiết Theo Layer

Để tìm hiểu chi tiết về từng unified UI layer:

| Layer | Tài Liệu | Nội Dung Chính |
|-------|----------|--------|
| **1: Reference** | [01-reference-layer.md](./unified-ui/01-reference-layer.md) | Company, Equity, Index, Industry, Warrant, Fund, Derivatives |
| **2: Market** | [02-market-layer.md](./unified-ui/02-market-layer.md) | Equity market, Index, Futures, Warrant, Fund, Market-wide |
| **3: Fundamental** | [03-fundamental-layer.md](./unified-ui/03-fundamental-layer.md) | Income statement, Balance sheet, Cash flow, Ratios |
| **4: Insights** | [04-insights-layer.md](./unified-ui/04-insights-layer.md) | Ranking, Valuation, Screener |
| **5: Macro** | [05-macro-layer.md](./unified-ui/05-macro-layer.md) | Economy, Currency, Commodity |

---

## 🔗 Cấu Trúc Registry

Mỗi domain được map tới các provider cụ thể thông qua **ProviderRegistry**:

```
Domain Method → (Source, ModuleType, ClassName, MethodName)

Ví dụ:
"reference.company.profile" → ("vci", "company", "Company", "overview")
"market.equity.ohlcv" → ("kbs", "quote", "Quote", "history")
"macro.economy.gdp" → ("mbk", "macro", "Macro", "gdp")
"macro.currency.interest_rate" → ("mbk", "macro", "Macro", "interest_rate")
```

---

## 🎯 Best Practices

### 1️⃣ Sử Dụng Domain Classes thay vì Provider trực tiếp

```python
# ✅ RECOMMENDED - Sử dụng Unified UI
mac = Macro()
df = mac.economy().gdp(period="quarter")

# ❌ Không khuyên - Gọi provider trực tiếp
from vnstock_data.api.macro import Macro
m = Macro(source="mbk")
df = m.gdp()
```

### 2️⃣ Method Chaining

```python
# Chaining API cho phép linh hoạt
df_gdp = Macro().economy().gdp(period="quarter")
df_gainers = Insights().ranking.gainer()
df_history = Market().equity("VIC").ohlcv(
    start="2026-02-06", 
    end="2026-03-06"
)
```

### 3️⃣ Xử Lý Lỗi

```python
try:
    df = Reference().company("INVALID").profile()
except ValueError as e:
    print(f"Lỗi: {e}")
except NotImplementedError as e:
    print(f"Phương thức không được hỗ trợ: {e}")
```

### 4️⃣ Nested Derivatives Structure

```python
# ✅ RECOMMENDED: Warrant & Futures nested under derivatives
warrant = Reference().derivatives().warrant("CACB2511").profile()
futures = Market().derivatives().futures("VN30F2503").ohlcv()

# ❌ Cũ (không tồn tại nữa)
warrant = Reference().warrant("CACB2511")  # AttributeError
futures = Market().futures("VN30F2503")    # AttributeError
```

### 5️⃣ Backward Compatibility (Deprecated)

```python
# ⚠️ DEPRECATED: Sẽ xóa sau 31/8/2026
m = Macro()
df = m.gdp()  # Shows deprecation warning (Tiếng Việt + English)

# ✅ RECOMMENDED: Cấu trúc mới
df = Macro().economy().gdp(period="quarter")
```

---

## 📊 Ví Dụ Thực Tế

### Ví dụ 1: Phân Tích Một Cổ Phiếu

```python
from vnstock_data import Reference, Market, Fundamental

ref = Reference()
mkt = Market()
fun = Fundamental()

symbol = "TCB"

# Thông tin công ty
company = ref.company(symbol).profile()

# Giá hiện tại
quote = mkt.equity(symbol).quote()

# Lịch sử giá 1 tháng
history = mkt.equity(symbol).ohlcv(
    start="2026-02-06", 
    end="2026-03-06"
)

# Tỷ số tài chính
ratio = fun.equity.ratio(symbol)

print(f"Company: {company['name']}")
print(f"Current Price: {quote['close']}")
print(f"PE Ratio: {ratio['pe']}")
```

### Ví dụ 2: Xem Top Cổ Phiếu Tăng Giá

```python
from vnstock_data import Insights

ins = Insights()

# Top 10 cổ phiếu tăng giá nhất
gainers = ins.ranking.gainer()
print(gainers[['code', 'change_percent']].head(10))

# Top cổ phiếu theo khối lượng giao dịch
high_volume = ins.ranking.volume()
print(high_volume.head(10))
```

### Ví dụ 3: Phân Tích Vĩ Mô

```python
from vnstock_data import Macro

mac = Macro()

# Dữ liệu GDP theo quý
gdp = mac.economy().gdp(period="quarter")
print(gdp.tail(4))

# Tỷ giá hối đoái
exchange = mac.currency().exchange_rate()
print(exchange.tail(1)['USD'].values[0])

# Giá vàng trong nước
gold = mac.commodity().gold(market="VN")
print(gold.tail(1))
```

### Ví dụ 4: Chứng Quyền & Hợp Đồng Tương Lai

```python
from vnstock_data import Reference, Market

ref = Reference()
mkt = Market()

# Lấy thông tin chứng quyền
warrant_info = ref.derivatives().warrant("CACB2511").profile()
print(warrant_info)

# Lấy lịch sử giá chứng quyền
warrant_price = mkt.derivatives().warrant("CACB2511").ohlcv(
    start="2026-02-06",
    end="2026-03-06"
)
print(warrant_price)

# Lấy thông tin hợp đồng tương lai
futures_info = ref.derivatives().futures("VN30F2503").profile()
futures_price = mkt.derivatives().futures("VN30F2503").quote()
```

---

## ⚠️ Migration Note: Backward Compatibility

### Deprecated Macro API

**Sẽ xóa sau 31/8/2026:**
```python
m = Macro()
m.interest_rate(length=90)  # ⚠️ Shows deprecation warning
```

**Dùng cấu trúc mới thay thế:**
```python
Macro().currency().interest_rate(length=90)  # ✓
Macro().economy().gdp(period="quarter")      # ✓
Macro().commodity().gold(market="VN")        # ✓
```

**Tất cả warning hiển thị song ngữ (Tiếng Việt + English):**
```
[DEPRECATED] Macro.interest_rate() sẽ bị xóa sau ngày 31/8/2026. 
Vui lòng sử dụng Macro().currency().interest_rate() thay thế. | 
Macro.interest_rate() is deprecated and will be removed after 31/8/2026. 
Please use Macro().currency().interest_rate() instead.
```

---

## 🔍 Troubleshooting

| Error | Nguyên Nhân | Giải Pháp |
|-------|-----------|----------|
| `AttributeError: 'Reference' has no attr 'warrant'` | Old API không tồn tại nữa | Dùng `ref.derivatives().warrant()` |
| `AttributeError: 'Market' has no attr 'futures'` | Old API không tồn tại nữa | Dùng `mkt.derivatives().futures()` |
| `NotImplementedError: Method not found` | Source không hỗ trợ | Xem tài liệu chi tiết từng layer |
| `ValueError: source not found` | Source name sai | Kiểm tra lowercase (ví dụ: "kbs" không "KBS") |
| `DeprecationWarning` | Dùng legacy Macro API | Migrate tới `Macro().economy()` structure |

---

## 📖 Lưu Ý Quan Trọng

### 1. Hiệu Suất
- API UI được thiết kế cho **tính thuận tiện** hơn **tốc độ**
- Nếu xử lý bulk data, xem xét sử dụng API layer trực tiếp

### 2. Khả Dụng Phương Thức
- Không phải method nào cũng hỗ trợ bởi tất cả sources
- Nếu gặp `NotImplementedError`, source khác có thể không implement
- Xem tài liệu chi tiết từng layer để biết support nào

### 3. Nested Structure
- **Warrant** & **Futures** bây giờ nested dưới `derivatives()`
- Áp dụng cả Reference và Market layers
- Giúp tổ chức code tốt hơn và dễ mở rộng

### 4. Backward Compatibility
- Legacy Macro API vẫn hoạt động cho đến **31/8/2026**
- Sẽ hiển thị deprecation warning (song ngữ)
- Hãy migrate sang cấu trúc mới

---

## ⚠️ Migration từ Legacy Explorer API (Sẽ Loại Bỏ)

Nếu bạn vẫn đang sử dụng các lớp explorer layer cũ, vui lòng migrate sang Unified UI architecture mới:

### Legacy API Được Bảo Trì Cho Đến 31/8/2026

Hai lớp hàm là Macro và Market sẽ được chuyển đổi sang mục đích sử dụng các phương thức mới theo Unified UI.

| Legacy Class | Status | Migration Guide |
|--------------|--------|-----------------|
| `Macro()` (explorer layer) | ⚠️ DEPRECATED | [09-macro.md](./09-macro.md) |
| `Market()` (explorer layer) | ⚠️ DEPRECATED | [10-market.md](./10-market.md) |

### Ví Dụ Chuyển Đổi

```python
# ❌ CŨ (sẽ không hoạt động sau 31/8/2026)
from vnstock_data import Macro, Market
macro = Macro()
gdp_df = macro.gdp()
market = Market()
pe_df = market.pe()

# ✅ MỚI (sử dụng cấu trúc Unified UI)
from vnstock_data import Macro, Market
macro = Macro()
gdp_df = macro.economy().gdp()
market = Market()
pe_df = market.equity().valuation().pe()
```

### Timeline Deprecation

- **Hiện tại (2026-03-06)**: Legacy API hoạt động, hiển thị deprecation warnings
- **31/8/2026**: Cutoff date - legacy explorer classes sẽ bị xóa
- **Sau 31/8/2026**: Chỉ Unified UI API khả dụng

**Lưu ý**: Import `Macro` và `Market` từ `vnstock_data` để sử dụng Unified UI, hoặc từ `vnstock_data` để sử dụng legacy explorer (cho đến deadline).

---

## 📞 Để Tìm Hiểu Thêm

- **Registry System:** `vnstock_data/ui/_registry.py`
- **Base Classes:** `vnstock_data/ui/_base.py`
- **Source Code:** `vnstock_data/ui/domains/`
- **Legacy API Migration:** [09-macro.md](./09-macro.md), [10-market.md](./10-market.md)

---

*Last Updated: March 6, 2026*  
*Status: Production Ready ✅*
