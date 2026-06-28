# Reference Layer Schema

### `Reference().bond('BAB123032').info()`
| Tên Cột             | Kiểu Dữ Liệu | Ý Nghĩa                                     | Giá Trị Mẫu |
| ------------------- | ------------ | ------------------------------------------- | ----------- |
| **`symbol`**        | `object`     | Mã định danh chứng khoán / tổ chức          | `BAB123032` |
| **`change_1m`**     | `float64`    | Thay đổi giá 1 tháng (%)                    | `0.0`       |
| **`change_1y`**     | `float64`    | Thay đổi giá 1 năm (%)                      | `0.0`       |
| **`current_ratio`** | `float64`    | Tỷ số thanh toán hiện hành                  | `0.07`      |
| **`debt_ratio`**    | `float64`    | Tỷ số nợ (Nợ/Tổng tài sản)                  | `933.43`    |
| **`roe`**           | `float64`    | Tỷ suất lợi nhuận trên vốn chủ sở hữu (ROE) | `14.75`     |
| **`roa`**           | `float64`    | Tỷ suất lợi nhuận trên tổng tài sản (ROA)   | `-116.35`   |
| **`pe`**            | `float64`    | Hệ số P/E                                   | `-0.14`     |
| **`pb`**            | `float64`    | Hệ số P/B                                   | `-0.02`     |
| **`report_period`** | `object`     | Kỳ báo cáo tài chính                        | `12/2024`   |

> [!NOTE]
> Đối với Trái phiếu Chính phủ (Government Bonds, ví dụ: `41BAGC000`), do tính chất không có báo cáo tài chính doanh nghiệp hay các chỉ số kinh doanh, API gốc của KBS chỉ trả về 3 trường dữ liệu. Vì vậy kết quả DataFrame trả về sẽ chỉ gồm 3 cột: `symbol`, `change_1m` và `change_1y`.



### `Reference().bond().list()`
| Tên Cột      | Kiểu Dữ Liệu | Ý Nghĩa                                                                                   | Giá Trị Mẫu |
| ------------ | ------------ | ----------------------------------------------------------------------------------------- | ----------- |
| **`symbol`** | `object`     | Mã định danh chứng khoán / tổ chức                                                        | `BAB123032` |
| **`type`**   | `object`     | Loại hình: `corporate` cho trái phiếu doanh nghiệp, `government` cho trái phiếu chính phủ | `corporate` |

### `Reference().company('FPT').events()`
| Tên Cột               | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu                                         |
| --------------------- | ------------ | ---------------------------------- | --------------------------------------------------- |
| **`id`**              | `object`     | Mã ID hệ thống                     | `6a0fa234a6ca51ba73a2a0a0`                          |
| **`event_name_vi`**   | `object`     | Tên sự kiện (Tiếng Việt)           | `Trả cổ tức bằng tiền mặt`                          |
| **`event_name_en`**   | `object`     | Tên sự kiện (Tiếng Anh)            | `Cash Dividend`                                     |
| **`ticker`**          | `object`     | Mã định danh chứng khoán / tổ chức | `FPT`                                               |
| **`event_code`**      | `object`     | Mã sự kiện                         | `DIV`                                               |
| **`event_title_vi`**  | `object`     | Tiêu đề sự kiện (Tiếng Việt)       | `Trả cổ tức bằng tiền mặt - Đợt 2 2025 - 1,000 VND` |
| **`event_title_en`**  | `object`     | Tiêu đề sự kiện (Tiếng Anh)        | `Cash Dividend - Interim 2 2025 - 1,000 VND`        |
| **`display_date1`**   | `object`     | Thời gian / Ngày tháng             | `2026-05-28T00:00:00`                               |
| **`display_date2`**   | `object`     | Thời gian / Ngày tháng             | `2026-05-22T00:00:00`                               |
| **`public_date`**     | `object`     | Public Ngày                        | `2026-05-22`                                        |
| **`record_date`**     | `object`     | Record Ngày                        | `2026-05-29`                                        |
| **`exright_date`**    | `object`     | Exright Ngày                       | `2026-05-28`                                        |
| **`payout_date`**     | `object`     | Payout Ngày                        | `2026-06-10T00:00:00`                               |
| **`value_per_share`** | `float64`    | Giá trị trên mỗi cổ phần           | `1000.0`                                            |
| **`exercise_ratio`**  | `float64`    | Tỷ lệ                              | `0.1`                                               |
| **`category`**        | `object`     | Phân loại                          | `DIVIDEND`                                          |
| **`start_date`**      | `object`     | Start Ngày                         | `None`                                              |
| **`end_date`**        | `object`     | End Ngày                           | `None`                                              |
| **`action_type_vi`**  | `object`     | Loại hành động (Tiếng Việt)        | `None`                                              |
| **`action_type_en`**  | `object`     | Loại hành động (Tiếng Anh)         | `None`                                              |
| **`issue_date`**      | `object`     | Ngày phát hành                     | `None`                                              |
| **`listing_date`**    | `object`     | Listing Ngày                       | `None`                                              |

