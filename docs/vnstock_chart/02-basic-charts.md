# Biểu đồ Cơ bản (Basic Charts)

Thư viện `vnstock_chart` cung cấp các lớp cơ bản để hiển thị các dạng dữ liệu khác nhau. Nhóm biểu đồ này kế thừa trực tiếp từ các biểu đồ cốt lõi của `pyecharts`.

## 1. CandleChart (Biểu đồ Nến)

Được thiết kế đặc biệt cho dữ liệu chứng khoán (nhóm OHLCV). Biểu đồ nến có thể hiển thị dưới nhiều chế độ (chỉ đường giá, hình nến + khối lượng, đè các chỉ báo).

**Lớp:** `vnstock_chart.CandleChart`

**Cú pháp Khởi tạo & Dữ liệu:**
`CandleChart(df=None, dates=None, ohlc=None, volume=None, indicators=None, mode="candle", **kwargs)`
- `df` (DataFrame): Bảng dữ liệu Pandas chứa tối thiểu các cột: `time`, `open`, `high`, `low`, `close`, `volume`.
- `mode` (str):
  - `"candle"`: Nến thường + Khối lượng bên dưới.
  - `"price"`: Đường màu lấp đầy khu vực giá (Area line) + Khối lượng bên dưới.
  - `"overlay"`: Nến + Các đường chỉ báo (`indicators`) nằm chung trên khung giá.
  - `"subplot"`: Nến + Khối lượng + Các chỉ báo ở từng khung phụ (subplots) độc lập.
- `indicators` (List[Dict]): Dành cho chế độ overlay/subplot. Chứa danh sách các đường chỉ báo kỹ thuật, định dạng `[{"name": "SMA20", "data": [...], "color": "#FFF"}, ...]`.

**Ví dụ hiển thị biểu đồ Nến cơ bản với dữ liệu Vnstock:**
```python
from vnstock_data import Market
from vnstock_chart import CandleChart

# Lấy dữ liệu thực tế
df = Market().equity("TCB").ohlcv(start='2024-01-01', end='2024-03-01')

# Thêm Mock Indicator (SMA) để vẽ Overlay
df['sma20'] = df['close'].rolling(20).mean()
indicators = [{"name": "SMA 20", "data": df['sma20'].tolist(), "color": "#f1c40f"}]

# Khởi tạo biểu đồ nến + chỉ báo
chart = CandleChart(
    df=df,
    mode="overlay",
    indicators=indicators,
    title="Biểu đồ giá TCB & SMA20",
    theme="dark",
    width=1000,
    height=600
)

# Hiển thị hoặc xuất HTML
chart.to_html("tcb_candle.html", auto_open=True)
```

## 2. LineChart (Biểu đồ Đường)

Hiển thị một chuỗi dữ liệu kết nối liền mạch qua các mốc thời gian. 

**Cú pháp Khởi tạo:**
`LineChart(x, y, name=None, title="", theme="dark", **kwargs)`

**Ví dụ (Sinh dữ liệu ngẫu nhiên):**
```python
import numpy as np
from vnstock_chart import LineChart

# Dữ liệu mô phỏng 10 ngày
x_days = [f"Day {i+1}" for i in range(10)]
y_values = np.cumsum(np.random.randn(10) * 2 + 1) + 100

line_chart = LineChart(
    x=x_days, 
    y=y_values.tolist(),
    name="Danh mục A",
    title="Tăng trưởng danh mục mô phỏng",
    theme="light"
)

line_chart.render()
```

## 3. BarChart (Biểu đồ Cột)

Phù hợp để so sánh nhiều hạng mục phân loại rời rạc hoặc đo lường chỉ số độc lập.

**Cú pháp Khởi tạo:**
`BarChart(x, y, name=None, show_title=True, show_legend=False, **kwargs)`

