# Insights Layer Schema

### `Insights().equity('ACB').order_flow()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`match_price`** | `int64` | Giá khớp lệnh | `26500` |
| **`active_buy_volume`** | `int64` | Active Buy Khối lượng | `0` |
| **`active_sell_volume`** | `int64` | Active Sell Khối lượng | `0` |
| **`unknown_volume`** | `int64` | Khối lượng không xác định | `0` |

### `Insights().equity('ACB').order_flow_history()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `ACB` |
| **`time`** | `object` | Thời gian giao dịch | `2/9/2026 00:00:00` |
| **`outstanding_shares`** | `int64` | Cổ phiếu lưu hành | `5136656599` |
| **`listed_shares`** | `int64` | Khối lượng cổ phiếu niêm yết | `5136656599` |
| **`free_float`** | `int64` | Tỷ lệ cổ phiếu tự do chuyển nhượng | `4622990939` |
| **`market_cap`** | `float64` | Vốn hóa thị trường | `117886.26895` |
| **`reference_price`** | `int64` | Giá tham chiếu | `23000` |
| **`avg_price`** | `int64` | Avg Giá | `23100` |
| **`ceiling_price`** | `int64` | Giá trần | `24600` |
| **`floor_price`** | `int64` | Giá sàn | `21400` |
| **`open_price`** | `int64` | Giá mở cửa | `23200` |
| **`close`** | `int64` | Giá đóng cửa | `22950` |
| **`price_change_percent_1d`** | `int64` | Giá Change Percent 1d | `23000` |
| **`close_index`** | `float64` | Close index | `1754.82` |
| **`high_52w`** | `int64` | Giá cao nhất 52 tuần | `29500` |
| **`low_52w`** | `float64` | Giá thấp nhất 52 tuần | `17339.04` |
| **`foreign_held_volume`** | `int64` | Foreign Held Khối lượng | `1426039537` |
| **`foreign_room`** | `int64` | Foreign room | `114957442` |
| **`volume`** | `int64` | Khối lượng giao dịch | `13677300` |
| **`total_value`** | `float64` | Tổng giá trị | `316394.285` |
| **`put_through_volume`** | `int64` | Put Through Khối lượng | `2549000` |
| **`put_through_value`** | `int64` | Giá trị giao dịch thỏa thuận | `59376900000` |
| **`foreign_buy_volume`** | `int64` | Khối lượng khối ngoại mua | `755900` |
| **`foreign_sell_volume`** | `int64` | Khối lượng khối ngoại bán | `3553300` |
| **`proprietary_buy_volume`** | `int64` | Proprietary Buy Khối lượng | `1101000` |
| **`proprietary_sell_volume`** | `int64` | Proprietary Sell Khối lượng | `1784900` |
| **`remain_buy_volume`** | `int64` | Remain Buy Khối lượng | `8680448` |
| **`remain_sell_volume`** | `int64` | Remain Sell Khối lượng | `8525238` |
| **`foreign_net_buy_volume`** | `int64` | Foreign Net Buy Khối lượng | `-2797400` |
| **`foreign_net_buy_value`** | `int64` | Giá trị khối ngoại mua ròng | `-64648120000` |
| **`proprietary_net_buy_volume`** | `int64` | Proprietary Net Buy Khối lượng | `-683900` |
| **`proprietary_net_buy_value`** | `int64` | Giá trị tự doanh mua ròng | `-15531960000` |
| **`rs_1m`** | `float64` | Sức mạnh giá (RS) 1 tháng | `-0.49332` |
| **`rs_3m`** | `float64` | Sức mạnh giá (RS) 3 tháng | `-16.01023` |
| **`rs_1y`** | `float64` | Sức mạnh giá (RS) 1 năm | `-22.34161` |
| **`avg_volume_10d`** | `int64` | Avg Khối lượng 10d | `17439250` |
| **`avg_volume_5d`** | `int64` | Avg Khối lượng 5d | `15862120` |
| **`avg_volume_20d`** | `int64` | Avg Khối lượng 20d | `16047190` |
| **`vol_10d_vs_3m`** | `float64` | Khối lượng | `52.44404` |
| **`vol_10d_vs_6m`** | `float64` | Khối lượng | `18.29683` |
| **`avg_price_5d`** | `int64` | Avg Giá 5d | `23340` |
| **`avg_price_10d`** | `int64` | Avg Giá 10d | `23695` |
| **`avg_price_20d`** | `float64` | Avg Giá 20d | `24297.5` |
| **`avg_price_50d`** | `int64` | Avg Giá 50d | `24221` |
| **`avg_price_200d`** | `float64` | Avg Giá 200d | `23950.66` |
| **`bid_price`** | `object` | Bid Giá | `22950\|22900\|22850` |
| **`bid_size`** | `object` | Bid size | `284500\|703000\|308300` |
| **`ask_price`** | `object` | Ask Giá | `23000\|23050\|23100` |
| **`ask_size`** | `object` | Ask size | `107000\|21900\|76400` |
| **`daily_return`** | `float64` | Lợi nhuận hàng ngày | `-0.21739` |
| **`return_mean`** | `float64` | Return mean | `0.06267` |
| **`std_return`** | `float64` | Độ lệch chuẩn lợi nhuận | `1.50197` |
| **`var_5percent`** | `float64` | Var 5percent | `-1.96851` |
| **`adj_close_price`** | `int64` | Adj Close Giá | `22950` |
| **`active_buy_value`** | `int64` | Giá trị mua chủ động | `89250030000` |
| **`active_sell_value`** | `int64` | Giá trị bán chủ động | `153407630000` |
| **`active_buy_volume`** | `int64` | Active Buy Khối lượng | `0` |
| **`active_sell_volume`** | `int64` | Active Sell Khối lượng | `0` |

