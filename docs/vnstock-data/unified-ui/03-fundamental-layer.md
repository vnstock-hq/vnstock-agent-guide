# Layer 3: Fundamental Data (Dữ Liệu Cơ Bản)

## 📌 Tổng Quan

**Fundamental Layer** cung cấp dữ liệu **báo cáo tài chính** (BCTC) và **chỉ số tài chính** phục vụ cho phân tích cơ bản của doanh nghiệp. Bao gồm báo cáo thu nhập, cân đối kế toán, lưu chuyển tiền tệ, và các tỷ số tài chính quan trọng.

## 🏗️ Cấu Trúc Domain

```python
Fundamental()
└── .equity          # Dữ liệu tài chính chứng khoán
    ├── .income_statement        # Báo cáo thu nhập
    ├── .balance_sheet           # Cân đối kế toán
    ├── .cash_flow               # Lưu chuyển tiền tệ
    └── .ratio                   # Tỷ số tài chính
```

## 📋 Chi Tiết Các Domain

### 1. Income Statement (Báo Cáo Thu Nhập)

**Source:** KBS (kbs)  
**Registry Key:** `"equity.fundamental.income_statement"`

#### Mô Tả

Báo cáo thu nhập hàng quý/năm, gồm doanh thu, chi phí, lợi nhuận.

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `income_statement()` | `symbol`, `period` | Báo cáo thu nhập | DataFrame |

**Parameters:**
- `symbol`: Mã chứng khoán (ví dụ: "TCB")
- `period`: "Q" (quý) hoặc "Y" (năm), default = "Q"

#### Ví Dụ

```python
from vnstock_data import Fundamental

fun = Fundamental()

# Báo cáo thu nhập quý
df_income_q = fun.equity.income_statement("TCB", period="Q")
print(df_income_q)
# Output columns: 
# date, revenue, cost_of_revenue, gross_profit, 
# operating_expense, operating_profit, net_profit, eps

# Báo cáo thu nhập năm
df_income_y = fun.equity.income_statement("HPG", period="Y")
print(df_income_y[['date', 'revenue', 'net_profit']])

# 5 năm gần nhất
df_income_hist = fun.equity.income_statement("VNM", period="Y")
print(df_income_hist.tail(5))
#                date     revenue    net_profit
# 0      2021-12-31  123456789.0     12345678.0
# 1      2022-12-31  145678901.0     15678901.0
```

---

### 2. Balance Sheet (Cân Đối Kế Toán)

**Source:** KBS (kbs)  
**Registry Key:** `"equity.fundamental.balance_sheet"`

#### Mô Tả

Cân đối kế toán hàng quý/năm, gồm tài sản, nợ, vốn chủ sở hữu.

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `balance_sheet()` | `symbol`, `period` | Cân đối kế toán | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Fundamental

fun = Fundamental()

# Cân đối kế toán quý
df_bs_q = fun.equity.balance_sheet("TCB", period="Q")
print(df_bs_q)
# Output columns:
# date, total_assets, current_assets, fixed_assets,
# total_liabilities, current_liabilities, long_term_liabilities,
# equity

# Cân đối kế toán năm
df_bs_y = fun.equity.balance_sheet("VIC", period="Y")
print(df_bs_y[['date', 'total_assets', 'total_liabilities', 'equity']])

# Phân tích xu hướng tài sản
assets_trend = fun.equity.balance_sheet("HPG", period="Y")
print(assets_trend[['date', 'total_assets']].tail(3))
```

---

### 3. Cash Flow (Lưu Chuyển Tiền Tệ)

**Source:** KBS (kbs)  
**Registry Key:** `"equity.fundamental.cash_flow"`

#### Mô Tả

Báo cáo lưu chuyển tiền tệ từ hoạt động kinh doanh, đầu tư, và tài chính.

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `cash_flow()` | `symbol`, `period` | Lưu chuyển tiền tệ | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Fundamental

fun = Fundamental()

# Lưu chuyển tiền tệ quý
df_cf_q = fun.equity.cash_flow("TCB", period="Q")
print(df_cf_q)
# Output columns:
# date, operating_cash_flow, investing_cash_flow,
# financing_cash_flow, free_cash_flow

# Lưu chuyển tiền tệ năm
df_cf_y = fun.equity.cash_flow("VNM", period="Y")
print(df_cf_y[['date', 'operating_cash_flow', 'free_cash_flow']])

# Kiểm tra sức khỏe dòng tiền
cf_health = fun.equity.cash_flow("VIC", period="Y")
print(cf_health[['date', 'operating_cash_flow', 'investing_cash_flow']].tail(3))
```

---

### 4. Financial Ratio (Tỷ Số Tài Chính)

**Source:** KBS (kbs)  
**Registry Key:** `"equity.fundamental.ratio"`

#### Mô Tả

Các tỷ số tài chính quan trọng: PE, PB, ROE, ROA, Debt/Equity, v.v.

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `ratio()` | `symbol`, `period` | Tỷ số tài chính | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Fundamental

fun = Fundamental()

# Tỷ số tài chính
df_ratio = fun.equity.ratio("TCB")
print(df_ratio)
# Output columns:
# date, pe_ratio, pb_ratio, eps, roa, roe,
# debt_to_equity, current_ratio, quick_ratio,
# profit_margin, return_on_assets, return_on_equity

# Tỷ số chính
ratios = fun.equity.ratio("HPG")
print(ratios[['date', 'pe_ratio', 'pb_ratio', 'roe', 'roa']].tail(3))
#               date  pe_ratio  pb_ratio     roe     roa
# 0      2026-03-06      10.5       0.85   15.2%    5.8%
# 1      2026-02-06      10.3       0.83   15.0%    5.6%

