# 07 - Financial API - Dữ Liệu Tài Chính

## 📖 Giới Thiệu

Financial API cung cấp các phương thức lấy dữ liệu tài chính doanh nghiệp, bao gồm:

- **Báo cáo tài chính**: Bảng cân đối kế toán, Khoản lợi nhập, Lưu chuyển tiền tệ
- **Chỉ số tài chính**: ROE, ROA, EPS, P/E, Debt ratio, v.v.
- **Chu kỳ báo cáo**: Hàng quý (Quarter) hoặc hàng năm (Year)
- **Phân tích**: Xu hướng tài chính, so sánh ngành

## 🔌 So Sánh Nguồn Dữ Liệu

| Method | KBS | VCI | Ghi Chú |
|--------|-----|-----|---------|
| **income_statement()** | ✅ | ✅ | KBS: 90 items, VCI: 25+ columns |
| **balance_sheet()** | ✅ | ✅ | KBS: 162 items, VCI: 36 columns |
| **cash_flow()** | ✅ | ✅ | KBS: 159 items, VCI: 39 columns |
| **ratio()** | ✅ | ✅ | KBS: 27 ratios, VCI: 37+ ratios |

**Tổng số methods:**
- **KBS**: 4 methods
- **VCI**: 4 methods

**Khuyến nghị:**
- **KBS**: Dữ liệu chi tiết theo dòng (item-based), phù hợp phân tích chuyên sâu
- **VCI**: Dữ liệu theo cột (column-based), dễ sử dụng và tích hợp

## 🏗️ Khởi Tạo

```python
from vnstock import Finance

# Khởi tạo với KBS
finance_kbs = Finance(
    source="kbs",           # Nguồn dữ liệu
    symbol="VCI",            # Mã chứng khoán
    standardize_columns=True,  # Chuẩn hóa tên cột
    random_agent=False      # Sử dụng random user agent
)

# Khởi tạo với VCI
finance_vci = Finance(
    source="vci",            # Nguồn dữ liệu
    symbol="VCI",            # Mã chứng khoán
    period="quarter",        # Chu kỳ mặc định
    get_all=True,            # Lấy tất cả các trường
    show_log=False           # Hiển thị log
)
```

## 📊 Cấu Trúc Dữ Liệu So Sánh

### KBS Data Structure

**Format:** Item-based (dòng-based)
- **Shape**: (N items, 10 columns)
- **Index**: Không có index name
- **Columns tiêu chuẩn**:
  ```
  ['item', 'item_en', 'item_id', 'unit', 'levels', 'row_number', 
   '2025-Q3', '2025-Q2', '2025-Q1', '2024-Q4']
  ```
- **Đặc điểm**:
  - Mỗi dòng là một chỉ tiêu tài chính
  - Các cột thời gian là các quý/ năm
  - Có cả tên tiếng Việt và tiếng Anh
  - Có hierarchical levels

### VCI Data Structure

**Format:** Column-based (cột-based)
- **Shape**: (51 periods, N columns)
- **Index**: Không có index name
- **Columns tiêu chuẩn**:
  ```
  ['ticker', 'yearReport', 'lengthReport', ...financial_fields...]
  ```
- **Đặc điểm**:
  - Mỗi dòng là một kỳ báo cáo
  - Các cột là các chỉ tiêu tài chính
  - Tên cột theo tiếng Anh có đơn vị
  - MultiIndex cho ratios

## 📚 Phương Thức Chính

### 1. income_statement() - Báo Cáo Kết Quả Kinh Doanh

Lấy dữ liệu báo cáo kết quả hoạt động kinh doanh.

**KBS:**
```python
finance = Finance(source="kbs", symbol="VCI")
df = finance.income_statement(period="quarter")

print(f"Shape: {df.shape}")  # (90, 10)
print(f"Columns: {list(df.columns)}")
# ['item', 'item_en', 'item_id', 'unit', 'levels', 'row_number', 
#  '2025-Q3', '2025-Q2', '2025-Q1', '2024-Q4']

# Xem các chỉ tiêu chính
print(df[df['levels'] == 1][['item', 'item_en', '2025-Q3']].head())
```

**Output KBS:**
```
Shape: (90, 10)
Columns: ['item', 'item_en', 'item_id', 'unit', 'levels', 'row_number', '2025-Q3', '2025-Q2', '2025-Q1', '2024-Q4']

                 item                 item_en  2025-Q3
0            Doanh thu               Revenue  1200.5
1        Lợi nhuận gộp           Gross_profit   450.2
2    Lợi nhuận hoạt động       Operating_profit   180.3
3  Lợi nhuận trước thuế     Profit_before_tax   165.1
4      Lợi nhuận sau thuế           Net_profit   132.4
```

