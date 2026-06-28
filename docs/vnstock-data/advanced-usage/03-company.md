# Company - Thông Tin Công Ty, Cổ Đông, Ban Lãnh Đạo

Lớp `Company` cung cấp thông tin chi tiết về các công ty niêm yết, bao gồm hồ sơ, cổ đông, ban lãnh đạo và các sự kiện liên quan.

## Tổng Quan & So Sánh Nguồn Dữ Liệu

Package hỗ trợ 2 nguồn dữ liệu: **VCI** (Vietcap) và **KBS** (KB Securities). Dưới đây là bảng so sánh khả năng hỗ trợ của từng nguồn:

| Tính năng (Method)  |  VCI  |  KBS  | Mô tả                                                                                                                      |
| :------------------ | :---: | :---: | :------------------------------------------------------------------------------------------------------------------------- |
| **overview**        |   ✅   |   ✅   | Thông tin hồ sơ doanh nghiệp. VCI chi tiết hơn về cơ cấu cổ đông.                                                          |
| **shareholders**    |   ✅   |   ✅   | Danh sách cổ đông lớn.                                                                                                     |
| **officers**        |   ✅   |   ✅   | Ban lãnh đạo. VCI hỗ trợ lọc trạng thái (đương nhiệm/từ nhiệm).                                                            |
| **subsidiaries**    |   ✅   |   ✅   | Công ty con & liên kết.                                                                                                    |
| **news**            |   ✅   |   ✅   | Tin tức liên quan.                                                                                                         |
| **events**          |   ✅   |   ⚠️   | Sự kiện quyền (trả cổ tức, họp ĐHCĐ). KBS hiện tại trả về dữ liệu trống.                                                   |
| **capital_history** |   ❌   |   ✅   | Lịch sử tăng vốn. **Chỉ có trên KBS**.                                                                                     |
| **insider_trading** |   ❌   |   ⚠️   | Giao dịch nội bộ. **Chỉ có trên KBS** (tuy nhiên dữ liệu trả về tuỳ cổ phiếu, có thể trống nếu không có giao dịch nội bộ). |
| **ratio_summary**   |   ✅   |   ❌   | Tóm tắt tỷ số tài chính (P/E, ROE...). **Chỉ có trên VCI**.                                                                |
| **trading_stats**   |   ✅   |   ❌   | Thống kê giao dịch (NN mua/bán, Room). **Chỉ có trên VCI**.                                                                |

**Khuyến nghị**:
- Sử dụng **VCI** làm mặc định cho hầu hết nhu cầu phân tích cơ bản.
- Sử dụng **KBS** khi cần lấy **Lịch sử vốn (Capital History)**.

---

## Khởi Tạo

```python
from vnstock_data import Company

# Nguồn VCI
company_vci = Company(source="VCI", symbol="TCB")

# Nguồn KBS
company_kbs = Company(source="KBS", symbol="TCB")
```

---

## 1. overview() - Thông Tin Tổng Quan

### Nguồn VCI

```python
df = company_vci.overview()
```

| Cột (Column)                  | Kiểu Dữ Liệu | Mô Tả                            |
| :---------------------------- | :----------- | :------------------------------- |
| `symbol`                      | string       | Mã chứng khoán                   |
| `id`                          | string       | ID nội bộ                        |
| `issue_share`                 | int          | Số lượng cổ phiếu lưu hành       |
| `history`                     | string       | Lịch sử hình thành và phát triển |
| `company_profile`             | string       | Giới thiệu chung về công ty      |
| `icb_name3`                   | string       | Ngành cấp 3 (ICB)                |
| `icb_name2`                   | string       | Ngành cấp 2 (ICB)                |
| `icb_name4`                   | string       | Ngành cấp 4 (ICB)                |
| `financial_ratio_issue_share` | int          | SLCP dùng tính chỉ số tài chính  |
| `charter_capital`             | int          | Vốn điều lệ (VND)                |

### Nguồn KBS

```python
df = company_kbs.overview()
```

| Cột (Column)          | Kiểu Dữ Liệu | Mô Tả                           |
| :-------------------- | :----------- | :------------------------------ |
| `business_model`      | string       | Mô hình kinh doanh              |
| `symbol`              | string       | Mã chứng khoán                  |
| `founded_date`        | string       | Ngày thành lập                  |
| `charter_capital`     | int          | Vốn điều lệ                     |
| `number_of_employees` | int          | Số lượng nhân viên              |
| `listing_date`        | string       | Ngày niêm yết                   |
| `exchange`            | string       | Sàn giao dịch                   |
| `listing_price`       | int          | Giá chào sàn                    |
| `listed_volume`       | int          | Khối lượng niêm yết lần đầu     |
| `ceo_name`            | string       | Tên CEO                         |
| `ceo_position`        | string       | Chức vụ CEO                     |
| `inspector_name`      | string       | Trưởng Ban Kiểm Soát            |
| `address`             | string       | Địa chỉ trụ sở                  |
| `phone`               | string       | Số điện thoại                   |
| `email`               | string       | Email liên hệ                   |
| `website`             | string       | Website công ty                 |
| `history`             | string       | Lịch sử công ty                 |
| `outstanding_shares`  | int          | Số lượng cổ phiếu đang lưu hành |

