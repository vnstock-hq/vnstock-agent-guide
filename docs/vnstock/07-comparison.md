---
title: "05. So sánh Miễn phí vs Tài trợ"
nav_order: 6
parent: "Giao diện Hợp nhất (Unified UI)"
---

# Đối chiếu 1:1 Toàn diện: Vnstock (Free) vs Vnstock Data (Sponsor)

Tài liệu này cung cấp cái nhìn chi tiết và khách quan nhất về sự khác biệt giữa phiên bản cộng đồng (`vnstock`) và phiên bản tài trợ (`vnstock_data`) thông qua giao diện **Unified UI**. Chúng tôi sử dụng `vnstock_data` làm chuẩn tham chiếu cao nhất để chỉ ra những thiếu hụt hoặc giới hạn của bản miễn phí.

---

## 1. Giới hạn truy xuất & Xử lý lỗi (Rate Limit)

Việc sử dụng các hạng thành viên Tài trợ sẽ giúp bạn mở rộng đáng kể giới hạn truy xuất (Rate Limit).

| Tiêu Chí            | Cộng đồng | Bronze   | Silver    | Golden    | Diamond   |
| ------------------- | --------- | -------- | --------- | --------- | --------- |
| **Hạn mức/Phút**    | 60        | 180      | 300       | 500       | 600       |
| **Hạn mức/Giờ**     | 3.600     | 10.800   | 15.000    | 30.000    | 36.000    |
| **Hạn mức/Ngày**    | 10.000    | 50.000   | 100.000   | 150.000   | 180.000   |
| **Hạn mức/Tháng**   | 100.000   | 600.000  | 1.500.000 | 2.500.000 | 3.500.000 |
| **Thiết bị (Tổng)** | 1         | 3        | 6         | 6         | 13        |
| **Tốc độ tải**      | 1X        | 1X       | 1X        | 5X-8X     | 5X-8X     |
| **Dữ liệu giá**     | Trễ 1-3s  | Trễ 1-3s | Trễ 1-3s  | Real-time | Real-time |
| **Số lượng thư viện**| 1 (Free)  | 1 (Data) | 3         | 4         | 4         |

(*) **Lưu ý quan trọng về Rate Limit:**
- Khi chạm giới hạn API, chương trình sẽ báo lỗi `RateLimitExceeded` và tự động dừng.
- Hạn mức tổng/tháng nhằm hạn chế tác động tiêu cực của việc lạm dụng hệ thống. Khuyến nghị bạn nên lưu trữ (cache) cục bộ đối với dữ liệu tần suất thấp.
- Số lượng thiết bị là tổng số máy (Mac, Windows, Linux) được phép dùng chung tài khoản (Tuỳ hạng thành viên). Riêng bản phân phối Linux cho server (hạng thành viên Diamond) cho phép thay đổi phần cứng 20 lần/ngày.

### Xử lý lỗi Rate Limit trong code

Khi vượt quá giới hạn, thư viện sẽ tự động sinh lỗi `RateLimitExceeded`. AI Agents cần chú ý bắt lỗi này để tránh treo chương trình và thông báo cho người dùng về việc đạt tới giới hạn.

```python
from vnstock.core.quota import RateLimitExceeded
from vnstock_data import Market

try:
    mkt = Market()
    df = mkt.equity("VCB").ohlcv(start="2024-01-01", end="2024-12-31")
except RateLimitExceeded as e:
    print(f"Đã đạt giới hạn truy xuất API: {e}") 
    # AI nên hướng dẫn người dùng kiểm tra lại hạng thành viên tài khoản hoặc áp dụng cơ chế cache
```

---

## 2. So sánh Cấu trúc Domain & Lớp (Class-by-Class)

Hệ thống Unified UI được thiết kế đồng bộ, nhưng bản Tài trợ mở rộng thêm nhiều Domain và Class chuyên sâu để phục vụ phân tích chuyên nghiệp.

