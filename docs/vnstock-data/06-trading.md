# Trading - Dữ Liệu Giao Dịch, Bảng Giá, Thống Kê

Lớp `Trading` cung cấp dữ liệu giao dịch chi tiết, bảng giá, thống kê giao dịch nước ngoài và tự doanh.

## Khởi Tạo

```python
from vnstock_data import Trading

# VCI: Dữ liệu từ bảng giá giao dịch
trading_vci = Trading(source="vci", symbol="VCB")

# CafeF: Dữ liệu có thể không đầy đủ và ổn định, sử dụng làm nguồn bổ sung
trading_cafef = Trading(source="cafef", symbol="VCB")
```

**Lưu ý**: VCI và CafeF có một số method (phương thức) khác nhau.

## Phương Thức VCI

### price_board() - Bảng Giá Realtime

```python
df = trading_vci.price_board(
    symbols_list=['VCB', 'ACB', 'TCB'],
    flatten_columns=True,
    drop_levels=[0]
)
```

**Trả về**: DataFrame với 70 cột (shape: N, 70)
- Cột chính: `symbol`, `match_price`, `ceiling_price`, `floor_price`, `reference_price`, `open_price`, `highest`, `lowest`
- Cột khối lượng: `accumulated_volume`, `match_vol`, `foreign_buy_volume`, `foreign_sell_volume`
- Cột giá trị: `accumulated_value`, `foreign_buy_value`, `foreign_sell_value`
- Cột lệnh: `bid_1_price`, `bid_1_volume`, `ask_1_price`, `ask_1_volume` (và bid/ask 2,3)
- Cột khác: `trading_date`, `exchange`, `trading_status`, `total_room`, `current_room`
- Kiểu dữ liệu: float64 (giá), int64 (khối lượng, giá trị), object (symbol, status)

**Ví dụ** (VCB, ACB, TCB):
```
  symbol  ceiling  floor  ref_price  ... ask_1_price ask_1_volume ask_2_price ask_2_volume ask_3_price ask_3_volume
0    VCB    61500  53500      57500  ...       57300        43000       57400        48800       57500        69900
1    ACB    25650  22350      24000  ...       23900       137300       23950       197400       24000       580700
2    TCB    35500  30900      33200  ...       33350        69500       33400       180900       33450       103900
```

### price_history() - Lịch Sử Giá (Ngày)

```python
df = trading_vci.price_history(
    start="2024-01-01",
    end="2024-12-31",
    resolution="1D"  # 1D, 1W, 1M, 1Q, 1Y
)
```

**Trả về**: DataFrame với 36 cột (shape: N, 36)
- Cột giá: `open`, `close`, `high`, `low`, `match_price`, `ceiling_price`, `floor_price`, `reference_price`, `average_price`
- Cột điều chỉnh: `reference_price_adjusted`, `open_price_adjusted`, `close_price_adjusted`, `highest_price_adjusted`, `lowest_price_adjusted`
- Cột khối lượng: `matched_volume`, `deal_volume`, `total_volume`, `total_buy_trade_volume`, `total_sell_trade_volume`, `average_buy_trade_volume`, `average_sell_trade_volume`, `total_net_trade_volume`
- Cột giá trị: `matched_value`, `deal_value`, `total_value`
- Cột khác: `trading_date` (datetime64), `market_cap`, `total_shares`, `price_change`, `percent_price_change`, `total_buy_trade`, `total_sell_trade`, `total_buy_unmatched_volume`, `total_sell_unmatched_volume`
- Kiểu dữ liệu: float64 (giá, khối lượng, giá trị), datetime64 (trading_date)

## Phương Thức CafeF

### price_history() - Lịch Sử Giá

```python
df = trading_cafef.price_history(
    start="2024-01-01",
    end="2024-12-31"
)
```

