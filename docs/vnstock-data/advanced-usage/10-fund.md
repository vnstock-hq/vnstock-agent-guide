# Fund - Dữ Liệu Quỹ ETF & Chứng Chỉ Quỹ

Lớp `Fund` cung cấp dữ liệu về quỹ ETF và chứng chỉ quỹ từ Fmarket (nguồn dữ liệu chuyên về quỹ đầu tư tại Việt Nam).

## Khởi Tạo

```python
from vnstock_data import Fund

# Khởi tạo cơ bản
fund = Fund()

# Khởi tạo với random user agent (để tránh bị block)
fund = Fund(random_agent=True)
```

### Tham Số Khởi Tạo

- `random_agent` (bool, default=False): Sử dụng random user agent để tránh bị block API

**Lưu ý**: Chỉ **Fmarket** hỗ trợ Fund.

## Phương Thức

### 1. listing() - Danh sách tất cả quỹ

```python
# Lấy danh sách tất cả quỹ
df = fund.listing()

# Lọc theo loại quỹ
df = fund.listing(fund_type="STOCK")  # "STOCK", "BOND", "BALANCED" hoặc rỗng
```

**Tham Số**:
- `fund_type` (str, default=""): Loại quỹ - `STOCK`, `BOND`, `BALANCED` hoặc rỗng để lấy tất cả

**Trả về**: DataFrame với 21 cột gồm:
- `short_name` (str): Mã quỹ (ví dụ: SSISCA, DCDS)
- `name` (str): Tên đầy đủ quỹ
- `fund_type` (str): Loại quỹ (Quỹ cổ phiếu, Quỹ trái phiếu, v.v.)
- `fund_owner_name` (str): Tên công ty quản lý
- `management_fee` (float64): Phí quản lý năm (%)
- `inception_date` (str): Ngày thành lập
- `nav` (float64): Giá trị tài sản ròng (NAV) hiện tại
- `nav_change_*` (float64): % thay đổi NAV (previous, last_year, inception, 1m, 3m, 6m, 12m, 24m, 36m, 36m_annualized)
- `nav_update_at` (str): Ngày cập nhật NAV
- `fund_id_fmarket`, `fund_code`, `vsd_fee_id` (mixed): ID và mã khác

**Ví dụ** (3 dòng đầu tiên):
```
  short_name                                        name     fund_type        nav  management_fee inception_date
0       DCDS         QUỸ ĐẦU TƯ CHỨNG KHOÁN NĂNG ĐỘNG DC  Quỹ cổ phiếu  103858.67            1.95     2004-05-19
1     SSISCA  QUỸ ĐẦU TƯ LỢI THẾ CẠNH TRANH BỀN VỮNG SSI  Quỹ cổ phiếu   44822.70            1.75     2014-09-25
2      BVFED      QUỸ ĐẦU TƯ CỔ PHIẾU NĂNG ĐỘNG BẢO VIỆT  Quỹ cổ phiếu   30563.00            1.00     2014-01-07
```

### 2. filter() - Tìm quỹ theo mã

```python
# Tìm quỹ SSISCA
df = fund.filter(symbol="SSISCA")
```

**Tham Số**:
- `symbol` (str, default=""): Mã quỹ cần tìm (ví dụ: SSISCA, DCDS)

**Trả về**: DataFrame với 2 cột:
- `id` (int64): ID của quỹ trong Fmarket
- `shortName` (str): Mã quỹ

**Ví dụ**:
```
   id shortName
0  11    SSISCA
```

### 3. top_holding() - Top cổ phiếu trong quỹ

```python
# Lấy top cổ phiếu của quỹ SSISCA (fundId=11)
df = fund.top_holding(fundId=11)
```

**Tham Số**:
- `fundId` (int, default=23): ID của quỹ (lấy từ `filter()`)

**Trả về**: DataFrame với 6 cột:
- `stock_code` (str): Mã cổ phiếu (ví dụ: MWG, MBB, HPG)
- `industry` (str): Ngành của cổ phiếu
- `net_asset_percent` (float64): % tài sản ròng đầu tư vào cổ phiếu này
- `type_asset` (str): Loại tài sản (STOCK, BOND)
- `update_at` (str): Ngày cập nhật
- `fundId` (int64): ID quỹ

