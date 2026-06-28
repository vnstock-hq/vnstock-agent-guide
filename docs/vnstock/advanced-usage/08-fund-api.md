# 07 - Fund API - Dữ Liệu Quỹ Đầu Tư

## 📖 Giới Thiệu

**Fund API** cung cấp thông tin chi tiết về các quỹ đầu tư mở từ Fmarket, bao gồm danh sách quỹ, hiệu suất, và giá trị tài sản ròng (NAV).

## 🔌 Nguồn Dữ Liệu

| Nguồn | Hỗ Trợ | Loại Dữ Liệu |
|-------|--------|-------------|
| **Fmarket** | ✅ | Quỹ đầu tư mở (58 quỹ) |

## 🚀 Bắt Đầu

```python
from vnstock import Fund

# Khởi tạo
fund = Fund()

# Xem danh sách quỹ
funds_list = fund.listing()
print(f"Tổng quỹ: {len(funds_list)}")
print(funds_list.head())
```

## 📚 Phương Thức Chính

### 1. listing() - Danh Sách Quỹ

Lấy danh sách tất cả các quỹ mở hiện có trên Fmarket.

**Tham số:**
- `fund_type` (str, tùy chọn): Loại quỹ
  - `""` - Tất cả quỹ (mặc định)
  - `"STOCK"` - Quỹ cổ phiếu
  - `"BOND"` - Quỹ trái phiếu
  - `"BALANCED"` - Quỹ cân bằng

**Trả về:** `pd.DataFrame` (58 dòng, 21 cột)

**Các cột chính:**
- `short_name` - Mã quỹ, ví dụ: "DCDS", "VFMVFQ" (str)
- `name` - Tên đầy đủ quỹ (str)
- `fund_type` - Loại quỹ (str)
- `fund_owner_name` - Công ty quản lý (str)
- `management_fee` - Phí quản lý hàng năm (float64, %)
- `inception_date` - Ngày thành lập (str, "YYYY-MM-DD")
- `nav` - Giá NAV hiện tại (float64, VND)
- `nav_update_at` - Ngày cập nhật NAV (str)

**Cột Lợi Suất (Return, %):**
- `nav_change_previous` - Thay đổi từ phiên trước (float64, %)
- `nav_change_last_year` - Lợi suất năm ngoái (float64, %)
- `nav_change_1m` - Lợi suất 1 tháng (float64, %)
- `nav_change_3m` - Lợi suất 3 tháng (float64, %)
- `nav_change_6m` - Lợi suất 6 tháng (float64, %)
- `nav_change_12m` - Lợi suất 1 năm (float64, %)
- `nav_change_24m` - Lợi suất 2 năm (float64, %)
- `nav_change_36m` - Lợi suất 3 năm (float64, %)
- `nav_change_36m_annualized` - Lợi suất 3 năm (annualized, %)
- `nav_change_inception` - Lợi suất từ khi thành lập (float64, %)

**Ví dụ:**
```python
from vnstock import Fund

fund = Fund()

# Tất cả quỹ
all_funds = fund.listing()
print(f"Tổng quỹ: {len(all_funds)}")  # 58

# Quỹ cổ phiếu
stock_funds = fund.listing(fund_type="STOCK")
print(f"Quỹ cổ phiếu: {len(stock_funds)}")

# Top 5 quỹ theo lợi suất 1 năm
top_5 = all_funds.nlargest(5, 'nav_change_12m')
print(top_5[['short_name', 'name', 'nav', 'nav_change_12m']])
```

**Output:**
```
  short_name                        name        nav  nav_change_12m
0       DCDS  QUỸ ĐẦU TƯ...      105760.69          33.25
1      SSISCA  QUỸ ĐẦU TƯ...       45770.78          15.17
2       BVFED  QUỸ ĐẦU TƯ...       31194.00          40.72
```

## 💡 Ví Dụ Thực Tế

### So Sánh Hiệu Suất Quỹ

```python
from vnstock import Fund

fund = Fund()

# Lấy quỹ cổ phiếu
stock_funds = fund.listing(fund_type="STOCK")

# So sánh lợi suất
comparison = stock_funds[[
    'short_name', 'name', 'nav', 
    'nav_change_12m', 'nav_change_36m', 
    'nav_change_36m_annualized'
]].copy()

# Sắp xếp theo lợi suất 1 năm
comparison_sorted = comparison.sort_values('nav_change_12m', ascending=False)
print("Top 10 quỹ cổ phiếu (lợi suất 1 năm):")
print(comparison_sorted.head(10).to_string())
```

### Phân Loại Quỹ

```python
from vnstock import Fund

fund = Fund()
all_funds = fund.listing()

# Đếm theo loại quỹ
fund_types = all_funds['fund_type'].value_counts()
print("Phân loại quỹ:")
print(fund_types)

# Trung bình phí quản lý theo loại
avg_fee = all_funds.groupby('fund_type')['management_fee'].mean()
print("\nPhí quản lý trung bình (%):")
print(avg_fee)
```

### Tìm Quỹ Phù Hợp

```python
from vnstock import Fund

fund = Fund()
all_funds = fund.listing()

# Tiêu chí: lợi suất 1 năm cao, phí quản lý thấp
filtered = all_funds[
    (all_funds['nav_change_12m'] > 20) &  # Lợi suất > 20%
    (all_funds['management_fee'] < 1.5)   # Phí < 1.5%
].copy()

filtered['score'] = (
    filtered['nav_change_12m'] - 
    filtered['management_fee'] * 5
)

top_picks = filtered.nlargest(10, 'score')
print("Top quỹ theo tiêu chí:")
print(top_picks[[
    'short_name', 'nav_change_12m', 'management_fee', 'score'
]])
```

## 📊 Loại Quỹ

### Quỹ Cổ Phiếu (Stock Funds)

- **Mục tiêu**: Tăng trưởng vốn
- **Danh mục**: 80-100% cổ phiếu
- **Rủi ro**: Cao
- **Horizon**: Dài hạn (3-5+ năm)

### Quỹ Trái Phiếu (Bond Funds)

- **Mục tiêu**: Sinh lợi tức ổn định
- **Danh mục**: 80-100% trái phiếu
- **Rủi ro**: Thấp đến trung bình
- **Horizon**: Trung bình đến dài hạn

### Quỹ Cân Bằng (Balanced Funds)

- **Mục tiêu**: Cân bằng giữa tăng trưởng và lợi tức
- **Danh mục**: Hỗn hợp cổ phiếu + trái phiếu
- **Rủi ro**: Trung bình
- **Horizon**: Trung bình (2-3+ năm)

## ⚠️ Ghi Chú Quan Trọng

1. **58 Quỹ Đủ**: Hiện tại có 58 quỹ mở trên Fmarket
2. **NAV Hàng Ngày**: Giá NAV được cập nhật hàng ngày
3. **Lợi Suất Quá Khứ**: Không đảm bảo lợi suất tương lai
4. **Phí Quản Lý**: Đã tính vào lợi suất trả về
5. **Chi Tiết Quỹ**: Hiện tại API không hỗ trợ `details.overview()`, `details.nav_history()`, `details.holdings()`

## 🔗 Xem Thêm

- **[02-Installation](02-installation.md)** - Cài đặt
- **[08-Best Practices](08-best-practices.md)** - Mẹo tối ưu hóa

---

**Last Updated**: 2024-12-04  
**Version**: 3.3.0  
**Status**: Verified with actual data ✅
