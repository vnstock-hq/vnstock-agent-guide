# Market Layer Schema

### `Market().equity('TCB').foreign_flow()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`time`** | `datetime64[ns]` | Thời gian giao dịch | `2026-06-12T00:00:00.000` |
| **`buy_vol`** | `float64` | Khối lượng mua | `5268002.0` |
| **`buy_val`** | `float64` | Giá trị mua | `164585137600.0` |
| **`sell_vol`** | `float64` | Khối lượng bán | `5121658.0` |
| **`sell_val`** | `float64` | Giá trị bán | `160037861200.0` |
| **`net_vol`** | `float64` | Khối lượng ròng | `146344.0` |
| **`net_val`** | `float64` | Giá trị ròng | `4547276400.0` |

### `Market().equity('TCB').history(length='1Y')`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`time`** | `datetime64[ns]` | Thời gian giao dịch | `2025-06-16T07:00:00.000` |
| **`open`** | `float64` | Giá mở cửa | `29.58` |
| **`high`** | `float64` | Giá cao nhất | `30.87` |
| **`low`** | `float64` | Giá thấp nhất | `29.53` |
| **`close`** | `float64` | Giá đóng cửa | `30.82` |
| **`volume`** | `int64` | Khối lượng giao dịch | `23148300` |

### `Market().equity('TCB').intraday()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`index`** | `int64` | Mã chỉ số | `999` |
| **`time`** | `datetime64[ns]` | Thời gian giao dịch | `2026-06-12T13:06:31.000` |
| **`price`** | `float64` | Giá giao dịch | `31.35` |
| **`volume`** | `int64` | Khối lượng giao dịch | `300` |
| **`match_type`** | `object` | Loại lệnh khớp (Buy/Sell) | `Sell` |
| **`id`** | `object` | Mã ID hệ thống | `2026-06-12_130631_313500_300` |

### `Market().equity('TCB').matched_by_price()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`price`** | `int64` | Giá giao dịch | `31050` |
| **`buy_volume`** | `int64` | Khối lượng mua | `0` |
| **`sell_volume`** | `int64` | Khối lượng bán | `233500` |
| **`unknown_volume`** | `int64` | Khối lượng không xác định | `0` |
| **`total_volume`** | `int64` | Tổng khối lượng | `233500` |

### `Market().equity('TCB').odd_lot()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `TCB` |
| **`exchange`** | `object` | Sàn giao dịch (HOSE, HNX, UPCOM) | `HOSE` |
| **`reference_price`** | `int64` | Giá tham chiếu | `30850` |
| **`ceiling_price`** | `int64` | Giá trần | `33000` |
| **`floor_price`** | `int64` | Giá sàn | `28700` |
| **`open_price`** | `int64` | Giá mở cửa | `31000` |
| **`high_price`** | `int64` | Giá cao nhất | `31550` |
| **`low_price`** | `int64` | Giá thấp nhất | `31000` |
| **`match_price`** | `int64` | Giá khớp lệnh | `31200` |
| **`match_vol`** | `int64` | Khối lượng khớp lệnh | `1` |
| **`total_volume`** | `int64` | Tổng khối lượng | `5765` |
| **`bid_price_1`** | `object` | Giá Mua 1 | `31200.0` |
| **`bid_vol_1`** | `int64` | Khối lượng Mua 1 | `192` |
| **`bid_price_2`** | `int64` | Giá Mua 2 | `31150` |
| **`bid_vol_2`** | `int64` | Khối lượng Mua 2 | `736` |
| **`bid_price_3`** | `int64` | Giá Mua 3 | `31100` |
| **`bid_vol_3`** | `int64` | Khối lượng Mua 3 | `516` |
| **`ask_price_1`** | `object` | Giá Bán 1 | `31250.0` |
| **`ask_vol_1`** | `int64` | Khối lượng Bán 1 | `16` |
| **`ask_price_2`** | `int64` | Giá Bán 2 | `31350` |
| **`ask_vol_2`** | `int64` | Khối lượng Bán 2 | `33` |
| **`ask_price_3`** | `int64` | Giá Bán 3 | `31450` |
| **`ask_vol_3`** | `int64` | Khối lượng Bán 3 | `70` |
| **`foreign_buy_volume`** | `int64` | Khối lượng khối ngoại mua | `5268002` |
| **`foreign_sell_volume`** | `int64` | Khối lượng khối ngoại bán | `0` |

### `Market().equity('TCB').ohlcv(length='1Y')`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`time`** | `datetime64[ns]` | Thời gian giao dịch | `2025-06-16T07:00:00.000` |
| **`open`** | `float64` | Giá mở cửa | `29.58` |
| **`high`** | `float64` | Giá cao nhất | `30.87` |
| **`low`** | `float64` | Giá thấp nhất | `29.53` |
| **`close`** | `float64` | Giá đóng cửa | `30.82` |
| **`volume`** | `int64` | Khối lượng giao dịch | `23148300` |

