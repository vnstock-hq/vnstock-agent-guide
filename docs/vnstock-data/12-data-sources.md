# Data Sources Matrix - Ma Trận Hỗ Trợ Nguồn Dữ Liệu

**Tài liệu này là index toàn diện giúp bạn lựa chọn đúng nguồn dữ liệu cho từng ngữ cảnh sử dụng.** Hiện tại, Vnstock_data hỗ trợ 8 nguồn dữ liệu chính, mỗi nguồn có điểm mạnh riêng. Cấu trúc thư viện được thiết kế tương đồng thư viện Vnstock bản mã nguồn mở, giúp bạn dễ dàng chuyển đổi các chức năng khi tham gia gói tài trợ và sử dụng quyền lợi của mình.

## Tóm Tắt Nhanh - Quick Reference

| Lớp       | VCI | VND | MAS | CafeF | MBK | SPL | Fmarket | Chủ yếu dùng cho                  |
| --------- | :-: | :-: | :-: | :---: | :-: | :-: | :-----: | --------------------------------- |
| Listing   |  ✅  |  ✅  |  -  |   -   |  -  |  -  |    -    | Danh sách cổ phiếu, ngành, chỉ số |
| Quote     |  ✅  |  ✅  |  ✅  |   -   |  -  |  -  |    -    | Lịch sử giá OHLCV                 |
| Company   |  ✅  |  -  |  -  |   -   |  -  |  -  |    -    | Thông tin công ty                 |
| Finance   |  ✅  |  ✅  |  ✅  |   -   |  -  |  -  |    -    | Báo cáo tài chính                 |
| Trading   |  ✅  |  -  |  -  |   ✅   |  -  |  -  |    -    | Dữ liệu giao dịch chi tiết        |
| Market    |  -  |  ✅  |  -  |   -   |  -  |  -  |    -    | Định giá P/E, P/B                 |
| Insights  |  -  |  ✅  |  -  |   -   |  -  |  -  |    -    | Top cổ phiếu, insights thị trường |
| Macro     |  -  |  -  |  -  |   -   |  ✅  |  -  |    -    | Dữ liệu kinh tế vĩ mô             |
| Commodity |  -  |  -  |  -  |   -   |  -  |  ✅  |    -    | Giá hàng hóa (vàng, dầu, khí)     |
| Fund      |  -  |  -  |  -  |   -   |  -  |  -  |    ✅    | Quỹ ETF, NAV, cấu trúc danh mục   |

## Nguồn Dữ Liệu Chi Tiết

### 1. VCI - Nguồn Dữ Liệu Toàn Diện

**Đặc điểm**:
- ✅ Đầy đủ nhất: Hỗ trợ tất cả class chính
- ✅ Dữ liệu lịch sử dài (kể từ 27/8/2000)
- ✅ Cổ phiếu, chỉ số, trái phiếu, hợp đồng tương lai, chứng quyền
- ✅ Thông tin công ty chi tiết (cổ đông, ban lãnh đạo, công ty con)
- ⚠️ Thường gặp hạn chế truy cập khi sử dụng trên các dịch vụ Google Cloud như Google Colab, Kaggle do bị chặn dải IP từ server dịch vụ.
- ⚠️ Một số nhóm dữ liệu đôi khi không trùng khớp với dữ liệu tương đương từ các nguồn khác.

**Hỗ trợ**:

