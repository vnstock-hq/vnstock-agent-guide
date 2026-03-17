import numpy as np
import pandas as pd
import webbrowser
import os
from vnstock_chart import (
    LineChart, BarChart, CandleChart, ScatterChart, BoxplotChart, HeatmapChart
)
from vnstock_chart.gallery.backtest import (
    EquityCurve, ReturnsHistogram, MonthlyReturnsHeatmap, RollingMetrics
)
from vnstock_chart.gallery.advanced import MonteCarloResults
from vnstock_chart.gallery.performance import AllocationChart

def generate_mock_data():
    dates = pd.date_range("2023-01-01", "2024-12-31", freq="B")
    
    # 1. Price Data
    start_price = 15.0
    price_returns = np.random.normal(0.0005, 0.02, len(dates))
    closes = start_price * (1 + price_returns).cumprod()
    
    df = pd.DataFrame(index=dates)
    df['time'] = dates
    df['close'] = closes
    df['open'] = closes * (1 + np.random.normal(0, 0.005, len(dates)))
    df['high'] = df[['open', 'close']].max(axis=1) * (1 + np.abs(np.random.normal(0, 0.005, len(dates))))
    df['low'] = df[['open', 'close']].min(axis=1) * (1 - np.abs(np.random.normal(0, 0.005, len(dates))))
    df['volume'] = np.random.randint(1_000_000, 10_000_000, len(dates))
    
    # 2. Portfolio Returns & Benchmark
    port_returns = pd.Series(np.random.normal(0.001, 0.015, len(dates)), index=dates)
    equity = (1 + port_returns).cumprod() * 100_000
    roll_max = equity.cummax()
    drawdown = (equity - roll_max) / roll_max
    
    bm_returns = pd.Series(np.random.normal(0.0005, 0.012, len(dates)), index=dates)
    benchmark = (1 + bm_returns).cumprod() * 100_000
    
    # 3. Monte Carlo
    mc_matrix = np.cumprod(1 + np.random.normal(0.0008, 0.015, (200, 252)), axis=1) * 100_000
    
    # 4. Allocation
    alloc_df = pd.DataFrame({
        "Ngành": ["Ngân hàng", "Công nghệ", "Bán lẻ", "Tiền mặt"],
        "weight": [40, 30, 20, 10]
    })
    
    return df, port_returns, equity, drawdown, benchmark, mc_matrix, alloc_df