### `Market().equity('TCB').order_book()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`bid_price_1`** | `object` | Giá Mua 1 | `31200.0` |
| **`bid_vol_1`** | `int64` | Khối lượng Mua 1 | `500` |
| **`bid_price_2`** | `int64` | Giá Mua 2 | `31150` |
| **`bid_vol_2`** | `int64` | Khối lượng Mua 2 | `11800` |
| **`bid_price_3`** | `int64` | Giá Mua 3 | `31100` |
| **`bid_vol_3`** | `int64` | Khối lượng Mua 3 | `300800` |
| **`ask_price_1`** | `object` | Giá Bán 1 | `31250.0` |
| **`ask_vol_1`** | `int64` | Khối lượng Bán 1 | `4200` |
| **`ask_price_2`** | `int64` | Giá Bán 2 | `31300` |
| **`ask_vol_2`** | `int64` | Khối lượng Bán 2 | `135900` |
| **`ask_price_3`** | `int64` | Giá Bán 3 | `31350` |
| **`ask_vol_3`** | `int64` | Khối lượng Bán 3 | `50100` |

### `Market().equity('TCB').price_board()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `TCB` |
| **`exchange`** | `object` | Sàn giao dịch (HOSE, HNX, UPCOM) | `HOSE` |
| **`reference_price`** | `int64` | Giá tham chiếu | `30850` |
| **`ceiling_price`** | `int64` | Giá trần | `33000` |
| **`floor_price`** | `int64` | Giá sàn | `28700` |
| **`open_price`** | `int64` | Giá mở cửa | `31300` |
| **`high_price`** | `int64` | Giá cao nhất | `31450` |
| **`low_price`** | `int64` | Giá thấp nhất | `31050` |
| **`close_price`** | `int64` | Giá đóng cửa | `31250` |
| **`bid_price_1`** | `object` | Giá Mua 1 | `31200.0` |
| **`bid_vol_1`** | `int64` | Khối lượng Mua 1 | `500` |
| **`bid_price_2`** | `int64` | Giá Mua 2 | `31150` |
| **`bid_vol_2`** | `int64` | Khối lượng Mua 2 | `11800` |
| **`bid_price_3`** | `int64` | Giá Mua 3 | `31100` |
| **`bid_vol_3`** | `int64` | Khối lượng Mua 3 | `300800` |
| **`ask_price_1`** | `object` | Giá Bán 1 | `31250.0` |
| **`ask_vol_1`** | `int64` | Khối lượng Bán 1 | `4200` |
| **`ask_price_2`** | `int64` | Giá Bán 2 | `31300` |
| **`ask_vol_2`** | `int64` | Khối lượng Bán 2 | `135900` |
| **`ask_price_3`** | `int64` | Giá Bán 3 | `31350` |
| **`ask_vol_3`** | `int64` | Khối lượng Bán 3 | `50100` |
| **`foreign_buy_volume`** | `int64` | Khối lượng khối ngoại mua | `5268002` |
| **`foreign_sell_volume`** | `int64` | Khối lượng khối ngoại bán | `5121658` |

### `Market().equity('TCB').price_depth()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`bid_price_1`** | `object` | Giá Mua 1 | `31200.0` |
| **`bid_vol_1`** | `int64` | Khối lượng Mua 1 | `500` |
| **`bid_price_2`** | `int64` | Giá Mua 2 | `31150` |
| **`bid_vol_2`** | `int64` | Khối lượng Mua 2 | `11800` |
| **`bid_price_3`** | `int64` | Giá Mua 3 | `31100` |
| **`bid_vol_3`** | `int64` | Khối lượng Mua 3 | `300800` |
| **`ask_price_1`** | `object` | Giá Bán 1 | `31250.0` |
| **`ask_vol_1`** | `int64` | Khối lượng Bán 1 | `4200` |
| **`ask_price_2`** | `int64` | Giá Bán 2 | `31300` |
| **`ask_vol_2`** | `int64` | Khối lượng Bán 2 | `135900` |
| **`ask_price_3`** | `int64` | Giá Bán 3 | `31350` |
| **`ask_vol_3`** | `int64` | Khối lượng Bán 3 | `50100` |

### `Market().equity('TCB').proprietary_flow()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`time`** | `datetime64[ns]` | Thời gian giao dịch | `2026-06-12T00:00:00.000` |
| **`buy_vol`** | `float64` | Khối lượng mua | `1371600.0` |
| **`buy_val`** | `float64` | Giá trị mua | `42915945000.0` |
| **`sell_vol`** | `float64` | Khối lượng bán | `2390500.0` |
| **`sell_val`** | `float64` | Giá trị bán | `74721895000.0` |
| **`net_vol`** | `float64` | Khối lượng ròng | `-1018900.0` |
| **`net_val`** | `float64` | Giá trị ròng | `-31805950000.0` |