| Lớp         | Phương Thức           | Ghi Chú                                  |
| ----------- | --------------------- | ---------------------------------------- |
| **Listing** | all_symbols           | 1727 mã cổ phiếu, chỉ số                 |
|             | industry              | Danh sách ngành ICB                      |
|             | symbols_by_industries | Cổ phiếu theo ngành (10 cột ICB)         |
|             | symbols_by_exchange   | Cổ phiếu theo sàn HOSE/HNX/UPCOM         |
|             | symbols_by_group      | VN30, VN100, HNX30... (returns Series)   |
|             | industries_icb        | Chi tiết chuẩn ICB 4 cấp                 |
|             | all_future_indices    | Danh sách hợp đồng tương lai             |
|             | all_government_bonds  | Danh sách OBond, T-bond                  |
|             | all_covered_warrant   | Danh sách chứng quyền (305+)             |
|             | all_bonds             | Danh sách trái phiếu doanh nghiệp (81+)  |
| **Quote**   | history               | OHLCV từ 2000, interval: 1m-1M           |
|             | intraday              | Khớp lệnh chi tiết trong ngày            |
|             | price_depth           | Bước giá, dư mua/bán                     |
| **Company** | overview              | Info cơ bản công ty                      |
|             | shareholders          | Danh sách cổ đông lớn                    |
|             | officers              | Ban lãnh đạo                             |
|             | subsidiaries          | Công ty con, liên kết                    |
|             | events                | Sự kiện (tách cổ phiếu, thưởng...)       |
|             | news                  | Tin tức công ty                          |
|             | reports               | Báo cáo từ các SSC                       |
|             | trading_stats         | Thống kê giao dịch                       |
|             | ratio_summary         | Tóm tắt chỉ số tài chính                 |
| **Finance** | balance_sheet         | Bảng cân đối kế toán                     |
|             | income_statement      | Báo cáo kết quả KD                       |
|             | cashflow              | Báo cáo lưu chuyển tiền tệ               |
|             | ratio                 | Chỉ số tài chính                         |
|             | note                  | Thuyết minh BCTC                         |
| **Trading** | price_board           | Bảng giá realtime (70 cột)               |
|             | price_history         | Lịch sử giá OHLCV                        |
|             | trading_stats         | Thống kê giao dịch (trị giá, khối lượng) |
|             | side_stats            | Cung cầu (dư mua/bán lũy tích)           |

**Khi nào dùng VCI?**
- ✅ Cần thông tin công ty chi tiết
- ✅ Cần danh sách đầy đủ (ngành, trái phiếu, hợp đồng tương lai)
- ✅ Cần BCTC đầy đủ (cảnh báo: cấu trúc khác MAS)
- ✅ Phân tích danh mục lâu dài

### 2. VND - Dữ liệu dự phòng ổn định

**Đặc điểm**:
- ✅ Tốc độ nhanh
- ✅ Định giá thị trường (P/E, P/B theo thời gian)
- ✅ Insights thị trường (top gainer, loser, nước ngoài)
- ✅ Hỗ trợ interval phút chi tiết (1m, 5m, 15m, 30m)
- ⚠️ Ít phương thức hơn VCI, hiện tại chỉ tập trung vào dữ liệu niêm yết, giá/khối lượng lịch sử và khám phá cơ hội đầu tư

**Hỗ trợ**:

| Lớp | Phương Thức | Đặc Điểm |
|---|---|---|
| **Listing** | all_symbols | 1727 mã (nhanh hơn VCI) |
| **Quote** | history | OHLCV 6 cột (time, open, high, low, close, volume) |
| | intraday | Khớp lệnh theo phút |
| | price_depth | Mức giá, dư mua/bán |
| **Finance** | balance_sheet | BCTC cơ bản |
| | income_statement | KQH KD cơ bản |
| | cashflow | Lưu chuyển tiền tệ cơ bản |
| | ratio | Chỉ số cơ bản |
| **Market** | pe | P/E ratio lịch sử (VN Index) |
| | pb | P/B ratio lịch sử |
| | evaluation | Định giá thị trường |
| **Insights** | gainer | Top tăng giá (15 cột) |
| | loser | Top giảm giá |
| | value | Top theo trị giá giao dịch |
| | volume | Top theo khối lượng |
| | deal | Top giao dịch thỏa thuận |
| | foreign_buy | Top NĐTNN mua ròng (3 cột) |
| | foreign_sell | Top NĐTNN bán ròng |

