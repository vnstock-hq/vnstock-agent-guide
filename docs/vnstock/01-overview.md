# VNStock 3.3.0 - Tổng Quan

## 📖 Giới Thiệu

**VNStock** là thư viện Python mạnh mẽ để lấy dữ liệu chứng khoán Việt Nam từ nhiều nguồn uy tín. Thư viện được thiết kế với kiến trúc provider-based, cho phép bạn dễ dàng chuyển đổi giữa các nguồn dữ liệu khác nhau mà không thay đổi code.

### 🎯 Đặc Điểm Chính

- **Nhiều nguồn dữ liệu**: VCI, TCBS, MSN, và các connectors bên ngoài (FMP, XNO, DNSE, Binance)
- **API thống nhất**: Cùng một interface cho tất cả các nguồn dữ liệu
- **Dữ liệu lịch sử & Real-time**: Giá lịch sử, dữ liệu trong ngày, giá realtime
- **Dữ liệu công ty**: Hồ sơ công ty, cổ đông chính, nhân viên quản lý
- **Dữ liệu tài chính**: Báo cáo tài chính, chỉ số tài chính, các dòng tiền
- **Lọc & Phân loại**: Tìm kiếm theo ngành, sàn giao dịch, chỉ số
- **Xử lý lỗi thông minh**: Retry tự động với exponential backoff

## 🏗️ Kiến Trúc

```
┌─────────────────────────────────────────┐
│         User Code (Your App)            │
├─────────────────────────────────────────┤
│  Quote | Listing | Company | Finance    │  ← Adapter Layer (API thống nhất)
│  Trading | Screener                     │
├─────────────────────────────────────────┤
│  Provider Registry (Dynamic Discovery)  │
├─────────────────────────────────────────┤
│        Explorer (Web Scraping)          │
│  ┌──────────────────────────────────┐   │
│  │ VCI | TCBS | MSN | Fmarket       │   │
│  └──────────────────────────────────┘   │
│                                          │
│    Connector (External APIs)             │
│  ┌──────────────────────────────────┐   │
│  │ FMP | XNO | DNSE | Binance       │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Cách Hoạt Động

1. **Adapter Layer**: Bạn sử dụng các class như `Quote`, `Listing`, `Company` v.v.
2. **Provider Registry**: Thư viện tìm kiếm provider phù hợp dựa trên `source` parameter
3. **Dynamic Method Detection**: Chỉ các phương thức mà provider hỗ trợ mới được gọi
4. **Parameter Filtering**: Tự động lọc tham số để phù hợp với provider signature

## 📊 Nguồn Dữ Liệu

### Explorer (Web Scraping)

| Nguồn | Domain | Hỗ trợ | Phương pháp |
|-------|--------|--------|-----------|
| **VCI** | vci.com.vn | Quote, Listing, Company, Finance, Trading | Web Scraping |
| **TCBS** | tcbs.com.vn | Quote, Listing, Company, Finance, Trading | Web Scraping |
| **MSN** | msn.com | Quote, Listing | Web Scraping |
| **Fmarket** | fmarket.vn | Fund | Web Scraping |

### Connector (API bên ngoài)

| API | Domain | Đặc điểm | Chi phí |
|-----|--------|---------|--------|
| **FMP** | financialmodelingprep.com | Dữ liệu tài chính toàn cầu | Freemium |
| **XNO** | xnodata.com | Dữ liệu chứng khoán Việt Nam | Có phí |
| **DNSE** | dnse.vn | Dữ liệu trao đổi ghi danh | Có phí |

## 📈 Các Loại Dữ Liệu

### 1. Dữ Liệu Giá (Quote Data)

```
- Giá lịch sử: Open, High, Low, Close, Volume
- Dữ liệu trong ngày (Intraday)
- Bảng giá realtime
- Độ sâu giá (Price Depth / Order Book)
```

**Hỗ trợ TimeFrame**: 1m, 5m, 15m, 30m, 1H, 4h, 1D (Daily), 1W (Weekly), 1M (Monthly)

### 2. Dữ Liệu Danh Sách (Listing Data)

```
- Tất cả mã chứng khoán
- Lọc theo sàn giao dịch (HOSE, HNX, UPCOM)
- Lọc theo ngành (ICB Industries)
- Lọc theo chỉ số (VN30, VNMID, VNSML, v.v.)
- Futures, Bonds, Warrants, Funds
```

### 3. Dữ Liệu Công Ty (Company Data)

```
- Hồ sơ công ty
- Thông tin cổ đông chính
- Danh sách nhân viên quản lý
- Công ty con & chi nhánh
- Tin tức & sự kiện
```

### 4. Dữ Liệu Tài Chính (Financial Data)

```
- Báo cáo tài chính:
  ├─ Bảng cân đối kế toán (Balance Sheet)
  ├─ Khoản lợi nhập (Income Statement)
  ├─ Lưu chuyển tiền tệ (Cash Flow)
  └─ Chỉ số tài chính (Ratios)