### `Reference().company('FPT').info()`
| Tên Cột            | Kiểu Dữ Liệu | Ý Nghĩa                                | Giá Trị Mẫu                                          |
| ------------------ | ------------ | -------------------------------------- | ---------------------------------------------------- |
| **`symbol`**       | `object`     | Mã định danh chứng khoán / tổ chức     | `FPT`                                                |
| **`name`**         | `object`     | Tên đầy đủ của tổ chức / công ty / quỹ | `Công ty Cổ phần FPT`                                |
| **`sector`**       | `object`     | Ngành nghề                             | `Technology`                                         |
| **`profile`**      | `object`     | Hồ sơ công ty / Mô tả hoạt động        | `Công ty Cổ phần FPT (FPT) có tiền thân là Công ...` |
| **`listing_date`** | `object`     | Listing Ngày                           | `2006-12-13T00:00:00`                                |
| **`issued_share`** | `float64`    | Khối lượng cổ phiếu lưu hành           | `1703507121.0`                                       |

### `Reference().company('FPT').news()`
| Tên Cột            | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu                                         |
| ------------------ | ------------ | ---------------------------------- | --------------------------------------------------- |
| **`id`**           | `object`     | Mã ID hệ thống                     | `6a309785e56b40f0536c38cd`                          |
| **`symbol`**       | `object`     | Mã định danh chứng khoán / tổ chức | `FPT`                                               |
| **`title`**        | `object`     | Tiêu đề tin tức                    | `FPT: Thông báo giao dịch cổ phiếu ESOP...`         |
| **`summary`**      | `object`     | Nội dung tóm tắt                   | `None`                                              |
| **`content`**      | `object`     | Nội dung đầy đủ                    | `None`                                              |
| **`publish_time`** | `object`     | Thời gian công bố                  | `2026-06-15T08:58:00`                               |
| **`source`**       | `object`     | Nguồn tin                          | `None`                                              |
| **`url`**          | `object`     | Đường dẫn nguồn gốc                | `None`                                              |
| **`category`**     | `object`     | Phân loại chuyên mục tin tức       | `None`                                              |
| **`image_url`**    | `object`     | Đường dẫn ảnh tin tức              | `https://cdn.example.com/medialib/145689/I/2024...` |

### `Reference().company('FPT').officers()`
| Tên Cột            | Kiểu Dữ Liệu | Ý Nghĩa                                | Giá Trị Mẫu                  |
| ------------------ | ------------ | -------------------------------------- | ---------------------------- |
| **`index`**        | `int64`      | Mã chỉ số                              | `0`                          |
| **`symbol`**       | `object`     | Mã định danh chứng khoán / tổ chức     | `FPT`                        |
| **`name`**         | `object`     | Tên đầy đủ của tổ chức / công ty / quỹ | `Trương Gia Bình`            |
| **`position`**     | `object`     | Chức vụ                                | `Chủ tịch Hội đồng Quản trị` |
| **`total_shares`** | `int64`      | Tổng số cổ phần nắm giữ                | `117347966`                  |
| **`rate`**         | `float64`    | Tỷ lệ sở hữu                           | `0.0689`                     |

