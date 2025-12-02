# Vnstock TA - Thư Viện Phân Tích Kỹ Thuật

## 📚 Tài Liệu Tham Khảo Toàn Diện

Chào mừng đến với tài liệu hoàn chỉnh cho **vnstock_ta** - thư viện Python cung cấp 25+ chỉ báo kỹ thuật và công cụ vẽ biểu đồ tương tác cho phân tích dữ liệu thị trường chứng khoán Việt Nam.

---

## 🎯 Bắt Đầu Nhanh (Quick Start)

### Cài Đặt Thư Viện

Các gói thư viện vnstock_data được cài đặt **chung** thông qua chương trình cài đặt của Vnstock. Để cài đặt và kích hoạt vnstock_data, vui lòng tham khảo hướng dẫn chi tiết tại:

**🔗 [Hướng Dẫn Cài Đặt Vnstock](https://vnstocks.com/onboard-member)**

Sau khi hoàn thành cài đặt, bạn có thể bắt đầu sử dụng các module trong vnstock_data ngay lập tức.

### 2. Import & Sử Dụng Cơ Bản

```python
from vnstock_data import Quote
from vnstock_ta import Indicator, Plotter

# Lấy dữ liệu
quote = Quote(source="vnd", symbol="VCB")
df = quote.history(start="2024-09-01", end="2024-12-02", interval="1D")
df = df.set_index('time')

# Tính chỉ báo
indicator = Indicator(data=df)
sma = indicator.sma(length=20)
rsi = indicator.rsi(length=14)
macd = indicator.macd()

# Vẽ biểu đồ
plotter = Plotter(data=df, theme='light')
plotter.sma(length=[20, 50], title='SMA 20/50')
plotter.rsi(length=14, title='RSI 14')
```

---

## 📖 Nội Dung Tài Liệu

### [01-overview.md](./01-overview.md)
**Giới thiệu, cấu trúc và cách sử dụng cơ bản**
- Giới thiệu vnstock_ta
- Cấu trúc package
- Các loại chỉ báo (Trend, Momentum, Volatility, Volume)
- Yêu cầu dữ liệu
- Cách sử dụng cơ bản

👉 **Bắt đầu từ đây nếu bạn mới**

### [02-indicators.md](./02-indicators.md)
**Chi tiết 25+ chỉ báo với ví dụ và output thực tế**
- **Trend Indicators** (8 chỉ báo): SMA, EMA, VWAP, VWMA, ADX, AROON, PSAR, SUPERTREND
- **Momentum Indicators** (7 chỉ báo): RSI, MACD, WILLR, CMO, STOCH, ROC, MOM
- **Volatility Indicators** (5 chỉ báo): BBANDS, KC, ATR, STDEV, LINREG
- **Volume Indicators** (1 chỉ báo): OBV

Mỗi chỉ báo bao gồm:
- ✅ Mô tả chi tiết
- ✅ Tham số có thể điều chỉnh
- ✅ Output format (kiểu, cột, giá trị)
- ✅ Ví dụ code thực tế
- ✅ Cách sử dụng best practices

👉 **Đi vào chi tiết từng chỉ báo**

### [03-plotting.md](./03-plotting.md)
**Hướng dẫn vẽ biểu đồ tương tác**
- Khởi tạo Plotter (cơ bản)
- Vẽ từng loại chỉ báo
- Tùy biến giao diện (theme, color, legend)
- Lưu biểu đồ (HTML, PNG, PDF)
- Ví dụ hoàn chỉnh
- Best practices vẽ biểu đồ

👉 **Học cách trực quan hóa dữ liệu**

### [04-best-practices.md](./04-best-practices.md)
**Best practices, patterns, tips & tricks từ thực tế**
- Chuẩn bị dữ liệu (data preparation)
- Kết hợp chỉ báo (indicator combination)
  - Trend following
  - Mean reversion
  - Momentum trading
  - Volatility-based
- Backtesting (thử nghiệm chiến lược)
- Tối ưu hóa tham số
- Giám sát real-time
- Những lỗi phổ biến
- Tips & tricks

👉 **Ứng dụng thực tế trong trading/analysis**

---

## 🔍 Mô Tả Nhanh Các Loại Chỉ Báo

### Trend Indicators (Chỉ Báo Xu Hướng)
Dùng để xác định **xu hướng** của thị trường (tăng, giảm, hay ngang).

| Chỉ báo | Output | Phạm vi | Ứng dụng |
|---------|--------|---------|---------|
| **SMA** | Series | Float | Xu hướng dài hạn |
| **EMA** | Series | Float | Phản ứng nhanh xu hướng |
| **VWAP** | Series | Float | Intraday trading |
| **ADX** | DataFrame | 0-100 | Cường độ xu hướng |
| **SUPERTREND** | DataFrame | Float | Trend + Stop loss |
| **AROON** | DataFrame | 0-100 | Vị trí cao/thấp |
| **PSAR** | DataFrame | Float | Stop loss động |

### Momentum Indicators (Chỉ Báo Động Lực)
Dùng để xác định **sức mạnh** của chuyển động giá.

| Chỉ báo | Output | Phạm vi | Ứng dụng |
|---------|--------|---------|---------|
| **RSI** | Series | 0-100 | Overbought/Oversold |
| **MACD** | DataFrame | Float | Crossover signals |
| **Stoch** | DataFrame | 0-100 | Entry points |
| **ROC** | Series | % | Tốc độ thay đổi |
| **CMO** | Series | -100 to 100 | Động lực |
| **WILLR** | Series | -100 to 0 | Overbought/Oversold |
| **MOM** | Series | Float | Động lực tuyệt đối |

### Volatility Indicators (Chỉ Báo Biến Động)
Dùng để xác định **mức độ dao động** của giá.

| Chỉ báo | Output | Ứng dụng |
|---------|--------|---------|
| **BBANDS** | DataFrame (5 cột) | Dải biến động, breakout |
| **KC** | DataFrame (3 cột) | Alternative to BBANDS |
| **ATR** | Series | Đo biến động tuyệt đối |
| **STDEV** | Series | Độ lệch chuẩn |
| **LINREG** | Series | Hồi quy tuyến tính |

### Volume Indicators (Chỉ Báo Khối Lượng)
Dùng để xác định **xu hướng khối lượng** giao dịch.

| Chỉ báo | Output | Ứng dụng |
|---------|--------|---------|
| **OBV** | Series | Khối lượng tích lũy |

---

## 🎓 Các Bước Sử Dụng

### Step 1: Chuẩn Bị Dữ Liệu
```
Data → set_index('time') → DatetimeIndex ✓
```

### Step 2: Tạo Indicator Object
```
Indicator(data=df) → Indicator object
```

### Step 3: Chọn Chỉ Báo
```
indicator.sma()   → Trend
indicator.rsi()   → Momentum
indicator.bbands() → Volatility
indicator.obv()   → Volume
```

### Step 4: Xử Lý Kết Quả
```
Series → Add to df
DataFrame → Expand columns
```

### Step 5: Phân Tích (Optional)
```
Plotter(data=df) → Vẽ biểu đồ
```

---

## 🚀 Các Trường Hợp Sử Dụng (Use Cases)

### 📈 Phân Tích Xu Hướng Dài Hạn
```python
sma_50 = indicator.sma(length=50)
sma_200 = indicator.sma(length=200)
# Khi SMA50 > SMA200: Uptrend
# Khi SMA50 < SMA200: Downtrend
```

### 📊 Giao Dịch Ngắn Hạn (Swing Trading)
```python
supertrend = indicator.supertrend(length=10, multiplier=3)
rsi = indicator.rsi(length=14)
# Entry: Supertrend up + RSI < 70
# Stop: Supertrend down
```

### 🎯 Bắt Cơ Hội Quay Về Trung Bình
```python
bbands = indicator.bbands(length=20, std=2)
rsi = indicator.rsi(length=14)
# Entry: Giá chạm BBL + RSI < 30
# Exit: Giá về BBM
```

### 🔥 Giao Dịch Động Lực (Momentum)
```python
macd = indicator.macd(fast=12, slow=26, signal=9)
obv = indicator.obv()
# Entry: MACD vượt Signal + OBV tăng
# Exit: MACD xuyên Signal
```

### 🛡️ Quản Lý Rủi Ro
```python
atr = indicator.atr(length=14)
# Stop loss = Entry - (ATR * 2)
# Take profit = Entry + (ATR * 3)
```

---

## ❓ FAQ - Câu Hỏi Thường Gặp

### Q: NaN ở đầu dữ liệu là bình thường?
**A**: Có. Các chỉ báo cần N bars để tính toán, nên N-1 giá trị đầu sẽ là NaN. Ví dụ: SMA(20) sẽ có 19 NaN ở đầu.

### Q: Có thể sử dụng multi-timeframe?
**A**: Có. Bạn có thể lấy dữ liệu từ nhiều timeframe khác nhau và tính chỉ báo cho mỗi timeframe.

### Q: Performance như thế nào?
**A**: Rất nhanh. Hầu hết chỉ báo tính trong < 10ms cho 1000 bars. SUPERTREND là chậm nhất (~20ms).

### Q: Có thể backtest?
**A**: Có. Tài liệu có hướng dẫn backtest trong `04-best-practices.md`.

### Q: Có thể sử dụng intraday?
**A**: Có. Hỗ trợ tất cả timeframe: 1m, 5m, 15m, 1h, 1D, 1W, 1M.

### Q: Có API documentation?
**A**: Có. Mỗi method có docstring chi tiết. Dùng `help(indicator.sma)` để xem.

---

## 🔗 Liên Kết Hữu Ích

- **Vnstock**: https://vnstocks.com/
- **pandas-ta**: https://github.com/twopirllc/pandas-ta
- **TradingView**: https://www.tradingview.com/
- **Investopedia**: https://www.investopedia.com/
- **Technical Analysis Wiki**: https://school.stockcharts.com/

---

## 📝 Tóm Tắt Cấu Trúc Tài Liệu

```
vnstock_ta/
├── 01-overview.md          ← Bắt đầu từ đây
├── 02-indicators.md        ← Chi tiết 25+ chỉ báo
├── 03-plotting.md          ← Vẽ biểu đồ
├── 04-best-practices.md    ← Ứng dụng thực tế
└── README.md              ← File này
```

---

## 🤝 Đóng Góp & Feedback

Nếu bạn có:
- ❓ Câu hỏi → Tạo issue
- 🐛 Bug → Report trên GitHub
- 💡 Ý tưởng cải thiện → Pull request
- 📚 Documentation improvement → Gửi suggestion

---

## 📜 Giấy Phép

Vnstock_ta được cấp phép riêng được quy định [tại đây](https://vnstocks.com/onboard/giay-phep-su-dung). Xem LICENSE file để chi tiết.

---

## 🙏 Cảm Ơn

Cảm ơn bạn đã sử dụng vnstock_ta. Chúc bạn giao dịch thành công! 🚀

---

**Cập nhật lần cuối**: 2024-12-02  
**Phiên bản tài liệu**: 1.0
