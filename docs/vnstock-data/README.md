# Vnstock Data - Hướng Dẫn Toàn Diện cho AI Agents

## Giới Thiệu

`vnstock_data` là thư viện Python cung cấp khả năng truy xuất toàn diện dữ liệu thị trường chứng khoán Việt Nam từ nhiều nguồn dữ liệu đáng tin cậy. Thư viện sử dụng **Adapter Pattern** để cho phép chuyển đổi dễ dàng giữa các nguồn dữ liệu mà không cần thay đổi code logic chính.

### Đặc Điểm Chính

- **Dữ liệu phân tích kỹ thuật (Technical)**: Giá lịch sử (OHLCV), chỉ báo (Indicators), mẫu hình nến (Candlestick Patterns).
- **Dữ liệu phân tích cơ bản (Fundamental)**: 
  - Báo cáo tài chính: Bảng cân đối kế toán, KQKD, Lưu chuyển tiền tệ.
  - Chỉ số tài chính, định giá, hồ sơ doanh nghiệp.
  - [Tham chiếu cấu trúc dữ liệu](08-schema-reference.md): Hệ thống lược đồ chuẩn đảm bảo tính tương thích chéo.
- **Dữ liệu chuyên sâu**: Giao dịch khối ngoại, tự doanh, top cổ phiếu ảnh hưởng chỉ số, bản đồ nhiệt (Heatmap).
- **Hiệu suất cao**: Caching, retry logic, rate limit handling.
- **Xử lý lỗi mạnh mẽ**: Tự động retry khi kết nối mất.
- **Minh bạch**: Dữ liệu công khai, có thể kiểm tra và ghi nguồn.
- **Unified UI**: Giao diện hợp nhất mới với `show_api()` / `show_doc()` để tra cứu cấu trúc tính năng.

### Cài Đặt Thư Viện

