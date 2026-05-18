# WebSocket Streaming Data — Standard Schema Reference

> Tài liệu chi tiết cấu trúc dữ liệu streaming từ WebSocket feed theo **tiêu chuẩn mới (FIX/Bloomberg-aligned)**.
> Tiêu chuẩn này được thiết kế để tương thích hoàn toàn với lớp UI `vnstock_data` .

---

## Tổng quan Thay Đổi Naming Conventions (Legacy vs Standard)

Tiêu chuẩn mới áp dụng các nguyên tắc đặt tên (naming conventions) sau so với bản Legacy:

1. **Sử dụng `snake_case`** cho tất cả các trường dữ liệu.
2. **Không viết tắt** trừ các chuẩn quốc tế như (OI, ETF, CW).
3. **Suffix `_price`** cho tất cả các mức giá: `open_price`, `high_price`, `close_price`.
4. **Suffix `_volume`** cho tất cả các khối lượng: `total_volume`, `buy_volume` (trước đây là `last_volume` hay `vol`).
5. **Suffix `_value`** cho giá trị: `total_value`, `net_value`.
6. **Prefix `foreign_`** cho dữ liệu giao dịch nước ngoài (trước đây dùng `fBVol`, `fSVal`...).
7. **Thay `timestamp` bằng `time`** (nhất quán với lớp UI `vnstock_data`).
8. **Thay `ticker` bằng `symbol`** trong streaming (nhất quán chuẩn FIX).
9. **Sổ lệnh (Board)** tự động nhận diện bên mua/bán (side) và map ra `bid_price_N` / `ask_price_N`.
10. **Lược bỏ các trường thừa (metadata)**: `event_type`, `change_flag`, `low_flag`.

Dưới đây là bộ từ điển field trả về cho 14 loại event theo chuẩn Standard.

---

## 1. `stock` — Giá Cổ Phiếu Cơ Sở

**Mô tả**: Dữ liệu khớp lệnh real-time cho cổ phiếu (HOSE, HNX, UPCOM). 

| Standard Field   | Type        | Mô tả                          | Legacy Field Tương Ứng | Sample Value          |
| ---------------- | ----------- | ------------------------------ | ---------------------- | --------------------- |
| `time`           | `timestamp` | Thời gian sự kiện              | `timestamp`            | `2026-03-20 09:10:14` |
| `symbol`         | `str`       | Mã chứng khoán                 | `symbol`               | `PVS`                 |
| `id`             | `int`       | ID session từ                  | `stock_id`             | `3220`                |
| `price`          | `float`     | Giá khớp lệnh cuối             | `last_price`           | `42.3`                |
| `volume`         | `int`       | Khối lượng lệnh vừa khớp       | `last_volume`          | `10`                  |
| `price_change`   | `float`     | Thay đổi giá so với tham chiếu | `change`               | `0.60`                |
| `percent_change` | `float`     | % thay đổi giá                 | `change_percent`       | `1.40`                |
| `total_volume`   | `int`       | Tổng KL giao dịch phiên        | `total_volume`         | `4280`                |
| `high_price`     | `float`     | Giá cao nhất phiên             | `high_price`           | `43.1`                |
| `low_price`      | `float`     | Giá thấp nhất phiên            | `low_price`            | `42.2`                |
| `open_price`     | `float`     | Giá mở cửa                     | `open_price`           | `43.0`                |
| `average_price`  | `float`     | Giá bình quân                  | `average_price`        | `42.72`               |
| `ceiling_price`  | `str/float` | Giá trần (trả về flag)         | `ceiling_actual`       | `i`                   |
| `side`           | `str`       | Bên mua/bán (B/S)              | `side`                 | `B`                   |
| `session_id`     | `str`       | ID phiên giao dịch             | — (Mới thêm)           | `1773972279123`       |

---

## 2. `stockps` — Giá Phái Sinh

**Mô tả**: Dữ liệu khớp lệnh cho hợp đồng tương lai VN30 và trái phiếu.