**Khi nào dùng VND?**
- ✅ Sử dụng làm nguồn dữ liệu bổ trợ cho các nhóm thông tin về giao dịch, niêm yết bên cạnh VCI có thể bị chặn hoặc dùng quá phổ biến do có trong thư viện nguồn mở Vnstock
- ✅ Phân tích kỹ thuật (interval phút)
- ✅ Theo dõi định giá thị trường (P/E, P/B)
- ✅ Phân tích khối ngoại
- ✅ Top stocks insights

**Ví dụ**: Quote.history với VND là nhanh nhất cho backtest dữ liệu lớn.

### 3. MAS - Dữ Liệu BCTC Chi Tiết & Excel-style

**Đặc điểm**:
- ✅ BCTC chi tiết, phân cấp cha-con
- ✅ Kế hoạch năm (annual_plan) - duy nhất MAS có
- ✅ Định dạng Excel-style, giữ nguyên cấu trúc thông thường
- ✅ Phù hợp phân tích tài chính chuyên sâu
- ⚠️ Cấu trúc phân cấp cha con, có thể có tên cột trùng lặp cần xử lý thêm nếu viết thuật toán với Pandas

**Hỗ trợ**:

| Lớp | Phương Thức | Đặc Điểm |
|---|---|---|
| **Quote** | history | OHLCV như VND |
| **Finance** | balance_sheet | BCTC chi tiết, phân cấp |
| | income_statement | KQH KD chi tiết |
| | cashflow | Lưu chuyển tiền tệ chi tiết |
| | ratio | Chỉ số tài chính |
| | annual_plan | Kế hoạch năm (📌 chỉ MAS có) |

**Cấu Trúc Dữ Liệu MAS**:
```
Excel-style với cấu trúc cha-con:
├─ Tài sản (Assets)
│  ├─ Tài sản hiện hành (Current Assets)
│  │  ├─ Tiền mặt
│  │  ├─ Khoản phải thu
│  │  └─ Hàng tồn kho
│  └─ Tài sản cố định (Fixed Assets)
│     └─ ...
├─ Nợ (Liabilities)
└─ Vốn (Equity)
```

**Khi nào dùng MAS?**
- ✅ Phân tích tài chính chuyên sâu
- ✅ So sánh chi tiết cha-con (ví dụ: phân loại tài sản)
- ✅ Cần kế hoạch năm
- ✅ Export BCTC với định dạng Excel

### 4. CafeF - Dữ Liệu Giao Dịch Lịch Sử

**Đặc điểm**:
- ✅ Giao dịch chi tiết (nước ngoài, tự doanh, nội bộ)
- ✅ Thống kê đặt lệnh chi tiết
- ✅ Phù hợp phân tích khối ngoại, tổ chức
- ⚠️ Chỉ hỗ trợ Trading
- ⚠️ API đôi khi không ổn định

**Hỗ trợ**:

| Lớp | Phương Thức | Ghi Chú |
|---|---|---|
| **Trading** | price_history | Lịch sử giá |
| | foreign_trade | Giao dịch nước ngoài (8 cột) |
| | prop_trade | Giao dịch tự doanh (4 cột) |
| | order_stats | Thống kê đặt lệnh (7 cột) |
| | insider_deal | Giao dịch nội bộ |

**Khi nào dùng CafeF?**
- ✅ Phân tích khối ngoại chi tiết
- ✅ Phân tích tự doanh
- ✅ Phân tích giao dịch nội bộ

### 5. MBK - Dữ Liệu Kinh Tế Vĩ Mô

**Đặc điểm**:
- ✅ Dữ liệu kinh tế Việt Nam tương ứng dữ liệu từ Vietstock
- ✅ Đầy đủ các dữ liệu kinh tế vĩ mô phổ biến: GDP, CPI, FDI, tỷ giá, tiền tệ, vv

**Hỗ trợ**:

| Lớp       | Phương Thức      | Số Dòng | Cột                                       |
| --------- | ---------------- | ------- | ----------------------------------------- |
| **Macro** | gdp              | 255     | 7 (tên, giá trị, đơn vị, loại báo cáo...) |
|           | cpi              | 512     | 5                                         |
|           | industry_prod    | -       | -                                         |
|           | import_export    | -       | -                                         |
|           | retail           | -       | -                                         |
|           | fdi              | 68      | 6                                         |
|           | money_supply     | 128     | 5                                         |
|           | exchange_rate    | 54      | 5                                         |
|           | population_labor | -       | -                                         |

