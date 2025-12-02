# Finance - Báo Cáo Tài Chính, Chỉ Số, Kế Hoạch

Lớp `Finance` cung cấp dữ liệu báo cáo tài chính, chỉ số tài chính và kế hoạch kinh doanh.

## Khởi Tạo

```python
from vnstock_data import Finance

# VCI (đơn giản, dễ phân tích)
fin = Finance(source="vci", symbol="VCB", period="year")

# MAS (chi tiết, Excel-style)
fin_mas = Finance(source="mas", symbol="VCB", period="year")
```

**Tham số**:
- `source`: `"vci"` hoặc `"mas"`
- `symbol`: Mã cổ phiếu
- `period`: `"year"` (báo cáo năm) hoặc `"quarter"` (báo cáo quý)

## Phương Thức VCI

### balance_sheet() - Bảng Cân Đối Kế Toán

```python
df = fin.balance_sheet(lang="vi")
```

**Tham số**:
- `lang`: `'vi'` (Tiếng Việt) hoặc `'en'` (Tiếng Anh) - Mặc định là `'vi'`

**Kiểu Dữ Liệu Trả Về**: DataFrame với 94 cột (shape: 43, 94)
- Dòng: Giai đoạn báo cáo (2017-2025-Q3)
- Cột: Tài sản, Nợ phải trả, Vốn chủ sở hữu với các chi tiết lẻ
- Kiểu dữ liệu: float64 (số tiền), object (report_period, Mã CP)

### income_statement() - Báo Cáo Kết Quả Kinh Doanh