### `Insights().equity('ACB').peer_compare()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `ACB` |
| **`icb_code`** | `object` | Mã chuẩn phân ngành ICB | `8350` |
| **`pe`** | `float64` | Hệ số Giá / Lợi nhuận (P/E) | `8.36804` |
| **`pb`** | `float64` | Hệ số Giá / Giá trị sổ sách (P/B) | `1.37843` |
| **`ev_ebitda`** | `object` | Ev ebitda | `None` |
| **`eps`** | `float64` | Thu nhập trên mỗi cổ phần (EPS) | `3166.81107` |
| **`bvps`** | `float64` | Giá trị sổ sách trên mỗi cổ phần (BVPS) | `19224.77201` |
| **`ebitda_per_share`** | `int64` | Ebitda per share | `0` |
| **`industry_pe`** | `float64` | Industry pe | `9.32892` |
| **`industry_pb`** | `float64` | Industry pb | `1.45262` |
| **`industry_ev_ebitda`** | `object` | Industry ev ebitda | `None` |
| **`market_pe`** | `float64` | Market pe | `13.4422` |
| **`market_pb`** | `float64` | Market pb | `1.93898` |
| **`market_ev_ebitda`** | `object` | Market ev ebitda | `None` |
| **`related_securities`** | `object` | Related Chứng khoán | `[{'symbol': 'VPB', 'pe': 7.84531, 'pb': 1.10545...` |
| **`free_cash_flow_to_equity`** | `object` | Dòng tiền tự do cho vốn chủ (FCFE) | `[{'time': '20251231', 'free_cash_flow_to_equity...` |
| **`sustainable_growth_rate`** | `object` | Tốc độ tăng trưởng bền vững | `None` |
| **`cost_of_equity`** | `object` | Chi phí vốn chủ sở hữu | `None` |
| **`outstanding_shares`** | `int64` | Cổ phiếu lưu hành | `5136656599` |
| **`avg_index_return_5y`** | `float64` | Avg index return 5y | `13.62465` |
| **`avg_bank_interest_12m`** | `float64` | Avg bank interest 12m | `5.9` |
| **`beta_1y`** | `float64` | Hệ số Beta 1 năm | `0.9025758988` |
| **`roe`** | `float64` | Tỷ suất sinh lời trên vốn chủ (ROE) | `17.49605` |
| **`industry_roe`** | `float64` | Industry roe | `16.91109` |
| **`market_roe`** | `float64` | Market roe | `16.02409` |

### `Insights().equity('ACB').rrg()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `ACB` |
| **`time`** | `object` | Thời gian giao dịch | `20250612` |
| **`price`** | `float64` | Giá giao dịch | `21.05` |
| **`index_price`** | `float64` | Index Giá | `1322.99` |
| **`rrg_rs_mid`** | `float64` | Sức mạnh tương đối trung hạn (RRG) | `0.0` |
| **`rrg_rm_mid`** | `float64` | Momentum tương đối trung hạn (RRG) | `0.0` |
| **`rrg_rs_standard`** | `float64` | Sức mạnh tương đối tiêu chuẩn (RRG) | `0.0` |
| **`rrg_rm_standard`** | `float64` | Momentum tương đối tiêu chuẩn (RRG) | `0.0` |
| **`rrg_rs_short`** | `float64` | Sức mạnh tương đối ngắn hạn (RRG) | `0.0` |
| **`rrg_rm_short`** | `float64` | Momentum tương đối ngắn hạn (RRG) | `0.0` |
| **`rsi_14`** | `float64` | Chỉ báo RSI | `0.0` |
| **`stoch_rsi_14`** | `float64` | Chỉ báo Stochastic RSI 14 | `0.0` |
| **`draw_down_status`** | `object` | Draw down status | `None` |
| **`draw_down_value`** | `float64` | Draw Down Giá trị | `-0.06004` |

