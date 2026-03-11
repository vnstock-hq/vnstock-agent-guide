# Layer 2: Market Data (Dữ Liệu Giao Dịch Thị Trường)

## 📌 Tổng Quan

**Market Layer** cung cấp dữ liệu **realtime & historical** về giá, khối lượng, vốn hóa, thanh khoản ngay từ các sàn giao dịch và data providers. Đây là dữ liệu **thay đổi liên tục** và phục vụ cho trading, phân tích kỹ thuật, và monitoring portfolio.

## 🏗️ Cấu Trúc Domain

```python
Market()
├── .equity(symbol)        # Thị trường cổ phiếu
├── .index(symbol)         # Thị trường chỉ số
├── .futures(symbol)       # Thị trường hợp đồng tương lai
├── .warrant(symbol)       # Thị trường chứng quyền
├── .etf(symbol)           # Thị trường ETF
├── .fund(symbol)          # Thị trường quỹ đầu tư mở
├── .crypto(symbol)        # 🧪 Tiền mã hoá (experimental)
├── .forex(symbol)         # 🧪 Ngoại hối (experimental)
├── .commodity(symbol)     # 🧪 Hàng hoá quốc tế (experimental)
└── .quote(symbols_list)   # Bảng giá nhiều mã
```

## 📋 Chi Tiết Các Domain

### 1. Equity Market (Thị Trường Cổ Phiếu)

**Nguồn chính:** KBS (kbs), VCI (vci)  
**Registry Key:** `"market.equity"`

#### Phương Thức

| Method | Mô Tả | Return |
|--------|------|--------|
| `ohlcv()` | Giá OHLCV lịch sử | DataFrame |
| `trades()` | Lệnh giao dịch chi tiết (Time & Sales) | DataFrame |
| `order_book()` | Cấp độ mua/bán | DataFrame |
| `quote()` | Giá hiện tại / Bảng giá | DataFrame |
| `session_stats()` | Thống kê phiên giao dịch | DataFrame |
| `foreign_flow()` | Dòng tiền nước ngoài | DataFrame |
| `proprietary_flow()` | Dòng tiền tự doanh | DataFrame |
| `block_trades()` | Giao dịch thỏa thuận | DataFrame |
| `odd_lot()` | Giao dịch lô lẻ | DataFrame |
| `volume_profile()` | Phân bố khối lượng theo giá | DataFrame |
| `summary()` | Tổng hợp thông tin cổ phiếu | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Market

mkt = Market()

# ===== OHLCV Data (Giá & Khối lượng) =====
df_ohlc = mkt.equity("VIC").ohlcv(
    start="2026-02-01",
    end="2026-03-01"
)
print(df_ohlc)
# Columns: ['time', 'open', 'high', 'low', 'close', 'volume']

# ===== Intraday Trades (Chi tiết lệnh) =====
df_trades = mkt.equity("TCB").trades()
print(df_trades)

# ===== Order Book (Cấp độ mua/bán) =====
df_orderbook = mkt.equity("VNM").order_book()
print(df_orderbook)

# ===== Quote (Bảng giá) =====
quote = mkt.equity("HPG").quote()
print(quote)

# ===== Dòng tiền Nước ngoài =====
foreign = mkt.equity("VIC").foreign_flow()
print(foreign)

# ===== Dòng tiền Tự doanh =====
proprietary = mkt.equity("VIC").proprietary_flow()
print(proprietary)

# ===== Giao dịch Thỏa thuận =====
blocks = mkt.equity("VIC").block_trades()
print(blocks)