### `Market().equity('TCB').quote()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `TCB` |
| **`exchange`** | `object` | Sàn giao dịch (HOSE, HNX, UPCOM) | `HOSE` |
| **`reference_price`** | `int64` | Giá tham chiếu | `30850` |
| **`ceiling_price`** | `int64` | Giá trần | `33000` |
| **`floor_price`** | `int64` | Giá sàn | `28700` |
| **`open_price`** | `int64` | Giá mở cửa | `31300` |
| **`high_price`** | `int64` | Giá cao nhất | `31450` |
| **`low_price`** | `int64` | Giá thấp nhất | `31050` |
| **`close_price`** | `int64` | Giá đóng cửa | `31250` |
| **`bid_price_1`** | `object` | Giá Mua 1 | `31200.0` |
| **`bid_vol_1`** | `int64` | Khối lượng Mua 1 | `500` |
| **`bid_price_2`** | `int64` | Giá Mua 2 | `31150` |
| **`bid_vol_2`** | `int64` | Khối lượng Mua 2 | `11800` |
| **`bid_price_3`** | `int64` | Giá Mua 3 | `31100` |
| **`bid_vol_3`** | `int64` | Khối lượng Mua 3 | `300800` |
| **`ask_price_1`** | `object` | Giá Bán 1 | `31250.0` |
| **`ask_vol_1`** | `int64` | Khối lượng Bán 1 | `4200` |
| **`ask_price_2`** | `int64` | Giá Bán 2 | `31300` |
| **`ask_vol_2`** | `int64` | Khối lượng Bán 2 | `135900` |
| **`ask_price_3`** | `int64` | Giá Bán 3 | `31350` |
| **`ask_vol_3`** | `int64` | Khối lượng Bán 3 | `50100` |
| **`foreign_buy_volume`** | `int64` | Khối lượng khối ngoại mua | `5268002` |
| **`foreign_sell_volume`** | `int64` | Khối lượng khối ngoại bán | `5121658` |

### `Market().equity('TCB').session_stats()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`average_match_volume`** | `float64` | Trung bình KL khớp lệnh | `8863796.895261845` |
| **`average_match_value`** | `float64` | Trung bình GT khớp lệnh | `310968578068.45386` |
| **`average_deal_volume`** | `float64` | Trung bình KL thỏa thuận | `2834322.1596009973` |
| **`average_deal_value`** | `float64` | Trung bình GT thỏa thuận | `87226991919.49677` |
| **`average_volume`** | `float64` | Khối lượng trung bình | `11698119.054862842` |
| **`average_value`** | `float64` | Giá trị trung bình | `398195569987.9506` |
| **`total_match_volume`** | `float64` | Tổng khối lượng khớp lệnh | `17771912775.0` |
| **`total_match_value`** | `float64` | Tổng giá trị khớp lệnh | `623491999027250.0` |
| **`total_deal_volume`** | `float64` | Tổng khối lượng thỏa thuận | `5682815930.0` |
| **`total_deal_value`** | `float64` | Tổng giá trị thỏa thuận | `174890118798591.0` |
| **`total_volume`** | `float64` | Tổng khối lượng | `23454728705.0` |
| **`total_value`** | `float64` | Tổng giá trị | `798382117825841.0` |
| **`fr_buy_volume_total`** | `float64` | Tổng KL khối ngoại mua | `1738063605.0` |
| **`fr_buy_value_total`** | `float64` | Tổng GT khối ngoại mua | `54610779605061.0` |
| **`fr_sell_volume_total`** | `float64` | Tổng KL khối ngoại bán | `1762840358.0` |
| **`fr_sell_value_total`** | `float64` | Tổng GT khối ngoại bán | `55729699300661.0` |
| **`fr_net_volume_total`** | `float64` | KL ròng khối ngoại | `-24776753.0` |
| **`fr_net_value_total`** | `float64` | GT ròng khối ngoại | `-1118919695600.0` |
| **`fr_buy_volume_matched`** | `float64` | KL khớp lệnh khối ngoại mua | `523616350.0` |
| **`fr_buy_value_matched`** | `float64` | GT khớp lệnh khối ngoại mua | `15415173454200.0` |
| **`fr_sell_volume_matched`** | `float64` | KL khớp lệnh khối ngoại bán | `574388489.0` |
| **`fr_sell_value_matched`** | `float64` | GT khớp lệnh khối ngoại bán | `17317785196500.0` |
| **`fr_buy_volume_deal`** | `float64` | KL thỏa thuận khối ngoại mua | `1214447255.0` |
| **`fr_buy_value_deal`** | `float64` | GT thỏa thuận khối ngoại mua | `39195606150861.0` |
| **`fr_sell_volume_deal`** | `float64` | KL thỏa thuận khối ngoại bán | `1188451917.0` |
| **`fr_sell_value_deal`** | `float64` | GT thỏa thuận khối ngoại bán | `38411915482511.0` |
| **`fr_buy_volume_total_avg`** | `float64` | TB tổng KL khối ngoại mua | `866864.6408977556` |
| **`fr_buy_value_total_avg`** | `float64` | TB tổng GT khối ngoại mua | `27237296561.12768` |
| **`fr_sell_volume_total_avg`** | `float64` | TB tổng KL khối ngoại bán | `879222.123690773` |
| **`fr_sell_value_total_avg`** | `float64` | TB tổng GT khối ngoại bán | `27795361247.212467` |
| **`fr_net_volume_total_avg`** | `float64` | Trung bình KL ròng khối ngoại | `-12357.4827930174` |
| **`fr_net_value_total_avg`** | `float64` | Trung bình GT ròng khối ngoại | `-558064686.084787` |
| **`fr_buy_volume_matched_avg`** | `float64` | TB KL khớp lệnh khối ngoại mua | `261155.2867830424` |
| **`fr_buy_value_matched_avg`** | `float64` | TB GT khớp lệnh khối ngoại mua | `7688365812.568579` |
| **`fr_sell_volume_matched_avg`** | `float64` | TB KL khớp lệnh khối ngoại bán | `286478.0493765586` |
| **`fr_sell_value_matched_avg`** | `float64` | TB GT khớp lệnh khối ngoại bán | `8637299349.87531` |
| **`fr_buy_volume_deal_avg`** | `float64` | TB KL thỏa thuận khối ngoại mua | `605709.3541147133` |
| **`fr_buy_value_deal_avg`** | `float64` | TB GT thỏa thuận khối ngoại mua | `19548930748.5591` |
| **`fr_sell_volume_deal_avg`** | `float64` | TB KL thỏa thuận khối ngoại bán | `592744.0982543641` |
| **`fr_sell_value_deal_avg`** | `float64` | TB GT thỏa thuận khối ngoại bán | `19158062584.793518` |
| **`fr_net_volume_matched`** | `float64` | KL khớp lệnh ròng khối ngoại | `-50772139.0` |
| **`fr_net_value_matched`** | `float64` | GT khớp lệnh ròng khối ngoại | `-1902611742300.0` |
| **`fr_net_volume_matched_avg`** | `float64` | TB KL khớp lệnh ròng khối ngoại | `-25322.7625935162` |
| **`fr_net_value_matched_avg`** | `float64` | TB GT khớp lệnh ròng khối ngoại | `-948933537.306731` |
| **`fr_net_volume_deal`** | `float64` | KL thỏa thuận ròng khối ngoại | `25995338.0` |
| **`fr_net_value_deal`** | `float64` | GT thỏa thuận ròng khối ngoại | `783690668350.0` |
| **`fr_net_volume_deal_avg`** | `float64` | TB KL thỏa thuận ròng khối ngoại | `12965.2558603492` |
| **`fr_net_value_deal_avg`** | `float64` | TB GT thỏa thuận ròng khối ngoại | `390868163.765582` |
| **`total_buy_trade_volume`** | `float64` | Tổng khối lượng lệnh mua | `30708003090.0` |
| **`total_sell_trade_volume`** | `float64` | Tổng khối lượng lệnh bán | `31838178005.0` |
| **`total_buy_trade_volume_avg`** | `float64` | TB khối lượng lệnh mua | `15315712.264339153` |
| **`total_sell_trade_volume_avg`** | `float64` | TB khối lượng lệnh bán | `15879390.526184538` |
| **`total_buy_unmatched_volume_avg`** | `float64` | TB khối lượng mua chưa khớp | `6451915.369077308` |
| **`total_sell_unmatched_volume_avg`** | `float64` | TB khối lượng bán chưa khớp | `7015593.630922693` |
| **`total_buy_unmatched_volume`** | `float64` | Tổng khối lượng mua chưa khớp | `12936090315.0` |
| **`total_sell_unmatched_volume`** | `float64` | Tổng khối lượng bán chưa khớp | `14066265230.0` |

