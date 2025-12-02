# Listing - Danh Sách Niêm Yết, Phân Ngành, Chỉ Số

## Giới Thiệu

Lớp `Listing` cung cấp thông tin về các chứng khoán niêm yết tại các sàn giao dịch Việt Nam và các phân loại của chúng. Bạn có thể:

- Lấy danh sách tất cả mã cổ phiếu (~1.7K mã), chỉ số, hợp đồng tương lai, chứng quyền, trái phiếu niêm yết
- Phân loại cổ phiếu theo ngành theo chuẩn ICB (4 cấp)
- Xem danh sách các chỉ số thị trường (VN30, VN100, VNMidCap, HNX30, etc.)
- Tìm hợp đồng tương lai (10 loại), chứng quyền (305), trái phiếu doanh nghiệp (81)

### Trường Hợp Sử Dụng

- **Lấy danh sách cổ phiếu toàn thị trường**: Xây dựng tập hợp mã cổ phiếu chủ đạo cho backtesting hoặc phân tích
- **Phân tích theo ngành**: Lọc các công ty theo ngành (Ngân hàng, Bất động sản, Công nghệ, etc.)
- **Lấy thành phần chỉ số**: Tìm tất cả mã trong VN30, VN100, HNX30, etc.
- **Lọc công cụ khác**: Tìm hợp đồng tương lai, chứng quyền, trái phiếu để giao dịch

## Khởi Tạo Object

```python
from vnstock_data import Listing

# Khởi tạo với nguồn VCI (mặc định, đầy đủ tính năng)
listing = Listing(source="vci")

# Khởi tạo với nguồn VND (nguồn bổ sung cung cấp danh sách cổ phiếu, ít method gọi hơn)
listing_vnd = Listing(source="vnd")
```

### Tham Số Khởi Tạo

- `source` (str, tùy chọn): Nguồn dữ liệu - `"vci"` hoặc `"vnd"`. Mặc định là `"vci"`
- `random_agent` (bool, tùy chọn): Sử dụng random user agent để tránh bị block. Mặc định là `False`

**Ghi Chú**: VCI có hỗ trợ tất cả method, còn VND chỉ hỗ trợ `all_symbols()`. Xem phần "Ma Trận Nguồn Dữ Liệu Hỗ Trợ" ở cuối.

## Các Phương Thức

### 1. all_symbols() - Danh Sách Tất Cả Mã Niêm Yết

Lấy danh sách toàn bộ mã cổ phiếu niêm yết tại HOSE, HNX, UPCOM.

**Cú Pháp**
```python
df = listing.all_symbols()
```

**Tham Số**

Không có tham số bắt buộc.

**Kiểu Dữ Liệu Trả Về**

**DataFrame** với 2 cột:
- `symbol`: object (str)
- `organ_name`: object (str)

**Ví Dụ**
```python
from vnstock_data import Listing

listing = Listing(source="vci")
df_all = listing.all_symbols()

print(f"Tổng số mã niêm yết: {len(df_all)}")
print(df_all.head(3))
#   symbol                                         organ_name
# 0    YTC  Công ty Cổ phần Xuất nhập khẩu Y tế Thành phố ...
# 1    YEG                     Công ty Cổ phần Tập đoàn Yeah1
# 2    YBM     Công ty Cổ phần Khoáng sản Công nghiệp Yên Bái
```

### 2. symbols_by_industries() - Mã Cổ Phiếu Theo Ngành (theo chuẩn ICB)

Lấy danh sách tất cả cổ phiếu với thông tin phân loại theo ngành ICB (cấp 1-4).

**Cú Pháp**
```python
df = listing.symbols_by_industries(lang='vi')
```

**Tham Số**
- `lang` (str, tùy chọn): Ngôn ngữ - `'vi'` (Tiếng Việt) hoặc `'en'` (Tiếng Anh). Mặc định là `'vi'`

**Ghi Chú Quan Trọng**: Method này trả về **TẤT CẢ CỔ PHIẾU (\~1.6K mã)** với thông tin ngành. Không có parameter để lọc theo tên ngành cụ thể. Dùng chế độ lọc của DataFrame để lọc theo sàn cụ thể khi đã có kết quả trả về.