**Ví dụ (So sánh lợi nhuận rổ cổ phiếu):**
```python
from vnstock_chart import BarChart

symbols = ["VCB", "TCB", "MBB", "ACB"]
returns = [5.2, 12.4, 8.1, -2.5] # Phần trăm

bar_chart = BarChart(
    x=symbols,
    y=returns,
    name="Lợi nhuận %",
    title="So sánh hiệu suất Ngân hàng (Tháng 1)",
    theme="dark"
)

bar_chart.to_html("bar_chart.html")
```

## 4. ScatterChart (Biểu đồ Tần suất/Phân tán)

Dùng phân tích sự tương quan giữa hai biến, hoặc dùng để chấm các điểm "Mua/Bán" đè lên biểu đồ giá khi kết hợp.

**Cú pháp Khởi tạo:**
`ScatterChart(x, y, name=None, symbol_size=10, **kwargs)`

**Ví dụ:**
```python
import numpy as np
from vnstock_chart import ScatterChart

# Giả lập điểm P/E và LNST của 50 cổ phiếu
pe_ratios = np.random.uniform(5, 25, 50).tolist()
eps_growth = np.random.uniform(-10, 50, 50).tolist()

scatter = ScatterChart(
    x=pe_ratios,
    y=eps_growth,
    name="Cổ phiếu",
    title="Tương quan P/E và Tăng trưởng EPS",
    theme="dark",
    symbol_size=8
)

# Chú ý: Scatter trên pyecharts thường dùng x là category. 
# Trục X cũng có thể truyền list số liệu, hệ thống tự parse.
scatter.render()
```

## 5. HeatmapChart (Biểu đồ Nhiệt)

Dùng cho phân tích ma trận dữ liệu (Ví dụ: Sự biến động giá trị theo Giờ - Ngày, hoặc Danh mục - Tháng).

**Cú pháp Khởi tạo:**
`HeatmapChart(x, y, value, min_value=None, max_value=None, name=None, **kwargs)`
- Tham số `value` trong pyecharts Heatmap yêu cầu định dạng `[[index_x, index_y, value], ...]`. Tuy nhiên `vnstock_chart` có thể tự động handle nếu truyền list phẳng, tùy phiên bản triển khai nội bộ.
- Truyền `x` và `y` là các nhãn (labels).

**Ví dụ:**
```python
import random
from vnstock_chart import HeatmapChart

months = ["Tháng 1", "Tháng 2", "Tháng 3"]
years = ["2022", "2023", "2024"]

# Tạo data dạng [x_idx, y_idx, value]
data = []
for i in range(len(months)):
    for j in range(len(years)):
        val = round(random.uniform(-10, 20), 2)
        data.append([i, j, val])

heatmap = HeatmapChart(
    x=months,
    y=years,
    value=data,
    min_value=-10,
    max_value=20,
    title="Lợi nhuận theo Tháng/Năm",
    theme="dark"
)

heatmap.render()
```

## 6. BoxplotChart (Biểu đồ Hộp)

Phân tích dải phân tán, Outlier của giá trị (thường ứng dụng cho việc so sánh biên độ phần trăm lãi lỗ của các cổ phiếu trong 1 rổ).

**Cú pháp Khởi tạo:**
`BoxplotChart(x, y, name=None, **kwargs)`
- Tham số `y` yêu cầu `List[List[float]]`. Mỗi mảng con là tập giá trị tương ứng với nhãn tại trục `x`.

**Ví dụ:**
```python
import numpy as np
from vnstock_chart import BoxplotChart

sectors = ["Ngân hàng", "Bất động sản", "Thép"]
# Mô phỏng tỷ suất lợi nhuận của 20 mã trong từng ngành
data_bank = np.random.normal(5, 2, 20).tolist()
data_re = np.random.normal(2, 6, 20).tolist()
data_steel = np.random.normal(8, 4, 20).tolist()

box = BoxplotChart(
    x=sectors,
    y=[data_bank, data_re, data_steel],
    name="Biên độ Lợi nhuận %",
    title="Phân bố Lợi nhuận theo Ngành",
    theme="light"
)

box.render()
```