### `Insights().flow.active()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`volume_1d`** | `int64` | Khối lượng 1d | `-175900` |
| **`value_1d`** | `int64` | Giá trị 1 ngày | `-8865820000` |
| **`volume_10d`** | `int64` | Khối lượng 10d | `-1744500` |
| **`value_10d`** | `int64` | Giá trị 10 ngày | `-88553360000` |
| **`value_1m`** | `float64` | Giá trị 1 tháng | `None` |
| **`volume_1m`** | `float64` | Khối lượng 1m | `None` |
| **`volume_3m`** | `float64` | Khối lượng 3m | `None` |
| **`value_3m`** | `float64` | Giá trị 3 tháng | `None` |
| **`volume_6m`** | `float64` | Khối lượng 6m | `None` |
| **`value_6m`** | `float64` | Giá trị 6 tháng | `None` |
| **`status`** | `object` | Trạng thái (Ví dụ: CLOSED, OPEN) | `None` |

### `Insights().flow.foreign()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `REE` |
| **`volume_1d`** | `int64` | Khối lượng 1d | `18` |
| **`value_1d`** | `int64` | Giá trị 1 ngày | `912600` |
| **`volume_10d`** | `int64` | Khối lượng 10d | `-2881` |
| **`value_10d`** | `int64` | Giá trị 10 ngày | `-148379900` |
| **`value_1m`** | `float64` | Giá trị 1 tháng | `None` |
| **`volume_1m`** | `float64` | Khối lượng 1m | `None` |
| **`volume_3m`** | `float64` | Khối lượng 3m | `None` |
| **`value_3m`** | `float64` | Giá trị 3 tháng | `None` |
| **`volume_6m`** | `float64` | Khối lượng 6m | `None` |
| **`value_6m`** | `float64` | Giá trị 6 tháng | `None` |

### `Insights().flow.proprietary()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `REE` |
| **`volume_1d`** | `int64` | Khối lượng 1d | `-15900` |
| **`value_1d`** | `int64` | Giá trị 1 ngày | `-803700000` |
| **`volume_10d`** | `int64` | Khối lượng 10d | `-172000` |
| **`value_10d`** | `int64` | Giá trị 10 ngày | `-8975450000` |
| **`value_1m`** | `float64` | Giá trị 1 tháng | `None` |
| **`volume_1m`** | `float64` | Khối lượng 1m | `None` |
| **`volume_3m`** | `float64` | Khối lượng 3m | `None` |
| **`value_3m`** | `float64` | Giá trị 3 tháng | `None` |
| **`volume_6m`** | `float64` | Khối lượng 6m | `None` |
| **`value_6m`** | `float64` | Giá trị 6 tháng | `None` |

### `Insights().ranking.deal()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `TCI` |
| **`exchange`** | `object` | Sàn giao dịch (HOSE, HNX, UPCOM) | `HOSE` |
| **`last_price`** | `float64` | Last Giá | `12.25` |
| **`last_updated`** | `object` | Thời gian / Ngày tháng | `2026-06-12 15:15` |
| **`price_change_1d`** | `float64` | Giá Change 1d | `-0.2` |
| **`price_change_percent_1d`** | `float64` | Giá Change Percent 1d | `-1.6064257028` |
| **`total_value`** | `float64` | Tổng giá trị | `9490685000.0` |
| **`deal_volume_spike_20d_percent`** | `float64` | Deal Khối lượng Spike 20d Percent | `524.5447607158` |

### `Insights().ranking.foreign_buy()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `MSN` |
| **`date`** | `object` | Ngày giao dịch / Dấu thời gian | `2026-05-25` |
| **`net_value`** | `float64` | Net Giá trị | `145318424000.0` |

