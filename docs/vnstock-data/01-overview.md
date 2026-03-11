# Vnstock Data - Hướng Dẫn Toàn Diện cho AI Agents

## Giới Thiệu

`vnstock_data` là thư viện Python cung cấp khả năng truy xuất toàn diện dữ liệu thị trường chứng khoán Việt Nam từ nhiều nguồn dữ liệu đáng tin cậy. Thư viện sử dụng **Adapter Pattern** để cho phép chuyển đổi dễ dàng giữa các nguồn dữ liệu mà không cần thay đổi code logic chính.

### Cấu Trúc Thư Viện

Thư viện được tổ chức theo cấu trúc module rõ ràng để dễ dàng bảo trì và mở rộng:

```
vnstock_data/
├── __init__.py          # Khởi tạo package, export các class chính
├── base.py              # Base classes và utilities chung
├── config.py            # Cấu hình toàn cục
├── api/                 # API interfaces thống nhất
│   ├── __init__.py
│   ├── commodity.py     # Dữ liệu hàng hóa
│   ├── company.py       # Thông tin công ty
│   ├── financial.py     # Báo cáo tài chính
│   ├── insight.py       # Phân tích insights
│   ├── listing.py       # Danh sách niêm yết
│   ├── macro.py         # Kinh tế vĩ mô
│   ├── market.py        # Dữ liệu thị trường
│   ├── quote.py         # Dữ liệu giá
│   └── trading.py       # Dữ liệu giao dịch
├── core/               # Core utilities
│   ├── __init__.py
│   ├── const.py        # Constants
│   └── utils/          # Utility functions
├── explorer/           # Data explorers cho từng nguồn
│   ├── __init__.py
│   ├── cafef/          # CafeF data source
│   ├── fmarket/        # Fmarket data source
│   ├── mas/            # MAS data source
│   ├── mbk/            # MBK data source
│   ├── spl/            # SPL data source
│   ├── vci/            # VCI data source
│   └── vnd/            # VND data source
└── ui/                 # Unified UI - Giao diện hợp nhất thế hệ mới
    ├── __init__.py
    ├── helper.py       # show_api(), show_doc()
    ├── reference.py    # Layer 1: Dữ liệu tham chiếu
    ├── market.py       # Layer 2: Dữ liệu giao dịch
    ├── fundamental.py  # Layer 3: Báo cáo tài chính
    ├── analytics.py    # Layer 4: Phân tích định giá
    ├── macro.py        # Layer 5: Kinh tế vĩ mô
    ├── insights.py     # Layer 6: Xếp hạng & lọc
    └── domains/        # Domain implementations
```

**Giải thích cấu trúc:**
- **`api/`**: Chứa các interface thống nhất cho từng loại dữ liệu (giá, công ty, tài chính, v.v.)
- **`explorer/`**: Implementations cụ thể cho từng nguồn dữ liệu (VCI, VND, CafeF, v.v.)
- **`core/`**: Utilities và constants dùng chung
- **`ui/`**: **Unified UI** - Giao diện hợp nhất thế hệ mới (áp dụng từ 11/3/2026), cung cấp trải nghiệm sử dụng tốt hơn và toàn vẹn hơn

### Đặc Điểm Chính

- **Linh hoạt đa nguồn**: Hỗ trợ các nguồn VCI, VND, MAS, CafeF, v.v.
- **API thống nhất**: Một chuẩn giao tiếp duy nhất cho tất cả loại dữ liệu
- **Dữ liệu phong phú**: Cổ phiếu, chỉ số, trái phiếu, chứng quyền, hàng hóa, kinh tế vĩ mô
- **Hiệu suất cao**: Caching, retry logic, rate limit handling
- **Xử lý lỗi mạnh mẽ**: Tự động retry khi kết nối mất
- **Minh bạch**: Dữ liệu công khai, có thể kiểm tra và ghi nguồn.
- **Unified UI**: Giao diện hợp nhất mới với `show_api()` / `show_doc()` để tra cứu cấu trúc tính năng

### Các Loại Dữ Liệu Chính

| Loại Dữ Liệu | Lớp (Legacy) | Unified UI | Mô Tả |
|---|---|---|---|
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

### Cài Đặt Thư Viện

