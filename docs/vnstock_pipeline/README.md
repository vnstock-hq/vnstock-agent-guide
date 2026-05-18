# Vnstock Pipeline - Tài Liệu Hướng Dẫn

Chào mừng bạn đến với tài liệu hướng dẫn sử dụng thư viện **vnstock_pipeline**. Đây là công cụ chuyên nghiệp giúp bạn xây dựng các hệ thống thu thập, xử lý và xuất dữ liệu chứng khoán tự động theo mô hình chuẩn hóa: **Fetcher → Validator → Transformer → Exporter**.

---

## 🚀 Bắt Đầu Nhanh

**Cài đặt:**

```bash
pip install -U vnstock_pipeline
```

**Sử dụng cơ bản (Tải dữ liệu giá EOD):**

```python
from vnstock_pipeline.tasks.ohlcv import run_task

# Tải dữ liệu và tự động lưu ra file CSV theo chuẩn thư mục
run_task(['VCB', 'FPT', 'HPG'], start="2024-01-01", end="2024-12-31")
print("✅ Dữ liệu đã lưu thành công vào thư mục ./data/ohlcv/")
```

---

## 📑 Mục Lục Tài Liệu

Bộ tài liệu này đã được tinh chỉnh (Agent-Ready) để hỗ trợ bạn đi từ mức độ làm quen cơ bản đến việc vận hành hệ thống dữ liệu thực tế:

1. **[Tổng Quan Kiến Trúc & Luồng Xử Lý](01-overview.md)**
   Cái nhìn toàn cảnh về kiến trúc lõi và triết lý thiết kế của thư viện.
1. **[Các Tác Vụ Sẵn Có (Tasks) & Cách Xây Dựng (Builders)](02-tasks-and-builders.md)**
   Hướng dẫn chi tiết chạy 4 loại dữ liệu chính: Giá OHLCV, Báo cáo tài chính, Dữ liệu Intraday và Bảng giá trực tuyến (Price Board).
1. **[Các Mẫu Thiết Kế Pipeline Tùy Chỉnh (Custom Pipelines)](03-custom-pipelines.md)**
   Hướng dẫn tự viết code kế thừa các lớp `VNFetcher`, `VNValidator`, `VNTransformer`, và `Exporter` để nhúng logic nghiệp vụ riêng (VD: làm giàu chỉ báo kỹ thuật, lọc dữ liệu).
1. **[Luồng Dữ Liệu Thời Gian Thực (Streaming)](04-streaming.md)**
   *(Đặc quyền gói Golden/Diamond)* Hướng dẫn kiến trúc Streaming, giới thiệu cấu trúc bộ code mẫu độc quyền tích hợp Redis, Discord Webhook và xử lý tín hiệu.
1. **[Kinh Nghiệm Vận Hành (Best Practices & CLI)](05-best-practices.md)**
   Bí quyết cấu hình `Scheduler` tối ưu (tránh Rate Limit), lập lịch chạy nền, và hướng dẫn sử dụng công cụ kiểm tra dữ liệu **Data Inspection CLI**.
1. **[Tiêu Chuẩn Cấu Trúc Dữ Liệu Streaming (Schemas)](07-streaming-data-schemas.md)**
   Từ điển tham chiếu (Dictionary) toàn bộ các trường dữ liệu trả về từ kết nối WebSocket (Chuẩn hoá theo FIX/Bloomberg-aligned).
1. **[Hướng Dẫn Nâng Cấp (Migration Guide)](08-streaming-migration-guide.md)**
   Hướng dẫn chuyển đổi code an toàn từ phiên bản cũ (v2.2.1 trở xuống) lên cấu trúc dữ liệu tiêu chuẩn (v2.2.2+).

---

## 🔗 Liên Kết Hệ Sinh Thái

Để phát huy tối đa sức mạnh, hãy kết hợp `vnstock_pipeline` với các module khác:

- **vnstock_data**: [Tài liệu Data Wrapper](../vnstock-data/)
- **vnstock_ta**: [Tài liệu Phân Tích Kỹ Thuật](../vnstock_ta/)

---

*Phiên bản tài liệu: 2.2.2+ | Cập nhật: 19/05/2026*