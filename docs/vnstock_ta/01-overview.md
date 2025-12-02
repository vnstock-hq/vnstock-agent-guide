# Vnstock TA - Thư Viện Phân Tích Kỹ Thuật

## Giới Thiệu

`vnstock_ta` (Vnstock Technical Analysis) là thư viện Python chuyên dụng cung cấp các chỉ báo kỹ thuật (Technical Indicators) và công cụ vẽ biểu đồ (Plotting) cho phân tích dữ liệu thị trường chứng khoán. Thư viện được thiết kế để tích hợp liền mạch với `vnstock_data`, cung cấp quy trình hoàn chỉnh từ lấy dữ liệu đến phân tích kỹ thuật.

### Đặc Điểm Chính

- **Chỉ báo phong phú**: 25+ chỉ báo kỹ thuật được phân loại theo 4 danh mục (Trend, Momentum, Volatility, Volume)
- **API thống nhất**: Giao diện đơn giản, dễ sử dụng cho cả chỉ báo và biểu đồ
- **Tích hợp pandas**: Hoạt động trực tiếp với DataFrame, output là Series hoặc DataFrame
- **Biểu đồ tương tác**: Hỗ trợ vẽ biểu đồ với theme sáng/tối và các tùy chọn tùy biến chuyên nghiệp trong Python.
- **Tài liệu đầy đủ**: Mỗi chỉ báo có tài liệu mô tả chi tiết.

### Cấu Trúc Package

```
vnstock_ta/
├── __init__.py          # Export Indicator, Plotter, DataSource
├── interface.py         # Indicator và Plotter classes chính
├── get_data.py          # DataSource - lấy dữ liệu từ vnstock_data
├── indicators/          # Chỉ báo kỹ thuật
│   ├── __init__.py
│   ├── trend.py        # SMA, EMA, VWAP, VWMA, ADX, AROON, PSAR, SUPERTREND
│   ├── momentum.py      # RSI, MACD, WILLR, CMO, STOCH, ROC, MOM
│   ├── volatility.py    # BBANDS, KC, ATR, STDEV, LINREG
│   ├── volume.py        # OBV
│   └── docs.py         # Tài liệu cho tất cả chỉ báo
├── chart/               # Vẽ biểu đồ
│   ├── __init__.py
│   ├── core.py         # TAChart - base class
│   ├── trend.py        # TATrend - vẽ chỉ báo Trend
│   ├── momentum.py      # TAMomentum - vẽ chỉ báo Momentum
│   ├── volatility.py    # TAVolatility - vẽ chỉ báo Volatility
│   └── volume.py        # TAVolume - vẽ chỉ báo Volume
└── utils/               # Utilities
    ├── __init__.py
    ├── const.py        # Màu sắc, palettes, constants
    └── env.py          # Biến môi trường
```

### Các Loại Chỉ Báo

#### 1. **Trend Indicators** (Chỉ báo Xu Hướng)

| Chỉ báo | Ký hiệu | Mô tả | Output |
|---------|---------|-------|--------|
| Simple Moving Average | SMA | Trung bình di động đơn giản | Series |
| Exponential Moving Average | EMA | Trung bình di động hàm mũ | Series |
| Volume Weighted Average Price | VWAP | Giá trung bình có trọng số khối lượng | Series |
| Volume Weighted Moving Average | VWMA | Trung bình di động có trọng số khối lượng | Series |
| Average Directional Index | ADX | Chỉ số đo cường độ xu hướng | DataFrame (3 cột) |
| Aroon & Aroon Oscillator | AROON | Chỉ số đo vị trí cao/thấp | DataFrame (3 cột) |
| Parabolic Stop and Reverse | PSAR | Điểm dừng động | DataFrame (4 cột) |
| Supertrend | SUPERTREND | Xu hướng & điểm dừng | DataFrame (4 cột) |

#### 2. **Momentum Indicators** (Chỉ báo Động Lực)

| Chỉ báo | Ký hiệu | Mô tả | Output |
|---------|---------|-------|--------|
| Relative Strength Index | RSI | Đo cường độ mua/bán | Series (0-100) |
| MACD | MACD | Sự hội tụ/phân kỳ trung bình di động | DataFrame (3 cột) |
| Williams %R | WILLR | Chỉ báo mua/bán | Series (-100 to 0) |
| Chande Momentum Oscillator | CMO | Dao động động lực | Series (-100 to 100) |
| Stochastic Oscillator | STOCH | Chỉ báo mua/bán nhanh | DataFrame (2 cột) |
| Rate of Change | ROC | Tỷ lệ thay đổi giá | Series (%) |
| Momentum | MOM | Động lực giá | Series |

#### 3. **Volatility Indicators** (Chỉ báo Biến Động)

| Chỉ báo | Ký hiệu | Mô tả | Output |
|---------|---------|-------|--------|
| Bollinger Bands | BBANDS | Dải bao quanh giá | DataFrame (5 cột) |
| Keltner Channels | KC | Kênh xung quanh EMA | DataFrame (3 cột) |
| Average True Range | ATR | Phạm vi thực trung bình | Series |
| Standard Deviation | STDEV | Độ lệch chuẩn | Series |
| Linear Regression | LINREG | Đường hồi quy tuyến tính | Series |

#### 4. **Volume Indicators** (Chỉ báo Khối Lượng)

