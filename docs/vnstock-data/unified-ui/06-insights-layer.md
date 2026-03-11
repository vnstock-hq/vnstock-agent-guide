# Layer 6: Insights (Phân Tích Chuyên Sâu)

## 📌 Tổng Quan

**Insights Layer** cung cấp **xếp hạng top cổ phiếu** và **bộ lọc chứng khoán** để nhà đầu tư nhận diện cơ hội và xu hướng thị trường.

> **Lưu ý**: Domain **Valuation** (P/E, P/B toàn thị trường) đã được chuyển sang **[Analytics Layer](07-analytics-layer.md)** từ phiên bản Unified UI mới. Nếu trước đây bạn dùng `Insights().valuation`, vui lòng chuyển sang `Analytics().valuation(index)`.

## 🏗️ Cấu Trúc Domain

```python
Insights()
├── .ranking()       # Xếp hạng top cổ phiếu
└── .screener()      # Bộ lọc chứng khoán
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
| `gainer()` | `index`, `limit` | Top cổ phiếu tăng giá | DataFrame |
| `loser()` | `index`, `limit` | Top cổ phiếu giảm giá | DataFrame |
| `value()` | `index`, `limit` | Top cổ phiếu theo giá trị giao dịch | DataFrame |
| `volume()` | `index`, `limit` | Top cổ phiếu theo khối lượng | DataFrame |
| `foreign_buy()` | `date`, `limit` | Top nước ngoài mua nhiều | DataFrame |
| `foreign_sell()` | `date`, `limit` | Top nước ngoài bán nhiều | DataFrame |
| `deal()` | `index`, `limit` | Top giao dịch thỏa thuận | DataFrame |

**Parameters:**
- `index` (str, optional): Chỉ số lọc (ví dụ: `'VNINDEX'`, `'HNX'`). Mặc đình lấy toàn thị trường.
- `limit` (int, optional): Số lượng kết quả. Mặc định 10.
- `date` (str, optional): Ngày giao dịch (YYYY-MM-DD).

#### Ví Dụ

```python
from vnstock_data import Insights

ins = Insights()

# ===== Top Gainer (Tăng Giá) =====
df_gainers = ins.ranking().gainer()
print(df_gainers)

# Top gainer sàn VNINDEX
df_gainers_vn = ins.ranking().gainer(index='VNINDEX', limit=10)
print(df_gainers_vn)

# ===== Top Loser (Giảm Giá) =====
df_losers = ins.ranking().loser()
print(df_losers)

# ===== Top Volume (Khối Lượng) =====
df_volume = ins.ranking().volume()
print(df_volume)

# ===== Foreign Flow (Nước Ngoài Mua) =====
df_foreign_buy = ins.ranking().foreign_buy()
print(df_foreign_buy)

# ===== Foreign Sell (Nước Ngoài Bán) =====
df_foreign_sell = ins.ranking().foreign_sell()
print(df_foreign_sell)

# ===== Top Deal (Giao Dịch Thỏa Thuận) =====
df_deals = ins.ranking().deal()
print(df_deals)
```

---

### 2. Screener Domain (Bộ Lọc Chứng Khoán)

**Source:** VCI (vci)  
**Registry Key:** `"insights.screener"`

#### Mô Tả

Bộ lọc chứng khoán cung cấp dữ liệu toàn thị trường với hàng trăm chỉ tiêu tài chính. Người dùng có thể áp dụng logic lọc tùy chỉnh bằng Pandas.

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `criteria()` | `lang` | Danh sách giải thích tên cột (vi/en) | DataFrame |
| `filter()` | `limit` | Dữ liệu screener toàn thị trường | DataFrame |

**Parameters:**
- `lang` (str): Ngôn ngữ ('vi' hoặc 'en'). Mặc định 'vi'.
- `limit` (int): Số lượng bản ghi tối đa. Mặc định 2000.

#### Ví Dụ

```python
from vnstock_data import Insights

ins = Insights()

# ===== Xem Danh Sách Tiêu Chí =====
criteria_df = ins.screener().criteria(lang="vi")
print(criteria_df)

# ===== Lọc Toàn Thị Trường =====
# Lấy dữ liệu tất cả cổ phiếu với hàng trăm chỉ tiêu
df_all = ins.screener().filter()
print(f"Total stocks: {len(df_all)}")
print(f"Total columns: {len(df_all.columns)}")

# Lọc thủ công bằng Pandas
# Cổ phiếu có P/E < 10 và ROE > 15%
cheap_good = df_all[
    (df_all['pe'] < 10) & (df_all['roe'] > 15)
]
print(f"Cổ phiếu rẻ + chất lượng: {len(cheap_good)}")
print(cheap_good[['ticker', 'pe', 'roe']].head(10))
```

---

## 💡 Best Practices

### 1. Tìm Cơ Hội Giá Trị

```python
from vnstock_data import Insights

ins = Insights()

# Cổ phiếu giảm giá mạnh nhưng có chất
losers = ins.ranking().loser()
screener = ins.screener().filter()

# Merge để tìm cơ hội
opportunity = losers.merge(screener, left_on='code', right_on='ticker', how='inner')
print(opportunity[['ticker', 'pe', 'roe']].head())
```

### 2. Tra Cứu Methods

```python
from vnstock_data import show_api, Insights
show_api(Insights())  # Xem tất cả methods
```

---

## ⚠️ Lưu Ý Quan Trọng

1. **Valuation đã chuyển sang Analytics**: Dùng `Analytics().valuation(index).pe()` thay cho `Insights().valuation.pe()` (đã có ở phiên bản trước)
2. **Phân Tích Không Phải Khuyến Nghị**: Insights là phân tích thị trường, **không phải lời khuyên đầu tư**
3. **Đa Khía Cạnh**: Nên kết hợp nhiều tiêu chí thay vì dựa vào 1 chỉ số
4. **Verify Data**: Luôn xác minh dữ liệu với các nguồn khác trước khi quyết định

---

## 🚦 Next Steps

- **Analytics Layer**: Để xem định giá P/E, P/B thị trường
- **Market Layer**: Để lấy giá thực tế và giao dịch
- **Fundamental Layer**: Để phân tích sâu hơn về BCTC
- **Macro Layer**: Để hiểu tác động của yếu tố vĩ mô
