# Layer 2: Market Data (Dữ Liệu Giao Dịch Thị Trường)

> [!IMPORTANT]
> **Data Schema (Từ điển dữ liệu):** Để xem chính xác tên cột, kiểu dữ liệu (`Dtype`) và ý nghĩa (`Meaning`) của các DataFrame trả về từ layer này, vui lòng tham khảo [Data Schema](schema/02-market.md). KHÔNG được đoán mò tên cột khi viết code xử lý dữ liệu.

## 📌 Tổng Quan

**Market Layer** cung cấp dữ liệu **realtime & historical** về giá, khối lượng, vốn hóa, thanh khoản ngay từ các sàn giao dịch và data providers. Đây là dữ liệu **thay đổi liên tục** và phục vụ cho trading, phân tích kỹ thuật, và monitoring portfolio.

## 🏗️ Cấu Trúc Domain

```python
Market()
├── .equity(symbol)        # Thị trường cổ phiếu
├── .index(symbol)         # Thị trường chỉ số
├── .futures(symbol)       # Thị trường hợp đồng tương lai
├── .warrant(symbol)       # Thị trường chứng quyền
├── .bond(symbol)          # Thị trường trái phiếu
├── .etf(symbol)           # Thị trường ETF
├── .fund(symbol)          # Thị trường quỹ đầu tư mở
├── .crypto(symbol)        # Tiền mã hoá
├── .forex(symbol)         # Ngoại hối
├── .commodity(symbol)     # Hàng hoá quốc tế
└── .quote(symbols_list)   # Bảng giá nhiều mã
```

## ⚙️ Cấu Trúc Tham Số (Parameters)

Đa số các phương thức trong Market Layer đều tuân theo hệ thống tham số chuẩn hóa:

### 1. Dữ liệu Lịch sử (Historical Data)
Các hàm lấy chuỗi thời gian như `ohlcv()`, `trade_history()`, `foreign_flow()`, `proprietary_flow()`... hỗ trợ:
- `start` (`str`): Ngày bắt đầu lấy dữ liệu (VD: `"2024-01-01"`).
- `end` (`str`): Ngày kết thúc (VD: `"2024-12-31"`). Nếu bỏ trống sẽ lấy đến hiện tại.
- `interval` (`str`, tuỳ chọn): Độ phân giải dữ liệu. Các giá trị hợp lệ:
  - Khung ngày/tuần/tháng: `'1D'`, `'1W'`, `'1M'` (Mặc định thường là `'1D'`).
  - Khung phút (Intraday): `'1m'`, `'5m'`, `'15m'`, `'1H'` (Chỉ khả dụng với tài khoản Premium/Pro tuỳ nguồn cung cấp).
- `length` (`int` | `str`, tuỳ chọn): Số lượng nến/kỳ cần lấy ngược về quá khứ tính từ `end`. Có thể dùng thay cho `start` (VD: `100` nến, hoặc chuỗi thời gian như `"30D"`, `"1Y"`).

### 2. Dữ liệu Chi tiết Giao dịch (Intraday / Trades)
Các hàm lấy thông tin từng lệnh (Time & Sales) như `trades()`, `block_trades()`... hỗ trợ:
- `limit` (`int`): Giới hạn số lượng lệnh trả về trên mỗi trang. Mặc định `1000`.
- `page` (`int`): Số thứ tự trang cần truy xuất. Mặc định `1`.
- `get_all` (`bool`): Nếu `True`, API sẽ tự động quét qua tất cả các trang để lấy toàn bộ dữ liệu lịch sử lệnh (cẩn trọng với mã thanh khoản lớn). Mặc định `False`.

### 3. Dữ liệu Tức thời & Thống kê (Snapshot / Stats)
Các hàm truy xuất trạng thái hiện tại như `quote()`, `order_book()`, `session_stats()`, `summary()`, `volume_profile()`, `odd_lot()`:
- Hầu hết **không yêu cầu truyền tham số** thời gian. Dữ liệu trả về mặc định là snapshot tại thời điểm truy vấn hoặc thống kê tổng hợp của ngày giao dịch hiện hành.

---

## 📋 Chi Tiết Các Domain

### 1. Equity Market (Thị Trường Cổ Phiếu)

**Nguồn chính:** KBS (kbs), VCI (vci)  
**Registry Key:** `"market.equity"`

#### Phương Thức