| Domain          | Lớp (Class) | Vnstock (Miễn phí) | Vnstock Data (Sponsor) | Thiếu ở bản miễn phí                                                                                                                                                                                                             |
| :-------------- | :---------- | :----------------- | :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Reference**   | `company`   | 9 methods (KBS)    | 7 methods (VCI/KBS)    |                                                                                                                                                                                                                                  |
|                 | `equity`    | Cơ bản             | Đầy đủ                 | Nguồn dữ liệu phân tích chuyên sâu                                                                                                                                                                                               |
|                 | `index`     | Cơ bản             | Đầy đủ                 | Truy cập đầy đủ bộ chỉ số ngành, chỉ số đầu tư HOSE, HNX, UPCOM trong bản sponsor                                                                                                                                                |
|                 | `events`    | Cơ bản             | Chuyên sâu             | Thiếu `market` events toàn thị trường                                                                                                                                                                                            |
|                 | `search`    | MSN (Cơ bản)       | Dukascopy              | Nguồn Dukascopy hoạt động ổn định, ít gián đoạn bất ngờ như MSN                                                                                                                                                                  |
|                 | `bond`      | list (Cơ bản)      | list (Chuyên sâu)      | Thiếu phân loại trái phiếu chính phủ/doanh nghiệp chi tiết                                                                                                                                                                       |
| **Market**      | `equity`    | 3 methods          | **12 methods**         | **Thiếu**: `block_trades`, `foreign_flow`, `odd_lot`, `proprietary_flow`, `volume_profile`, `session_stats`, `order_book`... phục vụ phân tích chuyên sâu                                                                        |
|                 | `index`     | ohlcv              | 5 methods              | **Thiếu**: `quote`, `session_stats`, `trade_history`                                                                                                                                                                             |
|                 | `crypto`    | ohlcv (MSN)        | **11 methods**         | **Thiếu**: `daily_stats`, `order_book`, `vwap`, `rolling_stats`, `trade_history` sử dụng nguồn dữ liệu từ API chính thức của Binane với độ chi tiết cao thay vì dữ liệu miễn phí từ MSN thể hiện thông tin cơ bản, thiếu ổn định |
|                 | `commodity` | ohlcv (MSN)        | 3 methods              | **Thiếu**: `quote`, `summary`. Nguồn Dukascopy cho tải dữ liệu lịch sử chi tiết đến cấp độ phút, ổn định                                                                                                                         |
|                 | `fund`      | history, nav...    | Đầy đủ                 | Giới hạn API, thời gian thực hiện phân tích chậm hơn dùng bản Sponsor                                                                                                                                                            |
| **Fundamental** | `equity`    | 4 methods          | **6 methods**          | **Thiếu**: `financial_health` (Scorecard TCBS), `note` (Thuyết minh BCTC)                                                                                                                                                        |
| **Analytics**   | `valuation` | **Không hỗ trợ**   | Đầy đủ                 | Dữ liệu chỉ có ở bản Sponsor cho định giá P/E, P/B toàn thị trường                                                                                                                                                               |
| **Macro**       | `commodity` | **Không hỗ trợ**   | 11 methods             | Dữ liệu chỉ có ở bản Sponsor: Giá cao su, ngô, dầu, lợn, thép... toàn cầu & VN                                                                                                                                                   |
|                 | `currency`  | **Không hỗ trợ**   | 2 methods              | Dữ liệu chỉ có ở bản Sponsor: Tỷ giá & Lãi suất liên ngân hàng (MBK)                                                                                                                                                             |
|                 | `economy`   | **Không hỗ trợ**   | 8 methods              | Dữ liệu chỉ có ở bản Sponsor: GDP, CPI, FDI, Xuất nhập khẩu, Lao động...                                                                                                                                                         |
| **Insights**    | `ranking`   | **Không hỗ trợ**   | 7 methods              | Dữ liệu chỉ có ở bản Sponsor: Xếp hạng tăng/giảm, khối ngoại, giá trị...                                                                                                                                                         |
|                 | `screener`  | **Không hỗ trợ**   | Đầy đủ                 | Dữ liệu chỉ có ở bản Sponsor: Bộ lọc cổ phiếu toàn thị trường (VCI Engine)                                                                                                                                                       |

---

## 3. So sánh Nguồn Dữ liệu (Data Source Matrix)

