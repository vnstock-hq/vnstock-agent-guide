# Layer 1: Reference Data (Dữ Liệu Tham Chiếu)

> [!IMPORTANT]
> **Data Schema (Từ điển dữ liệu):** Để xem chính xác tên cột, kiểu dữ liệu (`Dtype`) và ý nghĩa (`Meaning`) của các DataFrame trả về từ layer này, vui lòng tham khảo [Data Schema](schema/01-reference.md). KHÔNG được đoán mò tên cột khi viết code xử lý dữ liệu.

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

| Method           | Tham Số | Mô Tả                       |
| ---------------- | ------- | --------------------------- |
| `info()`         | -       | Thông tin tổng quan công ty |
| `shareholders()` | `mode`  | Cơ cấu cổ đông và cổ đông lớn. `mode` có thể là `'detailed'` (mặc định) hoặc `'summary'` |
| `officers()`     | -       | Danh sách quản lý cấp cao   |
| `subsidiaries()` | -       | Danh sách công ty con       |
| `news()`         | -       | Tin tức công ty             |
| `events()`       | -       | Sự kiện công ty             |

#### 📝 Chi Tiết Các Phương Thức

**1. Thông tin tổng quan (`info`)**
- **Mục đích:** Truy xuất hồ sơ cơ bản của doanh nghiệp, ngày niêm yết, số lượng cổ phiếu lưu hành.
```python
from vnstock_data import Reference
ref = Reference()

df_profile = ref.company("TCB").info()
```

**2. Cơ cấu & danh sách cổ đông (`shareholders`)**
- **Mục đích:** Truy xuất cơ cấu sở hữu tổng hợp hoặc danh sách chi tiết và tỷ lệ sở hữu của các cổ đông lớn.
- **Tham số:** `mode` (`str`): `'detailed'` (danh sách chi tiết cổ đông lớn - mặc định) hoặc `'summary'` (cơ cấu sở hữu tổng hợp như nhà nước, khối ngoại, v.v.).
```python
# 1. Danh sách chi tiết cổ đông lớn kèm phân loại (Cá nhân/Tổ chức)
df_detailed = ref.company("VIC").shareholders(mode="detailed")

# 2. Cơ cấu sở hữu tổng hợp (tỷ lệ nhà nước, khối ngoại...)
df_summary = ref.company("VIC").shareholders(mode="summary")
```

**3. Ban lãnh đạo (`officers`)**
- **Mục đích:** Lấy danh sách thành viên Hội đồng quản trị, Ban giám đốc.
- **Tham số:** `filter_by` (`str`): `'working'` (đang làm việc - mặc định), `'resigned'` (đã nghỉ), hoặc `'all'`.
```python
df_officers = ref.company("HPG").officers(filter_by="working")
```

**4. Công ty con (`subsidiaries`)**
- **Mục đích:** Tra cứu danh sách các công ty con, công ty liên kết của doanh nghiệp.
- **Tham số:** `filter_by` (`str`): `'all'` (tất cả - mặc định), `'subsidiary'` (công ty con), hoặc `'affiliate'` (công ty liên kết).
```python
df_subs = ref.company("TCB").subsidiaries(filter_by="subsidiary")
```

**5. Tin tức (`news`)**
- **Mục đích:** Danh sách các bài báo, tin tức mới nhất liên quan đến mã chứng khoán.
- **Tham số:** `start` (ngày bắt đầu), `end` (ngày kết thúc), `length` (số ngày lùi lại mặc định 90), `limit` (giới hạn bài viết), `mode` (`'list'` hoặc `'detail'`), `**kwargs` (tuỳ chỉnh phụ thuộc từng source).

