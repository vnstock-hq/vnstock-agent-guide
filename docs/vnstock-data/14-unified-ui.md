# Unified UI - Giao Diện Hợp Nhất (Unified Financial Data Platform)

> **Áp dụng từ ngày 11/3/2026**. Đây là giao diện người dùng thế hệ mới nhất của `vnstock_data`, thay thế dần cách gọi hàm trực tiếp từ các lớp API/Explorer cũ. Cách gọi hàm cũ vẫn hoạt động nhưng sẽ dần chuyển đổi sang phương thức mới với trải nghiệm tốt hơn, tiện lợi, và toàn vẹn hơn.

Thư mục `vnstock_data` cung cấp một cấu trúc giao diện cấp cao gom nhóm tất cả các tính năng dữ liệu thành từng **cụm ngữ nghĩa** để dễ dàng tra cứu và gọi lệnh.

Các lớp dữ liệu được phân chia thành **7 nhóm chính**: `Reference`, `Market`, `Fundamental`, `Analytics`, `Alternative` (đang phát triển), `Macro`, và `Insights`.

---

## 🔍 Tra Cứu API: `show_api()` & `show_doc()`

Trước khi sử dụng Unified UI, bạn (hoặc AI Agent) có thể dùng 2 hàm tiện ích `show_api()` và `show_doc()` để **khám phá cấu trúc API** và **đọc tài liệu hướng dẫn** cho từng thành phần mà không cần đọc source code.

### Import

```python
from vnstock_data import show_api, show_doc
```

### `show_api()` — Hiển thị cây cấu trúc API

Hiển thị toàn bộ cây cấu trúc tính năng có sẵn trong Unified UI.

**Cách sử dụng:**

```python
# Hiển thị toàn bộ 7 nhóm (đầy đủ nhất)
show_api()

# Chỉ hiển thị endpoint methods (ẩn navigation)
show_api(show_navigation=False)

# Chỉ hiển thị 1 nhóm cụ thể
from vnstock_data import Reference, Market
show_api(Reference())    # Cây của Reference layer
show_api(Market())       # Cây của Market layer
show_api('Analytics')    # Truyền tên layer dạng chuỗi cũng được
```

**Kết quả mẫu (rút gọn):**

```
API STRUCTURE TREE - VNSTOCK_DATA (Unified UI Endpoints)
vnstock_data
├── Reference
│   ├── bond
│   │   ├── list()
│   ├── company()
│   │   ├── info() [VCI] -> DataFrame
│   │   ├── shareholders() [VCI] -> DataFrame
│   ├── equity
│   │   ├── list() [VCI] -> DataFrame
│   ├── etf
│   │   ├── list() [KBS] -> DataFrame
│   ├── events
│   │   ├── calendar() [VCI] -> DataFrame
│   │   ├── market() -> DataFrame
│   ├── search
│   │   ├── symbol() [MSN] -> DataFrame
│   ├── futures()
│   │   ├── info() [KBS] -> DataFrame
│   │   ├── list() [VCI] -> DataFrame
│   └── warrant()
│       ├── info() [KBS] -> DataFrame
│       ├── list() [VCI] -> DataFrame
├── Market
│   ├── equity()
│   │   ├── ohlcv() [KBS] -> DataFrame
│   │   ├── trades() [KBS] -> DataFrame
│   │   ├── quote() [KBS] -> DataFrame
│   ...
├── Fundamental
├── Analytics
├── Macro
└── Insights
```

**Giải thích output:**

- `[VCI]`, `[KBS]`, `[MSN]`: Nguồn dữ liệu (data source)
- `-> DataFrame`: Kiểu dữ liệu trả về
- `# ...`: Mô tả ngắn từ docstring của method
- Methods có `()` sau tên (ví dụ `company()`, `equity()`) là **hàm điều hướng** nhận tham số
- Methods không có `()` (ví dụ `bond`, `equity`, `etf`) là **thuộc tính** truy cập trực tiếp

### `show_doc()` — Đọc tài liệu mô tả

Hiển thị tài liệu mô tả (docstring) đầy đủ của bất kỳ class hoặc method nào. Hữu ích khi cần biết chi tiết tham số, kiểu dữ liệu trả về, và cách sử dụng.

**Cách sử dụng:**

```python
from vnstock_data import show_doc, Reference, Market, Macro

# Xem docstring của một layer class
show_doc(Reference)
# Output:
# Signature: Reference()
# Reference Data Layer (Layer 1).
# Provides access to static/master data for various domains.

# Xem docstring của một method cụ thể
show_doc(Reference.company)
show_doc(Market.equity)

# Truyền tên dạng chuỗi
show_doc('Macro')
show_doc('Market')
```

