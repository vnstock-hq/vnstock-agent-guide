# 05 - Trading API - Dữ Liệu Giao Dịch

## 📖 Giới Thiệu

**Trading API** cung cấp dữ liệu giao dịch chi tiết: bảng giá real-time, mức bid/ask, và thông tin giao dịch thị trường.

## 🔌 Nguồn Dữ Liệu

| Nguồn | Hỗ Trợ | Ghi Chú |
|-------|--------|--------|
| VCI | ✅ | Web scraping |
| TCBS | ✅ | Web scraping |

## 🚀 Bắt Đầu

```python
from vnstock import Trading

# Khởi tạo
trading = Trading(source="vci", symbol="VCI")

# Lấy bảng giá thị trường
board = trading.price_board(symbols_list=['VCI', 'VCB', 'ACB'])
print(board)
```

## 📚 Phương Thức Chính

### 1. price_board() - Bảng Giá Real-Time

Lấy bảng giá hiện tại (real-time) của nhiều chứng khoán cùng lúc.

**Tham số:**
- `symbols_list` (list, tùy chọn): Danh sách mã chứng khoán
  - Nếu không cung cấp, sẽ lấy tất cả
- `**kwargs`: Các tham số khác tùy theo nguồn

**Trả về:** `pd.DataFrame` với **70 cột** (dữ liệu phức tạp, cấu trúc đa cấp):

**Cột chính (Listing):**
- `('listing', 'symbol')` - Mã chứng khoán (str)
- `('listing', 'ceiling')` - Giá trần (int64)
- `('listing', 'floor')` - Giá sàn (int64)
- `('listing', 'ref_price')` - Giá tham chiếu (int64)
- `('listing', 'trading_status')` - Trạng thái giao dịch

**Cột Bid/Ask (3 levels):**
- `('bid_ask', 'bid_1_price')` - Giá mua tốt nhất (int64)
- `('bid_ask', 'bid_1_volume')` - Khối lượng mua tốt nhất (int64)
- `('bid_ask', 'bid_2_price')` - Giá mua thứ 2 (int64)
- `('bid_ask', 'bid_2_volume')` - Khối lượng mua thứ 2 (int64)
- `('bid_ask', 'bid_3_price')` - Giá mua thứ 3 (int64)
- `('bid_ask', 'bid_3_volume')` - Khối lượng mua thứ 3 (int64)
- `('bid_ask', 'ask_1_price')` - Giá bán tốt nhất (int64)
- `('bid_ask', 'ask_1_volume')` - Khối lượng bán tốt nhất (int64)
- `('bid_ask', 'ask_2_price')` - Giá bán thứ 2 (int64)
- `('bid_ask', 'ask_2_volume')` - Khối lượng bán thứ 2 (int64)
- `('bid_ask', 'ask_3_price')` - Giá bán thứ 3 (int64)
- `('bid_ask', 'ask_3_volume')` - Khối lượng bán thứ 3 (int64)

**Cột Match (giao dịch):**
- `('match', 'match_price')` - Giá giao dịch cuối (int64)
- `('match', 'accumulated_volume')` - Khối lượng tích lũy (int64)
- `('match', 'accumulated_value')` - Giá trị tích lũy (float64)
- `('match', 'highest')` - Giá cao nhất (int64)
- `('match', 'lowest')` - Giá thấp nhất (int64)
- `('match', 'open_price')` - Giá mở cửa (int64)
- `('match', 'avg_match_price')` - Giá giao dịch trung bình (float64)

**Ví dụ:**
```python
from vnstock import Trading

trading = Trading(source="vci")

# Lấy bảng giá
board = trading.price_board(symbols_list=['VCI', 'VCB', 'ACB'])
print(board.shape)  # (3, 70)

# Trích xuất dữ liệu từ structure columns
symbols = board[('listing', 'symbol')].tolist()
prices = board[('match', 'match_price')].tolist()
print(dict(zip(symbols, prices)))
# {'VCI': 35050, 'VCB': 58900, 'ACB': 24900}

# Top theo khối lượng
top_by_volume = board.nlargest(3, ('match', 'accumulated_volume'))
print(top_by_volume[[('listing', 'symbol'), ('match', 'accumulated_volume')]])
```

### 2. trading_stats() - Thống Kê Giao Dịch

⚠️ **Lưu ý:** Phương thức này không được hỗ trợ trên VCI

Lấy thống kê giao dịch hàng ngày của một chứng khoán.

**Tham số:**
- `start` (str): Ngày bắt đầu (format: "YYYY-MM-DD")
- `end` (str): Ngày kết thúc (format: "YYYY-MM-DD")
- `limit` (int, tùy chọn): Giới hạn số bản ghi, mặc định: 1000

**Trả về:** `pd.DataFrame` (không khả dụng hiện tại)

