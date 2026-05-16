# Vnstock TA - Thư Viện Phân Tích Kỹ Thuật

## Giới Thiệu

`vnstock_ta` là thư viện Python chuyên dụng cung cấp các chỉ báo kỹ thuật (Technical Indicators) cho phân tích dữ liệu thị trường chứng khoán. Thư viện được thiết kế để tích hợp liền mạch với `vnstock_data`, cung cấp quy trình hoàn chỉnh từ lấy dữ liệu đến phân tích kỹ thuật.

### Đặc Điểm Chính

- **Chỉ báo phong phú**: 60 chỉ báo kỹ thuật được phân loại theo 5 danh mục (Trend, Momentum, Volatility, Volume, Statistics).
- **API thống nhất**: Giao diện đơn giản, hướng đối tượng dễ sử dụng thông qua lớp `Indicator`.
- **Tích hợp pandas**: Hoạt động trực tiếp với DataFrame, output là Series hoặc DataFrame.
- **Vẽ biểu đồ**: Việc vẽ biểu đồ được chuyển giao cho `vnstock_ezchart` thay vì cấu hình sẵn trong thư viện để tối ưu và đảm bảo tính nhất quán nếu người dùng cần thiết, hiện tại chức năng vẽ biểu đồ tương tác sẽ bị loại bỏ sau 31/8/2026 để tập trung vào khả năng tính toán chỉ báo.

### Cấu Trúc Package

```
vnstock_ta/
├── __init__.py          # Export Indicator, DataSource
├── interface.py         # Cung cấp Indicator class chính
├── get_data.py          # DataSource - lấy dữ liệu từ vnstock_data
├── indicators/          # Chỉ báo kỹ thuật
│   ├── __init__.py
│   ├── trend.py         # Trend indicators
│   ├── momentum.py      # Momentum indicators
│   ├── volatility.py    # Volatility indicators
│   ├── volume.py        # Volume indicators
│   ├── statistics.py    # Statistics & structure indicators
│   └── docs.py          # Tài liệu docstring
└── utils/               # Utilities
```

### Các Loại Chỉ Báo

#### 1. **Trend Indicators** (Chỉ báo Xu Hướng)
| Chỉ báo    | Ký hiệu    | Mô tả                          |
| ---------- | ---------- | ------------------------------ |
| SMA        | sma        | Simple Moving Average          |
| EMA        | ema        | Exponential Moving Average     |
| WMA        | wma        | Weighted Moving Average        |
| HMA        | hma        | Hull Moving Average            |
| SMMA       | smma       | Smoothed Moving Average        |
| ALMA       | alma       | Arnaud Legoux Moving Average   |
| VWMA       | vwma       | Volume-Weighted Moving Average |
| ADX        | adx        | Average Directional Index      |
| ICHIMOKU   | ichimoku   | Ichimoku Cloud                 |
| PSAR       | psar       | Parabolic SAR                  |
| SUPERTREND | supertrend | Supertrend                     |
| DM         | dm         | Directional Movement           |
| LINREG     | linreg     | Linear Regression              |
| AROON      | aroon      | Aroon Indicator                |

#### 2. **Momentum Indicators** (Chỉ báo Động Lực)
| Chỉ báo  | Ký hiệu  | Mô tả                                 |
| -------- | -------- | ------------------------------------- |
| RSI      | rsi      | Relative Strength Index               |
| STOCH    | stoch    | Stochastic Oscillator                 |
| STOCHRSI | stochrsi | Stochastic RSI                        |
| ROC      | roc      | Rate of Change                        |
| AO       | ao       | Awesome Oscillator                    |
| CCI      | cci      | Commodity Channel Index               |
| WILLR    | willr    | Williams %R                           |
| TSI      | tsi      | True Strength Index                   |
| CMO      | cmo      | Chande Momentum Oscillator            |
| UO       | uo       | Ultimate Oscillator                   |
| FISHER   | fisher   | Fisher Transform                      |
| CG       | cg       | Center of Gravity                     |
| KST      | kst      | Know Sure Thing                       |
| MACD     | macd     | Moving Average Convergence Divergence |

#### 3. **Volatility Indicators** (Chỉ báo Biến Động)
| Chỉ báo     | Ký hiệu     | Mô tả                |
| ----------- | ----------- | -------------------- |
| BBANDS      | bbands      | Bollinger Bands      |
| KC          | kc          | Keltner Channels     |
| ATR         | atr         | Average True Range   |
| STDEV       | stdev       | Standard Deviation   |
| DONCHIAN    | donchian    | Donchian Channels    |
| MASSI       | massi       | Mass Index           |
| UI          | ui          | Ulcer Index          |
| SQUEEZE     | squeeze     | Squeeze Momentum     |
| SQUEEZE_PRO | squeeze_pro | Squeeze Momentum Pro |
| TRUE_RANGE  | true_range  | True Range           |

