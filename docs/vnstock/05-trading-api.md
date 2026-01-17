# 05 - Trading API - Dữ Liệu Giao Dịch

## 📖 Giới Thiệu

**Trading API** cung cấp dữ liệu giao dịch chi tiết: bảng giá real-time và mức bid/ask thị trường.

## 🔌 So Sánh Nguồn Dữ Liệu

| Method | KBS | VCI | Ghi Chú |
|--------|-----|-----|---------|
| **price_board()** | ✅ | ✅ | Cả hai đều có flat columns |

**Tổng số methods:**
- **KBS**: 1 method
- **VCI**: 1 method

**Khuyến nghị:**
- **KBS**: Dữ liệu gọn gàng, ổn định hơn, phù hợp cho basic usage
- **VCI**: Dữ liệu cực kỳ chi tiết (77 columns), phù hợp cho phân tích sâu

## 🚀 Bắt Đầu

```python
from vnstock import Trading

# Khởi tạo với KBS (khuyến nghị)
trading_kbs = Trading(source="KBS", symbol="VCI")

# Khởi tạo với VCI
trading_vci = Trading(source="VCI", symbol="VCI")

# Lấy bảng giá thị trường
board_kbs = trading_kbs.price_board(symbols_list=['VCI', 'VCB', 'ACB'])
board_vci = trading_vci.price_board(symbols_list=['VCI', 'VCB', 'ACB'])
```

## 📚 Phương Thức Chính

### 1. price_board() - Bảng Giá Real-Time

Lấy thông tin bảng giá của các mã chứng khoán theo thời gian thực.

**Parameters:**

**KBS:**
```
- symbols_list (List[str]): Danh sách mã chứng khoán
- exchange (str): Sàn giao dịch ('HOSE', 'HNX', 'UPCOM') - Mặc định 'HOSE'
- show_log (bool): Hiển thị log debug
- get_all (bool): Lấy tất cả columns - Mặc định False
```

**VCI:**
```
- symbols_list (List[str]): Danh sách mã chứng khoán
- show_log (bool): Hiển thị log debug
```

**Ví dụ:**

**Với KBS (khuyến nghị):**
```python
# Khởi tạo với KBS
trading = Trading(source="KBS", symbol="VCI")

# Lấy bảng giá (standard columns)
board = trading.price_board(symbols_list=['VCI', 'VCB', 'ACB'])
print(f"Shape: {board.shape}")  # (3, 28)
print(f"Columns: {list(board.columns)}")
print(f"Dtypes:\n{board.dtypes}")
# Output:
# Shape: (3, 28)
# Columns: ['symbol', 'exchange', 'ceiling_price', 'floor_price', 'reference_price',
#           'open_price', 'high_price', 'low_price', 'close_price', 'average_price',
#           'total_trades', 'total_value', 'price_change', 'percent_change',
#           'bid_price_1', 'bid_vol_1', 'bid_price_2', 'bid_vol_2', 'bid_price_3', 'bid_vol_3',
#           'ask_price_1', 'ask_vol_1', 'ask_price_2', 'ask_vol_2', 'ask_price_3', 'ask_vol_3',
#           'foreign_buy_volume', 'foreign_sell_volume']
# Dtypes:
# symbol                  object
# exchange                object
# ceiling_price            int64
# floor_price              int64
# reference_price          int64
# ...
print(board[['symbol', 'exchange', 'reference_price', 'price_change', 'percent_change']].head())
```

**Output với KBS:**
```
  symbol exchange  reference_price  price_change  percent_change
0    VCI     HOSE            34850           -50         -0.1435
1    VCB     HOSE            84500          100          0.1183
2    ACB     HOSE            23450           -50         -0.2128
```

**Với VCI (nguồn chi tiết):**
```python
# Khởi tạo với VCI
trading = Trading(source="VCI", symbol="VCI")

# Lấy bảng giá (flat columns)
board = trading.price_board(symbols_list=['VCI', 'VCB', 'ACB'])
print(f"Shape: {board.shape}")  # (3, 77)
print(f"Columns sample: {list(board.columns)[:10]}...")  # Flat columns
print(f"Dtypes sample:\n{board.dtypes.head(10)}")
# Output:
# Shape: (3, 77)
# Columns sample: ['symbol', 'ceiling', 'floor', 'ref_price', 'stock_type', 'exchange',
#                'trading_status', 'trading_status_code', 'transaction_time', 'bid_count', ...]
# Dtypes sample:
# symbol                  object
# ceiling                 int64
# floor                   int64
# ref_price               int64
# stock_type              object
# exchange                object
# ...

# Truy cập columns dễ dàng
print(board[['symbol', 'ref_price', 'match_price', 'total_volume']])
```

**Output với VCI:**
```
  symbol  ref_price  match_price  total_volume
0    VCI      34850        34700      11768600
1    VCB      84500        84600       2923100
2    ACB      23450        23350      12219800
```

## 🎯 So Sánh Dữ Liệu Chi Tiết

### price_board() Structure Comparison

| Feature | KBS | VCI | Ưu Điểm |
|---------|-----|-----|---------|
| **Columns** | 28 | 77 | VCI cực kỳ chi tiết |
| **Structure** | Flat columns | Flat columns | Cả hai đều dễ xử lý |
| **Price Data** | OHLC, change | Full market depth | VCI đầy đủ hơn |
| **Bid/Ask** | 3 levels | 3 levels | Cả hai đều có |
| **Foreign Trading** | Buy/Sell volume | Buy/Sell value | VCI có thêm value |
| **Processing** | Simple | Simple | Cả hai đều đơn giản |

