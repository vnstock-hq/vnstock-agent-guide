# Macro - Kinh Tế Vĩ Mô

Lớp `Macro` cung cấp dữ liệu kinh tế vĩ mô của Việt Nam từ MayBank (MBK).

## Khởi Tạo

```python
from vnstock_data import Macro

# Khởi tạo cơ bản
macro = Macro()

# Khởi tạo với random user agent
macro = Macro(random_agent=True)

# Hiển thị debug logs
macro = Macro(show_log=True)
```

### Tham Số Khởi Tạo

- `random_agent` (bool, default=False): Sử dụng random user agent để tránh bị block

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
- `start` (str): Ngày bắt đầu (format: "YYYY-MM"). Default: "2015-01"
- `end` (str): Ngày kết thúc (format: "YYYY-MM"). Default: "2025-04"
- `period` (str): "quarter" hoặc "year". Default: "quarter"
- `keep_label` (bool): Giữ lại cột label gốc. Default: False

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
- `start` (str): Ngày bắt đầu (format: "YYYY-MM"). Default: "2015-01"
- `end` (str): Ngày kết thúc (format: "YYYY-MM"). Default: "2025-04"
- `period` (str): "month" hoặc "year". Default: "month"

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
- `start` (str): Ngày bắt đầu (format: "YYYY-MM")
- `end` (str): Ngày kết thúc (format: "YYYY-MM")
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
- `start` (str): Ngày bắt đầu (format: "YYYY-MM-DD" cho period="day" hoặc "YYYY-MM" cho period="month")
- `end` (str): Ngày kết thúc (cùng format)
- `period` (str): "day", "month", hoặc "year". Default: "day"

**Trả về**: DataFrame với cột: `last_updated`, `name` (tên tỷ giá), `value` (float64), `unit`, `source`

**Ví dụ** (3 dòng gần nhất):
```
             last_updated                              name    value     unit                       source
report_time                                                                                              
2025-11-28    2025-11-27                    Liên ngân hàng      NaN  VNĐ/USD  Ngân hàng Nhà nước Việt Nam
2025-11-29    2025-11-28                    Liên ngân hàng      NaN  VNĐ/USD  Ngân hàng Nhà nước Việt Nam
2025-11-29    2025-11-28  Tỷ giá trung tâm (từ 04/01/2016)  25155.0  VNĐ/USD                         None
```

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