Bản Tài trợ tích hợp các nguồn dữ liệu trực tiếp từ các tổ chức lớn, đảm bảo tính chính xác và tốc độ vượt trội so với các nguồn crawler của bản miễn phí.

| Nhóm Dữ liệu          | Vnstock (Free)          | Vnstock Data (Sponsor) | Lợi thế bản Sponsor                                                                                                    |
| :-------------------- | :---------------------- | :--------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| **Giá trực tuyến**    | KBS, VCI*               | **MAS**, KBS, VCI, VND | Nhiều nguồn dữ liệu thay thế VCI cho tốc độ cao. *VCI có thể bị chặn trên Google Colab.*                               |
| **Báo cáo tài chính** | VCI, KBS (làm sạch thô) | **MAS, TCBS Standard** | Dữ liệu chuẩn hóa với bộ tiêu chí thường xuyên sử dụng, hạn chế thay đổi cấu trúc do đổi nguồn dữ liệu trong tương lai |
| **Tiền điện tử**      | MSN (Crawler)           | **Binance API**        | Dữ liệu API chính thức từ sàn Binance, ổn định                                                                         |
| **Hàng hóa/Forex**    | MSN (Crawler)           | **Dukascopy, SPL**     | Dữ liệu chuẩn quốc tế từ nguồn dữ liệu uy tín, ổn định                                                                 |
| **Vĩ mô**             | Không có                | **MBK, SPL**           | Cập nhật định kỳ từ các báo cáo chính thống                                                                            |

---

## 4. Khả năng Kỹ thuật & Hiệu suất

| Tiêu chí                   | Vnstock (Miễn phí)                                    | Vnstock Data (Sponsor)                                                                          |
| :------------------------- | :---------------------------------------------------- | :---------------------------------------------------------------------------------------------- |
| **Độ phân giải thời gian** | Ngày (1D), Giờ (1H), Phút (1M)                        | Giây (tick-by-tick), **Phút (1m, 5m, 15m, 1H...), Ngày (1D), Tuần (1W), Tháng (1M)              |
| **Lịch sử dữ liệu**        | Giới hạn (Tùy nguồn)                                  | Dữ liệu lịch sử dài (toàn bộ dải dữ liệu OHLCV, nhiều kỳ báo cáo tài chính (tùy vào từng nguồn) |
| **Rate Limit**             | Rất thấp (Chương trình bị gián đoạn khi gọi liên tục) | Cao (Phù hợp cho chương trình tự động hoặc chạy trên Server)                                    |
| **Hỗ trợ Tick-by-Tick**    | Không hỗ trợ                                          | Hỗ trợ cho mọi mã chứng khoán & chỉ số trong nước                                               |
| **Chuẩn hóa Scorecard**    | Không có                                              | Tự động phân loại bộ chỉ tiêu cốt lõi (~100 chỉ tiêu) tự động theo nhóm ngành                   |

---

## 5. Kết luận: Khi nào nên nâng cấp?

Việc sử dụng `vnstock_data` là cần thiết nếu quy trình công việc của bạn rơi vào các trường hợp sau:

1.  **Algo Trading / Bot**: Cần dữ liệu nến phút (Intraday) và Rate limit cao để không bị ngắt quãng luồng lệnh.
2.  **Phân tích chuyên sâu (Institutional Level)**: Cần sử dụng `financial_health()` để so sánh các doanh nghiệp trên cùng một hệ quy chiếu scorecard chuẩn mực.
3.  **Quản trị danh mục đa tài sản**: Theo dõi đồng thời Cổ phiếu, Crypto, Vĩ mô và Hàng hóa trên cùng một Dashboard Unified UI.
4.  **Sàng lọc cơ hội**: Cần dùng `screener` để tìm ra "siêu cổ phiếu" dựa trên hàng trăm tiêu chí định lượng thay vì lọc thủ công.

> [!TIP]
> Bạn có thể chạy `show_api()` trên cả hai phiên bản để tự mình đối chiếu sự chênh lệch khổng lồ về số lượng hàm (50 vs 150+). Mọi mã nguồn viết trên bản Free đều có thể chuyển đổi sang bản Sponsor chỉ bằng một dòng thay đổi import.