### `Insights().ranking.foreign_sell()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `MSB` |
| **`date`** | `object` | Ngày giao dịch / Dấu thời gian | `2026-05-25` |
| **`net_value`** | `float64` | Net Giá trị | `-1483883396550.0` |

### `Insights().ranking.gainer()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `APG` |
| **`exchange`** | `object` | Sàn giao dịch (HOSE, HNX, UPCOM) | `HOSE` |
| **`last_price`** | `float64` | Last Giá | `5.17` |
| **`last_updated`** | `object` | Thời gian / Ngày tháng | `2026-06-12 15:15` |
| **`price_change_1d`** | `float64` | Giá Change 1d | `0.33` |
| **`price_change_percent_1d`** | `float64` | Giá Change Percent 1d | `6.8181818182` |
| **`total_value`** | `float64` | Tổng giá trị | `1973389000.0` |
| **`avg_volume_20d`** | `float64` | Avg Khối lượng 20d | `226994.85` |
| **`volume_spike_20d_percent`** | `float64` | Khối lượng Spike 20d Percent | `168.1535946741` |

### `Insights().ranking.loser()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `HAP` |
| **`exchange`** | `object` | Sàn giao dịch (HOSE, HNX, UPCOM) | `HOSE` |
| **`last_price`** | `float64` | Last Giá | `6.08` |
| **`last_updated`** | `object` | Thời gian / Ngày tháng | `2026-06-12 15:15` |
| **`price_change_1d`** | `float64` | Giá Change 1d | `-0.45` |
| **`price_change_percent_1d`** | `float64` | Giá Change Percent 1d | `-6.8912710567` |
| **`total_value`** | `float64` | Tổng giá trị | `330739000.0` |

### `Insights().ranking.value()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `ACB` |
| **`exchange`** | `object` | Sàn giao dịch (HOSE, HNX, UPCOM) | `HOSE` |
| **`last_price`** | `float64` | Last Giá | `22.832` |
| **`last_updated`** | `object` | Thời gian / Ngày tháng | `2026-06-12 15:15` |
| **`price_change_1d`** | `float64` | Giá Change 1d | `0.0` |
| **`price_change_percent_1d`** | `float64` | Giá Change Percent 1d | `0.0` |
| **`total_value`** | `float64` | Tổng giá trị | `1646480345000.0` |

### `Insights().ranking.volume()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `AGG` |
| **`exchange`** | `object` | Sàn giao dịch (HOSE, HNX, UPCOM) | `HOSE` |
| **`last_price`** | `float64` | Last Giá | `12.6` |
| **`last_updated`** | `object` | Thời gian / Ngày tháng | `2026-06-12 15:15` |
| **`price_change_1d`** | `float64` | Giá Change 1d | `0.8` |
| **`price_change_percent_1d`** | `float64` | Giá Change Percent 1d | `6.7796610169` |
| **`total_value`** | `float64` | Tổng giá trị | `16837945000.0` |
| **`avg_volume_20d`** | `float64` | Avg Khối lượng 20d | `243509.75` |
| **`volume_spike_20d_percent`** | `float64` | Khối lượng Spike 20d Percent | `556.9386852066` |

### `Insights().screener.criteria()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`category`** | `object` | Phân loại | `general` |
| **`field_name`** | `object` | Tên trường | `sectorLv1` |
| **`column_name`** | `object` | Tên cột | `sector_lv1` |
| **`readable_name`** | `object` | Tên hiển thị | `sectorLv1` |
| **`select_type`** | `object` | Select type | `multiple` |