### `Market().equity('TCB').summary()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`high_52w`** | `int64` | Giá cao nhất 52 tuần | `40450` |
| **`low_52w`** | `int64` | Giá thấp nhất 52 tuần | `28109` |
| **`dividend`** | `int64` | Cổ tức | `1700` |
| **`beta`** | `float64` | Hệ số Beta | `1.03` |
| **`eps`** | `int64` | Thu nhập trên mỗi cổ phần (EPS) | `3675` |
| **`bvps`** | `float64` | Giá trị sổ sách trên mỗi cổ phần (BVPS) | `26344.4` |
| **`market_cap`** | `int64` | Vốn hóa thị trường | `221445012937500` |
| **`pe`** | `object` | Hệ số Giá / Lợi nhuận (P/E) | `8.39` |
| **`pb`** | `object` | Hệ số Giá / Giá trị sổ sách (P/B) | `1.17` |
| **`roe`** | `float64` | Tỷ suất sinh lời trên vốn chủ (ROE) | `15.85` |
| **`change_1m`** | `object` | Biến động giá 1 tháng (%) | `-6.16` |
| **`change_1y`** | `object` | Biến động giá 1 năm (%) | `4.97` |
| **`dividend_yield`** | `float64` | Tỷ suất cổ tức | `0.0544` |
| **`foreign_ownership_pct`** | `float64` | Tỷ lệ sở hữu nước ngoài (%) | `22.1251` |