```python
df = fin.income_statement(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 28 cột (shape: 43, 28)
- Doanh thu, chi phí, lợi nhuận chi tiết theo từng loại
- Ví dụ cột: 'Thu nhập lãi thuần', 'Chi phí dịch vụ', 'Lãi/(lỗ) thuần từ hoạt động khác', etc.
- Kiểu dữ liệu: float64 (số tiền), object (report_period, Mã CP)

### cash_flow() - Báo Cáo Lưu Chuyển Tiền Tệ

```python
df = fin.cash_flow(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 56 cột (shape: 43, 56)
- Dòng tiền từ hoạt động kinh doanh, đầu tư, tài chính
- Chi tiết về các khoản tiền thu/chi
- Kiểu dữ liệu: float64 (số tiền), object (report_period, Mã CP)

### ratio() - Chỉ Số Tài Chính

```python
df = fin.ratio(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 58 cột (shape: 42, 58)
- Chỉ số định giá: P/E, P/B, P/S, EV/EBITDA, etc.
- Chỉ số sinh lợi: ROE, ROA, ROIC, Biên lợi nhuận, etc.
- Chỉ số tăng trưởng: Tăng trưởng doanh thu, tăng trưởng cho vay, etc.
- Chỉ số độc lập: LDR, Nợ xấu, CAR, CASA, etc.
- Dòng: Quý (2017-Q1 to 2025-Q3)
- Kiểu dữ liệu: float64 (chỉ số), int64, object

### note() - Thuyết Minh BCTC Chi Tiết

```python
df = fin.note(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 307 cột (shape: 43, 307)
- Các thuyết minh chi tiết về từng khoản mục trong báo cáo
- Phân loại cho vay theo loại khách hàng, ngành, etc.
- Kiểu dữ liệu: float64, object

## Phương Thức MAS

**Lưu ý**: MAS có cấu trúc dữ liệu khác VCI - Cột chi tiết, định dạng giống Excel tải về từ website.

```python
fin_mas = Finance(source="mas", symbol="VCB", period="year")
df_bs = fin_mas.balance_sheet(lang="vi")      # 79 cột, 13 năm
df_ic = fin_mas.income_statement(lang="vi")   # 26 cột, 13 năm
df_cf = fin_mas.cash_flow(lang="vi")          # 52 cột, 13 năm
df_ratio = fin_mas.ratio(lang="vi")           # 8 cột, 13 năm
df_plan = fin_mas.annual_plan(lang="vi")      # 3 cột, 6 năm

# note() không được implement trong MAS
```

### balance_sheet() - Bảng Cân Đối Kế Toán

```python
df = fin_mas.balance_sheet(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 79 cột, có thể thay đổi theo loại hình doanh nghiệp (shape: 13, 79)
- Dòng: 13 giai đoạn báo cáo năm (2024-2012)
- Cột: Tài sản (cash, tiền gửi NHNN, cho vay, chứng khoán, TSCĐ, etc.), Nợ (tiền gửi khách, vay NHNN, phát hành giấy tờ), Vốn (vốn điều lệ, quỹ, lợi nhuận lũy kế)
- Kiểu dữ liệu: object (period, year_period, các khoản mục), int64 (số tiền - VND)

### income_statement() - Báo Cáo Kết Quả Kinh Doanh

```python
df = fin_mas.income_statement(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 26 cột, có thể thay đổi theo loại hình doanh nghiệp (shape: 13, 26)
- Dòng: 13 giai đoạn năm
- Cột: Thu nhập lãi, chi phí lãi, thu nhập dịch vụ, chi phí dịch vụ, lãi/lỗ các hoạt động, chi phí dự phòng, lợi nhuận trước/sau thuế, lợi nhuận sau thuế của cổ đông, EPS
- Kiểu dữ liệu: object (period, year_period, các khoản mục), int64 (số tiền - VND)

### cash_flow() - Báo Cáo Lưu Chuyển Tiền Tệ

```python
df = fin_mas.cash_flow(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 52 cột, có thể thay đổi theo loại hình doanh nghiệp (shape: 13, 52)
- Dòng: 13 giai đoạn năm
- Cột: Dòng tiền từ hoạt động kinh doanh (chi tiết: lãi, chi phí, dịch vụ, nhân viên), thay đổi tài sản, thay đổi công nợ, hoạt động đầu tư, hoạt động tài chính
- Kiểu dữ liệu: object (period, year_period), int64 (số tiền - VND)

### ratio() - Chỉ Số Tài Chính

```python
df = fin_mas.ratio(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 8 cột, có thể thay đổi theo loại hình doanh nghiệp (shape: 13, 8)
- Cột: `period`, `year_period`, `EPS`, `BVPS`, `P/E`, `P/B`, `Tỷ suất cổ tức`, `Beta`
- Kiểu dữ liệu: object (period, year_period), float64/int64 (chỉ số)

### annual_plan() - Kế Hoạch Kinh Doanh Hàng Năm

```python
df_plan = fin_mas.annual_plan(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 3 cột (shape: 6, 3)
- `period`: int64 - Năm kế hoạch
- `Lợi nhuận trước thuế kế hoạch`: object - Giá trị lợi nhuận kế hoạch (hoặc NULL)
- `Tỷ lệ cổ tức (%) kế hoạch`: object - Tỷ lệ cổ tức dự kiến (hoặc NULL)

**Ví dụ**:
```
   period Lợi nhuận trước thuế kế hoạch Tỷ lệ cổ tức (%) kế hoạch
0    2024                          None                      None
1    2023                42973304650000                      None
2    2022                30675680000000                      None
```

## Ví Dụ

```python
from vnstock_data import Finance
import pandas as pd

# VCI: Phân tích đơn giản
fin = Finance(source="vci", symbol="VCB", period="year")

# Lấy BCTC
bs = fin.balance_sheet(lang="vi")
ic = fin.income_statement(lang="vi")
ratio = fin.ratio(lang="vi")

# Phân tích xu hướng
print("Doanh thu qua các năm:")
print(ic[['Năm', 'Doanh thu']].head())

# Tính chỉ số
print("\nChỉ số tài chính:")
print(ratio[['Năm', 'P/E', 'P/B', 'ROE', 'ROA']].head())

# MAS: Dữ liệu chi tiết
fin_mas = Finance(source="mas", symbol="VCB", period="year")
bs_mas = fin_mas.balance_sheet(lang="vi")

# MAS có cấu trúc MultiIndex hoặc cột dài
print(f"\nSố cột MAS: {len(bs_mas.columns)}")
print(f"Số cột VCI: {len(bs.columns)}")
```

## So Sánh VCI vs MAS

| Tiêu Chí | VCI | MAS |
|---|:---:|:---:|
| Ổn định | ✅ | ✅ |
| Số cột | Lớn (28-307) | Vừa (8-79) |
| Kích thước dữ liệu | Lớn | Trung bình |
| Dễ sử dụng | ✅ | ✅ |
| Thuyết minh BCTC | ✅ | ❌ |
| Chỉ tiêu kế hoạch | ❌ | ✅ |
| Định dạng | Làm phẳng cột, rút gọn tiêu chí | Báo cáo chuẩn |
| Thích hợp cho | Phân tích chi tiết | Phân tích theo cấu trúc quan hệ |

**Khuyến Cáo**:
- **VCI**: Phân tích các tiêu chí quan trọng, theo dõi quý, cần thuyết minh BCTC. Báo cáo của ngành đặc thù như tài chính, ngân hàng có thể không giữ nguyên cấu trúc khoản mục gốc.
- **MAS**: Báo cáo theo định dạng tiêu chuẩn giữ nguyên cấu trúc khoản mục báo cáo, kế hoạch năm

## Tham Số Chính

### Khởi Tạo Finance
```python
fin = Finance(source="vci", symbol="VCB", period="year")
```

**Tham số**:
- `source`: `"vci"` (VCI) hoặc `"mas"` (MAS) - Mặc định là `"vci"`
- `symbol`: Mã cổ phiếu (ví dụ: `"VCB"`)
- `period`: `"year"` (năm) hoặc `"quarter"` (quý) - Mặc định là `"year"`

### Tham số Method

```python
df = fin.balance_sheet(lang="vi")
```

**Tham số**:
- `lang`: `"vi"` (tiếng Việt) hoặc `"en"` (tiếng Anh) - Mặc định là `"vi"`

## Ma Trận Các Phương Thức Hỗ Trợ

> Thông tin số dòng/cột chỉ mang tính chất tham khảo, có thể thay đổi theo mã cụ thể, thời gian, và đặc thù nhóm phân loại công ty.

| Phương Thức | VCI | MAS | Ghi Chú |
|---|:---:|:---:|---|
| balance_sheet | ✅ (94 cột, 43 kỳ) | ✅ (79 cột, 13 năm) | MAS theo chuẩn NHNN |
| income_statement | ✅ (28 cột, 43 kỳ) | ✅ (26 cột, 13 năm) | MAS theo chuẩn NHNN |
| cash_flow | ✅ (56 cột, 43 kỳ) | ✅ (52 cột, 13 năm) | MAS theo chuẩn NHNN |
| ratio | ✅ (58 cột, 42 kỳ) | ✅ (8 cột, 13 năm) | MAS chỉ có 6 chỉ số |
| note | ✅ (307 cột, 43 kỳ) | ❌ NotImplemented | Chỉ VCI có |
| annual_plan | ❌ | ✅ (3 cột, 6 năm) | MAS only |


## Ví Dụ Phân Tích

```python
from vnstock_data import Finance
import pandas as pd

fin = Finance(source="vci", symbol="VCB", period="year")

# Tính trend doanh thu
ic = fin.income_statement(lang="vi")
ic['revenue_growth'] = ic['Doanh thu'].pct_change()

print("Tăng trưởng doanh thu:")
print(ic[['Năm', 'Doanh thu', 'revenue_growth']])

# Tính lợi nhuận biên
ic['profit_margin'] = ic['Lợi nhuận'] / ic['Doanh thu']

print("\nLợi nhuận biên:")
print(ic[['Năm', 'profit_margin']])

# Lấy ratio
ratio = fin.ratio(lang="vi")
print("\nChỉ số định giá:")
print(ratio[['Năm', 'P/E', 'P/B', 'EPS']].tail(5))
```
