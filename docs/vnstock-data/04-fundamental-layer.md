# Layer 3: Fundamental Data (Dữ Liệu Cơ Bản)

> [!IMPORTANT]
> **Data Schema (Từ điển dữ liệu):** Để xem chính xác tên cột, kiểu dữ liệu (`Dtype`) và ý nghĩa (`Meaning`) của các DataFrame trả về từ layer này, vui lòng tham khảo [Data Schema](schema/03-fundamental.md). KHÔNG được đoán mò tên cột khi viết code xử lý dữ liệu.

## 📌 Tổng Quan

**Fundamental Layer** cung cấp dữ liệu **báo cáo tài chính** (BCTC) và **tỷ số tài chính** phục vụ cho phân tích cơ bản của doanh nghiệp. Ở phương thức nâng cao, hệ thống trang bị tính năng **quy chuẩn hoá (Force scorecard)** giúp định hình ma trận tài chính cực mạnh cho các mô hình AI dự báo.

Bao gồm Báo cáo kết quả kinh doanh, Bảng cân đối kế toán, Lưu chuyển tiền tệ, Tỷ số tài chính, Thuyết minh BCTC và Báo cáo sức khỏe tài chính tổng hợp (Auto Scorecard).

## 🏗️ Cấu Trúc Domain

Mô đun Fundamental hỗ trợ 2 dạng cú pháp linh hoạt (Proxy chaining):
1. **Dạng hướng đối tượng (Object Oriented):** `fun.equity("TCB").cash_flow()`
2. **Dạng hàm tiện ích (Utility Function):** `fun.equity.cash_flow("TCB")`

```python
Fundamental()
└── .equity                  # Dữ liệu tài chính chứng khoán (Cổ phiếu)
    ├── .income_statement()  # Báo cáo kết quả kinh doanh
    ├── .balance_sheet()     # Cân đối kế toán
    ├── .cash_flow()         # Lưu chuyển tiền tệ
    ├── .ratio()             # Tỷ số tài chính
    ├── .note()              # Thuyết minh cơ cấu BCTC
    ├── .filing()            # Hồ sơ & Tài liệu BCTC (PDF)
    └── .financial_health()  # Báo cáo hợp nhất với Auto Scorecard
```

## 📋 Chi Tiết Các Phương Thức

### 1. Income Statement (Báo Cáo Kết Quả Kinh Doanh)

**Source:** MAS  
**Registry Key:** `"equity.fundamental.income_statement"`  
**Tham số:**
- `period` (`str`): Kỳ báo cáo (`'year'` cho năm, `'quarter'` cho quý).
- `lang` (`str`): Ngôn ngữ (`'vi'` hoặc `'en'`). Mặc định `'vi'`.
- `dropna` (`bool`): Xoá các trường bị rỗng. Mặc định `True`.

**Ví Dụ:**
```python
from vnstock_data import Fundamental
fun = Fundamental()

# Báo cáo kết quả kinh doanh
df_income = fun.equity("TCB").income_statement(period="year")
```

---

### 2. Balance Sheet (Cân Đối Kế Toán)

**Source:** MAS  
**Registry Key:** `"equity.fundamental.balance_sheet"`  
**Tham số:** Tương tự `income_statement` (`period`, `lang`, `dropna`).

**Ví Dụ:**
```python
# Cân đối kế toán
df_bs = fun.equity.balance_sheet("VIC", period="quarter")
```

---

### 3. Cash Flow (Lưu Chuyển Tiền Tệ)

**Source:** MAS  
**Registry Key:** `"equity.fundamental.cash_flow"`  
**Tham số:** Tương tự `income_statement`.

**Ví Dụ:**
```python
df_cf = fun.equity("VNM").cash_flow(period="year")
```

---

### 4. Financial Ratio (Tỷ Số Tài Chính)

**Source:** MAS  
**Registry Key:** `"equity.fundamental.ratio"`  
**Tham số:** Tương tự `income_statement`.

Chứa các tỷ số quan trọng như PE, PB, ROE, Debt/Equity.  

**Ví Dụ:**
```python
df_ratio = fun.equity("HPG").ratio(period="quarter")
```

---

### 5. Note (Thuyết Minh BCTC)

**Source:** VCI  
**Registry Key:** `"equity.fundamental.note"`  
**Tham số:**
- `period` (`str`, optional): Kỳ báo cáo.
- `lang` (`str`): Ngôn ngữ (`'en'` hoặc `'vi'`). Mặc định `'en'`.
- `mode` (`str`): Trạng thái bản báo cáo (mặc định `'final'`).
- `style` (`str`): Cấu trúc format dữ liệu, mặc định `'readable'` cho định dạng dễ đọc.
- `get_all` (`bool`): Lấy toàn bộ hay không. Mặc định `False`.
- `dropna` (`bool`): Xóa trường rỗng. Mặc định `True`.