### 💡 Khi nào dùng `show_api` vs `show_doc`?

| Tình huống                                   | Dùng hàm                                                             |
| -------------------------------------------- | -------------------------------------------------------------------- |
| Muốn biết có những methods nào               | `show_api()` hoặc `show_api(layer)`                                  |
| Muốn biết parameters và cách gọi             | `show_doc(method)`                                                   |
| AI Agent cần inspect API trước khi viết code | `show_api(show_navigation=False)` rồi `show_doc()` cho method cụ thể |
| Muốn xem cây tính năng đầy đủ                | `show_api()` (mặc định `show_navigation=True`)                       |

---

## 📚 Tổng Quan Kiến Trúc

### Các Nhóm Tính Năng Chính (7 Nhóm)

| Nhóm            | Mô Tả                      | Mục Đích                                                                            |
| --------------- | -------------------------- | ----------------------------------------------------------------------------------- |
| **Reference**   | Dữ liệu tham chiếu         | Thông tin công ty, danh sách cổ phiếu, chỉ số, ETF, trái phiếu, sự kiện, tìm kiếm |
| **Market**      | Dữ liệu giao dịch          | Giá OHLCV, thanh khoản, sổ lệnh, dòng tiền nước ngoài/tự doanh                     |
| **Fundamental** | Dữ liệu cơ bản             | BCTC: Thu nhập, Cân đối kế toán, Dòng tiền, Tỷ số tài chính, Thuyết minh           |
| **Analytics**   | Phân tích định giá          | P/E, P/B, đánh giá định giá toàn thị trường                                        |
| **Alternative** | Dữ liệu thay thế (🔜)      | Đang phát triển — sẽ bổ sung trong phiên bản tiếp theo                               |
| **Macro**       | Dữ liệu vĩ mô              | GDP, CPI, FDI, tỷ giá, lãi suất, giá hàng hóa                                      |
| **Insights**    | Phân tích chuyên sâu        | Xếp hạng top cổ phiếu, bộ lọc                                                       |

### Cấu Trúc Phân Cấp

```
vnstock_data
├── Reference (Layer 1)
│   ├── .company(symbol)       # Thông tin công ty
│   ├── .equity                # Danh sách cổ phiếu (property)
│   ├── .index                 # Danh sách chỉ số (property)
│   ├── .industry              # Ngành kinh tế (property)
│   ├── .fund                  # Quỹ đầu tư mở (property)
│   ├── .etf                   # Quỹ ETF (property)
│   ├── .bond                  # Trái phiếu (property)
│   ├── .events                # Sự kiện thị trường (property)
│   ├── .search                # Tìm kiếm toàn cầu (property)
│   ├── .futures(symbol)       # Hợp đồng tương lai
│   └── .warrant(symbol)       # Chứng quyền
│
├── Market (Layer 2)
│   ├── .equity(symbol)        # Thị trường cổ phiếu
│   ├── .index(symbol)         # Thị trường chỉ số
│   ├── .futures(symbol)       # Thị trường hợp đồng tương lai
│   ├── .warrant(symbol)       # Thị trường chứng quyền
│   ├── .etf(symbol)           # Thị trường ETF
│   ├── .fund(symbol)          # Thị trường quỹ đầu tư mở
│   ├── .crypto(symbol)        # 🧪 Tiền mã hoá (đang hoàn thiện)
│   ├── .forex(symbol)         # 🧪 Ngoại hối (đang hoàn thiện)
│   ├── .commodity(symbol)     # 🧪 Hàng hoá quốc tế (đang hoàn thiện)
│   └── .quote(symbols_list)   # Bảng giá nhiều mã
│
├── Fundamental (Layer 3)
│   └── .equity(symbol)        # Báo cáo tài chính
│
├── Alternative (Layer 4 — 🔜 đang phát triển)
│
|
├── Macro (Layer 5)
│   ├── .economy()             # Dữ liệu kinh tế
│   ├── .currency()            # Tỷ giá & Lãi suất
│   └── .commodity()           # Hàng hóa nội địa & quốc tế (Macro)
│
├── Insights (Layer 6)
│   ├── .ranking()             # Xếp hạng top cổ phiếu
│   └── .screener()            # Bộ lọc chứng khoán
│
└── Analytics (Layer 7)
|   └── .valuation(index)      # Định giá thị trường (P/E, P/B)
|
└── Retail (Layer 8 🔜 đang phát triển)           # Dữ liệu thị trường bán lẻ và tiêu dùng

```

---

## 🚀 Khởi Tạo & Cách Sử Dụng

### Import

```python
from vnstock_data import Reference, Market, Fundamental, Analytics, Insights, Macro
from vnstock_data import show_api, show_doc  # Tra cứu cấu trúc tính năng
```

