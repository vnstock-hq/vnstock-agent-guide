# 09 - Screener API - Lọc Chứng Khoán Nâng Cao

## 📖 Giới Thiệu

**Screener API** cung cấp công cụ lọc chứng khoán nâng cao dựa trên 102 tiêu chí tài chính, kỹ thuật và cơ bản.

## 🔌 Nguồn Dữ Liệu

| Nguồn | Hỗ Trợ | Ghi Chú |
|-------|--------|--------|
| TCBS | ✅ | Screener chính thức của TCBS |

## 🚀 Bắt Đầu

```python
from vnstock import Screener

# Khởi tạo
screener = Screener(source="tcbs")

# Lọc chứng khoán
results = screener.stock(limit=30)
print(f"Tổng chứng khoán: {len(results)}")
print(results.columns)
```

## 📚 Phương Thức Chính

### 1. stock() - Lọc Chứng Khoán

Lọc chứng khoán theo các tiêu chí khác nhau.

**Tham số:**
- `params` (dict, tùy chọn): Các tiêu chí lọc (API TCBS)
  - Nếu `None`, lọc tất cả chứng khoán
- `limit` (int, tùy chọn): Giới hạn số kết quả, mặc định: 50
- `id` (str, tùy chọn): ID của screener được lưu
- `lang` (str, tùy chọn): Ngôn ngữ kết quả
  - `"vi"` - Tiếng Việt (mặc định)
  - `"en"` - Tiếng Anh

**Trả về:** `pd.DataFrame` (102 cột)

**Cột Chính:**
- `ticker` - Mã chứng khoán (str)
- `exchange` - Sàn giao dịch (str)
- `industry` - Ngành công nghiệp (str)

**Cột Tài Chính:**
- `market_cap` - Vốn hóa thị trường (float64)
- `pe` - Tỷ số P/E (float64)
- `pb` - Tỷ số P/B (float64)
- `ps` - Tỷ số P/S (float64)
- `ev_ebitda` - EV/EBITDA (float64)
- `roe` - ROE (float64, %)
- `roa` - ROA (float64, %)
- `dividend_yield` - Lợi suất cổ tức (float64, %)
- `gross_margin` - Lợi nhuận gộp (float64, %)
- `net_margin` - Lợi nhuận ròng (float64, %)
- `eps` - Earnings per share (float64)
- `eps_growth_1y` - Tăng trưởng EPS 1 năm (float64, %)
- `eps_growth_5y` - Tăng trưởng EPS 5 năm (float64, %)
- `revenue_growth_1y` - Tăng trưởng doanh thu 1 năm (float64, %)
- `revenue_growth_5y` - Tăng trưởng doanh thu 5 năm (float64, %)

**Cột Kỹ Thuật:**
- `price_near_realtime` - Giá gần real-time (float64)
- `price_vs_sma5`, `price_vs_sma10`, `price_vs_sma20`, `price_vs_sma50`, `price_vs_sma100`, `price_vs_sma200` - Giá so với SMA (str)
- `rsi14` - RSI(14) (float64)
- `rsi14_status` - Trạng thái RSI (str)
- `macd_histogram` - MACD Histogram (float64)
- `relative_strength_3d`, `rel_strength_1m`, `rel_strength_3m`, `rel_strength_1y` - Cường độ tương đối (float64)
- `breakout` - Tín hiệu vượt (str)
- `bolling_band_signal` - Tín hiệu Bollinger Band (str)
- `sar_vs_macd_hist` - SAR vs MACD (str)

**Cột Giao Dịch:**
- `avg_trading_value_5d`, `avg_trading_value_10d`, `avg_trading_value_20d` - Giá trị giao dịch trung bình (float64)
- `total_trading_value` - Tổng giá trị giao dịch (float64)
- `foreign_transaction` - Giao dịch của nước ngoài (str)
- `foreign_vol_pct` - Khối lượng nước ngoài (float64, %)
- `high_vol_match` - Khối lượng giao dịch cao (float64)

**Cột Khác:**
- `stock_rating` - Xếp hạng (float64)
- `tcbs_recommend` - Khuyến nghị TCBS (str)
- `tcbs_buy_sell_signal` - Tín hiệu mua/bán TCBS (str)
- ... và 50+ cột khác

**Ví dụ:**
```python
from vnstock import Screener

screener = Screener(source="tcbs")

# Lọc tất cả chứng khoán
results = screener.stock(limit=50)
print(f"Tổng chứng khoán: {len(results)}")  # 50
print(f"Tổng cột: {len(results.columns)}")  # 102

# Xem cột
print(list(results.columns)[:20])
```

## 💡 Ví Dụ Thực Tế

### Lọc Chứng Khoán Giá Trị (Value Stock)

```python
from vnstock import Screener
import pandas as pd

screener = Screener(source="tcbs")
results = screener.stock(limit=500)

# Tiêu chí value: P/E thấp, P/B thấp, dividend yield cao
value_stocks = results[
    (results['pe'] < 15) &
    (results['pb'] < 2) &
    (results['dividend_yield'] > 3)
].sort_values('dividend_yield', ascending=False)

if len(value_stocks) > 0:
    print(f"Chứng khoán giá trị: {len(value_stocks)}")
    print(value_stocks[[
        'ticker', 'pe', 'pb', 'dividend_yield'
    ]].head(10).to_string())
```

