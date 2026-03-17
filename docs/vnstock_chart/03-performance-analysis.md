# Phân tích Hiệu suất và Backtest (Performance & Backtest)

Thư viện `vnstock_chart` cung cấp một bộ công cụ hiển thị (Gallery) rất mạnh mẽ chuyên dùng cho phân tích kết quả giao dịch (backtesting) và quản trị rủi ro danh mục. Các lớp này nằm trong thư mục con `vnstock_chart.gallery.performance` và `vnstock_chart.gallery.backtest`.

Lưu ý: Các biểu đồ trong nhóm này hầu hết lấy đầu vào dạng `pandas.Series` hoặc `pandas.DataFrame`.

## 1. Biểu đồ Đường cong Vốn (EquityCurve)
Biểu đồ quan trọng nhất dùng để theo dõi sự tăng trưởng của NAV/Vốn theo thời gian, kết hợp đường so sánh (Benchmark) và dải màu cảnh báo sụt giảm (Drawdown).

**Cú pháp Khởi tạo:**
`EquityCurve(equity_data, drawdown_data=None, benchmark=None, show_drawdown=True, **kwargs)`

**Ví dụ hiển thị:**
```python
import pandas as pd
import numpy as np
from vnstock_chart.gallery.backtest import EquityCurve

# Tạo dữ liệu mô phỏng
dates = pd.date_range("2023-01-01", periods=252, freq="1D")
returns = np.random.normal(0.001, 0.015, 252) # Lợi nhuận kỳ vọng dương
equity = pd.Series((1 + returns).cumprod() * 100000, index=dates)

# Tính Drawdown (đỉnh gần nhất)
roll_max = equity.cummax()
drawdown = (equity - roll_max) / roll_max

# Đường VN-Index mô phỏng
bm_returns = np.random.normal(0.0005, 0.01, 252)
benchmark = pd.Series((1 + bm_returns).cumprod() * 100000, index=dates)

chart = EquityCurve(
    title="Đường cong vốn Danh mục A",
    theme="dark"
).build(
    equity_data=equity,
    drawdown_data=drawdown,
    benchmark=benchmark
)

chart.to_html("equity_curve.html")

```

## 2. Bản đồ Nhiệt Lợi nhuận (MonthlyReturnsHeatmap)
Thể hiện mức độ sinh lời (lãi/lỗ) của danh mục theo từng tháng trong các năm khác nhau.

**Cú pháp Khởi tạo:**
`MonthlyReturnsHeatmap(returns, **kwargs)`

**Ví dụ hiển thị:**
```python
from vnstock_chart.gallery.backtest import MonthlyReturnsHeatmap

# Tạo chuỗi tỷ suất lợi nhuận hàng ngày trong 3 năm
dates_3y = pd.date_range("2021-01-01", "2023-12-31", freq="1D")
daily_returns = pd.Series(np.random.normal(0.0005, 0.02, len(dates_3y)), index=dates_3y)

heatmap = MonthlyReturnsHeatmap(
    returns=daily_returns,
    title="Lợi nhuận theo tháng",
    theme="light"
)

heatmap.render()
```

## 3. Phân phối Lợi nhuận (ReturnsHistogram)
Biểu đồ phân phối chuẩn (Histogram) của chuỗi tỷ suất sinh lời, giúp nhận định rủi ro phân phối đuôi béo (fat-tail).

**Cú pháp Khởi tạo:**
`ReturnsHistogram(returns, bins=50, show_normal=True, **kwargs)`

**Ví dụ hiển thị:**
```python
from vnstock_chart.gallery.backtest import ReturnsHistogram

hist_chart = ReturnsHistogram(
    returns=daily_returns,
    bins=40,
    show_normal=True,
    title="Phân phối lợi nhuận hàng ngày",
    theme="dark",
    width=800,
    height=500
)

hist_chart.render()
```

## 4. Đo lường Hiệu suất Cuốn (RollingMetrics)
Đo lường độ ổn định của danh mục qua các khoảng thời gian trượt (Rolling Window) để xem Sharpe, Độ biến động... có nhất quán không.

**Cú pháp Khởi tạo:**
`RollingMetrics(returns, window=252, risk_free_rate=0.0, **kwargs)`

**Ví dụ:**
```python
from vnstock_chart.gallery.backtest import RollingMetrics

rolling = RollingMetrics(
    returns=daily_returns,
    window=126, # Nửa năm
    risk_free_rate=0.03, # 3% năm
    title="Hiệu suất cuốn (Rolling Sharpe & Volatility)"
)
rolling.render()
```

## 5. Tỷ trọng Danh mục (AllocationChart)
Hiển thị cơ cấu phân bổ dòng vốn hiện có. Thường là biểu đồ tròn (Pie/Donut).

**Cú pháp Khởi tạo:**
`AllocationChart(allocation_data, allocation_type="sector", **kwargs)`
- `allocation_data` (DataFrame): Bảng chứa giá trị và nhãn phân bổ. Cần cung cấp các cột hợp lệ cho vnstock_chart đọc. Thường là chỉ mục index.

**Ví dụ:**
```python
from vnstock_chart.gallery.performance import AllocationChart

# DataFrame mô phỏng tỷ trọng các ngành
alloc_df = pd.DataFrame({
    "value": [40, 25, 20, 15]
}, index=["Ngân hàng", "Bất động sản", "Bán lẻ", "Thép"])

alloc = AllocationChart(
    allocation_data=alloc_df,
    allocation_type="Ngành nghề",
    title="Phân bổ Theo ngành",
    theme="light"
)

alloc.render()
```

## 6. So sánh với Chỉ số Tham chiếu (BenchmarkComparison)
Biểu đồ theo dõi sự cách biệt (Alpha) giữa dòng tiền danh mục so với VNINDEX qua từng mốc Rolling rủi ro.

**Ví dụ:**
```python
from vnstock_chart.gallery.performance import BenchmarkComparison

bm_comp = BenchmarkComparison(
    portfolio_returns=daily_returns,
    benchmark_returns=pd.Series(np.random.normal(0.0003, 0.015, len(dates_3y)), index=dates_3y),
    window=252,
    title="So sánh với VN-Index"
)

bm_comp.render()
```

## 7. Các biểu đồ chi tiết vị thế (Trade)

- `ExposureChart(exposure_data, **kwargs)`: Độ phơi nhiễm rủi ro theo từng mã, đòn bẩy. Đầu vào là DataFrame lịch sử các mốc Cash/Stock ratio.
- `TopPositions(positions_data, top_n=10, chart_type="bar", **kwargs)`: Top `N` vị thế nắm giữ nhiều vốn hoặc sinh lời cao nhất.
- `TradeDuration(trades_data, bins=20, **kwargs)`: Phân tích thời gian nắm giữ cổ phiếu dài/ngắn dựa trên bảng lịch sử giao dịch. Thông thường nhận DataFrame `trades` có cột thời gian đóng mở lệnh.
