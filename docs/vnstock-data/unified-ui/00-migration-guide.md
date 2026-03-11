# Hướng Dẫn Chuyển Đổi Sang Unified UI

## 📌 Tổng Quan

Tài liệu này hướng dẫn cách chuyển đổi code đang sử dụng các lớp API/Explorer cũ (`vnstock_data.api`, `vnstock_data.explorer`) sang **Unified UI** — giao diện hợp nhất thế hệ mới.

### Tại sao nên chuyển đổi?

1. **Hợp nhất**: Unified UI gom tất cả tính năng dữ liệu từ `vnstock` (phiên bản cộng đồng) và `vnstock_data` (gói tài trợ) thành một hệ thống thống nhất. Người dùng có thể dễ dàng chuyển đổi giữa hai phiên bản mà không thay đổi code. Tại thời điểm 11/3/2026, Unified UI là giao diện được khuyến nghị sử dụng và đã sẵn sàng trong `vnstock_data`. Phiên bản `vnstock` sẽ được cập nhật Unified UI trong thời gian tới.
2. **Đơn giản**: Không cần nhớ tham số `source`, không cần biết tên class hay module nội bộ. Unified UI tự chọn nguồn dữ liệu tối ưu nhất cho từng loại dữ liệu.
3. **Nhất quán**: Cùng một cú pháp chaining API cho mọi loại dữ liệu, từ cổ phiếu trong nước đến kinh tế vĩ mô.
4. **Tra cứu nhanh**: `show_api()` và `show_doc()` giúp khám phá cấu trúc mà không cần đọc tài liệu hay source code.
5. **Phát triển nhanh chóng**: Với Unified UI, AI Agent có thể dễ dàng khám phá và sử dụng các tính năng dữ liệu mà không cần đọc tài liệu hay source code. Tác giả thư viện cũng có thể vận dụng cách "trám" (patching) dữ liệu nhanh chóng khi một api bất kỳ gặp lỗi mà không phải phát triển toàn bộ các api như cách làm trước đây khi bổ sung một nguồn cung cấp dữ liệu bất kỳ.

---

## 🔄 Bảng Chuyển Đổi Nhanh

### Lớp API cũ → Unified UI

