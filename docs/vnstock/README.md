# VNStock - Tài Liệu Hướng Dẫn

## 🎯 Giới Thiệu

**VNStock** là thư viện Python hàng đầu để lấy dữ liệu chứng khoán Việt Nam từ nhiều nguồn uy tín. Phiên bản hiện tại (3.5.1+) tập trung hoàn toàn vào **Giao diện Hợp nhất (Unified UI)**, cung cấp một API chuẩn hóa, nhất quán và cho phép chuyển đổi linh hoạt giữa các nguồn dữ liệu.

### ✨ Tính Năng Nổi Bật

- **API Thống nhất (Unified UI)**: Cấu trúc phân tầng rõ ràng (Reference, Market, Fundamental, Retail) thay thế cho hệ thống hàm phân mảnh cũ.
- **Đa nguồn dữ liệu**: Tích hợp các nguồn public (VCI, KBS, MSN) và official API (FMP, DNSE, XNO).
- **Dữ liệu Toàn diện**: Bao phủ dữ liệu giao dịch lịch sử/intraday, hồ sơ doanh nghiệp, báo cáo tài chính và các chỉ số kinh tế.
- ⚠️ **Lưu ý quan trọng**: Nguồn dữ liệu TCBS đã bị loại bỏ hoàn toàn. Các hàm (Legacy API) sẽ không còn được khuyến khích sử dụng và thay thế bằng cấu trúc Unified UI.

---

## 🚀 Cài Đặt Nhanh

Cài đặt phiên bản mới nhất thông qua `pip`:

```bash
pip install -U vnstock
```

---

## 📖 Cấu Trúc Tài Liệu & Lộ Trình Học Tập

Để nắm vững hệ thống Unified UI, hãy đọc tài liệu theo lộ trình được thiết kế dưới đây. Cấu trúc này sẽ đưa bạn từ các khái niệm cơ bản đến khả năng phân tích nâng cao.

| Phần  | Nội Dung & Liên Kết                                              | Mô tả chi tiết                                                     |
| :---- | :--------------------------------------------------------------- | :----------------------------------------------------------------- |
| **1** | [**Tổng quan Unified UI**](01-unified-ui.md)                     | Triết lý kiến trúc mới và các tầng dữ liệu cốt lõi                 |
| **2** | [**Cài đặt & Môi trường**](02-installation.md)                   | Thiết lập môi trường Python và xác thực thư viện                   |
| **3** | [**Tầng Reference**](03-reference-layer.md)                      | Tra cứu danh sách cổ phiếu, thông tin tĩnh, hồ sơ công ty          |
| **4** | [**Tầng Market**](04-market-layer.md)                            | Lấy dữ liệu giá trị động, OHLCV, sổ lệnh, giao dịch                |
| **5** | [**Tầng Fundamental**](05-fundamental-layer.md)                  | Truy cập báo cáo tài chính, chỉ số định giá và cân đối kế toán     |
| **6** | [**Tầng Retail**](06-retail-layer.md)                            | Khám phá dữ liệu thay thế (vàng, tỷ giá ngoại tệ)                  |
| **7** | [**So sánh Free vs Sponsor**](07-comparison.md)                  | Đánh giá giới hạn Rate Limit và các tính năng chuyên sâu           |
| **8** | [**Hướng dẫn Nâng cấp**](08-migration-guide.md)                  | Chuyển đổi mã nguồn từ vnstock (Free) sang vnstock_data (Sponsor)  |
| **9** | [**Advanced Usage (Legacy API)**](advanced-usage/00-overview.md) | Hướng dẫn gọi trực tiếp API kiểu cũ (Dành cho người dùng nâng cao) |

---

## 🏗️ Kiến Trúc Hệ Thống & Nguồn Dữ Liệu

VNStock sử dụng kiến trúc Adapter Pattern để đồng nhất đầu ra từ nhiều nguồn phân mảnh khác nhau:

```text
User Application
       ↓
Unified UI Layer (Reference, Market, Fundamental, Retail)
       ↓
Adapter Layer (Data Normalization & Rate Limiting)
       ↓
Data Providers (VCI, KBS, MSN, FMP, DNSE, XNO)
```

**Bảng tóm tắt các nguồn dữ liệu đang hỗ trợ:**

| Nguồn         | Danh mục | Giá (OHLCV) | Công ty | BCTC  | Phân loại                        |
| :------------ | :------: | :---------: | :-----: | :---: | :------------------------------- |
| **VCI / KBS** |    ✅     |      ✅      |    ✅    |   ✅   | Web Scraping (Hoạt động ổn định) |
| **MSN**       |    ✅     |      ✅      |    ❌    |   ❌   | Web Scraping                     |
| **FMP**       |    ✅     |      ✅      |    ✅    |   ✅   | External API                     |

---

## 🔗 Liên Kết Hữu Ích & Thông Tin

- **Website Chính Thức**: [vnstocks.com](https://vnstocks.com)
- **Mã nguồn (GitHub)**: [thinh-vu/vnstock](https://github.com/thinh-vu/vnstock)
- **Cài đặt (PyPI)**: [vnstock package](https://pypi.org/project/vnstock)
- **Phiên bản hiện tại**: 4.0.5
- **Giấy phép**: Custom License | non-commercial