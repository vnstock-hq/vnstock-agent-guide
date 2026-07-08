# Macro - Kinh Tế Vĩ Mô

> ⚠️ **Migration Notice**: Lớp `Macro` này sẽ chuyển đổi sang [Unified UI](../01-unified-ui.md) structure sau ngày **31/8/2026**. Vui lòng bắt đầu sử dụng cấu trúc mới: `Macro().economy()`, `Macro().currency()`, `Macro().commodity()` thay vì các method trực tiếp. Nếu code hiện tại của bạn đang sử dụng cấu trúc cũ, bạn có thể tiếp tục dùng đến hết 31/8/2026.

Lớp `Macro` cung cấp dữ liệu kinh tế vĩ mô của Việt Nam từ MayBank (MBK).

## Khởi Tạo

```python
from vnstock_data import Macro

# Khởi tạo cơ bản
macro = Macro()

# Khởi tạo với random user agent
macro = Macro()

# Hiển thị debug logs
macro = Macro()
```

### Tham Số Khởi Tạo

**Đặc tả mới từ bản cập nhật**:
- Các hàm truy xuất dữ liệu nay cung cấp tùy chọn tham số `length` (Khoảng thời gian tương đối như `'1Y'`, `'3M'`, `'30D'`, `'100b'`) làm mặc định thay vì bắt buộc truyền `start` và `end`.
- Nếu không truyền tham số nào, dữ liệu mặt định trả về là **1 năm (`1Y`)**.

**Lưu ý**: Chỉ **MBK** hỗ trợ Macro.

## Phương Thức

### gdp() - GDP

```python
# Lấy GDP theo quý từ 2023-2025
df = macro.gdp(start="2023-01", end="2025-12", period="quarter")

# Lấy GDP theo năm
df = macro.gdp(start="2020-01", end="2025-12", period="year")
```

