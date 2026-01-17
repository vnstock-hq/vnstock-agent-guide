# VNStock 3.4.0 - Tài Liệu Hướng Dẫn

## 🎯 Giới Thiệu

**VNStock** là thư viện Python để lấy dữ liệu chứng khoán Việt Nam từ nhiều nguồn uy tín. Thiết kế với kiến trúc provider-based, cho phép chuyển đổi linh hoạt giữa các nguồn dữ liệu khác nhau.

### ✨ Tính Năng Chính

- ✅ **Nhiều nguồn dữ liệu**: VCI, KBS, MSN (web scraping); FMP, XNO, DNSE (API bên ngoài)
- ⚠️ **TCBS**: Đã deprecated từ v3.4.0, sẽ loại bỏ trong v3.5.0 (tháng 3/2026)
- ✅ **API thống nhất**: Cùng interface cho tất cả nguồn
- ✅ **Dữ liệu lịch sử & Real-time**: Giá, công ty, tài chính
- ✅ **Dữ liệu công ty**: Hồ sơ, cổ đông, nhân viên quản lý
- ✅ **Dữ liệu tài chính**: Báo cáo, chỉ số, lưu chuyển tiền tệ
- ✅ **Lọc & Phân loại**: Theo ngành, sàn giao dịch, chỉ số

## 📚 Hướng Dẫn Sử Dụng

| Tài Liệu | Nội Dung | Mức Độ |
|---------|---------|--------|
| **[01-Overview](01-overview.md)** | Tổng quan kiến trúc, các loại dữ liệu | Cơ bản |
| **[02-Installation](02-installation.md)** | Cài đặt, thiết lập, kiểm tra | Cơ bản |
| **[03-Listing API](03-listing-api.md)** | API tìm kiếm và lọc chứng khoán | Cơ bản |
| **[04-Company API](04-company-api.md)** | Thông tin công ty, cổ đông, nhân viên quản lý | Cơ bản |
| **[05-Trading API](05-trading-api.md)** | Dữ liệu giao dịch, bid/ask, thống kê | Cơ bản |
| **[06-Quote & Price](06-quote-price-api.md)** | API lấy giá lịch sử và real-time | Cơ bản |
| **[07-Financial API](07-financial-api.md)** | API dữ liệu tài chính và báo cáo | Trung cấp |
| **[08-Fund API](08-fund-api.md)** | Dữ liệu quỹ đầu tư mở (Fmarket) | Trung cấp |
| **[09-Screener API](09-screener-api.md)** | Công cụ lọc chứng khoán nâng cao | Nâng cao |
| **[10-Connector Guide](10-connector-guide.md)** | Hướng dẫn API bên ngoài (FMP, XNO, DNSE) | Nâng cao |
| **[11-Best Practices](11-best-practices.md)** | Mẹo tối ưu hóa, xử lý lỗi, security | Nâng cao |
| **[12-Migration Guide](12-migration-guide.md)** | Hướng dẫn chuyển từ TCBS sang KBS/VCI | Quan trọng |

## 🚀 Bắt Đầu Nhanh

### Cài Đặt

```bash
pip install vnstock
```

Xem chi tiết tại **[02-Installation](02-installation.md)**

## 📖 Cấu Trúc Tài Liệu

Tài liệu được chia thành 11 phần theo thứ tự từ cơ bản đến nâng cao:

1. **[01-Overview](01-overview.md)** - Hiểu kiến trúc và các loại dữ liệu
2. **[02-Installation](02-installation.md)** - Cài đặt và kiểm tra môi trường
3. **[03-Listing API](03-listing-api.md)** - Tìm kiếm danh sách chứng khoán
4. **[04-Company API](04-company-api.md)** - Lấy thông tin công ty chi tiết
5. **[05-Trading API](05-trading-api.md)** - Dữ liệu giao dịch thị trường
6. **[06-Quote & Price](06-quote-price-api.md)** - Lấy dữ liệu giá
7. **[07-Financial API](07-financial-api.md)** - Truy cập dữ liệu tài chính
8. **[08-Fund API](08-fund-api.md)** - Thông tin quỹ đầu tư mở
9. **[09-Screener API](09-screener-api.md)** - Lọc chứng khoán nâng cao
10. **[10-Connector Guide](10-connector-guide.md)** - Sử dụng API bên ngoài
11. **[11-Best Practices](11-best-practices.md)** - Tối ưu hóa và xử lý lỗi
12. **[12-Migration Guide](12-migration-guide.md)** - Chuyển đổi từ TCBS sang KBS/VCI