### `Reference().company('FPT').shareholders()`
| Tên Cột                | Kiểu Dữ Liệu | Ý Nghĩa                                | Giá Trị Mẫu               |
| ---------------------- | ------------ | -------------------------------------- | ------------------------- |
| **`symbol`**           | `object`     | Mã định danh chứng khoán / tổ chức     | `FPT`                     |
| **`name`**             | `object`     | Tên đầy đủ của tổ chức / công ty / quỹ | `Trương Gia Bình`         |
| **`shareholder_type`** | `object`     | Loại cổ đông (Cá nhân/Tổ chức)         | `Individual`              |
| **`total_shares`**     | `int64`      | Tổng số cổ phần nắm giữ                | `117347966`               |
| **`rate`**             | `float64`    | Tỷ lệ sở hữu                           | `0.0689`                  |
| **`date`**             | `object`     | Ngày giao dịch / Dấu thời gian         | `2026-02-03T10:36:48.587` |

### `Reference().company('FPT').subsidiaries()`
| Tên Cột          | Kiểu Dữ Liệu | Ý Nghĩa                                | Giá Trị Mẫu           |
| ---------------- | ------------ | -------------------------------------- | --------------------- |
| **`symbol`**     | `object`     | Mã định danh chứng khoán / tổ chức     | `FPT`                 |
| **`name`**       | `object`     | Tên đầy đủ của tổ chức / công ty / quỹ | `Công ty TNHH FPT IS` |
| **`rate`**       | `float64`    | Tỷ lệ sở hữu                           | `1.0`                 |
| **`sub_symbol`** | `object`     | Mã công ty con                         | `FISC`                |

### `Reference().equity.by_exchange()`
| Tên Cột                | Kiểu Dữ Liệu | Ý Nghĩa                             | Giá Trị Mẫu                                          |
| ---------------------- | ------------ | ----------------------------------- | ---------------------------------------------------- |
| **`symbol`**           | `object`     | Mã định danh chứng khoán / tổ chức  | `YTC`                                                |
| **`exchange`**         | `object`     | Sàn giao dịch (HOSE, HNX, UPCOM)    | `UPCOM`                                              |
| **`type`**             | `object`     | Loại hình (Ví dụ: corporate, STOCK) | `STOCK`                                              |
| **`sid`**              | `float64`    | Mã định danh hệ thống (SID)         | `3346.0`                                             |
| **`organ_short_name`** | `object`     | Tên viết tắt của tổ chức            | `XNK Y tế TP.HCM`                                    |
| **`organ_name`**       | `object`     | Tên tổ chức                         | `Công ty Cổ phần Xuất nhập khẩu Y tế Thành phố H...` |
| **`product_grp_id`**   | `object`     | Mã nhóm sản phẩm                    | `UPX`                                                |
| **`icb_code2`**        | `object`     | Mã phân ngành ICB cấp 2             | `4500`                                               |

### `Reference().equity.by_group('VN30')`
| Tên Cột      | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu |
| ------------ | ------------ | ---------------------------------- | ----------- |
| **`symbol`** | `object`     | Mã định danh chứng khoán / tổ chức | `ACB`       |

### `Reference().equity.list()`
| Tên Cột        | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu                                          |
| -------------- | ------------ | ---------------------------------- | ---------------------------------------------------- |
| **`symbol`**   | `object`     | Mã định danh chứng khoán / tổ chức | `YTC`                                                |
| **`org_name`** | `object`     | Tên tổ chức                        | `Công ty Cổ phần Xuất nhập khẩu Y tế Thành phố H...` |

### `Reference().equity.list_by_exchange()`
| Tên Cột                | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu                                          |
| ---------------------- | ------------ | ---------------------------------- | ---------------------------------------------------- |
| **`symbol`**           | `object`     | Mã định danh chứng khoán / tổ chức | `YTC`                                                |
| **`exchange`**         | `object`     | Sàn giao dịch (HOSE, HNX, UPCOM)   | `UPCOM`                                              |
| **`organ_name`**       | `object`     | Tên tổ chức                        | `Công ty Cổ phần Xuất nhập khẩu Y tế Thành phố H...` |
| **`organ_short_name`** | `object`     | Tên viết tắt của tổ chức           | `XNK Y tế TP.HCM`                                    |
| **`icb_code_lv2`**     | `object`     | Mã phân ngành ICB cấp 2            | `4500`                                               |


### `Reference().equity.list_by_group('VN30')`
| Tên Cột      | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu |
| ------------ | ------------ | ---------------------------------- | ----------- |
| **`symbol`** | `object`     | Mã định danh chứng khoán / tổ chức | `ACB`       |

