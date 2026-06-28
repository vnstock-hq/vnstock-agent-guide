# Nhật ký thay đổi (Changelog) - Vnstock Data

Dưới đây là lịch sử các phiên bản và những cập nhật quan trọng liên quan đến thư viện `vnstock_data`.

## 24-05-2026 (v3.2.0)

> Phát hành vnstock_data phiên bản 3.2.0 với những tinh chỉnh nhỏ giúp tăng tính ổn định của hệ thống.

- **Tích hợp Toàn diện Dữ liệu ASEAN (Unified UI)**:
  - Tích hợp luồng dữ liệu từ trung tâm phân tích của Asean Securities, mở rộng mạnh mẽ năng lực phân tích và giúp người dùng tiếp cận dữ liệu với góc nhìn đa chiều:
    - **Insights**: Cung cấp bộ công cụ chuyên sâu đo lường tâm lý thị trường (`sentiment`: breadth, heatmap, contribution), theo vết dòng tiền (`flow`: foreign, proprietary, active). Đào sâu phân tích cấp độ Ngành (`sector`) và Cổ phiếu (`equity`) thông qua biểu đồ Relative Rotation Graph (`rrg`), định giá (`valuation`), so sánh ngang hàng (`peer_compare`), và phân tích dòng lệnh (`order_flow`).
    - **Vĩ mô & Hàng hoá (Macro)**: Thay thế lõi truy xuất dữ liệu Vĩ mô (Kinh tế, Tiền tệ) sang nguồn ASEAN với độ trễ thấp hơn. Tăng cường khả năng tiếp cận tức thời các chỉ số toàn cầu như Lợi suất trái phiếu (`bond_yield`), Lãi suất Fed (`fed_rate`), và các rổ hàng hoá phái sinh chuẩn quốc tế trực tiếp qua `Macro().global` và `Macro().commodity()`.
  - **Tương thích & Ổn định**:
    - Khi người dùng truy xuất các hàng hoá đặc thù của Việt Nam (VD: Vàng SJC, Thép D10, Lợn Hơi) qua tham số `market="VN"`, hệ thống tự động fallback mượt mà về nguồn SPL cũ, đảm bảo không bị gián đoạn trải nghiệm phân tích số liệu cục bộ.
  - **Trải nghiệm Phát triển**: Toàn bộ các endpoints mới được dán nhãn `[Experimental]` khi gọi lệnh `show_api()`, giúp các nhà phân tích phân biệt và nắm bắt nhanh chóng kho công cụ mới này.

## 16-05-2026 (v3.1.8)

- **Chuẩn hoá Báo cáo Tài chính (Unified UI)**:
  - Đồng bộ Schema báo cáo tài chính cho các nguồn dữ liệu (MAS, VCI), xử lý triệt để lỗi lệch cột và lẫn lộn ngôn ngữ (mixed labels) bằng hệ thống Mapping chỉ số La Mã (Roman numeral).
  - Bổ sung thông tin kỳ báo cáo (`report_period`) cho nguồn VCI, đảm bảo dữ liệu hiển thị đầy đủ và tương thích với giao diện Unified UI.
- **Thị trường Trái phiếu (Bond Market)**:
  - Tích hợp lớp domain `bond` vào hệ thống Unified UI, mở rộng khả năng tra cứu dữ liệu thị trường trái phiếu.

## 05-05-2026 (v3.1.7)

- Bổ sung khả năng truy xuất tài liệu và báo cáo tài chính cho từng mã chứng khoán. Người dùng có thể truy xuất hàng loạt liên kết đến file báo cáo tài chính định dạng PDF thông qua lập trình đơn giản.
  ```python
  from vnstock_data import Fundamental
  fun = Fundamental()
  fun.equity('FPT').filing(doc_type='annual_report')
  ```
- Tinh chỉnh chức năng hàm tiện ích `show_api` để hiển thị thông tin cây API trọn vẹn hơn theo từng cấp. 
  - Ví dụ để xem tất cả cấu trúc bên dưới nhóm hàm `Reference` có thể gọi `show_api('Reference')` 
  - Để xem chi tiết sâu hơn 1 cấp nữa, có thể sử dụng cú pháp chaining dạng `show_api('Reference.equity')` 

## 02-05-2026 (v3.1.6)

- Sửa lỗi xảy ra với `vnstock_data/explorer/vci/listing.py", line 35, in all_symbols` xung đột thư viện sau khi code bị làm rối.

## 01-05-2026 (v3.1.5)