**VCI:**
```python
finance = Finance(source="vci", symbol="VCI")
df = finance.income_statement(period="quarter")

print(f"Shape: {df.shape}")  # (51, 25)
print(f"Columns: {list(df.columns)}")
# ['ticker', 'yearReport', 'lengthReport', 'Revenue (Bn. VND)', 
#  'Revenue YoY (%)', 'Cost of Sales', 'Gross Profit', ...]

# Xem dữ liệu gần nhất
print(df[['ticker', 'yearReport', 'Revenue (Bn. VND)', 'Net Profit For the Year']].tail())
```

**Output VCI:**
```
Shape: (51, 25)
Columns: ['ticker', 'yearReport', 'lengthReport', 'Revenue (Bn. VND)', 
          'Revenue YoY (%)', 'Attribute to parent company (Bn. VND)', ...]

   ticker  yearReport  Revenue (Bn. VND)  Net Profit For the Year
46    VCI        2025               1200                    132
47    VCI        2024               1150                    125
48    VCI        2023               1080                    118
```

### 2. balance_sheet() - Bảng Cân Đối Kế Toán

Lấy dữ liệu bảng cân đối kế toán.

**KBS:**
```python
df = finance.balance_sheet(period="quarter")
print(f"Shape: {df.shape}")  # (162, 10)

# Các chỉ tiêu quan trọng
key_items = ['Tổng tài sản', 'Tài sản ngắn hạn', 'Vốn chủ sở hữu', 'Nợ phải trả']
print(df[df['item'].isin(key_items)][['item', '2025-Q3']])
```

**VCI:**
```python
df = finance.balance_sheet(period="quarter")
print(f"Shape: {df.shape}")  # (51, 36)

# Các chỉ tiêu quan trọng
key_cols = ['TOTAL ASSETS (Bn. VND)', 'CURRENT ASSETS (Bn. VND)', 
           "OWNER'S EQUITY(Bn.VND)", 'LIABILITIES (Bn. VND)']
print(df[['ticker', 'yearReport'] + key_cols].tail())
```

### 3. cash_flow() - Báo Cáo Lưu Chuyển Tiền Tệ

Lấy dữ liệu báo cáo lưu chuyển tiền tệ.

**KBS:**
```python
df = finance.cash_flow(period="quarter")
print(f"Shape: {df.shape}")  # (159, 10)

# Các dòng tiền quan trọng
cash_items = ['Lưu chuyển tiền từ hoạt động', 'Lưu chuyển tiền từ đầu tư', 
              'Lưu chuyển tiền từ tài chính', 'Thay đổi tiền mặt']
print(df[df['item'].isin(cash_items)][['item', '2025-Q3']])
```

**VCI:**
```python
df = finance.cash_flow(period="quarter")
print(f"Shape: {df.shape}")  # (51, 39)

# Các dòng tiền quan trọng
cash_cols = ['Net cash inflows/outflows from operating activities',
             'Net Cash Flows from Investing Activities',
             'Cash flows from financial activities',
             'Net increase/decrease in cash and cash equivalents']
print(df[['ticker', 'yearReport'] + cash_cols].tail())
```

### 4. ratio() - Chỉ Số Tài Chính

Lấy các chỉ số tài chính quan trọng.

**KBS:**
```python
df = finance.ratio(period="quarter")
print(f"Shape: {df.shape}")  # (27, 10)

# Các chỉ số quan trọng
ratio_items = ['PE', 'PB', 'ROE', 'ROA', 'Beta']
print(df[df['item'].isin(ratio_items)][['item', 'item_en', '2025-Q3']])
```

**Output KBS:**
```
Shape: (27, 10)
     item item_en  2025-Q3
0      PE     pe     12.5
1      PB     pb      1.8
2     ROE    roe     15.2
3     ROA    roa      8.7
4   Beta   beta      1.2
```

**VCI:**
```python
df = finance.ratio(period="quarter", flatten_columns=True)
print(f"Shape: {df.shape}")  # (51, 37+)

# Các chỉ số quan trọng
ratio_cols = ['Chỉ tiêu định giá_P/E', 'Chỉ tiêu định giá_P/B', 
              'Chỉ tiêu khả năng sinh lợi_ROE (%)', 'Chỉ tiêu khả năng sinh lợi_ROA (%)']
print(df[['ticker', 'yearReport'] + ratio_cols].tail())
```

**Output VCI:**
```
Shape: (51, 37)
   ticker  yearReport  Chỉ tiêu định giá_P/E  Chỉ tiêu định giá_P/B  \
46    VCI        2025                   12.5                    1.8
47    VCI        2024                   11.8                    1.7

   Chỉ tiêu khả năng sinh lợi_ROE (%)  Chỉ tiêu khả năng sinh lợi_ROA (%)
46                             15.2                          8.7
47                             14.8                          8.3
```

## 🎯 So Sánh Chi Tiết