### `Reference().equity.list_by_industry('8773')`
| Tên Cột             | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu                                   |
| ------------------- | ------------ | ---------------------------------- | --------------------------------------------- |
| **`symbol`**        | `object`     | Mã định danh chứng khoán / tổ chức | `EVF`                                         |
| **`organ_name`**    | `object`     | Tên tổ chức                        | `Công ty Tài chính Tổng hợp Cổ phần Điện Lực` |
| **`com_type_code`** | `object`     | Loại hình công ty                  | `NH`                                          |
| **`icb_level`**     | `int64`      | Cấp độ ngành ICB                   | `4`                                           |
| **`icb_code`**      | `object`     | Mã chuẩn phân ngành ICB            | `8773`                                        |
| **`icb_name`**      | `object`     | Tên ngành ICB                      | `Tài chính cá nhân`                           |

### `Reference().etf.list()`
| Tên Cột      | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu |
| ------------ | ------------ | ---------------------------------- | ----------- |
| **`symbol`** | `object`     | Mã định danh chứng khoán / tổ chức | `E1VFVN30`  |

### `Reference().events.calendar()`
| Tên Cột             | Kiểu Dữ Liệu     | Ý Nghĩa                            | Giá Trị Mẫu                                          |
| ------------------- | ---------------- | ---------------------------------- | ---------------------------------------------------- |
| **`symbol`**        | `object`         | Mã định danh chứng khoán / tổ chức | `DXL`                                                |
| **`event_name`**    | `object`         | Tên sự kiện                        | `Đại hội Đồng Cổ đông`                               |
| **`event_title`**   | `object`         | Tiêu đề sự kiện                    | `DXL - Tổ chức ĐHĐCĐ thường niên 2026`               |
| **`ex_right_date`** | `datetime64[ns]` | Ex Right Ngày                      | `2026-04-21T00:00:00.000`                            |
| **`record_date`**   | `datetime64[ns]` | Record Ngày                        | `2026-04-22T00:00:00.000`                            |
| **`organ_name`**    | `object`         | Tên tổ chức                        | `Công ty Cổ phần Du lịch và Xuất nhập khẩu Lạng Sơn` |
| **`public_date`**   | `datetime64[ns]` | Public Ngày                        | `2026-04-02T00:00:00.000`                            |
| **`issue_date`**    | `datetime64[ns]` | Ngày phát hành                     | `2026-06-14T00:00:00.000`                            |
| **`event_type`**    | `object`         | Loại sự kiện                       | `AGME`                                               |

### `Reference().events.market()`
| Tên Cột          | Kiểu Dữ Liệu     | Ý Nghĩa                        | Giá Trị Mẫu               |
| ---------------- | ---------------- | ------------------------------ | ------------------------- |
| **`date`**       | `datetime64[ns]` | Ngày giao dịch / Dấu thời gian | `2000-01-01T00:00:00.000` |
| **`event_name`** | `object`         | Tên sự kiện                    | `Tết Dương Lịch`          |
| **`event_type`** | `object`         | Loại sự kiện                   | `Holiday`                 |
| **`duration`**   | `object`         | Thời lượng / Kỳ hạn            | `None`                    |

### `Reference().fund.list()`
| Tên Cột                | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu                                          |
| ---------------------- | ------------ | ---------------------------------- | ---------------------------------------------------- |
| **`ticker`**           | `object`     | Mã định danh chứng khoán / tổ chức | `DCDS`                                               |
| **`organ_name`**       | `object`     | Tên tổ chức                        | `QUỸ ĐẦU TƯ CHỨNG KHOÁN NĂNG ĐỘNG DC`                |
| **`organ_short_name`** | `object`     | Tên viết tắt của tổ chức           | `CÔNG TY CỔ PHẦN QUẢN LÝ QUỸ DRAGON CAPITAL VIỆT...` |
| **`fund_type`**        | `object`     | Loại quỹ (ETF, Mở, Đóng...)        | `equity_fund`                                        |
| **`management_fee`**   | `float64`    | Phí quản lý (%)                    | `1.95`                                               |
| **`inception_date`**   | `object`     | Ngày thành lập                     | `2004-05-19`                                         |
| **`nav`**              | `float64`    | Giá trị tài sản ròng               | `98464.3`                                            |
| **`nav_update_at`**    | `object`     | Thời gian / Ngày tháng             | `2026-06-13`                                         |