- Cập nhật khả năng tuỳ chỉnh điều kiện lọc cho hàm lọc dữ liệu cổ phiếu từ VCI trong giao diện hợp nhất tại lớp `Insights`.
- Sửa lỗi `ProxyConfig.update_forward_refs()` trong `vnstock_data/core/utils/client.py` khi gọi lệnh mẫu `Company(symbol='VIC', source='KBS').overview()`.

## 29-04-2026 (v3.1.4)

- Tích hợp thay đổi từ CLI Installer: Bổ sung danh sách mapping chính xác các chỉ số index từ HNX, UPCOM để truy xuất dữ liệu lịch sử ohlcv từ VCI.

## 23-04-2026 (v3.1.3)

- **Chuẩn hoá & Mở rộng Báo cáo Tài chính (Fundamental & Financial Health)**:
    - Mở rộng Schema tài chính với các trường dữ liệu chi tiết từ nguồn MAS.
    - Định chuẩn hóa bộ tiêu chí đánh giá cho 4 nhóm ngành: Ngân hàng, Chứng khoán, Bảo hiểm và Đa ngành theo tiêu chuẩn phân tích chung.
- **Hạ tầng & Tối ưu hóa (Infrastructure & Refactoring)**:
    - Nâng cấp các module tiện ích lõi (`client.py`, `user_agent.py`) để cải thiện hiệu năng kết nối và quản lý User-Agent.
- **Sửa lỗi & Ổn định hệ thống (Bug Fixes)**:
    - Khắc phục triệt để lỗi sai tỷ lệ giá (price scaling) cho các tài sản Chỉ số (Index) và Phái sinh (Derivative) tại module `quote` (nguồn KBS).
    - Sửa lỗi truy xuất dữ liệu danh sách niêm yết (listing) và báo giá (quote) cho nguồn Dukascopy.
    - Xử lý các lỗi nhỏ trong UI Registry và logic phân loại ngành giúp hệ thống hoạt động chính xác hơn.
- **Chuyển đổi giao thức dữ liệu VCI (API Migration)**:
    - Chuyển đổi toàn bộ quy trình lấy danh sách (Listing) và mã ngành (ICB) từ nguồn VCI từ GraphQL sang REST API để tăng độ ổn định.

## 12-04-2026 (v3.1.0)

> Phần mềm `vnstock_data` cập nhật phiên bản 3.1.0: Hoàn thiện bộ dữ liệu hợp nhất (Unified UI) và bổ sung dữ liệu thị trường Quốc tế.

- **Thị trường Quốc tế & Crypto**:
    - Tích hợp dữ liệu tiền mã hoá (Cryptocurrency) thông qua API Binance Spot.
    - Xây dựng kiến trúc Explorer cung cấp biểu đồ đa khung thời gian cho Ngoại hối (Forex), Hàng hoá (Commodity) và các chỉ số toàn cầu thông qua Dukascopy và ForexSB.
- **Thị trường Nội địa (Unified UI)**:
    - Nâng cấp API cho thị trường chỉ số (Index Market): Hệ thống hỗ trợ lấy bộ dữ liệu thống kê giao dịch lịch sử của tất cả các loại chỉ số thông qua phương thức `trade_history()`.
    - Bổ sung hàm tóm tắt bức tranh tài chính tổng hợp `financial_health` (tổ hợp 3 bảng báo cáo tài chính và các chỉ số tài chính). Chuẩn hoá chuyển ngữ thẻ Scorecard chuyên ngành: Ngân hàng, Chứng khoán, Bảo hiểm.
    - Nguồn dữ liệu cung cấp dữ liệu tài chính cho các hàm tại Unified UI được chuyển đổi từ KBS sang MAS để tăng số kỳ báo cáo tài chính lên trên 10 năm.
- Tối ưu tra cứu dữ liệu Vĩ mô (Macro) và Hàng hoá bằng kỹ thuật quét lùi tự động và đắp điền dữ liệu khuyết rỗng (Forward-fill).
- Cải thiện khả năng chuẩn hoá symbol nhập vào hàm của CafeF.

## 07-04-2026 (v3.0.1)

- **Unified UI**: Bổ sung hàm `cash_flow` vào giao diện hợp nhất; cập nhật mô tả cho hàm `trade_history`.
- **Nguồn KBS**: Sửa lỗi chia điểm index cho 1000 và lỗi 502 Bad Gateway; tinh chỉnh chuẩn hoá tên chỉ tiêu tài chính.
- **Nguồn MBK (Vĩ mô)**: Cải thiện thuật toán truy xuất dữ liệu theo tham số `length` và tự động *forward fill*.
- **Nguồn SPL (Hàng hoá)**: Sửa lỗi truy xuất dữ liệu null.
- **Nguồn VCI**: Bổ sung cơ chế tương thích pandas cho hàm map và applymap.

