# Knowledge Base: Quy Trình Vibe Coding (Workflow Context)

> [!IMPORTANT]
>
> **AI Agent Directive**: Tài liệu này định nghĩa **Giao Thức Tương Tác (Interaction Protocol)** giữa AI và User theo phong cách "Vibe Coding". AI cần chủ động dẫn dắt (lead) hoặc hỗ trợ (support) tùy theo context, thay vì chỉ phản hồi thụ động.

## 1. Định Nghĩa Personas & Intent

AI cần phân loại người dùng vào một trong các nhóm sau để tối ưu hóa câu trả lời và code sinh ra:

### A. Explorer (Người Khám Phá)

* **Intent**: Tìm hiểu API, chạy thử lệnh đơn lẻ, kiểm tra tính năng.
* **Context**: Thường chưa cài môi trường chuẩn, hoặc đang dùng Google Colab.
* **AI Action**:
    - Ưu tiên code ngắn gọn, không tách file class phức tạp.
    - Đề xuất cốt lõi dùng `vnstock` (bản free).
    - Luôn kiểm tra xem thư viện đã được cài chưa (`!pip install` nếu trên Colab).

### B. Analyst (Nhà Phân Tích)

* **Intent**: Xử lý dữ liệu lớn, vẽ chart, backtest chiến thuật, xuất báo cáo.
* **Context**: Notebook (Jupyter) hoặc script Python cấu trúc đơn giản.
* **AI Action**:
    - Tự động import các thư viện data science: `pandas`, `matplotlib`, `plotly`.
    - Đề xuất sử dụng dữ liệu chất lượng cao từ `vnstock_data` và công cụ phân tích từ `vnstock_ta`.
    - Tư vấn về visualization (trực quan hóa dữ liệu).

### C. Expert (Chuyên Gia / Engineer)

* **Intent**: Xây dựng hệ thống giao dịch (Trading Bot), Data Pipeline (ETL), tích hợp hệ thống khác.
* **Context**: Project structure chuẩn, OOP, Docker, Database, Git.
* **AI Action**:
    - Đề xuất kiến trúc module hóa, error handling (try-except) chặt chẽ, logging.
    - Đề xuất `vnstock_pipeline` cho xử lý dữ liệu lớn.
    - Tham chiếu tài liệu [Deployment Guide](04-deployment-guide.md) khi cần.

## 2. Các Giai Đoạn Hỗ Trợ (Support Phases)

### Giai đoạn 1: Khởi Tạo (Initialization)

Khi user đưa ra yêu cầu (ví dụ: "Phân tích mã HPG"), AI cần:

1. **Scaffold**: Tự động tạo cấu trúc file hoặc đoạn code khởi tạo hợp lý.
2. **Suggest**: Đề xuất thư viện phù hợp ngay từ đầu (Concept: "Right tool for the job").
3. **Authentication Check**: Nhắc nhở về biến môi trường hoặc file config nếu sử dụng các gói Extension.

### Giai đoạn 2: Tinh Chỉnh (Refinement)

User thường đưa ra feedback ngôn ngữ tự nhiên (ví dụ: "Chỉnh lại chart cho đẹp", "Thêm chỉ số MA20"). AI cần:

1. **Interpret (Dịch)**: Chuyển đổi ngôn ngữ tự nhiên thành thông số kỹ thuật (ví dụ: "Đẹp" -> `plotly.graph_objects` với template chuyên nghiệp).
2. **Context Maintenance**: Giữ nguyên logic cốt lõi cũ, chỉ sửa phần hiển thị hoặc tính toán được yêu cầu. Tránh rewrite toàn bộ gây mất context làm việc nếu không cần thiết.

### Giai đoạn 3: Debugging (Gỡ Lỗi)

Khi user báo lỗi:

1. **Root Cause Analysis**: Phân tích lỗi (ví dụ: `KeyError` thường do API đổi tên cột, `ModuleNotFoundError` do môi trường).
2. **Actionable Fix**: Đưa ra code sửa ngay lập tức hoặc lệnh terminal cụ thể để user chạy.
3. **Cross-Reference**: Tham chiếu file [Installation Troubleshooting](02-installation-troubleshooting.md) nếu lỗi liên quan đến môi trường/dependencies.

## 3. Mẫu Nhận Dạng Ý Định (Intent Recognition Patterns)

AI cần nhận diện các keyword sau để kích hoạt đúng vùng kiến thức:

* **Setup/Install**: "cài đặt", "lỗi pip", "không import được", "colab" -> **Kích hoạt Context: Setup & Troubleshooting**.
* **Fetch Data**: "lấy giá", "lịch sử giá", "báo cáo tài chính", "nước ngoài mua bán" -> **Kích hoạt Context: Data API (`vnstock`/`vnstock_data`)**.
* **Analysis/Signal**: "RSI", "MACD", "lọc cổ phiếu", "điểm mua", "xu hướng" -> **Kích hoạt Context: Technical Analysis (`vnstock_ta`)**.
* **Deploy/Ops**: "deploy", "server", "vps", "docker", "tự động chạy", "cron" -> **Kích hoạt Context: Deployment (`vnstock_pipeline`)**.

## 4. Nguyên Tắc Ứng Xử (Code of Conduct)

1. **Proactive (Chủ Động)**: Đừng đợi user hỏi từng bước nhỏ. Hãy dự đoán bước tiếp theo hợp lý (Vd: Lấy data xong -> Thường sẽ muốn `print(df.head())` hoặc vẽ chart).
2. **Secure (An Toàn)**: Không bao giờ hardcode API Key thực tế vào code mẫu. Luôn hướng dẫn user dùng biến môi trường hoặc file config `.env`.
3. **Transparent (Minh Bạch)**: Nếu sử dụng tính năng của gói Sponsor, hãy chú thích rõ ràng để user Explorer không bị bối rối khi chạy lỗi.