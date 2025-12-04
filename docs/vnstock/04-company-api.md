# 04 - Company API - Thông Tin Công Ty

## 📖 Giới Thiệu

**Company API** cung cấp thông tin chi tiết về các công ty cổ phần, bao gồm hồ sơ cơ bản, cấu trúc cổ đông, nhân viên quản lý, sự kiện công ty, và tin tức.

## 🔌 Nguồn Dữ Liệu

| Nguồn | Hỗ Trợ | Ghi Chú |
|-------|--------|--------|
| VCI | ✅ | Web scraping |
| TCBS | ✅ | Web scraping |

## 🚀 Bắt Đầu

```python
from vnstock import Company

# Khởi tạo
company = Company(source="vci", symbol="VCI")

# Xem thông tin cổ đông
shareholders = company.shareholders()
print(shareholders)
```

## 📚 Phương Thức Chính

### 1. overview() - Thông Tin Cơ Bản

Lấy thông tin tổng quan về công ty.

**Tham số:** Không có

**Trả về:** `pd.DataFrame` (1 dòng) với các cột:
- `symbol` - Mã chứng khoán
- `issue_share` - Số cổ phiếu phát hành
- `company_profile` - Hồ sơ công ty (JSON)
- `icb_name2`, `icb_name3`, `icb_name4` - Phân loại ngành (ICB)
- `financial_ratio_issue_share` - Thông tin tài chính
- `charter_capital` - Vốn điều lệ

**Ví dụ:**
```python
company = Company(source="vci", symbol="VCI")
overview = company.overview()
print(overview.shape)  # (1, 10)
```

### 2. shareholders() - Cổ Đông Chính

Lấy danh sách các cổ đông lớn.

**Tham số:** Không có

**Trả về:** `pd.DataFrame` với các cột:
- `id` - ID cổ đông
- `share_holder` - Tên cổ đông (str)
- `quantity` - Số cổ phiếu sở hữu (int64)
- `share_own_percent` - Tỷ lệ sở hữu (float64, %)
- `update_date` - Ngày cập nhật (str, format: "YYYY-MM-DD")

**Ví dụ:**
```python
company = Company(source="vci", symbol="VCI")
shareholders = company.shareholders()
print(shareholders.shape)  # (31, 5)
print(shareholders[['share_holder', 'quantity', 'share_own_percent']].head(3))
```

**Output:**
```
       share_holder   quantity  share_own_percent
0          Tô Hải  129139403            0.17870
1    PYN Elite Fund    8132100            0.04910
2 Nguyễn Phan Minh Khôi    7483872            0.04591
```

### 3. officers() - Nhân Viên Quản Lý

Lấy danh sách nhân viên quản lý (Ban điều hành, Hội đồng quản trị).

**Tham số:**
- `filter_by` (str, tùy chọn): Loại lọc
  - `"all"` - Tất cả (mặc định)
  - `"ceo"` - Chỉ CEO
  - `"boc"` - Board of Directors

**Trả về:** `pd.DataFrame` với các cột:
- `id` - ID nhân viên
- `officer_name` - Tên nhân viên (str)
- `officer_position` - Vị trí công việc (str, VN)
- `position_short_name` - Viết tắt vị trí (str)
- `update_date` - Ngày cập nhật (str)
- `officer_own_percent` - Tỷ lệ sở hữu cổ phiếu (float64, %)
- `quantity` - Số cổ phiếu sở hữu (int64)
- `type` - Trạng thái ("đang làm việc", "đã từng làm việc")

**Ví dụ:**
```python
company = Company(source="vci", symbol="VCI")
officers = company.officers(filter_by="all")
print(officers.shape)  # (20, 8)
print(officers[['officer_name', 'officer_position', 'quantity']].head(3))
```

### 4. subsidiaries() - Công Ty Con

Lấy danh sách công ty con.

**Tham số:**
- `filter_by` (str, tùy chọn): 
  - `"subsidiary"` - Công ty con trực tiếp
  - `"all"` - Tất cả

**Trả về:** `pd.DataFrame`

⚠️ **Lưu ý:** Phương thức này có thể trả về lỗi nếu không có dữ liệu

### 5. affiliate() - Công Ty Liên Kết

Lấy danh sách công ty liên kết.

**Tham số:** Không có

**Trả về:** `pd.DataFrame`

⚠️ **Lưu ý:** Phương thức này có thể trả về lỗi nếu không có dữ liệu

### 6. news() - Tin Tức

Lấy tin tức gần đây về công ty.

**Tham số:** Không có

**Trả về:** `pd.DataFrame` với các cột:
- `id`, `news_id` - ID tin tức
- `news_title` - Tiêu đề (str)
- `news_sub_title` - Phụ đề
- `friendly_sub_title` - Phụ đề thân thiện
- `news_image_url` - URL hình ảnh
- `news_source_link` - Liên kết nguồn
- `created_at`, `public_date`, `updated_at` - Thời gian (timestamp)
- `news_short_content` - Nội dung tóm tắt (HTML)
- `news_full_content` - Nội dung đầy đủ (HTML)
- `close_price`, `ref_price`, `floor`, `ceiling` - Dữ liệu giá (int64)
- `price_change_pct` - Thay đổi giá (float64, %)

