# 05 - Financial API - Dữ Liệu Tài Chính

## 📖 Giới Thiệu

Financial API cung cấp các phương thức lấy dữ liệu tài chính doanh nghiệp, bao gồm:

- **Báo cáo tài chính**: Bảng cân đối kế toán, Khoản lợi nhập, Lưu chuyển tiền tệ
- **Chỉ số tài chính**: ROE, ROA, EPS, P/E, Debt ratio, v.v.
- **Chu kỳ báo cáo**: Hàng quý (Quarter) hoặc hàng năm (Year)
- **Phân tích**: Xu hướng tài chính, so sánh ngành

## 🏗️ Khởi Tạo

```python
from vnstock import Finance

# Khởi tạo Finance adapter
# Hỗ trợ: VCI, TCBS
finance = Finance(
    source="vci",           # Nguồn dữ liệu
    symbol="VCI",           # Mã chứng khoán
    random_agent=False,     # Sử dụng random user agent
    show_log=True           # Hiển thị log chi tiết
)
```

## 📊 Báo Cáo Tài Chính

### 1. balance_sheet() - Bảng Cân Đối Kế Toán

Lấy dữ liệu bảng cân đối kế toán theo quý hoặc năm.

**Ví dụ:**

```python
from vnstock import Finance

finance = Finance(source="vci", symbol="VCI")

# Bảng cân đối năm
df = finance.balance_sheet(period="year")

print(f"Số bản ghi: {len(df)}")
print(f"Các cột: {df.columns.tolist()}")
print(df)
```

**Output:**
```
Số bản ghi: 13
Các cột: ['ticker', 'yearReport', 'CURRENT ASSETS (Bn. VND)', 'Cash and cash equivalents (Bn. VND)', ...]
```

### 2. income_statement() - Báo Cáo Khoản Lợi Nhập

Lấy dữ liệu báo cáo khoản lợi nhập theo quý hoặc năm.

**Ví dụ:**

```python
from vnstock import Finance

finance = Finance(source="vci", symbol="VCI")

# Báo cáo khoản lợi nhập năm
df = finance.income_statement(period="year")

print(f"Số bản ghi: {len(df)}")
print(f"Các cột: {df.columns.tolist()}")
print(df)
```

**Output:**
```
Số bản ghi: 13
Các cột: ['ticker', 'yearReport', 'Revenue (Bn. VND)', 'Revenue YoY (%)', 'Attribute to parent company (Bn. VND)', ...]
```

### 3. cash_flow() - Lưu Chuyển Tiền Tệ

Lấy dữ liệu báo cáo lưu chuyển tiền tệ theo quý hoặc năm.

**Ví dụ:**

```python
from vnstock import Finance

finance = Finance(source="vci", symbol="VCI")

# Lưu chuyển tiền tệ năm
df = finance.cash_flow(period="year")

print(f"Số bản ghi: {len(df)}")
print(f"Các cột: {df.columns.tolist()}")
print(df)
```

**Output:**
```
Số bản ghi: 13
Các cột: ['ticker', 'yearReport', 'Net Profit/Loss before tax', 'Depreciation and Amortisation', ...]
```

## 💹 Chỉ Số Tài Chính

### 4. ratio() - Các Chỉ Số Tài Chính

Lấy các chỉ số tài chính khác nhau (MultiIndex DataFrame).

**Ví dụ:**

```python
from vnstock import Finance

finance = Finance(source="vci", symbol="VCI")

# Lấy tất cả chỉ số
df = finance.ratio()

print(f"Số bản ghi: {len(df)}")
print(f"Các nhóm chỉ số: {df.columns.get_level_values(0).unique().tolist()}")
print(df)
```

**Output:**
```
Số bản ghi: 51
Các nhóm chỉ số: ['Meta', 'Chỉ tiêu cơ cấu nguồn vốn', 'Chỉ tiêu hiệu quả hoạt động', 'Chỉ tiêu khả năng sinh lợi', 'Chỉ tiêu thanh khoản', 'Chỉ tiêu định giá']
```

## 📈 Phân Tích Tài Chính

### Ví dụ 1: Lấy Dữ Liệu Báo Cáo Tài Chính