> [!TIP] 
> **Phân biệt `vnstock_data` và `vnstock_news`:**
> - Hàm `news()` trong `vnstock_data` tập trung vào tin tức **đã được phân loại** cho một doanh nghiệp cụ thể (Bao gồm: thông báo nội bộ, công bố thông tin, tin từ sở giao dịch, tin tức trực tiếp về mã cổ phiếu).
> - Gói `vnstock_news` chuyên dùng để cào **tin tức đại chúng chưa dán nhãn** trực tiếp từ các trang báo (thích hợp làm nguyên liệu thô cho mô hình ML/AI hoặc sử dụng AI Agent để gán nhãn).

```python
df_news_list = ref.company("TCB").news(length=90, mode='list')
df_news_detail = ref.company("TCB").news(length=10, mode='detail', limit=50)
```

**6. Sự kiện (`events`)**
- **Mục đích:** Lấy các sự kiện trả cổ tức, họp đại hội cổ đông... của riêng mã chứng khoán đó.
```python
df_events = ref.company("TCB").events()
```

---

### 2. Equity Domain (Danh Sách Cổ Phiếu)

**Nguồn:** VCI (vci)  
**Registry Key:** `"equity"`

#### Phương thức

| Method               | Tham Số | Mô Tả                              |
| -------------------- | ------- | ---------------------------------- |
| `list()`             | -       | Toàn bộ danh sách cổ phiếu         |
| `list_by_group()`    | `group` | Cổ phiếu theo nhóm (VN30, HOSE...) |
| `list_by_exchange()` | -       | Cổ phiếu theo sàn (HSX, HNX...)    |
| `list_by_industry()` | -       | Cổ phiếu theo ngành ICB            |

#### 📝 Chi Tiết Các Phương Thức

**1. Toàn bộ danh sách cổ phiếu (`list`)**
- **Mục đích:** Tra cứu toàn bộ các mã cổ phiếu đang giao dịch trên thị trường.
```python
from vnstock_data import Reference
ref = Reference()

all_symbols = ref.equity.list()
```

**2. Cổ phiếu theo nhóm (`list_by_group`)**
- **Mục đích:** Liệt kê các cổ phiếu thuộc các rổ chỉ số phổ biến hoặc nhóm thị trường.
- **Tham số:** `group` (`str`): Mã nhóm chỉ số (VD: `"VN30"`, `"HNX30"`, `"HOSE"`...).
```python
vn30 = ref.equity.list_by_group("VN30")
```

**3. Cổ phiếu theo sàn (`list_by_exchange`)**
- **Mục đích:** Trả về danh sách cổ phiếu được nhóm sẵn theo sàn giao dịch (HOSE, HNX, UPCOM).
```python
exchange_stocks = ref.equity.list_by_exchange()
```

**4. Cổ phiếu theo ngành (`list_by_industry`)**
- **Mục đích:** Lọc cổ phiếu theo phân ngành ICB.
- **Tham số:** 
  - `icb_code` (`str`, optional): Mã ngành ICB (Ví dụ: `"8773"`). Nếu không truyền sẽ trả về tất cả.
  - `lang` (`str`): Ngôn ngữ (`'vi'` hoặc `'en'`). Mặc định `'vi'`.
```python
icb_stocks = ref.equity.list_by_industry(icb_code="8355", lang="vi")
```

---

### 3. Index Domain (Danh Sách Chỉ Số)

**Nguồn:** KBS, VCI  
**Registry Key:** `"index"`

#### Phương thức

| Method                 | Tham Số | Mô Tả                                 |
| ---------------------- | ------- | ------------------------------------- |
| `list()`               | -       | Toàn bộ danh sách chỉ số với metadata |
| `groups()`             | -       | Liệt kê các nhóm chỉ số               |
| `members(group)`       | `group` | Thành phần cổ phiếu của chỉ số        |
| `list_by_group(group)` | `group` | Chỉ số theo nhóm                      |

#### 📝 Chi Tiết Các Phương Thức

**1. Liệt kê tất cả chỉ số (`list`)**
- **Mục đích:** Liệt kê danh sách tất cả các chỉ số chuẩn (VN30, VN100, HNX30...) kèm theo metadata.
```python
from vnstock_data import Reference
ref = Reference()

all_indices = ref.index.list()
```