def add_html_title(filepath, title, theme="dark"):
    """
    Do cơ chế pyecharts đôi khi đè title hoặc title quá bé, 
    ta chèn trực tiếp 1 thẻ HTML <h2> vào thân file để đảm bảo lúc nào title cũng hiển thị rõ, nổi bật.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    color = "#fff" if theme == "dark" else "#111"
    title_html = f'<h2 style="text-align: center; margin-top: 30px; font-family: sans-serif; color: {color};">{title}</h2>'
    
    html = html.replace('<body>', f'<body>\n    {title_html}')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

def run_demo():
    print("🚀 Đang khởi tạo dữ liệu mô phỏng cao cấp...")
    df, port_returns, equity, drawdown, benchmark, mc_matrix, alloc_df = generate_mock_data()
    
    output_dir = os.path.abspath("vnstock_demo_outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    print("📈 Đang render Basic Charts...")
    title1 = "1. Đường giá Đóng cửa (Line Chart)"
    c1 = LineChart(
        x=df['time'].dt.strftime('%Y-%m-%d').tolist(), y=df['close'].tolist(),
        name="Giá đóng cửa",
        title=title1, theme="light"
    )
    p1 = os.path.join(output_dir, "01_line_chart.html")
    c1.to_html(p1)
    add_html_title(p1, title1, "light")
    
    title2 = "2. So sánh Lợi nhuận các tháng (Bar Chart)"
    c2 = BarChart(
        x=["Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5"], y=[5.2, 10.1, -2.5, 8.4, 3.1],
        name="Lợi nhuận %",
        title=title2, theme="dark"
    )
    p2 = os.path.join(output_dir, "02_bar_chart.html")
    c2.to_html(p2)
    add_html_title(p2, title2, "dark")
    
    df['sma20'] = df['close'].rolling(20).mean()
    indicators = [{"name": "SMA 20", "data": df['sma20'].tolist(), "color": "#f1c40f"}]
    title3 = "3. Đồ thị nến đa lớp (Candle Overlay)"
    c3 = CandleChart(
        df=df, mode="overlay", indicators=indicators,
        title=title3, theme="dark", width=1200, height=600
    )
    p3 = os.path.join(output_dir, "03_candle_overlay.html")
    c3.to_html(p3)
    add_html_title(p3, title3, "dark")
    
    title4 = "4. Tương quan P/E và Lợi nhuận (Scatter Chart)"
    c4 = ScatterChart(
        x=np.random.uniform(5, 25, 50).tolist(), y=np.random.uniform(-10, 50, 50).tolist(),
        name="Stock",
        title=title4, theme="dark"
    )
    p4 = os.path.join(output_dir, "04_scatter_chart.html")
    c4.to_html(p4)
    add_html_title(p4, title4, "dark")
    
    heatmap_data = []
    for i in range(3):
        for j in range(3):
            heatmap_data.append([i, j, round(np.random.uniform(-10, 20), 2)])
    title5 = "5. Biểu đồ nhiệt Ma trận (Heatmap Chart)"
    c5 = HeatmapChart(
        x=["Jan", "Feb", "Mar"], y=["2022", "2023", "2024"], value=heatmap_data, min_value=-10, max_value=20,
        name="Return", title=title5, theme="light"
    )
    p5 = os.path.join(output_dir, "05_heatmap_chart.html")
    c5.to_html(p5)
    add_html_title(p5, title5, "light")
    
    box_data = [
        np.random.normal(5, 2, 20).tolist(),
        np.random.normal(2, 6, 20).tolist(),
        np.random.normal(8, 4, 20).tolist()
    ]
    title6 = "6. Phân tán lợi nhuận theo ngành (Boxplot Chart)"
    c6 = BoxplotChart(
        x=["Ngân hàng", "BĐS", "Thép"], y=box_data, name="Lợi nhuận %",
        title=title6, theme="dark"
    )
    p6 = os.path.join(output_dir, "06_boxplot_chart.html")
    c6.to_html(p6)
    add_html_title(p6, title6, "dark")

    print("📊 Đang render Performance & Backtest Charts...")
    title7 = "7. Đường cong vốn & Drawdown (Equity Curve)"
    c7 = EquityCurve(
        title=title7, theme="dark", width=1200, height=500
    ).build(equity_data=equity, drawdown_data=drawdown, benchmark=benchmark)
    
    p7 = os.path.join(output_dir, "07_equity_curve.html")
    c7.to_html(p7)
    add_html_title(p7, title7, "dark")

    title8 = "8. Phân phối lợi nhuận (Returns Histogram)"
    c8 = ReturnsHistogram(
        returns=port_returns, bins=50, show_normal=True,
        title=title8, theme="dark"
    )
    p8 = os.path.join(output_dir, "08_returns_histogram.html")
    c8.to_html(p8)
    add_html_title(p8, title8, "dark")
    
    title9 = "9. Bản đồ nhiệt lợi nhuận (Monthly Heatmap)"
    c9 = MonthlyReturnsHeatmap(
        returns=port_returns,
        title=title9, theme="dark"
    )
    p9 = os.path.join(output_dir, "09_monthly_heatmap.html")
    c9.to_html(p9)
    add_html_title(p9, title9, "dark")
    
    title10 = "10. Hiệu suất Rolling (Rolling Metrics)"
    c10 = RollingMetrics(
        returns=port_returns, window=126, risk_free_rate=0.03,
        title=title10, theme="dark", width=1200, height=400
    )
    p10 = os.path.join(output_dir, "10_rolling_metrics.html")
    c10.to_html(p10)
    add_html_title(p10, title10, "dark")
    
    print("🔮 Đang render Advanced & Dashboards...")
    title11 = "11. Thuật toán mô phỏng Monte Carlo (200 trajectories)"
    c11 = MonteCarloResults(
        simulation_results=mc_matrix, percentiles=[5, 25, 50, 75, 95],
        title=title11, theme="dark"
    )
    p11 = os.path.join(output_dir, "11_monte_carlo.html")
    c11.to_html(p11)
    add_html_title(p11, title11, "dark")
    
    title12 = "12. Cơ cấu phân bổ danh mục (Allocation Chart)"
    c12 = AllocationChart(
        allocation_data=alloc_df, allocation_type="Ngành",
        title=title12, theme="light"
    )
    p12 = os.path.join(output_dir, "12_allocation.html")
    c12.to_html(p12)
    add_html_title(p12, title12, "light")

    # Đổi title của file HTML xuất ra bằng cách Regex Replace (Vì pyecharts render default title = Awesome-pyecharts)
    for i in range(1, 13):
        fname = [f for f in os.listdir(output_dir) if f.startswith(f"{i:02d}_") and f.endswith(".html")][0]
        filepath = os.path.join(output_dir, fname)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace("<title>Awesome-pyecharts</title>", f"<title>Chart {i} Demo</title>")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    # Khởi tạo trang Index gom link
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f'''
        <html><head><title>Vnstock Chart Showcase</title>
        <style>body{{font-family: Arial; padding: 40px; background: #111; color: #fff;}} a{{color: #00bcd4; text-decoration: none; font-size: 18px; line-height: 2;}} a:hover{{color: #00e5ff;}}</style>
        </head><body>
        <h1>🌟 Chào mừng đến với Vnstock Chart Full Showcase 🌟</h1>
        <p>Thư viện hiện sở hữu hơn 10 loại biểu đồ tối ưu hoàn chỉnh cho tài chính. Bấm xem báo cáo:</p>
        <h2>Basic Charts</h2>
        <ul>
            <li><a href="01_line_chart.html" target="_blank">📉 1. Line Chart (Đường Giá)</a></li>
            <li><a href="02_bar_chart.html" target="_blank">📊 2. Bar Chart (Cột SO SÁNH)</a></li>
            <li><a href="03_candle_overlay.html" target="_blank">📈 3. Candle Overlay Chart (Nến Đa Lớp)</a></li>
            <li><a href="04_scatter_chart.html" target="_blank">🌌 4. Scatter Chart (Phân Tán)</a></li>
            <li><a href="05_heatmap_chart.html" target="_blank">🔥 5. Basic Heatmap Chart (Biểu đồ Nhiệt)</a></li>
            <li><a href="06_boxplot_chart.html" target="_blank">📦 6. Boxplot Chart (Biểu đồ Hộp)</a></li>
        </ul>
        <h2>Performance & Backtest</h2>
        <ul>
            <li><a href="07_equity_curve.html" target="_blank">⛰️ 7. Equity Curve (Đường Cong Vốn)</a></li>
            <li><a href="08_returns_histogram.html" target="_blank">📏 8. Returns Histogram (Phân Phối LN)</a></li>
            <li><a href="09_monthly_heatmap.html" target="_blank">📅 9. Monthly Heatmap (LN Hàng Tháng)</a></li>
            <li><a href="10_rolling_metrics.html" target="_blank">⚙️ 10. Rolling Metrics</a></li>
        </ul>
        <h2>Advanced & Portfolio</h2>
        <ul>
            <li><a href="11_monte_carlo.html" target="_blank">🎲 11. Monte Carlo Simulation</a></li>
            <li><a href="12_allocation.html" target="_blank">🥧 12. Portfolio Allocation</a></li>
        </ul>
        </body></html>
        ''')
        
    print(f"\n[HOÀN TẤT] Báo cáo Showcase ĐẦY ĐỦ đã sẵn sàng tại: {index_path}")
    webbrowser.open(f"file://{index_path}")

if __name__ == "__main__":
    run_demo()