Các gói thư viện vnstock_data được cài đặt **chung** thông qua chương trình cài đặt của Vnstock. Để cài đặt và kích hoạt vnstock_data, vui lòng tham khảo hướng dẫn chi tiết tại **[Hướng Dẫn Cài Đặt Vnstock](https://vnstocks.com/onboard-member)**.

## Cách sử dụng cơ bản
### Unified UI - Giao Diện Hợp Nhất (Khuyến Nghị dùng từ 11/3/2026)

**Unified UI** là giao diện sử dụng thế hệ mới nhất, cung cấp 8 nhóm tính năng dữ liệu với cú pháp chaining API trực quan. Các cách gọi hàm trước kia vẫn hoạt động nhưng được khuyến nghị chuyển đổi dần sang Unified UI để tận dụng bộ dữ liệu toàn diện và chặt chẽ nhất.

```python
from vnstock_data import Reference, Market, Fundamental, Analytics, Insights, Macro
from vnstock_data import show_api, show_doc  # Tra cứu cấu trúc tính năng

# Tra cứu cấu trúc tính năng
show_api()                    # Xem toàn bộ cây tính năng
show_doc(Reference.company)   # Đọc hướng dẫn chi tiết

# Sử dụng chaining API
ref = Reference()
df = ref.company("TCB").info()                          # Thông tin công ty
df = Market().equity("VIC").ohlcv(start="2026-02-01", end="2026-03-01")  # Lịch sử giá
df = Fundamental().equity("HPG").income_statement()     # BCTC
df = Analytics().valuation("VNINDEX").pe(duration="1Y") # P/E thị trường
df = Insights().ranking().gainer()                       # Top tăng giá
df = Macro().economy().gdp(period="quarter")             # GDP
```

> **Chi tiết đầy đủ**: Xem **[14-unified-ui.md](14-unified-ui.md)** và các file trong thư mục **[unified-ui/](./unified-ui/)**. Hướng dẫn chuyển đổi: **[04-migration-guide.md](unified-ui/00-migration-guide.md)**.

### Legacy API: Cách dùng cũ vẫn được duy trì

Các cách sử dụng bên dưới vẫn hoạt động nhưng dần chuyển đổi sang Unified UI.

#### 1. Cách Thứ Nhất: Adapter Chung (Linh Hoạt)

```python
from vnstock_data import Quote, Finance, Trading

# Chỉ định nguồn dữ liệu
quote = Quote(source="vci", symbol="VCB")
df_price = quote.history(start="2024-01-01", end="2024-12-31", interval="1D")

# Dễ dàng đổi nguồn nếu cần
quote_vnd = Quote(source="vnd", symbol="VCB")
df_price_vnd = quote_vnd.history(start="2024-01-01", end="2024-12-31", interval="1D")
```

#### 2. Cách Thứ Hai: Import Trực Tiếp (Ổn Định)

```python
from vnstock_data.explorer.vci import Quote, Finance, Trading

# Sử dụng trực tiếp từ nguồn cụ thể
quote = Quote(symbol="VCB")
df_price = quote.history(start="2024-01-01", end="2024-12-31", interval="1D")
```

## Tham Số Thời Gian Tương Đối (`length`)

Trong nhiều hàm truy xuất dữ liệu (như `Macro`, `CommodityPrice`, `Quote`,...), thư viện cung cấp cờ `length` để thiết lập khoảng thời gian lấy dữ liệu tương đối so với hiện tại, thay vì phải truyền `start` và `end` cố định. 

Hệ thống cung cấp cơ chế giải mã linh hoạt cho `length`. Bạn có thể truyền các định dạng sau:

1. **Số ngày chính xác (Integer/Numeric String)**
   - Ví dụ: `150`, `"150"` (Truy xuất dữ liệu 150 ngày qua).
2. **Preset Chuẩn (Milestones)**
   - Các mốc tính bằng ngày được định nghĩa sẵn:
     - **Tuần**: `"1W"`, `"2W"`, `"3W"`, `"6W"`
     - **Tháng**: `"1M"`, `"2M"`, `"3M"`, `"4M"`, `"5M"`, `"6M"`, `"9M"`, `"18M"`
     - **Năm**: `"1Y"`, `"2Y"`, `"3Y"`, `"5Y"`
3. **Cấu Trúc Động (Dynamic Parsing)**
   - Bạn có thể tùy biến tổ hợp `<Số><Đơn Vị>`:
     - `D` (Ngày), `W` (Tuần), `M` (Tháng ~30 ngày), `Q` (Quý ~90 ngày), `Y` (Năm ~365 ngày).
     - Ví dụ: `"100W"` (100 tuần), `"4Q"` (4 quý), `"10Y"` (10 năm).
4. **Định dạng số nến (Bars)**
   - Khai báo số lượng nến/thanh dữ liệu với hậu tố `b` (Ví dụ: `"100b"` hoặc `100` trong một số context chuyên biệt của Quote Intraday/Lịch sử). Với Macro và Commodity, hệ thống sẽ tự động chuyển đổi sang số ngày tương ứng để duy trì tính tương thích.

### Các Nguồn Dữ Liệu Chính

| Tên | Code | Mô Tả | Ưu Điểm |
|---|---|---|---|
| **VCI** | `vci` | Dữ liệu từ Vietcap | Dữ liệu phong phú, support đầy đủ |
| **VND** | `vnd` | VNDirect | Dữ liệu đầy đủ, nhanh chóng |
| **MAS** | `mas` | Mirae Asset | BCTC định dạng Excel-style |
| **CafeF** | `cafef` | CafeF Vietnam | Dữ liệu phong phú |
| **MBK** | `mbk` | Maybank Kimeng - Kinh tế Vĩ Mô | Dữ liệu kinh tế vĩ mô |
| **KBS** | `kbs` | KIS Berger Sec. | Dữ liệu giao dịch, phái sinh, bảng giá |
| **SPL** | `spl` | Dữ Lệu Hàng Hóa | Giá hàng hóa |
| **MSN** | `msn` | MSN Finance | Chứng khoán quốc tế, crypto, forex |

### Lý Do Sử Dụng Vnstock_data

1. **Toàn Diện**: Cung cấp tất cả loại dữ liệu từ giá, BCTC đến kinh tế vĩ mô
2. **Đáng Tin**: Kết nối từ các website công ty chứng khoán & nguồn dữ lệu uy tín (VCI, VND, VCI,...)
3. **Linh Hoạt**: Dễ dàng chuyển đổi giữa các nguồn
4. **Bảo Trì**: Được update thường xuyên, support tốt
5. **Cộng Đồng**: Có cộng đồng người dùng lớn, tài liệu đầy đủ

### Miễn Trừ Trách Nhiệm

- Dữ liệu được cung cấp **chỉ nhằm mục đích nghiên cứu, giáo dục, sử dụng cá nhân**
- Không sử dụng dữ liệu này làm cơ sở duy nhất cho quyết định giao dịch thực tế
- Dữ liệu có thể không đầy đủ, không liên tục hoặc có sai lệch so với nguồn gốc
- Vnstock và tác giả **không chịu trách nhiệm** về bất kỳ tổn thất nào phát sinh từ việc sử dụng dữ liệu

### Cấu Trúc Tài Liệu Này

Tài liệu được chia thành các phần chính:

1. **[01-overview.md](01-overview.md)** (Tệp này) - Tổng quan, cách sử dụng cơ bản
2. **[02-listing.md](02-listing.md)** - Danh sách niêm yết, phân ngành, chỉ số
3. **[03-quote.md](03-quote.md)** - Lịch sử giá, OHLCV, intraday, price depth
4. **[04-company.md](04-company.md)** - Thông tin công ty, cổ đông, ban lãnh đạo
5. **[05-finance.md](05-finance.md)** - Báo cáo tài chính, chỉ số, kế hoạch
6. **[06-trading.md](06-trading.md)** - Giao dịch, bảng giá, thống kê
7. **[07-market.md](07-market.md)** - Định giá thị trường (P/E, P/B)
8. **[08-insights.md](08-insights.md)** - Top stock (gainer, loser, volume, deal)
9. **[09-macro.md](09-macro.md)** - Kinh tế vĩ mô (GDP, CPI, FDI, tỷ giá)
10. **[10-commodity.md](10-commodity.md)** - Giá hàng hóa (vàng, dầu, khí, nông sản)
11. **[11-fund.md](11-fund.md)** - Dữ liệu quỹ ETF
12. **[12-data-sources.md](12-data-sources.md)** - Ma trận support các nguồn dữ liệu
13. **[13-best-practices.md](13-best-practices.md)** - Best practices và tips sử dụng
14. **[14-unified-ui.md](14-unified-ui.md)** - 🆕 Unified UI: Giao diện hợp nhất thế hệ mới (`show_api`, `show_doc`)
15. **[unified-ui/](./unified-ui/)** - Tài liệu chi tiết từng layer của Unified UI

> **Lưu ý**: Để tìm hiểu chi tiết hơn về các lỗi phổ biến, tips tối ưu, templates sử dụng và so sánh các nguồn dữ liệu, vui lòng xem **[README.md](README.md)**.