**2. Nhóm chỉ số (`groups`)**
- **Mục đích:** Danh sách các nhóm/bộ chỉ số đang được phân loại (VD: `HOSE Indices`, `Sector Indices`).
```python
groups = ref.index.groups()
```

**3. Thành phần chỉ số (`members`)**
- **Mục đích:** Liệt kê các cổ phiếu cấu thành nên một chỉ số (VD: 30 mã trong VN30).
- **Tham số:** `group` (`str`): Tên chỉ số (VD: `"VN30"`).
```python
vn30_members = ref.index.members("VN30")
```

**4. Chi tiết một chỉ số (`info`, `description`)**
- **Mục đích:** Xem thông tin hoặc mô tả chi tiết của riêng một chỉ số bằng cách truyền thẳng mã vào domain.
```python
vn30_detail = ref.index("VN30")
print(vn30_detail.info())
print(vn30_detail.description())
```

---

### 4. Industry Domain (Ngành Kinh Tế)

**Nguồn:** VCI (vci)  
**Registry Key:** `"industry"`

#### Phương thức

| Method      | Tham Số | Mô Tả                         |
| ----------- | ------- | ----------------------------- |
| `list()`    | -       | Toàn bộ danh sách ngành ICB   |
| `sectors()` | -       | Phân loại cổ phiếu theo ngành |

#### 📝 Chi Tiết Các Phương Thức

**1. Toàn bộ ngành ICB (`list`)**
- **Mục đích:** Tra cứu cây phân loại nhóm ngành chuẩn quốc tế ICB (từ level 1 đến level 4) dành cho thị trường Việt Nam.
- **Tham số:** `lang` (`str`): Ngôn ngữ trả về (`'vi'` hoặc `'en'`). Mặc định `'vi'`.
```python
from vnstock_data import Reference
ref = Reference()

industries = ref.industry.list(lang="vi")
```

**2. Phân loại cổ phiếu theo ngành (`sectors`)**
- **Mục đích:** Liệt kê các mã cổ phiếu và mapping của chúng với các nhóm ngành ICB tương ứng.
- **Tham số:**
  - `icb_code` (`str`, optional): Lọc riêng một mã ngành cụ thể. Mặc định `None`.
  - `lang` (`str`): Ngôn ngữ (`'vi'` hoặc `'en'`). Mặc định `'vi'`.
```python
sectors = ref.industry.sectors()
```

---

### 5. Fund Domain (Quỹ Mở)

**Nguồn:** FMarket (fmarket)  
**Registry Key:** `"reference.fund"`

#### Phương thức

| Method   | Tham Số | Mô Tả                   |
| -------- | ------- | ----------------------- |
| `list()` | -       | Danh sách quỹ đầu tư mở |

#### 📝 Chi Tiết Các Phương Thức

**1. Danh sách Quỹ Đầu Tư Mở (`list`)**
- **Mục đích:** Tra cứu danh sách tất cả các quỹ mở (Mutual Funds) đang hoạt động trên FMarket.
- **Tham số:** `fund_type` (`str`): Loại quỹ muốn lọc (VD: `"Cổ phiếu"`, `"Trái phiếu"`, `"Cân bằng"`). Để trống `""` sẽ lấy toàn bộ.
```python
from vnstock_data import Reference
ref = Reference()

funds = ref.fund.list(fund_type="")
```

---

### 6. ETF Domain (Quỹ ETF)

**Nguồn:** KBS (kbs)  
**Registry Key:** `"etf"`

#### Phương thức

| Method   | Tham Số | Mô Tả                |
| -------- | ------- | -------------------- |
| `list()` | -       | Danh sách tất cả ETF |

#### 📝 Chi Tiết Các Phương Thức