### Khởi Tạo

```python
ref = Reference()
mkt = Market()
fun = Fundamental()
ana = Analytics()
ins = Insights()
mac = Macro()
```

### Truy xuất dữ liệu (Chaining API)

```python
# Reference: Lấy thông tin công ty
df_company = ref.company("TCB").info()

# Market: Lấy lịch sử giá
df_history = mkt.equity("VIC").ohlcv(
    start="2026-02-01", 
    end="2026-03-01"
)

# Fundamental: Lấy báo cáo tài chính
df_income = fun.equity("HPG").income_statement(period="Y")

# Analytics: Lấy P/E toàn thị trường
df_pe = ana.valuation("VNINDEX").pe(duration="1Y")

# Insights: Lấy top gainer
df_gainers = ins.ranking().gainer()

# Macro: Lấy dữ liệu kinh tế
df_gdp = mac.economy().gdp(period="quarter")
df_interest = mac.currency().interest_rate(length=90)
df_gold = mac.commodity().gold(market="VN")
```

---

## 🎯 Quick Start - Ví Dụ Đầy Đủ

```python
from vnstock_data import Reference, Market, Fundamental, Analytics, Insights, Macro

# === REFERENCE: Dữ liệu tham chiếu ===
ref = Reference()
companies = ref.company("TCB").info()
equity_list = ref.equity.list()
etf_list = ref.etf.list()

# Futures & Warrant (truy cập trực tiếp, không qua derivatives)
futures_list = ref.futures().list()
futures_info = ref.futures("VN30F2503").info()
warrant_list = ref.warrant().list()

# Tìm kiếm toàn cầu
search_results = ref.search.symbol("VNM")

# Sự kiện thị trường
events = ref.events.calendar(start="2026-03-01", end="2026-03-31")

# === MARKET: Dữ liệu giao dịch ===
mkt = Market()
price_history = mkt.equity("VIC").ohlcv(start="2026-02-01", end="2026-03-01")
quote = mkt.equity("VIC").quote()

# Futures & Warrant market data (truy cập trực tiếp)
futures_price = mkt.futures("VN30F2503").ohlcv(start="2026-02-01", end="2026-03-01")
warrant_price = mkt.warrant("CACB2511").ohlcv(start="2026-02-01", end="2026-03-01")

# ETF market data
etf_price = mkt.etf("E1VFVN30").ohlcv(start="2026-02-01", end="2026-03-01")

# === FUNDAMENTAL: Báo cáo tài chính ===
fun = Fundamental()
income = fun.equity("HPG").income_statement(period="Y")
ratio = fun.equity("TCB").ratio()

# === ANALYTICS: Định giá ===
ana = Analytics()
pe_data = ana.valuation("VNINDEX").pe(duration="1Y")

# === INSIGHTS: Xếp hạng & Lọc ===
ins = Insights()
gainers = ins.ranking().gainer()
screener_data = ins.screener().filter()

# === MACRO: Kinh tế vĩ mô & Hàng hóa ===
mac = Macro()
gdp = mac.economy().gdp(period="quarter")
exchange = mac.currency().exchange_rate()
gold = mac.commodity().gold(market="VN")
```

---

## 📖 Tài Liệu Chi Tiết Theo Nhóm Tính Năng

Để tìm hiểu chi tiết từng nhóm tính năng:

| Layer              | Tài Liệu                                                        | Nội Dung Chính                                                                      |
| ------------------ | --------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **1: Reference**   | [01-reference-layer.md](./unified-ui/01-reference-layer.md)     | Company, Equity, Index, Industry, Fund, ETF, Bond, Events, Search, Futures, Warrant |
| **2: Market**      | [02-market-layer.md](./unified-ui/02-market-layer.md)           | Equity, Index, Futures, Warrant, ETF, Fund, Crypto 🧪, Forex 🧪, Commodity 🧪       |
| **3: Fundamental** | [03-fundamental-layer.md](./unified-ui/03-fundamental-layer.md) | Income statement, Balance sheet, Cash flow, Ratios, Note                            |
| **4: Analytics**   | [07-analytics-layer.md](./unified-ui/07-analytics-layer.md)                  | Định giá thị trường (P/E, P/B, Evaluation)                                          |
| **5: Alternative** | 🔜 (đang phát triển)                                            | Sẽ bổ sung trong phiên bản tiếp theo                                                |
| **6: Macro**       | [05-macro-layer.md](./unified-ui/05-macro-layer.md)             | Economy, Currency, Commodity (nội địa & quốc tế)                                    |
| **7: Insights**    | [06-insights-layer.md](./unified-ui/06-insights-layer.md)                    | Ranking (top movers), Screener (lọc chứng khoán)                                    |

