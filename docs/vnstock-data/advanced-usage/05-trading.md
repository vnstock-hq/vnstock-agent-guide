# Trading - Dữ Liệu Giao Dịch

Module `Trading` cung cấp các hàm để truy xuất dữ liệu giao dịch realtime (bảng giá), lịch sử giá, thống kê giao dịch khối ngoại (Foreign), tự doanh (Proprietary), và giao dịch nội bộ (Insider Dealing).

## Điểm Nổi Bật & Lưu Ý Nguồn Dữ Liệu

| Nguồn | Đặc Điểm | Độ Trễ / Tần Suất | Lưu Ý Quan Trọng |
| :--- | :--- | :--- | :--- |
| **VCI** | Nguồn dữ liệu phong phú nhất. Phân tách rõ ràng các hàm lấy dữ liệu Khối ngoại, Tự doanh, Summary. | **Realtime** cho bảng giá. **T-1** cho lịch sử. | Dữ liệu lịch sử thường chốt vào cuối ngày giao dịch. |
| **KBS** | Hỗ trợ bảng giá Realtime cập nhật nhanh (T). Gộp chung thông tin khối ngoại trong lịch sử giá/bảng giá. | **Realtime** (Cập nhật tại ngày giao dịch hiện tại). | Hàm `trade_history` là thuật ngữ chuẩn mới (thay thế `price_history`). |
| **CafeF** | Nguồn dữ liệu lịch sử lâu đời. | **T-1** (thường cập nhật sau phiên). | **Lưu ý:** Dữ liệu đôi khi bị **khuyết ngày** không rõ lý do. Nên dùng đối chiếu hoặc dự phòng. |

---

## 1. Khởi Tạo & Sử Dụng

```python
from vnstock_data import Trading

# Khởi tạo
tr_vci = Trading(symbol='TCB', source='VCI') 
tr_kbs = Trading(symbol='TCB', source='KBS')

# Lấy lịch sử giá
df_hist = tr_vci.price_history(start='2024-01-01', end='2024-01-31')

# Lấy bảng giá realtime
df_board = tr_kbs.price_board(['TCB', 'VNM'])
```

---

## 2. Chi Tiết Nguồn VCI (Vietcap)

### Bảng Giá (Realtime)
**`price_board(symbols_list, board='stock'|'odd_lot'|'put_through')`**

| Field | Type | Description |
| :--- | :--- | :--- |
| `listing_symbol` | `str` | Mã chứng khoán |
| `listing_exchange` | `str` | Sàn giao dịch |
| `match_price` | `float` | Giá khớp gần nhất |
| `match_vol` | `float` | Khối lượng khớp |
| `highest` | `float` | Giá cao nhất |
| `lowest` | `float` | Giá thấp nhất |
| `avg_match_price` | `float` | Giá khớp bình quân |

### Lịch Sử Giá
**`price_history(start, end, ...)`**

| Field | Type | Description |
| :--- | :--- | :--- |
| `trading_date` | `datetime` | Ngày giao dịch |
| `open` | `float` | Giá mở cửa |
| `high` | `float` | Giá cao nhất |
| `low` | `float` | Giá thấp nhất |
| `close` | `float` | Giá đóng cửa |
| `matched_volume` | `float` | Khối lượng khớp lệnh |
| `price_change` | `float` | Thay đổi giá so với phiên trước |
| `percent_price_change`| `float` | % thay đổi giá |

### Summary (Thống kê tổng hợp)
**`summary(start, end, ...)`**

| Field | Type | Description |
| :--- | :--- | :--- |
| `average_match_volume`| `float` | Khối lượng khớp lệnh trung bình |
| `average_deal_volume` | `float` | Khối lượng thỏa thuận trung bình |
| `total_match_volume` | `float` | Tổng khối lượng khớp lệnh trong kỳ |
| `total_deal_volume` | `float` | Tổng khối lượng thỏa thuận trong kỳ |
| `fr_net_volume_total` | `float` | Tổng khối lượng ròng khối ngoại |

### Foreign Trade (Khối ngoại)
**`foreign_trade(start, end)`**

