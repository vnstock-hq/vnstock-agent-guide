---
title: "[Version] Migration Guide"
nav_order: 100
parent: "Migrations"
---

# Hướng Dẫn Chuyển Đổi Sang [Phiên bản đích] (Migration vX.Y.Z)

Bản cập nhật vX.Y.Z ([Ngày phát hành]) mang đến những thay đổi [Mô tả ngắn gọn về sự thay đổi, ví dụ: nâng cấp kiến trúc, tích hợp nguồn dữ liệu mới, loại bỏ hàm cũ...]. 
Tài liệu này hướng dẫn cách thay đổi cú pháp mã nguồn từ phiên bản cũ sang chuẩn mới.

## 📌 1. Tổng Quan Những Thay Đổi Lớn

> [!WARNING]
> **Breaking Changes**: Liệt kê ngắn gọn những thay đổi có thể làm hỏng code cũ của người dùng (ví dụ: tham số bị xoá, module bị đổi tên, hàm bị deprecate).

- **Điểm 1**: ...
- **Điểm 2**: ...

---

## 🔄 2. Bảng Chuyển Đổi API (Mapping)

Hướng dẫn AI Agent và người dùng ánh xạ từ các API cũ sang API mới. Phân chia thành các bảng theo Domain (nếu có nhiều thay đổi).

### [Tên Domain / Lớp] (Ví dụ: Insights & Analytics)

| Legacy API (Bản < X.Y.Z) | New API (Bản >= X.Y.Z) | Tình Trạng |
| :--- | :--- | :--- |
| `OldClass().old_method()` | `NewClass().new_method()` | Chuyển tiếp / Deprecated / Xoá bỏ |

---

## 📋 3. Chi Tiết Cập Nhật (Kèm Code Mẫu)

Mô tả sâu hơn về sự thay đổi, hướng dẫn truyền tham số mới, và đưa ra ví dụ Before/After trực quan.

### Thay đổi: [Tên thay đổi]

**Nguyên tắc chuyển đổi:**
1. [Bước 1]
2. [Bước 2]

**Cú pháp cũ (Bản < X.Y.Z):**
```python
# Ví dụ về cách dùng cũ
```

**Cú pháp mới (Bản >= X.Y.Z):**
```python
# Ví dụ về cách dùng mới
```

---

## 🚀 4. Lộ Trình Ngừng Hỗ Trợ (Deprecation Timeline)

> [!IMPORTANT]
> Lưu ý các mốc thời gian quan trọng nếu có API bị loại bỏ hoàn toàn trong các phiên bản sau.

| Tính năng cũ | Thay thế bằng | Hạn cuối (Deadline) |
| :--- | :--- | :--- |
| `old_method()` | `new_method()` | 31/12/2026 |
