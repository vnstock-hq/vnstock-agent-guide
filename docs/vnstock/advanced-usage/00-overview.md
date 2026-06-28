# Tổng Quan Tùy Chỉnh Nâng Cao (Legacy APIs)

Tài liệu này hướng dẫn bạn cách sử dụng các hàm cấp thấp (Legacy APIs) của Vnstock. Đây là cách tiếp cận truyền thống (trước v3.5.1), yêu cầu bạn tương tác trực tiếp với các lớp xử lý dữ liệu như `Quote`, `Company`, `Listing`, `Finance`, v.v.

---

## 🆚 Sự khác biệt so với Unified UI

Kể từ phiên bản v3.5.1, **Unified UI** (`Market`, `Reference`, `Fundamental`) được giới thiệu làm chuẩn mực mới, trong khi cách gọi hàm cũ được xếp vào nhóm **Advanced Usage** (Tuỳ chỉnh nâng cao).

| Tiêu Chí            | Unified UI (Khuyên dùng)                                    | Advanced Usage (Legacy APIs)                                   |
| ------------------- | ----------------------------------------------------------- | -------------------------------------------------------------- |
| **Tính Trừu Tượng** | Cao. Ẩn đi sự phức tạp của nguồn dữ liệu.                   | Thấp. Tương tác trực tiếp với class từng nghiệp vụ.            |
| **Quản Lý Nguồn**   | Tự động chọn nguồn tốt nhất, tự động fallback.              | Bắt buộc khai báo `source` rõ ràng (ví dụ: `source="vci"`).    |
| **Cấu Trúc**        | Phân tầng theo chuẩn tài chính quốc tế (Market, Reference). | Phân chia theo class chức năng (Quote, Company, Listing).      |
| **Mục Đích**        | Dành cho 95% người dùng, phân tích dữ liệu tiêu chuẩn.      | Dành cho việc cần truy cập dữ liệu đặc thù của 1 nguồn cụ thể. |

## 🎯 Khi nào nên sử dụng Advanced Usage?

Bạn chỉ nên sử dụng các API nâng cao này khi:
1. **Bạn cần dữ liệu đặc thù**: Một số nguồn cung cấp dữ liệu độc quyền không có ở nguồn khác (ví dụ: `capital_history()` chỉ có ở KBS). Unified UI có thể chưa bao bọc (wrap) hết các hàm ngách này.
2. **Bạn muốn kiểm soát nguồn tuyệt đối**: Bạn muốn ép hệ thống chỉ lấy dữ liệu từ một nguồn duy nhất mà không muốn cơ chế tự fallback của Unified UI can thiệp.
3. **Tương thích ngược**: Hệ thống của bạn đã được viết bằng các class cũ (`Quote`, `Company`) từ trước v3.5.1 và bạn chưa có thời gian nâng cấp lên Unified UI.

---

## 🛠 Cách Khởi Tạo & Sử Dụng Cơ Bản

Để sử dụng, bạn cần import trực tiếp class tương ứng và **bắt buộc** truyền tham số `source`.

### Khởi Tạo

```python
from vnstock import Quote, Listing, Company, Finance, Trading
from vnstock.core.types import DataSource

# Khởi tạo class Quote với nguồn VCI
quote = Quote(source="vci", symbol="VCB")
# Hoặc dùng Enum
quote_kbs = Quote(source=DataSource.KBS, symbol="VCB")

# Khởi tạo các class khác
listing = Listing(source="vci")
company = Company(source="vci", symbol="VCB")
finance = Finance(source="vci", symbol="VCB")
trading = Trading(source="vci")
```

### Gọi Hàm

```python
# Lấy giá lịch sử
df = quote.history(start="2024-01-01", end="2024-12-31", interval="1D")

# Lấy thông tin tổng quan công ty
profile = company.overview()

# Lấy báo cáo tài chính
income = finance.income_statement(period="year")
```

---

## 📋 Các Nhóm Hàm Khả Dụng

Dưới đây là bảng tóm tắt các tính năng khả dụng qua Legacy API. Tham khảo các file tiếp theo trong thư mục này để xem chi tiết tham số.