| Field | Type | Description |
| :--- | :--- | :--- |
| `trading_date` | `datetime` | Ngày giao dịch |
| `fr_buy_value_matched`| `float` | Giá trị mua khớp lệnh |
| `fr_sell_value_matched`|`float` | Giá trị bán khớp lệnh |
| `fr_net_value_total` | `float` | Giá trị ròng tổng quát |
| `fr_total_room` | `float` | Room khối ngoại tối đa |
| `fr_current_room` | `float` | Room khối ngoại hiện tại |

### Proprietary Trade (Tự doanh)
**`prop_trade(start, end)`**

| Field | Type | Description |
| :--- | :--- | :--- |
| `trading_date` | `datetime` | Ngày giao dịch |
| `total_buy_trade_volume`| `float`| Tổng khối lượng mua tự doanh |
| `total_sell_trade_volume`|`float`| Tổng khối lượng bán tự doanh |
| `total_trade_net_value` | `float`| Giá trị ròng tự doanh |
| `percent_buy_trade_volume`|`float`| % Tỷ trọng mua tự doanh |

### Insider Deal (Giao dịch nội bộ)
**`insider_deal(limit, ...)`**

| Field | Type | Description |
| :--- | :--- | :--- |
| `trader_name` | `str` | Người thực hiện giao dịch |
| `trader_position` | `str` | Chức vụ |
| `event_name` | `str` | Loại sự kiện (GD nội bộ...) |
| `action_type` | `str` | Loại hành động (Mua/Bán) |
| `start_date` | `datetime` | Ngày bắt đầu đăng ký |
| `end_date` | `datetime` | Ngày kết thúc đăng ký |
| `share_register` | `float` | Lượng đăng ký |
| `share_acquire` | `float` | Lượng thực hiện |

---

## 3. Chi Tiết Nguồn KBS (KB Securities)

### Price Board (Bảng giá)
**`price_board(symbols_list, board='stock'|'odd_lot'|'put_through')`**

| Field | Type | Description |
| :--- | :--- | :--- |
| `symbol` | `str` | Mã chứng khoán |
| `time` | `int` | Timestamp cập nhật (ms) |
| `ceiling_price` | `int` | Giá trần |
| `floor_price` | `int` | Giá sàn |
| `bid_price_1`...`3` | `float` | Giá đặt mua |
| `ask_price_1`...`3` | `float` | Giá đặt bán |
| `foreign_buy_volume` | `int` | Khối lượng nước ngoài mua |
| `foreign_sell_volume` | `int` | Khối lượng nước ngoài bán |

### Matched By Price (Intraday)
**`matched_by_price()`**

| Field | Type | Description |
| :--- | :--- | :--- |
| `price` | `int` | Mức giá khớp |
| `buyVol` | `int` | Khối lượng mua chủ động |
| `sellVol` | `int` | Khối lượng bán chủ động |
| `totalVol` | `int` | Tổng khối lượng khớp tại mức giá |

### Trade History
**`trade_history()`**: Dữ liệu lịch sử giao dịch (bao gồm cả OHLCV và Foreign).
*(Cấu trúc tương tự Price History nhưng có thêm cột Foreign)*

---

## 4. Chi Tiết Nguồn CafeF

### Thông tin cơ bản
**`price_history`**: `open`, `high`, `low`, `close`, `matched_volume`, `change_pct`.

### Foreign Trade (Khối ngoại)
**`foreign_trade`**: `fr_buy_volume`, `fr_sell_volume`, `fr_net_volume`, `fr_ownership` (% sở hữu).

### Proprietary Trade (Tự doanh)
**`prop_trade`**: `prop_buy_volume`, `prop_sell_volume` (đã chuẩn hóa prefix `prop_`).

### Insider Deal
**`insider_deal`**

| Field | Type | Description |
| :--- | :--- | :--- |
| `transaction_man` | `str` | Người giao dịch |
| `transaction_man_position`| `str` | Chức vụ |
| `plan_buy_volume` | `int` | Lượng mua đăng ký |
| `real_buy_volume` | `int` | Lượng mua thực tế |
| `transaction_note` | `str` | Ghi chú giao dịch |

### Order Stats (Thống kê lệnh)
**`order_stats`**

| Field | Type | Description |
| :--- | :--- | :--- |
| `buy_orders` | `int` | Số lệnh mua |
| `sell_orders` | `int` | Số lệnh bán |
| `buy_volume` | `int` | Khối lượng đặt mua |
| `sell_volume` | `int` | Khối lượng đặt bán |
| `avg_buy_order_volume`| `int` | Trung bình lệnh mua |
