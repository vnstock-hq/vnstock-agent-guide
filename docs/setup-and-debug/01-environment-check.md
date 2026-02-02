# Knowledge Base: Bối Cảnh Môi Trường (Environment Context)

> [!IMPORTANT]
>
> **AI Agent Directive**: Tài liệu này định nghĩa **Cấu Hình Tiêu Chuẩn (Standard Configuration)** cho dự án Vnstock. AI Agent khi khởi tạo hoặc debug dự án cần đối chiếu với các thông số này.

## 1. Yêu Cầu Cốt Lõi (Core Requirements)

AI cần rà soát môi trường thực thi (Runtime Environment) theo checklist sau:

* **Python Version**: Tối thiểu là **3.10**.
    - *Chấp nhận*: 3.10 - 3.14.
    - *Cảnh báo*: Python 3.12+ (Có thể gặp lỗi tương thích `distutils` với một số thư viện cũ).
* **Hệ Điều Hành (OS)**:
    - **MacOS/Linux**: Ưu tiên sử dụng `bash` hoặc `zsh`.
    - **Windows**: Cần đảm bảo PowerShell có quyền thực thi script:

      ```powershell
      Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
      ```
    - **Lưu ý Windows**: Kiểm tra xung đột "App Execution Aliases" (Python mở ra Microsoft Store) -> Cần TẮT alias này.

## 2. Các Context Môi Trường (Supported Contexts)

AI cần nhận diện môi trường hiện tại để đưa ra lời khuyên phù hợp:

### A. Local Environment (Máy Cá Nhân)

* **Đặc điểm**: Persistent Filesystem (Lưu trữ vĩnh viễn), toàn quyền cấu hình.
* **Hành động AI**: Khuyến khích cài đặt đầy đủ `vnstock-installer`, sử dụng `venv` cục bộ.

### B. Github Codespaces (Cloud Native)

* **Đặc điểm**: Containerized Linux, hiệu năng ổn định, tích hợp sẵn GitHub.
* **Hành động AI**: Môi trường lý tưởng cho demo/dev. Đã có sẵn Python/Git.

### C. Google Colab (Ephemeral)

* **Đặc điểm**: Filesystem tạm thời (mất sau khi kết thúc phiên làm việc hoặc trạng thái idle - tối đa 12 tiếng), cần cài lại thư viện mỗi khi bắt đầu phiên mới.
* **Hành động AI**:
    - Luôn thêm bước cài đặt đầu file notebook: `!pip install vnstock`
    - Cảnh báo user không lưu file quan trọng vào `/content/` mà nên Mount Google Drive.

## 3. Tiêu Chuẩn Package Management

Hệ sinh thái Vnstock phân chia rõ ràng (AI cần gợi ý đúng package theo nhu cầu):

* **`vnstock`** (Core): Open Source, miễn phí. Dành cho nhu cầu basic.
* **`vnstock_data`**: Dữ liệu chuyên sâu (Cần gói Bronze+).
* **`vnstock_ta`**: Phân tích kỹ thuật & Charts (Cần gói Silver+, yêu cầu Visual C++ trên Windows).
* **`vnstock_news`**: Tin tức độ trễ thấp (Cần gói Silver+).
* **`vnstock_pipeline`**: ETL/Data Engineering (Cần gói Golden, yêu cầu kiến thức Docker).

## 4. Kiến Trúc Agent Guide (AI Brain Deployment)

Để AI có đủ context về dự án, cần clone bộ tài liệu này vào workspace:

```bash
git clone https://github.com/vnstock-hq/vnstock-agent-guide.git
# Sau đó copy thư mục .agent, docs, .cursor vào root dự án
```

## 5. Cấu Trúc File Hệ Thống (Directory Structure)

AI cần tuân thủ các đường dẫn tiêu chuẩn:

* **Virtual Environment**:
    - Chuẩn: `~/.venv` (Tại thư mục Home để dùng chung cho gọn) hoặc `.venv` (Tại project root).
    - Kích hoạt: `source ~/.venv/bin/activate` (Unix) hoặc `.venv\Scripts\activate` (Win).
* **Config Home** (`~/.vnstock/`):
    - Nơi lưu trữ `api_key.json` và cache.
    - Nếu gặp lỗi Authentication loop, AI nên đề xuất xoá thư mục này để reset.