**Trả về**: DataFrame với 10 cột (shape: N, 10)
- Cột giá: `open`, `high`, `low`, `close`, `adjusted_price`
- Cột khối lượng: `matched_volume`, `deal_volume`
- Cột giá trị: `matched_value`, `deal_value`
- Cột khác: `change_pct` (% thay đổi giá)
- Kiểu dữ liệu: float64 (giá, %), int64 (khối lượng, giá trị)
- Index: `time` (datetime)

**Ví dụ** (3 ngày gần nhất VCB):
```
             open  high   low  close adjusted_price matched_volume matched_value  deal_volume  deal_value
time                                                                                                      
2024-11-29  92.6  93.3  92.5   93.3          61.96      1010500    93955000000        64600    5949660000
2024-11-28  93.1  93.5  92.5   92.6          61.49      1289900   120033000000        99000    9207000000
2024-11-27  92.3  93.2  92.3   92.7          61.56      1048309    97319490000            0             0
```

### order_stats() - Thống Kê Đặt Lệnh

```python
df = trading_cafef.order_stats(
    start="2024-01-01",
    end="2024-12-31"
)
```

Trả về: buy_orders, sell_orders, buy_volume, sell_volume, volume_diff, avg_buy_order_volume, avg_sell_order_volume

### foreign_trade() - Giao Dịch Nước Ngoài

```python
df = trading_cafef.foreign_trade(
    start="2024-01-01",
    end="2024-12-31"
)
```

**Trả về**: DataFrame với 8 cột (shape: N, 8)
- Cột khối lượng: `fr_buy_volume`, `fr_sell_volume`, `fr_net_volume`
- Cột giá trị: `fr_buy_value`, `fr_sell_value`, `fr_net_value`
- Cột khác: `fr_remaining_room` (phòng còn lại), `fr_ownership` (% sở hữu của nước ngoài)
- Kiểu dữ liệu: int64, float64
- Index: `time` (datetime)

**Ví dụ** (3 ngày gần nhất VCB):
```
            fr_buy_volume  fr_sell_volume  fr_net_volume  fr_buy_value  fr_sell_value  fr_net_value  fr_remaining_room  fr_ownership
time                                                                                                                                      
2024-11-29        51400         342600      -291200     4784820000    31851880000   -27067060000          381515749           23.17
2024-11-28        13000         663400      -650400     1211420000    61721750000   -60510330000          381113505           23.18
2024-11-27       160900         453500      -292600    14950780000    42087290000   -27136510000          380404163           23.19
```

### prop_trade() - Giao Dịch Tự Doanh

```python
df = trading_cafef.prop_trade(
    start="2024-01-01",
    end="2024-12-31"
)
```

**Trả về**: DataFrame với 4 cột (shape: N, 4)
- `prop_buy_volume`: Khối lượng mua tự doanh (int64)
- `prop_sell_volume`: Khối lượng bán tự doanh (int64)
- `prop_buy_value`: Giá trị mua tự doanh (int64 - VND)
- `prop_sell_value`: Giá trị bán tự doanh (int64 - VND)
- Index: `time` (datetime)

**Ví dụ** (3 ngày gần nhất VCB):
```
            prop_buy_volume  prop_sell_volume  prop_buy_value  prop_sell_value
time                                                                           
2024-11-29          118900           154700    11061620000      14372650000
2024-11-28          139200           188700    12968610000      17546430000
2024-11-27           96900           215800     8994070000      20018910000
```

### insider_deal() - Giao Dịch Nội Bộ

```python
df = trading_cafef.insider_deal(
    start="2024-01-01",
    end="2024-12-31"
)
```

**Trạng thái**: Dữ liệu có sẵn chỉ cho một số cổ phiếu và thời kỳ cụ thể.

### order_stats() - Thống Kê Đặt Lệnh

```python
df = trading_cafef.order_stats(
    start="2024-01-01",
    end="2024-12-31"
)
```