**Dữ Liệu Mẫu**:
- **GDP Q3/2025**: Tổng GDP 8.23%, Nông nghiệp 3.74%
- **CPI 11/2025**: CPI tổng 0.05%, Thực phẩm 0.01%
- **FDI**: FDI đăng ký 2.98 tỷ USD, giải ngân 2.50 tỷ USD
- **Exchange Rate**: VND/USD = 25155

**Khi nào dùng MBK?**
- ✅ Phân tích vĩ mô
- ✅ Tìm correlation Macro ↔ Stock

### 6. SPL - Dữ Liệu Hàng Hóa (Commodity)

**Đặc điểm**:
- ✅ Duy nhất nguồn hàng hóa
- ✅ Vàng, dầu, khí, thép, nông sản
- ⚠️ Dữ liệu thỉnh thoảng bị cách

**Hỗ trợ (15 loại hàng hóa)**:

| Hàng Hóa | Loại | Mẫu Dữ Liệu |
|---|---|---|
| gold_vn | 2 cột (buy, sell) | 152600/154600 VND/chỉ |
| gold_global | 5 cột OHLCV | Giá vàng thế giới USD/oz |
| gas_vn | 3 cột | RON95, RON92, oil_do (VND/lít) |
| oil_crude | 5 cột OHLCV | 59.46 USD/barrel |
| gas_natural | 5 cột OHLCV | USD/MMBtu |
| steel_hrc | 5 cột OHLCV | 903 USD/tấn |
| steel_d10 | 5 cột OHLCV | VND/tấn |
| iron_ore | 5 cột OHLCV | USD/tấn |
| coke | 5 cột OHLCV | USD/tấn |
| fertilizer_ure | 5 cột OHLCV | USD/tấn |
| soybean | 5 cột OHLCV | USD/bushel |
| corn | 5 cột OHLCV | USD/bushel |
| sugar | 5 cột OHLCV | USD/pound |
| pork_north_vn | 1 cột (close) | 54400 VND/kg |
| pork_china | 1 cột (close) | CNY/kg |

**Khi nào dùng SPL?**
- ✅ Phân tích ngành khoáng sản, năng lượng
- ✅ Phân tích nông sản
- ✅ Hedging risk hàng hóa

### 7. Fmarket - Dữ Liệu Quỹ Đầu Tư

**Đặc điểm**:
- ✅ Duy nhất nguồn quỹ đầu tư
- ✅ 58 quỹ, NAV lịch sử, cấu trúc danh mục

**Hỗ trợ**:

| Lớp | Phương Thức | Dữ Liệu |
|---|---|---|
| **Fund** | listing | 58 quỹ, 21 cột (NAV, phí, lợi suất) |
| | filter | Tìm quỹ theo mã |
| | top_holding | 10 cổ phiếu hàng đầu (6 cột) |
| | industry_holding | Cấu trúc ngành (14 ngành) |
| | nav_report | Lịch sử NAV (2000+ dòng cho SSISCA) |
| | asset_holding | Cấu trúc tài sản (cổ phiếu/trái phiếu/tiền) |

**Mẫu Dữ Liệu SSISCA**:
- NAV hiện tại: 44,822.70
- Phí quản lý: 1.75%
- Top holdings: MWG 8.48%, MBB 6.42%, HPG 6.13%
- Asset: 95.66% cổ phiếu, 4.06% tiền, 0.28% khác

**Khi nào dùng Fmarket?**
- ✅ Phân tích quỹ ETF
- ✅ So sánh lợi suất quỹ
- ✅ Phân tích danh mục quỹ

## Quyết Định Nhanh - Decision Tree