**Kiểu Dữ Liệu Trả Về**

DataFrame với 10 cột (tất cả object):
- `symbol`: object (str)
- `organ_name`: object (str)
- `icb_name3`: object (str) - Tên ngành cấp 3
- `icb_name2`: object (str) - Tên ngành cấp 2
- `icb_name4`: object (str) - Tên ngành cấp 4
- `com_type_code`: object (str) - Mã loại công ty
- `icb_code1`: object (str) - Mã ICB cấp 1
- `icb_code2`: object (str) - Mã ICB cấp 2
- `icb_code3`: object (str) - Mã ICB cấp 3
- `icb_code4`: object (str) - Mã ICB cấp 4

**Ví Dụ**
```python
# Lấy tất cả mã với thông tin ngành
df_ind = listing.symbols_by_industries()
print(f"Số cổ phiếu: {len(df_ind)}")
print(df_ind.head(3))
#   symbol                                         organ_name  icb_name3             icb_name2       icb_name4  ...
# 0    BQP  Công ty Cổ phần Nhựa chất lượng cao Bình Thuận     Hóa chất              Hóa chất & ...  Hóa chất công...
# 1    F88  Công ty Cổ phần Đầu tư F88                         Dịch vụ tài chính     Tài chính       Dịch vụ tài...
# 2    DVT  Trung tâm Đào tạo nghiệp vụ Giao thông vận tải...  Tư vấn & Hỗ trợ...    Dịch vụ ki...   Tư vấn & Hỗ trợ...

# Lọc chỉ các mã Ngân hàng bằng DataFrame filtering
banks = df_ind[df_ind['icb_name3'] == 'Ngân hàng']
print(f"Số mã ngân hàng: {len(banks)}")
print(banks[['symbol', 'organ_name', 'icb_name3']].head(3))
```

### 3. symbols_by_exchange() - Mã Theo Sàn Giao Dịch

Lấy danh sách tất cả chứng khoán niêm yết với thông tin sàn giao dịch (>3K mã bao gồm STOCK, FUND, BOND, CW, etc.).

**Cú Pháp**
```python
df = listing.symbols_by_exchange(lang='vi')
```

**Tham Số**
- `lang` (str, tùy chọn): Ngôn ngữ - `'vi'` hoặc `'en'`. Mặc định là `'vi'`

**Ghi Chú Quan Trọng**: Method này không có parameter để lọc theo tên sàn. Trả về TẤT CẢ (3150 mã) từ 3 sàn. Dùng chế độ lọc của DataFrame để lọc theo sàn cụ thể khi đã có kết quả trả về.

**Kiểu Dữ Liệu Trả Về**

DataFrame với 6 cột:
- `symbol`: object (str)
- `exchange`: object (str) - Giá trị: 'HOSE', 'HNX', 'UPCOM'
- `type`: object (str) - Loại: 'STOCK', 'BOND', 'CW', 'FUND', etc.
- `organ_short_name`: object (str)
- `organ_name`: object (str)
- `product_grp_id`: object (str)

**Ví Dụ**
```python
# Lấy tất cả chứng khoán
df_ex = listing.symbols_by_exchange()
print(f"Tổng số chứng khoán: {len(df_ex)}")
print(df_ex.head(3))
#   symbol exchange   type       organ_short_name                                         organ_name
# 0    YTC    UPCOM  STOCK        XNK Y tế TP.HCM  Công ty Cổ phần Xuất nhập khẩu Y tế Thành phố...
# 1    YEG      HSX  STOCK         Tập đoàn Yeah1                     Công ty Cổ phần Tập đoàn Yeah1
# 2    YBM      HSX  STOCK  Khoáng sản CN Yên Bái     Công ty Cổ phần Khoáng sản Công nghiệp Yên Bái

# Lọc chỉ STOCK trên HOSE
hose_stocks = df_ex[(df_ex['exchange'] == 'HOSE') & (df_ex['type'] == 'STOCK')]
print(f"Số STOCK trên HOSE: {len(hose_stocks)}")
```

