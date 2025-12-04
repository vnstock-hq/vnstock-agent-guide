# 03 - Listing API - Tìm Kiếm & Lọc Chứng Khoán

## 📖 Giới Thiệu

Listing API cung cấp các phương thức tìm kiếm, lọc và lấy thông tin về các chứng khoán có sẵn trên thị trường. Dữ liệu bao gồm:

- Danh sách tất cả mã chứng khoán
- Lọc theo sàn giao dịch (HOSE, HNX, UPCOM)
- Lọc theo ngành công nghiệp (ICB)
- Lọc theo chỉ số (VN30, VNMID, VNSML, etc.)
- Futures, Bonds, Warrants, Funds
- Industries & Sector classification

## 🏗️ Khởi Tạo

```python
from vnstock import Listing

# Khởi tạo Listing adapter
# Hỗ trợ VCI, MSN
listing = Listing(
    source="vci",           # Nguồn dữ liệu
    random_agent=False,     # Sử dụng random user agent
    show_log=True           # Hiển thị log chi tiết
)

# Hoặc với TCBS (nếu có hỗ trợ)
# listing = Listing(source="msn")
```

## 📋 Các Phương Thức

### 1. all_symbols() - Tất Cả Mã Chứng Khoán

Lấy danh sách tất cả mã chứng khoán.

**Parameters:**

```
- to_df (bool): Trả về DataFrame (default: True)
- lang (str): Ngôn ngữ ('vi' hoặc 'en')
```

**Ví dụ:**

```python
# Trả về DataFrame
df = listing.all_symbols(to_df=True)
print(df.head())
# Output:
#   symbol     company_name   exchange  industry
# 0   AAA      AAA Company      HOSE     Real Estate
# 1   AAH      AAH Company      HOSE     Finance
# 2   AAT      AAT Company      HOSE     Telecom
# ...

# Trả về list
symbols = listing.all_symbols(to_df=False)
print(symbols[:10])
# Output: ['AAA', 'AAH', 'AAT', 'ABS', 'ABT', ...]

# Tiếng Anh
df_en = listing.all_symbols(lang='en')
print(df_en[['symbol', 'company_name', 'industry']].head())
```

**Kiến Thức:**

```python
# Lấy số lượng mã
total_symbols = len(listing.all_symbols())
print(f"Total symbols: {total_symbols}")

# Tìm công ty theo tên
all_df = listing.all_symbols(to_df=True)
banking = all_df[all_df['industry'] == 'Finance']
print(banking[['symbol', 'company_name']])

# Export ra CSV
all_df.to_csv('all_symbols.csv', index=False)
```

### 2. symbols_by_exchange() - Lọc Theo Sàn

Lấy danh sách mã chứng khoán theo sàn giao dịch.

**Parameters:**

```
- exchange (str): Sàn giao dịch
  ├─ 'HOSE': Sở giao dịch Hà Nội (HOSE) - Thị trường chính
  ├─ 'HNX': Sở giao dịch Hà Nội (HNX) - Thị trường phụ
  └─ 'UPCOM': Chứng khoán chưa niêm yết (UPCOM)
- lang (str): Ngôn ngữ ('vi' hoặc 'en')
```

**Ví dụ:**

```python
# Lấy các mã HOSE
hose_symbols = listing.symbols_by_exchange(exchange="HOSE")
print(f"Total HOSE symbols: {len(hose_symbols)}")
print(f"First 10: {hose_symbols[:10]}")

# Lấy các mã HNX
hnx_symbols = listing.symbols_by_exchange(exchange="HNX")
print(f"Total HNX symbols: {len(hnx_symbols)}")

# Lấy các mã UPCOM
upcom_symbols = listing.symbols_by_exchange(exchange="UPCOM")
print(f"Total UPCOM symbols: {len(upcom_symbols)}")

# Kết hợp
all_hose_hnx = hose_symbols + hnx_symbols
print(f"Total HOSE + HNX: {len(all_hose_hnx)}")
```

**Kiến Thức Nâng Cao:**