### `Market().equity('TCB').trade_history()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`trading_date`** | `datetime64[ns]` | Ngày giao dịch | `2026-06-12T00:00:00.000` |
| **`end_trading_date`** | `object` | Ngày kết thúc giao dịch | `2026-06-12T00:00:00` |
| **`market_cap`** | `float64` | Vốn hóa thị trường | `221445012937500.0` |
| **`total_shares`** | `float64` | Tổng số cổ phần nắm giữ | `7086240414.0` |
| **`ceiling_price`** | `float64` | Giá trần | `33000.0` |
| **`floor_price`** | `float64` | Giá sàn | `28700.0` |
| **`reference_price`** | `float64` | Giá tham chiếu | `30850.0` |
| **`open`** | `float64` | Giá mở cửa | `31300.0` |
| **`close`** | `float64` | Giá đóng cửa | `31250.0` |
| **`match_price`** | `float64` | Giá khớp lệnh | `31250.0` |
| **`price_change`** | `float64` | Biến động giá | `400.0` |
| **`percent_price_change`** | `float64` | Biến động giá (%) | `0.01296596` |
| **`high`** | `float64` | Giá cao nhất | `31450.0` |
| **`low`** | `float64` | Giá thấp nhất | `31050.0` |
| **`average_price`** | `float64` | Giá trung bình | `31235.6860584628` |
| **`matched_volume`** | `float64` | Khối lượng khớp lệnh | `10936965.0` |
| **`matched_value`** | `float64` | Giá trị khớp lệnh | `341984224050.0` |
| **`deal_volume`** | `float64` | Khối lượng thỏa thuận | `3380000.0` |
| **`deal_value`** | `float64` | Giá trị thỏa thuận | `105216000000.0` |
| **`total_volume`** | `float64` | Tổng khối lượng | `14316965.0` |
| **`total_value`** | `float64` | Tổng giá trị | `447200224050.0` |
| **`total_buy_trade`** | `float64` | Tổng số lệnh mua | `3718.0` |
| **`total_buy_trade_volume`** | `float64` | Tổng khối lượng lệnh mua | `20335867.0` |
| **`total_sell_trade`** | `float64` | Tổng số lệnh bán | `4437.0` |
| **`total_sell_trade_volume`** | `float64` | Tổng khối lượng lệnh bán | `18804019.0` |
| **`reference_price_adjusted`** | `float64` | Giá tham chiếu điều chỉnh | `30850.0` |
| **`open_price_adjusted`** | `float64` | Giá mở cửa điều chỉnh | `31300.0` |
| **`close_price_adjusted`** | `float64` | Giá đóng cửa điều chỉnh | `31250.0` |
| **`price_change_adjusted`** | `float64` | Biến động giá điều chỉnh | `400.0` |
| **`percent_price_change_adjusted`** | `float64` | Biến động giá điều chỉnh (%) | `0.01296596` |
| **`highest_price_adjusted`** | `float64` | Giá cao nhất điều chỉnh | `31450.0` |
| **`lowest_price_adjusted`** | `float64` | Giá thấp nhất điều chỉnh | `31050.0` |
| **`price_change_value`** | `object` | Giá trị biến động | `+400 (+1.3%)` |
| **`total_buy_unmatched_volume`** | `float64` | Tổng khối lượng mua chưa khớp | `9398902.0` |
| **`total_sell_unmatched_volume`** | `float64` | Tổng khối lượng bán chưa khớp | `7867054.0` |
| **`average_buy_trade_volume`** | `float64` | Trung bình KL mỗi lệnh mua | `5469.5715438408` |
| **`average_sell_trade_volume`** | `float64` | Trung bình KL mỗi lệnh bán | `4238.0029299076` |
| **`total_net_trade_volume`** | `float64` | Tổng KL giao dịch ròng | `1531848.0` |

### `Market().equity('TCB').trades()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`index`** | `int64` | Mã chỉ số | `999` |
| **`time`** | `datetime64[ns]` | Thời gian giao dịch | `2026-06-12T13:06:31.000` |
| **`price`** | `float64` | Giá giao dịch | `31.35` |
| **`volume`** | `int64` | Khối lượng giao dịch | `300` |
| **`match_type`** | `object` | Loại lệnh khớp (Buy/Sell) | `Sell` |
| **`id`** | `object` | Mã ID hệ thống | `2026-06-12_130631_313500_300` |