---

## 🎯 Thực hành tốt

### 1️⃣ Sử Dụng `show_api()` Trước Khi Viết Code

```python
from vnstock_data import show_api, show_doc

# Bước 1: Xem cấu trúc tổng thể
show_api(show_navigation=False)

# Bước 2: Xem chi tiết method cần dùng
show_doc(Reference.company)
```

### 2️⃣ Sử Dụng Unified UI Thay Vì Gọi Trực Tiếp Explorer

```python
# ✅ RECOMMENDED - Sử dụng Unified UI
mac = Macro()
df = mac.economy().gdp(period="quarter")

# ❌ Không khuyến nghị — Gọi trực tiếp qua lớp API cũ
from vnstock_data.api.macro import Macro as LegacyMacro
m = LegacyMacro(source="mbk")
df = m.gdp()
```

### 3️⃣ Method Chaining

```python
# Chaining API cho phép linh hoạt
df_gdp = Macro().economy().gdp(period="quarter")
df_gainers = Insights().ranking().gainer()
df_history = Market().equity("VIC").ohlcv(
    start="2026-02-01", 
    end="2026-03-01"
)
```

### 4️⃣ Xử Lý Lỗi

```python
try:
    df = Reference().company("INVALID").info()
except ValueError as e:
    print(f"Lỗi: {e}")
except NotImplementedError as e:
    print(f"Phương thức không được hỗ trợ: {e}")
```

### 5️⃣ Truy Cập Futures & Warrant (Cú Pháp Mới)

```python
# ✅ RECOMMENDED: Truy cập trực tiếp
ref = Reference()
warrant = ref.warrant("CACB2511").info()
futures = ref.futures("VN30F2503").info()

mkt = Market()
futures_price = mkt.futures("VN30F2503").ohlcv(start="2026-02-01", end="2026-03-01")
```

---

## 🧪 Tính Năng Thử Nghiệm

Các nhóm sau đang trong giai đoạn phát triển và có thể chưa ổn định:

| Domain                       | Trạng Thái      | Ghi Chú                                       |
| ---------------------------- | --------------- | --------------------------------------------- |
| `Market().crypto(symbol)`    | 🧪 Experimental | Dữ liệu lịch sử qua MSN, chỉ hỗ trợ `ohlcv()` |
| `Market().forex(symbol)`     | 🧪 Experimental | Dữ liệu lịch sử qua MSN, chỉ hỗ trợ `ohlcv()` |
| `Market().commodity(symbol)` | 🧪 Experimental | Dữ liệu lịch sử qua MSN, chỉ hỗ trợ `ohlcv()` |

> **Lưu ý**: Các tính năng thử nghiệm này sử dụng nguồn dữ liệu MSN cung cấp dữ liệu thị trường quốc tế và chỉ hỗ trợ method `ohlcv()` cho dữ liệu lịch sử. Để tìm đúng mã symbol, dùng `Reference().search.symbol("tên_tài_sản")` để tra cứu `symbol_id`.

---
## 📖 Lưu Ý Quan Trọng

### 1. Tra Cứu Trước Khi Dùng

- Luôn dùng `show_api()` để xem cấu trúc trước khi viết code
- Dùng `show_doc(method)` để đọc parameters và return type

### 2. Hiệu Suất

- API UI được thiết kế cho **tính thuận tiện** hơn **tốc độ**
- Nếu xử lý bulk data, xem xét sử dụng API layer trực tiếp

### 3. Khả Dụng Phương Thức

- Không phải method nào cũng hỗ trợ bởi tất cả sources
- Dùng `show_api()` để xem danh sách methods được hỗ trợ

### 4. Backward Compatibility

- Các cách gọi hàm cũ (Legacy Macro, Market valuation, derivatives nesting) vẫn hoạt động cho đến **31/8/2026**
- Sẽ hiển thị cảnh báo ngừng hỗ trợ (song ngữ)
- Khuyến nghị chuyển sang cấu trúc mới — xem **[Hướng dẫn chuyển đổi](unified-ui/00-migration-guide.md)**

---

## 📞 Để Tìm Hiểu Thêm

- **Registry System:** `vnstock_data/ui/_registry.py`
- **Base Classes:** `vnstock_data/ui/_base.py`
- **Source Code:** `vnstock_data/ui/domains/`
- **Hàm tra cứu:** `vnstock_data/ui/helper.py` (`show_api`, `show_doc`)
- **Hướng dẫn chuyển đổi:** [00-migration-guide.md](unified-ui/00-migration-guide.md)

---

*Last Updated: March 11, 2026*  
*Status: Production Ready ✅*