```python
# Đếm mã theo sàn
from collections import Counter

all_df = listing.all_symbols(to_df=True)
exchange_counts = all_df['exchange'].value_counts()
print(exchange_counts)
# Output:
# HOSE     1020
# HNX      140
# UPCOM     80
# Name: exchange, dtype: int64

# So sánh giữa các sàn
hose_df = all_df[all_df['exchange'] == 'HOSE']
hnx_df = all_df[all_df['exchange'] == 'HNX']

print(f"HOSE industries: {hose_df['industry'].nunique()}")
print(f"HNX industries: {hnx_df['industry'].nunique()}")
```

### 3. symbols_by_industries() - Lọc Theo Ngành

Lấy danh sách mã chứng khoán theo ngành công nghiệp.

**Parameters:**

```
- to_df (bool): Trả về DataFrame
- lang (str): Ngôn ngữ
```

**Ví dụ:**

```python
# Trả về DataFrame
df = listing.symbols_by_industries(to_df=True)
print(df.head())
# Output:
#   symbol  industry_id  industry_name  sector
# 0   AAA        130     Finance        Real Estate
# 1   ACB        130     Finance        Banking
# ...

# Lọc theo ngành
finance_df = df[df['industry_name'] == 'Finance']
print(f"Total Finance stocks: {len(finance_df)}")
print(finance_df[['symbol', 'company_name']].head())

# Lọc theo sector
real_estate = df[df['sector'] == 'Real Estate']
print(f"Real Estate symbols: {real_estate['symbol'].tolist()}")
```

**Kiến Thức Nâng Cao:**

```python
# Danh sách tất cả ngành
industries = listing.symbols_by_industries(to_df=True)
unique_industries = industries['industry_name'].unique()
print(f"Total industries: {len(unique_industries)}")
print(unique_industries)

# Số mã theo ngành
industry_counts = industries['industry_name'].value_counts()
print(industry_counts)
# Output:
# Finance           200
# Technology        150
# Real Estate       120
# ...

# Top 5 ngành có nhiều mã nhất
top_5 = industry_counts.head(5)
print(top_5)
```

### 4. industries_icb() - Phân Loại ICB

Lấy thông tin chi tiết về các ngành ICB (Industry Classification Benchmark).

**Parameters:**

```
- lang (str): Ngôn ngữ
```

**Ví dụ:**

```python
# Lấy danh sách ICB
icb_df = listing.industries_icb()
print(icb_df.head())
# Output:
#   icb_id  icb_code  icb_name            super_group
# 0  6001    1000     Oil & Gas           Energy
# 1  6002    1001     Coal                Energy
# 2  6003    1010     Alternative Energy Energy
# ...

# Thong tin chi tiet
print(f"Total ICB categories: {len(icb_df)}")
print(f"Columns: {icb_df.columns.tolist()}")

# Tim theo super_group
energy = icb_df[icb_df['super_group'] == 'Energy']
print(f"Energy sectors: {energy['icb_name'].tolist()}")
```

**Kiến Thức:**

```python
# Lấy danh sách các super_group
super_groups = icb_df['super_group'].unique()
print(f"Total super_groups: {len(super_groups)}")
for group in super_groups:
    sectors = icb_df[icb_df['super_group'] == group]
    print(f"{group}: {len(sectors)} sectors")
```

### 5. symbols_by_group() - Lọc Theo Chỉ Số

Lấy danh sách mã chứng khoán theo chỉ số (Index Group).

**Parameters:**

```
- group (str): Tên chỉ số
  ├─ VN30, VN100, VNMID, VNSML, VNALL, VNSI
  ├─ VNIT, VNIND, VNCONS, VNCOND, VNHEAL, VNENE
  ├─ VNUTI, VNREAL, VNFIN, VNMAT
  ├─ VNDIAMOND, VNFINLEAD, VNFINSELECT
  └─ VNX50, VNXALL
```

**Ví dụ:**

