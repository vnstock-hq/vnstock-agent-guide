# Vnstock TA - Vẽ Biểu Đồ (Plotting)

> **⚠️ DEPRECATION WARNING**: Lớp `Plotter` và module `vnstock_ta.chart` (dựa trên `pyecharts` và `panel`) **đã bị deprecated** và sẽ chính thức bị gỡ bỏ vào ngày 31/08/2026.

Để vẽ biểu đồ phân tích kỹ thuật hiện đại, đẹp mắt và hỗ trợ agent-ready, vui lòng chuyển sang sử dụng thư viện **`vnstock_ezchart`**.

## Hướng Dẫn Di Chuyển (Migration Guide)

### Cách Cũ (vnstock_ta.chart) - ❌ KHÔNG KHUYẾN NGHỊ

```python
from vnstock_ta import Plotter

# Đã deprecated
plotter = Plotter(data=df, theme='light')
plotter.sma(length=20, title='SMA 20')
```

### Cách Mới (vnstock_ezchart) - ✅ ĐƯỢC KHUYẾN NGHỊ

`vnstock_ezchart` cung cấp tính năng vẽ biểu đồ tương tác, tĩnh và lưu ảnh cho báo cáo.

```python
from vnstock_ta import Indicator
from vnstock_ezchart import Chart

# 1. Tính toán chỉ báo bằng vnstock_ta
ta = Indicator(data=df)
df['SMA_20'] = ta.trend.sma(length=20)
df['RSI_14'] = ta.momentum.rsi(length=14)

# 2. Định nghĩa cấu hình hiển thị
overlays = [
    {"data": df['SMA_20'], "color": "#2563eb", "width": 2}
]

subplots = [
    [{"data": df['RSI_14'], "color": "#8b5cf6", "ylabel": "RSI"}]
]

# 3. Vẽ biểu đồ bằng Chart.candle()
fig, ax = Chart.candle(
    df, 
    title="Biểu đồ với SMA và RSI", 
    figsize=(12, 8), 
    overlays=overlays, 
    subplots=subplots
)
```

Tham khảo thêm tài liệu của `vnstock_ezchart` để xem các kỹ thuật vẽ biểu đồ chuyên sâu, hỗ trợ theme sáng/tối tự động, và xuất ra hình ảnh độ phân giải cao phục vụ backtesting.
