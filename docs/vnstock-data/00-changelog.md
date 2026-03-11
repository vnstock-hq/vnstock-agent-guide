## 11-03-2026

> **Phát hành vnstock_data 3.0.0: Thế hệ mới với Unified UI và Thị trường Quốc tế.**
> 
> Phiên bản 3.0.0 không chỉ là một bản cập nhật thông thường, mà là bước chuyển mình quan trọng của hệ sinh thái Vnstock. Chúng tôi mang đến kiến trúc 7 lớp tiêu chuẩn nghiệp vụ, khả năng tiếp cận thị trường toàn cầu và trải nghiệm lập trình (DX) được nâng cấp vượt trội.

- **Kiến trúc 7 Lớp & Unified UI (U2)**:
  - Hoàn thiện mô hình **Unified UI** với 7 phân vùng chức năng rõ rệt: `Reference`, `Market`, `Fundamental`, `Analytics`, `Alternative`, `Macro`, và `Insights`.
  - Cách tiếp cận "Vấn đề là trên hết": Bạn không còn phải lo lắng về việc dữ liệu đến từ đâu, chỉ cần tập trung vào việc bạn muốn làm gì (định giá, xem bảng giá hay tra cứu thông tin cơ bản). Chất lượng và nguồn dữ liệu tốt nhất sẽ được Vnstock khuyến nghị. Bạn có thể cá nhân hoá nguồn dữ liệu như cách lập trình cũ nếu muốn để khai thác các chức năng có sẵn nhưng ẩn sâu trong mã nguồn.
  - Bổ sung thông tin hồ sơ (profile) chi tiết cho **Chứng quyền** và **Hợp đồng tương lai**, giúp bạn nắm bắt đầy đủ thông tin sản phẩm trước khi giao dịch.
  - Tích hợp **Lịch sự kiện thị trường** toàn diện: từ dữ liệu lịch sử (nghỉ lễ, sự cố thị trường... từ năm 2000) đến các sự kiện hiện tại và tương lai giúp bạn bao quát toàn cảnh thị trường một cách chuyên sâu.

- **Trợ lý lập trình thông minh (Next-Gen DX)**:
  - Tái kích hoạt tính năng **Autocomplete** và **Docstring** vượt trội trên các IDE (VSCode, PyCharm), giúp việc viết code nhanh và ít lỗi hơn.
  - Bổ sung bộ công cụ khám phá API: `show_api()` để vẽ sơ đồ thư viện ngay trong terminal và `show_doc()` để đọc nhanh hướng dẫn sử dụng cho từng hàm.
  - Tài liệu (Docstrings) đã được chuyển đổi sang tiếng Anh chuẩn để dễ dàng tiếp cận và phù hợp với tiêu chuẩn lập trình hiện đại và tương tác với AI Agent.

- **Chuẩn hóa & Tối ưu hóa hệ thống**:
  - **Chuẩn hoá dữ liệu bảng giá từ nguồn KBS**: Giải quyết triệt để các vấn đề về hiển thị lô chẵn, lô lẻ; đồng bộ hóa dữ liệu cho đa dạng loại tài sản từ cổ phiếu, phái sinh, chứng quyền đến trái phiếu.
  - Dữ liệu được **tự động chuẩn hóa (Normalization)** từ nhiều nguồn khác nhau về một định dạng duy nhất, giúp việc tính toán và phân tích nhất quán hơn.
  - Cơ chế **Lọc tham số (Kwargs Filtering)**: Giúp giảm thiểu lỗi runtime khi bạn vô tình truyền thừa tham số, tăng tính ổn định cho chương trình.
  - Tối ưu hóa tốc độ tải dữ liệu và cấu trúc nội bộ để sẵn sàng cho các bài toán phân tích dữ liệu lớn.

- **Cập nhật Vnstock Agent Guide**: Tài liệu hướng dẫn chi tiết và các quy tắc cho AI Agent trong lập trình tự động được cập nhật qua Agent Guide [tại đây](https://github.com/vnstock-hq/vnstock-agent-guide/blob/main/docs/vnstock-data/14-unified-ui.md)

## 05-03-2026

> Phát hành phiên bản vnstock_data 2.5.0

- **Cải thiện & bổ sung API nguồn Vĩ mô (MBK) tại module `vnstock_data/explorer/mbk/macro.py`**:
  - Bổ sung method `interest_rate` để lấy dữ liệu Lãi suất bình quân & Doanh số trên thị trường liên ngân hàng. Hỗ trợ tham số `format='pivot'` (mặc định) để trả về bảng dạng nhóm cột (MultiIndex giống biểu diễn trên website) hoặc `format='long'` để trả về định dạng phẳng (raw format).
  - Tích hợp thêm tham số khoảng thời gian tương đối `length` (ví dụ: `1Y`, `30D`, `100b`) tương tự như cách sử dụng trong `quote.history`. Tính năng này áp dụng đồng bộ cho tất cả các hàm vĩ mô (`gdp`, `cpi`, `interest_rate`, `exchange_rate` v.v...) để bỏ qua việc nhập ngày bắt đầu `start` và kết thúc `end`.
  - Thay đổi thời gian lấy dữ liệu mặc định (*khi không cung cấp `start`, `end`, hoặc `length`*) là 1 năm (`1Y`) để trả về thông tin ở khoảng thời gian phù hợp và nhẹ.
- **Cập nhật UI module**: Cập nhật các lớp UI cung cấp cấu trúc lệnh hợp nhất với phân nhóm chặt chẽ giúp điều hướng dễ dàng theo mặc định mà không cần quan tâm đến thông tin nguồn dữ liệu.

- **Cải thiện API nguồn Hàng hoá (SPL) tại module `vnstock_data/explorer/spl/commodity.py`**:
  - Tích hợp khả năng lấy thời gian tương đối thông qua tham số `length` tương tự như module `macro` và `quote.history`.
  - Thay đổi thời gian lấy dữ liệu mặc định (*khi không cung cấp `start`, `end`, hoặc `length`*) về 1 năm (`1Y`) thay vì lấy toàn bộ lịch sử như trước đây.