# Layer 1: Reference Data (Dữ Liệu Tham Chiếu)

## 📌 Tổng Quan

**Reference Layer** cung cấp thông tin nền tảng, tĩnh về các sản phẩm tài chính - công ty, chỉ số, ngành, danh sách símbol, v.v. Đây là dữ liệu **không thay đổi thường xuyên** và được sử dụng để **lookup** hay **master data**.

## 🏗️ Cấu Trúc Domain

```python
Reference()
├── .company         # Thông tin công ty
├── .equity          # Danh sách cổ phiếu
├── .index           # Danh sách chỉ số
├── .industry        # Ngành kinh tế
├── .fund            # Quỹ đầu tư
└── .derivatives     # Chứng chỉ phái sinh
    ├── .warrant()   # Chứng quyền (nested)
    └── .futures()   # Hợp đồng tương lai (nested)
```

## 📋 Chi Tiết Các Domain

### 1. Company Domain (Thông Tin Công Ty)

**Source:** VCI (vci)  
**Registry Key:** `"company"`

#### Phương Thức

| Method | Tham Số | Mô Tả | Ví Dụ |
|--------|---------|-------|-------|
| `profile()` | `symbol` | Thông tin tổng quan công ty | `ref.company.profile("TCB")` |
| `shareholders()` | `symbol` | Danh sách cổ đông chính | `ref.company.shareholders("VIC")` |
| `officers()` | `symbol` | Danh sách quản lý cấp cao | `ref.company.officers("HPG")` |
| `subsidiaries()` | `symbol` | Danh sách công ty con | `ref.company.subsidiaries("VNM")` |
| `news()` | `symbol` | Tin tức công ty | `ref.company.news("TCB")` |
| `events()` | `symbol` | Sự kiện công ty | `ref.company.events("VIC")` |

#### Ví Dụ

```python
from vnstock_data import Reference

ref = Reference()

# Thông tin công ty
df_profile = ref.company.profile("TCB")
print(df_profile)
# Output: 
# {
#   'name': 'Techcombank',
#   'established': 1993,
#   'website': 'https://techcombank.com.vn',
#   'sector': 'Finance',
#   ...
# }

# Danh sách cổ đông lớn
df_shareholders = ref.company.shareholders("VIC")
print(df_shareholders[['name', 'ownership_percent']])

# Quản lý cấp cao
df_officers = ref.company.officers("HPG")
print(df_officers[['name', 'position']])
```

---

### 2. Equity Domain (Danh Sách Cổ Phiếu)

**Source:** VCI (vci)  
**Registry Key:** `"equity"`

#### Phương Thức

| Method | Tham Số | Mô Tả | Ví Dụ |
|--------|---------|-------|-------|
| `list()` | - | Toàn bộ danh sách cổ phiếu | `ref.equity.list()` |
| `by_group()` | `group_id` (opt) | Cổ phiếu theo nhóm | `ref.equity.by_group("BLUECHIP")` |
| `by_exchange()` | `exchange` (opt) | Cổ phiếu theo sàn | `ref.equity.by_exchange("HSX")` |

#### Ví Dụ

```python
from vnstock_data import Reference

ref = Reference()

# Tất cả síbol
all_symbols = ref.equity.list()
print(f"Total symbols: {len(all_symbols)}")

# Cổ phiếu blue chip
blue_chips = ref.equity.by_group("BLUECHIP")
print(blue_chips[['code', 'name']])

# Cổ phiếu sàn HSX
hsx_stocks = ref.equity.by_exchange("HSX")
print(f"HSX symbols: {len(hsx_stocks)}")
```

---

### 3. Index Domain (Danh Sách Chỉ Số)

**Source:** VCI (vci)  
**Registry Key:** `"index"`

#### Phương Thức

| Method | Tham Số | Mô Tả | Ví Dụ |
|--------|---------|-------|-------|
| `futures()` | - | Danh sách chỉ số tương lai | `ref.index.futures()` |

#### Ví Dụ

```python
from vnstock_data import Reference

ref = Reference()

# Danh sách chỉ số tương lai
indices = ref.index.futures()
print(indices[['code', 'name']])
```

---

### 4. Industry Domain (Ngành Kinh Tế)

**Source:** VCI (vci)  
**Registry Key:** `"industry"`

#### Phương Thức

| Method | Tham Số | Mô Tả | Ví Dụ |
|--------|---------|-------|-------|
| `list()` | - | Toàn bộ danh sách ngành | `ref.industry.list()` |

#### Ví Dụ

```python
from vnstock_data import Reference

ref = Reference()

# Toàn bộ ngành ICB
industries = ref.industry.list()
print(industries[['code', 'name']])
```

---

### 5. Derivatives Domain (Chứng Chỉ Phái Sinh)