**Ví dụ** (top 3 cổ phiếu của SSISCA):
```
  stock_code           industry  net_asset_percent type_asset   update_at  fundId
0        MWG             Bán lẻ               8.48      STOCK  2025-11-06      11
1        MBB          Ngân hàng               6.42      STOCK  2025-11-06      11
2        HPG  Vật liệu xây dựng               6.13      STOCK  2025-11-06      11
```

### 4. industry_holding() - Cấu trúc ngành trong quỹ

```python
# Lấy cấu trúc ngành của quỹ SSISCA
df = fund.industry_holding(fundId=11)
```

**Tham Số**:
- `fundId` (int, default=23): ID của quỹ

**Trả về**: DataFrame với 2 cột:
- `industry` (str): Tên ngành
- `net_asset_percent` (float64): % tài sản ròng đầu tư vào ngành

**Ví dụ** (5 ngành cuối cùng):
```
                    industry  net_asset_percent
9        Thực phẩm - Đồ uống               3.14
10                  Tiện ích               2.32
11  Sản xuất Nhựa - Hóa chất               2.23
12                      Khác               1.51
13                  Bán buôn               0.84
```

### 5. nav_report() - Lịch sử NAV quỹ

```python
# Lấy toàn bộ lịch sử NAV của quỹ SSISCA
df = fund.nav_report(fundId=11)
```

**Tham Số**:
- `fundId` (int, default=23): ID của quỹ

**Trả về**: DataFrame với 2 cột:
- `date` (str): Ngày (format: YYYY-MM-DD)
- `nav_per_unit` (float64): NAV trên một đơn vị quỹ

**Ví dụ** (3 dòng gần nhất):
```
            date  nav_per_unit
2016  2025-11-27      44918.76
2017  2025-11-28      45014.93
2018  2025-12-01      44822.70
```

Số lượng dòng có thể lên đến hàng nghìn (ví dụ: 2019 dòng cho SSISCA từ ngày thành lập).

### 6. asset_holding() - Cấu trúc tài sản trong quỹ

```python
# Lấy cấu trúc tài sản của quỹ SSISCA
df = fund.asset_holding(fundId=11)
```

**Tham Số**:
- `fundId` (int, default=23): ID của quỹ

**Trả về**: DataFrame với 2 cột:
- `asset_percent` (float64): % tài sản
- `asset_type` (str): Loại tài sản (Cổ phiếu, Trái phiếu, Tiền mặt, v.v.)

**Ví dụ** (cấu trúc tài sản SSISCA):
```
   asset_percent                asset_type
0          95.66                  Cổ phiếu
1           0.28                      Khác
2           4.06  Tiền và tương đương tiền
```

## Ví Dụ Sử Dụng

```python
from vnstock_data import Fund
import pandas as pd

fund = Fund()

# 1. Lấy danh sách quỹ cổ phiếu
funds = fund.listing(fund_type="STOCK")
print(f"Tổng số quỹ cổ phiếu: {len(funds)}")

# 2. Tìm quỹ SSISCA
fund_info = fund.filter(symbol="SSISCA")
fund_id = fund_info['id'].iloc[0]
print(f"Quỹ SSISCA (ID={fund_id})")

# 3. Xem top 5 cổ phiếu của quỹ
top_stocks = fund.top_holding(fundId=fund_id)
print("\nTop 5 cổ phiếu:")
print(top_stocks[['stock_code', 'industry', 'net_asset_percent']].head(5))

# 4. Xem cấu trúc ngành
industries = fund.industry_holding(fundId=fund_id)
print(f"\nQuỹ đầu tư vào {len(industries)} ngành")
print(industries.nlargest(5, 'net_asset_percent'))

# 5. Xem NAV hiện tại
nav_history = fund.nav_report(fundId=fund_id)
latest_nav = nav_history.iloc[-1]
print(f"\nNAV hiện tại (2025-12-01): {latest_nav['nav_per_unit']:,.2f} VND")

# 6. Xem cấu trúc tài sản
assets = fund.asset_holding(fundId=fund_id)
print("\nCấu trúc tài sản:")
print(assets)
```

## Phân Tích Ví Dụ