| Chỉ báo | Ký hiệu | Mô tả | Output |
|---------|---------|-------|--------|
| On Balance Volume | OBV | Khối lượng cân bằng | Series |

### Cách Sử Dụng Cơ Bản

#### 1. Lấy Dữ Liệu

Sử dụng `DataSource` để lấy dữ liệu với index là thời gian:

```python
from vnstock_ta import DataSource

# Lấy dữ liệu từ vnstock_data
data_source = DataSource(
    symbol='VCB',
    start='2024-09-01',
    end='2024-12-02',
    interval='1D',
    source='vnd'
)

df = data_source.data  # DataFrame với index là 'time'
```

**Output DataFrame:**
```
                  open    high     low   close   volume
time                                                    
2024-09-04   60.498  60.498  59.967  60.432  1012700
2024-09-05   60.166  60.498  59.834  59.834  1184100
...
2024-12-02   63.022  63.154  62.357  62.557  1573100
```

#### 2. Tính Chỉ Báo

Khởi tạo object `Indicator` và gọi các method chỉ báo:

```python
from vnstock_ta import Indicator

# Khởi tạo
indicator = Indicator(data=df)

# Tính SMA
sma = indicator.sma(length=20)  # Returns: pd.Series with name 'SMA_20'

# Tính MACD
macd = indicator.macd(fast=12, slow=26, signal=9)  # Returns: pd.DataFrame

# Tính RSI
rsi = indicator.rsi(length=14)  # Returns: pd.Series
```

#### 3. Vẽ Biểu Đồ

Khởi tạo object `Plotter` để vẽ biểu đồ tương tác:

```python
from vnstock_ta import Plotter

# Khởi tạo với theme sáng
plotter = Plotter(data=df, theme='light', watermark=False)

# Vẽ SMA
plotter.sma(length=20, title='SMA 20', legend=True)

# Vẽ RSI
plotter.rsi(length=14, title='RSI 14')
```

### Yêu Cầu Dữ Liệu

DataFrame phải có các yêu cầu sau:

1. **Index**: Phải là `DatetimeIndex` với tên là `'time'`
2. **Cột bắt buộc**:
   - `'close'`: Giá đóng (float)
   - `'open'`: Giá mở (float)
   - `'high'`: Giá cao (float)
   - `'low'`: Giá thấp (float)
   - `'volume'`: Khối lượng giao dịch (int)

**Ví dụ đặt đúng format:**

```python
from vnstock_data import Quote

# Lấy dữ liệu
quote = Quote(source="vnd", symbol="VCB")
df = quote.history(start="2024-09-01", end="2024-12-02", interval="1D")

# Đặt index là 'time'
df = df.set_index('time')

# Bây giờ có thể dùng với vnstock_ta
indicator = Indicator(data=df)
```

### Cài Đặt & Import

```python
# Import từ package chính
from vnstock_ta import Indicator, Plotter, DataSource

# Hoặc import từ module riêng
from vnstock_ta.interface import Indicator, Plotter
from vnstock_ta.get_data import DataSource
```

### Cấu Trúc Tài Liệu

Tài liệu được chia thành các phần chính:

1. **01-overview.md** (Tệp này) - Giới thiệu, cấu trúc, cách sử dụng cơ bản
2. **02-indicators.md** - Chi tiết từng chỉ báo với ví dụ và output
3. **03-plotting.md** - Hướng dẫn vẽ biểu đồ, tùy chỉnh theme
4. **04-best-practices.md** - Best practices, pattern phổ biến, tips & tricks

Mỗi phần bao gồm:
- **Chi tiết**: Giải thích chỉ báo, tham số
- **Ví dụ**: Code thực tế với output
- **Output**: Kiểu dữ liệu, cột, giá trị
- **Tips**: Khi nào sử dụng, cách sử dụng tối ưu

### Dependencies

- **pandas**: Xử lý DataFrame
- **pandas-ta** (pTA): Tính toán chỉ báo kỹ thuật
- **pyecharts**: Vẽ biểu đồ tương tác
- **vnstock_data**: Lấy dữ liệu thị trường

### Lưu Ý Quan Trọng

1. **Index phải là datetime**: Hầu hết chỉ báo yêu cầu index là DatetimeIndex
2. **Giá trị NaN ban đầu**: Các chỉ báo có period lớn sẽ có NaN ở đầu dữ liệu (ví dụ: SMA với length=20 sẽ có 19 NaN ở đầu)
3. **Tên cột output**: Output tự động đặt tên dựa vào tham số (ví dụ: `RSI_14`, `SMA_20`, `MACD_12_26_9`)
4. **Theme cho biểu đồ**: 'light' (mặc định) hoặc 'dark', ảnh hưởng đến palette màu
5. **Watermark**: Có thể bật/tắt bằng tham số `watermark=True/False`

### Miễn Trừ Trách Nhiệm

- Vnstock_ta chỉ cung cấp wrapper tính toán chỉ báo tiêu chuẩn
- **Không nên** dựa vào một chỉ báo duy nhất để quyết định giao dịch
- Nên kết hợp nhiều chỉ báo và phân tích cơ bản trước khi quyết định
- Tác giả thư viện không chịu trách nhiệm về tổn thất từ việc sử dụng thư viện này. Bạn phải tự chịu trách nhiệm về quyết định giao dịch của mình.