| Method | Mô Tả | Return |
|--------|------|--------|
| `ohlcv()` | Giá OHLCV lịch sử | DataFrame |
| `trade_history()` | Lịch sử thống kê giao dịch (giá, khối lượng, giá trị) | DataFrame |
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

#### 📝 Chi Tiết Các Phương Thức

**1. Lịch sử Giá (`ohlcv`)**
- **Mục đích:** Lấy dữ liệu giá mở, cao, thấp, đóng và khối lượng theo chuỗi thời gian để vẽ biểu đồ kỹ thuật.
```python
from vnstock_data import Market
mkt = Market()

df_ohlc = mkt.equity("VIC").ohlcv(
    start="2026-02-01", 
    end="2026-03-01",
    interval="1D"
)
```

**2. Thống kê Giao dịch Lịch sử (`trade_history`)**
- **Mục đích:** Cung cấp dữ liệu thống kê tổng hợp cuối ngày về giá trị, khối lượng khớp lệnh và thỏa thuận.
```python
history_stats = mkt.equity("VIC").trade_history(
    start="2026-02-01", 
    end="2026-03-01"
)
```

**3. Khớp Lệnh Intraday (`trades`)**
- **Mục đích:** Truy xuất danh sách các lệnh khớp chi tiết trong phiên (Time & Sales) để phân tích hành vi dòng tiền.
```python
df_trades = mkt.equity("TCB").trades(limit=100)
```

**4. Sổ Lệnh (`order_book`)**
- **Mục đích:** Xem thông tin các mức giá chờ mua/bán tốt nhất trên sổ lệnh (thường là 3-10 mức).
```python
df_orderbook = mkt.equity("VNM").order_book()
```

**5. Bảng Giá (`quote`)**
- **Mục đích:** Lấy trạng thái giá và các chỉ số giao dịch realtime mới nhất, snapshot tức thời.
```python
quote = mkt.equity("HPG").quote()
```

**6. Thống kê Phiên (`session_stats`)**
- **Mục đích:** Tổng hợp các chỉ số thanh khoản, trung bình lệnh, tỷ lệ mua/bán chủ động trong ngày.
```python
session = mkt.equity("VIC").session_stats()
```

**7. Tổng Hợp Cổ Phiếu (`summary`)**
- **Mục đích:** Các chỉ số định giá cơ bản (PE, PB), biên độ 52 tuần, số lượng cổ phiếu lưu hành, vốn hoá.
```python
summary_info = mkt.equity("VIC").summary()
```

**8. Dòng Tiền Nước Ngoài (`foreign_flow`)**
- **Mục đích:** Lịch sử thống kê khối lượng và giá trị mua/bán ròng của nhà đầu tư nước ngoài.
```python
foreign = mkt.equity("VIC").foreign_flow()
```

**9. Dòng Tiền Tự Doanh (`proprietary_flow`)**
- **Mục đích:** Lịch sử thống kê giao dịch của khối Tự doanh các Công ty Chứng khoán.
```python
proprietary = mkt.equity("VIC").proprietary_flow()
```

**10. Giao Dịch Thỏa Thuận (`block_trades`)**
- **Mục đích:** Thông tin các lệnh thỏa thuận khối lượng lớn được thực hiện ngoài sàn khớp lệnh liên tục.
```python
blocks = mkt.equity("VIC").block_trades(limit=50)
```

**11. Giao Dịch Lô Lẻ (`odd_lot`)**
- **Mục đích:** Thông tin các lệnh giao dịch có khối lượng dưới tiêu chuẩn lô chẵn (thường < 100 cổ phiếu).
```python
odds = mkt.equity("VIC").odd_lot()
```

**12. Phân Bố Khối Lượng (`volume_profile`)**
- **Mục đích:** Tổng hợp khối lượng giao dịch đã khớp tại từng mức giá cụ thể trong phiên.
```python
vol_profile = mkt.equity("VJC").volume_profile()
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

#### 📝 Chi Tiết Các Phương Thức

**1. Điểm Chỉ Số Lịch Sử (`ohlcv`)**
- **Mục đích:** Lấy lịch sử biến động điểm số (mở, cao, thấp, đóng) của Index theo thời gian.
```python
from vnstock_data import Market
mkt = Market()