### `Reference().futures('VN30F1M').info()`
| Tên Cột                   | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu                 |
| ------------------------- | ------------ | ---------------------------------- | --------------------------- |
| **`symbol`**              | `object`     | Mã định danh chứng khoán / tổ chức | `41I1G6000`                 |
| **`full_name`**           | `object`     | Tên đầy đủ                         | `VN30 Index Futures 062026` |
| **`underlying_symbol`**   | `object`     | Mã chứng khoán cơ sở               | `VN30`                      |
| **`exchange`**            | `object`     | Sàn giao dịch (HOSE, HNX, UPCOM)   | `HNX`                       |
| **`first_trading_date`**  | `object`     | First Trading Ngày                 | `17/10/2025`                |
| **`last_trading_date`**   | `object`     | Last Trading Ngày                  | `18/06/2026`                |
| **`reference_price`**     | `float64`    | Giá tham chiếu                     | `1952.8`                    |
| **`ceiling_price`**       | `float64`    | Giá trần                           | `2089.4`                    |
| **`floor_price`**         | `float64`    | Giá sàn                            | `1816.2`                    |
| **`open_price`**          | `int64`      | Giá mở cửa                         | `1968`                      |
| **`high_price`**          | `float64`    | Giá cao nhất                       | `1974.7`                    |
| **`low_price`**           | `int64`      | Giá thấp nhất                      | `1935`                      |
| **`close_price`**         | `int64`      | Giá đóng cửa                       | `1939`                      |
| **`open_interest`**       | `object`     | Hợp đồng mở (OI)                   | `36798`                     |
| **`basis`**               | `object`     | Độ lệch (Basis)                    | `-5.36`                     |
| **`foreign_buy_volume`**  | `int64`      | Khối lượng khối ngoại mua          | `9495`                      |
| **`foreign_sell_volume`** | `int64`      | Khối lượng khối ngoại bán          | `0`                         |

### `Reference().futures().list()`
| Tên Cột      | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu |
| ------------ | ------------ | ---------------------------------- | ----------- |
| **`symbol`** | `object`     | Mã định danh chứng khoán / tổ chức | `41I1G6000` |

### `Reference().index.groups()`
| Tên Cột           | Kiểu Dữ Liệu | Ý Nghĩa       | Giá Trị Mẫu                                         |
| ----------------- | ------------ | ------------- | --------------------------------------------------- |
| **`group_name`**  | `object`     | Tên nhóm      | `BOND`                                              |
| **`group_code`**  | `object`     | Mã nhóm       | `BOND`                                              |
| **`category`**    | `object`     | Phân loại     | `Trái phiếu`                                        |
| **`description`** | `object`     | Mô tả tóm tắt | `Corporate Bond - Trái phiếu doanh nghiệp niêm yết` |

### `Reference().index.list()`
| Tên Cột           | Kiểu Dữ Liệu | Ý Nghĩa                                | Giá Trị Mẫu                                          |
| ----------------- | ------------ | -------------------------------------- | ---------------------------------------------------- |
| **`symbol`**      | `object`     | Mã định danh chứng khoán / tổ chức     | `VN30`                                               |
| **`name`**        | `object`     | Tên đầy đủ của tổ chức / công ty / quỹ | `VN30`                                               |
| **`description`** | `object`     | Mô tả tóm tắt                          | `30 cổ phiếu vốn hóa lớn nhất & thanh khoản tốt ...` |
| **`full_name`**   | `object`     | Tên đầy đủ                             | `VN30 Index`                                         |
| **`group`**       | `object`     | Nhóm chỉ số / Nhóm ngành               | `HOSE Indices`                                       |
| **`index_id`**    | `float64`    | Mã ID chỉ số                           | `5.0`                                                |
| **`sector_id`**   | `float64`    | Mã ID ngành                            | `None`                                               |

### `Reference().index.members('VN30')`
| Tên Cột      | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu |
| ------------ | ------------ | ---------------------------------- | ----------- |
| **`symbol`** | `object`     | Mã định danh chứng khoán / tổ chức | `ACB`       |