| Lớp cũ (`vnstock_data.api`) | Unified UI tương ứng                                                             |
| --------------------------- | ------------------------------------------------------------------------------- |
| `Quote(source, symbol)`     `Market().equity(symbol)` / `.index()` /  `etf()`/ `.futures()` /  `.warrant()` /  |
| `Company(source, symbol)`   | `Reference().company(symbo                                                       |
| `Finance(source, symbol)`   | `Fundamental().equity(symb                                                       |
| `Listing(source)`           | `Reference().equity` / `.index` / `                                              |
| `Trading(source)`           | `Market().equity(sy                                                              |
| `Market(source)`            | `Analytics().valuation(                                                          |
| `TopStock(source)`          | `Insights().ra                                                                   |
| `Macro(source)`             | `Macro().economy()` / `.currency()` / `.com                                      |
| `CommodityPrice(source)`    | `Macro().co                                                                      |

---

## 📋 Chi Tiết Chuyển Đổi

### 1. Giá lịch sử & Giao dịch (`Quote` → `Market`)

**Cú pháp cũ:**
```python
# Qua lớp api — tham số source linh hoạt nhưng phải nhớ nguồn nào hỗ trợ gì
from vnstock_data.api import Quote

q = Quote(source="kbs", symbol="VIC")
df = q.history(start="2026-01-01", end="2026-03-01", interval="1D")
df_intraday = q.intraday(page_size=100)

# Hoặc import trực tiếp từ explorer
from vnstock_data.explorer.kbs import Quote
q = Quote(symbol="VIC")
df = q.history(start="2026-01-01", end="2026-03-01", interval="1D")
```

**Cú pháp mới (Unified UI):**
```python
from vnstock_data import Market

mkt = Market()
df = mkt.equity("VIC").ohlcv(start="2026-01-01", end="2026-03-01")
df_intraday = mkt.equity("VIC").trades()

# Với các loại tài sản khác — cùng cú pháp
df_index = mkt.index("VNINDEX").ohlcv(start="2026-01-01", end="2026-03-01")
df_futures = mkt.futures("VN30F2503").ohlcv(start="2026-01-01", end="2026-03-01")
df_etf = mkt.etf("E1VFVN30").ohlcv(start="2026-01-01", end="2026-03-01")
```

**Điểm khác biệt chính:**
- Không cần chỉ định `source` — Unified UI chọn nguồn tối ưu tự động (KBS cho giá lịch sử, VCI cho thống kê phiên, v.v.)
- Tên method chuẩn hóa: `history()` → `ohlcv()`, `intraday()` → `trades()`, `price_depth()` → `order_book()`
- Các tên cũ vẫn dùng được qua alias: `.history()` chuyển tiếp tới `.ohlcv()`

---

### 2. Thông tin công ty (`Company` → `Reference`)

**Cú pháp cũ:**
```python
from vnstock_data.api import Company

c = Company(source="vci", symbol="TCB")
df_profile = c.overview()
df_shareholders = c.shareholders()
df_officers = c.officers()
```

**Cú pháp mới:**
```python
from vnstock_data import Reference

ref = Reference()
df_profile = ref.company("TCB").info()
df_shareholders = ref.company("TCB").shareholders()
df_officers = ref.company("TCB").officers()
```

---

### 3. Báo cáo tài chính (`Finance` → `Fundamental`)

**Cú pháp cũ:**
```python
from vnstock_data.api import Finance

f = Finance(source="kbs", symbol="HPG")
income = f.income_statement(period="Y")
balance = f.balance_sheet(period="Q")
ratio = f.ratio()
```

**Cú pháp mới:**
```python
from vnstock_data import Fundamental

fun = Fundamental()
income = fun.equity("HPG").income_statement(period="Y")
balance = fun.equity("HPG").balance_sheet(period="Q")
ratio = fun.equity("HPG").ratio()
```

---

### 4. Danh sách niêm yết (`Listing` → `Reference`)

**Cú pháp cũ:**
```python
from vnstock_data.api import Listing

lst = Listing(source="vci")
symbols = lst.all_symbols()
industries = lst.industries_icb()
by_group = lst.symbols_by_group("VN30")
```

**Cú pháp mới:**
```python
from vnstock_data import Reference

ref = Reference()
symbols = ref.equity.list()
industries = ref.industry.list()
by_group = ref.equity.list_by_group("VN30")

# Các tính năng mới không có ở lớp cũ
etf_list = ref.etf.list()
bond_list = ref.bond.list()
events = ref.events.calendar(start="2026-03-01", end="2026-03-31")
search = ref.search.symbol("Bitcoin")  # Tìm kiếm toàn cầu
```

---

### 5. Định giá thị trường (`Market` → `Analytics`)

**Cú pháp cũ:**
```python
from vnstock_data.api import Market

m = Market(source="vnd")
pe = m.pe(duration="5Y")
pb = m.pb(duration="5Y")
```

**Cú pháp mới:**
```python
from vnstock_data import Analytics

ana = Analytics()
pe = ana.valuation("VNINDEX").pe(duration="5Y")
pb = ana.valuation("VNINDEX").pb(duration="5Y")
```

---

### 6. Xếp hạng cổ phiếu (`TopStock` → `Insights`)

**Cú pháp cũ:**
```python
from vnstock_data.api import TopStock

ts = TopStock(source="vnd")
gainer = ts.gainer()
loser = ts.loser()
```

**Cú pháp mới:**
```python
from vnstock_data import Insights

ins = Insights()
gainer = ins.ranking().gainer()
loser = ins.ranking().loser()
```

---

### 7. Dữ liệu vĩ mô (`Macro` → `Macro` domain mới)

**Cú pháp cũ:**
```python
from vnstock_data.api import Macro

m = Macro(source="mbk")
gdp = m.gdp()
cpi = m.cpi()
exchange = m.exchange_rate()
interest = m.interest_rate(length=90)
```

**Cú pháp mới:**
```python
from vnstock_data import Macro

mac = Macro()
gdp = mac.economy().gdp(period="quarter")
cpi = mac.economy().cpi(period="quarter")
exchange = mac.currency().exchange_rate()
interest = mac.currency().interest_rate(length=90)
```

---

### 8. Giá hàng hóa (`CommodityPrice` → `Macro`)

**Cú pháp cũ:**
```python
from vnstock_data.api import CommodityPrice

cp = CommodityPrice(source="spl")
gold = cp.gold_vn()
oil = cp.oil_crude()
```

**Cú pháp mới:**
```python
from vnstock_data import Macro

mac = Macro()
gold = mac.commodity().gold(market="VN")
oil = mac.commodity().oil(product="crude")
```

---

## ⚡ Có gì khác khi không dùng tham số `source`?

### Lớp API cũ

Hệ thống lớp `vnstock_data.api` cho phép chỉ định `source` để lựa chọn nguồn dữ liệu:

```python
# Chọn nguồn VCI
q = Quote(source="vci", symbol="VIC")

# Chọn nguồn KBS
q = Quote(source="kbs", symbol="VIC")
```

Ưu điểm: linh hoạt chuyển nguồn khi gặp sự cố với một nguồn cụ thể.

Nhược điểm: phải nhớ mỗi nguồn hỗ trợ những method nào, mỗi cặp `source + method` có thể trả về kết quả khác nhau.

### Unified UI

Unified UI **không yêu cầu** chỉ định `source`. Registry đã cấu hình sẵn nguồn dữ liệu tối ưu cho từng method:

```python
# Hệ thống tự chọn nguồn phù hợp nhất
mkt = Market()
df = mkt.equity("VIC").ohlcv(...)     # → KBS (tốt nhất cho giá lịch sử)
df = mkt.equity("VIC").session_stats() # → VCI (tốt nhất cho thống kê phiên)
```

**Khi nào cần quay lại dùng lớp API trực tiếp?**
- Khi cần lựa chọn nguồn cụ thể do yêu cầu đặc thù
- Khi cần truy cập tính năng nâng cao của nguồn cụ thể (ví dụ: định dạng xuất BCTC kiểu Excel từ Mirae Asset)
- Khi gỡ lỗi hoặc so sánh dữ liệu giữa các nguồn

```python
# Trường hợp cần dùng trực tiếp explorer
from vnstock_data.explorer.mas import Finance
f = Finance(symbol="HPG")
df = f.income_statement(period="Y")  # Định dạng Excel-style của MAS
```

---

## 🏗️ Hợp nhất vnstock và vnstock_data

Unified UI cũng là cầu nối giữa hai phiên bản:

| Đặc điểm            | `vnstock` (cộng đồng) | `vnstock_data` (gói tài trợ) |
| -------------------- | ---------------------- | ---------------------------- |
| Giá               | Miễn phí              | Tài trợ                     |
| Nguồn dữ liệu     | VCI, VND               | VCI, KBS, MAS, MBK, SPL, MSN |
| Phạm vi             | Cổ phiếu Việt Nam      | Đa nguồn + quốc tế + vĩ mô  |
| Giao diện           | **Unified UI** ✅       | **Unified UI** ✅             |

Khi chuyển đổi giữa hai phiên bản, code Unified UI **không cần thay đổi**. Sự khác biệt chỉ nằm ở tầng registry nội bộ — nguồn dữ liệu nào khả dụng sẽ tự động được sử dụng.

---

## ⏰ Lộ Trình Ngừng Hỗ Trợ

| Tính năng cũ | Thay thế bằng | Hạn cuối |
|---|---|---|
| `Macro().gdp()`, `Macro().cpi()`, ... | `Macro().economy().gdp()`, ... | 31/8/2026 |
| `Macro().exchange_rate()`, `Macro().interest_rate()` | `Macro().currency().exchange_rate()`, ... | 31/8/2026 |
| `Reference().derivatives()` | `Reference().futures()` / `.warrant()` | 31/8/2026 |
| `Market().pe()`, `.pb()`, `.evaluation()` | `Analytics().valuation(index).pe()`, ... | 31/8/2026 |

Trước khi ngừng hỗ trợ, tất cả cách gọi cũ sẽ hiển thị **cảnh báo song ngữ** (Việt + Anh) và tự động chuyển tiếp sang method mới.

---

## 🚦 Tóm Tắt

1. **Import mới**: `from vnstock_data import Reference, Market, Fundamental, Analytics, Insights, Macro`
2. **Không cần `source`**: Unified UI tự chọn nguồn tối ưu
3. **Cùng cú pháp**: Chaining API thống nhất cho mọi loại dữ liệu
4. **Tra cứu**: `show_api()` + `show_doc()` thay cho đọc source code
5. **Chuyển đổi phiên bản**: Code Unified UI tương thích cả `vnstock` và `vnstock_data`
