# Company - Thông Tin Công Ty, Cổ Đông, Ban Lãnh Đạo

Lớp `Company` cung cấp thông tin chi tiết về các công ty niêm yết tại thị trường chứng khoán Việt Nam.

## Khởi Tạo

```python
from vnstock_data import Company

company = Company(source="vci", symbol="VCB")
```

**Lưu ý**: Hiện tại chỉ **VCI** hỗ trợ Company.

## Phương Thức

### overview() - Thông Tin Tổng Quan

```python
df = company.overview()
```

Trả về: DataFrame với 10 cột (shape: 1, 10)
- `symbol`: object (str) - Mã cổ phiếu
- `id`: object (str) - ID công ty
- `issue_share`: int64 - Số cổ phiếu phát hành
- `history`: object (str) - Lịch sử công ty
- `company_profile`: object (str) - Mô tả công ty
- `icb_name3`: object (str) - Ngành cấp 3
- `icb_name2`: object (str) - Ngành cấp 2
- `icb_name4`: object (str) - Ngành cấp 4
- `financial_ratio_issue_share`: int64 - Số CP phát hành (dùng cho tỷ lệ tài chính)
- `charter_capital`: int64 - Vốn điều lệ

### shareholders() - Cổ Đông Lớn

```python
df = company.shareholders()
```

Trả về: DataFrame với 5 cột
- `id`: object (str) - ID cổ đông
- `share_holder`: object (str) - Tên cổ đông
- `quantity`: int64 - Số cổ phần sở hữu
- `share_own_percent`: float64 - Tỷ lệ sở hữu (%)
- `update_date`: object (str) - Ngày cập nhật

**Ví dụ output** (3 cổ đông lớn VCB):
```
         share_holder    quantity  share_own_percent update_date
0   Ngân Hàng Nhà Nước Việt Nam  6250338579             0.7480  2025-11-21
1   Mizuho Bank Limited         1253366534             0.1500  2025-11-21
2   Quỹ Đầu tư Chính phủ Singapore (GIC)    84503639             0.0101  2025-10-05
```

### officers() - Ban Lãnh Đạo

```python
df = company.officers(filter_by='working')
```

**Tham số**:
- `filter_by`: `'working'` (đang làm), `'resigned'` (đã nghỉ), `'all'` - Mặc định là `'working'`

Trả về: DataFrame với 7 cột
- `id`: object (str) - ID người quản lý
- `officer_name`: object (str) - Tên người
- `officer_position`: object (str) - Vị trí chính
- `position_short_name`: object (str) - Tên vị trí viết tắt
- `update_date`: object (str) - Ngày cập nhật
- `officer_own_percent`: float64 - Tỷ lệ cổ phần sở hữu (%)
- `quantity`: int64 - Số cổ phần sở hữu

**Ví dụ output** (3 người quản lý VCB):
```
    officer_name                     officer_position update_date  officer_own_percent  quantity
0   Phùng Nguyễn Hải Yến   Phụ trách CBTT/Phó TGĐ  2025-07-30             0.000005     42339
1   Nguyễn Thanh Tùng      Phó Tổng Giám đốc     2025-10-03             0.000003     22324
2   Đào Minh Tuấn           Phó Tổng Giám đốc     2015-09-14             0.000002      5810
```

### subsidiaries() - Công Ty Con

```python
df = company.subsidiaries()
```

Trả về: DataFrame với 5 cột
- `id`: object (str) - ID công ty con
- `sub_organ_code`: object (str) - Mã công ty con
- `ownership_percent`: float64 - Tỷ lệ sở hữu (%)
- `organ_name`: object (str) - Tên công ty con/liên kết
- `type`: object (str) - Loại ('công ty con' hoặc 'công ty liên kết')

**Ví dụ output** (3 công ty con của VCB):
```
    sub_organ_code  ownership_percent                                     organ_name        type
0       2646966              0.875    Công ty Chuyển tiền Vietcombank      công ty con
1       TB                 1.000    Ngân hàng Thương mại TNHH MTV...     công ty con
2       VCB198             0.700    Công ty TNHH Cao Ốc Vietcombank 198  công ty con
```

### events() - Sự Kiện Công Ty

```python
df = company.events()
```

Trả về: DataFrame với 13 cột
- `id`: object (str) - ID sự kiện
- `event_title`: object (str) - Tiêu đề sự kiện
- `en__event_title`: object (str) - Tiêu đề sự kiện Tiếng Anh
- `public_date`: object (str) - Ngày thông báo
- `issue_date`: object (str) - Ngày thanh toán
- `source_url`: object (str) - Đường dẫn nguồn
- `event_list_code`: object (str) - Mã loại sự kiện
- `ratio`: float64 - Tỉ lệ sự kiện (nếu có, NULL nếu không)
- `value`: float64 - Giá trị sự kiện (nếu có, NULL nếu không)
- `record_date`: object (str) - Ngày đăng ký cuối cùng
- `exright_date`: object (str) - Ngày giao dịch không hưởng quyền
- `event_list_name`: object (str) - Tên loại sự kiện (ví dụ: 'Trả cổ tức bằng tiền mặt')
- `en__event_list_name`: object (str) - Tên loại sự kiện Tiếng Anh

### news() - Tin Tức

```python
df = company.news()
```