### `Market().equity('TCB').trading_stats()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`average_match_volume`** | `float64` | Trung bình KL khớp lệnh | `8863796.895261845` |
| **`average_match_value`** | `float64` | Trung bình GT khớp lệnh | `310968578068.45386` |
| **`average_deal_volume`** | `float64` | Trung bình KL thỏa thuận | `2834322.1596009973` |
| **`average_deal_value`** | `float64` | Trung bình GT thỏa thuận | `87226991919.49677` |
| **`average_volume`** | `float64` | Khối lượng trung bình | `11698119.054862842` |
| **`average_value`** | `float64` | Giá trị trung bình | `398195569987.9506` |
| **`total_match_volume`** | `float64` | Tổng khối lượng khớp lệnh | `17771912775.0` |
| **`total_match_value`** | `float64` | Tổng giá trị khớp lệnh | `623491999027250.0` |
| **`total_deal_volume`** | `float64` | Tổng khối lượng thỏa thuận | `5682815930.0` |
| **`total_deal_value`** | `float64` | Tổng giá trị thỏa thuận | `174890118798591.0` |
| **`total_volume`** | `float64` | Tổng khối lượng | `23454728705.0` |
| **`total_value`** | `float64` | Tổng giá trị | `798382117825841.0` |
| **`fr_buy_volume_total`** | `float64` | Tổng KL khối ngoại mua | `1738063605.0` |
| **`fr_buy_value_total`** | `float64` | Tổng GT khối ngoại mua | `54610779605061.0` |
| **`fr_sell_volume_total`** | `float64` | Tổng KL khối ngoại bán | `1762840358.0` |
| **`fr_sell_value_total`** | `float64` | Tổng GT khối ngoại bán | `55729699300661.0` |
| **`fr_net_volume_total`** | `float64` | KL ròng khối ngoại | `-24776753.0` |
| **`fr_net_value_total`** | `float64` | GT ròng khối ngoại | `-1118919695600.0` |
| **`fr_buy_volume_matched`** | `float64` | KL khớp lệnh khối ngoại mua | `523616350.0` |
| **`fr_buy_value_matched`** | `float64` | GT khớp lệnh khối ngoại mua | `15415173454200.0` |
| **`fr_sell_volume_matched`** | `float64` | KL khớp lệnh khối ngoại bán | `574388489.0` |
| **`fr_sell_value_matched`** | `float64` | GT khớp lệnh khối ngoại bán | `17317785196500.0` |
| **`fr_buy_volume_deal`** | `float64` | KL thỏa thuận khối ngoại mua | `1214447255.0` |
| **`fr_buy_value_deal`** | `float64` | GT thỏa thuận khối ngoại mua | `39195606150861.0` |
| **`fr_sell_volume_deal`** | `float64` | KL thỏa thuận khối ngoại bán | `1188451917.0` |
| **`fr_sell_value_deal`** | `float64` | GT thỏa thuận khối ngoại bán | `38411915482511.0` |
| **`fr_buy_volume_total_avg`** | `float64` | TB tổng KL khối ngoại mua | `866864.6408977556` |
| **`fr_buy_value_total_avg`** | `float64` | TB tổng GT khối ngoại mua | `27237296561.12768` |
| **`fr_sell_volume_total_avg`** | `float64` | TB tổng KL khối ngoại bán | `879222.123690773` |
| **`fr_sell_value_total_avg`** | `float64` | TB tổng GT khối ngoại bán | `27795361247.212467` |
| **`fr_net_volume_total_avg`** | `float64` | Trung bình KL ròng khối ngoại | `-12357.4827930174` |
| **`fr_net_value_total_avg`** | `float64` | Trung bình GT ròng khối ngoại | `-558064686.084787` |
| **`fr_buy_volume_matched_avg`** | `float64` | TB KL khớp lệnh khối ngoại mua | `261155.2867830424` |
| **`fr_buy_value_matched_avg`** | `float64` | TB GT khớp lệnh khối ngoại mua | `7688365812.568579` |
| **`fr_sell_volume_matched_avg`** | `float64` | TB KL khớp lệnh khối ngoại bán | `286478.0493765586` |
| **`fr_sell_value_matched_avg`** | `float64` | TB GT khớp lệnh khối ngoại bán | `8637299349.87531` |
| **`fr_buy_volume_deal_avg`** | `float64` | TB KL thỏa thuận khối ngoại mua | `605709.3541147133` |
| **`fr_buy_value_deal_avg`** | `float64` | TB GT thỏa thuận khối ngoại mua | `19548930748.5591` |
| **`fr_sell_volume_deal_avg`** | `float64` | TB KL thỏa thuận khối ngoại bán | `592744.0982543641` |
| **`fr_sell_value_deal_avg`** | `float64` | TB GT thỏa thuận khối ngoại bán | `19158062584.793518` |
| **`fr_net_volume_matched`** | `float64` | KL khớp lệnh ròng khối ngoại | `-50772139.0` |
| **`fr_net_value_matched`** | `float64` | GT khớp lệnh ròng khối ngoại | `-1902611742300.0` |
| **`fr_net_volume_matched_avg`** | `float64` | TB KL khớp lệnh ròng khối ngoại | `-25322.7625935162` |
| **`fr_net_value_matched_avg`** | `float64` | TB GT khớp lệnh ròng khối ngoại | `-948933537.306731` |
| **`fr_net_volume_deal`** | `float64` | KL thỏa thuận ròng khối ngoại | `25995338.0` |
| **`fr_net_value_deal`** | `float64` | GT thỏa thuận ròng khối ngoại | `783690668350.0` |
| **`fr_net_volume_deal_avg`** | `float64` | TB KL thỏa thuận ròng khối ngoại | `12965.2558603492` |
| **`fr_net_value_deal_avg`** | `float64` | TB GT thỏa thuận ròng khối ngoại | `390868163.765582` |
| **`total_buy_trade_volume`** | `float64` | Tổng khối lượng lệnh mua | `30708003090.0` |
| **`total_sell_trade_volume`** | `float64` | Tổng khối lượng lệnh bán | `31838178005.0` |
| **`total_buy_trade_volume_avg`** | `float64` | TB khối lượng lệnh mua | `15315712.264339153` |
| **`total_sell_trade_volume_avg`** | `float64` | TB khối lượng lệnh bán | `15879390.526184538` |
| **`total_buy_unmatched_volume_avg`** | `float64` | TB khối lượng mua chưa khớp | `6451915.369077308` |
| **`total_sell_unmatched_volume_avg`** | `float64` | TB khối lượng bán chưa khớp | `7015593.630922693` |
| **`total_buy_unmatched_volume`** | `float64` | Tổng khối lượng mua chưa khớp | `12936090315.0` |
| **`total_sell_unmatched_volume`** | `float64` | Tổng khối lượng bán chưa khớp | `14066265230.0` |

### `Market().equity('TCB').volume_profile()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`price`** | `int64` | Giá giao dịch | `31050` |
| **`buy_volume`** | `int64` | Khối lượng mua | `0` |
| **`sell_volume`** | `int64` | Khối lượng bán | `233500` |
| **`unknown_volume`** | `int64` | Khối lượng không xác định | `0` |
| **`total_volume`** | `int64` | Tổng khối lượng | `233500` |

### `Market().index('VNINDEX').ohlcv(length='1Y')`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`time`** | `datetime64[ns]` | Thời gian giao dịch | `2025-06-16T07:00:00.000` |
| **`open`** | `float64` | Giá mở cửa | `1315.49` |
| **`high`** | `float64` | Giá cao nhất | `1338.66` |
| **`low`** | `float64` | Giá thấp nhất | `1307.37` |
| **`close`** | `float64` | Giá đóng cửa | `1338.11` |
| **`volume`** | `int64` | Khối lượng giao dịch | `778082690` |

