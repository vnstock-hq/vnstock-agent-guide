# Vnstock TA - Hướng Dẫn Vẽ Biểu Đồ

## Giới Thiệu

Chương này hướng dẫn sử dụng lớp `Plotter` để vẽ các biểu đồ tương tác (interactive charts) từ dữ liệu và chỉ báo kỹ thuật. Biểu đồ được sinh ra bằng `pyecharts` và có thể xem trong trình duyệt hoặc Jupyter notebook.

---

## I. Khởi Tạo Plotter

### Cú Pháp Cơ Bản

```python
from vnstock_ta import Plotter

plotter = Plotter(
    data=df,           # DataFrame với index là datetime
    theme='light',      # 'light' hoặc 'dark'
    watermark=False,    # Hiển thị watermark
    display=True        # Hiển thị biểu đồ
)
```

### Tham Số

- **`data`** (pd.DataFrame): DataFrame với index là `time` (DatetimeIndex), chứa cột: 'open', 'high', 'low', 'close', 'volume'
- **`theme`** (str): Giao diện
  - `'light'`: Sáng (mặc định)
  - `'dark'`: Tối, phù hợp cho màn hình
- **`watermark`** (bool): Hiển thị watermark Vnstock (mặc định: False)
- **`display`** (bool): Hiển thị biểu đồ ngay (mặc định: True)

### Ví Dụ

```python
from vnstock_data import Quote
from vnstock_ta import Plotter

# Lấy dữ liệu
quote = Quote(source="vnd", symbol="VCB")
df = quote.history(start="2024-09-01", end="2024-12-02", interval="1D")
df = df.set_index('time')

# Tạo Plotter
plotter = Plotter(data=df, theme='light', watermark=False)
```

---

## II. Vẽ Chỉ Báo Xu Hướng

### 1. SMA - Simple Moving Average

**Mô tả**: Vẽ SMA một hoặc nhiều kỳ trên biểu đồ giá.

**Tham số**:
- `length` (int hoặc list): Kỳ SMA. Có thể là số (VD: 20) hoặc danh sách (VD: [20, 50])
- `title` (str): Tiêu đề biểu đồ (mặc định: 'Simple Moving Average')
- `color` (str): Màu sắc (hex color, VD: '#FF6B6B')
- `legend` (bool): Hiển thị legend (mặc định: True)
- `watermark` (bool): Hiển thị watermark (mặc định: False)
- `minimal` (bool): Hiển thị tối thiểu (chỉ SMA, không giá) (mặc định: False)

**Ví dụ**:

```python
# SMA 20
plotter.sma(length=20, title='SMA 20', legend=True)

# SMA 20 & 50
plotter.sma(length=[20, 50], title='SMA Crossover')
```

### 2. EMA - Exponential Moving Average

**Mô tả**: Vẽ EMA, tương tự SMA nhưng phản ứng nhanh hơn.

**Tham số**: Tương tự SMA

**Ví dụ**:

```python
# EMA 12
plotter.ema(length=12, title='EMA 12', legend=True)

# EMA 12 & 26
plotter.ema(length=[12, 26], title='MACD EMA Lines')
```

### 3. VWAP - Volume Weighted Average Price

**Mô tả**: Vẽ VWAP trên biểu đồ giá.

**Tham số**:
- `anchor` (str): Khoảng thời gian (mặc định: 'D' - Daily)
- Tham số khác tương tự SMA

**Ví dụ**:

```python
# VWAP hàng ngày
plotter.vwap(anchor='D', title='VWAP Daily', legend=True)

# VWAP hàng tuần
plotter.vwap(anchor='W', title='VWAP Weekly')
```

### 4. VWMA - Volume Weighted Moving Average

**Mô tả**: Vẽ VWMA.

**Ví dụ**:

```python
plotter.vwma(length=20, title='VWMA 20', legend=True)
```

### 5. ADX - Average Directional Index

**Mô tả**: Vẽ ADX, DMP, DMN dưới biểu đồ giá.

**Tham số**:
- `length` (int): Số kỳ (mặc định: 14)
- Tham số khác tương tự SMA

**Ví dụ**:

```python
plotter.adx(length=14, title='ADX 14')
```

### 6. Aroon & Aroon Oscillator

**Mô tả**: Vẽ Aroon Up, Down, và Oscillator.

**Ví dụ**:

```python
plotter.aroon(length=14, title='Aroon Indicator')
```

### 7. PSAR - Parabolic Stop and Reverse

**Mô tả**: Vẽ PSAR làm stop loss động.

**Ví dụ**:

```python
plotter.psar(af0=0.02, af=0.02, max_af=0.2, title='Parabolic SAR')
```

### 8. SUPERTREND - Supertrend

**Mô tả**: Vẽ Supertrend trên biểu đồ giá.

**Tham số**:
- `length` (int): Kỳ ATR (mặc định: 10)
- `multiplier` (float): Hệ số nhân ATR (mặc định: 3)

**Ví dụ**:

```python
plotter.supertrend(length=10, multiplier=3, title='Supertrend')
```

---

