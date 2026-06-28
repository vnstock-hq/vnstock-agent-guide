# Finance - Báo Cáo Tài Chính & Chỉ Số

Module `Finance` cung cấp khả năng truy xuất dữ liệu báo cáo tài chính (BCTC) từ nhiều nguồn, bao gồm:
*   **VCI** (Vietcap): Dữ liệu chi tiết, hỗ trợ cả Thuyết minh BCTC. (Dạng Long-form: Dòng là kỳ, Cột là chỉ tiêu).
*   **MAS** (Mirae Asset): Hỗ trợ Kế hoạch kinh doanh năm. (Dạng Long-form).
*   **KBS** (KB Securities): Dữ liệu trình bày dạng bảng ngang (Dạng Wide-form: Dòng là chỉ tiêu, Cột là kỳ). 

Nguồn KBS và MAS giữ nguyên cấu trúc phân cấp cho báo cáo tài chính phổ biến, tiện cho phân tích thô. Trong khi đó VCI trình bày dữ liệu dạng chỉ tiêu, có thể chuẩn hoá để tiện lưu trữ cơ sở dữ liệu nhưng phá vỡ cấu trúc phân cấp.

## Tổng Quan & So Sánh

| Tính năng | VCI (Mới) | VCI (Cũ/Legacy) | MAS | KBS |
| :--- | :---: | :---: | :---: | :---: |
| **Dạng dữ liệu** | Long-form | Long-form | Long-form | **Wide-form** |
| **Income Statement** | ✅ | ✅ | ✅ | ✅ |
| **Balance Sheet** | ✅ | ✅ | ✅ | ✅ |
| **Cash Flow** | ✅ | ✅ | ✅ | ✅ |
| **Ratio** | ✅ (Rất chi tiết) | ✅ | ✅ (Cơ bản) | ✅ |
| **Thuyết Minh (Note)** | ✅ | ❌ | ❌ | ❌ |
| **Kế Hoạch (Plan)** | ❌ | ❌ | ✅ | ❌ |

---

## 1. Khởi Tạo

```python
from vnstock_data import Finance

# Nguồn VCI (Mặc định & Khuyên dùng)
finance = Finance(source='VCI', symbol='TCB')

# Nguồn MAS
finance_mas = Finance(source='MAS', symbol='TCB')

# Nguồn KBS
finance_kbs = Finance(source='KBS', symbol='TCB')

# Nguồn VCI Legacy (Dành cho code cũ chưa migration)
from vnstock_data.explorer.vci.financial_old import Finance as FinanceLegacy
finance_old = FinanceLegacy(symbol='TCB')
```

---

## 2. Nguồn VCI (Vietcap)

Trả về dữ liệu dạng **Long-form** (mỗi dòng là một kỳ báo cáo).
Mặc định tên cột Tiếng Anh (`lang='en'`) và dễ đọc (`style='readable'`).

### Các hàm hỗ trợ

| Hàm | Mô tả | Tham số chính |
| :--- | :--- | :--- |
| `income_statement()` | Kết quả kinh doanh | `period`, `lang`, `get_all` |
| `balance_sheet()` | Cân đối kế toán | `period`, `lang` |
| `cash_flow()` | Lưu chuyển tiền tệ | `period`, `lang` |
| `ratio()` | Chỉ số tài chính | `period`, `lang` |
| `note()` | Thuyết minh BCTC | `period`, `lang` |

### Ví dụ sử dụng

```python
# Lấy Báo cáo Kết quả kinh doanh theo Quý
df = finance.income_statement(period='quarter', lang='vi')

# Lấy Thuyết minh BCTC (Chỉ có ở VCI)
df_note = finance.note(period='quarter', lang='en')
```

**Cấu trúc dữ liệu trả về (VCI):**
*   `report_period`: Kỳ báo cáo (VD: `2024-Q3`)
*   `ticker`: Mã chứng khoán
*   Các cột chỉ tiêu: Tên cột là tên chỉ tiêu (VD: `Doanh thu thuần`, `Net Revenue`)

---

## 3. Nguồn KBS (KB Securities)

Trả về dữ liệu dạng **Wide-form** (mỗi dòng là một chỉ tiêu, các cột là các kỳ báo cáo `2024-Q1`, `2024-Q2`...).
Đây là định dạng thường thấy khi xem bảng so sánh trên web.

### Các hàm hỗ trợ

| Hàm | Mô tả | Tham số chính |
| :--- | :--- | :--- |
| `income_statement()` | Kết quả kinh doanh | `period` ('year'/'quarter'), `limit` (số kỳ) |
| `balance_sheet()` | Cân đối kế toán | `period`, `limit` |
| `cash_flow()` | Lưu chuyển tiền tệ | `period`, `limit` |
| `ratio()` | Chỉ số tài chính | `period`, `limit` |

### Ví dụ sử dụng

```python
# Lấy 8 quý gần nhất
df = finance_kbs.income_statement(period='quarter', limit=8)
```

**Cấu trúc dữ liệu trả về (KBS):**
*   `item`: Tên chỉ tiêu (VD: `Doanh thu thuần`)
*   `item_id`: Mã định danh chỉ tiêu (chuẩn hóa snake_case)
*   `2024-Q4`, `2024-Q3`...: Các cột giá trị theo kỳ.

---

## 4. Nguồn MAS (Mirae Asset)

Trả về dữ liệu dạng **Long-form**. Đặc biệt hỗ trợ **Kế hoạch kinh doanh**.

### Các hàm hỗ trợ

| Hàm | Mô tả |
| :--- | :--- |
| `annual_plan()` | Kế hoạch kinh doanh năm (Lợi nhuận, Cổ tức...) |
| `income_statement()`, `balance_sheet()`, `cash_flow()`, `ratio()` | Các báo cáo cơ bản |

### Ví dụ sử dụng

```python
# Lấy kế hoạch năm
df = finance_mas.annual_plan()
# Cột: period, Lợi nhuận trước thuế kế hoạch, ...
```

---

## 5. VCI Legacy (Hỗ trợ tương thích ngược)

Module dành cho người dùng quen với cấu trúc API cũ của `vnstock`.
Chỉ nên sử dụng khi chưa kịp nâng cấp code, vì module VCI mới (`source='VCI'`) tối ưu hơn và hỗ trợ nhiều tính năng hơn (như `note`).

```python
from vnstock_data.explorer.vci.financial_old import Finance as FinanceLegacy

f = FinanceLegacy(symbol='TCB', period='quarter')
df = f.ratio()
```

**Lưu ý**: Hàm `ratio()` của Legacy có thể trả về MultiIndex columns. Bạn có thể cần xử lý `flatten_columns=True` nếu muốn xuất ra Excel phẳng.

---

## Tham số chung thường gặp

*   `source`: Nguồn dữ liệu ('VCI', 'KBS', 'MAS').
*   `symbol`: Mã chứng khoán.
*   `period`: Kỳ báo cáo (`'quarter'` - Quý, `'year'` - Năm).
*   `lang`: Ngôn ngữ (`'vi'` - Tiếng Việt, `'en'` - Tiếng Anh). *Lưu ý: KBS không hỗ trợ tham số này, tên cột được lấy theo cấu hình mặc định*.