**Trả về**: DataFrame với 7 cột (shape: N, 7)
- Cột lệnh: `buy_orders`, `sell_orders` (số lệnh - int64)
- Cột khối lượng: `buy_volume`, `sell_volume`, `volume_diff` (int64)
- Cột trung bình: `avg_buy_order_volume`, `avg_sell_order_volume` (float64)
- Index: `time` (datetime)

**Ví dụ** (3 ngày gần nhất VCB):
```
            buy_orders  sell_orders  buy_volume  sell_volume  volume_diff  avg_buy_order_volume  avg_sell_order_volume
time                                                                                                                     
2024-11-29         869         1047    1715000      2094000      -379000              1974                   2000
2024-11-28        1501         2111    2053600      2610100      -556500              1368                   1236
2024-11-27         762         1190    2230500      1858700       371800              2927                   1562
```

```python
from vnstock_data import Trading

# VCI
trading_vci = Trading(source="vci", symbol="VCB")

# Bảng giá hiện tại
board = trading_vci.price_board(symbols_list=['VCB', 'ACB'])
print("Bảng giá:")
print(board[['symbol', 'match_price', 'total_volume']])

# Lịch sử giao dịch
history = trading_vci.price_history(start="2024-01-01", end="2024-12-31")
print(f"\nLịch sử giao dịch: {len(history)} dòng")

# CafeF
trading_cafef = Trading(source="cafef", symbol="VCB")

# Giao dịch nước ngoài
foreign = trading_cafef.foreign_trade(start="2024-01-01", end="2024-12-31")
print(f"\nGiao dịch nước ngoài:")
print(foreign[['fr_buy_volume', 'fr_sell_volume', 'fr_net_volume']].tail())

# Giao dịch tự doanh
prop = trading_cafef.prop_trade(start="2024-01-01", end="2024-12-31")
print(f"\nGiao dịch tự doanh:")
print(prop[['prop_buy_volume', 'prop_sell_volume']].tail())

# Giao dịch nội bộ
insider = trading_cafef.insider_deal(start="2024-01-01", end="2024-12-31")
print(f"\nGiao dịch nội bộ:")
print(insider[['transaction_man', 'real_buy_volume', 'real_sell_volume']])
```

## So Sánh VCI vs CafeF

| Dữ Liệu | VCI | CafeF |
|---|:---:|:---:|
| Giá lịch sử | ✅ | ✅ |
| Bảng giá realtime | ✅ | ❌ |
| Thống kê giao dịch | ✅ | ✅ |
| Nước ngoài | ✅ | ✅ |
| Tự doanh | ✅ | ✅ |
| Nội bộ | ✅ | ✅ |
| Thống kê đặt lệnh | ✅ | ✅ |

## Phân Tích Ví Dụ

```python
from vnstock_data import Trading

# Phân tích khối ngoại
trading = Trading(source="cafef", symbol="VCB")
foreign = trading.foreign_trade(start="2024-01-01", end="2024-12-31")

# Net volume nước ngoài
foreign['net_pct'] = foreign['fr_net_volume'] / (
    foreign['fr_buy_volume'] + foreign['fr_sell_volume']
)

print("Top ngày mua ròng nước ngoài:")
print(foreign.nlargest(5, 'fr_net_volume')[
    ['fr_buy_volume', 'fr_sell_volume', 'fr_net_volume']
])
```

## Ma Trận Phương Thức Hỗ Trợ

| Phương Thức | VCI | CafeF |
|---|:---:|:---:|
| price_board | ✅ (70 cột) | ❌ |
| price_history | ✅ (36 cột, quý/năm) | ✅ (10 cột) |
| trading_stats | ❌ NotImplemented | ❌ |
| side_stats | ❌ NotImplemented | ❌ |
| order_stats | ❌ | ✅ (7 cột) |
| foreign_trade | ❌ | ✅ (8 cột) |
| prop_trade | ❌ | ✅ (4 cột) |
| insider_deal | ❌ | ⚠️ (hiếm) |
