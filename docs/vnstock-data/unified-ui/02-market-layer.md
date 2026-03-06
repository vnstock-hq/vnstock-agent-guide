# Layer 2: Market Data (Dữ Liệu Giao Dịch Thị Trường)

## 📌 Tổng Quan

**Market Layer** cung cấp dữ liệu **realtime & historical** về giá, khối lượng, vốn hóa, thanh khoản ngay từ các sàn giao dịch và data providers. Đây là dữ liệu **thay đổi liên tục** và phục vụ cho trading, phân tích kỹ thuật, và monitoring portfolio.

## 🏗️ Cấu Trúc Domain

```python
Market()
├── .equity          # Thị trường chứng khoán cổ phiếu
├── .index           # Thị trường chỉ số
├── .fund            # Thị trường quỹ đầu tư
└── .derivatives     # Thị trường chứng chỉ phái sinh
    ├── .futures()   # Thị trường hợp đồng tương lai (nested)
    └── .warrant()   # Thị trường chứng quyền (nested)
```

## 📋 Chi Tiết Các Domain

### 1. Equity Market (Thị Trường Chứng Khoán)

**Primary Source:** KBS (kbs)  
**Fallback:** VCI (vci)  
**Registry Key:** `"market.equity"`

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `ohlcv()` | `symbol`, `start`, `end` | Giá mở/cao/thấp/đóng/khối lượng | DataFrame |
| `trades()` | `symbol`, `start`, `end` | Lệnh giao dịch chi tiết | DataFrame |
| `order_book()` | `symbol` | Cấp độ mua/bán | DataFrame |
| `quote()` | `symbol` (opt) | Giá hiện tại | DataFrame |
| `session_stats()` | - | Thống kê phiên giao dịch | DataFrame |
| `foreign_flow()` | - | Dòng tiền nước ngoài | DataFrame |
| `proprietary_flow()` | - | Dòng tiền tự doanh | DataFrame |
| `block_trades()` | - | Giao dịch khối | DataFrame |
| `odd_lot()` | - | Giao dịch lẻ | DataFrame |
| `volume_profile()` | `symbol` | Phân bố khối lượng theo giá | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Market

mkt = Market()

# ===== OHLCV Data (Giá & Khối lượng) =====
# Lịch sử giá 1 tháng
df_ohlc = mkt.equity.ohlcv(
    "VIC",
    start="2026-02-06",
    end="2026-03-06"
)
print(df_ohlc[['time', 'open', 'high', 'low', 'close', 'volume']])
#             time    open    high     low   close    volume
# 0  2026-02-06  14.50  14.75  14.45  14.65  2500000
# 1  2026-02-09  14.70  14.90  14.60  14.80  3100000

# ===== Intraday Trades (Chi tiết lệnh) =====
# Các lệnh giao dịch trong ngày
df_trades = mkt.equity.trades("TCB")
print(df_trades[['time', 'price', 'volume', 'side']])

# ===== Order Book (Cấp độ mua/bán) =====
# Cấp độ thầu mua/bán
df_orderbook = mkt.equity.order_book("VNM")
print(df_orderbook[['bid_price', 'bid_volume', 'ask_price', 'ask_volume']])

# ===== Quote (Giá Hiện Tại) =====
# Giá realtime
quote_all = mkt.equity.quote()  # Toàn bộ
quote_symbol = mkt.equity.quote("HPG")  # Một síbol

print(quote_all[['code', 'close', 'change_percent', 'volume']])

# ===== Session Stats (Thống kê Phiên) =====
# Thống kê toàn thị trường
session = mkt.equity.session_stats()
print(f"Toàn thị trường - Advance: {session['advance']}, Decline: {session['decline']}")

# ===== Foreign Flow (Dòng Nước Ngoài) =====
# Mua/Bán nước ngoài
foreign = mkt.equity.foreign_flow()
print(foreign[['code', 'foreign_buy', 'foreign_sell', 'foreign_net']])

