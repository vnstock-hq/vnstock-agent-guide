# Knowledge Base: Bối Cảnh Triển Khai Vnstock (Deployment Context)

> [!IMPORTANT]
> **Chỉ Dẫn Cho AI Agent**: Tài liệu này định nghĩa **Quy Trình Hoạt Động Tiêu Chuẩn (SOP)** về kỹ thuật để triển khai các ứng dụng Vnstock. Khi hỗ trợ người dùng deploy, hãy tuân thủ nghiêm ngặt các cấu hình và ràng buộc dưới đây.

## 1. Tiêu Chuẩn Dockerization

Khi tạo `Dockerfile` cho ứng dụng Vnstock, bạn bắt buộc phải đảm bảo các ràng buộc môi trường sau để hỗ trợ các thư viện C++ extension (như `vnstock_ta`, `vnstock_pipeline`).

### Khuyến Nghị Base Image
*   **Ưu tiên (Primary)**: `python:3.10-slim-bullseye` (Cân bằng tốt nhất giữa kích thước và độ ổn định).
*   **Thứ cấp (Secondary)**: `python:3.11-slim` (Nếu cần hiệu năng cao, nhưng cần kiểm tra tính tương thích).
*   **Tránh dùng (Avoid)**: `Alpine Linux` (Do vấn đề tương thích của thư viện `musl` libc với một số wheel đã biên dịch trong hệ sinh thái Python data science).

### Các Gói Phụ Thuộc Build (Build Dependencies)
Các gói hệ thống sau **BẮT BUỘC** phải được cài đặt trước khi chạy lệnh `pip install`:
```dockerfile
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*
```

### Chiến Lược Tối Ưu Hóa (Optimization Strategy)
*   Sử dụng **Multi-stage builds**: Biên dịch dependencies ở giai đoạn `builder` và chỉ copy thư mục `site-packages` sang image cuối cùng để giảm kích thước.
*   **Pip Flags**: Luôn sử dụng `--no-cache-dir` để giữ cho image nhỏ gọn nhất.

## 2. Chiến Lược Triển Khai VPS (Ubuntu/Debian)

Khi tạo các script cài đặt tự động (Bash/Ansible) cho VPS, hãy ép buộc trạng thái sau:

### Yêu Cầu Hệ Thống
*   **Hệ Điều Hành**: Ubuntu 22.04 LTS hoặc mới hơn.
*   **Python**: Phiên bản 3.10+.
*   **Môi Trường Ảo (Virtual Environment)**: BẮT BUỘC. Không được cài đặt gói vào môi trường global của hệ thống.

### Quản Lý Service (Systemd)
Luôn ưu tiên sử dụng `systemd` cho các tiến trình chạy ngầm (ví dụ: trading bot, crawler).
**Context cho Service Template chuẩn:**
*   **User**: Nên dùng user thường (non-root, ví dụ: `vnstock`).
*   **Restart Policy**: `on-failure` hoặc `always`.
*   **Environment**: Load biến môi trường từ file `.env`.

### Context Bảo Mật (Security)
*   **Tường Lửa (Firewall)**: UFW phải được bật. Chỉ cho phép Port SSH (22) và Web Ports (80/443).
*   **Dependencies**: Đề xuất sử dụng `vnstock-installer` để setup môi trường ban đầu, đảm bảo các dependencies nội bộ (`vnii`, `vnai`) được giải quyết đúng đắn.

## 3. Context Cho Serverless & PaaS (Railway, Netlify, Render)

### Cảnh Báo Hệ Thống File "Vô Thường" (Ephemeral Filesystem)
**QUAN TRỌNG**: Các môi trường Serverless (Railway, Render, Vercel) có hệ thống file tạm thời.
*   **Ràng Buộc**: Dữ liệu ghi vào file cục bộ (CSV, Excel, JSON) sẽ bị **MẤT** khi redeploy hoặc restart.
*   **Chỉ Dẫn**: Hãy phát hiện các đoạn code lưu file trong code người dùng (ví dụ: `df.to_csv`) và đề xuất tái cấu trúc (refactor) để sử dụng:
    *   **Cloud Storage**: AWS S3, Google Cloud Storage, MinIO.
    *   **Database**: PostgreSQL, MongoDB (cho dữ liệu có cấu trúc).

### File Cấu Hình (Config Files)
*   **Railway/Render**: Xác định điểm khởi chạy (entry point) và tạo lệnh `start`.
    *   *Python Scripts*: `python main.py`
    *   *Web Apps (FastAPI/Flask)*: `gunicorn app:app -k uvicorn.workers.UvicornWorker`
*   **Procfile**: Tạo file này nếu deploy lên các nền tảng giống Heroku.

## 4. Context Cho CI/CD
Khi tạo pipeline cho GitHub Actions hoặc GitLab CI:
*   **Quản Lý Secret**: KHÔNG BAO GIỜ hardcode API Key hoặc Credentials trong code. Hãy dùng `secrets.VNSTOCK_API_KEY`.
*   **Testing**: Chạy unit test trong môi trường container hóa (containerized environment) được thiết kế theo tiêu chuẩn Dockerization ở Mục 1.