### 4. industries_icb() - Danh Sách Ngành Theo Chuẩn ICB

Lấy danh sách tất cả các ngành theo chuẩn ICB (155 ngành từ cấp 1-4).

**Cú Pháp**
```python
df = listing.industries_icb()
```

**Tham Số**

Không có tham số bắt buộc.

**Kiểu Dữ Liệu Trả Về**

DataFrame với 4 cột:
- `icb_name`: object (str) - Tên ngành Tiếng Việt - 155 non-null
- `en_icb_name`: object (str) - Tên ngành Tiếng Anh - 155 non-null
- `icb_code`: object (str) - Mã ICB - 155 non-null
- `level`: int64 - Cấp độ (1-4) - 155 non-null

**Ví Dụ**
```python
df_icb = listing.industries_icb()
print(f"Tổng số ngành: {len(df_icb)}")
print(df_icb.head(3))
#                                  icb_name                             en_icb_name icb_code  level
# 0                        Sản xuất Dầu khí                     Oil & Gas Producers     0530      3
# 1  Thiết bị, Dịch vụ và Phân phối Dầu khí  Oil Equipment, Services & Distribution     0570      3
# 2                                Hóa chất                               Chemicals     1350      3

# Lọc các ngành cấp 3 (chi tiết nhất thường dùng)
level3_industries = df_icb[df_icb['level'] == 3]
print(f"Số ngành cấp 3: {len(level3_industries)}")
```

### 5. symbols_by_group() - Mã Theo Nhóm/Chỉ Số

Lấy danh sách mã thuộc một nhóm hoặc chỉ số cụ thể.

**Cú Pháp**
```python
s = listing.symbols_by_group(group='VN30')
```

**Tham Số**
- `group` (str): Tên nhóm/chỉ số. Các giá trị được hỗ trợ:
  - **Sàn giao dịch**: `'HOSE'`, `'HNX'`, `'UPCOM'`
  - **Chỉ số chính**: `'VN30'`, `'VN100'`, `'HNX30'`
  - **Chỉ số đặc biệt**: `'VNMidCap'`, `'VNSmallCap'`, `'VNAllShare'`, `'HNXCon'`, `'HNXFin'`, `'HNXLCap'`, `'HNXMSCap'`, `'HNXMan'`
  - **ETF**: `'ETF'`
  - **Hợp đồng tương lai**: `'FU_INDEX'` (mã chỉ số hợp đồng tương lai)
  - **Chứng quyền**: `'CW'` (chứng quyền)

**Kiểu Dữ Liệu Trả Về**

Pandas Series với dtype object (str):
- Dữ liệu: Mã cổ phiếu (symbol)
- Series name: 'symbol'

**Ví Dụ**
```python
# Lấy VN30
vn30 = listing.symbols_by_group(group='VN30')
print(f"VN30 có {len(vn30)} mã:")
print(vn30.head(3).tolist())
# ['ACB', 'BCM', 'BID']

# Lấy VN100
vn100 = listing.symbols_by_group(group='VN100')
print(f"VN100 có {len(vn100)} mã")

# Lấy VNMidCap
mid_cap = listing.symbols_by_group(group='VNMidCap')
print(f"VNMidCap có {len(mid_cap)} mã")

# Lấy HNX30
hnx30 = listing.symbols_by_group(group='HNX30')
print(f"HNX30 có {len(hnx30)} mã")

# Chuyển thành list
vn30_list = vn30.tolist()
```

### 6. all_future_indices() - Danh Sách Hợp Đồng Tương Lai

Lấy danh sách tất cả hợp đồng tương lai niêm yết (tương đương `symbols_by_group(group='FU_INDEX')`).

**Cú Pháp**
```python
s = listing.all_future_indices()
```

**Kiểu Dữ Liệu Trả Về**

Pandas Series với 10 mã tương lai (dtype: object):
- Ví dụ: '41I1FB000', '41I1G1000', '41I1G3000', etc.