# ===== Proprietary Flow (Dòng Tự Doanh) =====
# Mua/Bán tự doanh
proprietary = mkt.equity.proprietary_flow()
print(proprietary[['code', 'prop_buy', 'prop_sell']])

# ===== Block Trades (Giao Dịch Khối) =====
# Giao dịch khối trong ngày
blocks = mkt.equity.block_trades()
print(blocks[['code', 'price', 'volume', 'time']])

# ===== Odd Lot (Giao Dịch Lẻ) =====
# Giao dịch lẻ
odd_lots = mkt.equity.odd_lot()
print(odd_lots[['code', 'price', 'quantity']])

# ===== Volume Profile (Phân Bố Khối Lượng) =====
# Khối lượng tích lũy theo giá
vol_profile = mkt.equity.volume_profile("VJC")
print(vol_profile[['price', 'cumulative_volume']])
```

---

### 2. Index Market (Thị Trường Chỉ Số)

**Source:** KBS (kbs)  
**Registry Key:** `"market.index"`

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `ohlcv()` | `index`, `start`, `end` | Điểm chỉ số, cao/thấp | DataFrame |
| `quote()` | `index` (opt) | Điểm chỉ số hiện tại | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Market

mkt = Market()

# Lịch sử điểm VNIndex
df_vnindex = mkt.index.ohlcv(
    "VNINDEX",
    start="2026-01-06",
    end="2026-03-06"
)
print(df_vnindex[['time', 'open', 'high', 'low', 'close']])

# Điểm hiện tại
quote_index = mkt.index.quote("VNINDEX")
print(f"VNIndex: {quote_index['close'].values[0]}")
```

---

### 3. Futures Market (Thị Trường Tương Lai)

**Source:** KBS (kbs)  
**Registry Key:** `"market.futures"`

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `ohlcv()` | `contract`, `start`, `end` | Giá hợp đồng | DataFrame |
| `quote()` | `contract` | Giá hiện tại | DataFrame |
| `trades()` | `contract` | Giao dịch chi tiết | DataFrame |
| `order_book()` | `contract` | Cấp độ mua/bán | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Market

mkt = Market()

# Lịch sử VN30F (VNIndex Futures) - nested under derivatives
df_vn30f = mkt.derivatives().futures("VN30F").ohlcv(
    start="2026-02-06",
    end="2026-03-06"
)
print(df_vn30f)

# Giá hiện tại
quote_vn30f = mkt.derivatives().futures("VN30F").quote()
```

---

### 4. Warrant Market (Thị Trường Chứng Quyền)

**Source:** KBS (kbs)  
**Registry Key:** `"market.warrant"`

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `ohlcv()` | `warrant`, `start`, `end` | Giá chứng quyền | DataFrame |
| `quote()` | `warrant` | Giá hiện tại | DataFrame |
| `trades()` | `warrant` | Giao dịch chi tiết | DataFrame |
| `order_book()` | `warrant` | Cấp độ mua/bán | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Market

mkt = Market()

# Lịch sử giá warrant - nested under derivatives
df_warrant = mkt.derivatives().warrant("VICW-VIC26A").ohlcv(
    start="2026-02-06",
    end="2026-03-06"
)
print(df_warrant)

# Giá hiện tại warrant
quote = mkt.derivatives().warrant("VICW-VIC26A").quote()
```

---

### 5. Fund Market (Thị Trường Quỹ)

**Source:** FMarket (fmarket)  
**Registry Key:** `"market.fund"`

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `history()` | `fund_code` | Lịch sử NAV | DataFrame |
| `top_holding()` | `fund_code` | Top ứng cử viên | DataFrame |
| `industry_holding()` | `fund_code` | Nắm giữ theo ngành | DataFrame |
| `asset_holding()` | `fund_code` | Nắm giữ theo loại tài sản | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Market