Các gói thư viện vnstock_data được cài đặt **chung** thông qua chương trình cài đặt của Vnstock. Để cài đặt và kích hoạt vnstock_data, vui lòng tham khảo hướng dẫn chi tiết tại **[Hướng Dẫn Cài Đặt Vnstock](https://vnstocks.com/onboard-member)**.

## Định hướng Sử dụng (Điều Hướng)

Thư viện `vnstock_data` cung cấp hai phong cách lập trình để đáp ứng mọi nhu cầu. Hãy chọn phương pháp phù hợp nhất với dự án của bạn:

### 1. Unified UI - Giao Diện Hợp Nhất (Khuyến Nghị Mặc Định)

**Unified UI** là giao diện tiêu chuẩn được khuyến nghị cho người dùng mới và đa số các dự án.

- **Ưu điểm**: Ưu tiên tính ổn định cao và cấu trúc dữ liệu chuẩn hóa chung cho mọi nguồn. Cú pháp chaining API (vd: `Market().equity()`) rất trực quan và dễ nhớ.
- **Trường hợp sử dụng**: Phù hợp khi bạn cần sự ổn định, không muốn bận tâm đến sự khác biệt giữa các nguồn cấp dữ liệu, và muốn một luồng phân tích liền mạch.

> **Khám phá Unified UI**: Hãy bắt đầu với tệp **[01-unified-ui.md](01-unified-ui.md)** để tìm hiểu về kiến trúc và cách sử dụng Giao Diện Hợp Nhất.

### 2. Advanced Usage (Sử dụng Nâng Cao - Legacy API)

Ngoài Unified UI, bạn vẫn có thể sử dụng **Adapter API** hoặc gọi trực tiếp vào từng module gốc.

- **Ưu điểm**: Cho phép kiểm soát hoàn toàn truy vấn, cho phép tự trích xuất các thông tin nguyên bản hoặc dữ liệu ngách mà Unified UI có thể đã ẩn đi để chuẩn hóa. Giúp khai thác trọn vẹn toàn bộ khả năng của `vnstock_data`.
- **Trường hợp sử dụng**: Phù hợp cho lập trình viên có kinh nghiệm, xây dựng pipeline tùy chỉnh, hoặc cần dữ liệu thô (raw data) đặc thù.

> **Khám phá Advanced Usage**: Xem hướng dẫn tại **[advanced-usage/00-overview.md](advanced-usage/00-overview.md)**.

## Hướng Dẫn Chuyển Đổi Phiên Bản (Migration)

Khi hệ sinh thái Vnstock liên tục phát triển, chúng tôi cung cấp các hướng dẫn chuyển đổi để nâng cấp hệ thống:

- **[Chuyển đổi sang v3.2.x](migrations/v3.2.md)**: Cập nhật API vĩ mô, hàng hóa.
- **[Chuyển đổi sang v3.0 (Unified UI)](migrations/v3.0.md)**: Nâng cấp lớn từ Legacy API sang Unified UI.

## Tham Số Thời Gian Tương Đối (`length`)

Trong nhiều hàm truy xuất dữ liệu, thư viện cung cấp cờ `length` để thiết lập khoảng thời gian lấy dữ liệu tương đối so với hiện tại. Các định dạng được hỗ trợ:

1. **Số ngày**: `150`, `"150"`
2. **Preset Chuẩn**: `"1W"`, `"2M"`, `"1Y"`
3. **Cấu Trúc Động**: `D` (Ngày), `W` (Tuần), `M` (Tháng), `Q` (Quý), `Y` (Năm). VD: `"100W"`.
4. **Số nến**: Khai báo hậu tố `b` (VD: `"100b"`).

## Các Nguồn Dữ Liệu Chính

| Tên       | Code    | Mô Tả                                  |
| --------- | ------- | -------------------------------------- |
| **VCI**   | `vci`   | Dữ liệu từ Vietcap                     |
| **VND**   | `vnd`   | VNDirect                               |
| **MAS**   | `mas`   | Mirae Asset                            |
| **CafeF** | `cafef` | CafeF Vietnam                          |
| **MBK**   | `mbk`   | Maybank Kimeng - Kinh tế Vĩ Mô         |
| **KBS**   | `kbs`   | KIS Berger Sec. - Giao dịch, phái sinh |
| **SPL**   | `spl`   | Dữ Lệu Hàng Hóa                        |
| **MSN**   | `msn`   | MSN Finance - Quốc tế, crypto          |

## Lý Do Sử Dụng Vnstock_data

1. **Toàn Diện**: Từ giá, BCTC đến kinh tế vĩ mô.
2. **Đáng Tin**: Nguồn cấp dữ liệu uy tín (VCI, VND,...).
3. **Linh Hoạt**: Chuyển đổi linh hoạt.
4. **Bảo Trì Tốt**: Cập nhật thường xuyên.
5. **Cộng Đồng**: Hỗ trợ nhiệt tình.

## Miễn Trừ Trách Nhiệm

Dữ liệu được cung cấp **chỉ nhằm mục đích nghiên cứu, giáo dục**. Không sử dụng làm cơ sở duy nhất cho quyết định giao dịch thực tế. Tác giả không chịu trách nhiệm về tổn thất.

## Cấu Trúc Tài Liệu Vnstock-Data

Tài liệu được chia thành các phần chính:

1. **[README.md](README.md)** (Tệp này) - Tổng quan và Điều hướng
2. **[01-unified-ui.md](01-unified-ui.md)** - Giao diện hợp nhất và Mô hình dữ liệu
3. **[02-reference-layer.md](02-reference-layer.md)** - Layer 1: Dữ liệu tham chiếu, công ty
4. **[03-market-layer.md](03-market-layer.md)** - Layer 2: Dữ liệu thị trường, giá cổ phiếu
5. **[04-fundamental-layer.md](04-fundamental-layer.md)** - Layer 3: Báo cáo tài chính, chỉ số
6. **[05-macro-layer.md](05-macro-layer.md)** - Layer 5: Kinh tế vĩ mô, hàng hóa
7. **[06-insights-layer.md](06-insights-layer.md)** - Layer 6: Xếp hạng, lọc cổ phiếu
8. **[07-analytics-layer.md](07-analytics-layer.md)** - Layer 7: Phân tích định giá
9. **[08-schema-reference.md](08-schema-reference.md)** - Tham chiếu cấu trúc dữ liệu
10. **[09-data-sources.md](09-data-sources.md)** - Ma trận support các nguồn dữ liệu
11. **[10-changelog.md](10-changelog.md)** - Nhật ký thay đổi phiên bản
12. **[advanced-usage/](./advanced-usage/)** - Tài liệu Adapter API & nâng cao (Legacy)