# ===== Volume Profile =====
vol_profile = mkt.equity("VJC").volume_profile()
print(vol_profile)
```

---

### 2. Index Market (Thị Trường Chỉ Số)

**Nguồn:** KBS (kbs)  
**Registry Key:** `"market.index"`

#### Phương Thức

| Method | Mô Tả | Return |
|--------|------|--------|
| `ohlcv()` | Điểm chỉ số lịch sử | DataFrame |
| `quote()` | Điểm chỉ số hiện tại | DataFrame |
| `summary()` | Tổng hợp chỉ số | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Market

mkt = Market()

# Lịch sử điểm VNIndex
df_vnindex = mkt.index("VNINDEX").ohlcv(
    start="2026-01-01",
    end="2026-03-01"
)
print(df_vnindex)
# Columns: ['time', 'open', 'high', 'low', 'close', 'volume']

# Điểm hiện tại
quote_index = mkt.index("VNINDEX").quote()
print(quote_index)
```

---

### 3. Futures Market (Thị Trường Hợp Đồng Tương Lai)

**Nguồn:** KBS (kbs)  
**Registry Key:** `"market.futures"`

#### Phương Thức

| Method | Mô Tả | Return |
|--------|------|--------|
| `ohlcv()` | Giá hợp đồng lịch sử | DataFrame |
| `quote()` | Giá hiện tại | DataFrame |
| `trades()` | Giao dịch chi tiết | DataFrame |
| `order_book()` | Cấp độ mua/bán | DataFrame |
| `summary()` | Thông tin hợp đồng | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Market

mkt = Market()

# Lịch sử VN30F (truy cập trực tiếp, KHÔNG qua derivatives)
df_vn30f = mkt.futures("VN30F2503").ohlcv(
    start="2026-02-01",
    end="2026-03-01"
)
print(df_vn30f)

# Giá hiện tại
quote_vn30f = mkt.futures("VN30F2503").quote()
print(quote_vn30f)
```

---

### 4. Warrant Market (Thị Trường Chứng Quyền)

**Nguồn:** KBS (kbs)  
**Registry Key:** `"market.warrant"`

#### Phương Thức

| Method | Mô Tả | Return |
|--------|------|--------|
| `ohlcv()` | Giá chứng quyền lịch sử | DataFrame |
| `quote()` | Giá hiện tại | DataFrame |
| `trades()` | Giao dịch chi tiết | DataFrame |
| `order_book()` | Cấp độ mua/bán | DataFrame |
| `summary()` | Thông tin chứng quyền | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Market

mkt = Market()

# Lịch sử giá warrant (truy cập trực tiếp)
df_warrant = mkt.warrant("CACB2511").ohlcv(
    start="2026-02-01",
    end="2026-03-01"
)
print(df_warrant)

# Giá hiện tại warrant
quote = mkt.warrant("CACB2511").quote()
print(quote)
```

---

### 5. ETF Market (Thị Trường ETF)

**Nguồn:** KBS (kbs), VCI (vci)  
**Registry Key:** `"market.etf"`

#### Phương Thức

Giống Equity Market (đầy đủ): `ohlcv()`, `trades()`, `order_book()`, `quote()`, `session_stats()`, `foreign_flow()`, `proprietary_flow()`, `block_trades()`, `odd_lot()`, `volume_profile()`, `summary()`.

#### Ví Dụ

```python
from vnstock_data import Market

mkt = Market()

# Lịch sử giá ETF
df_etf = mkt.etf("E1VFVN30").ohlcv(
    start="2026-02-01",
    end="2026-03-01"
)
print(df_etf)

# Giá hiện tại
quote_etf = mkt.etf("E1VFVN30").quote()
print(quote_etf)
```

---

### 6. Fund Market (Thị Trường Quỹ Đầu Tư Mở)

**Nguồn:** FMarket (fmarket)  
**Registry Key:** `"market.fund"`

#### Phương Thức

| Method | Mô Tả | Return |
|--------|------|--------|
| `history()` | Lịch sử NAV quỹ | DataFrame |
| `top_holding()` | Top cổ phiếu nắm giữ | DataFrame |
| `industry_holding()` | Nắm giữ theo ngành | DataFrame |
| `asset_holding()` | Nắm giữ theo loại tài sản | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Market

mkt = Market()