**Ví Dụ**
```python
futures = listing.all_future_indices()
print(f"Số hợp đồng tương lai: {len(futures)}")
print(futures.head(3).tolist())
# ['41I1FB000', '41I1G1000', '41I1G3000']
```

### 7. all_government_bonds() - Danh Sách Trái Phiếu Chính Phủ

Lấy danh sách tất cả trái phiếu chính phủ niêm yết (tương đương `symbols_by_group(group='FU_BOND')`).

**Cú Pháp**
```python
s = listing.all_government_bonds()
```

**Kiểu Dữ Liệu Trả Về**

Pandas Series với 6 mã trái phiếu chính phủ (dtype: object):
- Ví dụ: '41B5G3000', '41B5G6000', '41BAG3000', etc.

**Ví Dụ**
```python
gov_bonds = listing.all_government_bonds()
print(f"Số trái phiếu chính phủ: {len(gov_bonds)}")
print(gov_bonds.head(3).tolist())
# ['41B5G3000', '41B5G6000', '41BAG3000']
```

### 8. all_covered_warrant() - Danh Sách Chứng Quyền

Lấy danh sách tất cả chứng quyền niêm yết (tương đương `symbols_by_group(group='CW')`).

**Cú Pháp**
```python
s = listing.all_covered_warrant()
```

**Kiểu Dữ Liệu Trả Về**

Pandas Series với 305 mã chứng quyền (dtype: object):
- Ví dụ: 'CACB2502', 'CACB2503', 'CACB2508', etc.

**Ví Dụ**
```python
warrants = listing.all_covered_warrant()
print(f"Số chứng quyền: {len(warrants)}")
print(warrants.head(3).tolist())
# ['CACB2502', 'CACB2503', 'CACB2508']
```

### 9. all_bonds() - Danh Sách Trái Phiếu Doanh Nghiệp

Lấy danh sách tất cả trái phiếu doanh nghiệp niêm yết (tương đương `symbols_by_group(group='BOND')`).

**Cú Pháp**
```python
s = listing.all_bonds()
```

**Kiểu Dữ Liệu Trả Về**

Pandas Series với 81 mã trái phiếu doanh nghiệp (dtype: object):
- Ví dụ: 'BAB123007', 'BAB123032', 'BAB124014', etc.

**Ví Dụ**
```python
corp_bonds = listing.all_bonds()
print(f"Số trái phiếu doanh nghiệp: {len(corp_bonds)}")
print(corp_bonds.head(3).tolist())
# ['BAB123007', 'BAB123032', 'BAB124014']
```

## Ma Trận Nguồn Dữ Liệu Hỗ Trợ

> Số lượng mã có thể thay đổi theo thời gian, dữ liệu cập nhật từ nguồn được chỉ định.

| Phương Thức | VCI | VND |
|---|---|---|
| `all_symbols()` | ✅ (1727 mã STOCK) | ✅ (1969 mã, tất cả loại) |
| `symbols_by_industries()` | ✅ (1583 mã + thông tin ICB) | ❌ |
| `symbols_by_exchange()` | ✅ (3150 mã + type/exchange) | ❌ |
| `industries_icb()` | ✅ (155 ngành) | ❌ |
| `symbols_by_group()` | ✅ (tất cả group) | ❌ |
| `all_future_indices()` | ✅ (10 hợp đồng) | ❌ |
| `all_government_bonds()` | ✅ (6 trái phiếu) | ❌ |
| `all_covered_warrant()` | ✅ (305 chứng quyền) | ❌ |
| `all_bonds()` | ✅ (81 trái phiếu) | ❌ |

## VCI vs VND: So Sánh

### VCI Listing
- **all_symbols()**: Trả về 1727 mã STOCK (chỉ loại cổ phiếu)
  - Columns: symbol, organ_name
- **Khác**: Cả 9 method khác
- **Ưu điểm**: Đầy đủ, có phân loại ngành ICB chi tiết, có chỉ số và công cụ khác