Trả về: DataFrame với 18 cột
- `id`: object (str) - ID tin tức
- `news_title`: object (str) - Tiêu đề tin
- `news_sub_title`: object (str) - Phụ đề tin
- `friendly_sub_title`: object (str) - Phụ đề thân thiện
- `news_image_url`: object (str) - Đường dẫn ảnh
- `news_source_link`: object (str) - Đường dẫn nguồn
- `created_at`: object (str) - Ngày tạo
- `public_date`: int64 - Timestamp ngày công bố
- `updated_at`: object (str) - Ngày cập nhật
- `lang_code`: object (str) - Mã ngôn ngữ
- `news_id`: object (str) - ID tin (khác)
- `news_short_content`: object (str) - Nội dung tóm tắt
- `news_full_content`: object (str) - Nội dung đầy đủ
- `close_price`: int64 - Giá đóng cửa khi tin được công bố
- `ref_price`: int64 - Giá tham chiếu
- `floor`: int64 - Giá sàn
- `ceiling`: int64 - Giá trần
- `price_change_pct`: float64 - % thay đổi giá

### reports() - Báo Cáo Phân Tích

```python
df = company.reports()
```

Trả về: DataFrame với 4 cột
- `date`: object (str) - Ngày báo cáo (ISO 8601 format)
- `description`: object (str) - Mô tả báo cáo
- `link`: object (str) - Đường dẫn đến báo cáo
- `name`: object (str) - Tiêu đề báo cáo

### trading_stats() - Thống Kê Giao Dịch

```python
df = company.trading_stats()
```

Trả về: DataFrame với 24 cột
- `symbol`: object (str) - Mã cổ phiếu
- `exchange`: object (str) - Sàn giao dịch (ví dụ: 'HOSE')
- `ev`: int64 - Giá trị doanh nghiệp (Enterprise Value)
- `ceiling`: int64 - Giá trần
- `floor`: int64 - Giá sàn
- `ref_price`: int64 - Giá tham chiếu
- `open`: int64 - Giá mở cửa
- `match_price`: int64 - Giá khớp
- `close_price`: int64 - Giá đóng cửa
- `price_change`: int64 - Thay đổi giá tuyệt đối
- `price_change_pct`: float64 - % thay đổi giá
- `high`: int64 - Giá cao nhất
- `low`: int64 - Giá thấp nhất
- `total_volume`: int64 - Tổng khối lượng giao dịch
- `high_price_1y`: int64 - Giá cao nhất 1 năm
- `low_price_1y`: int64 - Giá thấp nhất 1 năm
- `pct_low_change_1y`: float64 - % từ thấp nhất 1 năm
- `pct_high_change_1y`: float64 - % từ cao nhất 1 năm
- `foreign_volume`: int64 - Khối lượng nhà đầu tư nước ngoài
- `foreign_room`: int64 - "Room ngoại" (sở hữu tối đa mà nhà đầu tư nước ngoài được phép nắm giữ)
- `avg_match_volume_2w`: int64 - Khối lượng giao dịch trung bình 2 tuần
- `foreign_holding_room`: int64 - "Room ngoại" đang nắm giữ
- `current_holding_ratio`: float64 - Sở hữu nước ngoài (x100%)
- `max_holding_ratio`: float64 - Sở hữu nước ngoài tối đa (x100%)

### ratio_summary() - Tóm Tắt Chỉ Số Tài Chính

```python
df = company.ratio_summary()
```

Trả về: DataFrame với 46 cột chứa các chỉ số tài chính chính:
- Các chỉ số định giá: `pe`, `pb`, `ps`, `pcf` (float64)
- Các chỉ số lợi suất: `roe`, `roa`, `roic` (float64)
- Các chỉ số tăng trưởng: `revenue_growth`, `net_profit_growth` (float64)
- Các chỉ số khác: `dividend`, `eps`, `bvps`, `ev_per_ebitda` (float64)
- Dữ liệu cơ bản: `symbol`, `year_report`, `length_report`, `update_date`, `charter_capital`, `issue_share` (object/int64)

Ghi chú: Một số cột có thể NULL (object) nếu chưa có dữ liệu. Một số cột chưa được chuẩn hoá hoàn toàn về cách trình bày.

## Ví Dụ

```python
from vnstock_data import Company
import pandas as pd

company = Company(source="vci", symbol="VCB")

# Thông tin công ty
overview = company.overview()
print(f"Công ty: {overview['company_name'].values[0]}")
print(f"Vốn điều lệ: {overview['charter_capital'].values[0]:,.0f}")

# Cổ đông lớn
shareholders = company.shareholders()
print(f"\nTop 5 cổ đông lớn:")
print(shareholders[['share_holder', 'share_own_percent']].head())

# Ban lãnh đạo
officers = company.officers(filter_by='working')
print(f"\nBan lãnh đạo (đang làm):")
print(officers[['officer_name', 'officer_position']].head())

# Sự kiện gần đây
events = company.events().head()
print(f"\nSự kiện gần đây:")
print(events[['event_title', 'public_date']])

# Thống kê giao dịch
stats = company.trading_stats()
print(f"\nThống kê giao dịch:")
print(f"Giá khớp: {stats['match_price'].values[0]}")
print(f"Khối lượng: {stats['total_volume'].values[0]:,.0f}")
```

## Thực hành tốt

1. **Cache dữ liệu công ty**: Thông tin công ty ít thay đổi, hãy cache
2. **Kết hợp với Quote**: Sử dụng Company + Quote để phân tích sâu hơn
3. **Kiểm tra update_date**: Xác nhận dữ liệu có mới nhất không

## Ma Trận Support

| Phương Thức | VCI |
|---|:---:|
| overview | ✅ |
| shareholders | ✅ |
| officers | ✅ |
| subsidiaries | ✅ |
| events | ✅ |
| news | ✅ |
| reports | ✅ |
| trading_stats | ✅ |
| ratio_summary | ✅ |

**Khuyến Nghị**: Luôn sử dụng VCI cho Company data.