```python
from vnstock import Finance

finance = Finance(source="vci", symbol="ACB")

# Bảng cân đối kế toán
bs = finance.balance_sheet(period="year")
print(f"Balance Sheet: {len(bs)} năm")
print(bs.columns.tolist()[:5])

# Báo cáo khoản lợi nhập
is_data = finance.income_statement(period="year")
print(f"\nIncome Statement: {len(is_data)} năm")
print(is_data.columns.tolist()[:5])

# Lưu chuyển tiền tệ
cf = finance.cash_flow(period="year")
print(f"\nCash Flow: {len(cf)} năm")
print(cf.columns.tolist()[:5])

# Chỉ số tài chính
ratios = finance.ratio()
print(f"\nRatios: {len(ratios)} bản ghi")
print(f"Các nhóm: {ratios.columns.get_level_values(0).unique().tolist()}")
```

### Ví dụ 2: So Sánh Nhiều Công Ty

```python
from vnstock import Finance

# Danh sách các cổ phiếu
symbols = ['ACB', 'BID', 'CTG']

for symbol in symbols:
    try:
        finance = Finance(source="vci", symbol=symbol)
        
        # Lấy dữ liệu năm mới nhất
        bs = finance.balance_sheet(period="year")
        is_data = finance.income_statement(period="year")
        
        print(f"\n✅ {symbol}")
        print(f"   Balance Sheet: {len(bs)} bản ghi")
        print(f"   Income Statement: {len(is_data)} bản ghi")
    except Exception as e:
        print(f"❌ {symbol}: {type(e).__name__}")
```

## 💾 Lưu Dữ Liệu Tài Chính

```python
from vnstock import Finance
import pandas as pd

finance = Finance(source="vci", symbol="VCI")

# Lấy dữ liệu
bs = finance.balance_sheet(period="year")
is_data = finance.income_statement(period="year")
cf = finance.cash_flow(period="year")

# Export ra CSV
bs.to_csv('balance_sheet.csv', index=False)
is_data.to_csv('income_statement.csv', index=False)
cf.to_csv('cash_flow.csv', index=False)

print("✅ Dữ liệu đã export ra CSV")

# Hoặc export ra Excel
with pd.ExcelWriter('vci_financials.xlsx') as writer:
    bs.to_excel(writer, sheet_name='Balance Sheet', index=False)
    is_data.to_excel(writer, sheet_name='Income Statement', index=False)
    cf.to_excel(writer, sheet_name='Cash Flow', index=False)

print("✅ Dữ liệu đã export ra Excel")
```

## ❌ Các Lỗi Thường Gặp

### Lỗi 1: Invalid Period

```python
# ❌ Sai
df = finance.balance_sheet(period="monthly")

# ✅ Đúng
df = finance.balance_sheet(period="quarter")  # hoặc "year"
```

### Lỗi 2: Source Không Hỗ Trợ

```python
# ❌ Sai - FMP không hỗ trợ Finance
finance = Finance(source="fmp", symbol="AAPL")

# ✅ Đúng - Dùng VCI hoặc TCBS
finance = Finance(source="vci", symbol="VCI")
finance = Finance(source="tcbs", symbol="VCI")
```

### Lỗi 3: Không Có Dữ Liệu

```python
finance = Finance(source="vci", symbol="UNKNOWN")
df = finance.balance_sheet(period="year")

if df is None or len(df) == 0:
    print("❌ Không có dữ liệu tài chính")
else:
    print(df)
```

## 📚 Bước Tiếp Theo

1. [02-Installation](02-installation.md) - Cài đặt
2. [01-Overview](01-overview.md) - Tổng quan
3. [03-Listing API](03-listing-api.md) - Danh sách chứng khoán
4. [04-Quote & Price](04-quote-price-api.md) - Giá lịch sử
5. ✅ **05-Financial API** - Bạn đã ở đây
6. [06-Connector Guide](06-connector-guide.md) - API bên ngoài
7. [07-Best Practices](07-best-practices.md) - Mẹo & kinh nghiệm

---

**Last Updated**: 2024-12-03  
**Version**: 3.3.0  
**Status**: Actively Maintained