### VND Listing
- **all_symbols()**: Trả về 1969 mã (tất cả loại: STOCK, BOND, CW, FUND, IFC, etc.)
  - Columns: symbol, type, exchange, status, company_name, company_name_eng, short_name, listed_date, delisted_date, company_id, isin, tax_code, short_name_eng, index_code (14 cột)
  - Hỗ trợ parameter `exchange=['HOSE', 'HNX', 'UPCOM']` để lọc
- **Ưu điểm**: Nhanh, chi tiết hơn (listed_date, delisted_date, isin, tax_code), hỗ trợ lọc theo sàn
- **Nhược điểm**: Không có phân loại ngành ICB, không có các method khác

### Khuyến Cáo
- **Dùng VCI** nếu cần: Phân loại ngành ICB, danh sách chỉ số (VN30, VN100), danh sách công cụ khác (tương lai, chứng quyền, trái phiếu)
- **Dùng VND** nếu cần: Lấy danh sách nhanh, thông tin trạng thái niêm yết chi tiết (listed_date/delisted_date/isin), lọc theo sàn

## Ví Dụ Thực Tế

### Ví Dụ 1: Tạo Universe Cổ Phiếu Theo Tiêu Chí

```python
from vnstock_data import Listing

listing = Listing(source="vci")

# Lấy tất cả cổ phiếu với thông tin ngành
df = listing.symbols_by_industries()

# Lọc chỉ các mã Ngân hàng
banks = df[df['icb_name3'] == 'Ngân hàng']
print(f"Số mã ngân hàng: {len(banks)}")

# Lọc HOSE + ngành Tài chính (cấp 2)
df_ex = listing.symbols_by_exchange()
df_merged = df.merge(df_ex[['symbol', 'exchange']], on='symbol')
finance_hose = df_merged[
    (df_merged['exchange'] == 'HSX') &
    (df_merged['icb_name2'] == 'Dịch vụ tài chính')
]
print(f"Cổ phiếu tài chính HOSE: {len(finance_hose)}")
```

### Ví Dụ 2: Tạo Danh Sách Mục Tiêu Cho Backtesting

```python
from vnstock_data import Listing

listing = Listing(source="vci")

# Lấy VN30 và VN100
vn30 = listing.symbols_by_group(group='VN30').tolist()
vn100 = listing.symbols_by_group(group='VN100').tolist()
vnmidcap = listing.symbols_by_group(group='VNMidCap').tolist()

# Tạo universe: VN30 + VN100 + VNMidCap (không trùng)
universe = list(set(vn30 + vn100 + vnmidcap))
print(f"Universe VN30+VN100+VNMidCap: {len(universe)} mã")

# Hoặc dùng VNAllShare nếu muốn tất cả
all_share = listing.symbols_by_group(group='VNAllShare').tolist()
print(f"VNAllShare: {len(all_share)} mã")
```

### Ví Dụ 3: Tìm Cổ Phiếu Mới Niêm Yết (Dùng VND)

```python
from vnstock_data import Listing
import pandas as pd

listing = Listing(source="vnd")
df = listing.all_symbols()

# Chuyển đổi listed_date thành datetime
df['listed_date'] = pd.to_datetime(df['listed_date'])

# Lọc các cổ phiếu niêm yết trong 12 tháng gần nhất
recent = df[
    (df['listed_date'] >= pd.Timestamp.now() - pd.Timedelta(days=365)) &
    (df['type'] == 'STOCK') &
    (df['status'] == 'listed')
].sort_values('listed_date', ascending=False)

print(f"Cổ phiếu niêm yết trong 12 tháng gần nhất: {len(recent)}")
print(recent[['symbol', 'company_name', 'exchange', 'listed_date']])
```

### Ví Dụ 4: Lọc Chứng Quyền và Hợp Đồng Tương Lai