### `Insights().screener.filter()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `ABB` |
| **`exchange`** | `object` | Sàn giao dịch (HOSE, HNX, UPCOM) | `UPCOM` |
| **`reference_price`** | `float64` | Giá tham chiếu | `16900.0` |
| **`ceiling_price`** | `float64` | Giá trần | `19400.0` |
| **`price`** | `float64` | Giá giao dịch | `16700.0` |
| **`floor_price`** | `float64` | Giá sàn | `14400.0` |
| **`accumulated_value`** | `float64` | Accumulated Giá trị | `17839930000.0` |
| **`accumulated_volume`** | `float64` | Accumulated Khối lượng | `1060500.0` |
| **`market_cap`** | `float64` | Vốn hóa thị trường | `23333385039500.0` |
| **`price_change_percent`** | `float64` | Giá Change Percent | `-1.18343195` |
| **`avg_value_30d`** | `float64` | TB giá trị 30 ngày | `15348420280.0` |
| **`avg_value_10d`** | `float64` | TB giá trị 10 ngày | `-21.47798149` |
| **`avg_volume_30d`** | `float64` | Avg Khối lượng 30d | `978265.3666666667` |
| **`est_volume`** | `float64` | Est Khối lượng | `940344.8275863` |
| **`volume_breakout_30d`** | `float64` | Khối lượng Breakout 30d | `-3.87630395` |
| **`pe`** | `float64` | Hệ số Giá / Lợi nhuận (P/E) | `5.3694548294` |
| **`pb`** | `float64` | Hệ số Giá / Giá trị sổ sách (P/B) | `1.0998780786` |
| **`roe`** | `float64` | Tỷ suất sinh lời trên vốn chủ (ROE) | `21.18864627` |
| **`profit_growth_yoy`** | `float64` | Tăng trưởng lợi nhuận (YoY) | `260.73978288` |
| **`revenue_growth_yoy`** | `float64` | Tăng trưởng doanh thu (YoY) | `49.46042643` |
| **`net_margin`** | `float64` | Biên lợi nhuận ròng (%) | `34.54884885` |
| **`gross_margin`** | `float64` | Biên lợi nhuận gộp (%) | `68.62084412` |
| **`match_price_time`** | `object` | Match Giá Time | `2026-06-12T08:34:30.163` |
| **`rs_3m`** | `int64` | Sức mạnh giá (RS) 3 tháng | `94` |
| **`ema_time`** | `object` | Thời gian / Ngày tháng | `1781136000` |
| **`ema_20`** | `float64` | Đường trung bình hàm mũ (EMA) 20 | `15920.4804283819` |
| **`price_ema_20`** | `float64` | Giá Ema 20 | `4.89633196` |
| **`ema_20_ema_50`** | `float64` | Độ lệch EMA 20 và EMA 50 | `3.86796993` |
| **`ema_50_ema_200`** | `float64` | Độ lệch EMA 50 và EMA 200 | `13.96154367` |
| **`macd_signal`** | `float64` | Đường tín hiệu MACD | `320.1624675356` |
| **`macd`** | `float64` | Chỉ báo MACD | `419.3024070622` |
| **`histogram`** | `float64` | Biểu đồ Histogram | `99.1399395266` |
| **`outperforms_index_3m`** | `float64` | Hiệu suất vượt trội chỉ số (3 tháng) | `19.8281104` |
| **`price_return_3m`** | `float64` | Giá Return 3m | `24.62686567` |
| **`price_fluctuation_30d`** | `float64` | Giá Fluctuation 30d | `13.42281879` |
| **`prev_rsi`** | `object` | Prev rsi | `{'avgGain': 113.2008776475, 'avgLoss': 18.66218...` |
| **`rsi`** | `float64` | Chỉ báo RSI | `76.8778705536` |
| **`last_modified_date`** | `object` | Last Modified Ngày | `2026-06-12T10:26:04.242` |
| **`company_name_en`** | `object` | Tên công ty (Tiếng Anh) | `An Binh Commercial Joint Stock Bank` |
| **`short_name_en`** | `object` | Tên viết tắt (Tiếng Anh) | `An Binh Bank` |
| **`company_name`** | `object` | Tên công ty | `Ngân hàng Thương mại Cổ phần An Bình` |
| **`short_name`** | `object` | Tên viết tắt | `Ngân hàng An Bình` |
| **`icb_code2`** | `object` | Mã phân ngành ICB cấp 2 | `8300` |
| **`industry_en`** | `object` | Ngành nghề (Tiếng Anh) | `Banks` |
| **`vi_sector`** | `object` | Vi sector | `Ngân hàng` |
| **`icb_code4`** | `object` | Icb code4 | `8355` |
| **`stock_strength`** | `int64` | Sức mạnh cổ phiếu | `91` |
| **`stock_trend`** | `object` | Xu hướng cổ phiếu | `STRONG_UPTREND` |
| **`adx`** | `float64` | Chỉ báo sức mạnh xu hướng (ADX) | `66.1957217119` |
| **`ao`** | `float64` | Chỉ báo Awesome Oscillator (AO) | `952.9411764706` |
| **`ao_trend`** | `object` | Xu hướng AO | `ABOVE_ZERO` |

### `Insights().sector('bank').flow_intraday()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`time`** | `datetime64[ns]` | Thời gian giao dịch | `2026-06-14T09:00:00.000` |
| **`net_active_buy_value`** | `int64` | Giá trị mua chủ động ròng | `3985720000` |

