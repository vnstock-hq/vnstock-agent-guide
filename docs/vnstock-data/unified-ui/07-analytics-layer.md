# Layer 7: Analytics (Phân Tích Định Giá)

## 📌 Tổng Quan

**Analytics Layer** cung cấp dữ liệu **định giá thị trường** bao gồm P/E, P/B, và đánh giá tổng quan cho các chỉ số thị trường. Layer này tách riêng từ Insights để tập trung vào phân tích chỉ số thị trường rộng.

## 🏗️ Cấu Trúc Domain

```python
Analytics()
└── .valuation(index)      # Định giá thị trường
    ├── .pe(duration)      # P/E ratio lịch sử
    ├── .pb(duration)      # P/B ratio lịch sử
    └── .evaluation(duration)  # Đánh giá tổng hợp
```

## 📋 Chi Tiết

### Valuation Domain (Định Giá Thị Trường)

**Source:** VND (vnd)  
**Registry Key:** `"insights.valuation"`

#### Mô Tả

Cung cấp dữ liệu P/E, P/B lịch sử theo chỉ số thị trường (VNINDEX, HNX, v.v.) để phân tích mức định giá hiện tại so với lịch sử.

#### Khởi Tạo

```python
from vnstock_data import Analytics

ana = Analytics()
val = ana.valuation("VNINDEX")  # Hoặc "HNX", "UPCOM"
```

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `pe()` | `duration` | P/E ratio lịch sử | DataFrame |
| `pb()` | `duration` | P/B ratio lịch sử | DataFrame |
| `evaluation()` | `duration` | Đánh giá tổng hợp (P/E + P/B) | DataFrame |

**Parameters:**
- `duration` (str): Khoảng thời gian lịch sử, mặc định `"5Y"`. Các giá trị: `"1Y"`, `"2Y"`, `"3Y"`, `"5Y"`.

#### Ví Dụ

```python
from vnstock_data import Analytics

ana = Analytics()

# ===== P/E Ratio Lịch Sử =====
# P/E VNINDEX 1 năm gần nhất
df_pe = ana.valuation("VNINDEX").pe(duration="1Y")
print(df_pe.head())
# Output:
#                    pe
# reportDate
# 2025-03-11  13.228029
# 2025-03-12  13.246481
# 2025-03-13  13.165441

# P/E HNX 5 năm
df_pe_hnx = ana.valuation("HNX").pe(duration="5Y")
print(df_pe_hnx.tail(5))

# ===== P/B Ratio Lịch Sử =====
df_pb = ana.valuation("VNINDEX").pb(duration="1Y")
print(df_pb.head())

# ===== Evaluation (Đánh Giá Tổng Hợp) =====
df_eval = ana.valuation("VNINDEX").evaluation(duration="5Y")
print(df_eval.head())
```

---

## 🔗 Registry Mapping

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

## 💡 Best Practices

### 1. So Sánh Định Giá Giữa Các Sàn

```python
from vnstock_data import Analytics

ana = Analytics()

# So sánh P/E giữa VNINDEX và HNX
pe_vn = ana.valuation("VNINDEX").pe(duration="1Y")
pe_hnx = ana.valuation("HNX").pe(duration="1Y")

print(f"VNINDEX PE hiện tại: {pe_vn['pe'].iloc[-1]:.2f}")
print(f"HNX PE hiện tại: {pe_hnx['pe'].iloc[-1]:.2f}")
```

### 2. Đánh Giá Mức Định Giá Hiện Tại

```python
from vnstock_data import Analytics

ana = Analytics()

# Lấy P/E 5 năm để so sánh
pe_5y = ana.valuation("VNINDEX").pe(duration="5Y")

# Tính trung bình và so sánh
pe_avg = pe_5y['pe'].mean()
pe_current = pe_5y['pe'].iloc[-1]

print(f"P/E hiện tại: {pe_current:.2f}")
print(f"P/E trung bình 5 năm: {pe_avg:.2f}")

if pe_current < pe_avg * 0.9:
    print("✓ Thị trường đang định giá thấp hơn trung bình")
elif pe_current > pe_avg * 1.1:
    print("⚠ Thị trường đang định giá cao hơn trung bình")
else:
    print("→ Thị trường quanh mức định giá trung bình")
```

---

## ⚠️ Lưu Ý Quan Trọng

1. **Migration từ Market**: Nếu trước đây bạn dùng `Market().pe()`, hãy chuyển sang `Analytics().valuation(index).pe()`. Cách cũ vẫn hoạt động nhưng sẽ hiển thị deprecation warning.
2. **Index parameter**: Luôn chỉ định `index` khi gọi `.valuation()`. Mặc định là `"VNINDEX"`.
3. **Duration**: Sử dụng `"1Y"`, `"2Y"`, `"3Y"`, hoặc `"5Y"`.

---

## 🚦 Next Steps

- **Insights Layer**: Để xem top cổ phiếu (ranking) và lọc (screener)
- **Market Layer**: Để lấy giá giao dịch thực tế  
- **Fundamental Layer**: Để phân tích cơ bản công ty
