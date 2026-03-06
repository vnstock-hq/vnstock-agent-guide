## 05-03-2026

> Phát hành phiên bản vnstock_data 2.5.0

- **Cải thiện & bổ sung API nguồn Vĩ mô (MBK) tại module `vnstock_data/explorer/mbk/macro.py`**:
  - Bổ sung method `interest_rate` để lấy dữ liệu Lãi suất bình quân & Doanh số trên thị trường liên ngân hàng. Hỗ trợ tham số `format='pivot'` (mặc định) để trả về bảng dạng nhóm cột (MultiIndex giống biểu diễn trên website) hoặc `format='long'` để trả về định dạng phẳng (raw format).
  - Tích hợp thêm tham số khoảng thời gian tương đối `length` (ví dụ: `1Y`, `30D`, `100b`) tương tự như cách sử dụng trong `quote.history`. Tính năng này áp dụng đồng bộ cho tất cả các hàm vĩ mô (`gdp`, `cpi`, `interest_rate`, `exchange_rate` v.v...) để bỏ qua việc nhập ngày bắt đầu `start` và kết thúc `end`.
  - Thay đổi thời gian lấy dữ liệu mặc định (*khi không cung cấp `start`, `end`, hoặc `length`*) là 1 năm (`1Y`) để trả về thông tin ở khoảng thời gian phù hợp và nhẹ.
- **Cập nhật UI module**: Cập nhật các lớp UI cung cấp cấu trúc lệnh hợp nhất với phân nhóm chặt chẽ giúp điều hướng dễ dàng theo mặc định mà không cần quan tâm đến thông tin nguồn dữ liệu.

- **Cải thiện API nguồn Hàng hoá (SPL) tại module `vnstock_data/explorer/spl/commodity.py`**:
  - Tích hợp khả năng lấy thời gian tương đối thông qua tham số `length` tương tự như module `macro` và `quote.history`.
  - Thay đổi thời gian lấy dữ liệu mặc định (*khi không cung cấp `start`, `end`, hoặc `length`*) về 1 năm (`1Y`) thay vì lấy toàn bộ lịch sử như trước đây.