```python
# VN30 - 30 cổ phiếu vốn hóa lớn nhất
vn30 = listing.symbols_by_group(group="VN30")
print(f"VN30 symbols: {vn30}")
# Output: ['VCI', 'ACB', 'BID', 'CTD', 'CTG', ...]

# VNMID - Mid-cap
vnmid = listing.symbols_by_group(group="VNMID")
print(f"VNMID count: {len(vnmid)}")

# VNSML - Small-cap
vnsml = listing.symbols_by_group(group="VNSML")
print(f"VNSML count: {len(vnsml)}")

# Chỉ số ngành
vnit = listing.symbols_by_group(group="VNIT")  # IT
vnfin = listing.symbols_by_group(group="VNFIN")  # Finance
print(f"IT stocks: {len(vnit)}")
print(f"Finance stocks: {len(vnfin)}")
```

**Kiến Thức Nâng Cao:**

```python
from vnstock.constants import INDEX_GROUPS

# Lấy tất cả chỉ số
all_groups = []
for group_category, indices in INDEX_GROUPS.items():
    print(f"{group_category}: {indices}")
    all_groups.extend(indices)

# Lấy tất cả mã từ VN30 đến VN100
vn30_symbols = set(listing.symbols_by_group(group="VN30"))
vn100_symbols = set(listing.symbols_by_group(group="VN100"))

# Mã ở VN100 nhưng không ở VN30
vn31_to_100 = vn100_symbols - vn30_symbols
print(f"VN31-100 symbols: {sorted(list(vn31_to_100))}")
```

### 6. all_future_indices() - Futures

Lấy danh sách tất cả hợp đồng tương lai.

**Ví dụ:**

```python
# Lấy danh sách futures
futures_df = listing.all_future_indices()
print(futures_df.head())
# Output:
#   symbol  contract_name  maturity_date
# 0   VNI   VN Index Futures  2024-12-31
# 1   VI1   VN30 Dec24        2024-12-31
# ...

print(f"Total futures: {len(futures_df)}")
```

### 7. all_government_bonds() - Trái Phiếu Chính Phủ

Lấy danh sách trái phiếu chính phủ.

**Ví dụ:**

```python
# Lấy danh sách trái phiếu
bonds_df = listing.all_government_bonds()
print(bonds_df.head())
# Output:
#   symbol  bond_name  maturity_date  coupon
# 0  GB01   10Y Bond   2030-01-01     5.5%
# ...
```

### 8. all_covered_warrant() - Warrant

Lấy danh sách warrant được phủ (Covered Warrant).

**Ví dụ:**

```python
# Lấy danh sách warrant
warrants_df = listing.all_covered_warrant()
print(warrants_df[['symbol', 'underlying', 'expiry_date']].head())
```

### 9. all_bonds() - Trái Phiếu Doanh Nghiệp

Lấy danh sách trái phiếu doanh nghiệp.

**Ví dụ:**

```python
# Lấy danh sách corporate bonds
bonds_df = listing.all_bonds()
print(bonds_df[['symbol', 'issuer', 'coupon', 'maturity']].head())
```

## 🔄 Kết Hợp & Lọc Nâng Cao

### Ví dụ 1: Cổ Phiếu Lớn ở Ngành Tài Chính

```python
import pandas as pd
from vnstock import Listing

listing = Listing(source="vci")

# Lấy dữ liệu
all_symbols = listing.all_symbols(to_df=True)
industries = listing.symbols_by_industries(to_df=True)

# Kết hợp dữ liệu
merged = all_symbols.merge(industries, on='symbol', how='left')

# Lọc theo ngành Finance và sàn HOSE
finance_hose = merged[
    (merged['industry'] == 'Finance') & 
    (merged['exchange'] == 'HOSE')
]

print(f"Finance stocks on HOSE: {len(finance_hose)}")
print(finance_hose[['symbol', 'company_name']].head())
```

### Ví dụ 2: So Sánh VN30 vs VN31-100

```python
# Lấy dữ liệu
vn30_set = set(listing.symbols_by_group(group="VN30"))
vn100_set = set(listing.symbols_by_group(group="VN100"))

# VN30
print("VN30 symbols:")
print(sorted(vn30_set))

# VN31-100 (ở VN100 nhưng không ở VN30)
vn31_100 = sorted(vn100_set - vn30_set)
print(f"\nVN31-100 symbols ({len(vn31_100)} stocks):")
print(vn31_100)

# Lấy chi tiết của VN31-100
all_df = listing.all_symbols(to_df=True)
vn31_100_df = all_df[all_df['symbol'].isin(vn31_100)]
print("\nVN31-100 details:")
print(vn31_100_df[['symbol', 'company_name', 'industry']].to_string())
```