| Standard Field   | Type        | Mô tả                         | Legacy Field Tương Ứng | Sample Value          |
| ---------------- | ----------- | ----------------------------- | ---------------------- | --------------------- |
| `time`           | `timestamp` | Thời gian sự kiện             | `timestamp`            | `2026-03-20 09:04:39` |
| `symbol`         | `str`       | Mã hợp đồng phái sinh         | `symbol`               | `41I1G4000`           |
| `id`             | `int`       | ID session                    | `stock_id`             | `3220`                |
| `board_id`       | `str`       | ID bảng giao dịch             | `board_id`             | `G1`                  |
| `market_id`      | `str`       | Mã thị trường (DVX=phái sinh) | `market_id`            | `DVX`                 |
| `price`          | `float`     | Giá khớp                      | `last_price`           | `1830.8`              |
| `volume`         | `int`       | KL lệnh vừa khớp              | `last_volume`          | `2`                   |
| `price_change`   | `float`     | Thay đổi giá                  | `change`               | `3.7`                 |
| `percent_change` | `float`     | % thay đổi                    | `change_percent`       | `0.2`                 |
| `total_volume`   | `int`       | Tổng KL phiên                 | `total_volume`         | `15048`               |
| `high_price`     | `float`     | Giá cao nhất                  | `high_price`           | `1841.9`              |
| `low_price`      | `float`     | Giá thấp nhất                 | `low_price`            | `1826.0`              |
| `open_price`     | `float`     | Giá mở cửa                    | `open_price`           | `1841.0`              |
| `average_price`  | `float`     | Giá bình quân                 | `average_price`        | `1835.02`             |
| `ceiling_price`  | `str/float` | Giá trần                      | `ceiling_actual`       | `i`                   |
| `side`           | `str`       | Bên mua/bán                   | `side`                 | `B`                   |
| `session_id`     | `str`       | ID phiên                      | `session_id`           | `1773972279123`       |

---

## 3. `board` — Sổ Lệnh Cổ Phiếu (3 Bước Giá)

**Mô tả**: Sổ lệnh (order book) cho cổ phiếu trên HOSE/HNX.

> [!TIP]
>
> Trong bản Standard, các cột giá và khối lượng được tách bạch tự động thành **bid** (mua) hoặc **ask** (bán) dựa vào cờ `side`, thay vì chung chung là `price_1` như trước đây.

| Standard Field   | Type        | Mô tả                | Legacy Field Tương Ứng  | Sample Value          |
| ---------------- | ----------- | -------------------- | ----------------------- | --------------------- |
| `time`           | `timestamp` | Thời gian            | `timestamp`             | `2026-03-20 09:00:25` |
| `symbol`         | `str`       | Mã CK                | `symbol`                | `LCG`                 |
| `id`             | `int`       | ID session           | `stock_id`              | `3210`                |
| `side`           | `str`       | Bên (B=bid, S=ask)   | `side`                  | `B`                   |
| `bid_price_1..3` | `float`     | Giá mua bước 1 đến 3 | `price_1` (khi side=B)  | `9.9`                 |
| `bid_vol_1..3`   | `int`       | KL mua bước 1 đến 3  | `volume_1` (khi side=B) | `30`                  |
| `ask_price_1..3` | `float`     | Giá bán bước 1 đến 3 | `price_1` (khi side=S)  | `14.5`                |
| `ask_vol_1..3`   | `int`       | KL bán bước 1 đến 3  | `volume_1` (khi side=S) | `60`                  |

*(Lưu ý: Metadata `flag_1..3` đã bị drop)*

---

## 4. `boardps` — Sổ Lệnh Phái Sinh (10 Bước Giá)

**Mô tả**: Sổ lệnh cho phái sinh với độ sâu 10 bước giá mỗi bên (bid/ask).

| Standard Field      | Type        | Mô tả                 | Sample Value          |
| ------------------- | ----------- | --------------------- | --------------------- |
| `time`              | `timestamp` | Thời gian             | `2026-03-20 08:58:46` |
| `symbol`            | `str`       | Mã hợp đồng phái sinh | `41I2G9000`           |
| `id`                | `int`       | ID session            | `3211`                |
| `side`              | `str`       | Bên (B=bid, S=ask)    | `B`                   |
| `bid_price_1`..`10` | `float`     | Giá mua từ 1 đến 10   | `1970.1`              |
| `bid_vol_1`..`10`   | `int`       | KL mua từ 1 đến 10    | `1`                   |
| `ask_price_1`..`10` | `float`     | Giá bán từ 1 đến 10   | —                     |
| `ask_vol_1`..`10`   | `int`       | KL bán từ 1 đến 10    | —                     |

---

## 5. `index` — Chỉ Số Thị Trường

**Mô tả**: Dữ liệu chỉ số (VN-Index, VN30, HNX-Index...). Cập nhật mỗi 1-5 giây.

