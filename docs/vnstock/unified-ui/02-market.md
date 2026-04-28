---
title: "02. Dữ liệu Thị trường (Market)"
nav_order: 3
parent: "Giao diện Hợp nhất (Unified UI)"
---

# Domain: Market - Dữ liệu Giao dịch Trực tuyến & Lịch sử

Domain `Market` tập trung vào các dữ liệu biến động của thị trường theo thời gian thực và dữ liệu lịch sử cho nhiều loại tài sản khác nhau.

---

## 1. Khởi tạo

```python
from vnstock.ui import Market

mkt = Market()
```

---

## 2. Các lớp và phương thức chi tiết

### A. Lớp `equity` (Cổ phiếu)

| Phương thức | Tham số | Mô tả |
| :--- | :--- | :--- |
| **`ohlcv()`** | `start, end, resolution='1D', count=100, source='kbs'` | Lấy dữ liệu nến (Mở, Cao, Thấp, Đóng, Khối lượng). |
| **`trades()`** | `source='kbs'` | Dữ liệu khớp lệnh chi tiết trong ngày (Tick-by-tick). |
| **`quote()`** | `source='kbs'` | Lấy thông tin giá hiện tại (Bảng giá). |

**Tham số chính của `ohlcv`:**
- `start / end`: Định dạng 'YYYY-MM-DD'.
- `resolution`: Khung thời gian (Bản Free chủ yếu hỗ trợ '1D').
- `count`: Số lượng nến cần lấy nếu không chỉ định `start`.

**Dữ liệu mẫu (`ohlcv`):**
| time | open | high | low | close | volume |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2024-01-02 07:00:00 | 55.05 | 55.52 | 54.59 | 55.45 | 1785800 |
| 2024-01-03 07:00:00 | 55.45 | 56.12 | 54.99 | 56.12 | 1373000 |

---

### B. Lớp `index` (Chỉ số)

Truy xuất biến động của các bộ chỉ số thị trường (VNINDEX, VN30...).

| Phương thức | Tham số | Mô tả |
| :--- | :--- | :--- |
| **`ohlcv()`** | `start, end, resolution='1D', count=100, source='kbs'` | Biểu đồ giá của chỉ số. |

```python
# Lấy dữ liệu VNINDEX
vnindex = mkt.index("VNINDEX").ohlcv(start="2024-01-01", end="2024-01-31")
```

---

### C. Dữ liệu Tài sản Quốc tế & Khác

Sử dụng nguồn dữ liệu MSN và FMarket để theo dõi các thị trường khác.

| Lớp | Phương thức | Mô tả |
| :--- | :--- | :--- |
| **`forex`** | `ohlcv()` | Tỷ giá ngoại hối (ví dụ: "USDVND"). |
| **`crypto`**| `ohlcv()` | Giá tiền điện tử (ví dụ: "BTC"). |
| **`commodity`**| `ohlcv()` | Giá hàng hóa (ví dụ: "Gold"). |
| **`fund`** | `history() / nav()` | Lịch sử giá NAV của quỹ mở. |
| **`etf`** | `ohlcv() / quote() / trades()` | Dữ liệu giao dịch chứng chỉ quỹ ETF. |
| **`futures`**| `ohlcv() / quote() / trades()` | Dữ liệu hợp đồng tương lai. |
| **`warrant`**| `ohlcv() / quote() / trades()` | Dữ liệu chứng quyền có bảo đảm. |

---

## 3. Lấy Bảng giá Nhanh

Bạn có thể lấy giá hiện tại cho một hoặc nhiều mã cùng lúc mà không cần thông qua các lớp tài sản.

```python
# Lấy giá của một mã
price_vcb = mkt.quote("VCB")

# Lấy giá của danh mục
prices = mkt.quote(["VCB", "HPG", "FPT"])
```

> [!NOTE]
> Các phương thức trong domain Market được thiết kế để tối ưu hóa việc lấy dữ liệu hàng loạt. Nếu bạn cần dữ liệu với tần suất cực cao cho mục đích giao dịch thuật toán (Algo Trading), vui lòng tham khảo các gói nâng cấp tại tài liệu **So sánh Miễn phí vs Tài trợ**.