### `Insights().sector('bank').index_intraday()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`time`** | `datetime64[ns]` | Thời gian giao dịch | `2026-06-14T09:00:00.000` |
| **`index_value`** | `float64` | Index Giá trị | `358.16298` |

### `Insights().sector('bank').members()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `ABB` |
| **`company_name`** | `object` | Tên công ty | `Ngân hàng An Bình` |
| **`company_name_en`** | `object` | Tên công ty (Tiếng Anh) | `An Binh Bank` |
| **`reference_price`** | `int64` | Giá tham chiếu | `16900` |
| **`floor_price`** | `int64` | Giá sàn | `14400` |
| **`ceiling_price`** | `int64` | Giá trần | `19400` |
| **`percent_change`** | `float64` | Biến động giá (%) | `-1.18343` |
| **`total_value`** | `float64` | Tổng giá trị | `17862097900.0` |
| **`market_cap`** | `int64` | Vốn hóa thị trường | `23333000000000` |
| **`pe`** | `float64` | Hệ số Giá / Lợi nhuận (P/E) | `6.34807` |
| **`pb`** | `float64` | Hệ số Giá / Giá trị sổ sách (P/B) | `1.30334` |
| **`eps`** | `float64` | Thu nhập trên mỗi cổ phần (EPS) | `None` |
| **`bvps`** | `float64` | Giá trị sổ sách trên mỗi cổ phần (BVPS) | `None` |
| **`beta`** | `float64` | Hệ số Beta | `0.2851` |
| **`dividend_yield`** | `float64` | Tỷ suất cổ tức | `None` |
| **`roe`** | `float64` | Tỷ suất sinh lời trên vốn chủ (ROE) | `22.419` |
| **`roa`** | `float64` | Tỷ suất sinh lời trên tổng tài sản (ROA) | `1.679` |
| **`eps_growth`** | `float64` | Tăng trưởng EPS (%) | `382.356` |
| **`revenue_growth`** | `float64` | Tăng trưởng doanh thu (%) | `55.461` |
| **`total_equity`** | `float64` | Tổng vốn chủ sở hữu | `None` |
| **`total_assets`** | `int64` | Tổng tài sản | `250098000000000` |

### `Insights().sector('bank').rrg()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`time`** | `datetime64[ns]` | Thời gian giao dịch | `2025-06-13T00:00:00.000` |
| **`index_price`** | `float64` | Index Giá | `1315.49` |
| **`rsi_14`** | `float64` | Chỉ báo RSI | `0.0` |
| **`stoch_rsi_14`** | `float64` | Chỉ báo Stochastic RSI 14 | `0.0` |

### `Insights().sentiment.breadth()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`time`** | `datetime64[ns]` | Thời gian giao dịch | `2023-06-14T00:00:00.000` |
| **`pe`** | `float64` | Hệ số Giá / Lợi nhuận (P/E) | `11.57459` |
| **`pb`** | `float64` | Hệ số Giá / Giá trị sổ sách (P/B) | `1.35718` |
| **`position_line`** | `float64` | Position line | `0.48589` |

### `Insights().sentiment.contribution()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `GAS` |
| **`value`** | `float64` | Giá trị giao dịch | `0.07378` |
| **`point`** | `float64` | Điểm số | `1.32701` |
| **`type`** | `object` | Loại hình (Ví dụ: corporate, STOCK) | `up` |
| **`time`** | `datetime64[ns]` | Thời gian giao dịch | `2026-12-06T00:00:00.000` |

### `Insights().sentiment.heatmap()`
| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa | Giá Trị Mẫu |
| --- | --- | --- | --- |
| **`symbol`** | `object` | Mã định danh chứng khoán / tổ chức | `REE` |
| **`icb_code`** | `object` | Mã chuẩn phân ngành ICB | `2750` |
| **`market_cap`** | `float64` | Vốn hóa thị trường | `31394.11141` |
| **`price_change`** | `float64` | Biến động giá | `-0.2` |
| **`price_change_status`** | `object` | Giá Change Status | `D` |
| **`volume_1d`** | `float64` | Khối lượng 1d | `300100.0` |
| **`value_1d`** | `float64` | Giá trị 1 ngày | `15136960000.0` |
| **`volume_10d`** | `float64` | Khối lượng 10d | `4726000.0` |
| **`value_10d`** | `float64` | Giá trị 10 ngày | `240125200000.0` |
| **`value_1m`** | `float64` | Giá trị 1 tháng | `None` |
| **`volume_1m`** | `float64` | Khối lượng 1m | `None` |