```
Bạn cần gì?

1️⃣ Giá lịch sử cổ phiếu?
   → Nhanh? → VND ✅
   → Đầy đủ? → VCI ✅
   → Interval phút? → VND ✅

2️⃣ Thông tin công ty?
   → Chỉ VCI ✅
   
3️⃣ BCTC chi tiết?
   → Phân cấp? → MAS ✅
   → Đơn giản? → VCI ✅

4️⃣ Giao dịch nước ngoài?
   → CafeF ✅

5️⃣ Định giá thị trường (P/E, P/B)?
   → VND ✅

6️⃣ Top cổ phiếu, insights?
   → VND ✅

7️⃣ Dữ liệu kinh tế?
   → MBK ✅

8️⃣ Hàng hóa?
   → SPL ✅

9️⃣ Quỹ ETF?
   → Fmarket ✅
```

## Workflow Khuyến Nghị

### Workflow 1: Phân Tích Kỹ Thuật (Technical Analysis)

```python
Quote (VND) 
  ↓ history + intraday (interval phút)
  ↓
TA Indicators (SMA, RSI, MACD, Bollinger)
  ↓
Trading Signals (Buy/Sell)
```

**Tại sao VND?** Nhanh, hỗ trợ interval phút

### Workflow 2: Phân Tích Cơ Bản (Fundamental Analysis)

```python
Listing (VCI) → symbols_by_industries
  ↓
Company (VCI) → overview, shareholders
  ↓
Finance (VCI hoặc MAS) → balance_sheet, income_statement
  ↓
Valuation (So sánh P/E, ROE, ROA)
```

**Tại sao VCI?** Đầy đủ thông tin công ty

### Workflow 3: Phân Tích Thị Trường (Market Analysis)

```python
Listing (VCI)
  ↓
Market (VND) → PE, PB, evaluation
  ↓
TopStock (VND) → gainer, loser, foreign_buy
  ↓
Market Insights
```

**Tại sao VND?** Định giá + insights

### Workflow 4: Phân Tích Khối Ngoại (Foreign Flow)

```python
Trading (CafeF) → foreign_trade
  ↓
TopStock (VND) → foreign_buy, foreign_sell
  ↓
Time Series Analysis
```

### Workflow 5: Phân Tích Macroeconomic

```python
Macro (MBK) → GDP, CPI, FDI
  ↓
Commodity (SPL) → oil, gold, steel
  ↓
Correlation with Market (VND)
```

## Error Handling & Fallback

### Fallback Strategy

Áp dụng với các loại dữ liệu có cấu trúc thống nhất xuyên suốt các nguồn được hỗ trợ và đã chuẩn hoá ví dụ dữ liệu OHLCV.

```python
def get_data_with_fallback(symbol):
    sources = ['vnd', 'vci']
    
    for source in sources:
        try:
            quote = Quote(source=source, symbol=symbol)
            return quote.history(...)
        except:
            continue
    
    raise Exception(f"All sources {sources} failed")
```

**Fallback Priority**:
1. VND (nhanh)
2. VCI (đầy đủ)
3. MAS (nếu cần BCTC chi tiết)

## Tóm Tắt & Đề Xuất

| Tình Huống | Nguồn Khuyến Nghị | Lý Do |
|---|---|---|
| Backtest dữ liệu lớn | VND | Tốc độ cao |
| Phân tích fundamental | VCI | Đầy đủ thông tin |
| BCTC chi tiết | MAS | Phân cấp cha-con |
| Khối ngoại | CafeF | Dữ liệu chi tiết |
| Định giá thị trường | VND | Chỉ VND có |
| Insights thị trường | VND | Chỉ VND có |
| Macro & Commodity | MBK & SPL | Duy nhất |
| Quỹ ETF | Fmarket | Duy nhất |

## Các Lưu Ý Quan Trọng

⚠️ **Chỉ nên dùng 1 nguồn chính** để tránh không nhất quán dữ liệu
⚠️ **Cache dữ liệu** nếu sử dụng API tương tự liên tục
⚠️ **Rate limiting** - không call API quá nhanh
⚠️ **Kiểm tra dữ liệu** - validate OHLC logic (high ≥ low, etc.)
✅ **Fallback** - luôn chuẩn bị phương án B nếu API chính down

