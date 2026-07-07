# Layer 6: Insights (Phân Tích Chuyên Sâu)

> [!IMPORTANT]
> **Data Schema (Từ điển dữ liệu):** Để xem chính xác tên cột, kiểu dữ liệu (`Dtype`) và ý nghĩa (`Meaning`) của các DataFrame trả về từ layer này, vui lòng tham khảo [Data Schema](schema/06-insights.md). KHÔNG được đoán mò tên cột khi viết code xử lý dữ liệu.

## 📌 Tổng Quan

**Insights Layer** cung cấp **xếp hạng top cổ phiếu** và **bộ lọc chứng khoán** để nhà đầu tư nhận diện cơ hội và xu hướng thị trường.

> **Lưu ý**: Domain **Valuation** (P/E, P/B toàn thị trường) đã được chuyển sang **[Analytics Layer](07-analytics-layer.md)** từ phiên bản Unified UI mới. Nếu trước đây bạn dùng `Insights().valuation`, vui lòng chuyển sang `Analytics().valuation(index)`.

## 🏗️ Cấu Trúc Domain

```python
Insights()
├── .ranking       # Xếp hạng top cổ phiếu
└── .screener      # Bộ lọc chứng khoán
```

## 📋 Chi Tiết Các Domain

### 1. Ranking Domain (Xếp Hạng & Top)

**Source:** VND (vnd)  
**Registry Key:** `"insights.ranking"`

#### Mô Tả

Xếp hạng top cổ phiếu theo các tiêu chí khác nhau: tăng giá, giảm giá, khối lượng, nước ngoài, v.v.

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `gainer()` | `index`, `limit` | Top cổ phiếu tăng giá | DataFrame |
| `loser()` | `index`, `limit` | Top cổ phiếu giảm giá | DataFrame |
| `value()` | `index`, `limit` | Top cổ phiếu theo giá trị giao dịch | DataFrame |
| `volume()` | `index`, `limit` | Top cổ phiếu theo khối lượng | DataFrame |
| `foreign_buy()` | `date`, `limit` | Top nước ngoài mua nhiều | DataFrame |
| `foreign_sell()` | `date`, `limit` | Top nước ngoài bán nhiều | DataFrame |
| `deal()` | `index`, `limit` | Top giao dịch thỏa thuận | DataFrame |

**Parameters:**
- `index` (str, optional): Chỉ số lọc (ví dụ: `'VNINDEX'`, `'HNX'`). Mặc đình lấy toàn thị trường.
- `limit` (int, optional): Số lượng kết quả. Mặc định 10.
- `date` (str, optional): Ngày giao dịch (YYYY-MM-DD).

#### Ví Dụ

```python
from vnstock_data import Insights

ins = Insights()

# ===== Top Gainer (Tăng Giá) =====
# Top gainer sàn VNINDEX
df_gainers_vn = ins.ranking.gainer(index='VNINDEX', limit=1)
print(df_gainers_vn)
```
| symbol | exchange | last_price | last_updated | price_change_1d | price_change_pct_1d | total_value | avg_volume_20d | volume_spike_20d_pct |
|:---|:---|---:|:---|---:|---:|---:|---:|---:|
| HID | HOSE | 4.65 | 2026-05-15 10:38 | 0.3 | 6.89655 | 7.35031e+08 | 446655 | 35.9562 |

# ===== Top Loser (Giảm Giá) =====
df_losers = ins.ranking.loser()
print(df_losers)

# ===== Top Volume (Khối Lượng) =====
df_volume = ins.ranking.volume()
print(df_volume)

```python
# ===== Foreign Flow (Nước Ngoài Mua) =====
df_foreign_buy = ins.ranking.foreign_buy(limit=1)
print(df_foreign_buy)
```
| symbol | date | net_value |
|:---|:---|---:|
| TCB | 2026-05-15 | 4.11252e+10 |

```python
# ===== Foreign Sell (Nước Ngoài Bán) =====
df_foreign_sell = ins.ranking.foreign_sell()
print(df_foreign_sell)

# ===== Top Deal (Giao Dịch Thỏa Thuận) =====
df_deals = ins.ranking.deal()
print(df_deals)
```

---

### 2. Screener Domain (Bộ Lọc Chứng Khoán)