### `Market().index('VNINDEX').stock_influence()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `GAS` |
| **`close_price`** | `int64` | Giá đóng cửa | `85100` |
| **`price_change`** | `float64` | Biến động giá | `2600.0` |
| **`percent_change`** | `float64` | Biến động giá (%) | `3.15` |
| **`outstanding_shares`** | `int64` | Cổ phiếu lưu hành | `2412949756` |
| **`market_cap`** | `int64` | Vốn hóa thị trường | `205342024235600` |
| **`weight`** | `float64` | Trọng số | `2.4398` |
| **`basic_index`** | `float64` | Chỉ số cơ sở | `1798.61` |
| **`influence_percent`** | `float64` | Tỷ lệ ảnh hưởng (%) | `0.0769` |
| **`influence_point`** | `float64` | Điểm ảnh hưởng | `1.3823` |
| **`influence_type`** | `int64` | Loại ảnh hưởng | `1` |
| **`rank`** | `int64` | Xếp hạng | `1` |

### `Market().index('VNINDEX').trade_history()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `VNINDEX` |
| **`trading_date`** | `datetime64[ns]` | Ngày giao dịch | `2026-06-12T00:00:00.000` |
| **`price_change`** | `float64` | Biến động giá | `-6.96` |
| **`percent_price_change`** | `float64` | Biến động giá (%) | `-0.00386965` |
| **`reference_price`** | `float64` | Giá tham chiếu | `1798.61` |
| **`open`** | `float64` | Giá mở cửa | `1813.07` |
| **`close`** | `float64` | Giá đóng cửa | `1791.65` |
| **`high`** | `float64` | Giá cao nhất | `1813.57` |
| **`low`** | `float64` | Giá thấp nhất | `1788.8` |
| **`matched_volume`** | `float64` | Khối lượng khớp lệnh | `579531594.0` |
| **`matched_value`** | `float64` | Giá trị khớp lệnh | `14684424706440.0` |
| **`deal_volume`** | `float64` | Khối lượng thỏa thuận | `62547894.0` |
| **`deal_value`** | `float64` | Giá trị thỏa thuận | `1724097882700.0` |
| **`total_volume`** | `float64` | Tổng khối lượng | `642079488.0` |
| **`total_value`** | `float64` | Tổng giá trị | `16408522589140.0` |
| **`total_stock_up_price`** | `float64` | Số mã tăng giá | `118.0` |
| **`total_stock_down_price`** | `float64` | Số mã giảm giá | `177.0` |
| **`total_stock_no_change_price`** | `float64` | Số mã đứng giá | `67.0` |
| **`total_stock_ceiling`** | `float64` | Số mã tăng trần | `4.0` |
| **`total_stock_floor`** | `float64` | Số mã giảm sàn | `2.0` |
| **`total_up_volume`** | `float64` | Tổng KL các mã tăng | `330654686.0` |
| **`total_down_volume`** | `float64` | Tổng KL các mã giảm | `205404849.0` |
| **`total_no_change_volume`** | `float64` | Tổng KL các mã đứng giá | `104139529.0` |
| **`total_trade`** | `float64` | Tổng số lệnh giao dịch | `333996.0` |
| **`total_buy_trade`** | `float64` | Tổng số lệnh mua | `321804.0` |
| **`total_buy_trade_volume`** | `float64` | Tổng khối lượng lệnh mua | `1238061142.0` |
| **`total_sell_trade`** | `float64` | Tổng số lệnh bán | `314589.0` |
| **`total_sell_trade_volume`** | `float64` | Tổng khối lượng lệnh bán | `1236216178.0` |
| **`total_shares`** | `float64` | Tổng số cổ phần nắm giữ | `217765258454.0` |
| **`market_cap`** | `float64` | Vốn hóa thị trường | `8471730528268030.0` |
| **`total_buy_unmatched_volume`** | `float64` | Tổng khối lượng mua chưa khớp | `658529548.0` |
| **`total_sell_unmatched_volume`** | `float64` | Tổng khối lượng bán chưa khớp | `656684584.0` |
| **`average_buy_trade_volume`** | `float64` | Trung bình KL mỗi lệnh mua | `3847.2521845595` |
| **`average_sell_trade_volume`** | `float64` | Trung bình KL mỗi lệnh bán | `3929.6230255985` |
| **`total_net_trade_volume`** | `float64` | Tổng KL giao dịch ròng | `1844964.0` |
| **`price_change_value`** | `object` | Giá trị biến động | `-6.96 (-0.4%)` |