## Kiến Trúc Hệ Thống

VNStock sử dụng kiến trúc provider-based cho phép chuyển đổi linh hoạt giữa các nguồn dữ liệu:

```
Ứng Dụng
   ↓
API Thống Nhất (Quote, Listing, Finance, Company)
   ↓
Adapter Layer (Chuẩn hóa dữ liệu)
   ↓
Các Nguồn Dữ Liệu (Web Scraping & API bên ngoài)
```

## 📊 Nguồn Dữ Liệu

### Web Scraping

| Nguồn | Danh Sách | Giá | Công Ty | Tài Chính | Trạng Thái |
|-------|----------|-----|--------|----------|-----------|
| **VCI** | ✅ | ✅ | ✅ | ✅ | Hoạt động |
| **KBS** | ✅ | ✅ | ✅ | ✅ | Mới (v3.4.0) |
| **TCBS** | ✅ | ✅ | ✅ | ✅ | ⚠️ Deprecated |
| **MSN** | ✅ | ✅ | ❌ | ❌ | Hoạt động |

### API Bên Ngoài

| API | Giá | Tài Chính | Công Ty |
|-----|-----|----------|---------|
| **FMP** | ✅ | ✅ | ✅ |
| **XNO** | ✅ | ✅ | ✅ |
| **DNSE** | ✅ | ❌ | ❌ |

## 🎓 Lộ Trình Học Tập

Khuyến nghị làm theo thứ tự từ trên xuống để hiểu toàn bộ hệ thống:

1. **[01-Overview](01-overview.md)** - Nắm vững kiến trúc và các khái niệm cơ bản
2. **[02-Installation](02-installation.md)** - Cài đặt và xác nhận môi trường hoạt động
3. **[03-Listing API](03-listing-api.md)** - Tìm kiếm chứng khoán theo tiêu chí
4. **[03a-Company API](03a-company-api.md)** - Tìm hiểu chi tiết về công ty
5. **[03b-Trading API](03b-trading-api.md)** - Phân tích dữ liệu giao dịch
6. **[04-Quote & Price](04-quote-price-api.md)** - Truy cập dữ liệu giá chứng khoán
7. **[05-Financial API](05-financial-api.md)** - Lấy dữ liệu tài chính chi tiết
8. **[05a-Fund API](05a-fund-api.md)** - Khám phá quỹ đầu tư mở
9. **[06-Connector Guide](06-connector-guide.md)** - Sử dụng API bên ngoài (FMP, XNO, DNSE)
10. **[06a-Screener API](06a-screener-api.md)** - Lọc chứng khoán theo tiêu chí nâng cao
11. **[07-Best Practices](07-best-practices.md)** - Áp dụng tối ưu hóa, xử lý lỗi, security

## 🔗 Liên Kết Hữu Ích

- **[GitHub](https://github.com/thinh-vu/vnstock)** - Mã nguồn và issue tracking
- **[PyPI](https://pypi.org/project/vnstock)** - Cài đặt package
- **[Website](https://vnstocks.com)** - Trang chính thức

## ℹ️ Thông Tin Phiên Bản

- **Phiên bản**: 3.4.0
- **Cập nhật lần cuối**: 2024-12-17
- **Trạng thái**: Đang bảo trì ✅
- **Thông báo**: TCBS đã deprecated, sẽ loại bỏ trong v3.5.0 (tháng 3/2026)
- **License**: MIT