### Data Format Comparison

| Feature | KBS | VCI | Ưu Điểm |
|---------|-----|-----|---------|
| **Structure** | Item-based rows | Column-based periods | KBS chi tiết, VCI dễ dùng |
| **Language** | Việt Nam + Anh | Tiếng Anh | KBS đa ngôn ngữ |
| **Units** | Trong column 'unit' | Trong tên column | VCI rõ ràng hơn |
| **Time Series** | Columns là thời gian | Rows là thời gian | Tùy chọn use case |
| **Hierarchical** | Có levels | Không | KBS có cấu trúc |

### Field Mapping Examples

**KBS → VCI Mapping:**
```
KBS: 'Doanh thu' → VCI: 'Revenue (Bn. VND)'
KBS: 'Lợi nhuận sau thuế' → VCI: 'Net Profit For the Year'
KBS: 'Tổng tài sản' → VCI: 'TOTAL ASSETS (Bn. VND)'
KBS: 'Vốn chủ sở hữu' → VCI: "OWNER'S EQUITY(Bn.VND)"
KBS: 'PE' → VCI: 'Chỉ tiêu định giá_P/E'
```

### Use Case Recommendations

**Dùng KBS khi:**
- Cần phân tích chi tiết theo dòng chỉ tiêu
- Muốn dữ liệu đa ngôn ngữ (Việt + Anh)
- Cần hierarchical structure
- Muốn số lượng items nhiều hơn

**Dùng VCI khi:**
- Cần tích hợp dễ dàng với pandas/Excel
- Muốn format column-based chuẩn
- Cần các chỉ tiêu tài chính đầy đủ
- Muốn multi-level ratios

## 💡 Mẹo Sử Dụng

### 1. Chuyển đổi KBS sang VCI format

```python
# KBS format → VCI format (transpose)
def kbs_to_vci_format(df_kbs):
    # Chọn các cột số liệu
    data_cols = [col for col in df_kbs.columns if col.isdigit() or 'Q' in col]
    
    # Transpose để thời gian thành rows
    df_transposed = df_kbs.set_index('item_en')[data_cols].T
    
    # Reset index để thời gian thành column
    df_transposed = df_transposed.reset_index()
    df_transposed.columns = ['period'] + list(df_transposed.columns[1:])
    
    return df_transposed

# Sử dụng
finance_kbs = Finance(source="kbs", symbol="VCI")
df_kbs = finance_kbs.income_statement(period="quarter")
df_vci_format = kbs_to_vci_format(df_kbs)
```

### 2. Lấy các chỉ tiêu quan trọng

```python
# KBS - Lọc theo levels
def get_kbs_key_items(df, level=1):
    """Lấy các chỉ tiêu chính (level 1)"""
    return df[df['levels'] == level]

# VCI - Lọc theo pattern
def get_vci_key_columns(df):
    """Lấy các cột chính"""
    key_patterns = ['Revenue', 'Profit', 'Assets', 'Equity', 'Cash']
    key_cols = [col for col in df.columns 
                if any(pattern in col for pattern in key_patterns)]
    return ['ticker', 'yearReport'] + key_cols
```

### 3. Kết hợp dữ liệu từ cả hai nguồn

```python
# Kết hợp để đối chiếu
finance_kbs = Finance(source="kbs", symbol="VCI")
finance_vci = Finance(source="vci", symbol="VCI")

# Lấy revenue từ cả hai nguồn
revenue_kbs = finance_kbs.income_statement(period="quarter")
revenue_vci = finance_vci.income_statement(period="quarter")

# Chuẩn hóa và so sánh
kbs_revenue = revenue_kbs[revenue_kbs['item_en'] == 'Revenue']['2025-Q3'].iloc[0]
vci_revenue = revenue_vci[revenue_vci['yearReport'] == 2025]['Revenue (Bn. VND)'].iloc[0]

print(f"KBS Revenue: {kbs_revenue}")
print(f"VCI Revenue: {vci_revenue}")
print(f"Difference: {abs(kbs_revenue - vci_revenue):.2f}")
```

## 🚨 Lưu Ý Quan Trọng

1. **Data Validation**: Luôn kiểm tra shape và columns trước khi xử lý
2. **Missing Data**: VCI có thể có NaN cho các chỉ tiêu không áp dụng
3. **Unit Differences**: KBS dùng unit column, VCI ghi trong tên column
4. **Period Format**: KBS dùng "2025-Q3", VCI dùng năm 2025
5. **Language**: KBS support Việt Nam, VCI chỉ tiếng Anh
6. **Memory Usage**: KBS có nhiều items hơn, VCI có nhiều periods hơn

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

# ✅ Đúng - Dùng VCI hoặc KBS
finance = Finance(source="vci", symbol="VCI")
finance = Finance(source="kbs", symbol="VCI")
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