# Lịch sử NAV quỹ
df_nav = mkt.fund("VFIBS").history()
print(df_nav)

# Top cổ phiếu trong quỹ
top_holding = mkt.fund("VFIBS").top_holding()
print(top_holding)

# Nắm giữ theo ngành
industry = mkt.fund("VFIBS").industry_holding()
print(industry)
```

---

### 7. Market Wide (Bảng Giá Nhiều Mã)

**Nguồn:** KBS (kbs)

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|------|--------|
| `quote()` | `symbols_list` | Giá nhiều mã cùng lúc | DataFrame |

#### Ví Dụ

```python
from vnstock_data import Market

mkt = Market()

# Bảng giá nhiều mã cùng lúc
df_quotes = mkt.quote(["VIC", "TCB", "HPG", "VNM"])
print(df_quotes)
```

---

### 8. 🧪 Thị Trường Quốc Tế (Experimental)

> **Lưu ý**: Các domain sau đang trong giai đoạn thử nghiệm và có thể chưa ổn định. Chỉ hỗ trợ method `ohlcv()` cho dữ liệu lịch sử thông qua nguồn MSN.

#### Crypto Market

```python
mkt = Market()
# Dữ liệu lịch sử Bitcoin (cần symbol_id từ MSN)
df = mkt.crypto("BTC").ohlcv(start="2026-01-01", end="2026-03-01")
```

#### Forex Market

```python
mkt = Market()
# Dữ liệu lịch sử cặp tiền tệ
df = mkt.forex("USDVND").ohlcv(start="2026-01-01", end="2026-03-01")
```

#### Commodity Market

```python
mkt = Market()
# Dữ liệu lịch sử hàng hóa
df = mkt.commodity("GC=F").ohlcv(start="2026-01-01", end="2026-03-01")
```

> **Tip**: Dùng `Reference().search.symbol("tên_tài_sản")` để tìm đúng mã symbol cho các thị trường quốc tế.

---

## 💡 Best Practices

### 1. Gọi nhiều mã cùng lúc

```python
# ❌ Không tối ưu - gọi 100 lần
mkt = Market()
for symbol in symbols:
    quote = mkt.equity(symbol).quote()

# ✅ Tốt - gọi 1 lần
all_quotes = mkt.quote(symbols)
```

### 2. Xử lý lỗi

```python
mkt = Market()

try:
    df = mkt.equity("INVALID").ohlcv(start="2026-02-01", end="2026-02-28")
except ValueError as e:
    print(f"Symbol không tồn tại: {e}")
except Exception as e:
    print(f"Lỗi: {e}")
```

### 3. Tra cứu tính năng khả dụng

```python
from vnstock_data import show_api, Market

# Xem tất cả methods trong Market layer
show_api(Market())
```

---

## ⚠️ Lưu Ý Quan Trọng

1. **Realtime vs Historical**: Dữ liệu intraday có thể bị delay 15-30 phút tùy provider
2. **Giờ giao dịch**: Dữ liệu chỉ cập nhật trong giờ giao dịch (9h-15h)
3. **Ngày nghỉ**: Không có dữ liệu vào các ngày nghỉ lễ
4. **Giới hạn tần suất**: Một số nguồn có giới hạn số lượng yêu cầu → nên gọi nhiều mã cùng lúc hoặc lưu tạm
5. **Deprecated `derivatives()`**: Dùng `mkt.futures(symbol)` / `mkt.warrant(symbol)` trực tiếp
6. **Deprecated `pe()`/`pb()`**: Đã chuyển sang `Analytics().valuation(index).pe()/.pb()`

---

## 🚦 Next Steps

- **Fundamental Layer**: Để phân tích các chỉ số tài chính
- **Analytics Layer**: Để định giá thị trường (P/E, P/B)
- **Insights Layer**: Để xem xếp hạng và lọc cổ phiếu
- **Macro Layer**: Để xem dữ liệu kinh tế toàn cảnh