- Theo kỳ: Hàng quý (Quarter) hoặc hàng năm (Year)
```

### 5. Dữ Liệu Giao Dịch (Trading Data)

```
- Khối lượng giao dịch
- Giá trị giao dịch
- Giao dịch cổ đông lớn
- Lịch sử chia cổ tức
```

## 🔄 TimeFrame (Khung Thời Gian)

VNStock hỗ trợ các khung thời gian sau:

| Khung | Mã | Mô tả |
|------|-----|--------|
| 1 Phút | `1m` | Dữ liệu mỗi 1 phút |
| 5 Phút | `5m` | Dữ liệu mỗi 5 phút |
| 15 Phút | `15m` | Dữ liệu mỗi 15 phút |
| 30 Phút | `30m` | Dữ liệu mỗi 30 phút |
| 1 Giờ | `1H` | Dữ liệu mỗi 1 giờ |
| 4 Giờ | `4h` | Dữ liệu mỗi 4 giờ |
| 1 Ngày | `1D` hoặc `DAILY` | Dữ liệu hàng ngày |
| 1 Tuần | `1W` hoặc `WEEKLY` | Dữ liệu hàng tuần |
| 1 Tháng | `1M` hoặc `MONTHLY` | Dữ liệu hàng tháng |

```python
from vnstock.core.types import TimeFrame

# Sử dụng enum
df = quote.history(
    symbol="VCI",
    start_date="2024-01-01",
    end_date="2024-12-31",
    resolution=TimeFrame.DAILY  # hoặc TimeFrame.DAY_1
)

# Hoặc sử dụng string trực tiếp
df = quote.history(
    symbol="VCI",
    start_date="2024-01-01",
    end_date="2024-12-31",
    resolution="1D"
)
```

## 💱 Sàn Giao Dịch (Exchanges)

```
- HOSE: Sở giao dịch Hà Nội (HOSE) - Thị trường chính
- HNX: Sở giao dịch Hà Nội (HNX) - Thị trường phụ
- UPCOM: Thị trường chứng khoán chưa niêm yết (UPCOM)
```

```python
from vnstock.constants import EXCHANGES

