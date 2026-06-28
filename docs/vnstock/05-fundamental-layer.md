---
title: "03. Phân tích Cơ bản (Fundamental)"
nav_order: 4
parent: "Giao diện Hợp nhất (Unified UI)"
---

# Domain: Fundamental - Phân tích Tài chính & Định giá

Domain `Fundamental` cung cấp bộ công cụ để truy xuất dữ liệu tài chính doanh nghiệp đã được chuẩn hóa, giúp bạn thực hiện phân tích cơ bản một cách nhanh chóng.

---

## 1. Khởi tạo

```python
from vnstock.ui import Fundamental

fun = Fundamental()
```

---

## 2. Các lớp và phương thức chi tiết

### A. Lớp `equity` (Cổ phiếu)

Truy xuất báo cáo tài chính và chỉ số định giá của các doanh nghiệp niêm yết.

| Phương thức | Tham số | Mô tả |
| :--- | :--- | :--- |
| **`income_statement()`**| `period='year', orient='report', **kwargs` | Kết quả kinh doanh. |
| **`balance_sheet()`** | `period='year', orient='report', **kwargs` | Bảng cân đối kế toán. |
| **`cash_flow()`** | `period='year', orient='report', **kwargs` | Lưu chuyển tiền tệ. |
| **`ratio()`** | `orient='report', **kwargs` | Các chỉ số tài chính (P/E, P/B, ROE...). |

---

## 3. Tham số nâng cao

### Tham số `period` (Kỳ báo cáo)
-   `'year'`: Báo cáo theo năm (Mặc định).
-   `'quarter'`: Báo cáo theo quý.

### Tham số `orient` (Định dạng kết quả)
Đây là tính năng độc đáo giúp bạn thay đổi cấu trúc DataFrame trả về để phù hợp với mục đích sử dụng:

-   **`'report'`** (Mặc định):
    -   Hàng (Rows): Các chỉ tiêu tài chính (Doanh thu, Lợi nhuận...).
    -   Cột (Columns): Các kỳ báo cáo (2023, 2022...).
    -   *Phù hợp để đọc và so sánh trực quan.*
-   **`'time_series'`**:
    -   Hàng (Rows): Các kỳ báo cáo.
    -   Cột (Columns): Các chỉ tiêu tài chính.
    -   *Phù hợp để vẽ biểu đồ hoặc chạy mô hình machine learning.*

```python
# Lấy báo cáo dưới dạng chuỗi thời gian để vẽ biểu đồ
df = fun.equity("VCB").income_statement(period='quarter', orient='time_series', limit=8)
```

---

## 4. Cấu trúc dữ liệu (Data Schema)

### Kết quả trả về của các báo cáo (`orient='report'`)
-   `item`: Tên chỉ tiêu tiếng Việt.
-   `item_en`: Tên chỉ tiêu tiếng Anh (nếu có).
-   `unit`: Đơn vị tính.
-   Các cột năm/quý (ví dụ: `2023`, `2022`...): Giá trị tương ứng.

### Các chỉ số tài chính (`ratio`)
Bao gồm hơn 50 chỉ số quan trọng, ví dụ:
-   `ticker`: Mã cổ phiếu.
-   `quarter` / `year`: Kỳ báo cáo.
-   `priceToEarning`: P/E.
-   `priceToBook`: P/B.
-   `roe`: Tỷ suất lợi nhuận trên vốn chủ sở hữu.
-   `roa`: Tỷ suất lợi nhuận trên tổng tài sản.

---

> [!TIP]
> Hệ thống tự động làm sạch dữ liệu như loại bỏ các hậu tố tên cột dư thừa (ví dụ: "-Năm") để đảm bảo DataFrame của bạn luôn sạch sẽ và sẵn sàng cho tính toán.