df_vnindex = mkt.index("VNINDEX").ohlcv(
    start="2026-01-01",
    end="2026-03-01"
)
```

**2. Điểm Hiện Tại (`quote`)**
- **Mục đích:** Truy xuất điểm số realtime hoặc điểm chốt phiên gần nhất của chỉ số.
```python
quote_index = mkt.index("VNINDEX").quote()
```

**3. Tổng Hợp Chỉ Số (`summary`)**
- **Mục đích:** Thống kê tổng quan trạng thái chỉ số (khối lượng, giá trị giao dịch toàn rổ, số mã tăng/giảm).
```python
summary_index = mkt.index("VNINDEX").summary()
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

#### 📝 Chi Tiết Các Phương Thức

**1. Lịch sử Hợp đồng (`ohlcv`)**
- **Mục đích:** Lấy dữ liệu nến lịch sử của hợp đồng phái sinh.
```python
from vnstock_data import Market
mkt = Market()

df_vn30f = mkt.futures("VN30F2503").ohlcv(
    start="2026-02-01",
    end="2026-03-01"
)
```

**2. Giá Hiện Tại (`quote`)**
- **Mục đích:** Lấy giá khớp gần nhất, khối lượng mở (OI) và độ lệch (Basis) của hợp đồng realtime.
```python
quote_vn30f = mkt.futures("VN30F2503").quote()
```

**3. Khớp Lệnh Intraday (`trades`)**
- **Mục đích:** Danh sách chi tiết các lệnh khớp phái sinh trong phiên.
```python
trades_vn30f = mkt.futures("VN30F2503").trades(limit=100)
```

**4. Sổ Lệnh (`order_book`)**
- **Mục đích:** Bảng giá các mức chờ mua/bán tốt nhất của hợp đồng.
```python
orderbook_vn30f = mkt.futures("VN30F2503").order_book()
```

**5. Thông tin Hợp đồng (`summary`)**
- **Mục đích:** Cung cấp thông tin tổng quan, ngày đáo hạn, số lượng hợp đồng mở (OI).
```python
summary_vn30f = mkt.futures("VN30F2503").summary()
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

#### 📝 Chi Tiết Các Phương Thức

**1. Lịch sử Giá Chứng Quyền (`ohlcv`)**
- **Mục đích:** Lấy dữ liệu nến lịch sử của mã chứng quyền.
```python
from vnstock_data import Market
mkt = Market()

df_warrant = mkt.warrant("CACB2511").ohlcv(
    start="2026-02-01",
    end="2026-03-01"
)
```

**2. Giá Hiện Tại (`quote`)**
- **Mục đích:** Lấy thông tin giá khớp lệnh hiện tại và các thông số thanh khoản của chứng quyền.
```python
quote_warrant = mkt.warrant("CACB2511").quote()
```

**3. Khớp Lệnh Intraday (`trades`)**
- **Mục đích:** Truy xuất danh sách các lệnh khớp chi tiết trong phiên của chứng quyền.
```python
trades_warrant = mkt.warrant("CACB2511").trades(limit=100)
```

**4. Sổ Lệnh (`order_book`)**
- **Mục đích:** Xem thông tin các mức giá chờ mua/bán tốt nhất.
```python
orderbook_warrant = mkt.warrant("CACB2511").order_book()
```

**5. Tổng hợp Chứng Quyền (`summary`)**
- **Mục đích:** Các chỉ số cơ bản của chứng quyền (ngày đáo hạn, tỷ lệ chuyển đổi, giá thực hiện, tổ chức phát hành).
```python
summary_warrant = mkt.warrant("CACB2511").summary()
```

---

### 5. Bond Market (Thị Trường Trái Phiếu)

**Nguồn:** KBS (kbs)  
**Registry Key:** `"market.bond"`

#### Phương Thức

| Method | Mô Tả | Return |
|--------|------|--------|
| `ohlcv()` | Giá trái phiếu lịch sử | DataFrame |
| `quote()` | Giá hiện tại | DataFrame |
| `trades()` | Giao dịch chi tiết | DataFrame |
| `order_book()` | Cấp độ mua/bán | DataFrame |
| `summary()` | Thông tin trái phiếu | DataFrame |

#### 📝 Chi Tiết Các Phương Thức

**1. Lịch sử Giá Trái Phiếu (`ohlcv`)**
- **Mục đích:** Lấy dữ liệu biến động giá trị giao dịch trái phiếu lịch sử.
```python
from vnstock_data import Market
mkt = Market()