**1. Danh sách Quỹ ETF (`list`)**
- **Mục đích:** Tra cứu danh sách tất cả các quỹ hoán đổi danh mục (ETF) đang niêm yết và giao dịch trên thị trường.
```python
from vnstock_data import Reference
ref = Reference()

etf_list = ref.etf.list()
```

---

### 7. Bond Domain (Trái Phiếu)

**Nguồn:** KBS, VCI  
**Registry Key:** `"bond"`

#### Phương thức

| Method   | Tham Số     | Mô Tả                                                                     |
| -------- | ----------- | ------------------------------------------------------------------------- |
| `list()` | `bond_type` | Danh sách trái phiếu. `bond_type`: `'all'`, `'corporate'`, `'government'` |

#### 📝 Chi Tiết Các Phương Thức

**1. Danh sách Trái Phiếu (`list`)**
- **Mục đích:** Liệt kê danh sách các mã trái phiếu (bao gồm cả trái phiếu chính phủ và doanh nghiệp).
- **Tham số:** `bond_type` (`str`): Lọc loại trái phiếu (`'all'`, `'corporate'`, `'government'`). Mặc định `'all'`.
```python
from vnstock_data import Reference
ref = Reference()

# Lấy toàn bộ danh sách trái phiếu
all_bonds = ref.bond.list(bond_type="all")

# Lọc riêng trái phiếu doanh nghiệp
corp_bonds = ref.bond.list(bond_type="corporate")
```

---

### 8. Events Domain (Sự Kiện)

**Nguồn:** VCI (vci), Vnstock internal  
**Registry Key:** `"events"`

#### Phương thức

| Method       | Tham Số                      | Mô Tả                                           |
| ------------ | ---------------------------- | ----------------------------------------------- |
| `calendar()` | `start`, `end`, `event_type` | Lịch sự kiện (cổ tức, ĐHCĐ, IPO...)             |
| `market()`   | `start`, `end`, `event_type` | Sự kiện thị trường đặc biệt (nghỉ lễ, sự cố...) |

**`event_type` cho `calendar()`:**
- `'dividend'`: Cổ tức, phát hành cổ phiếu
- `'insider'`: Giao dịch nội bộ
- `'agm'`: Đại hội cổ đông
- `'others'`: Biến động khác

#### 📝 Chi Tiết Các Phương Thức

**1. Lịch sự kiện (`calendar`)**
- **Mục đích:** Tra cứu lịch chi trả cổ tức, họp Đại hội đồng cổ đông, giao dịch nội bộ... theo thời gian.
- **Tham số:** 
  - `start`, `end` (`str`, optional): Khoảng thời gian lọc (`"YYYY-MM-DD"`).
  - `event_type` (`str`, optional): Loại sự kiện (`"dividend"`, `"insider"`, `"agm"`, `"others"`).
```python
from vnstock_data import Reference
ref = Reference()

# Lịch sự kiện tháng 3/2026
events = ref.events.calendar(start="2026-03-01", end="2026-03-31")

# Chỉ sự kiện cổ tức
dividends = ref.events.calendar(
    start="2026-03-01", end="2026-03-31", event_type="dividend"
)
```

**2. Sự kiện thị trường (`market`)**
- **Mục đích:** Tra cứu danh sách các ngày nghỉ lễ, ngày hệ thống bảo trì hoặc sự cố gián đoạn giao dịch.
- **Tham số:** `start`, `end` (`str`), `event_type` (`str`).
```python
market_events = ref.events.market()
```

---

### 9. Search Domain (Tìm Kiếm Toàn Cầu)

**Nguồn:** MSN  
**Registry Key:** `"search"`

#### Phương thức

| Method     | Tham Số                    | Mô Tả                                                      |
| ---------- | -------------------------- | ---------------------------------------------------------- |
| `symbol()` | `query`, `locale`, `limit` | Tìm kiếm symbol toàn cầu (cổ phiếu, crypto, forex, chỉ số) |

