---
title: "04. Tiện ích cá nhân (Retail)"
nav_order: 5
parent: "Giao diện Hợp nhất (Unified UI)"
---

# Domain: Retail - Tiện ích Dân sinh & Ngoại tệ

Domain `Retail` cung cấp các thông tin thiết thực phục vụ nhu cầu theo dõi tài sản cá nhân như giá vàng và tỷ giá hối đoái ngân hàng.

---

## 1. Khởi tạo

```python
from vnstock.ui import Retail

ret = Retail()
```

---

## 2. Các phương thức chi tiết

### A. Phương thức `gold()` (Giá Vàng)

Truy xuất dữ liệu giá vàng trong nước từ các nguồn niêm yết chính thống.

-   **Cú pháp**: `gold(source='sjc', date=None)`
-   **Tham số**:
    -   `source`: `'sjc'` (Mặc định) hoặc `'btmc'` (Bảo Tín Minh Châu).
    -   `date`: Định dạng 'YYYY-MM-DD'. Nếu bỏ trống sẽ lấy giá mới nhất.
-   **Dữ liệu trả về (Schema)**:
    -   `time`: Thời gian cập nhật.
    -   `buy`: Giá mua vào.
    -   `sell`: Giá bán ra.
    -   `type`: Loại vàng (Vàng miếng, Vàng nhẫn...).

```python
# Lấy giá vàng Bảo Tín Minh Châu
btmc_gold = ret.gold(source='btmc')
print(btmc_gold)
```

---

### B. Phương thức `exchange_rate()` (Tỷ giá Ngoại tệ)

Theo dõi biến động tỷ giá ngoại hối trực tiếp từ ngân hàng Vietcombank (VCB).

-   **Cú pháp**: `exchange_rate(date='')`
-   **Tham số**:
    -   `date`: Định dạng 'YYYY-MM-DD'. Để trống để lấy tỷ giá hiện tại.
-   **Dữ liệu trả về (Schema)**:
    -   `currency`: Mã tiền tệ (USD, EUR, JPY...).
    -   `buy_cash`: Giá mua tiền mặt.
    -   `buy_transfer`: Giá mua chuyển khoản.
    -   `sell`: Giá bán ra.

```python
# Xem tỷ giá VCB hôm nay
fx = ret.exchange_rate()
print(fx.head())
```

---

## 3. Lưu ý về dữ liệu

-   Dữ liệu giá vàng và tỷ giá được lấy trực tiếp từ website của các đơn vị cung cấp (SJC, BTMC, VCB).
-   Tần suất cập nhật phụ thuộc vào nguồn tin gốc (thường là thời gian thực trong giờ hành chính).
-   Dữ liệu được trả về dưới dạng `pandas.DataFrame` chuẩn, giúp bạn dễ dàng tích hợp vào các bảng tính hoặc biểu đồ theo dõi cá nhân.
