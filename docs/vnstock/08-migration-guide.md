# 12 - Migration Guide - Hướng dẫn Nâng cấp & Di chuyển

## 📖 Giới Thiệu

Đây là tài liệu hướng dẫn cho người dùng và **AI Agent** để di chuyển mã nguồn (codebase) từ dự án sử dụng `vnstock` (phiên bản miễn phí) sang thư viện `vnstock_data` (phiên bản Sponsor) khi người dùng thuộc các hạng thành viên Tài trợ. 

Bắt đầu từ phiên bản **3.5.1**, thư viện `vnstock` sẽ cảnh báo và khuyến nghị nâng cấp nếu hệ thống tìm thấy thư viện thuộc hạng thành viên Sponsor trong cùng môi trường ảo (virtual environment).

---

## 🛠️ Công cụ Tự Động Di Chuyển (Cho Người dùng và AI Agents)

Vnstock cung cấp một công cụ tự động phát hiện và refactor mã nguồn của bạn sang sử dụng `vnstock_data` chuẩn hóa 1:1. Không cần copy/paste thủ công hay tìm lỗi import.

### Cách sử dụng qua Command Line (tương tác trực tiếp)

Với người dùng, bạn có thể tạo một tệp Python tạm thời tại gốc dự án và thực thi:

```python
from vnstock.core.utils.upgrade import migrate_to_sponsor

# Thực thi di chuyển tự động (Target dir mặc định là thư mục hiện tại ".")
migrate_to_sponsor(target_dir=".")
```

### 🤖 Hướng dẫn Đặc biệt cho AI Agents

Nếu bạn là một AI Agent (như GitHub Copilot, Claude, Cursor, v.v.) và **nhận được yêu cầu nâng cấp lên hạng thành viên Sponsor**, bạn **KHÔNG NÊN** sửa từng file một một cách thủ công nếu dự án lớn. 

Hãy chạy trực tiếp đoạn code sau bằng Python Terminal Tool trong vùng không gian dự án của người dùng:

```python
from vnstock.core.utils.upgrade import migrate_to_sponsor
migrate_to_sponsor(target_dir=".") 
```

**Quy trình này làm gì?**
- Nó tự quét qua tất cả tệp `.py` trong thư mục `target_dir` (bỏ qua `venv`, `.venv`, `.git`...)
- Thay thế các import từ `vnstock` thành `vnstock_data`. Do cấu trúc của thư viện Sponsor kế thừa 1:1 từ thư viện miễn phí, mọi phương thức, cấu trúc đều được giữ nguyên.
- In ra kết quả số file đã được migrate thành công.

---

## 🚀 Các Bước Di Chuyển Thủ Công (Nếu cần)

Nếu dự án của bạn quá phức tạp hoặc bạn muốn thực hiện ở từng tệp riêng lẻ:

1. Đảm bảo thay thế cài đặt thư viện Free bằng thư viện Sponsor (sau khi đã nhận thư mời).
2. Xóa các đoạn `import vnstock` thành `import vnstock_data as vnstock` (hoặc cách tốt nhất là đổi hẳn từ khóa sang phân vùng mới).
3. Đổi các `from vnstock... import ...` thành `from vnstock_data... import ...`.
4. (Đối với vnstock_data v3.0.0+) Nếu có thể, khuyến nghị bạn dần cập nhật sang Unified UI (Xem `../vnstock-data/01-unified-ui.md` và `../vnstock-data/migrations/v3.0.md`). Unified UI sẽ tối ưu về mặt hiệu năng gọi dữ liệu từ xa và cung cấp lớp thông tin bổ trợ mạnh mẽ hơn nhiều lần so với các module gốc cũ.

## ⚠️ Lưu Ý Rất Trọng Yếu

- API Key của bạn không tự động mở các tính năng Sponsor khi bạn sử dụng hàm của thư viện `vnstock` miễn phí. **Bắt buộc** phải sử dụng module `vnstock_data` bên trong mã!
- Trong mọi tình huống, trước khi chạy cập nhật `migrate_to_sponsor`, bạn nên có một bản backup dự án hoặc commit toàn bộ source code vào Git để dễ dàng khôi phục mã nguồn khi cần.