#### 4. **Volume Indicators** (Chỉ báo Khối Lượng)
| Chỉ báo | Ký hiệu | Mô tả                         |
| ------- | ------- | ----------------------------- |
| OBV     | obv     | On-Balance Volume             |
| CMF     | cmf     | Chaikin Money Flow            |
| AD      | ad      | Accumulation/Distribution     |
| VP      | vp      | Volume Profile                |
| VWAP    | vwap    | Volume Weighted Average Price |
| PVO     | pvo     | Percentage Volume Oscillator  |
| EFI     | efi     | Force Index                   |
| EOM     | eom     | Ease of Movement              |
| NVI     | nvi     | Negative Volume Index         |
| MFI     | mfi     | Money Flow Index              |

#### 5. **Statistics Indicators** (Chỉ báo Thống Kê & Cấu Trúc)
| Chỉ báo    | Ký hiệu    | Mô tả                       |
| ---------- | ---------- | --------------------------- |
| PIVOTS     | pivots     | Pivot Points                |
| MAD        | mad        | Mean Absolute Deviation     |
| VARIANCE   | variance   | Variance                    |
| HL2        | hl2        | High-Low Average            |
| HLC3       | hlc3       | High-Low-Close Average      |
| OHLC4      | ohlc4      | Open-High-Low-Close Average |
| MIDPRICE   | midprice   | Midprice                    |
| DECREASING | decreasing | Decreasing Series           |
| INCREASING | increasing | Increasing Series           |

### Cách Sử Dụng Cơ Bản

#### 1. Lấy Dữ Liệu

Dữ liệu đầu vào cần có index là `time` và các cột `open, high, low, close, volume`.
Bạn có thể lấy dữ liệu trực tiếp từ `vnstock_data`:

```python
from vnstock_data import Quote

quote = Quote(source="vnd", symbol="VCB")
df = quote.history(start="2024-09-01", end="2024-12-02", interval="1D")
df = df.set_index('time')
```

#### 2. Tính Chỉ Báo

Khởi tạo object `Indicator` và gọi các method chỉ báo. Các chỉ báo được gom nhóm theo danh mục.

```python
from vnstock_ta import Indicator

# Khởi tạo
ta = Indicator(data=df)

# Cách 1: Gọi qua danh mục (Khuyến nghị)
sma = ta.trend.sma(length=20)
rsi = ta.momentum.rsi(length=14)
atr = ta.volatility.atr(length=14)
obv = ta.volume.obv()
hlc3 = ta.statistics.hlc3()

# Cách 2: Gọi trực tiếp (Backward compatibility)
macd = ta.macd(fast=12, slow=26, signal=9) 
```

#### 3. Vẽ Biểu Đồ

> **Lưu ý Quan Trọng**: Lớp `Plotter` và module `vnstock_ta.chart` đã bị deprecated và sẽ bị loại bỏ vào ngày 31/08/2026. Bạn nên chuyển sang sử dụng thư viện `vnstock_ezchart` để vẽ biểu đồ chuyên nghiệp.

```python
from vnstock_ezchart import Chart

# Vẽ biểu đồ nến với chỉ báo
Chart.candle(df, title="Biểu đồ với SMA và RSI")
```

### Yêu Cầu Dữ Liệu

DataFrame phải đáp ứng các yêu cầu:
1. **Index**: Tốt nhất là `DatetimeIndex` (tên `'time'`)
2. **Cột bắt buộc**: `'open'`, `'high'`, `'low'`, `'close'` (tất cả là float), `'volume'` (int)

### Cấu Trúc Tài Liệu

Tài liệu được chia thành các phần chính:
1. **01-overview.md** (Tệp này) - Giới thiệu, cấu trúc, cách sử dụng cơ bản
2. **02-indicators.md** - Danh sách toàn bộ các chỉ báo kỹ thuật và tham số
3. **03-plotting.md** - Hướng dẫn vẽ biểu đồ bằng `vnstock_ezchart`
4. **04-best-practices.md** - Best practices, tips & tricks

### Dependencies
- **pandas**: Xử lý DataFrame
- **pta-reload**: Động cơ tính toán chỉ báo kỹ thuật (Backend)
- **vnstock_data**: Lấy dữ liệu thị trường (Tùy chọn)
- **vnstock_ezchart**: Thư viện đồ thị (Tùy chọn)

### Lưu Ý Quan Trọng
1. **Index**: Hầu hết chỉ báo cần index liên tục.
2. **Giá trị NaN ban đầu**: Các chỉ báo có period lớn sẽ có NaN ở đầu dữ liệu.
3. **Miễn Trừ Trách Nhiệm**: Thư viện chỉ cung cấp công cụ tính toán, không chịu trách nhiệm về kết quả giao dịch.