## III. Vẽ Chỉ Báo Động Lực

### 1. RSI - Relative Strength Index

**Mô tả**: Vẽ RSI dưới biểu đồ giá với vùng overbought (> 70) và oversold (< 30).

**Tham số**:
- `length` (int): Số kỳ (mặc định: 14)
- `title`, `color`, `legend`, `watermark`, `minimal`: Tương tự SMA

**Ví dụ**:

```python
plotter.rsi(length=14, title='RSI 14', legend=True)
```

### 2. MACD - Moving Average Convergence Divergence

**Mô tả**: Vẽ MACD line, Signal line, và Histogram.

**Tham số**:
- `fast`, `slow`, `signal`: Tham số EMA (mặc định: 12, 26, 9)
- Tham số khác tương tự RSI

**Ví dụ**:

```python
plotter.macd(fast=12, slow=26, signal=9, title='MACD')
```

### 3. WILLR - Williams %R

**Mô tả**: Vẽ Williams %R.

**Ví dụ**:

```python
plotter.willr(length=14, title='Williams %R')
```

### 4. CMO - Chande Momentum Oscillator

**Mô tả**: Vẽ CMO.

**Ví dụ**:

```python
plotter.cmo(length=9, title='Chande Momentum Oscillator')
```

### 5. STOCH - Stochastic Oscillator

**Mô tả**: Vẽ %K và %D lines với vùng overbought (> 80) và oversold (< 20).

**Tham số**:
- `k`, `d`, `smooth_k`: Tham số (mặc định: 14, 3, 3)

**Ví dụ**:

```python
plotter.stoch(k=14, d=3, smooth_k=3, title='Stochastic Oscillator')
```

### 6. ROC - Rate of Change

**Mô tả**: Vẽ ROC.

**Ví dụ**:

```python
plotter.roc(length=9, title='Rate of Change')
```

### 7. MOM - Momentum

**Mô tả**: Vẽ MOM.

**Ví dụ**:

```python
plotter.mom(length=10, title='Momentum')
```

---

## IV. Vẽ Chỉ Báo Biến Động

### 1. BBANDS - Bollinger Bands

**Mô tả**: Vẽ Upper/Middle/Lower Bollinger Bands trên biểu đồ giá.

**Tham số**:
- `length` (int): Số kỳ (mặc định: 14)
- `std` (float): Độ lệch chuẩn (mặc định: 2)
- Tham số khác tương tự SMA

**Ví dụ**:

```python
plotter.bbands(length=14, std=2, title='Bollinger Bands (20, 2)')
```

### 2. KC - Keltner Channels

**Mô tả**: Vẽ Keltner Channels trên biểu đồ giá.

**Tham số**:
- `length`, `scalar`, `mamode`: Tham số KC

**Ví dụ**:

```python
plotter.kc(length=20, scalar=2.0, mamode='ema', title='Keltner Channels')
```

### 3. ATR - Average True Range

**Mô tả**: Vẽ ATR dưới biểu đồ.

**Ví dụ**:

```python
plotter.atr(length=14, title='Average True Range')
```

### 4. STDEV - Standard Deviation

**Mô tả**: Vẽ Standard Deviation.

**Ví dụ**:

```python
plotter.stdev(length=14, ddof=1, title='Standard Deviation')
```

### 5. LINREG - Linear Regression

**Mô tả**: Vẽ Linear Regression line.

**Ví dụ**:

```python
plotter.linreg(length=14, title='Linear Regression')
```

---

## V. Vẽ Chỉ Báo Khối Lượng

### 1. OBV - On Balance Volume

**Mô tả**: Vẽ OBV dưới biểu đồ.

**Ví dụ**:

```python
plotter.obv(title='On Balance Volume')
```

---

## VI. Tùy Biến Giao Diện

### Thay Đổi Theme

```python
# Theme sáng (Light)
plotter = Plotter(data=df, theme='light')

# Theme tối (Dark)
plotter = Plotter(data=df, theme='dark')
```

**Light Theme**:
- Màu nền: Trắng/xám nhạt
- Phù hợp: In ấn, báo cáo chính thức
- Màu sắc: Đa dạng, dễ phân biệt

**Dark Theme**:
- Màu nền: Đen/xám đậm
- Phù hợp: Màn hình, real-time trading
- Màu sắc: Nổi bật, dễ nhìn lâu

### Hiển Thị/Ẩn Watermark

```python
# Không watermark (mặc định)
plotter = Plotter(data=df, watermark=False)

# Có watermark
plotter = Plotter(data=df, watermark=True)
```

### Chế Độ Tối Thiểu (Minimal)

```python
# Chỉ hiển thị chỉ báo, không hiển thị giá
plotter.sma(length=20, minimal=True)
```

---

## VII. Lưu Biểu Đồ

### Lưu HTML

```python
from vnstock_ta import Plotter

plotter = Plotter(data=df, theme='light', display=False)
chart = plotter.sma(length=20, title='SMA 20')

# Lưu file HTML
chart.render_notebook()  # Trong Jupyter
# hoặc
chart.render('/path/to/chart.html')  # Lưu file
```

