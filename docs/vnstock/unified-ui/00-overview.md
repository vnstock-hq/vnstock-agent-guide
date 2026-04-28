---
title: "00. Tổng quan & Khởi tạo"
nav_order: 1
parent: "Giao diện Hợp nhất (Unified UI)"
---

# Unified UI: Kiến trúc & Khởi tạo

Giao diện Hợp nhất (Unified UI) là trái tim của Vnstock v4.0+, mang đến khả năng truy cập dữ liệu mạnh mẽ thông qua cấu trúc phân tầng rõ rệt. Tài liệu này sẽ hướng dẫn bạn cách thiết lập môi trường và làm quen với các khái niệm cốt lõi.

---

## 1. Triết lý thiết kế: Domain-Driven API

Unified UI chia các tính năng của Vnstock thành các **Domain** (Miền chức năng) chuyên biệt:

- **`Reference`**: Lưu trữ các thông tin tĩnh, danh mục cổ phiếu, chỉ số và cấu trúc ngành.
- **`Market`**: Tập trung vào dữ liệu động, giá giao dịch, khối lượng và biểu đồ.
- **`Fundamental`**: Chuyên về dữ liệu tài chính, báo cáo và các chỉ số sức khỏe doanh nghiệp.
- **`Retail`**: Cung cấp các dữ liệu dân sinh như vàng và ngoại tệ.

Mỗi Domain được thiết kế để hoạt động độc lập nhưng vẫn có thể kết hợp mượt mà trong các luồng xử lý phức tạp.

---

## 2. Cài đặt

Để sử dụng Unified UI, bạn cần cài đặt phiên bản Vnstock mới nhất (ưu tiên bản từ GitHub để có các tính năng cập nhật nhất):

```bash
# Cài đặt bản ổn định
pip install -U vnstock

# HOẶC Cài đặt bản mới nhất từ GitHub
pip install git+https://github.com/thinh-vu/vnstock
```

---

## 3. Khởi tạo & Sử dụng

Cách sử dụng Unified UI rất đơn giản thông qua việc import các Class đại diện cho Domain từ `vnstock.ui`.

### Ví dụ cơ bản:

```python
from vnstock.ui import Reference, Market, Fundamental

# 1. Khởi tạo các Domain
ref = Reference()
mkt = Market()
fun = Fundamental()

# 2. Sử dụng (Ví dụ: Lấy danh sách cổ phiếu VN30)
vn30 = ref.index.members("VN30")
print(vn30.head())
```

---

## 4. Khám phá API thông qua `show_api()`

Một trong những tính năng mạnh mẽ nhất của Unified UI là khả năng tự giới thiệu. Bạn không cần phải nhớ hết các câu lệnh, chỉ cần gọi `show_api()` để xem toàn bộ cấu trúc:

```python
from vnstock.ui import show_api

show_api()
```

**Kết quả mẫu:**

```text
vnstock (UI Layer)
├── Reference # Tra cứu thông tin tĩnh & danh mục.
│   ├── company # Thông tin doanh nghiệp (KBS).
│   ├── equity # Danh sách cổ phiếu (KBS/VCI).
│   ├── index # Chỉ số thị trường (KBS).
│   └── ...
├── Market # Dữ liệu thị trường (Giá & Khớp lệnh).
│   ├── equity(symbol) # Dữ liệu cổ phiếu.
│   ├── index(symbol) # Dữ liệu chỉ số.
│   └── ...
└── ...
```

---

## 5. Tra cứu chi tiết với `show_doc()`

Nếu bạn muốn biết chi tiết về một phương thức cụ thể (tham số, kiểu dữ liệu trả về), hãy sử dụng `show_doc()`:

```python
from vnstock.ui import show_doc

# Xem hướng dẫn cho phương thức lấy giá lịch sử
show_doc("Market.equity")
```

---

> [!NOTE]
>
> Unified UI trong phiên bản `vnstock` Community (Miễn phí) được thiết kế để tương thích hoàn toàn về mặt cú pháp với phiên bản `vnstock_data` (Sponsor). Điều này cho phép bạn chuyển đổi sang sử dụng thư viện vnstock_data trong gói tài trợ mà không cần sửa đổi mã nguồn phức tạp - chỉ đơn giản là đổi tên thư viện trong lệnh `import`.