### `Reference().industry.list()`
| Tên Cột         | Kiểu Dữ Liệu | Ý Nghĩa                 | Giá Trị Mẫu |
| --------------- | ------------ | ----------------------- | ----------- |
| **`icb_code`**  | `object`     | Mã chuẩn phân ngành ICB | `0001`      |
| **`icb_name`**  | `object`     | Tên ngành ICB           | `Dầu khí`   |
| **`icb_level`** | `int64`      | Cấp độ ngành ICB        | `1`         |

### `Reference().industry.sectors()`
| Tên Cột             | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu          |
| ------------------- | ------------ | ---------------------------------- | -------------------- |
| **`symbol`**        | `object`     | Mã định danh chứng khoán / tổ chức | `A32`                |
| **`organ_name`**    | `object`     | Tên tổ chức                        | `Công ty Cổ phần 32` |
| **`com_type_code`** | `object`     | Loại hình công ty                  | `CT`                 |
| **`icb_level`**     | `int64`      | Cấp độ ngành ICB                   | `1`                  |
| **`icb_code`**      | `object`     | Mã chuẩn phân ngành ICB            | `3000`               |
| **`icb_name`**      | `object`     | Tên ngành ICB                      | `Hàng Tiêu dùng`     |

### `Reference().market.status()`
| Tên Cột                 | Kiểu Dữ Liệu     | Ý Nghĩa                          | Giá Trị Mẫu               |
| ----------------------- | ---------------- | -------------------------------- | ------------------------- |
| **`exchange`**          | `object`         | Sàn giao dịch (HOSE, HNX, UPCOM) | `UPCOM`                   |
| **`asset_type`**        | `object`         | Loại tài sản (Ví dụ: EQUITY)     | `EQUITY`                  |
| **`status`**            | `object`         | Trạng thái (Ví dụ: CLOSED, OPEN) | `CLOSED`                  |
| **`timestamp`**         | `datetime64[ns]` | Dấu thời gian                    | `2026-06-14T05:05:26.024` |
| **`last_trading_date`** | `datetime64[ns]` | Last Trading Ngày                | `2026-06-12T12:00:02.739` |

### `Reference().search.info('EURUSD')`
| Tên Cột           | Kiểu Dữ Liệu | Ý Nghĩa                                | Giá Trị Mẫu         |
| ----------------- | ------------ | -------------------------------------- | ------------------- |
| **`symbol`**      | `object`     | Mã định danh chứng khoán / tổ chức     | `EURUSD`            |
| **`name`**        | `object`     | Tên đầy đủ của tổ chức / công ty / quỹ | `EUR/USD`           |
| **`exchange`**    | `object`     | Sàn giao dịch (HOSE, HNX, UPCOM)       | `FX`                |
| **`description`** | `object`     | Mô tả tóm tắt                          | `Euro vs US Dollar` |
| **`name_local`**  | `object`     | Tên địa phương (Tiếng Việt)            | `DE`                |
| **`symbol_id`**   | `object`     | Mã ID hệ thống                         | `EUR-USD`           |

### `Reference().search.symbol('EURUSD')`
| Tên Cột           | Kiểu Dữ Liệu | Ý Nghĩa                                | Giá Trị Mẫu         |
| ----------------- | ------------ | -------------------------------------- | ------------------- |
| **`symbol`**      | `object`     | Mã định danh chứng khoán / tổ chức     | `EURUSD`            |
| **`name`**        | `object`     | Tên đầy đủ của tổ chức / công ty / quỹ | `EUR/USD`           |
| **`description`** | `object`     | Mô tả tóm tắt                          | `Euro vs US Dollar` |

### `Reference().warrant('CHPG2322').info()`
| Tên Cột      | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu |
| ------------ | ------------ | ---------------------------------- | ----------- |
| **`symbol`** | `object`     | Mã định danh chứng khoán / tổ chức | `CHPG2322`  |

### `Reference().warrant().list()`
| Tên Cột      | Kiểu Dữ Liệu | Ý Nghĩa                            | Giá Trị Mẫu |
| ------------ | ------------ | ---------------------------------- | ----------- |
| **`symbol`** | `object`     | Mã định danh chứng khoán / tổ chức | `CACB2510`  |