## Chi Tiết Từng Lớp

### 1. Listing (Danh Sách Niêm Yết)

| Phương Thức | VCI | VND | Ghi Chú |
|---|:---:|:---:|---|
| all_symbols | ✅ | ✅ | Tất cả mã niêm yết |
| industry | ✅ | ❌ | Danh sách ngành ICB |
| symbols_by_industries | ✅ | ❌ | Cổ phiếu theo ngành |
| symbols_by_exchange | ✅ | ❌ | Cổ phiếu theo sàn giao dịch |
| symbols_by_group | ✅ | ❌ | Cổ phiếu theo chỉ số (VN30, VN100...) |
| industries_icb | ✅ | ❌ | Chi tiết ngành ICB |
| all_future_indices | ✅ | ❌ | Danh sách hợp đồng tương lai |
| all_government_bonds | ✅ | ❌ | Danh sách trái phiếu chính phủ |
| all_covered_warrant | ✅ | ❌ | Danh sách chứng quyền |
| all_bonds | ✅ | ❌ | Danh sách trái phiếu doanh nghiệp |

**Khuyến Nghị**: Sử dụng VCI cho danh sách đầy đủ.

### 2. Quote (Lịch Sử Giá)

| Phương Thức | VCI | VND | MAS | Ghi Chú |
|---|:---:|:---:|:---:|---|
| history | ✅ | ✅ | ✅ | Giá OHLCV |
| intraday | ✅ | ✅ | ❌ | Khớp lệnh trong ngày |
| price_depth | ✅ | ✅ | ❌ | Bước giá, dư mua/bán |

**Khuyến Nghị**: VCI & VND đầy đủ. VND thường nhanh hơn.

### 3. Company (Thông Tin Công Ty)

| Phương Thức | VCI | Ghi Chú |
|---|:---:|---|
| overview | ✅ | Thông tin tổng quan công ty |
| shareholders | ✅ | Cổ đông lớn |
| officers | ✅ | Ban lãnh đạo |
| subsidiaries | ✅ | Công ty con, liên kết |
| events | ✅ | Sự kiện công ty (tách cổ phiếu, thưởng...) |
| news | ✅ | Tin tức công ty |
| reports | ✅ | Báo cáo phân tích từ các công ty chứng khoán |
| trading_stats | ✅ | Thống kê giao dịch tổng hợp |
| ratio_summary | ✅ | Tóm tắt chỉ số tài chính |

**Khuyến Nghị**: Chỉ VCI hỗ trợ. Tất cả dữ liệu công ty chỉ lấy từ VCI.

### 4. Finance (Báo Cáo Tài Chính)

| Phương Thức | VCI | MAS | Ghi Chú |
|---|:---:|:---:|---|
| balance_sheet | ✅ | ✅ | Bảng cân đối kế toán |
| income_statement | ✅ | ✅ | Báo cáo kết quả kinh doanh |
| cashflow | ✅ | ✅ | Báo cáo lưu chuyển tiền tệ |
| ratio | ✅ | ✅ | Chỉ số tài chính |
| note | ✅ | ❌ | Thuyết minh BCTC |
| annual_plan | ❌ | ✅ | Kế hoạch năm |

**Lưu Ý**: 
- **VCI**: Cấu trúc dữ liệu đơn giản, dễ làm việc, thích hợp cho phân tích
- **MAS**: Cấu trúc Excel-style, phân cấp cha-con, chi tiết hơn

**Khuyến Nghị**: 
- Dùng VCI cho phân tích đơn giản
- Dùng MAS khi cần chi tiết và phân cấp

### 5. Trading (Dữ Liệu Giao Dịch)