# Danh sách tất cả sàn
print(EXCHANGES)
# Output:
# {
#     'HOSE': 'Sở giao dịch Hà Nội (HOSE)',
#     'HNX': 'Sở giao dịch Hà Nội (HNX)',
#     'UPCOM': 'Sở giao dịch Hà Nội (UPCOM)',
# }
```

## 📑 Chỉ Số Thị Trường (Indices)

VNStock cung cấp 20+ chỉ số thị trường được phân loại:

### 📊 Chỉ Số HOSE (6 chỉ số)

```
- VN30: 30 cổ phiếu vốn hóa lớn nhất & thanh khoản tốt nhất
- VN100: 100 cổ phiếu có vốn hoá lớn nhất HOSE
- VNMID: Mid-Cap Index - nhóm cổ phiếu vốn hóa trung bình
- VNSML: Small-Cap Index - nhóm cổ phiếu vốn hóa nhỏ
- VNALL: Tất cả cổ phiếu trên HOSE và HNX
- VNSI: Vietnam Small-Cap Index
```

### 🏭 Chỉ Số Ngành (10 chỉ số ICB)

```
- VNIT: Công nghệ thông tin
- VNIND: Công nghiệp
- VNCONS: Hàng tiêu dùng
- VNCOND: Hàng tiêu dùng thiết yếu
- VNHEAL: Chăm sóc sức khoẻ
- VNENE: Năng lượng
- VNUTI: Dịch vụ tiện ích
- VNREAL: Bất động sản
- VNFIN: Tài chính
- VNMAT: Nguyên vật liệu
```

### 💎 Chỉ Số Đầu Tư (3 chỉ số)

```
- VNDIAMOND: Chỉ số các cổ phiếu có triển vọng lớn
- VNFINLEAD: Chỉ số tài chính đầu ngành
- VNFINSELECT: Chỉ số tài chính được chọn lọc
```

```python
from vnstock.constants import INDICES_INFO, INDEX_GROUPS

# Thông tin chi tiết về chỉ số
vn30_info = INDICES_INFO['VN30']
print(vn30_info)
# Output:
# {
#     'name': 'VN30',
#     'description': '30 cổ phiếu vốn hóa lớn nhất & thanh khoản tốt nhất HOSE',
#     'full_name': 'VN30 Index',
#     'group': 'HOSE Indices',
#     'index_id': 5,
# }

# Danh sách theo nhóm
hose_indices = INDEX_GROUPS['HOSE Indices']
print(hose_indices)
# Output: ['VN30', 'VNMID', 'VNSML', 'VN100', 'VNALL', 'VNSI']
```

## 🏭 Ngành Công Nghiệp (Sectors)

VNStock sử dụng phân loại ICB (Industry Classification Benchmark) với 10 ngành chính:

```python
from vnstock.constants import SECTOR_IDS

# Danh sách tất cả ngành
for sector_id, sector_name in SECTOR_IDS.items():
    print(f"{sector_id}: {sector_name}")

# Output:
# 126: Dịch vụ viễn thông
# 130: Hàng tiêu dùng
# 133: Hàng tiêu dùng thiết yếu
# 135: Chăm sóc sức khoẻ
# 138: Tài chính
# 143: Nguyên vật liệu
# 150: Dịch vụ tiện ích
# 154: Năng lượng
# 155: Công nghiệp
# 159: Công nghệ thông tin
# 166: Bất động sản
```

## 🔌 Cách Sử Dụng Cơ Bản

### Khởi Tạo

```python

from vnstock import Quote, Listing, Company, Finance

# Quote - Giá chứng khoán
quote = Quote(source="vci", symbol="VCI")

# Listing - Danh sách chứng khoán
listing = Listing(source="vci")

# Company - Dữ liệu công ty
company = Company(source="vci", symbol="VCI")

# Finance - Dữ liệu tài chính
finance = Finance(source="vci", symbol="VCI")
```

### Parameters Phổ Biến

Tất cả adapter đều hỗ trợ các parameters:

```python
# Common parameters
Quote(
    source="vci",           # Nguồn dữ liệu: vci, tcbs, msn, etc.
    symbol="VCI",           # Mã chứng khoán
    random_agent=False,     # Sử dụng random user agent
    show_log=False          # Hiển thị log chi tiết
)
```

## 🔄 Source (Nguồn Dữ Liệu)

Bạn có thể chỉ định source một cách rõ ràng hoặc sử dụng giá trị mặc định:

```python
from vnstock.core.types import DataSource