df_bond = mkt.bond("TD2444161").ohlcv(
    start="2026-02-01",
    end="2026-03-01"
)
```

**2. Giá Hiện Tại (`quote`)**
- **Mục đích:** Trạng thái giá khớp và thanh khoản realtime của trái phiếu.
```python
quote_bond = mkt.bond("TD2444161").quote()
```

*(Các phương thức khác như `trades()`, `order_book()`, `summary()` được sử dụng hoàn toàn tương tự như `Equity Market`)*

---

### 6. ETF Market (Thị Trường ETF)

**Nguồn:** KBS (kbs), VCI (vci)  
**Registry Key:** `"market.etf"`

#### Phương Thức

Giống Equity Market (đầy đủ): `ohlcv()`, `trades()`, `order_book()`, `quote()`, `session_stats()`, `foreign_flow()`, `proprietary_flow()`, `block_trades()`, `odd_lot()`, `volume_profile()`, `summary()`.

#### 📝 Chi Tiết Các Phương Thức

**1. Lịch sử Giá ETF (`ohlcv`)**
- **Mục đích:** Lấy dữ liệu giá trị của chứng chỉ quỹ ETF trên sàn theo thời gian.
```python
from vnstock_data import Market
mkt = Market()

df_etf = mkt.etf("E1VFVN30").ohlcv(
    start="2026-02-01",
    end="2026-03-01"
)
```

**2. Giá Hiện Tại (`quote`)**
- **Mục đích:** Trạng thái giá khớp và thanh khoản realtime của ETF.
```python
quote_etf = mkt.etf("E1VFVN30").quote()
```

*(Các phương thức khác như `trades()`, `order_book()`, `summary()`, `session_stats()`, v.v. được sử dụng hoàn toàn tương tự như `Equity Market`)*

---

### 7. Fund Market (Thị Trường Quỹ Đầu Tư Mở)

**Nguồn:** FMarket (fmarket)  
**Registry Key:** `"market.fund"`

#### Phương Thức

| Method | Mô Tả | Return |
|--------|------|--------|
| `history()` | Lịch sử NAV quỹ | DataFrame |
| `top_holding()` | Top cổ phiếu nắm giữ | DataFrame |
| `industry_holding()` | Nắm giữ theo ngành | DataFrame |
| `asset_holding()` | Nắm giữ theo loại tài sản | DataFrame |

#### 📝 Chi Tiết Các Phương Thức

**1. Lịch sử NAV Quỹ (`history`)**
- **Mục đích:** Lấy chuỗi dữ liệu lịch sử giá trị tài sản ròng (NAV) của quỹ để đánh giá hiệu suất.
- **Tham số:** `limit` (`int`): Số lượng bản ghi giới hạn.
```python
from vnstock_data import Market
mkt = Market()

df_nav = mkt.fund("VFIBS").history(limit=100)
```

**2. Top Cổ Phiếu Nắm Giữ (`top_holding`)**
- **Mục đích:** Liệt kê các cổ phiếu có tỷ trọng lớn nhất trong danh mục đầu tư của quỹ.
- **Tham số:** `limit` (`int`): Số lượng cổ phiếu tối đa hiển thị (thường 10-20 mã).
```python
top_holding = mkt.fund("VFIBS").top_holding()
```

**3. Nắm Giữ Theo Ngành (`industry_holding`)**
- **Mục đích:** Xem tỷ trọng phân bổ vốn của quỹ vào các lĩnh vực kinh tế (Bất động sản, Ngân hàng, Bán lẻ...).
```python
industry = mkt.fund("VFIBS").industry_holding()
```

**4. Nắm Giữ Theo Loại Tài Sản (`asset_holding`)**
- **Mục đích:** Xem tỷ trọng phân bổ tài sản (Cổ phiếu, Trái phiếu, Tiền mặt).
```python
asset = mkt.fund("VFIBS").asset_holding()
```

---

### 8. Market Wide (Bảng Giá Nhiều Mã)

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

### 9. Thị Trường Quốc Tế (International Market)

#### Crypto Market (Thị Trường Tiền Mã Hóa)

**Nguồn chính:** Binance (Spot Trading API)  
**Registry Key:** `"market.crypto"`

Dữ liệu Crypto Market được liên kết trực tiếp từ **Binance Spot API**. Hỗ trợ truy xuất OHLCV theo khung thời gian (interval) tuỳ chỉnh, Orderbook Horizontal chuẩn hoá đa cấp độ (L1-L10), lịch sử giao dịch (Intraday Trades với cơ chế map Taker/Maker) và báo giá tổng hợp 24h.

| Method | Mô Tả | Return |
|--------|------|--------|
| `ohlcv()` | Giá lịch sử Klines đa khung thời gian (1m, 1h, 1d) | DataFrame |
| `quote()` | Báo giá ticker lũy kế 24 giờ dạng Snapshot | DataFrame |
| `intraday()` | Khớp lệnh chi tiết gần nhất (Time & Sales) | DataFrame |
| `order_book()` | Sổ lệnh L1 - L10 (được dàn đều theo chiều ngang) | DataFrame |
| `trade_history()` | Truy vấn lịch sử giao dịch bằng ID lệnh cũ (`/historicalTrades`) | DataFrame |
| `vwap()` | Giá trung bình theo khối lượng (`/avgPrice`) | DataFrame |
| `daily_stats()` | Thống kê phiên giao dịch (`/ticker/tradingDay`) | DataFrame |
| `last_price()` | Mức giá khớp lệnh cuối cùng (`/ticker/price`) | DataFrame |
| `rolling_stats()` | Thống kê theo cửa sổ trượt (Rolling Window Ticker) | DataFrame |
| `reference_price(mode)` | Giá tham chiếu (`price`) hoặc cấu trúc tính toán (`calc`) | DataFrame |

#### Ví dụ Truy xuất Crypto
```python
from vnstock_data import Market

