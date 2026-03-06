# Layer 7: Insights (Phân Tích Chuyên Sâu)

## 📌 Tổng Quan

**Insights Layer** cung cấp **phân tích chuyên sâu, xếp hạng, định giá, và khuyến nghị** từ các chuyên gia tài chính. Giúp nhà đầu tư nhận diện cơ hội, xu hướng thị trường, và đưa ra quyết định dựa trên dữ liệu phân tích.

## 🏗️ Cấu Trúc Domain

```python
Insights()
├── .ranking         # Xếp hạng, top cổ phiếu
├── .valuation       # Định giá, khuyến nghị
└── .screener        # Bộ lọc theo tiêu chí
```

## 📋 Chi Tiết Các Domain

### 1. Ranking Domain (Xếp Hạng & Top)

**Source:** VND (vnd)  
**Registry Key:** `"insights.ranking"`

#### Mô Tả

Xếp hạng top cổ phiếu theo các tiêu chí khác nhau: tăng giá, giảm giá, khối lượng, nước ngoài, v.v.

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `gainer()` | - | Top cổ phiếu tăng giá | DataFrame |
| `loser()` | - | Top cổ phiếu giảm giá | DataFrame |
| `value()` | - | Top cổ phiếu giá trị | DataFrame |
| `volume()` | - | Top cổ phiếu khối lượng cao | DataFrame |
| `foreign_buy()` | - | Top mua nhiều của nước ngoài | DataFrame |
| `foreign_sell()` | - | Top bán nhiều của nước ngoài | DataFrame |
| `deal()` | - | Top cổ phiếu giao dịch khối | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Insights

ins = Insights()

# ===== Top Gainer (Tăng Giá) =====
# Top 10 cổ phiếu tăng giá nhất hôm nay
df_gainers = ins.ranking.gainer()
print(df_gainers[['code', 'price', 'change_percent']].head(10))
#    code  price  change_percent
# 0   VIC  14.50           +5.2%
# 1   TCB  25.30           +4.8%
# 2   HPG  45.00           +4.5%

# ===== Top Loser (Giảm Giá) =====
df_losers = ins.ranking.loser()
print(df_losers[['code', 'price', 'change_percent']].head(5))

# ===== Top Value (Giá Trị) =====
# Cổ phiếu có P/E thấp, P/B thấp
df_value = ins.ranking.value()
print(df_value[['code', 'pe_ratio', 'pb_ratio']].head(10))
#    code  pe_ratio  pb_ratio
# 0   CTG      8.5      0.72
# 1   STB      9.2      0.78
# 2   ACB      9.8      0.85

# ===== Top Volume (Khối Lượng) =====
# Cổ phiếu giao dịch khối lượng cao
df_volume = ins.ranking.volume()
print(df_volume[['code', 'volume', 'value']].head(10))

# ===== Foreign Flow (Nước Ngoài Mua) =====
# Top cổ phiếu nước ngoài mua nhiều
df_foreign_buy = ins.ranking.foreign_buy()
print(df_foreign_buy[['code', 'foreign_buy', 'foreign_sell', 'net']].head(10))
#    code  foreign_buy  foreign_sell     net
# 0   VIC        1500     500     +1000
# 1   TCB         800     300      +500

# ===== Foreign Sell (Nước Ngoài Bán) =====
df_foreign_sell = ins.ranking.foreign_sell()
print(df_foreign_sell.head())