**Source:** KBS, VCI (kbs, vci)  
**Registry Key:** `"derivatives.warrant"`, `"derivatives.futures"`

Derivatives domain cung cấp access tới Warrant và Futures thông qua sub-domains structure.

#### 5.1 Warrant Sub-Domain (Chứng Quyền)

**Sub-domain:** `.warrant(symbol)`

| Method | Tham Số | Mô Tả | Ví Dụ |
|--------|---------|-------|-------|
| `profile()` | - | Thông tin chi tiết chứng quyền | `ref.derivatives().warrant("CACB2511").profile()` |

#### 5.2 Futures Sub-Domain (Hợp Đồng Tương Lai)

**Sub-domain:** `.futures(symbol)`

| Method | Tham Số | Mô Tả | Ví Dụ |
|--------|---------|-------|-------|
| `profile()` | - | Thông tin chi tiết hợp đồng | `ref.derivatives().futures("VN30F2503").profile()` |

#### Ví Dụ

```python
from vnstock_data import Reference

ref = Reference()

# Lấy thông tin chi tiết chứng quyền (nested under derivatives)
warrant = ref.derivatives().warrant("CACB2511")
df_warrant_profile = warrant.profile()
print(df_warrant_profile)

# Lấy thông tin chi tiết hợp đồng tương lai (nested under derivatives)
futures = ref.derivatives().futures("VN30F2503")
df_futures_profile = futures.profile()
print(df_futures_profile)
```

---

### 6. Fund Domain (Quỹ Đầu Tư)

**Source:** FMarket (fmarket)  
**Registry Key:** `"reference.fund"`

#### Phương Thức

| Method | Tham Số | Mô Tả | Ví Dụ |
|--------|---------|-------|-------|
| `list()` | - | Danh sách quỹ | `ref.fund.list()` |

#### Ví Dụ

```python
from vnstock_data import Reference

ref = Reference()

# Danh sách quỹ đầu tư
funds = ref.fund.list()
print(funds[['code', 'name', 'nav']])
```

---

### 8. Bond Domain (Trái Phiếu)

**Source:** VCI (vci)  
**Registry Key:** `"bond"`

#### Phương Thức

| Method | Tham Số | Mô Tả | Ví Dụ |
|--------|---------|-------|-------|
| `government()` | - | Trái phiếu Chính phủ | `ref.bond.government()` |
| `corporate()` | - | Trái phiếu doanh nghiệp | `ref.bond.corporate()` |

#### Ví Dụ

```python
from vnstock_data import Reference

ref = Reference()

# Trái phiếu Chính phủ
gov_bonds = ref.bond.government()
print(gov_bonds[['code', 'issuer', 'maturity']])

# Trái phiếu công ty
corp_bonds = ref.bond.corporate()
print(corp_bonds.head())
```

---

## 🔗 Registry Mapping

```python
REFERENCE_SOURCES = {
    "company": {
        "profile": ("vci", "company", "Company", "overview"),
        "shareholders": ("vci", "company", "Company", "shareholders"),
        "officers": ("vci", "company", "Company", "officers"),
        "subsidiaries": ("vci", "company", "Company", "subsidiaries"),
        "news": ("vci", "company", "Company", "news"),
        "events": ("vci", "company", "Company", "events"),
    },
    "equity": {
        "list": ("vci", "listing", "Listing", "all_symbols"),
        "by_group": ("vci", "listing", "Listing", "symbols_by_group"),
        "by_exchange": ("vci", "listing", "Listing", "symbols_by_exchange"),
    },
    # ... more domains
}
```

---

## 💡 Best Practices

### 1. Caching Master Data

```python
# Reference data thường không thay đổi → có thể cache
ref = Reference()
all_stocks = ref.equity.list()  # Cache kết quả này

# Sử dụng lại nhiều lần
for symbol in all_stocks['code'].tolist():
    # ...
```

### 2. Filtering Efficiently

```python
# Lấy toàn bộ rồi filter
all_stocks = ref.equity.list()
blue_chips = all_stocks[all_stocks['group'] == 'BLUECHIP']

# Tốt hơn: Gọi trực tiếp nếu API support
blue_chips_direct = ref.equity.by_group("BLUECHIP")
```

---

## ⚠️ Lưu Ý

- **Master data** ít thay đổi → thích hợp để cache
- Nếu muốn realtime data (giá, thanh khoản) → dùng **Market Layer**
- Ví dụ: sau khi có danh sách cổ phiếu từ Reference → fetch giá từ Market

---

## 🚦 Next Steps

- **Market Layer**: Lấy giá, thanh khoản, lịch sử giao dịch
- **Fundamental Layer**: Lấy báo cáo tài chính, tỷ số
- **Insights Layer**: Phân tích, xếp hạng, khuyến nghị