**Source:** VCI (vci)  
**Registry Key:** `"insights.screener"`

#### Mô Tả

Bộ lọc cổ phiếu cho phép lọc nhanh danh sách các mã cổ phiếu bạn quan tâm với bộ tiêu chí được hỗ trợ. Người dùng có thể nạp điều kiện lọc khi gọi API bằng cách truyền `filters` cấu hình bộ lọc nhằm rút ngắn thời gian và độ lớn dữ liệu tải về. (Mặc định nếu chạy không có tham số API sẽ kết hợp rất nhiều tiêu chí với biên độ lớn, đôi khi trả về rất ít kết quả).

#### Phương Thức

| Method | Tham Số | Mô Tả | Return |
|--------|---------|-------|--------|
| `criteria()` | `lang` | Danh sách giải thích tên cột và cấu hình (vi/en) | DataFrame |
| `filter()` | `filters`, `limit` | Dữ liệu screener theo bộ lọc hoặc toàn thị trường | DataFrame |

**Parameters:**
- `filters` (List[Dict], optional): Payload bộ lọc tùy chỉnh (là danh sách các tiêu chí lọc). Nếu không truyền, hệ thống sẽ gọi bộ lọc mặc định rộng nhất.
- `lang` (str): Ngôn ngữ ('vi' hoặc 'en'). Mặc định 'vi'.
- `limit` (int): Số lượng bản ghi tối đa. Mặc định 2000.

#### Bảng Tham Chiếu Cấu Trúc Bộ Lọc (Filters Payload)

Cấu trúc JSON cơ bản của `filters` (là một danh sách các dictionary) như sau:
```json
[
    {
        "name": "TÊN_TIÊU_CHÍ_TỪ_HÀM_CRITERIA",
        "extraName": "TÊN_BỔ_SUNG_NẾU_CÓ",
        "conditionOptions": [
            {"type": "value", "value": "GIÁ_TRỊ_LỰA_CHỌN"}, 
            {"from": 0, "to": 10} 
        ]
    }
]
```

**Lưu ý quan trọng**: Các `field_name` và `extraName` ở bảng dưới đây dùng để cấu hình `filters` khi gửi request. Khi dữ liệu trả về thành DataFrame, tên cột sẽ tự động chuyển sang định dạng `snake_case` (ví dụ: `priceEma` + `ema20` sẽ thành cột `price_ema_20`, `ema20Ema50` sẽ thành cột `ema_20_ema_50`). Vui lòng xem [Schema Reference](schema/06-insights.md) để biết chính xác tên cột của kết quả đầu ra.

Tất cả các tiêu chí lọc được hệ thống hỗ trợ bạn có thể tìm thấy ở bảng dưới đây (được rút trích từ bộ tiêu chí đầy đủ của hàm `criteria()`):

