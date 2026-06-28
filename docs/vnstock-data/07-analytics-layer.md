# Layer 7: Analytics (Phân Tích Định Giá)

> [!IMPORTANT]
> **Data Schema (Từ điển dữ liệu):** Để xem chính xác tên cột, kiểu dữ liệu (`Dtype`) và ý nghĩa (`Meaning`) của các DataFrame trả về từ layer này, vui lòng tham khảo [Data Schema](schema/04-analytics.md). KHÔNG được đoán mò tên cột khi viết code xử lý dữ liệu.

## 📌 Tổng Quan

**Analytics Layer** là một layer chuyên biệt cung cấp góc nhìn **định giá thị trường tổng quan** bao gồm biểu đồ P/E, P/B vĩ mô, và đánh giá sức khoẻ cho các rổ chỉ số chứng khoán. Đây là Layer được tách riêng từ mô đun Insights nhằm phục vụ độc lập cho mục tiêu đánh giá định giá rổ chứng khoán ở mức độ toàn cảnh trước khi nhà đầu tư đi sâu vào việc phân tích các mã lẻ.

## 🏗️ Cấu Trúc Domain

```python
Analytics()
└── .valuation(index)      # Định giá thị trường
    ├── .pe(duration)      # P/E ratio lịch sử
    ├── .pb(duration)      # P/B ratio lịch sử
    └── .evaluation(duration)  # Đánh giá tổng hợp P/E + P/B
```

## 📋 Chi Tiết

### Valuation Domain (Định Giá Thị Trường & Chỉ Số)

**Source:** VND  
**Registry Key:** `"insights.valuation"`  

#### Mô Tả

Cung cấp dữ liệu định giá chuẩn P/E, P/B trong quá khứ được tham chiếu theo các chỉ số thị trường vĩ mô (VNINDEX, HNX, UPCOM, v.v.) để phân tích mức độ đắt rẽ hiện tại so với bối cảnh lịch sử.

#### Khởi Tạo

```python
from vnstock_data import Analytics

ana = Analytics()
val = ana.valuation("VNINDEX")  # Cấu hình index mục tiêu (Mặc định: "VNINDEX")
```

#### Phương Thức

| Method         | Tham Số    | Mô Tả                         | Return    |
| -------------- | ---------- | ----------------------------- | --------- |
| `pe()`         | `duration` | P/E ratio lịch sử             | DataFrame |
| `pb()`         | `duration` | P/B ratio lịch sử             | DataFrame |
| `evaluation()` | `duration` | Đánh giá tổng hợp (P/E + P/B) | DataFrame |

**Parameters:**
- `index` (str) khi khởi tạo: Có thể chọn `"VNINDEX"`, `"HNX"`, `"VN30"`.
- `duration` (str) khi gọi method: Khoảng thời gian lịch sử cần lấy. Mặc định là `"5Y"`. Các giá trị tham chiếu: `"1Y"`, `"2Y"`, `"3Y"`, `"5Y"`.

#### Ví Dụ

```python
from vnstock_data import Analytics
ana = Analytics()

# ===== P/E Ratio Lịch Sử =====
# Lấy P/E VNINDEX 1 năm gần nhất
df_pe = ana.valuation("VNINDEX").pe(duration="1Y")
print(df_pe.tail())
# Output:
#                    pe
# reportDate
# 2025-03-11  13.22
# 2025-03-12  13.24

# P/E HNX 5 năm
df_pe_hnx = ana.valuation("HNX").pe(duration="5Y")

# ===== P/B Ratio Lịch Sử =====
df_pb = ana.valuation("VNINDEX").pb(duration="1Y")

# ===== Evaluation (Đánh Giá Tổng Hợp mức độ Đắt/Rẻ) =====
df_eval = ana.valuation("VNINDEX").evaluation(duration="5Y")
print(df_eval.head())
```

---

## 🔗 Registry Mapping Config

```python
INSIGHTS_SOURCES = {
    "insights.valuation": {
        "pe": ("vnd", "market", "Market", "pe"),
        "pb": ("vnd", "market", "Market", "pb"),
        "evaluation": ("vnd", "market", "Market", "evaluation"),
    }
}
```

---

## ⚠️ Lưu Ý Quan Trọng
1. **Migration từ Market Layer**: Nếu trước đây bạn dùng `Market().pe()` trong phiên bản cũ, thiết kế mới bắt buộc bạn di chuyển sang `Analytics().valuation(index).pe()`. Hàm cũ dù vẫn còn hoạt động có thể tung sẽ có cảnh báo deprecation warning.
2. **Default Arguments**: Luôn ưu tiên truyền Keyword argument thay vì Positional. (VD: `.pe(duration="5Y")`).