```python
from vnstock_data import Listing

listing = Listing(source="vci")

# Danh sách chứng quyền
warrants = listing.symbols_by_group(group='CW')
print(f"Chứng quyền: {len(warrants)} loại")
print(warrants.head(3).tolist())

# Danh sách hợp đồng tương lai
futures = listing.symbols_by_group(group='FU_INDEX')
print(f"Hợp đồng tương lai: {len(futures)} loại")
print(futures.head(3).tolist())

# Danh sách trái phiếu
bonds = listing.all_bonds()
print(f"Trái phiếu doanh nghiệp: {len(bonds)} loại")

gov_bonds = listing.all_government_bonds()
print(f"Trái phiếu chính phủ: {len(gov_bonds)} loại")
```

## Tips & Best Practices

### Tip 1: Cache Danh Sách Cổ Phiếu

Vì danh sách cổ phiếu không thay đổi thường xuyên, hãy cache nó:

```python
from vnstock_data import Listing
import pickle

listing = Listing(source="vci")

# Lần đầu tiên: lấy từ API
all_stocks = listing.all_symbols()
all_stocks.to_csv('stocks_cache.csv', index=False)

# Lần tiếp theo: đọc từ file
all_stocks = pd.read_csv('stocks_cache.csv')
```

### Tip 2: Lọc Sau Khi Lấy Dữ Liệu (Không Lọc Trong Method)

Vì các method trả về tất cả dữ liệu không có parameter lọc, hãy lọc bằng DataFrame:

```python
from vnstock_data import Listing

listing = Listing(source="vci")

# ĐÚNG: Lấy tất cả rồi lọc
df_ind = listing.symbols_by_industries()
banks = df_ind[df_ind['icb_name3'] == 'Ngân hàng']

# SAI: Không có parameter industry=...
# df = listing.symbols_by_industries(industry="Ngân hàng")  # ❌ Sai
```

### Tip 3: Tạo Mapping Giữa Symbol và Company Name

```python
from vnstock_data import Listing

listing = Listing(source="vci")
all_stocks = listing.all_symbols()

# Tạo mapping
symbol_to_name = dict(zip(all_stocks['symbol'], all_stocks['organ_name']))

# Sử dụng
print(symbol_to_name.get('VCB', 'Không tìm thấy'))
```

### Tip 4: Kiểm tra Source Được Hỗ Trợ Trước Khi Dùng

```python
from vnstock_data import Listing

# Kiểm tra source trước
listing = Listing(source="vci")  # VCI support tất cả

# Nếu dùng VND, chỉ có all_symbols()
listing_vnd = Listing(source="vnd")
df = listing_vnd.all_symbols()  # ✅ OK
# industries = listing_vnd.symbols_by_industries()  # ❌ Lỗi
```

## Sai Lầm Cần Tránh

### 1: Giả Định Tất Cả Nguồn Hỗ Trợ Tất Cả Methods

**Sai**:
```python
listing = Listing(source="vnd")
df = listing.symbols_by_industries()  # ❌ VND không support
```

**Đúng**:
```python
listing = Listing(source="vci")  # VCI support tất cả
df = listing.symbols_by_industries()
```

### 2: Giả Định Method Có Parameter Lọc

**Sai**:
```python
# Method không có parameter industry
df = listing.symbols_by_industries(industry="Ngân hàng")  # ❌ Sai
```

**Đúng**:
```python
df = listing.symbols_by_industries()  # Lấy tất cả
banks = df[df['icb_name3'] == 'Ngân hàng']  # Lọc sau
```

### 3: Không Cache Danh Sách Cổ Phiếu

**Sai**:
```python
# Gọi API nhiều lần không cần thiết
for i in range(100):
    listing = Listing(source="vci")
    all_stocks = listing.all_symbols()  # ❌ Gọi 100 lần
```

**Đúng**:
```python
listing = Listing(source="vci")
all_stocks = listing.all_symbols()  # Gọi 1 lần

for i in range(100):
    # Dùng dữ liệu đã cache
    vn30 = all_stocks[all_stocks['symbol'].isin(vn30_list)]
```

### 4: Không Check Kết Quả Rỗng

**Sai**:
```python
df = listing.all_symbols()
print(df.head())  # Có thể bị lỗi nếu trống
```

**Đúng**:
```python
df = listing.all_symbols()
if df.empty:
    print("Không lấy được dữ liệu!")
else:
    print(df.head())
```
