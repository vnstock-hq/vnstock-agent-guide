---
title: "02. Unified UI: Institutional Data & Standardized Scorecards"
nav_order: 2
parent: "Vnstock Data"
---

# Unified UI - Institutional Financial Scorecards (v3.1.0)

*(Ngày phát hành: 12/04/2026)*

Bắt đầu từ phiên bản **3.1.0**, Vnstock ra mắt cơ chế **Institutional Scorecard (Bộ Tiêu Chí Tổ Chức)** thông qua lớp giao diện `Unified UI`. Mục tiêu của kiến trúc này là cố định và tiêu chuẩn hóa các mô hình báo cáo tài chính trả về từ các nguồn dữ liệu (như MAS/KBS) thành các mẫu tiêu chuẩn tĩnh (Static Blueprint) dựa trên chuẩn mực phân tích chuyên nghiệp lấy cảm hứng từ hệ thống TCBS.

Hệ thống được thiết kế nhằm giải quyết bài toán: **Loại bỏ rủi ro vỡ cấu trúc dữ liệu** do nguồn dữ liệu bất ngờ bị thay đổi, trả về các giá trị trường thông tin không thể chuẩn hoá, hoặc khác biệt hoàn toàn cấu trúc báo cáo giữa các nhóm ngành (Ngân hàng, Chứng khoán, Bảo hiểm, Công ty chung).

---

## 1. Cơ Chế Hoạt Động (Architecture)

Hệ thống Scorecard hoạt động như một màng lọc dữ liệu 3 lớp chặt chẽ (Compact Core Schema):

1. **Extraction (Trích xuất nguyên bản):** Dữ liệu được fetch từ API của Provider (`MAS`/`KBS`) dưới dạng Raw Array chứa đầy đủ các phân nhóm báo cáo tài chính thô.
2. **Standardization Mapping (Bản đồ Dịch thuật Literal):** Thuật toán đối chiếu các cụm từ tĩnh có khả năng sai biệt giữa các công ty (Ví dụ: `TỔNG CỘNG TÀI SẢN` đối với Doanh nghiệp sản xuất, nhưng lại là `TÀI SẢN` đối với công ty chứng khoán) để dịch về định danh duy nhất như.
3. **Rigid Scorecard Filter (Bộ lọc phân ngành):** Khi phân ngành `scorecard="auto"` được kích hoạt, hệ thống sẽ gọi `SIC` lookup để tìm ra loại hình kinh doanh (Banking, Securities, Insurance, Generic). Dựa vào nhóm ngành, một nhóm gồm ~31 chỉ tiêu cốt lõi sẽ được áp dụng làm Mask để cắt bỏ mọi dữ liệu thứ cấp (như các loại quỹ con, chi phí trả trước không quan trọng), nhằm duy trì cấu trúc cố định tuyệt đối.
4. **Horizontal Aggregation (Gộp báo cáo diện rộng):** Method `financial_health()` hợp nhất Cân đối kể toán (Balance Sheet), KQ Kinh Doanh (Income Statement), Lưu chuyển tiền tệ (Cash Flow) và Tỉ lệ Tài chính (Ratio) vào cùng một DataFrame nằm ngang, căn dóng chính xác theo chỉ số `period`.

---

## 2. Lợi ích Cốt Lõi

- **Bền vững (Resilience):** Dù API nguồn đổi trả 200 hay 50 trường, hoặc đổi ký tự, thì miễn là Field Key cơ bản tồn tại, Schema của bạn vẫn trả về cố định 19-31 dòng chỉ tiêu duy nhất theo đúng tên tiếng Việt. Việc duy trì cấu trúc cố định sau này do tác giả thực hiện.
- **Auto-Detection (Tự nhận diện):** Tham số `scorecard="auto"` tự động nhận diện HPG là nhóm Sản Xuất (`generic`), TCB là (`banking`), SSI là (`securities`) để điều chỉnh layout báo cáo cho phù hợp. Điều này giảm thiểu việc bị lọt các trường rác (ví dụ: Công ty bán lẻ sẽ không bị hiện trường "Trích lập dự phòng Rủi ro Tín Dụng" vốn chỉ dành cho ngân hàng).
- **Chống Trùng Lặp (No Colisson):** Khắc phục lỗi báo cáo ghi đè (ví dụ: "NGUỒN VỐN" và "I. Vốn chủ sở hữu" đè nhau gây mất trường `Vốn chủ sở hữu` đã được sửa hoàn toàn thông qua cơ chế `groupby(level=0, axis=1).sum(min_count=1)`).

---

## 3. Cách Sử Dụng Phương Thức `financial_health()`

Hàm hợp nhất dữ liệu này là đại diện của kiến trúc mới, giúp gộp tất cả các mảng tài chính lại trong một câu lệnh duy nhất.

```python
from vnstock_data.ui.fundamental import Fundamental

fun = Fundamental(source="mas") # Lấy MAS làm chuẩn (Nhanh và tin cậy cho cấu trúc thô)

# 1. Đối với Công ty chung (Generic - HPG)
df_hpg = fun.equity("HPG").financial_health(scorecard="auto", lang="vi", limit=4)

# 2. Tuỳ chọn Custom Reports (Lấy duy nhất chỉ số Ratios và Income Statement để tối ưu tốc độ)
df_custom = fun.equity("TCB").financial_health(scorecard="auto", lang="vi", reports=["ratio", "income_statement"], limit=4)
```

### Tham Chiếu Output Đối Chứng (TCBS Terminal Replica)

Kết quả trả về sẽ giống hệt mô hình bạn đang xem trên giao diện TCBS:

**Ví dụ (Nhóm Chứng khoán - SSI):**
*   **Balance Sheet:** *Tài sản ngắn hạn, Tài sản cố định, Tổng tài sản, Vốn chủ sở hữu, Tổng nợ phải trả, Tài sản FVTPL, Cho vay Margin...*
*   **Income Statement:** *Doanh thu môi giới, Chi phí hoạt động, Lãi/Lỗ FVTPL, TỔNG LỢI NHUẬN TRƯỚC THUẾ...*
*   **Ratios:** *Trailing EPS, BVPS, P/E, P/B...*

*(Vui lòng tham khảo File Jupyter Example `03_Fundamental.ipynb` để có toàn bộ bảng minh hoạ DataFrame thực tế).*

> [!NOTE]
> **Về việc Tại sao số Rows trả về ngắn hơn Raw API:** Lớp lọc Scorecard chủ ý LÀM NGẮN báo cáo để giữ lại khoảng 15-30 KPIs phân tích định giá dòng tiền cốt yếu nhất (VD: thay vì đi sâu vào "Chi tiết chi phí bán hàng", "Quỹ khen thưởng phúc lợi", hệ thống dùng "Lãi trước thuế" và "Lợi nhuận gộp"). Nếu bạn cần 100% dữ liệu thô, gọi thẳng hàm `balance_sheet(scorecard=None)`.