```python
from vnstock_data import Fund
import pandas as pd
import matplotlib.pyplot as plt

fund = Fund()

# Phân tích lợi suất quỹ qua thời gian
funds_list = fund.listing()

# So sánh lợi suất 3 tháng của các quỹ
funds_3m = funds_list.nlargest(5, 'nav_change_3m')[['short_name', 'name', 'nav_change_3m']]
print("Top 5 quỹ tăng trưởng trong 3 tháng gần nhất:")
print(funds_3m)

# So sánh phí quỹ
funds_low_fee = funds_list.nsmallest(5, 'management_fee')[['short_name', 'management_fee']]
print("\n5 quỹ có phí quản lý thấp nhất:")
print(funds_low_fee)

# Tìm quỹ với lợi suất tốt nhất năm
funds_1y = funds_list.nlargest(5, 'nav_change_12m')[['short_name', 'nav_change_12m']]
print("\nTop 5 quỹ tăng trưởng trong 12 tháng gần nhất:")
print(funds_1y)

# Phân tích quỹ SSISCA
ssisca_info = funds_list[funds_list['short_name'] == 'SSISCA'].iloc[0]
print(f"\n--- Phân tích quỹ SSISCA ---")
print(f"NAV hiện tại: {ssisca_info['nav']:,.2f}")
print(f"Phí quản lý: {ssisca_info['management_fee']:.2f}%")
print(f"Lợi suất YTD: {ssisca_info['nav_change_last_year']:.2f}%")
print(f"Lợi suất 3 năm: {ssisca_info['nav_change_36m']:.2f}%")

# Phân tích NAV qua thời gian
fund_id = 11  # SSISCA
nav_data = fund.nav_report(fundId=fund_id)
nav_data['date'] = pd.to_datetime(nav_data['date'])
nav_data['year'] = nav_data['date'].dt.year

# Tính lợi suất hàng năm
yearly_returns = []
for year in nav_data['year'].unique():
    year_data = nav_data[nav_data['year'] == year]
    if len(year_data) > 0:
        start_nav = year_data.iloc[0]['nav_per_unit']
        end_nav = year_data.iloc[-1]['nav_per_unit']
        yearly_return = (end_nav - start_nav) / start_nav * 100
        yearly_returns.append({'year': year, 'return': yearly_return})

print("\nLợi suất hàng năm (SSISCA):")
for yr in yearly_returns[-5:]:  # 5 năm gần nhất
    print(f"  {yr['year']}: {yr['return']:.2f}%")
```

## Ma Trận Support

| Phương Thức | Fmarket |
|---|:---:|
| listing | ✅ |
| filter | ✅ |
| top_holding | ✅ |
| industry_holding | ✅ |
| nav_report | ✅ |
| asset_holding | ✅ |

**Khuyến Nghị**: Fmarket là nguồn dữ liệu chính dành cho quỹ.

## Use Case

- **Lựa chọn quỹ**: So sánh NAV, phí, lợi suất giữa các quỹ
- **Phân tích danh mục**: Xem quỹ đầu tư vào các cổ phiếu/ngành nào
- **Tracking hiệu suất**: Theo dõi NAV qua thời gian
- **Asset allocation**: Xác định tỷ lệ cổ phiếu/trái phiếu/tiền mặt
- **Diversification**: Quỹ cung cấp đa dạng tài sản tự động

## Best Practices

1. **So sánh phí**: Phí thấp hơn → lợi suất ròng cao hơn
   - Ví dụ: BVFED có phí 1.00% (thấp nhất), DCDS 1.95%

2. **Kiểm tra lợi suất dài hạn**: Xem lợi suất 3 năm, 5 năm chứ không chỉ ngắn hạn
   - `nav_change_36m`: lợi suất 3 năm
   - `nav_change_36m_annualized`: lợi suất năm hóa

3. **Phân tích cấu trúc**: Hiểu quỹ đầu tư vào đâu
   - Cổ phiếu giá trị? Cổ phiếu tăng trưởng? Trái phiếu?
   - Ngành nào? Công ty lớn hay nhỏ?

4. **Theo dõi NAV**: NAV tăng = lợi suất tốt
   - Xem NAV history để phát hiện xu hướng
   - So sánh với chỉ số thị trường (VNINDEX)

5. **Lưu ý rủi ro**: Cổ phiếu volatile, trái phiếu ổn định
   - Cân bằng theo mục tiêu đầu tư của bạn