| Phương Thức | VCI | CafeF | Ghi Chú |
|---|:---:|:---:|---|
| price_board | ✅ | ❌ | Bảng giá realtime |
| price_history | ✅ | ✅ | Lịch sử giá (mỗi ngày) |
| trading_stats | ✅ | ❌ | Thống kê giao dịch chi tiết |
| side_stats | ✅ | ❌ | Cung cầu (dư mua/bán lũy tích) |
| foreign_trade | ❌ | ✅ | Giao dịch nước ngoài |
| prop_trade | ❌ | ✅ | Giao dịch tự doanh |
| order_stats | ❌ | ✅ | Thống kê đặt lệnh |
| insider_deal | ❌ | ✅ | Giao dịch nội bộ |

**Khuyến Nghị**:
- VCI: Dữ liệu giao dịch cơ bản
- CafeF: Dữ liệu giao dịch chi tiết (nước ngoài, tự doanh, nội bộ)

### 6. Market (Định Giá Thị Trường)

| Phương Thức | VND | Ghi Chú |
|---|:---:|---|
| pe | ✅ | P/E Ratio theo thời gian |
| pb | ✅ | P/B Ratio theo thời gian |
| evaluation | ✅ | Lịch sử định giá thị trường |

**Khuyến Nghị**: Chỉ VND hỗ trợ dữ liệu định giá.

### 7. Insights / TopStock (Top Cổ Phiếu)

| Phương Thức | VND | Ghi Chú |
|---|:---:|---|
| gainer | ✅ | Top cổ phiếu tăng giá |
| loser | ✅ | Top cổ phiếu giảm giá |
| value | ✅ | Top theo giá trị giao dịch |
| volume | ✅ | Top theo khối lượng giao dịch |
| deal | ✅ | Top theo giao dịch thỏa thuận |
| foreign_buy | ✅ | Top NĐTNN mua ròng |
| foreign_sell | ✅ | Top NĐTNN bán ròng |

**Khuyến Nghị**: Chỉ VND cung cấp insights thị trường.

### 8. Macro (Kinh Tế Vĩ Mô)

| Phương Thức | MBK | Ghi Chú |
|---|:---:|---|
| gdp | ✅ | GDP theo quý/năm |
| cpi | ✅ | Chỉ số giá tiêu dùng |
| industry_prod | ✅ | Chỉ số sản xuất công nghiệp |
| import_export | ✅ | Xuất-nhập khẩu hàng hóa |
| retail | ✅ | Doanh thu bán lẻ tiêu dùng |
| fdi | ✅ | Vốn đầu tư trực tiếp nước ngoài |
| money_supply | ✅ | Cung tiền |
| exchange_rate | ✅ | Tỷ giá ngoại tệ |
| population_labor | ✅ | Thống kê dân số, lao động |

**Khuyến Nghị**: Chỉ MBK cung cấp dữ liệu kinh tế vĩ mô.

### 9. Commodity (Giá Hàng Hóa)

| Phương Thức | SPL | Ghi Chú |
|---|:---:|---|
| gold_vn | ✅ | Giá vàng Việt Nam |
| gold_global | ✅ | Giá vàng thế giới |
| gas_vn | ✅ | Giá xăng/dầu diesel VN |
| oil_crude | ✅ | Giá dầu thô thế giới |
| gas_natural | ✅ | Giá khí thiên nhiên |
| coke | ✅ | Giá than cốc |
| steel_d10 | ✅ | Giá thép D10 VN |
| iron_ore | ✅ | Giá quặng sắt thế giới |
| steel_hrc | ✅ | Giá thép HRC thế giới |
| fertilizer_ure | ✅ | Giá phân bón Urê |
| soybean | ✅ | Giá đậu nành |
| corn | ✅ | Giá ngô |
| sugar | ✅ | Giá đường |
| pork_north_vn | ✅ | Giá lợn miền Bắc VN |
| pork_china | ✅ | Giá lợn Trung Quốc |

**Khuyến Nghị**: SPL là nguồn duy nhất cho dữ liệu hàng hóa.

### 10. Fund (Quỹ ETF)

| Phương Thức | Fmarket | Ghi Chú |
|---|:---:|---|
| Các method của Fund | ✅ | Dữ liệu quỹ ETF |

**Khuyến Nghị**: Dùng để phân tích quỹ và chứng chỉ quỹ.
