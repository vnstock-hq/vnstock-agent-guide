# Layer 1: Reference Data (Dữ Liệu Tham Chiếu)

## 📌 Tổng Quan

**Reference Layer** cung cấp thông tin nền tảng, tĩnh về các sản phẩm tài chính - công ty, chỉ số, ngành, danh sách symbol, ETF, trái phiếu, sự kiện, v.v. Đây là dữ liệu **không thay đổi thường xuyên** và được sử dụng để **lookup** hay **master data**.

## 🏗️ Cấu Trúc Domain

```python
Reference()
├── .company(symbol)       # Thông tin công ty
├── .equity                # Danh sách cổ phiếu (property)
├── .index                 # Danh sách chỉ số (property)
├── .industry              # Ngành kinh tế (property)
├── .fund                  # Quỹ đầu tư mở (property)
├── .etf                   # Quỹ ETF (property)
├── .bond                  # Trái phiếu (property)
├── .events                # Sự kiện thị trường (property)
├── .search                # Tìm kiếm toàn cầu (property)
├── .futures(symbol)       # Hợp đồng tương lai
└── .warrant(symbol)       # Chứng quyền
```

## 📋 Chi Tiết Các Domain

### 1. Company Domain (Thông Tin Công Ty)

**Nguồn:** VCI, KBS  
**Registry Key:** `"company"`

#### Phương Thức

| Method | Tham Số | Mô Tả |
|--------|---------|-------|
| `info()` | - | Thông tin tổng quan công ty |
| `shareholders()` | - | Danh sách cổ đông chính |
| `officers()` | - | Danh sách quản lý cấp cao |
| `subsidiaries()` | - | Danh sách công ty con |
| `news()` | - | Tin tức công ty |
| `events()` | - | Sự kiện công ty |
| `margin_ratio()` | - | Tỷ lệ ký quỹ qua các broker |

#### Ví Dụ

```python
from vnstock_data import Reference

ref = Reference()

# Thông tin công ty
df_profile = ref.company("TCB").info()
print(df_profile)

# Danh sách cổ đông lớn
df_shareholders = ref.company("VIC").shareholders()
print(df_shareholders)

# Quản lý cấp cao
df_officers = ref.company("HPG").officers()
print(df_officers)
```

---

### 2. Equity Domain (Danh Sách Cổ Phiếu)

**Nguồn:** VCI (vci)  
**Registry Key:** `"equity"`

#### Phương thức

| Method | Tham Số | Mô Tả |
|--------|---------|-------|
| `list()` | - | Toàn bộ danh sách cổ phiếu |
| `list_by_group()` | `group` | Cổ phiếu theo nhóm (VN30, HOSE...) |
| `list_by_exchange()` | `exchange` | Cổ phiếu theo sàn (HSX, HNX...) |
| `list_by_industry()` | - | Cổ phiếu theo ngành ICB |

#### Ví dụ

```python
from vnstock_data import Reference

ref = Reference()

# Tất cả symbol (1700+ mã)
all_symbols = ref.equity.list()
print(f"Total symbols: {len(all_symbols)}")
# Columns: ['symbol', 'org_name']

# Cổ phiếu theo nhóm
vn30 = ref.equity.list_by_group("VN30")
print(vn30)

# Cổ phiếu sàn HSX
hsx_stocks = ref.equity.list_by_exchange("HSX")
print(f"HSX symbols: {len(hsx_stocks)}")
```

---

### 3. Index Domain (Danh Sách Chỉ Số)

**Nguồn:** KBS, VCI  
**Registry Key:** `"index"`

#### Phương thức

| Method | Tham Số | Mô Tả |
|--------|---------|-------|
| `list()` | - | Toàn bộ danh sách chỉ số với metadata |
| `groups()` | - | Liệt kê các nhóm chỉ số |
| `members(group)` | `group` | Thành phần cổ phiếu của chỉ số |
| `list_by_group(group)` | `group` | Chỉ số theo nhóm |

#### Ví dụ