### Khi Nào Dùng Nguồn Nào?

**Dùng KBS khi:**
- Cần dữ liệu nhanh và ổn định
- Chỉ cần thông tin cơ bản (giá, KL, thay đổi)
- Xử lý data đơn giản với flat columns
- Muốn data gọn gàng, dễ sử dụng

**Dùng VCI khi:**
- Cần phân tích sâu thị trường
- Cần market detail đầy đủ (77 columns)
- Cần foreign trading value
- Muốn data chi tiết với flat columns (dễ xử lý)

## 💡 Mẹo Sử Dụng

### 1. Truy Cập Columns Dễ Dàng

```python
# Cả KBS và VCI đều có flat columns
trading_kbs = Trading(source="KBS", symbol="VCI")
trading_vci = Trading(source="VCI", symbol="VCI")

# KBS - 28 columns
board_kbs = trading_kbs.price_board(symbols_list=['VCI', 'VCB'])
print(board_kbs[['symbol', 'reference_price', 'price_change']])

# VCI - 77 columns
board_vci = trading_vci.price_board(symbols_list=['VCI', 'VCB'])
print(board_vci[['symbol', 'ref_price', 'match_price', 'total_volume']])

# Cả hai đều dễ truy cập
print(f"KBS columns: {len(board_kbs.columns)}")
print(f"VCI columns: {len(board_vci.columns)}")
```

### 2. Lọc và Phân Tích Dữ Liệu

```python
# KBS - Lọc dữ liệu theo điều kiện
trading = Trading(source="KBS", symbol="VCI")
board = trading.price_board(symbols_list=['VCI', 'VCB', 'ACB', 'BID', 'CTG'])

# Lọc các cổ phiếu tăng giá
risers = board[board['price_change'] > 0]
print("Cổ phiếu tăng giá:")
print(risers[['symbol', 'reference_price', 'price_change', 'percent_change']])

# Lọc theo khối lượng giao dịch
high_volume = board[board['total_trades'] > 1000]
print("\nCổ phiếu giao dịch sôi động:")
print(high_volume[['symbol', 'total_trades', 'total_value']])

# Tính toán thống kê
avg_change = board['percent_change'].mean()
total_value = board['total_value'].sum()
print(f"\nTrung bình thay đổi: {avg_change:.2f}%")
print(f"Tổng giá trị giao dịch: {total_value:,.0f}")
```

### 3. Real-time Monitoring

```python
import time
from vnstock import Trading

def monitor_price(symbols, interval=30):
    """Monitor price changes in real-time"""
    trading = Trading(source="KBS", symbol=symbols[0])
    
    while True:
        try:
            board = trading.price_board(symbols_list=symbols)
            
            # Hiển thị thông tin chính
            for _, row in board.iterrows():
                change_emoji = "📈" if row['price_change'] > 0 else "📉" if row['price_change'] < 0 else "➡️"
                print(f"{change_emoji} {row['symbol']}: {row['reference_price']} "
                      f"({row['price_change']:+,} {row['percent_change']:+.2f}%)")
            
            print("-" * 50)
            time.sleep(interval)
            
        except KeyboardInterrupt:
            print("\nStopped monitoring.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

# Monitor VN30 stocks
vn30_stocks = ['VCI', 'VCB', 'ACB', 'BID', 'CTG', 'HDB', 'MBB', 'SSB', 'STB', 'TCB', 'TPB', 'VIB']
monitor_price(vn30_stocks, interval=30)
```

### 4. Export và Analysis

```python
# Export data cho analysis
trading = Trading(source="KBS", symbol="VCI")

# Lấy dữ liệu và export
board = trading.price_board(symbols_list=['VCI', 'VCB', 'ACB'])
board.to_csv('price_board.csv', index=False)

# Analysis với pandas
import pandas as pd

# Đọc lại data
df = pd.read_csv('price_board.csv')

# Phân tích theo sàn
exchange_stats = df.groupby('exchange').agg({
    'total_value': 'sum',
    'total_trades': 'sum',
    'symbol': 'count'
}).rename(columns={'symbol': 'stock_count'})
print("Thống kê theo sàn:")
print(exchange_stats)

# Phân tích theo mức thay đổi
df['change_category'] = pd.cut(df['percent_change'], 
                              bins=[-10, -2, 0, 2, 10], 
                              labels=['Giảm mạnh', 'Giảm nhẹ', 'Đứng giá', 'Tăng'])
change_dist = df['change_category'].value_counts()
print("\nPhân bổ thay đổi giá:")
print(change_dist)
```

## 🚨 Lưu Ý Quan Trọng

1. **Rate Limits**: Cả hai nguồn đều có rate limits, tránh request quá nhanh
2. **Market Hours**: Dữ liệu chỉ có trong giờ giao dịch (9:00-15:00)
3. **Data Freshness**: KBS thường nhanh hơn VCI
4. **Error Handling**: Luôn try-catch khi gọi API
5. **Memory**: VCI data lớn hơn, cẩn thận với memory usage

## 📚 Bước Tiếp Theo

1. [02-Installation](02-installation.md) - Cài đặt
2. [01-Overview](01-overview.md) - Tổng quan
3. [03-Listing API](03-listing-api.md) - Danh sách mã
4. [04-Company API](04-company-api.md) - Thông tin công ty
5. ✅ **05-Trading API** - Bạn đã ở đây
6. [06-Quote & Price](06-quote-price-api.md) - Giá lịch sử
7. [07-Financial API](07-financial-api.md) - Dữ liệu tài chính

---

**Last Updated**: 2024-12-17  
**Version**: 3.4.0  
**Status**: Actively Maintained