## 11-03-2026 (v3.0.0)

> **Phát hành vnstock_data 3.0.0: Thế hệ mới với Unified UI và Thị trường Quốc tế.**

- **Kiến trúc 7 Lớp & Unified UI (U2)**:
    - Hoàn thiện mô hình **Unified UI** với 7 phân vùng chức năng rõ rệt.
    - Cách tiếp cận "Vấn đề là trên hết": Chất lượng và nguồn dữ liệu tốt nhất sẽ được Vnstock khuyến nghị.
    - Bổ sung thông tin hồ sơ chi tiết cho **Chứng quyền** và **Hợp đồng tương lai**.
    - Tích hợp **Lịch sự kiện thị trường** toàn diện từ năm 2000.
- **Trợ lý lập trình thông minh (Next-Gen DX)**:
    - Tái kích hoạt tính năng **Autocomplete** và **Docstring**.
    - Bổ sung bộ công cụ khám phá API: `show_api()` và `show_doc()`.
- **Chuẩn hóa & Tối ưu hóa hệ thống**:
    - Chuẩn hoá dữ liệu bảng giá từ nguồn KBS.
    - Cơ chế **Lọc tham số (Kwargs Filtering)** giảm thiểu lỗi runtime.

## 05-03-2026 (v2.5.0)

- Cập nhật module **Unified UI (U2)**.
- Bổ sung hàm lấy thông tin Chứng quyền và hợp đồng tương lai thông qua `Reference().derivatives().warrant()` và `Reference().derivatives().futures()`.
- Bổ sung hàm lấy thông tin bộ lọc cổ phiếu từ VCI thông qua `Insights().screener()`.
- Cải thiện & bổ sung API nguồn Vĩ mô: Bổ sung method `interest_rate`, tích hợp tham số thời gian `length`.
- Cải thiện trải nghiệm sử dụng module lấy dữ liệu hàng hoá.

## 31-01-2026 (v2.3.4)

- Chuẩn hoá định dạng dữ liệu giá thành dạng thập phân cho hàm `history` và `intraday` (nguồn KBS).
- Sửa lỗi tham số `length` trong hàm `history` của lớp Quote (VCI, VND, MAS).
- Sửa lỗi không nhận diện nguồn VND cho lớp hàm Market.

## 28-01-2026 (v2.3.2)

- Chuẩn hoá tham số `period` để lấy dữ liệu báo cáo tài chính (KBS).
- Bổ sung tham số `length` cho lớp Hàng hóa (Commodity).

## 27-01-2026 (v2.3.1)

- Bổ sung hàm tiện ích `convert_derivative_symbol` giúp chuyển đổi mã phái sinh kiểu cũ sang mã chuẩn KRX mới.
- Cải thiện nguồn KBS:
  - Cho phép lấy dữ liệu báo cáo tài chính nhiều năm.
  - Hỗ trợ lấy dữ liệu các mã index phổ biến HNXINDEX, UPCOMINDEX...

## 23-01-2026 (v2.2.0)

- Bổ sung nguồn dữ liệu KBS cho phép truy cập từ các dịch vụ cloud (Colab, Kaggle).
- Bổ sung khả năng truy xuất thông tin bộ chỉ số đầu tư và chỉ số ngành từ HOSE vào Listing class.

## 21-07-2025 (v2.1.3)

- Bổ sung nguồn Fmarket vào mã nguồn.
- Thay thế và nâng cấp các API nguồn VCI (Quote, Listing, Financial, Trading).

## 02-06-2025 (v2.1.2)

- Bổ sung hàm truy xuất dữ liệu lịch sử giao dịch từ VCI với Trading class thay thế dữ liệu từ CafeF.

## 06-05-2025 (v2.1.1)

- Sửa lỗi hàm Intraday sau khi triển khai hệ thống KRX (từ 5/5/2025).
- Cập nhật thay đổi user_agent ngẫu nhiên và bổ sung hàm `price_board` cho nguồn VCI.

## 22-04-2025 (v2.1.0)

> Đánh dấu bước tiến lớn trong khả năng quản lý dữ liệu với việc áp dụng cấu trúc **Adapter Pattern** chuẩn hóa giao tiếp với các nguồn cấp dữ liệu. Bắt buộc truyền tham số `source` vào các lớp.