### Xuất PDF/PNG

pyecharts hỗ trợ xuất PDF/PNG qua `snapshot_phantomjs` hoặc công cụ khác:

```python
# Cần cài đặt: pip install pyecharts-snapshot
from pyecharts.commons.utils import write_png

chart = plotter.sma(length=20)
write_png(chart.render_notebook(), 'chart.png')
```

---

## VIII. Ví Dụ Hoàn Chỉnh

### Phân Tích Một Cổ Phiếu

```python
from vnstock_data import Quote
from vnstock_ta import Plotter

# 1. Lấy dữ liệu
quote = Quote(source="vnd", symbol="VCB")
df = quote.history(start="2024-09-01", end="2024-12-02", interval="1D")
df = df.set_index('time')

# 2. Tạo Plotter
plotter = Plotter(data=df, theme='light', watermark=False)

# 3. Vẽ biểu đồ
# Vẽ SMA
plotter.sma(length=[20, 50], title='SMA 20/50 Crossover')

# Vẽ RSI
plotter.rsi(length=14, title='RSI 14')

# Vẽ MACD
plotter.macd(fast=12, slow=26, signal=9, title='MACD')

# Vẽ Bollinger Bands
plotter.bbands(length=20, std=2, title='Bollinger Bands')

# Vẽ SUPERTREND
plotter.supertrend(length=10, multiplier=3, title='Supertrend')
```

### So Sánh Hai SMA

```python
# Vẽ SMA 20 và 50 cùng một chart
plotter.sma(length=[20, 50], title='SMA Crossover: 20 vs 50')
```

### Combo Chỉ Báo (Trend + Momentum)

```python
# SMA trên giá
plotter.sma(length=20, title='VCB - SMA 20 + RSI 14')

# RSI dưới
plotter.rsi(length=14, title='')
```

---

## IX. Best Practices Vẽ Biểu Đồ

### 1. Chọn Chỉ Báo Phù Hợp

```python
# Phân tích xu hướng dài hạn: SMA 50/200, ADX
plotter.sma(length=[50, 200], title='Long-term Trend')

# Phân tích ngắn hạn: SMA 5/10/20, RSI, MACD
plotter.sma(length=[5, 10, 20], title='Short-term Trend')

# Định vị điểm vào: RSI + Stoch
plotter.rsi(length=14, title='RSI 14 for Entry')
plotter.stoch(k=14, d=3, smooth_k=3, title='Stoch for Confirmation')
```

### 2. Combo Hiệu Quả

**Swing Trading**:
```python
plotter.supertrend(length=10, multiplier=3)  # Trend & Stop
plotter.rsi(length=14)                        # Momentum
plotter.obv()                                 # Volume
```

**Day Trading**:
```python
plotter.sma(length=[5, 10], title='5/10 SMA')
plotter.rsi(length=9)  # Faster RSI
plotter.stoch(k=5, d=3, smooth_k=3)
```

**Scalping**:
```python
plotter.vwap()
plotter.atr(length=5)
plotter.rsi(length=5)
```

### 3. Tránh Quá Tải Chỉ Báo

```python
# ❌ Tránh: Quá nhiều chỉ báo
plotter.sma(length=20)
plotter.ema(length=12)
plotter.vwap()
plotter.vwma(length=20)
plotter.adx()
# ...

# ✅ Tốt: Chọn 3-4 chỉ báo
plotter.sma(length=[20, 50])     # Trend
plotter.rsi(length=14)            # Momentum
plotter.bbands(length=20, std=2)  # Volatility
```

### 4. Sử Dụng Màu Sắc Hợp Lý

```python
# Light theme cho in ấn
plotter = Plotter(data=df, theme='light')

# Dark theme cho desktop
plotter = Plotter(data=df, theme='dark')

# Custom color
plotter.sma(length=20, color='#FF6B6B', title='Custom SMA')
```

---

## X. Lưu Ý & Troubleshooting

### Lỗi Thường Gặp

**1. ValueError: Index must be DatetimeIndex**

```python
# ❌ Sai: Index là RangeIndex
plotter = Plotter(data=df)  # df có RangeIndex

# ✅ Đúng: Index là DatetimeIndex
df = df.set_index('time')
plotter = Plotter(data=df)
```

**2. No module named 'pyecharts'**

```bash
# Cài đặt
pip install pyecharts
```

**3. Biểu đồ không hiển thị trong Jupyter**

```python
# Sử dụng render_notebook()
chart = plotter.sma(length=20)
chart.render_notebook()
```

### Performance Tips

- **Dữ liệu lớn**: Nên giảm số lượng chỉ báo hoặc dữ liệu
- **Render nhanh**: Sử dụng `display=False` và render sau
- **File nhỏ**: Giảm độ phân giải hoặc số điểm dữ liệu

---

## XI. Tài Liệu Tham Khảo

- **pyecharts**: https://pyecharts.org/
- **pandas-ta**: https://github.com/twopirllc/pandas-ta
- **TradingView**: https://www.tradingview.com/