### 3. side_stats() - Thông Tin Bid/Ask Chi Tiết

⚠️ **Lưu ý:** Phương thức này không được hỗ trợ trên VCI

Lấy thông tin chi tiết về các lệnh mua (bid) và bán (ask) hiện tại.

**Tham số:**
- `dropna` (bool, tùy chọn): Loại bỏ giá trị rỗng, mặc định: True

**Trả về:** `tuple` của 2 DataFrame: (bid_df, ask_df) (không khả dụng hiện tại)

## 💡 Ví Dụ Thực Tế

### Lấy Giá Thị Trường Hiện Tại

```python
from vnstock import Trading
import pandas as pd

trading = Trading(source="vci")

# Danh sách theo dõi
watchlist = ["VCI", "VCB", "ACB", "BID", "CTG"]

# Lấy bảng giá
board = trading.price_board(symbols_list=watchlist)

# Tạo DataFrame dễ đọc
data = {
    'symbol': board[('listing', 'symbol')],
    'price': board[('match', 'match_price')],
    'bid_1': board[('bid_ask', 'bid_1_price')],
    'ask_1': board[('bid_ask', 'ask_1_price')],
    'volume': board[('match', 'accumulated_volume')],
}

df = pd.DataFrame(data)
print(df)
```

**Output:**
```
  symbol  price   bid_1  ask_1     volume
0    VCI  35050  35000  35100  11768600
1    VCB  58900  58900  59000   2923100
2    ACB  24900  24900  25000  12219800
3    BID  ...
```

### Phân Tích Độ Sâu Thị Trường

```python
from vnstock import Trading
import pandas as pd

trading = Trading(source="vci")
board = trading.price_board(symbols_list=['VCI', 'VCB'])

# Tính độ sâu bid/ask
for idx, row in board.iterrows():
    symbol = row[('listing', 'symbol')]
    
    # Bid side
    bid_prices = [row[('bid_ask', f'bid_{i}_price')] for i in range(1, 4)]
    bid_volumes = [row[('bid_ask', f'bid_{i}_volume')] for i in range(1, 4)]
    bid_value = sum(p*v for p, v in zip(bid_prices, bid_volumes) if p > 0)
    
    # Ask side
    ask_prices = [row[('bid_ask', f'ask_{i}_price')] for i in range(1, 4)]
    ask_volumes = [row[('bid_ask', f'ask_{i}_volume')] for i in range(1, 4)]
    ask_value = sum(p*v for p, v in zip(ask_prices, ask_volumes) if p > 0)
    
    print(f"{symbol}: Bid={bid_value:,.0f} | Ask={ask_value:,.0f}")
```

### Theo Dõi Các Chứng Khoán Tích cực

```python
from vnstock import Trading
import pandas as pd

trading = Trading(source="vci")

# Danh sách lớn
all_symbols = ["VCI", "VCB", "ACB", "BID", "CTG", "VJC", "FPT"]
board = trading.price_board(symbols_list=all_symbols)

# Lọc theo khối lượng cao
high_volume = board[board[('match', 'accumulated_volume')] > 10_000_000]

result = pd.DataFrame({
    'symbol': high_volume[('listing', 'symbol')],
    'price': high_volume[('match', 'match_price')],
    'volume': high_volume[('match', 'accumulated_volume')],
})

print(f"Chứng khoán giao dịch tích cực: {len(result)}")
print(result.sort_values('volume', ascending=False))
```

## 📊 Cấu Trúc Dữ Liệu

Lưu ý rằng `price_board()` trả về DataFrame với **MultiIndex columns** (cột đa cấp):

```python
# Cách trích xuất giá trị
price = board.loc[0, ('match', 'match_price')]  # Giá giao dịch dòng đầu

# Hoặc sử dụng .xs() method
prices = board.xs('match_price', level=1, axis=1)
```

## ⚠️ Ghi Chú Quan Trọng

1. **Real-time vs Delayed**: Giá có thể bị trễ 1-5 phút tùy theo nguồn
2. **Bid/Ask levels**: Chỉ có 3 levels, không phải tất cả đều có giá
3. **Cấu trúc phức tạp**: DataFrame có MultiIndex columns, cần xử lý cẩn thận
4. **Hạn chế phương thức**: `trading_stats()` và `side_stats()` hiện không khả dụng

## 🔗 Xem Thêm

- **[03-Listing API](03-listing-api.md)** - Tìm kiếm chứng khoán
- **[06-Quote Price API](06-quote-price-api.md)** - Lấy dữ liệu giá lịch sử
- **[08-Best Practices](08-best-practices.md)** - Mẹo tối ưu hóa

---

**Last Updated**: 2024-12-04  
**Version**: 3.3.0  
**Status**: Verified with actual data ✅