mkt = Market()

# Lịch sử NAV quỹ
df_nav = mkt.fund.history("VFIBS")
print(df_nav[['date', 'nav', 'nav_change']])

# Top ứng cử viên trong quỹ
top_holding = mkt.fund.top_holding("VFIBS")
print(top_holding[['symbol', 'price', 'weight']])

# Nắm giữ theo ngành
industry = mkt.fund.industry_holding("VFIBS")
print(industry[['industry', 'percentage']])
```

---

### 6. Market Wide (Thị Trường Rộng)

**Source:** KBS (kbs)  
**Registry Key:** `"market.market_wide"`

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `quote()` | - | Tất cả giá thị trường | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Market

mkt = Market()

# Toàn bộ giá thị trường
all_quotes = mkt.market_wide.quote()
print(all_quotes.head())
```

---

## 🔗 Registry Mapping

```python
MARKET_SOURCES = {
    "market.equity": {
        "ohlcv": ("kbs", "quote", "Quote", "history"),
        "trades": ("kbs", "quote", "Quote", "intraday"),
        "order_book": ("kbs", "quote", "Quote", "price_depth"),
        "quote": ("kbs", "trading", "Trading", "price_board"),
        "session_stats": ("vci", "trading", "Trading", "summary"),
        "foreign_flow": ("vci", "trading", "Trading", "foreign_trade"),
        "proprietary_flow": ("vci", "trading", "Trading", "prop_trade"),
        "block_trades": ("kbs", "trading", "Trading", "put_through"),
        "odd_lot": ("kbs", "trading", "Trading", "odd_lot"),
        "volume_profile": ("kbs", "trading", "Trading", "matched_by_price"),
    },
    "market.index": {
        "ohlcv": ("kbs", "quote", "Quote", "history"),
        "quote": ("kbs", "trading", "Trading", "price_board"),
    },
    # ... more domains
}
```

---

## 💡 Best Practices

### 1. Batch Requests (Tối Ưu Hóa)

```python
# ❌ Không tối ưu - gọi 100 lần
mkt = Market()
for symbol in symbols:
    quote = mkt.equity.quote(symbol)

# ✅ Tốt - gọi 1 lần
all_quotes = mkt.equity.quote()
symbol_quotes = all_quotes[all_quotes['code'].isin(symbols)]
```

### 2. Caching Data

```python
import time
from functools import lru_cache

mkt = Market()

# Cache giá hiện tại 5 phút
@lru_cache(maxsize=128)
def get_quote_cached(symbol):
    return mkt.equity.quote(symbol)

# Lần đầu gọi API, lần sau dùng cache
quote1 = get_quote_cached("VIC")
quote2 = get_quote_cached("VIC")  # Từ cache (nhanh hơn)
```

### 3. Error Handling

```python
from pandas.errors import EmptyDataError

mkt = Market()

try:
    df = mkt.equity.ohlcv("INVALID", start="2026-02-01", end="2026-02-28")
except ValueError as e:
    print(f"Symbol không tồn tại: {e}")
except EmptyDataError:
    print("Không có dữ liệu trong khoảng ngày này")
except Exception as e:
    print(f"Lỗi: {e}")
```

---

## ⚠️ Lưu Ý Quan Trọng

1. **Realtime vs Historical**: Dữ liệu intraday có thể bị delay 15-30 phút tùy provider
2. **Market Hours**: Dữ liệu chỉ cập nhật trong giờ giao dịch (9h-15h)
3. **Holidays**: Không có dữ liệu vào các ngày nghỉ lễ
4. **Rate Limiting**: Một số API có giới hạn request → nên batch hoặc cache

---

## 🚦 Next Steps

- **Fundamental Layer**: Để phân tích các chỉ số tài chính
- **Insights Layer**: Để xem khuyến nghị, xếp hạng
- **Macro Layer**: Để xem dữ liệu kinh tế toàn cảnh
