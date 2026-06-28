# Advanced Usage (Sử Dụng Nâng Cao)

Hướng dẫn này dành riêng cho việc sử dụng **Adapter API** hoặc gọi trực tiếp vào từng module gốc (Legacy API) trong `vnstock_data`.

Nếu bạn là người mới sử dụng hoặc muốn tìm kiếm sự ổn định ưu tiên, hãy sử dụng **[Unified UI](../01-unified-ui.md)**.

## 1. Ưu Điểm & Trường Hợp Sử Dụng

- **Ưu điểm**: Cho phép kiểm soát hoàn toàn truy vấn, tự trích xuất các thông tin nguyên bản hoặc dữ liệu ngách mà Unified UI có thể đã ẩn đi để chuẩn hóa. Giúp khai thác trọn vẹn toàn bộ khả năng của `vnstock_data`.
- **Trường hợp sử dụng**: Phù hợp cho lập trình viên có kinh nghiệm, xây dựng pipeline tùy chỉnh, hoặc cần dữ liệu thô (raw data) đặc thù.

## 2. Các Loại Dữ Liệu Chính (Legacy API Mapping)

Dưới đây là bảng đối chiếu giữa các lớp Adapter API cũ và Unified UI hiện tại để bạn dễ hình dung:

| Loại Dữ Liệu | Lớp (Legacy) | Unified UI | Mô Tả |
| --- | --- | --- | --- |
| **Niêm Yết** | `Listing` | `Reference().equity` | Danh sách cổ phiếu, chỉ số, chứng quyền |
| **Giá Lịch Sử** | `Quote` | `Market().equity(symbol)` | OHLCV, intraday, order book |
| **Công Ty** | `Company` | `Reference().company(symbol)` | Thông tin, cổ đông, ban lãnh đạo |
| **Tài Chính** | `Finance` | `Fundamental().equity(symbol)` | BCTC, chỉ số tài chính |
| **Giao Dịch** | `Trading` | `Market().equity(symbol)` | Bảng giá, thống kê, nước ngoài, nội bộ |
| **Định Giá** | `Market` | `Analytics().valuation(index)` | P/E, P/B toàn thị trường |
| **Khám phá** | `TopStock` | `Insights().ranking()` | Top gainer, loser, volume, deal |
| **Kinh Tế Vĩ Mô** | `Macro` | `Macro().economy()` | GDP, CPI, FDI, tỷ giá, vv |
| **Hàng Hóa** | `CommodityPrice` | `Macro().commodity()` | Vàng, dầu, gas, sắt, thịt heo, vv |
| **Quỹ** | `Fund` | `Reference().fund` / `Market().fund()` | Quỹ đầu tư mở, ETF |

## 3. Cách Gọi API Nâng Cao

### 3.1. Adapter Chung (Linh Hoạt Nguồn Dữ Liệu)

Adapter chung tự động điều hướng kết nối API xuống các Explorer bên dưới tùy thuộc vào nguồn (source) được chọn.

```python
from vnstock_data import Quote, Finance, Trading

# Chỉ định nguồn dữ liệu
quote = Quote(source="vci", symbol="VCB")
df_price = quote.history(start="2024-01-01", end="2024-12-31", interval="1D")

# Dễ dàng đổi nguồn nếu cần
quote_vnd = Quote(source="vnd", symbol="VCB")
df_price_vnd = quote_vnd.history(start="2024-01-01", end="2024-12-31", interval="1D")
```

### 3.2. Import Trực Tiếp (Gọi Chi Tiết Module Nguyên Bản)

Cách tiếp cận này cho phép import trực tiếp lớp của Explorer, thay vì thông qua Adapter. Phù hợp nếu bạn cần dùng các tính năng riêng lẻ (chỉ có ở một source nhất định).

```python
from vnstock_data.explorer.vci import Quote, Finance, Trading

# Sử dụng trực tiếp từ nguồn cụ thể
quote = Quote(symbol="VCB")
df_price = quote.history(start="2024-01-01", end="2024-12-31", interval="1D")
```

## 4. Tham Khảo Tính Năng Advanced

Vui lòng tra cứu cấu trúc chi tiết các hàm Advanced (Legacy) API ở danh sách file trong thư mục `advanced-usage`:
- `01-listing.md`
- `02-quote.md`
- `03-company.md`
- `04-finance.md`
- `05-trading.md`
- `06-market.md`
- `07-insights.md`
- `08-macro.md`
- `09-commodity.md`
- `10-fund.md`