# ===== Block Deals (Giao Dịch Khối) =====
df_deals = ins.ranking.deal()
print(df_deals[['code', 'volume', 'price', 'time']].head(10))
```

---

### 2. Valuation Domain (Định Giá & Khuyến Nghị)

**Source:** VND (vnd)  
**Registry Key:** `"insights.valuation"`

#### Mô Tả

Định giá cổ phiếu, chỉ số P/E, P/B, khuyến nghị từ các chuyên gia.

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `pe()` | - | P/E ratio toàn thị trường | DataFrame |
| `pb()` | - | P/B ratio toàn thị trường | DataFrame |
| `evaluation()` | - | Đánh giá toàn bộ cổ phiếu | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Insights

ins = Insights()

# ===== P/E Ratio Toàn Thị Trường =====
# So sánh P/E của các cổ phiếu
df_pe = ins.valuation.pe()
print(df_pe[['code', 'price', 'eps', 'pe_ratio']].head(20))
#    code  price   eps  pe_ratio
# 0   VIC  14.50  1.45      10.0
# 1   TCB  25.30  3.10       8.2
# 2   HPG  45.00  6.25       7.2

# Phân tích:
# - PE < 10: Rẻ
# - PE 10-15: Bình thường
# - PE > 15: Đắt

cheap_stocks = df_pe[df_pe['pe_ratio'] < 10]
print(f"Cổ phiếu rẻ (PE<10): {len(cheap_stocks)}")
print(cheap_stocks[['code', 'pe_ratio']].head())

# ===== P/B Ratio Toàn Thị Trường =====
df_pb = ins.valuation.pb()
print(df_pb[['code', 'price', 'book_value', 'pb_ratio']].head(20))
#    code  price  book_value  pb_ratio
# 0   VIC  14.50        18.0      0.81
# 1   TCB  25.30        28.0      0.90

# Cổ phiếu dưới giá sổ sách
undervalued = df_pb[df_pb['pb_ratio'] < 0.9]
print(f"Cổ phiếu dưới giá sổ (PB<0.9): {len(undervalued)}")

# ===== Evaluation (Đánh Giá Toàn Thị Trường) =====
# Đánh giá tính hợp lý của giá cổ phiếu
df_eval = ins.valuation.evaluation()
print(df_eval[['code', 'price', 'fair_value', 'rating']].head(20))
#    code  price  fair_value  rating
# 0   VIC  14.50       19.00   UNDERVALUE
# 1   TCB  25.30       22.00   FAIRLY_VALUED
# 2   HPG  45.00       42.00   OVERVALUE

# Phân loại
undervalue = df_eval[df_eval['rating'] == 'UNDERVALUE']
fairly = df_eval[df_eval['rating'] == 'FAIRLY_VALUED']
overvalue = df_eval[df_eval['rating'] == 'OVERVALUE']

print(f"Undervalue: {len(undervalue)}")
print(f"Fairly Valued: {len(fairly)}")
print(f"Overvalue: {len(overvalue)}")
```

---

### 3. Screener Domain (Máy Lọc)

**Source:** VCI (vci)  
**Registry Key:** `"insights.screener"`

#### Mô Tả

Máy lọc chứng khoán theo các tiêu chí tùy chọn: P/E, P/B, ROE, v.v.

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `criteria()` | - | Danh sách các tiêu chí lọc | List |
| `filter()` | `criteria` | Lọc cổ phiếu theo tiêu chí | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Insights

ins = Insights()

# ===== Xem Các Tiêu Chí Có Sẵn =====
criteria_list = ins.screener.criteria()
print("Các tiêu chí lọc:", criteria_list)
# Output:
# ['pe_low', 'pe_high', 'pb_low', 'pb_high', 
#  'roe_low', 'roa_low', 'eps_growth', 'revenue_growth']

# ===== Lọc Cổ Phiếu =====

# Lọc cổ phiếu có P/E < 10 và ROE > 15%
filter_criteria = {
    'pe_low': 0,
    'pe_high': 10,
    'roe_low': 15
}

df_filtered = ins.screener.filter(filter_criteria)
print(df_filtered[['code', 'pe_ratio', 'roe']].head(10))
#    code  pe_ratio   roe
# 0   CTG      8.5  18.2%
# 1   STB      9.2  16.5%
# 2   ACB      9.8  20.1%

# Lọc cổ phiếu có giá tăng mạnh và khối lượng cao
growth_criteria = {
    'eps_growth_low': 10,  # Lợi nhuận tăng > 10%
    'volume_minimum': 1000000  # Khối lượng > 1 triệu
}

df_growth = ins.screener.filter(growth_criteria)
print(f"Cổ phiếu tăng trưởng nhanh: {len(df_growth)}")
```

---

## 🔗 Registry Mapping

```python
INSIGHTS_SOURCES = {
    "insights.ranking": {
        "gainer": ("vnd", "insight", "TopStock", "gainer"),
        "loser": ("vnd", "insight", "TopStock", "loser"),
        "value": ("vnd", "insight", "TopStock", "value"),
        "volume": ("vnd", "insight", "TopStock", "volume"),
        "foreign_buy": ("vnd", "insight", "TopStock", "foreign_buy"),
        "foreign_sell": ("vnd", "insight", "TopStock", "foreign_sell"),
        "deal": ("vnd", "insight", "TopStock", "deal"),
    },
    "insights.valuation": {
        "pe": ("vnd", "market", "Market", "pe"),
        "pb": ("vnd", "market", "Market", "pb"),
        "evaluation": ("vnd", "market", "Market", "evaluation"),
    },
    "insights.screener": {
        "criteria": ("vci", "screener", "Screener", "get_criteria"),
        "filter": ("vci", "screener", "Screener", "filter"),
    }
}
```

---

## 💡 Best Practices

### 1. Tìm Cơ Hội Giá Trị

```python
from vnstock_data import Insights