**Parameters:**
- `query` (str): Từ khóa tìm kiếm (ví dụ: "VNM", "Bitcoin", "Gold")
- `locale` (str, optional): Ngôn ngữ/khu vực (ví dụ: "vi-vn", "en-us")
- `limit` (int, optional): Số kết quả tối đa. Mặc định 10.

#### 📝 Chi Tiết Các Phương Thức

**1. Tìm kiếm symbol (`symbol`)**
- **Mục đích:** Công cụ tìm kiếm toàn cầu cho phép gõ từ khoá linh hoạt (tên công ty, mã cổ phiếu, crypto, forex) để tìm mã ticker chính xác.
- **Tham số:**
  - `query` (`str`): Từ khóa (VD: `"VNM"`, `"Bitcoin"`, `"Gold"`).
  - `locale` (`str`, optional): Vùng dữ liệu (VD: `"vi-vn"`, `"en-us"`).
  - `limit` (`int`, optional): Giới hạn kết quả, mặc định `10`.
```python
from vnstock_data import Reference
ref = Reference()

# Tìm kiếm "VNM"
results = ref.search.symbol("VNM")

# Tìm kiếm Bitcoin
btc = ref.search.symbol("Bitcoin", limit=5)

# Tìm kiếm vàng
gold = ref.search.symbol("Gold", locale="en-us")
```

**2. Tìm kiếm info (`info`)**
- **Mục đích:** Tìm kiếm và trả về thông tin metadata chi tiết của tài sản toàn cầu.
- **Tham số:** `query`, `locale`, `limit` tương tự như `symbol()`.
```python
asset_info = ref.search.info("Apple")
```

> **Lưu ý**: `symbol_id` từ kết quả tìm kiếm có thể dùng cho các domain Market experimental (crypto, forex, commodity).

---

### 10. Futures Domain (Hợp Đồng Tương Lai)

**Nguồn:** KBS, VCI  
**Registry Key:** `"derivatives.futures"`

#### Phương thức

| Method   | Tham Số | Mô Tả                                    |
| -------- | ------- | ---------------------------------------- |
| `list()` | -       | Danh sách hợp đồng tương lai             |
| `info()` | -       | Thông tin chi tiết hợp đồng (cần symbol) |

#### 📝 Chi Tiết Các Phương Thức

**1. Danh sách Hợp Đồng Tương Lai (`list`)**
- **Mục đích:** Lấy toàn bộ danh sách các hợp đồng tương lai đang giao dịch.
```python
from vnstock_data import Reference
ref = Reference()

futures_list = ref.futures().list()
```

**2. Thông tin chi tiết Hợp Đồng (`info`)**
- **Mục đích:** Truy xuất thông tin (ngày đáo hạn, mã cơ sở) của một hợp đồng cụ thể.
```python
futures_info = ref.futures("VN30F2503").info()
```

---

### 11. Warrant Domain (Chứng Quyền)

**Nguồn:** KBS, VCI  
**Registry Key:** `"derivatives.warrant"`

#### Phương Thức

| Method   | Tham Số | Mô Tả                                       |
| -------- | ------- | ------------------------------------------- |
| `list()` | -       | Danh sách chứng quyền                       |
| `info()` | -       | Thông tin chi tiết chứng quyền (cần symbol) |

#### 📝 Chi Tiết Các Phương Thức

**1. Danh sách Chứng Quyền (`list`)**
- **Mục đích:** Lấy danh sách toàn bộ các chứng quyền có bảo đảm (Covered Warrant) trên thị trường.
```python
from vnstock_data import Reference
ref = Reference()

warrant_list = ref.warrant().list()
```

**2. Thông tin chi tiết Chứng Quyền (`info`)**
- **Mục đích:** Xem thông tin tổ chức phát hành, tỷ lệ chuyển đổi, ngày đáo hạn, giá thực hiện.
```python
warrant_info = ref.warrant("CACB2511").info()
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