| Standard Field   | Type        | Mô tả                    | Legacy Field Tương Ứng | Sample Value          |
| ---------------- | ----------- | ------------------------ | ---------------------- | --------------------- |
| `time`           | `timestamp` | Thời gian sự kiện        | `timestamp`            | `2026-03-20 09:00:25` |
| `id`             | `int`       | ID chỉ số                | `index_id`             | `1101`                |
| `market_code`    | `str`       | Mã thị trường            | `market_code`          | `40` (HOSE)           |
| `close_price`    | `float`     | Giá trị chỉ số hiện tại  | `current_index`        | `2994.76`             |
| `open_price`     | `float`     | Giá trị mở cửa           | `open_index`           | `2999.12`             |
| `price_change`   | `float`     | Thay đổi                 | `change`               | `-4.36`               |
| `percent_change` | `float`     | % thay đổi               | `percent_change`       | `-0.145`              |
| `volume`         | `int`       | KL giao dịch             | `volume`               | `0`                   |
| `value`          | `float`     | Giá trị giao dịch        | `value`                | `0`                   |
| `advances`       | `int`       | Số mã tăng               | `advances`             | `0`                   |
| `declines`       | `int`       | Số mã giảm               | `declines`             | `0`                   |
| `no_change`      | `int`       | Số mã đứng yên           | `unchanged`            | `0`                   |
| `session_status` | `str`       | Trạng thái phiên (P/O/C) | `status`               | `P`                   |

---

## 6. `aggregatemarket` — Tổng Hợp Toàn Thị Trường

**Mô tả**: Snapshot tổng KL/giá trị giao dịch, dữ liệu GDNN toàn thị trường. 

| Standard Field        | Type        | Mô tả                        | Legacy Field          | Sample Value          |
| --------------------- | ----------- | ---------------------------- | --------------------- | --------------------- |
| `time`                | `timestamp` | Thời gian cập nhật           | `timestamp`           | `2026-03-20 09:14:55` |
| `total_volume`        | `int`       | Tổng KL giao dịch khớp lệnh  | `total_volume`        | `6008568`             |
| `total_value`         | `float`     | Tổng giá trị giao dịch       | `total_value`         | `66895.332`           |
| `put_through_volume`  | `int`       | KL giao dịch thỏa thuận      | `put_through_volume`  | `354915`              |
| `put_through_value`   | `float`     | Giá trị giao dịch thỏa thuận | `put_through_value`   | `36160250.47`         |
| `foreign_buy_volume`  | `int`       | KL khối ngoại mua            | `foreign_buy_volume`  | `119800`              |
| `foreign_sell_volume` | `int`       | KL khối ngoại bán            | `foreign_sell_volume` | `83270`               |
| `foreign_buy_value`   | `float`     | Giá trị KN mua               | `foreign_buy_value`   | `2188240000`          |
| `foreign_sell_value`  | `float`     | Giá trị KN bán               | `foreign_sell_value`  | `1405906645`          |
| `foreign_net_volume`  | `int`       | KL KN ròng (mua - bán)       | `foreign_net_volume`  | `36530`               |
| `foreign_net_value`   | `float`     | Giá trị KN ròng              | `foreign_net_value`   | `782333355`           |
| `advances`            | `int`       | Số mã tăng                   | `advances`            | `81`                  |
| `declines`            | `int`       | Số mã giảm                   | `declines`            | `66`                  |
| `no_change`           | `int`       | Số mã đứng giá               | `unchanged`           | `96`                  |

---

## 7. `aggregateps` — Tổng Hợp Phái Sinh

| Standard Field        | Type        | Mô tả                   | Legacy Field          | Sample Value          |
| --------------------- | ----------- | ----------------------- | --------------------- | --------------------- |
| `time`                | `timestamp` | Thời gian               | `timestamp`           | `2026-03-20 09:02:25` |
| `lot`                 | `int`       | Tổng hợp đồng giao dịch | `lot`                 | `11175`               |
| `foreign_buy_volume`  | `int`       | KN mua (hợp đồng)       | `foreign_buy_volume`  | `78`                  |
| `foreign_sell_volume` | `int`       | KN bán                  | `foreign_sell_volume` | `968`                 |
| `foreign_net_volume`  | `int`       | KN ròng                 | `foreign_net_volume`  | `-890`                |
| `bid_volume`          | `int`       | Tổng KL chờ mua         | `bid_volume`          | `2264`                |
| `ask_volume`          | `int`       | Tổng KL chờ bán         | `ask_volume`          | `4914`                |
| `open_interest`       | `int`       | Tổng vị thế mở (OI)     | `open_interest`       | `25368`               |

---

## 8. `aggregatecw` & `aggregateetf` — Tổng Hợp CW / ETF

Cấu trúc giống hệt nhau.

| Standard Field | Type        | Mô tả             | Legacy Field   | Sample Value          |
| -------------- | ----------- | ----------------- | -------------- | --------------------- |
| `time`         | `timestamp` | Thời gian         | `timestamp`    | `2026-03-20 09:16:00` |
| `total_volume` | `int`       | Tổng KL giao dịch | `total_volume` | `91300`               |
| `total_value`  | `float`     | Tổng giá trị      | `total_value`  | `81580000`            |
| `advances`     | `int`       | Số mã tăng        | `advances`     | `37`                  |
| `declines`     | `int`       | Số mã giảm        | `declines`     | `9`                   |
| `no_change`    | `int`       | Số mã đứng        | `unchanged`    | `12`                  |