mkt = Market()
crypto = mkt.crypto("BTCUSDT")

# Báo giá Ticker hiện tại (24HR Rolling)
df_quote = crypto.quote()

# Dữ liệu OHLCV (ví dụ khung 1 ngày)
df_ohlcv = crypto.ohlcv(interval="1d", limit=500)

# Sổ lệnh (Order Book 10 mức giá Mua/Bán)
df_orderbook = crypto.order_book(limit=10)

# Lịch sử khớp lệnh trong phiên (Intraday)
df_trades = crypto.intraday()

# Trích xuất VWAP
df_vwap = crypto.vwap()
```

#### Forex, Commodity & Global Index (Thị Trường Cầu & Hàng hóa)

**Nguồn chính:** Dukascopy  
**Registry Key:** `"market.forex"`, `"market.commodity"`, `"market.index"`

Các domain Forex, Commodity, Index (Chỉ số Quốc Tế) giờ đây được hợp nhất kiến trúc và trực tiếp truy xuất Data **Tick/Phút liên tục** thông qua `Dukascopy`. Hệ thống còn cho phép cơ chế *Resampling* nội bộ đối với các khung cao (1h, 4h, 1d...).

| Method | Tham Số Chính | Mô Tả | Return |
|--------|---------------|------|--------|
| `ohlcv()` | `interval`, `length`, `timezone` | Lịch sử giá theo khoảng thời gian tuỳ chọn | DataFrame |
| `intraday()`| `timezone` | Dữ liệu Tick (Khớp lệnh) | DataFrame |

> **🌟 Tính năng Timezone Configuration Parameter**:  
> Lịch sử giá Dukascopy và Quốc tế mặc định được tự động map về quy chuẩn giờ Hệ thống Việt Nam (`Asia/Ho_Chi_Minh` / GMT+7). Tuy nhiên, có thể tuỳ ý ghi đè múi giờ gốc (UTC) hoặc bất kỳ giờ khu vực nào qua tham số `timezone`.

#### Ví Dụ
```python
mkt = Market()

# Lịch sử tỷ giá tiền tệ theo giờ nội địa VN
df_eurusd = mkt.forex("EURUSD").ohlcv(interval="1h", length=15)

# Định dạng nến trả về đúng múi giờ quốc tế gốc UTC!
df_utc_eurusd = mkt.forex("EURUSD", timezone="UTC").ohlcv(interval="1h", length=15)

# Lịch sử giá vàng
df_gold = mkt.commodity("XAUUSD").ohlcv(interval="1d", length=5)

# Lấy dữ liệu Chỉ Số chứng khoán Mỹ (Dow Jones USA30) qua tham số scope="global"
df_djia = mkt.index("USA30", scope="global").ohlcv(interval="4h")
```

> **Tip**: Có thể dùng `Reference().search.symbol("tên_tài_sản")` để tìm mã Symbol nếu không chắc chắn.

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