### Lọc Chứng Khoán Tăng Trưởng (Growth Stock)

```python
from vnstock import Screener

screener = Screener(source="tcbs")
results = screener.stock(limit=500)

# Tiêu chí growth: P/E cao nhưng có growth cao
growth_stocks = results[
    (results['pe'] > 20) &
    (results['eps_growth_5y'] > 15) &
    (results['market_cap'] > 100000)
].sort_values('eps_growth_5y', ascending=False)

if len(growth_stocks) > 0:
    print(f"Chứng khoán tăng trưởng: {len(growth_stocks)}")
    print(growth_stocks[[
        'ticker', 'pe', 'eps_growth_5y'
    ]].head(10).to_string())
```

### Lọc Chứng Khoán Theo Ngành

```python
from vnstock import Screener

screener = Screener(source="tcbs")
results = screener.stock(limit=500)

# Xem các ngành
industries = results['industry'].unique()
print(f"Số ngành: {len(industries)}")
print(list(industries)[:10])

# Lọc ngành Công nghệ/IT
tech_stocks = results[results['industry'].str.contains(
    'Công nghệ|IT|Điện tử', case=False, na=False
)]

print(f"\nChứng khoán công nghệ: {len(tech_stocks)}")
print(tech_stocks[[
    'ticker', 'industry', 'pe', 'revenue_growth_1y'
]].head())
```

### Tìm Chứng Khoán Xu Hướng Tăng (Momentum)

```python
from vnstock import Screener

screener = Screener(source="tcbs")
results = screener.stock(limit=500)

# Xu hướng tăng: Giá trên SMA, RSI tích cực
momentum_stocks = results[
    (results['price_vs_sma20'].notna()) &
    (results['price_vs_sma20'].str.contains('trên|cắt lên', case=False, na=False)) &
    (results['rsi14'] > 50) &
    (results['rsi14'] < 70)  # Không quá mua
]

if len(momentum_stocks) > 0:
    print(f"Chứng khoán momentum: {len(momentum_stocks)}")
    print(momentum_stocks[[
        'ticker', 'price_near_realtime', 'rsi14', 'price_vs_sma20'
    ]].head(10).to_string())
```

### Tích Hợp Nhiều Tiêu Chí

```python
from vnstock import Screener

screener = Screener(source="tcbs")
results = screener.stock(limit=500)

# Tiêu chí tổng hợp
candidates = results[
    (results['pe'].notna()) &
    (results['pe'] > 0) &
    (results['pe'] < 20) &
    (results['roe'] > 10) &
    (results['revenue_growth_1y'] > 0) &
    (results['market_cap'] > 10000)  # > 10 tỷ
].copy()

# Tính điểm
candidates['score'] = (
    (20 - candidates['pe']) / 2 +      # P/E thấp tốt
    candidates['roe'] / 5 +            # ROE cao tốt
    candidates['revenue_growth_1y']    # Doanh thu tăng tốt
)

top_picks = candidates.nlargest(15, 'score')
print("Top gợi ý:")
print(top_picks[[
    'ticker', 'pe', 'roe', 'revenue_growth_1y', 'score'
]].to_string())
```

## 📊 Tiêu Chí Lọc Phổ Biến

### Value Screening

| Tiêu Chí | Ưu Tiên | Phạm Vi |
|---------|--------|--------|
| **P/E** | Thấp | < 15 |
| **P/B** | Thấp | < 2 |
| **Dividend Yield** | Cao | > 3% |
| **ROE** | Cao | > 10% |

### Growth Screening

| Tiêu Chí | Ưu Tiên | Phạm Vi |
|---------|--------|--------|
| **P/E** | Cao | > 20 |
| **EPS Growth** | Cao | > 15% |
| **Revenue Growth** | Cao | > 15% |
| **ROE** | Cao | > 12% |

### Quality Screening

| Tiêu Chí | Ưu Tiên | Phạm Vi |
|---------|--------|--------|
| **ROE** | Cao | > 15% |
| **Net Margin** | Cao | > 10% |
| **EPS Growth (5Y)** | Cao | > 10% |
| **Debt/Equity** | Thấp | < 1 |

## ⚠️ Ghi Chú Quan Trọng

1. **102 Cột**: Screener trả về rất nhiều dữ liệu, cần select các cột cần dùng
2. **Giá trị NaN**: Nhiều cột có thể chứa NaN (không có dữ liệu), cần filter trước sử dụng
3. **Giới hạn kết quả**: Mặc định 50, tối đa tuỳ API
4. **Dữ liệu định kỳ**: Cập nhật sau giờ giao dịch hàng ngày
5. **String vs Float**: Một số cột trạng thái là string (ví dụ: "Giá nằm trên SMA")

## 🔗 Xem Thêm

- **[03-Listing API](03-listing-api.md)** - Tìm kiếm cơ bản
- **[06-Quote Price API](06-quote-price-api.md)** - Lấy dữ liệu giá
- **[08-Best Practices](08-best-practices.md)** - Mẹo tối ưu hóa

---

**Last Updated**: 2024-12-04  
**Version**: 3.3.0  
**Status**: Verified with actual data ✅  
**Cột Dữ Liệu**: 102 tiêu chí tài chính, kỹ thuật, giao dịch