### `Market().odd_lot(['TCB', 'SSI'])`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `TCB` |
| **`exchange`** | `object` | Sàn giao dịch (HOSE, HNX, UPCOM) | `HOSE` |
| **`reference_price`** | `int64` | Giá tham chiếu | `30850` |
| **`ceiling_price`** | `int64` | Giá trần | `33000` |
| **`floor_price`** | `int64` | Giá sàn | `28700` |
| **`open_price`** | `int64` | Giá mở cửa | `31000` |
| **`high_price`** | `int64` | Giá cao nhất | `31550` |
| **`low_price`** | `int64` | Giá thấp nhất | `31000` |
| **`match_price`** | `int64` | Giá khớp lệnh | `31200` |
| **`match_vol`** | `int64` | Khối lượng khớp lệnh | `1` |
| **`total_volume`** | `int64` | Tổng khối lượng | `5765` |
| **`bid_price_1`** | `object` | Giá Mua 1 | `31200.0` |
| **`bid_vol_1`** | `int64` | Khối lượng Mua 1 | `192` |
| **`bid_price_2`** | `int64` | Giá Mua 2 | `31150` |
| **`bid_vol_2`** | `int64` | Khối lượng Mua 2 | `736` |
| **`bid_price_3`** | `int64` | Giá Mua 3 | `31100` |
| **`bid_vol_3`** | `int64` | Khối lượng Mua 3 | `516` |
| **`ask_price_1`** | `object` | Giá Bán 1 | `31250.0` |
| **`ask_vol_1`** | `int64` | Khối lượng Bán 1 | `16` |
| **`ask_price_2`** | `int64` | Giá Bán 2 | `31350` |
| **`ask_vol_2`** | `int64` | Khối lượng Bán 2 | `33` |
| **`ask_price_3`** | `int64` | Giá Bán 3 | `31450` |
| **`ask_vol_3`** | `int64` | Khối lượng Bán 3 | `70` |
| **`foreign_buy_volume`** | `int64` | Khối lượng khối ngoại mua | `5268002` |
| **`foreign_sell_volume`** | `int64` | Khối lượng khối ngoại bán | `0` |

### `Market().price_board(['TCB', 'SSI'])`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `TCB` |
| **`exchange`** | `object` | Sàn giao dịch (HOSE, HNX, UPCOM) | `HOSE` |
| **`reference_price`** | `int64` | Giá tham chiếu | `30850` |
| **`ceiling_price`** | `int64` | Giá trần | `33000` |
| **`floor_price`** | `int64` | Giá sàn | `28700` |
| **`open_price`** | `int64` | Giá mở cửa | `31300` |
| **`high_price`** | `int64` | Giá cao nhất | `31450` |
| **`low_price`** | `int64` | Giá thấp nhất | `31050` |
| **`close_price`** | `int64` | Giá đóng cửa | `31250` |
| **`bid_price_1`** | `object` | Giá Mua 1 | `31200.0` |
| **`bid_vol_1`** | `int64` | Khối lượng Mua 1 | `500` |
| **`bid_price_2`** | `int64` | Giá Mua 2 | `31150` |
| **`bid_vol_2`** | `int64` | Khối lượng Mua 2 | `11800` |
| **`bid_price_3`** | `int64` | Giá Mua 3 | `31100` |
| **`bid_vol_3`** | `int64` | Khối lượng Mua 3 | `300800` |
| **`ask_price_1`** | `object` | Giá Bán 1 | `31250.0` |
| **`ask_vol_1`** | `int64` | Khối lượng Bán 1 | `4200` |
| **`ask_price_2`** | `int64` | Giá Bán 2 | `31300` |
| **`ask_vol_2`** | `int64` | Khối lượng Bán 2 | `135900` |
| **`ask_price_3`** | `int64` | Giá Bán 3 | `31350` |
| **`ask_vol_3`** | `int64` | Khối lượng Bán 3 | `50100` |
| **`foreign_buy_volume`** | `int64` | Khối lượng khối ngoại mua | `5268002` |
| **`foreign_sell_volume`** | `int64` | Khối lượng khối ngoại bán | `5121658` |

### `Market().quote(['TCB', 'SSI'])`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `TCB` |
| **`exchange`** | `object` | Sàn giao dịch (HOSE, HNX, UPCOM) | `HOSE` |
| **`reference_price`** | `int64` | Giá tham chiếu | `30850` |
| **`ceiling_price`** | `int64` | Giá trần | `33000` |
| **`floor_price`** | `int64` | Giá sàn | `28700` |
| **`open_price`** | `int64` | Giá mở cửa | `31300` |
| **`high_price`** | `int64` | Giá cao nhất | `31450` |
| **`low_price`** | `int64` | Giá thấp nhất | `31050` |
| **`close_price`** | `int64` | Giá đóng cửa | `31250` |
| **`bid_price_1`** | `object` | Giá Mua 1 | `31200.0` |
| **`bid_vol_1`** | `int64` | Khối lượng Mua 1 | `500` |
| **`bid_price_2`** | `int64` | Giá Mua 2 | `31150` |
| **`bid_vol_2`** | `int64` | Khối lượng Mua 2 | `11800` |
| **`bid_price_3`** | `int64` | Giá Mua 3 | `31100` |
| **`bid_vol_3`** | `int64` | Khối lượng Mua 3 | `300800` |
| **`ask_price_1`** | `object` | Giá Bán 1 | `31250.0` |
| **`ask_vol_1`** | `int64` | Khối lượng Bán 1 | `4200` |
| **`ask_price_2`** | `int64` | Giá Bán 2 | `31300` |
| **`ask_vol_2`** | `int64` | Khối lượng Bán 2 | `135900` |
| **`ask_price_3`** | `int64` | Giá Bán 3 | `31350` |
| **`ask_vol_3`** | `int64` | Khối lượng Bán 3 | `50100` |
| **`foreign_buy_volume`** | `int64` | Khối lượng khối ngoại mua | `5268002` |
| **`foreign_sell_volume`** | `int64` | Khối lượng khối ngoại bán | `5121658` |