---

## 2. shareholders() - Cổ Đông Lớn & Cơ Cấu Cổ Đông

Phương thức `shareholders` hỗ trợ truy xuất danh sách cổ đông lớn hoặc cấu trúc cơ cấu sở hữu tổng hợp của doanh nghiệp thông qua tham số `mode`:
- `mode='detailed'` (Mặc định): Danh sách chi tiết các cổ đông lớn cá nhân/tổ chức.
- `mode='summary'`: Báo cáo cơ cấu sở hữu tổng hợp (tỷ lệ nhà nước, khối ngoại, ban lãnh đạo, tổ chức, cá nhân...).

### Nguồn VCI

#### 1. Chi tiết cổ đông lớn (`mode='detailed'`)

```python
df = company_vci.shareholders(mode='detailed')
```

| Cột (Column)       | Kiểu Dữ Liệu | Mô Tả                                                                    |
| :----------------- | :----------- | :----------------------------------------------------------------------- |
| `symbol`           | string       | Mã chứng khoán                                                           |
| `name`             | string       | Tên cổ đông lớn                                                          |
| `shareholder_type` | string       | Phân loại cổ đông (`Individual` - Cá nhân hoặc `Organization` - Tổ chức) |
| `total_shares`     | int          | Số lượng cổ phiếu nắm giữ                                                |
| `rate`             | float        | Tỷ lệ sở hữu (ví dụ: `0.15` tương ứng với 15%)                           |
| `date`             | string       | Ngày cập nhật                                                            |

#### 2. Cơ cấu sở hữu tổng hợp (`mode='summary'`)

```python
df = company_vci.shareholders(mode='summary')
```

| Cột (Column)             | Kiểu Dữ Liệu | Mô Tả                                    |
| :----------------------- | :----------- | :--------------------------------------- |
| `symbol`                 | string       | Mã chứng khoán                           |
| `total_shares`           | int          | Tổng số lượng cổ phiếu dùng để phân tích |
| `state_percentage`       | float        | Tỷ lệ sở hữu của Nhà nước                |
| `foreign_percentage`     | float        | Tỷ lệ sở hữu nước ngoài                  |
| `other_percentage`       | float        | Tỷ lệ sở hữu khác                        |
| `foreigner_volume`       | int          | Số lượng cổ phiếu khối ngoại nắm giữ     |
| `other_volume`           | int          | Số lượng cổ phiếu khác nắm giữ           |
| `state_volume`           | int          | Số lượng cổ phiếu nhà nước nắm giữ       |
| `bod_percentage`         | float        | Tỷ lệ sở hữu của Hội đồng quản trị       |
| `institution_percentage` | float        | Tỷ lệ sở hữu của tổ chức                 |

---

### Nguồn KBS

#### 1. Chi tiết cổ đông lớn (`mode='detailed'`)

```python
df = company_kbs.shareholders(mode='detailed')
```

| Cột (Column)           | Kiểu Dữ Liệu | Mô Tả                     |
| :--------------------- | :----------- | :------------------------ |
| `name`                 | string       | Tên cổ đông lớn           |
| `date`                 | string       | Ngày cập nhật             |
| `shares_owned`         | int          | Số lượng cổ phiếu nắm giữ |
| `ownership_percentage` | float        | Tỷ lệ sở hữu (%)          |
| `owner_type`           | string       | Phân loại cổ đông         |

#### 2. Cơ cấu sở hữu tổng hợp (`mode='summary'`)

> 💡 **Lưu ý**: Trên nguồn KBS, chế độ này tương đương với hàm `company_kbs.ownership()` trước đây.

```python
df = company_kbs.shareholders(mode='summary')
```

| Cột (Column)           | Kiểu Dữ Liệu | Mô Tả                                                                      |
| :--------------------- | :----------- | :------------------------------------------------------------------------- |
| `owner_type`           | string       | Phân loại thành phần sở hữu (VD: Cổ đông nước ngoài, Hội đồng quản trị...) |
| `ownership_percentage` | float        | Tỷ lệ sở hữu (%)                                                           |
| `shares_owned`         | int          | Số lượng cổ phiếu nắm giữ                                                  |
| `update_date`          | string       | Ngày cập nhật                                                              |

---

## 3. officers() - Ban Lãnh Đạo

