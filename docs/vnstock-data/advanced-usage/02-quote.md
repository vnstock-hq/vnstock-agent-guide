
# Quote API

Module `quote` cung cấp các hàm chuyên biệt để truy xuất dữ liệu thị trường (market data) bao gồm: lịch sử giá OHLCV, dữ liệu khớp lệnh trong ngày (intraday), và độ sâu thị trường (price depth/order book).

Hiện tại, module này hỗ trợ 4 nguồn dữ liệu chính thông qua cơ chế unified wrapper: `VCI`, `KBS`, `VND`, và `MAS`.

## Khởi tạo

Để sử dụng, bạn khởi tạo class `Quote` từ package `vnstock_data`. Class này sẽ tự động routing request đến implementation phù hợp dựa trên tham số `source`.

```python
from vnstock_data import Quote

# Khởi tạo quote adapter với nguồn dữ liệu VCI (mặc định KBS nếu không truyền source)
quote = Quote(source='VCI')
```

**Tham số khởi tạo:**

| Tham số | Kiểu dữ liệu | Mặc định | Mô tả |
| :--- | :--- | :--- | :--- |
| `source` | `str` | `'KBS'` | Mã nguồn dữ liệu. Hỗ trợ: `'VCI'`, `'KBS'`, `'VND'`, `'MAS'`. |
| `symbol` | `str` | `""` | (Tùy chọn) Mã chứng khoán (cổ phiếu, chỉ số, hợp đồng tương lai, chứng quyền, ETF, trái phiếu, vv) mặc định cho các gọi hàm sau này. |

---

## 2. Lịch sử giá (History)

Truy xuất dữ liệu lịch sử giá (OHLCV) theo khung thời gian ngày. Dữ liệu này đã được điều chỉnh kỹ thuật (adjusted price) phù hợp để vẽ biểu đồ kỹ thuật.

### Hàm: `history`

```python
def history(self, symbol=None, start=None, end=None, interval='1D', length=None)
```

**Tham số:**

-   `symbol` (`str`): Mã chứng khoán hoặc mã chỉ số.
    - **Hỗ trợ Index**: HNXINDEX, UPCOMINDEX, VN30, VN100, HNX30 (chỉ khung ngày).
    - **Hỗ trợ Phái sinh**: Tự động nhận diện và chuyển đổi mã hợp đồng tương lai sang kiểu mới để gọi hàm (Ví dụ: `VN30F1M` -> `41I1G2000`).
-   `start` (`str`): Ngày bắt đầu (định dạng `YYYY-mm-dd`). Bắt buộc nếu không có `length`.
-   `end` (`str`): Ngày kết thúc (định dạng `YYYY-mm-dd`). Mặc định là ngày hiện tại.
-   `length` (`str` | `int`): Khoảng thời gian lấy dữ liệu kể từ `end` ngược về quá khứ.
    -   Ví dụ: `'1M'` (1 tháng), `'3M'` (3 tháng), `'1Y'` (1 năm), `'2W'` (2 tuần).
    -   Nếu dùng `length`, `start` và `end` sẽ được tự động tính toán.
-   `interval` (`str`): Khung thời gian.
    -   `'1D'` (Daily): Hỗ trợ bởi tất cả các nguồn (`VCI`, `KBS`, `VND`, `MAS`).
    -   `'1m'` (1 Minute): Hỗ trợ bởi tất cả các nguồn (dữ liệu ngắn hạn).
    -   `'1H'` (Hourly): Ổn định nhất trên `VCI` và `MAS`.
    -   Các khung khác tùy nguồn: `'5m'`, `'15m'`, `'30m'`.

**Dữ liệu trả về (DataFrame):**

Tất cả các nguồn dữ liệu đều được chuẩn hóa bao gồm: `time`, `open`, `high`, `low`, `close`, `volume`.

### Ví dụ sử dụng

```python
from vnstock_data import Quote

quote = Quote(source='VCI')

# Cách 1: Sử dụng Start/End
df = quote.history(symbol='TCB', start='2023-12-01', end='2023-12-05', interval='1D')

# Cách 2: Sử dụng Length (tiện lợi)
# Lấy dữ liệu 3 tháng gần nhất, khung 1 giờ
df = quote.history(symbol='TCB', length='3M', interval='1H')

print(df.tail())
```

**Kết quả mẫu:**

```
        time   open   high    low  close   volume
0 2023-12-01  13.98  14.10  13.86  14.05  2696825
1 2023-12-04  14.08  14.41  14.08  14.27  4762393
2 2023-12-05  14.29  14.31  14.12  14.20  3094771
```

### Hỗ trợ chỉ số thị trường

Ngoài mã cổ phiếu, bạn có thể truyền vào các mã chỉ số thị trường phổ biến. Các mã này được hỗ trợ trên tất cả các nguồn (`VCI`, `KBS`, `VND`, `MAS`):

| Mã chỉ số | Mô tả |
| :--- | :--- |
| `VNINDEX` | Chỉ số VN-Index (HOSE) |
| `VN30` | Chỉ số VN30 |
| `HNX` | Chỉ số HNX-Index |
| `UPCOM` | Chỉ số UPCoM-Index |