**Tham Số**:
- `start` (str, optional): Ngày bắt đầu (format: "YYYY-MM"). 
- `end` (str, optional): Ngày kết thúc (format: "YYYY-MM"). 
- `length` (str|int, optional): Khoảng thời gian tương đối (ví dụ: `90` ngày, `'3Y'`, `'100b'`). Xem chi tiết format tại [README.md](../README.md#tham-số-thời-gian-tương-đối-length).
- `period` (str): "quarter" hoặc "year". Default: "quarter"
- `keep_label` (bool): Giữ lại cột label gốc. Default: False

*Lưu ý*: Nếu không cung cấp `start`, `end`, hay `length`, hàm lấy mặc định `length="1Y"`.

**Trả về**: DataFrame với cột: `last_updated`, `group_name`, `name`, `value` (float64), `unit`, `source`, `report_type`

**Ví dụ** (3 dòng gần nhất):
```
             last_updated                group_name         name  value unit             source report_type
report_time                                                                                               
2025-09-01    2025-10-05  Tăng trưởng thực của GDP  Nông nghiệp   3.74    %  Tổng cục thống kê       Quý 3
2025-09-30    2025-10-05  Tăng trưởng thực của GDP     Tổng GDP   7.85    %  Tổng cục thống kê     9 tháng
2025-09-01    2025-10-05  Tăng trưởng thực của GDP     Tổng GDP   8.23    %  Tổng cục thống kê       Quý 3
```

### cpi() - Chỉ Số Giá Tiêu Dùng

```python
# Lấy CPI theo tháng
df = macro.cpi(start="2023-01", end="2025-12", period="month")

# Lấy CPI theo năm
df = macro.cpi(start="2020-01", end="2025-12", period="year")
```

**Tham Số**:
- `start` (str, optional): Ngày bắt đầu (format: "YYYY-MM"). 
- `end` (str, optional): Ngày kết thúc (format: "YYYY-MM"). 
- `length` (str|int, optional): Khoảng thời gian tương đối. Xem [Định dạng length](../README.md#tham-số-thời-gian-tương-đối-length).
- `period` (str): "month" hoặc "year". Default: "month"

*Lưu ý*: Nếu không cung cấp `start`, `end`, hay `length`, hàm lấy mặc định `length="1Y"`.

**Trả về**: DataFrame với cột: `last_updated`, `name`, `value` (float64), `unit`, `source`

**Ví dụ** (3 dòng gần nhất):
```
             last_updated                          name  value unit             source
report_time                                                                          
2025-08-31    2025-09-05                    Lương thực   0.01    %  Tổng cục thống kê
2025-08-31    2025-09-05  Thiết bị và đồ dùng gia đình   0.11    %  Tổng cục thống kê
2025-08-31    2025-09-05          Chỉ số giá tiêu dùng   0.05    %  Tổng cục thống kê
```

### industry_prod() - Chỉ Số Sản Xuất Công Nghiệp

```python
df = macro.industry_prod(start="2023-01", end="2025-12", period="month")
```

**Tham Số**:
- `start` (str, optional): Ngày bắt đầu (format: "YYYY-MM")
- `end` (str, optional): Ngày kết thúc (format: "YYYY-MM")
- `length` (str|int, optional): Khoảng thời gian tương đối. Xem [Định dạng length](../README.md#tham-số-thời-gian-tương-đối-length).
- `period` (str): "month" hoặc "year"

**Trả về**: DataFrame chỉ số sản xuất công nghiệp

### import_export() - Xuất-Nhập Khẩu Hàng Hóa

```python
df = macro.import_export(start="2023-01", end="2025-12", period="month")
```

**Trả về**: DataFrame dữ liệu xuất-nhập khẩu theo tháng/năm

### retail() - Doanh Thu Bán Lẻ

```python
df = macro.retail(start="2023-01", end="2025-12", period="month")
```

**Trả về**: DataFrame doanh thu bán lẻ tiêu dùng

### fdi() - Vốn Đầu Tư Trực Tiếp Nước Ngoài

```python
# Lấy FDI theo tháng
df = macro.fdi(start="2023-01", end="2025-12", period="month")
```

**Trả về**: DataFrame với cột: `last_updated`, `group_name`, `name`, `value` (float64 - Tỷ USD), `unit`, `source`

**Ví dụ** (3 dòng gần nhất):
```
             last_updated group_name       name  value    unit                 source
report_time                                                                         
2025-09-30    2025-10-05   Tổng FDI  Giải ngân   3.40  Tỷ USD  Cục Đầu tư nước ngoài
2025-10-31    2025-11-05   Tổng FDI    Đăng ký   2.98  Tỷ USD  Cục Đầu tư nước ngoài
2025-10-31    2025-11-05   Tổng FDI  Giải ngân   2.50  Tỷ USD  Cục Đầu tư nước ngoài
```

### money_supply() - Cung Tiền

```python
df = macro.money_supply(start="2023-01", end="2025-12", period="month")
```

**Trả về**: DataFrame cung tiền M0, M1, M2

### exchange_rate() - Tỷ Giá Ngoại Tệ

```python
# Lấy tỷ giá theo ngày
df = macro.exchange_rate(start="2025-11-01", end="2025-12-02", period="day")
```

**Tham Số**:
- `start` (str, optional): Ngày bắt đầu (format: "YYYY-MM-DD" cho period="day" hoặc "YYYY-MM" cho period="month")
- `end` (str, optional): Ngày kết thúc (cùng format)
- `length` (str|int, optional): Khoảng thời gian tương đối. Xem [Định dạng length](../README.md#tham-số-thời-gian-tương-đối-length).
- `period` (str): "day", "month", hoặc "year". Default: "day"

*Lưu ý*: Nếu không truyền `start`, `end`, hoặc `length`, hàm tự quy định `length="1Y"`.

**Trả về**: DataFrame với cột: `last_updated`, `name` (tên tỷ giá), `value` (float64), `unit`, `source`

**Ví dụ** (3 dòng gần nhất):
```
             last_updated                              name    value     unit                       source
report_time                                                                                              
2025-11-28    2025-11-27                    Liên ngân hàng      NaN  VNĐ/USD  Ngân hàng Nhà nước Việt Nam
2025-11-29    2025-11-28                    Liên ngân hàng      NaN  VNĐ/USD  Ngân hàng Nhà nước Việt Nam
2025-11-29    2025-11-28  Tỷ giá trung tâm (từ 04/01/2016)  25155.0  VNĐ/USD                         None
```

### interest_rate() - Lãi Suất Định Cố & Doanh Số

```python
# Lãi suất theo ngày dạng pivot (wide table)
df = macro.interest_rate(length="30D", period="day")

# Lãi suất định dạng long (flat table)
df = macro.interest_rate(length="30D", period="day", format="long")

# Lãi suất theo năm
df = macro.interest_rate(start="2024-01", end="2025-12", period="year")
```

**Tham Số**:
- `start` (str, optional): Ngày bắt đầu (format: "YYYY-MM-DD" cho period="day" hoặc "YYYY-MM" cho period="year").
- `end` (str, optional): Ngày kết thúc (cùng format với start).
- `length` (str|int, optional): Khoảng thời gian tương đối. Default: `"1Y"`. Xem [Định dạng length](../README.md#tham-số-thời-gian-tương-đối-length).
- `period` (str): "day" hoặc "year". Default: "day"
- `format` (str): "pivot" hoặc "long". 
  - **pivot**: Xoay trục cột, tạo MultiIndex DataFrame (wide format) - dễ đọc
  - **long**: Định dạng raw flat table - phù hợp cho xử lý dữ liệu
  - Default: "pivot"

**Trả về**: 
- `format="pivot"`: DataFrame với MultiIndex (group_name, name) trên cột - easy-to-read wide format
- `format="long"`: DataFrame flat với cột: `last_updated`, `group_name`, `name`, `value` (float64), `unit`, `source`

**Ví dụ Pivot Format** (3 dòng gần nhất):
```
group_name   Doanh số                      ... Lãi suất bình quân liên ngân hàng (%/năm)
name         1 tháng    1 tuần    2 tuần   ...                                 6 tháng   9 tháng Qua đêm
report_time                                ...                                                          
2026-02-26     4201.0   92459.0   12220.0  ...                                      8.00    7.82    2.83
2026-02-27     3262.0   39565.0    8875.0  ...                                      7.80    7.82    4.70
2026-03-02     2280.0    6420.0    2615.0  ...                                      7.80    7.82   11.21
```

**Ví dụ Long Format** (3 dòng gần nhất):
```
             last_updated                            group_name                name    value unit             source
report_time                                                                                                       
2026-02-26    2026-02-26                              Doanh số              1 tháng   4201.0   Tr   Ngân hàng Nhà nước
2026-02-26    2026-02-26  Lãi suất bình quân liên...                      Qua đêm    2.83    %   Ngân hàng Nhà nước
2026-02-27    2026-02-27                              Doanh số              1 tuần  39565.0   Tr   Ngân hàng Nhà nước
```

*Lưu ý*: Nếu không cung cấp `start`, `end`, hay `length`, hàm lấy mặc định `length="1Y"`.

### population_labor() - Dân Số & Lao Động

```python
df = macro.population_labor(start="2020-01", end="2025-12", period="year")
```

**Trả về**: DataFrame thống kê dân số, lao động theo năm

## Ví Dụ

```python
from vnstock_data import Macro
import pandas as pd

macro = Macro()

# Lấy GDP theo quý
gdp_data = macro.gdp(start="2024-01", end="2025-12", period="quarter")
print("GDP Tổng theo quý:")
print(gdp_data[gdp_data['name'] == 'Tổng GDP'][['name', 'value', 'unit', 'report_type']].tail(5))

# Lấy CPI theo tháng
cpi_data = macro.cpi(start="2024-01", end="2025-12", period="month")
print("\nChỉ số giá tiêu dùng:")
cpi_latest = cpi_data[cpi_data['name'] == 'Chỉ số giá tiêu dùng'].tail(3)
print(cpi_latest[['name', 'value', 'unit']].to_string())

# Lấy FDI
fdi_data = macro.fdi(start="2024-01", end="2025-12", period="month")
print("\nFDI giải ngân:")
fdi_release = fdi_data[fdi_data['name'] == 'Giải ngân'].tail(3)
print(fdi_release[['name', 'value', 'unit']].to_string())

# Lấy tỷ giá
exr_data = macro.exchange_rate(start="2025-11-01", end="2025-12-02", period="day")
print("\nTỷ giá USD/VND:")
exr_vnindex = exr_data[exr_data['name'].str.contains('trung tâm')].tail(3)
print(exr_vnindex[['name', 'value', 'unit']].to_string())
```

## Phân Tích Ví Dụ

```python
from vnstock_data import Macro
import pandas as pd

macro = Macro()

# Phân tích lạm phát
cpi_data = macro.cpi(start="2020-01", end="2025-12", period="month")
cpi_all = cpi_data[cpi_data['name'] == 'Chỉ số giá tiêu dùng'].copy()

# Lạm phát mới nhất
latest_cpi = cpi_all['value'].iloc[-1]
avg_cpi = cpi_all['value'].mean()

print(f"CPI tháng gần nhất: {latest_cpi:.2f}%")
print(f"CPI trung bình: {avg_cpi:.2f}%")

if latest_cpi > 5:
    print("⚠️ Lạm phát cao")
elif latest_cpi > 3:
    print("➡️ Lạm phát ở mức trung bình")
else:
    print("✅ Lạm phát thấp")

# Phân tích FDI
fdi_data = macro.fdi(start="2020-01", end="2025-12", period="month")
fdi_registered = fdi_data[fdi_data['name'] == 'Đăng ký'].copy()

if len(fdi_registered) > 0:
    fdi_trend = fdi_registered['value'].tail(12).mean()
    latest_fdi = fdi_registered['value'].iloc[-1]
    
    print(f"\nFDI giải ngân trung bình 12 tháng: ${fdi_trend:.2f} tỷ USD")
    
    if latest_fdi > fdi_trend:
        print("📈 FDI đang tăng")
    else:
        print("📉 FDI đang giảm")
```

## Ứng Dụng

- **Phân tích macro**: Hiểu nền kinh tế, lạm phát, tăng trưởng
- **Dự báo chứng khoán**: Kinh tế tốt → cổ phiếu tốt
- **Quản lý rủi ro**: Lạm phát cao → điều chỉnh portfolio
- **Chọn ngành**: FDI tăng → công ty xuất khẩu tốt
