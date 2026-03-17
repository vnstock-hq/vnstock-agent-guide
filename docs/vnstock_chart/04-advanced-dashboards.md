# Phân tích Nâng cao và Bảng Điều khiển (Advanced & Dashboards)

Trong `vnstock_chart`, nhóm biểu đồ trong `vnstock_chart.gallery.advanced` và `vnstock_chart.gallery.dashboard` cung cấp các trang giám sát tích hợp toàn diện. Những lớp này đóng vai trò gom nhóm nhiều biểu đồ lại với nhau trên cùng 1 giao diện dưới dạng thẻ (Tabs/Page).

## Phân tích Nâng cao (Advanced Analysis)

Các lớp biểu đồ phân tích sâu sát kết quả giả lập hoặc thuật toán.

**1. MonteCarloResults**
Hiển thị kết quả của thuật toán mô phỏng đường giá ngẫu nhiên (Monte Carlo Simulation).

**Ví dụ:**
```python
import numpy as np
import pandas as pd
from vnstock_chart.gallery.advanced import MonteCarloResults

# Nhập ma trận giả lập: 1000 đường giá, độ dài 252 ngày
mc_sims_matrix = np.cumprod(1 + np.random.normal(0.0005, 0.015, (1000, 252)), axis=1) * 10000

# Vẽ biểu đồ với các dải phân vị p5, p25, p50, p75, p95
mc_chart = MonteCarloResults(
    simulation_results=mc_sims_matrix,
    percentiles=[5, 25, 50, 75, 95],
    title="Mô phỏng 1000 đường giá danh mục",
    theme="dark"
)

mc_chart.to_html("monte_carlo.html", auto_open=True)
```

**2. Phân tích khác**
- `WalkForwardResults(walkforward_data, **kwargs)`: Thể hiện Backtest Out-of-sample chạy dọc theo thời gian.
- `CapacityAnalysis(capacity_data, **kwargs)`: Mô hình hóa giới hạn quy mô giao dịch (Quy mô NAV tối đa liên quan tới Slippage/Thanh khoản thị trường).
- `ExecutionVisualization(execution_data, **kwargs)`: Đánh giá chất lượng thực thi lệnh giao dịch (tốc độ khớp, giá bị trượt lệnh đo với VWAP).
- `RoundTripAnalysis(trades_data, **kwargs)`: Trải nghiệm vòng đời một cặp lệnh mua-bán khép kín trên cổ phiếu.

*Lưu ý: Các data input ở đây là các mốc thống kê Backtest được tính toán trước qua các framework như VectorBT hoặc Zipline.*

## Xây dựng Dashboard Quản trị (Dashboards)

Dashboards là các lớp "Wrapper" giúp gộp nhiều đối tượng `ChartBase` thành 1 trang duy nhất để báo cáo. Sau khi gọi `.build()`, nó trả về một đối tượng đại diện HTML của `pyecharts` có thể trực tiếp xuất ra.

**1. CompleteDashboard**
Gộp toàn bộ quá trình phân tích lợi nhuận - rủi ro vào một báo cáo điều hướng tổng quát bằng các Tab lớn.

**Ví dụ sử dụng:**
```python
from vnstock_chart.gallery.dashboard import CompleteDashboard

# Khai báo Mock Data (Chuỗi lợi nhuận rỗng cho ví dụ)
dates = pd.date_range("2021-01-01", "2023-12-31", freq="1D")
returns = pd.Series(np.random.normal(0.0002, 0.015, len(dates)), index=dates)
bm_returns = pd.Series(np.random.normal(0.0001, 0.01, len(dates)), index=dates)
equity = (1 + returns).cumprod() * 100_000

# Dummy trades history
trades_df = pd.DataFrame({
    "Symbol": ["TCB", "VCB", "MBB"],
    "Type": ["Long", "Short", "Long"],
    "Return": [0.05, -0.02, 0.12]
})

# Complete Dashboard - Tab mode
# (Yêu cầu phải có method `.build()` thay vì khởi tạo trực tiếp qua `__init__` như các chart lẻ khác)
dashboard_tabs = CompleteDashboard().build(
    equity_data=equity, 
    returns=returns, 
    benchmark_returns=bm_returns, 
    trades=trades_df
)

# Để render:
dashboard_tabs.render("complete_dashboard.html")
# Mở trực tiếp trên web
import webbrowser
webbrowser.open('complete_dashboard.html')
```

**2. BacktestDashboard**
Giống với `CompleteDashboard` nhưng tập trung vào kết quả tĩnh trên màn hình lớn.
`dashboard = BacktestDashboard().build(equity_data, returns, trades, benchmark, positions)`

**3. Các trang lẻ chuyên biệt (Pages)**
Phù hợp cho việc muốn tùy chỉnh Layout website, cho phép bạn trích xuất riêng theo từng module logic:
- `PerformancePage().build(portfolio_returns, benchmark_returns, exposure_data, positions, allocation)`
- `RiskPage().build(equity_data, returns, monte_carlo, capacity_data)`
- `TradingPage().build(trades, execution_data, walkforward_data)`

**Ví dụ xuất một trang Rủi ro cụ thể:**
```python
from vnstock_chart.gallery.dashboard import RiskPage

risk_page = RiskPage().build(
    equity_data=equity, 
    returns=returns, 
    monte_carlo=mc_sims_matrix
)
risk_page.render("my_risk_page_report.html")
```