```python
from vnstock_data import Reference

ref = Reference()

# Liệt kê tất cả chỉ số
all_indices = ref.index.list()
print(all_indices)

# Nhóm chỉ số
groups = ref.index.groups()
print(groups)

# Thành phần VN30
vn30_members = ref.index.members("VN30")
print(vn30_members)

# Chi tiết một chỉ số cụ thể
vn30_detail = ref.index("VN30")
print(vn30_detail.info())
print(vn30_detail.description())
```

---

### 4. Industry Domain (Ngành Kinh Tế)

**Nguồn:** VCI (vci)  
**Registry Key:** `"industry"`

#### Phương thức

| Method | Tham Số | Mô Tả |
|--------|---------|-------|
| `list()` | - | Toàn bộ danh sách ngành ICB |
| `sectors()` | - | Phân loại cổ phiếu theo ngành |

#### Ví dụ

```python
from vnstock_data import Reference

ref = Reference()

# Toàn bộ ngành ICB
industries = ref.industry.list()
print(industries)

# Cổ phiếu theo ngành
sectors = ref.industry.sectors()
print(sectors)
```

---

### 5. Fund Domain (Quỹ Mở)

**Nguồn:** FMarket (fmarket)  
**Registry Key:** `"reference.fund"`

#### Phương thức

| Method | Tham Số | Mô Tả |
|--------|---------|-------|
| `list()` | - | Danh sách quỹ đầu tư mở |

#### Ví dụ

```python
from vnstock_data import Reference

ref = Reference()

# Danh sách quỹ đầu tư mở
funds = ref.fund.list()
print(funds)
```

---

### 6. ETF Domain (Quỹ ETF)

**Nguồn:** KBS (kbs)  
**Registry Key:** `"etf"`

#### Phương thức

| Method | Tham Số | Mô Tả |
|--------|---------|-------|
| `list()` | - | Danh sách tất cả ETF |

#### Ví dụ

```python
from vnstock_data import Reference

ref = Reference()

# Danh sách ETF
etf_list = ref.etf.list()
print(etf_list)
```

---

### 7. Bond Domain (Trái Phiếu)

**Nguồn:** KBS, VCI  
**Registry Key:** `"bond"`

#### Phương thức

| Method | Tham Số | Mô Tả |
|--------|---------|-------|
| `list()` | `bond_type` | Danh sách trái phiếu. `bond_type`: `'all'`, `'corporate'`, `'government'` |

#### Ví dụ

```python
from vnstock_data import Reference

ref = Reference()

# Tất cả trái phiếu
all_bonds = ref.bond.list(bond_type="all")
print(all_bonds)

# Chỉ trái phiếu doanh nghiệp
corp_bonds = ref.bond.list(bond_type="corporate")
print(corp_bonds)
```

---

### 8. Events Domain (Sự Kiện)

**Nguồn:** VCI (vci), Vnstock internal  
**Registry Key:** `"events"`

#### Phương thức

| Method | Tham Số | Mô Tả |
|--------|---------|-------|
| `calendar()` | `start`, `end`, `event_type` | Lịch sự kiện (cổ tức, ĐHCĐ, IPO...) |
| `market()` | `start`, `end`, `event_type` | Sự kiện thị trường đặc biệt (nghỉ lễ, sự cố...) |

**`event_type` cho `calendar()`:**
- `'dividend'`: Cổ tức, phát hành cổ phiếu
- `'insider'`: Giao dịch nội bộ
- `'agm'`: Đại hội cổ đông
- `'others'`: Biến động khác

#### Ví dụ

```python
from vnstock_data import Reference

ref = Reference()

# Lịch sự kiện tháng 3/2026
events = ref.events.calendar(start="2026-03-01", end="2026-03-31")
print(events)

# Chỉ sự kiện cổ tức
dividends = ref.events.calendar(
    start="2026-03-01", end="2026-03-31", event_type="dividend"
)
print(dividends)

# Sự kiện thị trường (nghỉ lễ, sự cố)
market_events = ref.events.market()
print(market_events)
```