Trích xuất tự động các thuyết minh con/ghi chú chi tiết đính kèm trên báo cáo tài chính hàng quý.

**Ví Dụ:**
```python
df_note = fun.equity("FPT").note(period="year", lang="vi")
```

---

### 6. Filing (Hồ Sơ & Tài Liệu PDF)

**Source:** MBK  
**Registry Key:** `"equity.fundamental.filing"`  
**Tham số:**
- `doc_type` (`str`, optional): Phân loại tài liệu muốn lấy. Mặc định `None` (lấy tất cả). Các tuỳ chọn hợp lệ bao gồm:
  - `'financial_report'`: Báo cáo tài chính
  - `'annual_report'`: Báo cáo thường niên
  - `'prospectus'`: Bản cáo bạch
  - `'shareholder_resolution'`: Nghị quyết HĐCĐ
  - `'shareholder_material'`: Tài liệu HĐCĐ
  - `'business_explanation'`: Giải trình KQKD
  - `'management_report'`: Báo cáo tình hình quản trị
  - `'capital_adequacy'`: Báo cáo tỷ lệ an toàn vốn
  - `'board_resolution'`: Nghị quyết HĐQT
  - `'capital_safety'`: Tỷ lệ an toàn tài chính
  - `'other'`: Khác

Cung cấp đường dẫn tải trực tiếp đến các bản cáo bạch, báo cáo thường niên, file PDF BCTC.

**Ví Dụ:**
```python
df_filing = fun.equity("TCB").filing()
```

---

### 7. Financial Health (Bảng Tổng Hợp Scorecard)

**Từ Vnstock 3.1.0, hàm này được trang bị nhằm đáp ứng nhu cầu khắt khe của Quant Trading và AI Model:**
Thay vì để phơi nhiễm cấu trúc JSON thô tuỳ thích của nguồn cấp, `financial_health` sẽ:
- Dò tìm mã ngành ICB tự động (qua `Reference` layer).
- **Ép buộc (force)** dữ liệu tài chính đi qua **Scorecard** (Ngân hàng, CK, Bảo hiểm, chung...).
- Chỉ cho phép lọt qua các fields có trong thẻ Scorecard (các cấu trúc rác bị loại bỏ hoàn toàn).
- Nối BCTC theo phương ngang dựa vào index là `period`.
- Áp `lang="vi"` để ánh xạ ra giao diện Terminal TCBS.

**Tham số bổ sung:**
- `scorecard`: `"auto"`, `"banking"`, `"securities"`, `"insurance"`, `"generic"`
- `reports`: List các loại báo cáo muốn hợp nhất (Mặc định: cả 4 fundamental reports).

**Ví Dụ:**
```python
# 1. Tự động phát hiện Chứng khoán và lấy scorecard VI
df_ssi = fun.equity("SSI").financial_health(scorecard="auto", lang="vi", limit=4)

# 2. Ép sử dụng Scorecard Ngân hàng với chuẩn EN
df_tcb = fun.equity("TCB").financial_health(scorecard="banking", lang="en", limit=4)
```

---

## 🔗 Registry Mapping Config

```python
FUNDAMENTAL_SOURCES = {
    "equity.fundamental": {
        "income_statement": ("mas", "financial", "Finance", "income_statement"),
        "balance_sheet":    ("mas", "financial", "Finance", "balance_sheet"),
        "cash_flow":        ("mas", "financial", "Finance", "cash_flow"),
        "ratio":            ("mas", "financial", "Finance", "ratio"),
        "note":             ("vci", "financial", "Finance", "note"),
        "filing":           ("mbk", "financial", "Finance", "document")
    }
}
```

## ⚠️ Lưu Ý Quan Trọng
1. **Tần Suất Update**: BCTC được công bố cuối mỗi kỳ, không có realtime.
2. **Khoảng Trống**: Một số doanh nghiệp có thể che dấu field hoặc không phát sinh nghiệp vụ, khi rập scorecard sẽ tự quy thành `NaN` chống gãy logic.
3. **Múc Tiền Tệ**: Mặc định là VND trừ phi có scale format tại tầng ứng dụng.

## 🚦 Next Steps
- **Market Layer**: Để lấy giá hiện tại và lịch sử giao dịch so kè PE, PB.
- **Insights Layer**: Gửi bảng financial_health cho các model phân tích tín hiệu.