# Phân tích xu hướng ROE
roe_trend = fun.equity.ratio("VNM")
print(roe_trend[['date', 'roe']].tail(5))

# So sánh các tỷ số trong ngành
tech_stocks = ["FPT", "MWG", "VTG"]
for symbol in tech_stocks:
    ratio = fun.equity.ratio(symbol)
    print(f"{symbol}: PE={ratio['pe_ratio'].iloc[-1]:.1f}, "
          f"ROE={ratio['roe'].iloc[-1]:.1f}%")
```

---

## 🔗 Registry Mapping

```python
FUNDAMENTAL_SOURCES = {
    "equity.fundamental": {
        "income_statement": ("kbs", "financial", "Finance", "income_statement"),
        "balance_sheet": ("kbs", "financial", "Finance", "balance_sheet"),
        "cash_flow": ("kbs", "financial", "Finance", "cash_flow"),
        "ratio": ("kbs", "financial", "Finance", "ratio"),
        "note": ("vci", "financial", "Finance", "note")
    }
}
```

---

## 💡 Best Practices

### 1. Phân Tích Tài Chính Cơ Bản

```python
from vnstock_data import Fundamental, Market

fun = Fundamental()
mkt = Market()

symbol = "TCB"

# Lấy dữ liệu tài chính
income = fun.equity.income_statement(symbol, period="Y")
balance = fun.equity.balance_sheet(symbol, period="Y")
ratio = fun.equity.ratio(symbol)

# Lấy giá hiện tại
quote = mkt.equity.quote(symbol)

# Tính toán các chỉ số
recent_ratio = ratio.iloc[-1]
recent_income = income.iloc[-1]

print(f"Stock: {symbol}")
print(f"Current Price: {quote['close'].values[0]:.0f}")
print(f"PE Ratio: {recent_ratio['pe_ratio']:.1f}")
print(f"PB Ratio: {recent_ratio['pb_ratio']:.2f}")
print(f"ROE: {recent_ratio['roe']:.1f}%")
print(f"Annual Revenue: {recent_income['revenue']:,.0f}")
print(f"Net Profit: {recent_income['net_profit']:,.0f}")
```

### 2. So Sánh Giữa Các Công Ty

```python
from vnstock_data import Fundamental

fun = Fundamental()

# So sánh PE ratio trong ngành Ngân hàng
banks = ["TCB", "VCB", "BID", "ACB"]
pe_ratios = {}

for bank in banks:
    ratio = fun.equity.ratio(bank)
    pe_ratios[bank] = ratio['pe_ratio'].iloc[-1]

# Tìm cổ phiếu rẻ nhất
cheapest = min(pe_ratios, key=pe_ratios.get)
print(f"Rẻ nhất: {cheapest} (PE={pe_ratios[cheapest]:.1f})")

# Tìm đắt nhất
most_expensive = max(pe_ratios, key=pe_ratios.get)
print(f"Đắt nhất: {most_expensive} (PE={pe_ratios[most_expensive]:.1f})")
```

### 3. Kiểm Tra Xu Hướng Lợi Nhuận

```python
from vnstock_data import Fundamental
import pandas as pd

fun = Fundamental()

# Lợi nhuận 5 năm
income = fun.equity.income_statement("VNM", period="Y")
gross_margin = income['revenue'] / income['gross_profit']
net_margin = income['net_profit'] / income['revenue']

df_margins = pd.DataFrame({
    'date': income['date'],
    'revenue': income['revenue'],
    'gross_margin': gross_margin,
    'net_margin': net_margin
})

print(df_margins.tail())

# Kiểm tra xu hướng
if df_margins['net_margin'].iloc[-1] > df_margins['net_margin'].iloc[-2]:
    print("✓ Lợi nhuận ròng tăng")
else:
    print("✗ Lợi nhuận ròng giảm")
```

### 4. Phân Tích Khả Năng Thanh Toán

```python
from vnstock_data import Fundamental

fun = Fundamental()

symbol = "HPG"
ratio = fun.equity.ratio(symbol)
recent_ratio = ratio.iloc[-1]

current_ratio = recent_ratio.get('current_ratio', 0)
quick_ratio = recent_ratio.get('quick_ratio', 0)
debt_to_equity = recent_ratio.get('debt_to_equity', 0)

print(f"Stock: {symbol}")
print(f"Current Ratio: {current_ratio:.2f} (>1.0 tốt)")
print(f"Quick Ratio: {quick_ratio:.2f} (>1.0 tốt)")
print(f"Debt/Equity: {debt_to_equity:.2f} (<1.0 tốt)")

# Nhận xét
if current_ratio > 1.5:
    print("✓ Khả năng thanh toán ngắn hạn tốt")
else:
    print("⚠️ Khả năng thanh toán ngắn hạn yếu")
```

---

## ⚠️ Lưu Ý Quan Trọng

1. **Tần Suất Update**: BCTC được công bố quý/năm, không update realtime
2. **Độ Trễ**: Dữ liệu thường có độ trễ 1-2 tuần sau kì báo cáo
3. **Tính Toán Lại**: Một số dữ liệu có thể được tính toán lại (restatement)
4. **Múc Tiền Tệ**: Toàn bộ dữ liệu tính bằng VND

---

## 🚦 Next Steps

- **Market Layer**: Để lấy giá hiện tại và lịch sử giao dịch
- **Insights Layer**: Để xem khuyến nghị dựa trên phân tích
- **Macro Layer**: Để hiểu tác động của yếu tố kinh tế toàn cảnh