---

## 9. `aggregateforeigngroup` — GDNN Theo Nhóm (ETF, CW)

| Standard Field | Type        | Mô tả                         | Sample Value          |
| -------------- | ----------- | ----------------------------- | --------------------- |
| `time`         | `timestamp` |                               | `2026-03-20 10:45:00` |
| `group`        | `str`       | Nhóm tài sản (ETF, CW, Stock) | `ETF`                 |
| `buy_volume`   | `int`       | KL mua                        | `42260`               |
| `sell_volume`  | `int`       | KL bán                        | `413800`              |
| `buy_value`    | `float`     | Giá trị mua                   | `1388002500.0`        |
| `sell_value`   | `float`     | Giá trị bán                   | `13837818000.0`       |
| `net_volume`   | `int`       | KL ròng                       | `-371540`             |
| `net_value`    | `float`     | Giá trị ròng                  | `-12449815500.0`      |

---

## 10. `aggregateforeignmarket` — GDNN Theo Sàn

| Standard Field | Type        | Mô tả                    | Sample Value          |
| -------------- | ----------- | ------------------------ | --------------------- |
| `time`         | `timestamp` |                          | `2026-03-20 10:45:00` |
| `market_code`  | `str`       | Mã sàn (10=HOSE, 02=HNX) | `10`                  |
| `buy_volume`   | `int`       | KL mua                   | `20636040`            |
| `sell_volume`  | `int`       | KL bán                   | `37855410`            |
| `buy_value`    | `float`     | Giá trị mua              | `598890357500.0`      |
| `sell_value`   | `float`     | Giá trị bán              | `1279557381150.0`     |
| `net_volume`   | `int`       | KL ròng                  | `-17219370`           |
| `net_value`    | `float`     | Giá trị ròng             | `-680667023650.0`     |
| `room`         | `int`       | Tổng room                | `...`                 |
| `current_room` | `int`       | Room còn lại             | `...`                 |

---

## 11. `spt` — Giao Dịch Thỏa Thuận (Put-Through)

| Standard Field     | Type        | Mô tả                        | Legacy Field       | Sample Value          |
| ------------------ | ----------- | ---------------------------- | ------------------ | --------------------- |
| `time`             | `timestamp` | Thời gian                    | `timestamp`        | `2026-03-20 09:59:46` |
| `id`               | `int`       | ID giao dịch                 | `transaction_id`   | `2112`                |
| `transaction_type` | `str`       | Loại (PTM=Put-Through Match) | `transaction_type` | `PTM`                 |
| `symbol`           | `str`       | Mã CK                        | `symbol`           | `DSE125004`           |
| `price`            | `float`     | Giá thỏa thuận               | `price`            | `101.766`             |
| `volume`           | `int`       | Khối lượng                   | `volume`           | `9`                   |
| `value`            | `float`     | Giá trị                      | `value`            | `915.894`             |
| `market_id`        | `str`       | Sàn                          | `market_id`        | `02`                  |
| `firm_no`          | `str`       | Mã CTCK                      | `firm_no`          | —                     |

---

## 12. `soddlot` — Giao Dịch Lô Lẻ

| Standard Field    | Type        | Mô tả          | Legacy Field      | Sample Value          |
| ----------------- | ----------- | -------------- | ----------------- | --------------------- |
| `time`            | `timestamp` | Thời gian      | `timestamp`       | `2026-03-20 09:00:25` |
| `symbol`          | `str`       | Mã CK          | `symbol`          | `GVR`                 |
| `id`              | `int`       | ID             | `stock_id`        | `9100`                |
| `market_id`       | `str`       | Mã thị trường  | `market_id`       | `G4`                  |
| `ceiling_price`   | `float`     | Giá trần       | `ceiling_price`   | `34.7`                |
| `floor_price`     | `float`     | Giá sàn        | `floor_price`     | `30.2`                |
| `reference_price` | `float`     | Giá tham chiếu | `reference_price` | `32.45`               |
| `price`           | `float`     | Giá khớp       | `last_price`      | `0`                   |
| `volume`          | `int`       | KL khớp        | `last_volume`     | `0`                   |
| `lot`             | `int`       | Số lô          | `lot`             | `0`                   |
| `market_code`     | `str`       | Mã sàn         | `market_code`     | `10`                  |
| `bid_price_1..3`  | `float`     | 3 bước giá mua | `bid_price_1..3`  | `32.45`               |
| `bid_vol_1..3`    | `int`       | KL mua         | `bid_volume_1..3` | `221`                 |
| `ask_price_1..3`  | `float`     | 3 bước giá bán | `ask_price_1..3`  | `33.5`                |
| `ask_vol_1..3`    | `int`       | KL bán         | `ask_volume_1..3` | `66`                  |