---

### 9. Search Domain (Tìm Kiếm Toàn Cầu)

**Nguồn:** MSN  
**Registry Key:** `"search"`

#### Phương thức

| Method | Tham Số | Mô Tả |
|--------|---------|-------|
| `symbol()` | `query`, `locale`, `limit` | Tìm kiếm symbol toàn cầu (cổ phiếu, crypto, forex, chỉ số) |

**Parameters:**
- `query` (str): Từ khóa tìm kiếm (ví dụ: "VNM", "Bitcoin", "Gold")
- `locale` (str, optional): Ngôn ngữ/khu vực (ví dụ: "vi-vn", "en-us")
- `limit` (int, optional): Số kết quả tối đa. Mặc định 10.

#### Ví dụ

```python
from vnstock_data import Reference

ref = Reference()

# Tìm kiếm "VNM"
results = ref.search.symbol("VNM")
print(results)
# Columns: ['symbol', 'name', 'exchange', 'short_name', 
#           'description', 'name_en', 'name_local', 'symbol_id']

# Tìm kiếm Bitcoin
btc = ref.search.symbol("Bitcoin", limit=5)
print(btc)

# Tìm kiếm vàng
gold = ref.search.symbol("Gold", locale="en-us")
print(gold)
```

> **Lưu ý**: `symbol_id` từ kết quả tìm kiếm có thể dùng cho các domain Market experimental (crypto, forex, commodity).

---

### 10. Futures Domain (Hợp Đồng Tương Lai)

**Nguồn:** KBS, VCI  
**Registry Key:** `"derivatives.futures"`

#### Phương thức

| Method | Tham Số | Mô Tả |
|--------|---------|-------|
| `list()` | - | Danh sách hợp đồng tương lai |
| `info()` | - | Thông tin chi tiết hợp đồng (cần symbol) |

#### Ví dụ

```python
from vnstock_data import Reference

ref = Reference()

# Danh sách hợp đồng tương lai
futures_list = ref.futures().list()
print(futures_list)

# Thông tin chi tiết hợp đồng
futures_info = ref.futures("VN30F2503").info()
print(futures_info)
```

---

### 11. Warrant Domain (Chứng Quyền)

**Nguồn:** KBS, VCI  
**Registry Key:** `"derivatives.warrant"`

#### Phương Thức

| Method | Tham Số | Mô Tả |
|--------|---------|-------|
| `list()` | - | Danh sách chứng quyền |
| `info()` | - | Thông tin chi tiết chứng quyền (cần symbol) |

#### Ví Dụ

```python
from vnstock_data import Reference

ref = Reference()

# Danh sách chứng quyền
warrant_list = ref.warrant().list()
print(warrant_list)

# Thông tin chi tiết
warrant_info = ref.warrant("CACB2511").info()
print(warrant_info)
```

> **Lưu ý**: `derivatives()` đã deprecated. Dùng `ref.futures()` / `ref.warrant()` trực tiếp.

---

## 💡 Best Practices

### 1. Caching Master Data

```python
# Reference data thường không thay đổi → có thể cache
ref = Reference()
all_stocks = ref.equity.list()  # Cache kết quả này

# Sử dụng lại nhiều lần
for symbol in all_stocks['symbol'].tolist():
    # ...
    pass
```

### 2. Dùng `show_api()` để tra cứu

```python
from vnstock_data import show_api, Reference
show_api(Reference())  # Xem toàn bộ Reference tree
```

---

## ⚠️ Lưu Ý

- **Master data** ít thay đổi → thích hợp để cache
- Nếu muốn realtime data (giá, thanh khoản) → dùng **Market Layer**
- `derivatives()` đã deprecated → dùng `futures()` / `warrant()` trực tiếp

---

## 🚦 Next Steps

- **Market Layer**: Lấy giá, thanh khoản, lịch sử giao dịch
- **Fundamental Layer**: Lấy báo cáo tài chính, tỷ số
- **Insights Layer**: Phân tích, xếp hạng
