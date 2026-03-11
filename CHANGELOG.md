# Nhật Ký Thay Đổi (Changelog)

Tất cả các thay đổi đáng chú ý của dự án **vnstock-agent-guide** sẽ được ghi lại trong tập tin này.

## [1.1.1] - 11/03/2026

- Cập nhật tài liệu cho `vnstock_data` v3.0.0 và tinh chỉnh các hướng dẫn hành vi cho AI Agent.

## [1.1.0] - 02/02/2026

### 🚀 Tính Năng & Cải Tiến

- **Tích hợp Quy trình "Vibe Coding"**: Cập nhật kỹ năng `vnstock-solution-architect` để hỗ trợ tối đa phong cách làm việc "Vibe Coding".
  - Định nghĩa 3 nhóm người dùng rõ ràng: **Người Khám Phá (Explorer)**, **Nhà Phân Tích (Analyst)**, **Chuyên Gia (Expert)**.
  - Triển khai quy trình hỗ trợ 3 giai đoạn: **Khởi tạo** -> **Tinh chỉnh** -> **Gỡ lỗi**.
  - Thêm "Bản đồ hệ sinh thái" để AI chọn đúng thư viện (`vnstock` bản mã nguồn mở miễn phí với `vnstock_data` bản cao cấp).
- **Cải thiện điều hướng AI**:
  - Cập nhật các file hướng dẫn `AGENTS.md`, `CLAUDE.md`, và `GEMINI.md` để tự động trỏ tới tài liệu `setup-and-debug` khi gặp lỗi.
  - Cập nhật câu lệnh copy các file quan trọng vào thư mục dự án của người dùng
  - Bổ sung hướng dẫn xử lý lỗi cụ thể, ưu tiên tham chiếu tài liệu gỡ lỗi thay vì tự đoán.

### 📚 Tài Liệu

- **Module Thiết lập & Gỡ lỗi mới**: Thêm thư mục `docs/setup-and-debug/` vào cấu trúc tài liệu chính trong `README.md` và hướng dẫn cho Agent.
- **Bảng tham chiếu**: Cập nhật bảng "Tra cứu tài liệu" trong tất cả các file hướng dẫn để bao gồm mục Thiết lập & Gỡ lỗi.

### ⚙️ Hệ Thống & Cấu Hình

- Cập nhật `.gitignore` để loại trừ chính xác các file kỹ năng của agent không cần thiết.
- Đồng bộ thông tin phiên bản (v1.1) trên toàn bộ hệ thống tài liệu.

## [1.0.9] - 31/01/2026

### 📚 Tài Liệu

- **Cập nhật vnstock-data**: Làm mới tài liệu cho các module dữ liệu nâng cao trong thư mục `docs/vnstock-data`.
- **Demo Quickstart**: Bổ sung hình ảnh minh họa giao diện Colab vào notebook hướng dẫn nhanh để người dùng dễ hình dung.
- **Sửa lỗi README**: Điều chỉnh đường dẫn lệnh copy trong hướng dẫn cài đặt để khớp với cấu trúc thư mục thực tế.