| Phân Loại | Tiêu Chí | `field_name` | `extraName` / `extraName2` | Kiểu Filter (conditionOptions) | Ví dụ |
|---|---|---|---|---|---|
| **Thông tin chung** | Sàn giao dịch | `exchange` | | chọn giá trị (hsx, hnx, upcom) | `{"type": "value", "value": "hsx"}` |
| | Nhóm ngành cấp 1 | `sectorLv1` | | chọn mã ngành | `{"type": "value", "value": "1000"}` |
| | Vốn hóa (VND) | `marketCap` | | khoảng giá trị | `{"from": 0, "to": 1000000000}` |
| | Thị giá | `marketPrice` | | khoảng giá trị | `{"from": 10000, "to": 50000}` |
| **Giá & Khối lượng** | % Biến động giá hàng ngày | `dailyPriceChangePercent` | | khoảng giá trị | `{"from": -5, "to": 5}` |
| | Giá trị GD trung bình | `adtv` | `30Days` | khoảng giá trị | `{"from": 1e9, "to": 5e9}` |
| | Khối lượng TB | `avgVolume` | `30Days` | khoảng giá trị | `{"from": 100000, "to": 2000000}` |
| | Đột biến KL (vs TB) | `esVolumeVsAvgVolume` | `30Days` | khoảng giá trị (%) | `{"from": 20, "to": 100}` |
| | Tỷ suất lợi nhuận | `priceReturn` | `3Month` | khoảng giá trị (%) | `{"from": 5, "to": 20}` |
| | Hiệu suất vs VN-Index | `outperformsIndex` | `3Month` | khoảng giá trị (%) | `{"from": 0, "to": 15}` |
| | Mức biến động giá | `priceFluctuation` | `30Days` | khoảng giá trị (%) | `{"from": 0, "to": 10}` |
| **Phân tích kỹ thuật** | Sức mạnh giá (Stock Strength) | `stockStrength` | | khoảng giá trị | `{"from": 50, "to": 100}` |
| | Sức mạnh tương đối (RS) | `rs` | `3Month` | khoảng giá trị | `{"from": 70, "to": 100}` |
| | RSI | `rsi` | | khoảng giá trị | `{"from": 30, "to": 70}` |
| | Giá so với EMA | `priceEma` | `ema20` | khoảng giá trị (%) | `{"from": -5, "to": 5}` |
| | Tương quan EMA20 & EMA50 | `ema20Ema50` | | khoảng giá trị (%) | `{"from": 0, "to": 5}` |
| | Tương quan EMA50 & EMA200| `ema50Ema200` | | khoảng giá trị (%) | `{"from": 0, "to": 5}` |
| | MACD | `macd` | | khoảng giá trị | `{"from": 0, "to": 5}` |
| | MACD Histogram | `histogram` | | khoảng giá trị | `{"from": 0, "to": 1}` |
| | ADX | `adx` | | khoảng giá trị | `{"from": 25, "to": 100}` |
| | Xu hướng cổ phiếu | `stockTrend` | | chọn giá trị string | `{"type": "value", "value": "STRONG_UPTREND"}` |
| | Xu hướng AO (Awesome Osc)| `aoTrend` | | chọn giá trị string | `{"type": "value", "value": "ABOVE_ZERO"}` |
| **Định giá & Tài chính** | P/E cơ bản | `ttmPe` | | khoảng giá trị | `{"from": 5, "to": 15}` |
| | P/B cơ bản | `ttmPb` | | khoảng giá trị | `{"from": 0.5, "to": 2.5}` |
| | ROE | `ttmRoe` | | khoảng giá trị (%) | `{"from": 15, "to": 50}` |
| | Tăng trưởng LNST (Mẹ) | `npatmiGrowth` | `Yoy`, `Qm1` (extraName2) | khoảng giá trị (%) | `{"from": 10, "to": 100}` |
| | Tăng trưởng doanh thu | `revenueGrowth` | `Yoy` | khoảng giá trị (%) | `{"from": 10, "to": 100}` |
| | Biên Lợi nhuận ròng | `netMargin` | | khoảng giá trị (%) | `{"from": 10, "to": 100}` |
| | Biên Lợi nhuận gộp | `grossMargin` | | khoảng giá trị (%) | `{"from": 15, "to": 100}` |

#### 🤖 Mẹo: Dùng AI Để Viết Bộ Lọc

Do số lượng tiêu chí lọc rất lớn, bạn nên yêu cầu AI viết cấu trúc payload JSON `filters` bằng cách cung cấp danh sách cột từ hàm `criteria()`.

**Prompt mẫu:**
> "Tôi đang dùng thư viện vnstock_data, hàm `ins.screener.filter(filters=...)` cho phép truyền payload JSON để lọc cổ phiếu từ máy chủ. Dưới đây là danh sách tiêu chí lấy từ hàm `criteria()`: 
> 
> [Copy/paste kết quả từ hàm `ins.screener.criteria().to_csv()` hoặc `to_json()` vào đây]. 
> 
> Hãy soạn cho tôi một danh sách Python (cấu trúc JSON array) để lọc các cổ phiếu thuộc sàn HSX, có ROE > 15%, P/E < 10, và khối lượng giao dịch trung bình 30 ngày > 1,000,000."

#### Ví Dụ

