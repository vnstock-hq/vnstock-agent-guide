# Migration Guide - Chuyển Đổi từ TCBS sang KBS/VCI

## 🚨 Thông Báo Quan Trọng

**TCBS đã được deprecated từ phiên bản 3.4.0 và sẽ bị loại bỏ hoàn toàn trong phiên bản 3.5.0 (tháng 3/2026)**

Hướng dẫn này sẽ giúp bạn chuyển đổi code từ TCBS sang các nguồn dữ liệu thay thế được khuyến nghị: **KBS** (mới) hoặc **VCI** (ổn định).

---

## 📋 vnstock vs vnstock_data - Chọn Thư Viện Phù Hợp

### 🆓 vnstock (Miễn Phí)

- **Đối tượng**: Người dùng khách, người dùng miễn phí
- **API Key**: Không cần hoặc có API key miễn phí
- **Nguồn dữ liệu**: KBS, VCI (hạn chế)
- **Đặc điểm**:
    - Miễn phí sử dụng
    - Có rate limits
    - Nguồn dữ liệu giới hạn
    - Phù hợp học tập và research cá nhân

### 💎 vnstock_data (Sponsor)

- **Đối tượng**: Người dùng sponsor (trả phí)
- **API Key**: Cần API key và tài khoản đã tham gia [gói tài trợ Vnstock](https://vnstocks.com/insiders-program#tiers).
- **Nguồn dữ liệu**: Tất cả nguồn (VCI, KBS - sẽ bổ sung, VND, MAS, CafeF, FMarket, MBK, SPL)
- **Đặc điểm**:
    - Dải dữ liệu rộng hơn nhiều
    - Tăng mức độ rate limits ít nhất gấp 3 lần và tăng tốc độ tải dữ liệu
    - Nguồn dữ liệu đa dạng, dễ dàng chuyển đổi khi một nguồn gặp sự cố
    - Phù hợp phân tích và ứng dụng trong đầu tư chuyên nghiệp, tạo app/website

### 🔄 Migration Path

```python
# ✅ vnstock (Miễn phí)
from vnstock import Quote, Finance
quote = Quote(source="vci", symbol="VCB")  # hoặc source="kbs"

# ✅ vnstock_data (Sponsor) - Chuyển đổi dễ dàng
from vnstock_data import Quote, Finance
quote = Quote(source="vci", symbol="VCB")  # cùng syntax, nhiều nguồn hơn
```

**Lợi ích của vnstock_data:**

- Cú pháp giống hệt vnstock
- Hỗ trợ nhiều nguồn dữ liệu hơn (VND, MAS, CafeF, v.v.)
- Dữ liệu phong phú và chính xác hơn
- Tối ưu cho người dùng tài trợ dự án

---

## 📋 Tóm Tắt Thay Đổi

| Chức năng      | TCBS (Deprecated)                 | vnstock (Miễn Phí) | vnstock_data (Sponsor)         |
| -------------- | --------------------------------- | ------------------ | ------------------------------ |
| Quote Data     | ❌ ngưng hoạt động do api thay đổi | ✅ (KBS, VCI)       | ✅ (VCI, VND, MAS, CafeF, v.v.) |
| Company Data   | ❌ ngưng hoạt động do api thay đổi | ✅ (KBS, VCI)       | ✅ (VCI, VND, MAS, v.v.)        |
| Financial Data | ❌ ngưng hoạt động do api thay đổi | ✅ (KBS, VCI)       | ✅ (VCI, VND, MAS, v.v.)        |
| Trading Data   | ❌ ngưng hoạt động do api thay đổi | ✅ (KBS, VCI)       | ✅ (VCI, VND, MAS, v.v.)        |
| Listing Data   | ❌ ngưng hoạt động do api thay đổi | ✅ (KBS, VCI)       | ✅ (VCI, VND, MAS, v.v.)        |
| Macro Data     | ❌ ngưng hoạt động do api thay đổi | ❌                  | ✅ (vnstock_data độc quyền)     |
| Commodity Data | ❌ ngưng hoạt động do api thay đổi | ❌                  | ✅ (vnstock_data độc quyền)     |
| Fund Data      | ❌ ngưng hoạt động do api thay đổi | ❌                  | ✅ (vnstock_data độc quyền)     |
| Screener       | ❌ ngưng hoạt động do api thay đổi | ❌                  | ❌                              |

---

## 🔄 Migration Steps

### Step 1: Update Source Parameter

**Before (TCBS):**

```python
from vnstock import Quote, Company, Finance, Listing

# ❌ Deprecated
quote = Quote(source="tcbs", symbol="VCI")
company = Company(source="tcbs", symbol="VCI")
finance = Finance(source="tcbs", symbol="VCI")
listing = Listing(source="tcbs")
```

**After (KBS - Recommended):**

```python
from vnstock import Quote, Company, Finance, Listing

# ✅ Recommended (mới trong v3.4.0)
quote = Quote(source="kbs", symbol="VCI")
company = Company(source="kbs", symbol="VCI")
finance = Finance(source="kbs", symbol="VCI")
listing = Listing(source="kbs")
```

**After (VCI - Alternative):**

```python
from vnstock import Quote, Company, Finance, Listing

# ✅ Alternative (ổn định)
quote = Quote(source="vci", symbol="VCI")
company = Company(source="vci", symbol="VCI")
finance = Finance(source="vci", symbol="VCI")
listing = Listing(source="vci")
```

**After (vnstock_data - Sponsor Upgrade):**

```python
# ✅✅ Chuyển lên vnstock_data (dễ dàng nhất)
from vnstock_data import Quote, Company, Finance, Listing

# Cùng syntax, nhiều nguồn hơn
quote = Quote(source="vci", symbol="VCI")  # VCI, VND, MAS, CafeF, v.v.
company = Company(source="vci", symbol="VCI")
finance = Finance(source="vci", symbol="VCI")
listing = Listing(source="vci")

# Hoặc dùng các nguồn khác không có trong vnstock miễn phí
quote_vnd = Quote(source="vnd", symbol="VCB")  # VND Data
quote_mas = Quote(source="mas", symbol="VCB")  # MAS Data
```

### Step 2: Choose Your Library

**Option A: vnstock (Miễn Phí)**

```python
from vnstock import Quote

# Hạn chế: chỉ KBS và VCI
quote = Quote(source="vci", symbol="VCB")
df = quote.history(start="2024-01-01", end="2024-12-31")
```

**Option B: vnstock_data (Sponsor)**

```python
from vnstock_data import Quote

# Nhiều nguồn hơn, dữ liệu phong phú hơn
quote = Quote(source="vnd", symbol="VCB")  # Nguồn VND (chỉ có trong vnstock_data)
df = quote.history(start="2024-01-01", end="2024-12-31")

# Dữ liệu macro (chỉ có trong vnstock_data)
from vnstock_data import Macro
macro = Macro()
gdp_data = macro.gdp()
```

### Step 3: Update DataSource Enum

**Before:**

```python
from vnstock.core.types import DataSource

# ❌ Deprecated
quote = Quote(source=DataSource.TCBS, symbol="VCI")
```

**After:**

```python
from vnstock.core.types import DataSource

# ✅ Recommended
quote = Quote(source=DataSource.KBS, symbol="VCI")

# ✅ Alternative
quote = Quote(source=DataSource.VCI, symbol="VCI")
```

---

## 📊 So Sánh Tính Năng

### Quote API

| Feature             | TCBS | KBS | VCI |
| ------------------- | ---- | --- | --- |
| `history()`         | ✅    | ✅   | ✅   |
| `intraday()`        | ✅    | ✅   | ✅   |
| `price_depth()`     | ✅    | ✅   | ✅   |
| Real-time data      | ✅    | ✅   | ✅   |
| Multiple timeframes | ✅    | ✅   | ✅   |

### Company API

| Feature          | TCBS | KBS | VCI |
| ---------------- | ---- | --- | --- |
| `overview()`     | ✅   | ✅  | ✅  |
| `officers()`     | ✅   | ✅  | ✅  |
| `shareholders()` | ✅   | ✅  | ✅  |
| `subsidiaries()` | ✅   | ✅  | ✅  |
| `news()`         | ✅   | ✅  | ✅  |
| `ratio_summary()`| ❌   | ❌  | ✅  |
| `capital_history()`| ❌  | ✅  | ❌  |

### Financial API

| Feature              | TCBS | KBS | VCI |
| -------------------- | ---- | --- | --- |
| `balance_sheet()`    | ✅   | ✅  | ✅  |
| `income_statement()` | ✅   | ✅  | ✅  |
| `cash_flow()`        | ✅   | ✅  | ✅  |
| `ratio()`            | ✅   | ✅  | ✅  |
| Quarterly/Yearly     | ✅   | ✅  | ✅  |

### Trading API

| Feature          | TCBS | KBS | VCI |
| ---------------- | ---- | --- | --- |
| `price_board()`  | ✅   | ✅  | ✅  |
| `price_history()`| ❌   | ❌  | ✅  |
| `trading_stats()`| ❌   | ❌  | ✅  |
| `side_stats()`   | ❌   | ❌  | ✅  |

### Listing API

| Feature             | TCBS | KBS | VCI |
| ------------------- | ---- | --- | --- |
| `all_symbols()`     | ✅   | ✅  | ✅  |
| `symbols_by_exchange()`| ❌ | ❌  | ✅  |
| `government_bonds()`| ❌   | ❌  | ✅  |
| `indices()`         | ❌   | ❌  | ✅  |

---

## 🔧 Code Examples

### Example 1: Lấy Giá Lịch Sử

**TCBS (Deprecated):**

```python
from vnstock import Quote
from vnstock.core.types import TimeFrame

quote = Quote(source="tcbs", symbol="VCI")
df = quote.history(
    start_date="2024-01-01",
    end_date="2024-12-31",
    resolution=TimeFrame.DAILY
)
```

**KBS (Recommended):**

```python
from vnstock import Quote
from vnstock.core.types import TimeFrame

quote = Quote(source="kbs", symbol="VCI")
df = quote.history(
    start_date="2024-01-01",
    end_date="2024-12-31",
    resolution=TimeFrame.DAILY
)
```

**VCI (Alternative):**

```python
from vnstock import Quote
from vnstock.core.types import TimeFrame

quote = Quote(source="vci", symbol="VCI")
df = quote.history(
    start_date="2024-01-01",
    end_date="2024-12-31",
    resolution=TimeFrame.DAILY
)
```

### Example 2: Lấy Thông Tin Công Ty

**TCBS (Deprecated):**

```python
from vnstock import Company

company = Company(source="tcbs", symbol="VCI")
overview = company.overview()
shareholders = company.shareholders()
officers = company.officers()
```

**KBS (Recommended):**

```python
from vnstock import Company

company = Company(source="kbs", symbol="VCI")
overview = company.overview()
shareholders = company.shareholders()
officers = company.officers()
```

### Example 3: Lấy Báo Cáo Tài Chính

**TCBS (Deprecated):**

```python
from vnstock import Finance

finance = Finance(source="tcbs", symbol="VCI")
balance_sheet = finance.balance_sheet(period="quarter")
income_statement = finance.income_statement(period="quarter")
cash_flow = finance.cash_flow(period="quarter")
ratios = finance.ratios()
```

**KBS (Recommended):**

```python
from vnstock import Finance

finance = Finance(source="kbs", symbol="VCI")
balance_sheet = finance.balance_sheet(period="quarter")
income_statement = finance.income_statement(period="quarter")
cash_flow = finance.cash_flow(period="quarter")
ratios = finance.ratios()
```

---

## ⚠️ Lưu Ý Quan Trọng

### 1. Screener API

- **TCBS Screener sẽ không có thay thế trực tiếp**
- Sử dụng các API lọc của VCI/KBS thay thế
- Xem thêm tại [09-Screener API](09-screener-api.md)

### 2. Data Format

- KBS và VCI có thể có định dạng dữ liệu hơi khác nhau
- Kiểm tra và điều chỉnh code xử lý dữ liệu nếu cần

### 3. Rate Limits

- Mỗi nguồn có rate limits khác nhau
- KBS có thể có rate limits tốt hơn so với TCBS

### 4. Error Handling

- KBS và VCI có thể trả về lỗi khác nhau
- Cập nhật error handling code cho phù hợp

---

## 🛠️ Best Practices

### 1. Sử dụng Environment Variable

```python
import os
from vnstock import Quote

# Flexible source selection
DATA_SOURCE = os.getenv('VNSTOCK_SOURCE', 'kbs')  # Default to KBS

quote = Quote(source=DATA_SOURCE, symbol="VCI")
```

### 2. Fallback Mechanism

```python
from vnstock import Quote
from vnstock.core.utils.logger import get_logger

logger = get_logger(__name__)

def get_quote_with_fallback(symbol):
    """Try KBS first, fallback to VCI"""
    try:
        return Quote(source="kbs", symbol=symbol)
    except Exception as e:
        logger.warning(f"KBS failed for {symbol}: {e}, trying VCI")
        return Quote(source="vci", symbol=symbol)
```

### 3. Validation

```python
from vnstock.core.types import DataSource

def validate_source(source):
    """Validate data source"""
    if source == DataSource.TCBS:
        raise ValueError("TCBS is deprecated. Use KBS or VCI instead.")
    return source
```

---

## � Nâng Cấp Lên vnstock_data - Lợi Ích Vượt Trội

### 🚀 Tại Sao Nên Nâng Cấp?

**1. Dải Dữ Liệu Rộng Hơn Gấp Bội**

```python
# vnstock (miễn phí) - chỉ 2 nguồn
from vnstock import Quote
quote = Quote(source="vci", symbol="VCB")  # VCI
quote = Quote(source="kbs", symbol="VCB")  # KBS

# vnstock_data (sponsor) - 7+ nguồn
from vnstock_data import Quote
quote = Quote(source="vci", symbol="VCB")  # VCI
quote = Quote(source="vnd", symbol="VCB")  # VND Data
quote = Quote(source="mas", symbol="VCB")  # MAS Data
quote = Quote(source="cafeF", symbol="VCB")  # CafeF
quote = Quote(source="fmarket", symbol="VCB")  # FMarket
quote = Quote(source="mbk", symbol="VCB")  # MBK
quote = Quote(source="spl", symbol="VCB")  # SPL
```

**2. Dữ Liệu Độc Quyền**

```python
# Chỉ có trong vnstock_data
from vnstock_data import Macro, CommodityPrice, Fund

# Kinh tế vĩ mô
macro = Macro()
gdp = macro.gdp()
cpi = macro.cpi()
exchange_rate = macro.exchange_rate()

# Hàng hóa
commodity = CommodityPrice()
gold_price = commodity.gold()
oil_price = commodity.oil()
pork_price = commodity.pork()

# Quỹ đầu tư
fund = Fund()
etf_list = fund.etf_list()
fund_nav = fund.nav()
```

**3. Không Rate Limits**

- **vnstock**: Có rate limits, có thể bị block khi request nhiều
- **vnstock_data**: Rate limits rất cao hoặc không có, phù hợp trading tần suất cao

**4. Dữ Liệu Chính Thức & Đầy Đủ**

- Nguồn dữ liệu từ các nhà cung cấp chính thức
- Coverage tốt hơn cho các chứng chỉ quỹ, trái phiếu, chứng quyền
- Data quality cao và consistency tốt hơn

### 🔄 Chuyển Đổi Dễ Dàng

**Chỉ cần đổi import:**

```python
# ❌ vnstock
from vnstock import Quote, Finance, Trading

# ✅ vnstock_data
from vnstock_data import Quote, Finance, Trading

# Code còn lại giữ nguyên!
quote = Quote(source="vci", symbol="VCB")
finance = Finance(source="vci", symbol="VCB")
trading = Trading(source="vci", symbol="VCB")
```

### 📈 So Sánh Chi Tiết

| Tiêu Chí          | vnstock (Miễn Phí)    | vnstock_data (Sponsor)           |
| ----------------- | --------------------- | -------------------------------- |
| **Nguồn dữ liệu** | 2 (KBS, VCI)          | 7+ (VCI, VND, MAS, CafeF, v.v.)  |
| **Rate limits**   | Có                    | Không/Rất cao                    |
| **Dữ liệu macro** | ❌                    | ✅                               |
| **Hàng hóa**      | ❌                    | ✅                               |
| **Quỹ ETF**       | ❌                    | ✅                               |
| **Chi phí**       | Miễn phí              | Trả phí                          |
| **Cú pháp**       | `from vnstock import` | `from vnstock_data import`       |
| **Phù hợp**       | Học tập, research     | Trading, phân tích chuyên nghiệp |

### 🎯 Khi Nào Nên Nâng Cấp?

**Nâng cấp lên vnstock_data khi bạn:**

- Cần dữ liệu từ nhiều nguồn khác nhau
- Muốn dữ liệu kinh tế vĩ mô
- Trading tần suất cao (bị rate limits)
- Cần dữ liệu hàng hóa, quỹ đầu tư
- Muốn data quality và consistency tốt nhất
- Sẵn sàng trả phí cho dịch vụ tốt hơn

**Tiếp tục dùng vnstock khi bạn:**

- Mới học về chứng khoán
- Chỉ cần dữ liệu cơ bản
- Research cá nhân không thường xuyên
- Ngân sách hạn chế

---

## �📅 Timeline

| Version | Status     | Action                          |
| ------- | ---------- | ------------------------------- |
| 3.4.0   | Current    | TCBS deprecated, KBS introduced |
| 3.5.0   | March 2026 | TCBS removed completely         |

---

## 🆘 Help & Support

### Common Issues

1. **DeprecatedWarning**

   ```
   UserWarning: Provider 'TCBS' is deprecated since version 3.4.0 
   and will be removed in version 3.5.0. Use 'VCI' provider instead.
   ```

   **Solution:** Chuyển sang KBS hoặc VCI
1. **ImportError**

   ```
   ImportError: cannot import name 'TCBS' from DataSource
   ```

   **Solution:** Sử dụng `DataSource.KBS` hoặc `DataSource.VCI`
1. **Data Format Differences**

   - Kiểm tra column names
   - Validate data types
   - Update data processing logic

### Getting Help

- **GitHub Issues**: [vnstock issues](https://github.com/thinh-vu/vnstock/issues)
- **Documentation**: [VNStock Docs](https://vnstocks.com/docs)
- **Community**: [VNStock Community](https://community.vnstocks.com)

---

## ✅ Migration Checklist

- [ ] Thay thế `source="tcbs"` thành `source="kbs"` hoặc `source="vci"`
- [ ] Cập nhật `DataSource.TCBS` thành `DataSource.KBS` hoặc `DataSource.VCI`
- [ ] Test lại tất cả các function
- [ ] Kiểm tra format dữ liệu
- [ ] Update error handling
- [ ] Update documentation
- [ ] Test trong production environment

---

**Last Updated**: 2024-12-17  

**Version**: 3.4.0  

**Status**: Migration Required