### 1. Quote API - Dữ Liệu Giá (`06-quote-price-api.md`)
| Method          | Mô Tả                        | Sources            |
| --------------- | ---------------------------- | ------------------ |
| `history()`     | Dữ liệu lịch sử OHLCV        | KBS, VCI, MSN, FMP |
| `intraday()`    | Dữ liệu giao dịch trong ngày | KBS, VCI           |
| `price_depth()` | Sổ lệnh (order book)         | KBS, VCI           |

### 2. Company API - Thông Tin Công Ty (`04-company-api.md`)
| Method              | Mô Tả               | Sources       |
| ------------------- | ------------------- | ------------- |
| `overview()`        | Thông tin tổng quan | KBS, VCI, FMP |
| `officers()`        | Ban lãnh đạo        | KBS, VCI      |
| `shareholders()`    | Cổ đông lớn         | KBS, VCI      |
| `subsidiaries()`    | Công ty con         | KBS, VCI      |
| `news()`            | Tin tức             | KBS, VCI      |
| `capital_history()` | Lịch sử vốn         | KBS only      |
| `ratio_summary()`   | Tóm tắt chỉ số      | VCI only      |

### 3. Finance API - Báo Cáo Tài Chính (`07-financial-api.md`)
| Method               | Mô Tả                | Sources       |
| -------------------- | -------------------- | ------------- |
| `income_statement()` | Báo cáo thu nhập     | KBS, VCI, FMP |
| `balance_sheet()`    | Bảng cân đối kế toán | KBS, VCI, FMP |
| `cash_flow()`        | Báo cáo dòng tiền    | KBS, VCI, FMP |
| `ratio()`            | Chỉ số tài chính     | KBS, VCI, FMP |

### 4. Trading API - Dữ Liệu Giao Dịch (`05-trading-api.md`)
| Method            | Mô Tả              | Sources  |
| ----------------- | ------------------ | -------- |
| `price_board()`   | Bảng giá realtime  | KBS, VCI |
| `price_history()` | Lịch sử giá        | VCI only |
| `trading_stats()` | Thống kê giao dịch | VCI only |
| `side_stats()`    | Thống kê mua/bán   | VCI only |

### 5. Listing API - Danh Sách Chứng Khoán (`03-listing-api.md`)
| Method                  | Mô Tả                 | Sources            |
| ----------------------- | --------------------- | ------------------ |
| `all_symbols()`         | Tất cả mã chứng khoán | KBS, VCI, MSN, FMP |
| `symbols_by_exchange()` | Mã theo sàn           | VCI only           |
| `government_bonds()`    | Trái phiếu chính phủ  | VCI only           |
| `indices()`             | Danh sách chỉ số      | VCI, MSN, FMP      |

---

## 🛠 Core Utilities

Các tiện ích cốt lõi của Vnstock vẫn có thể sử dụng độc lập để hỗ trợ các chức năng nâng cao:

- **Market Utilities** (`vnstock.core.utils.market`): `trading_hours()`, `is_trading_hour()`, `market_status()`.
- **Interval Utilities** (`vnstock.core.utils.interval`): Xử lý timeframe.
- **Lookback Utilities** (`vnstock.core.utils.lookback`): Parse các chuỗi khoảng thời gian như `1M`, `100D`.

---

## 🛡️ Xử Lý Lỗi & Retry

Khi tương tác trực tiếp với API, bạn vẫn được hưởng lợi từ cơ chế xử lý lỗi tự động:

```python
from vnstock.config import Config

# Tuỳ chỉnh retry behavior
Config.RETRIES = 3  # Số lần retry
Config.BACKOFF_MULTIPLIER = 2  # Hệ số backoff
Config.BACKOFF_MIN = 1  # Độ trễ tối thiểu (giây)
Config.BACKOFF_MAX = 30  # Độ trễ tối đa (giây)
```

**Các lỗi thường gặp:**
- `RateLimitExceeded`: Xảy ra khi bạn gọi quá số lần giới hạn của hạng thành viên Tài trợ. Tham khảo giới hạn trên trang [Insiders Program](https://vnstocks.com/insiders-program#comparison).
- `NotImplementedError`: Xảy ra khi nguồn bạn chỉ định (ví dụ `msn`) không hỗ trợ chức năng (ví dụ `Finance`). Bạn cần đổi sang nguồn khác hỗ trợ như `vci` hoặc `kbs`.