ins = Insights()

# Cổ phiếu vừa giảm giá nhưng có giá trị
losers = ins.ranking.loser()
valuations = ins.valuation.evaluation()

# Merge để tìm cổ phiếu giảm giá nhưng undervalue
opportunity = losers.merge(valuations, on='code')
opportunity = opportunity[
    (opportunity['change_percent'] < -5) &  # Giảm > 5%
    (opportunity['rating'] == 'UNDERVALUE')  # Nhưng undervalue
]

print("Cơ hội mua:")
print(opportunity[['code', 'price', 'change_percent', 'rating']])
```

### 2. Theo Dõi Dòng Tiền Nước Ngoài

```python
from vnstock_data import Insights

ins = Insights()

# Cổ phiếu nước ngoài mua nhiều
foreign_buying = ins.ranking.foreign_buy()
print("Top nước ngoài mua:")
print(foreign_buying[['code', 'foreign_buy', 'net']].head(10))

# Cổ phiếu nước ngoài bán nhiều
foreign_selling = ins.ranking.foreign_sell()
print("Top nước ngoài bán:")
print(foreign_selling[['code', 'foreign_sell', 'net']].head(10))

# Tín hiệu: Nước ngoài bán mạnh có thể là cảnh báo
```

### 3. Phân Tích Tham Chiếu Định Giá

```python
from vnstock_data import Insights, Reference

ins = Insights()
ref = Reference()

# Danh sách cổ phiếu
stocks = ref.equity.list()

# Lấy P/E toàn thị trường
pe_data = ins.valuation.pe()

# Tính P/E trung bình ngành
pe_bank = pe_data[pe_data['code'].isin(['TCB', 'VCB', 'BID', 'ACB'])]
avg_pe_bank = pe_bank['pe_ratio'].mean()

print(f"P/E trung bình ngân hàng: {avg_pe_bank:.1f}")

# Tìm ngân hàng rẻ hơn trung bình
cheap_banks = pe_bank[pe_bank['pe_ratio'] < avg_pe_bank * 0.9]
print("Ngân hàng rẻ hơn 10% trung bình:")
print(cheap_banks[['code', 'pe_ratio']].head())
```

### 4. Quản Lý Danh Mục Đầu Tư

```python
from vnstock_data import Insights

ins = Insights()

# Danh mục cá nhân
my_portfolio = ['TCB', 'VIC', 'HPG', 'VNM']

# Lấy valuation
pe_data = ins.valuation.pe()
portfolio_pe = pe_data[pe_data['code'].isin(my_portfolio)]

print("Định giá danh mục:")
print(portfolio_pe[['code', 'price', 'pe_ratio', 'change_percent']])

# Đánh giá
eval_data = ins.valuation.evaluation()
portfolio_eval = eval_data[eval_data['code'].isin(my_portfolio)]

for _, row in portfolio_eval.iterrows():
    print(f"{row['code']}: {row['rating']} " 
          f"(Fair: {row['fair_value']:.0f}, Current: {row['price']:.0f})")
```

---

## ⚠️ Lưu Ý Quan Trọng

1. **Phân Tích Không Phải Khuyến Nghị**: Insights là phân tích thị trường, **không phải lời khuyên đầu tư**
2. **Thay Đổi Thường Xuyên**: Xếp hạng top, valuation thay đổi hằng ngày
3. **Đa Khía Cạnh**: Nên kết hợp nhiều tiêu chí (PE, PB, ROE, etc.) thay vì dựa vào 1 chỉ số
4. **Verify Data**: Luôn xác minh dữ liệu với các nguồn khác trước khi quyết định

---

## 🚦 Next Steps

- **Market Layer**: Để lấy giá thực tế và giao dịch
- **Fundamental Layer**: Để phân tích sâu hơn về BCTC
- **Macro Layer**: Để hiểu tác động của yếu tố vĩ mô
