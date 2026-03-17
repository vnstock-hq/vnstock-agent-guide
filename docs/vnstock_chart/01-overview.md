# Tổng quan vnstock_chart

## 1. Giới thiệu

`vnstock_chart` là thư viện hỗ trợ vẽ biểu đồ chuyên nghiệp cho hệ sinh thái vnstock, được xây dựng dựa trên `pyecharts`. Thư viện giúp trực quan hóa dữ liệu tài chính từ cấu trúc cơ bản (Nến, Đường, Cột) đến các Dashboard phân tích hiệu suất và rủi ro phức tạp.

Đặc điểm nổi bật:
- Hỗ trợ hiển thị tự động trên nhiều môi trường: Jupyter Notebook, Google Colab, và Terminal.
- Cung cấp sẵn các giao diện (themes) và bảng màu (palettes) tối/sáng chuẩn tài chính, đẹp mắt.
- Tích hợp sẵn công cụ tương tác: DataZoom (phóng to/thu nhỏ), Tooltip (xem chi tiết giá trị), Toolbox (tải ảnh, đổi loại biểu đồ).
- Dễ dàng xuất biểu đồ ra file HTML phục vụ chia sẻ hoặc nhúng (embed) vào web app (Streamlit, Flask, Dash).

## 2. Cài đặt

Để cài đặt phiên bản mới nhất của `vnstock_chart`, vui lòng chạy lệnh sau trong Terminal của bạn:

```bash
pip install --extra-index-url https://vnstocks.com/api/simple vnstock_chart
```

> **Mách nhỏ**: Bạn có thể trải nghiệm ngay độ "ngầu" và toàn bộ hơn 12 loại biểu đồ trong thư viện bằng cách chạy kịch bản Demo có sẵn:
> ```bash
> python docs/vnstock_chart/demo_vnstock_chart.py
> ```
> Script sẽ sinh dữ liệu mô phỏng, xuất tất cả file báo cáo hiển thị chuyên nghiệp với tab/tiêu đề rõ ràng vào thư mục `vnstock_demo_outputs` và tự động mở trên trình duyệt.

## 3. Giao diện và Kích thước

`vnstock_chart` quản lý giao diện thông qua tham số khởi tạo cấu hình chung cho mọi biểu đồ kế thừa từ `ChartBase`.

### 3.1. Tham số dùng chung
Khi khởi tạo bất kỳ biểu đồ nào, hệ thống đều hỗ trợ các tham số sau:
- `title` (str): Tiêu đề của biểu đồ.
- `theme` (str): Giao diện tổng thể. Thường dùng `"dark"` hoặc `"light"`.
- `color_category` (str): Chủ đề màu cụ thể (ví dụ: `"default"`, `"paper"`). Nếu bỏ trống sẽ tự chọn theo `theme`.
- `width` (int): Chiều rộng ngầm định (pixel).
- `height` (int): Chiều cao ngầm định (pixel).
- `size_preset` (str): Preset kích thước có sẵn (ví dụ: `"mini"`, `"small"`, `"medium"`, `"large"`, `"wide"`, `"tall"`). Dùng khi lười nhập width/height.

### 2.2. Ví dụ cách áp dụng cài đặt chung
```python
from vnstock_chart import LineChart

# Khởi tạo sử dụng preset size và giao diện sáng
chart = LineChart(
    x=["2024", "2025", "2026"],
    y=[100, 150, 120],
    title="Lợi nhuận",
    theme="light",
    size_preset="medium"
)
```

## 3. Các Phương thức Xuất & Hiển thị

Tất cả các đối tượng biểu đồ trong `vnstock_chart` đều hỗ trợ 3 phương thức xuất chính để hiển thị kết quả:

### `render(auto_open: Optional[bool] = None)`
Tự động phát hiện môi trường đang chạy và thiết lập cách thức hiển thị hợp lý nhất.
- Tại Jupyter/Colab: Biểu đồ được vẽ trực tiếp dưới cell.
- Tại Terminal: Tạo file tệp HTML ở background và mở bằng trình duyệt mặc định nếu `auto_open=True`.

### `to_html(path: str, auto_open: bool = False)`
Lưu trực tiếp biểu đồ tương tác thành một file HTML độc lập.
- `path` (str): Đường dẫn lưu file mong muốn (ví dụ: `"my_chart.html"`).
- `auto_open` (bool): Tự động mở trình duyệt web sau khi lưu.

### `embed() -> str`
Trả về một đoạn mã HTML dạng chuỗi (string) chứa nội dung của biểu đồ. Chức năng này tối ưu để dùng cho các UI Framework (chèn trực tiếp HTML vào Streamlit qua `components.html(...)`).