### Nguồn VCI

Dữ liệu chi tiết, bao gồm cả số lượng cổ phiếu sở hữu.

```python
# filter_by='working' (đương nhiệm), 'resigned' (đã nghỉ), 'all'
df = company_vci.officers(filter_by='working')
```

| Cột (Column)          | Kiểu Dữ Liệu | Mô Tả                   |
| :-------------------- | :----------- | :---------------------- |
| `id`                  | string       | ID lãnh đạo             |
| `officer_name`        | string       | Tên lãnh đạo            |
| `officer_position`    | string       | Chức vụ                 |
| `position_short_name` | string       | Chức vụ viết tắt        |
| `update_date`         | string       | Ngày cập nhật           |
| `officer_own_percent` | float        | Tỷ lệ sở hữu cổ phần    |
| `quantity`            | int          | Số lượng cổ phần sở hữu |

### Nguồn KBS

Danh sách cơ bản.

```python
df = company_kbs.officers()
```

| Cột (Column)  | Kiểu Dữ Liệu | Mô Tả                |
| :------------ | :----------- | :------------------- |
| `from_date`   | string       | Năm bắt đầu/bổ nhiệm |
| `position`    | string       | Chức vụ              |
| `name`        | string       | Tên lãnh đạo         |
| `position_en` | string       | Chức vụ (Tiếng Anh)  |
| `owner_code`  | string       | Mã chức vụ           |

---

## 4. subsidiaries() - Công Ty Con & Liên Kết

### Nguồn VCI

```python
df = company_vci.subsidiaries()
```

| Cột (Column)        | Kiểu Dữ Liệu | Mô Tả                                  |
| :------------------ | :----------- | :------------------------------------- |
| `sub_organ_code`    | string       | Mã công ty con                         |
| `organ_name`        | string       | Tên công ty con                        |
| `ownership_percent` | float        | Tỷ lệ sở hữu                           |
| `type`              | string       | Loại hình ('công ty con' / 'liên kết') |

### Nguồn KBS

```python
df = company_kbs.subsidiaries()
```

| Cột (Column)        | Kiểu Dữ Liệu | Mô Tả            |
| :------------------ | :----------- | :--------------- |
| `name`              | string       | Tên công ty con  |
| `charter_capital`   | int          | Vốn điều lệ      |
| `ownership_percent` | float        | Tỷ lệ sở hữu (%) |
| `type`              | string       | Loại hình        |

---

## 5. news() - Tin Tức

Hàm `news()` truy xuất tin tức liên quan đến doanh nghiệp, được chuẩn hoá giao diện (Unified Interface) cho tất cả các nguồn hỗ trợ.

> [!TIP] 
> **Phân biệt `vnstock_data` và `vnstock_news`:**
> - Hàm `news()` trong `vnstock_data` tập trung vào tin tức **đã được phân loại** cho một doanh nghiệp cụ thể (Bao gồm: thông báo nội bộ, công bố thông tin, tin từ sở giao dịch, tin tức trực tiếp về mã cổ phiếu).
> - Gói `vnstock_news` chuyên dùng để cào **tin tức đại chúng chưa dán nhãn** trực tiếp từ các trang báo (thích hợp làm nguyên liệu thô cho mô hình ML/AI hoặc sử dụng AI Agent để gán nhãn).

**Các nguồn hỗ trợ:** `vci`, `kbs`, `cafef`

```python
df = company_vci.news(length=90, mode='list')
# Truy xuất chi tiết bài báo
df_detail = company_vci.news(length=10, mode='detail', limit=50)
```

**Tham số hỗ trợ:**
- `start` (str, optional): Ngày bắt đầu lấy dữ liệu (định dạng `YYYY-MM-DD`).
- `end` (str, optional): Ngày kết thúc lấy dữ liệu (định dạng `YYYY-MM-DD`).
- `length` (int, default=90): Khoảng thời gian (số ngày) lùi lại từ ngày `end` (nếu `start` không được cung cấp).
- `limit` (int, default=10000): Số lượng tin tức tối đa được trả về.
- `mode` (str, default='list'): 
  - `'list'`: Lấy danh sách tin tức (thường không bao gồm nội dung chi tiết).
  - `'detail'`: Lấy chi tiết toàn bộ nội dung từng bài báo.
- `show_log` (bool, default=False): Bật/tắt log debug.
- `**kwargs`: Các tham số tuỳ chỉnh bổ sung (sẽ được truyền trực tiếp xuống nguồn dữ liệu nếu nguồn đó có hỗ trợ).

**Cấu trúc dữ liệu trả về (áp dụng chung cho mọi nguồn):**