### Ví dụ 3: Ngành Công Nghệ

```python
# Lấy tất cả cổ phiếu IT
vnit_symbols = listing.symbols_by_group(group="VNIT")
print(f"IT stocks ({len(vnit_symbols)}): {vnit_symbols}")

# Lấy chi tiết
industries_df = listing.symbols_by_industries(to_df=True)
it_stocks = industries_df[industries_df['symbol'].isin(vnit_symbols)]
print("\nIT stocks details:")
print(it_stocks[['symbol', 'industry_name']].to_string())
```

### Ví dụ 4: Export Danh Sách

```python
# Export VN30
vn30 = listing.symbols_by_group(group="VN30")
with open('vn30_symbols.txt', 'w') as f:
    for symbol in vn30:
        f.write(symbol + '\n')

# Export tất cả cổ phiếu theo ngành
industries = listing.symbols_by_industries(to_df=True)
industries.to_excel('all_stocks_by_industry.xlsx', index=False)

# Export VN100 chi tiết
all_df = listing.all_symbols(to_df=True)
vn100_symbols = listing.symbols_by_group(group="VN100")
vn100_df = all_df[all_df['symbol'].isin(vn100_symbols)]
vn100_df.to_csv('vn100_details.csv', index=False)

print("✅ Exported successfully!")
```

## 📊 Performance & Caching

### Caching Dữ Liệu

```python
import pickle
import os
from vnstock import Listing

listing = Listing(source="vci")

CACHE_FILE = 'listing_cache.pkl'

# Lấy hoặc load từ cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'rb') as f:
        all_symbols = pickle.load(f)
    print("✅ Loaded from cache")
else:
    all_symbols = listing.all_symbols(to_df=True)
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(all_symbols, f)
    print("✅ Cached for next time")

print(all_symbols.head())
```

### Batch Operations

```python
# Lấy dữ liệu một lần, dùng nhiều lần
all_symbols = listing.all_symbols(to_df=True)
industries = listing.symbols_by_industries(to_df=True)
icb = listing.industries_icb()

# Lọc theo nhiều tiêu chí
hose_df = all_symbols[all_symbols['exchange'] == 'HOSE']
print(f"HOSE: {len(hose_df)}")

finance_df = hose_df[hose_df['industry'] == 'Finance']
print(f"HOSE Finance: {len(finance_df)}")
```

## ❌ Các Lỗi Thường Gặp

### Lỗi 1: ValueError - Invalid Source

```python
# ❌ Sai
listing = Listing(source="invalid")

# ✅ Đúng
listing = Listing(source="vci")  # hoặc "msn"
```

### Lỗi 2: Network/Timeout

```python
# Tăng timeout
from vnstock.config import Config
Config.TIMEOUT = 60

# Hoặc retry
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
def get_symbols():
    return listing.all_symbols()
```

### Lỗi 3: Empty Result

```python
# Nếu không có dữ liệu
symbols = listing.symbols_by_group(group="INVALID_INDEX")
if not symbols or len(symbols) == 0:
    print("⚠️ No symbols found for this group")
```

## 📚 Bước Tiếp Theo

1. [02-Installation](02-installation.md) - Cài đặt
2. [01-Overview](01-overview.md) - Tổng quan
3. ✅ **03-Listing API** - Bạn đã ở đây
4. [04-Quote & Price](04-quote-price-api.md) - Giá lịch sử
5. [05-Financial API](05-financial-api.md) - Dữ liệu tài chính
6. [06-Connector Guide](06-connector-guide.md) - API bên ngoài
7. [07-Best Practices](07-best-practices.md) - Mẹo & kinh nghiệm

---

**Last Updated**: 2024-12-03  
**Version**: 3.3.0  
**Status**: Actively Maintained