Một số dạng chỉ số khác được hỗ trợ tuỳ nguồn ví dụ VND:
- `VN30`, `VN100`, `HNX30`, `VNSML`, `VNMID`, `VNALL`

**Chỉ Số Ngành**:
- `VNREAL` - Bất động sản
- `VNMAT` - Nguyên vật liệu
- `VNIT` - Công nghệ
- `VNHEAL` - Chăm sóc sức khỏe
- `VNFINSELECT`, `VNFIN` - Tài chính
- `VNENE` - Năng lượng
- `VNCONS`, `VNCOND` - Hàng tiêu dùng
**Ví dụ lấy lịch sử VNINDEX:**

```python
df_index = quote.history(symbol='VNINDEX', start='2023-01-01', end='2023-01-31')
```

---

## 3. Khớp lệnh trong ngày (Intraday)

Truy xuất danh sách các lệnh đã khớp (order matching) real-time hoặc lịch sử trong phiên của một mã chứng khoán.

### Hàm: `intraday`

```python
def intraday(self, symbol=None, page_size=100)
```

**Tham số:**

-   `symbol` (`str`): Mã chứng khoán.
-   `page_size` (`int`): Số lượng bản ghi muốn lấy trong một lần gọi (paging).

**Dữ liệu trả về:**

Cấu trúc dữ liệu có sự khác biệt nhỏ giữa các nguồn:

| Nguồn | Các cột trả về |
| :--- | :--- |
| **VCI / KBS** | `time`, `price`, `volume`, `match_type`, `id` |
| **MAS** | `time`, `price`, `volume`, `match_type` (không có `id`) |
| **VND** | *Hiện tại chưa đẩy đủ các method như KBS và VCI, MAS* |

### Ví dụ sử dụng

```python
from vnstock_data import Quote

# Sử dụng nguồn VCI cho dữ liệu Intraday chi tiết
quote = Quote(source='VCI')
df = quote.intraday(symbol='TCB', page_size=10)
print(df.head())
```

**Kết quả mẫu (VCI Source):**

```
                       time  price  volume match_type         id
0 2024-01-30 14:29:19+07:00  35.25     200       Sell  429964787
1 2024-01-30 14:29:23+07:00  35.25     100       Sell  429965133
2 2024-01-30 14:29:23+07:00  35.25    1800       Sell  429965132
3 2024-01-30 14:29:27+07:00  35.25     500        Buy  429965494
4 2024-01-30 14:29:42+07:00  35.25    1000        Buy  429967143
```

---

## 4. Độ sâu thị trường (Price Depth)

Truy xuất thông tin độ sâu thị trường, bao gồm các mức giá đặt mua (bid) và đặt bán (ask) tốt nhất cùng khối lượng tương ứng.

### Hàm: `price_depth`

```python
def price_depth(self, symbol=None)
```

**Tham số:**

-   `symbol` (`str`): Mã chứng khoán.

**Dữ liệu trả về (DataFrame):**

| Nguồn | Các cột trả về |
| :--- | :--- |
| **VCI / MAS** | `price` (Giá), `volume` (Tổng KL), `buy_volume` (KL Mua), `sell_volume` (KL Bán), `undefined_volume` |
| **KBS** | `price`, `buyVol` (KL Mua), `sellVol` (KL Bán), `unknownVol`, `totalVol` (Tổng KL) |
| **VND** | *Chưa hỗ trợ* |

### Ví dụ sử dụng

```python
from vnstock_data import Quote

quote = Quote(source='VCI')
df = quote.price_depth(symbol='TCB')
print(df.head())
```

**Kết quả mẫu (VCI Source):**

```
     price     volume  buy_volume  sell_volume  undefined_volume
0  35900.0  3424400.0         0.0          0.0         3424400.0
1  35300.0   328100.0    316900.0      11200.0               0.0
```

---

## Tổng kết so sánh nguồn dữ liệu

| Tính năng | VCI | KBS | VND | MAS |
| :--- | :---: | :---: | :---: | :---: |
| **Lịch sử giá (History)** | ✅ Ổn định | ✅ Ổn định | ✅ Ổn định | ✅ Ổn định |
| **Intraday** | ✅ Chi tiết | ✅ Chi tiết | ⚠️ Chưa ổn định | ✅ Cơ bản |
| **Price Depth** | ✅ Có | ✅ Có | ❌ Chưa có | ✅ Có |
| **Chỉ số thị trường** | ✅ Có | ✅ Có | ✅ Có | ✅ Có |

**Khuyến nghị**:
- Sử dụng **VCI**, **KBS** hoặc **MAS** cho nhu cầu dữ liệu **History** và **Intraday** vì tính ổn định và chi tiết cao. Dùng **VND** để lấy dữ liệu `history` cho các mã chỉ số đa dạng. Không sử dụng nguồn VCI trên Google Colab hoặc dịch vụ liên quan Google Cloud do chính sách chặn IP từ nguồn dữ liệu này.