| Cột (Column)   | Kiểu Dữ Liệu | Mô Tả |
| :------------- | :----------- | :---- |
| `id`           | string       | Mã định danh duy nhất của bài báo |
| `symbol`       | string       | Mã chứng khoán tương ứng |
| `title`        | string       | Tiêu đề bài báo |
| `summary`      | string       | Tóm tắt nội dung bài báo |
| `content`      | string       | Nội dung chi tiết (HTML hoặc Text tuỳ nguồn, chỉ có khi `mode='detail'`) |
| `publish_time` | string       | Thời gian đăng tải (chuẩn hoá ISO 8601, VD: `2026-06-22T13:38:00.000`) |
| `source`       | string       | Nguồn cung cấp bài báo (VD: `CafeF`, `VCI`, `KBS`) |
| `url`          | string       | Đường dẫn gốc để đọc bài báo |
| `category`     | string       | Chuyên mục của bài báo (nếu có) |
| `image_url`    | string       | Đường dẫn ảnh minh hoạ |

---

## 6. events() - Sự Kiện Quyền

### Nguồn VCI (Khuyên dùng)

VCI cung cấp dữ liệu sự kiện chi tiết.

```python
df = company_vci.events()
```

| Cột (Column)      | Kiểu Dữ Liệu | Mô Tả                            |
| :---------------- | :----------- | :------------------------------- |
| `event_title`     | string       | Tên sự kiện                      |
| `public_date`     | string       | Ngày công bố                     |
| `exright_date`    | string       | Ngày giao dịch không hưởng quyền |
| `record_date`     | string       | Ngày đăng ký cuối cùng           |
| `value`           | int          | Giá trị (cổ tức tiền mặt, v.v.)  |
| `ratio`           | float        | Tỷ lệ thực hiện                  |
| `event_list_name` | string       | Loại sự kiện                     |

### Nguồn KBS

> ⚠️ Hiện tại chưa ghi nhận dữ liệu sự kiện từ API KBS cho các mã VN30 phổ biến. API có thể trả về DataFrame rỗng.

---

## 7. capital_history() - Lịch Sử Tăng Vốn (Chỉ KBS)

Chỉ hỗ trợ trên nguồn **KBS**.

```python
df = company_kbs.capital_history()
```

| Cột (Column)      | Kiểu Dữ Liệu | Mô Tả                    |
| :---------------- | :----------- | :----------------------- |
| `date`            | datetime     | Ngày thay đổi            |
| `charter_capital` | int          | Vốn điều lệ sau thay đổi |
| `currency`        | string       | Đơn vị tiền tệ           |

---

## 8. insider_trading() - Giao Dịch Nội Bộ (Chỉ KBS)

Chỉ hỗ trợ trên nguồn **KBS**.

> ⚠️ Hiện tại chưa ghi nhận dữ liệu từ API KBS cho các mã VN30 phổ biến.

---

## 9. ratio_summary() - Chỉ Số Tài Chính (Chỉ VCI)

Chỉ hỗ trợ trên nguồn **VCI**. Cung cấp ảnh chụp nhanh các chỉ số quan trọng.

```python
df = company_vci.ratio_summary()
```

| Cột (Column)        | Kiểu Dữ Liệu | Mô Tả                                                                |
| :------------------ | :----------- | :------------------------------------------------------------------- |
| `pe`                | float        | P/E                                                                  |
| `pb`                | float        | P/B                                                                  |
| `roe`               | float        | ROE                                                                  |
| `roa`               | float        | ROA                                                                  |
| `eps`               | float        | EPS cơ bản                                                           |
| `revenue_growth`    | float        | Tăng trưởng doanh thu                                                |
| `net_profit_growth` | float        | Tăng trưởng lợi nhuận                                                |
| `dividend`          | int          | Cổ tức tiền mặt gần nhất                                             |
| `net_profit_margin` | float        | Biên lợi nhuận ròng                                                  |
| `debt_equity`       | float        | Tỷ số Nợ/Vốn chủ sở hữu (vắng mặt trong một số trường hợp, xem `de`) |

---

## 10. trading_stats() - Thống Kê Giao Dịch (Chỉ VCI)

Chỉ hỗ trợ trên nguồn **VCI**.

```python
df = company_vci.trading_stats()
```

| Cột (Column)            | Kiểu Dữ Liệu | Mô Tả                   |
| :---------------------- | :----------- | :---------------------- |
| `open`                  | int          | Giá mở cửa              |
| `high`                  | int          | Giá cao nhất            |
| `low`                   | int          | Giá thấp nhất           |
| `close_price`           | int          | Giá đóng cửa            |
| `total_volume`          | int          | Tổng khối lượng         |
| `foreign_volume`        | int          | Khối lượng nước ngoài   |
| `foreign_room`          | int          | Room nước ngoài         |
| `current_holding_ratio` | float        | Tỷ lệ sở hữu nước ngoài |