**Ví dụ:**
```python
company = Company(source="vci", symbol="VCI")
news = company.news()
print(news.shape)  # (10, 18)
print(news[['news_title', 'public_date']].head(3))
```

### 7. events() - Sự Kiện Công Ty

Lấy danh sách sự kiện công ty (chia cổ tức, phát hành cổ phiếu, niêm yết, v.v.).

**Tham số:** Không có

**Trả về:** `pd.DataFrame` với các cột:
- `id` - ID sự kiện
- `event_title` - Tiêu đề sự kiện (str, VN)
- `en__event_title` - Tiêu đề sự kiện (str, EN)
- `public_date` - Ngày công bố (str)
- `issue_date` - Ngày phát hành (str)
- `source_url` - Liên kết tài liệu
- `event_list_code` - Mã loại sự kiện (str)
- `event_list_name` - Tên loại sự kiện (str, VN)
- `en__event_list_name` - Tên loại sự kiện (str, EN)
- `ratio` - Tỷ lệ (float64, VD: 0.35 = 35%)
- `value` - Giá trị (float64)
- `record_date` - Ngày ghi danh (str)
- `exright_date` - Ngày hết quyền (str)

**Ví dụ:**
```python
company = Company(source="vci", symbol="VCI")
events = company.events()
print(events.shape)  # (30, 13)
print(events[['event_title', 'event_list_name', 'public_date']].head(5))
```

**Output:**
```
                               event_title        event_list_name public_date
0  VCI-Phát hành cổ phiếu thưởng tỷ lệ 10:3,5  Phát hành cổ phiếu  2018-06-29
1  VCI-Chính thức niêm yết cổ phiếu trên HOSE      Niêm yết mới    2017-06-30
2  VCI- Niêm yết bổ sung 132.569.480 cổ phiếu    Niêm yết thêm   2024-10-11
```

## 💡 Ví Dụ Thực Tế

### Phân Tích Cấu Trúc Cổ Đông

```python
from vnstock import Company

company = Company(source="vci", symbol="VCI")
shareholders = company.shareholders()

# Top 5 cổ đông lớn
top_5 = shareholders.nlargest(5, 'quantity')
print("Top 5 cổ đông:")
print(top_5[['share_holder', 'quantity', 'share_own_percent']])

# Tính tập trung cổ đông
top_10_pct = shareholders.nlargest(10, 'share_own_percent')['share_own_percent'].sum()
print(f"\nTrong lượng cổ đông top 10: {top_10_pct:.2f}%")
```

### Theo Dõi Ban Quản Trị

```python
from vnstock import Company

company = Company(source="vci", symbol="VCI")
officers = company.officers()

# Các vị trí lãnh đạo
positions = officers['officer_position'].unique()
print(f"Số lượng vị trí quản lý: {len(positions)}")

# Cổ đông sáng lập/nội bộ
insiders = officers[officers['quantity'] > 0].sort_values('quantity', ascending=False)
print(f"\nNhân viên nội bộ sở hữu cổ phiếu: {len(insiders)}")
print(insiders[['officer_name', 'officer_position', 'quantity']])
```

### Theo Dõi Sự Kiện

```python
from vnstock import Company

company = Company(source="vci", symbol="VCI")
events = company.events()

# Sự kiện chia cổ tức
dividend_events = events[events['event_list_code'] == 'DIV']
print(f"Số lần chia cổ tức: {len(dividend_events)}")

# Sự kiện phát hành cổ phiếu
issue_events = events[events['event_list_code'] == 'ISS']
print(f"Số lần phát hành cổ phiếu: {len(issue_events)}")
print(issue_events[['event_title', 'public_date', 'ratio']])
```

## ⚠️ Ghi Chú Quan Trọng

1. **Dữ liệu không đầy đủ**: Không phải công ty nào cũng có đầy đủ thông tin cho tất cả phương thức
2. **Giá trị NaN**: Nếu không có dữ liệu, sẽ trả về `NaN` hoặc rỗng
3. **Phụ thuộc vào nguồn**: Thông tin khác nhau giữa VCI và TCBS
4. **Dữ liệu lịch sử**: Thông tin lịch sử được cập nhật định kỳ

## 🔗 Xem Thêm

- **[03-Listing API](03-listing-api.md)** - Tìm kiếm chứng khoán
- **[05-Trading API](05-trading-api.md)** - Dữ liệu giao dịch
- **[06-Financial API](06-financial-api.md)** - Dữ liệu tài chính
- **[08-Best Practices](08-best-practices.md)** - Mẹo tối ưu hóa

---

**Last Updated**: 2024-12-04  
**Version**: 3.3.0  
**Status**: Verified with actual data ✅