```python
from vnstock_data import Insights

ins = Insights()

# ===== 1. Lọc Trực Tiếp Qua API (Sử dụng filters) =====
custom_filters = [
    {
        "name": "exchange",
        "conditionOptions": [{"type": "value", "value": "hsx"}]
    },
    {
        "name": "ttmRoe",
        "conditionOptions": [{"from": 15, "to": 100}]
    },
    {
        "name": "ttmPe",
        "conditionOptions": [{"from": 0, "to": 10}]
    }
]

# Chỉ trả về kết quả thỏa mãn cấu hình trên
df_filtered = ins.screener.filter(filters=custom_filters)
print(f"Cổ phiếu HSX, P/E < 10, ROE > 15: {len(df_filtered)}")
print(df_filtered[['ticker', 'ttm_pe', 'ttm_roe']].head())

# ===== 2. Kết hợp với Listing để tra cứu mã Ngành ICB =====
from vnstock_data import Listing

# Lấy danh sách phân ngành từ nguồn VCI
lst_vci = Listing(source="vci")
icb_df = lst_vci.industries_icb()

# Tra cứu mã ICB cấp 1 (level = 1)
lv1_sectors = icb_df[icb_df['level'] == 1]
print("Danh sách mã ngành cấp 1:\n", lv1_sectors[['icb_code', 'icb_name']].head())

# Giả sử '1000' là "Công nghiệp" (tùy thuộc vào kết quả trả về của icb_df)
sector_code = "1000" 
sector_filter = [
    {
        "name": "sectorLv1",
        "conditionOptions": [{"type": "value", "value": sector_code}]
    }
]

df_sector = ins.screener.filter(filters=sector_filter)
print(f"\nCổ phiếu thuộc nhóm ngành {sector_code}: {len(df_sector)}")
print(df_sector[['ticker', 'exchange', 'sector_lv1']].head())

# ===== 3. Lọc Toàn Thị Trường & Phân Tích Bằng Pandas =====
# Lấy mọi cổ phiếu với bộ lọc mặc định rộng nhất
df_all = ins.screener.filter()
print(f"Total stocks: {len(df_all)}")

# Lọc thủ công bằng Pandas
cheap_good = df_all[
    (df_all['pe'] < 10) & (df_all['roe'] > 15)
]
print(cheap_good[['symbol', 'pe', 'roe']].head())
```

| symbol | exchange | ref_price | ceiling | price | floor | accumulated_value | accumulated_volume | market_cap | price_change_percent | avg_value_30d | avg_value_10d | avg_volume_30d | est_volume | volume_breakout_30d | pe | pb | roe | profit_growth_yoy | revenue_growth_yoy | net_margin | gross_margin |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ABB | UPCOM | 15200 | 17400 | 15200 | 13000 | 1.65051e+09 | 107900 | 1.57326e+13 | 0 | 1.23616e+10 | -86.8034 | 831840 | 302733 | -63.6068 | 4.69571 | 0.986995 | 21.1886 | 260.74 | 49.4604 | 34.5488 | 68.6208 |

---

## 💡 Best Practices

### 1. Tìm Cơ Hội Giá Trị

```python
from vnstock_data import Insights

ins = Insights()

# Cổ phiếu giảm giá mạnh nhưng có chất
losers = ins.ranking.loser()
screener = ins.screener.filter()

# Merge để tìm cơ hội
opportunity = losers.merge(screener, left_on='code', right_on='ticker', how='inner')
print(opportunity[['ticker', 'pe', 'roe']].head())
```

### 2. Tra Cứu Methods

```python
from vnstock_data import show_api, Insights
show_api(Insights())  # Xem tất cả methods
```

---

## ⚠️ Lưu Ý Quan Trọng

1. **Valuation đã chuyển sang Analytics**: Dùng `Analytics().valuation(index).pe()` thay cho `Insights().valuation.pe()` (đã có ở phiên bản trước)
2. **Phân Tích Không Phải Khuyến Nghị**: Insights là phân tích thị trường, **không phải lời khuyên đầu tư**
3. **Đa Khía Cạnh**: Nên kết hợp nhiều tiêu chí thay vì dựa vào 1 chỉ số
4. **Verify Data**: Luôn xác minh dữ liệu với các nguồn khác trước khi quyết định

---

## 🚦 Next Steps

- **Analytics Layer**: Để xem định giá P/E, P/B thị trường
- **Market Layer**: Để lấy giá thực tế và giao dịch
- **Fundamental Layer**: Để phân tích sâu hơn về BCTC
- **Macro Layer**: Để hiểu tác động của yếu tố vĩ mô