# Liệt kê tất cả available sources
print(DataSource.all_sources())
# Output: ['vci', 'tcbs', 'msn', 'dnse', 'binance', 'fmp', 'xno', 'fmarket']

# Sử dụng enum
quote_vci = Quote(source=DataSource.VCI, symbol="VCI")
quote_tcbs = Quote(source=DataSource.TCBS, symbol="VCI")
quote_msn = Quote(source=DataSource.MSN, symbol="VCI")
```

## 🛡️ Xử Lý Lỗi & Retry

VNStock tự động xử lý lỗi tạm thời với:

- **Retry tự động**: Tối đa 5 lần (có thể cấu hình)
- **Exponential Backoff**: Tăng độ trễ giữa các lần thử
- **Timeout thông minh**: Tránh treo khi kết nối chậm

```python
from vnstock.config import Config

# Tuỳ chỉnh retry behavior
Config.RETRIES = 3  # Số lần retry
Config.BACKOFF_MULTIPLIER = 2  # Hệ số backoff
Config.BACKOFF_MIN = 1  # Độ trễ tối thiểu (giây)
Config.BACKOFF_MAX = 30  # Độ trễ tối đa (giây)
```

## 📚 Cấu Trúc Dữ Liệu Trả Về

### DataFrame (Pandas)

Hầu hết các phương thức trả về `pd.DataFrame`:

```python
df = quote.history(
    symbol="VCI",
    start_date="2024-01-01",
    end_date="2024-12-31"
)

# Output: DataFrame với các cột
# Columns: time, open, high, low, close, volume, value
#
#                 time   open   high    low  close    volume
# 0      2024-01-01  21.00  21.50  20.80  21.40  1234567
# 1      2024-01-02  21.40  21.80  21.10  21.50  2345678
# ...
```

### Dictionary

Một số phương thức trả về `dict`:

```python
profile = company.overview()

# Output: Dictionary với thông tin công ty
# {
#     'symbol': 'VCI',
#     'company_name': 'VCI Trading & Investment Joint Stock Company',
#     'exchange': 'HOSE',
#     'industry': 'Real Estate',
#     'website': 'https://...',
#     ...
# }
```

### List

Danh sách:

```python
symbols = listing.all_symbols()

# Output: List of strings
# ['AAA', 'AAH', 'AAT', 'ABS', 'ABT', 'AC1', 'ACB', ...]
```

## ✅ Kiểm Tra Lỗi Thường Gặp

### 1. ModuleNotFoundError

```python
# ❌ Sai
from vnstock import Quote

# ✅ Đúng (dev version)
import sys
sys.path.insert(0, './private_packages')
from vnstock import Quote
```

### 2. ValueError: Invalid Source

```python
# ❌ Sai
quote = Quote(source="invalid_source", symbol="VCI")

# ✅ Đúng
quote = Quote(source="vci", symbol="VCI")
```

### 3. NotImplementedError

```python
# ❌ Sai - MSN không hỗ trợ Finance
finance = Finance(source="msn", symbol="VCI")
df = finance.balance_sheet()  # NotImplementedError

# ✅ Đúng - Sử dụng VCI hoặc TCBS
finance = Finance(source="vci", symbol="VCI")
df = finance.balance_sheet()
```

## 🔗 Bước Tiếp Theo

1. **[02-Installation](02-installation.md)** - Cài đặt & cấu hình
2. **[03-Listing API](03-listing-api.md)** - Tìm kiếm chứng khoán
3. **[04-Quote & Price](04-quote-price-api.md)** - Giá lịch sử & realtime
4. **[05-Financial API](05-financial-api.md)** - Dữ liệu tài chính
5. **[06-Connector Guide](06-connector-guide.md)** - API bên ngoài
6. **[07-Best Practices](07-best-practices.md)** - Mẹo & kinh nghiệm

---

**Last Updated**: 2024-12-03  
**Version**: 3.3.0  
**Status**: Actively Maintained
