# Vnstock TA - Chi Tiết Chỉ Báo Kỹ Thuật

## Giới Thiệu

Chương này cung cấp chi tiết cho tất cả 25+ chỉ báo trong vnstock_ta, được chia thành 4 danh mục chính. Mỗi chỉ báo bao gồm:
- **Mô tả**: Khái niệm, ứng dụng
- **Tham số**: Các tham số có thể điều chỉnh
- **Output**: Kiểu dữ liệu, cột, phạm vi giá trị
- **Ví dụ**: Code thực tế với output xác thực
- **Cách sử dụng**: Best practices khi nào dùng

---

## I. TREND INDICATORS (Chỉ Báo Xu Hướng)

### 1. SMA - Simple Moving Average

**Mô tả**: Trung bình cộng đơn giản của giá đóng trong N kỳ. Dùng để làm mượt dữ liệu và xác định xu hướng chung.

**Tham số**:
- `length` (int): Số kỳ để tính SMA. Mặc định: 14

**Output**: 
- **Kiểu**: `pd.Series` 
- **Tên**: `SMA_{length}` (ví dụ: `SMA_20`)
- **Giá trị**: Float, cùng đơn vị với giá đóng
- **NaN**: Có NaN ở đầu (length-1 giá trị)

**Ví dụ**:

```python
from vnstock_data import Quote
from vnstock_ta import Indicator

# Lấy dữ liệu
quote = Quote(source="vnd", symbol="VCB")
df = quote.history(start="2024-09-01", end="2024-12-02", interval="1D")
df = df.set_index('time')

# Tính SMA
indicator = Indicator(data=df)
sma = indicator.sma(length=20)

print(sma.tail())
```

**Output**:
```
time
2024-11-26    61.04265
2024-11-27    61.07590
2024-11-28    61.04270
2024-11-29    61.03605
2024-12-02    61.09250
Name: SMA_20, dtype: float64
```

**Cách sử dụng**:
- SMA 50 & 200 để xác định xu hướng dài hạn
- SMA 20 để xác định xu hướng ngắn hạn
- Khi giá > SMA: Xu hướng tăng
- Khi giá < SMA: Xu hướng giảm
- Golden Cross: SMA ngắn cắt lên SMA dài → Tín hiệu mua

---

### 2. EMA - Exponential Moving Average

**Mô tả**: Trung bình di động có trọng số hàm mũ, trọng số lớn hơn cho dữ liệu gần đây hơn SMA. Phản ứng nhanh hơn SMA với thay đổi giá.

**Tham số**:
- `length` (int): Số kỳ để tính EMA. Mặc định: 14

**Output**: 
- **Kiểu**: `pd.Series`
- **Tên**: `EMA_{length}`
- **Giá trị**: Float
- **NaN**: Có NaN ở đầu (length-1 giá trị) nhưng ít hơn SMA

**Ví dụ**:

```python
ema = indicator.ema(length=12)
print(ema.tail())
```

**Output**:
```
time
2024-11-26    60.711016
2024-11-27    60.841782
2024-11-28    60.942124
2024-11-29    61.098566
2024-12-02    61.322941
Name: EMA_12, dtype: float64
```

**Cách sử dụng**:
- EMA 12 & 26 thường dùng trong MACD
- EMA phản ứng nhanh hơn SMA, phù hợp cho giao dịch ngắn hạn
- Giá vượt EMA từ dưới lên: Tín hiệu mua
- Giá thủng EMA từ trên xuống: Tín hiệu bán

---

### 3. VWAP - Volume Weighted Average Price

**Mô tả**: Giá trung bình có trọng số theo khối lượng giao dịch. Chỉ báo quan trọng dùng trong intraday trading.

**Tham số**:
- `anchor` (str): Khoảng thời gian để reset VWAP. Mặc định: 'D' (hàng ngày)
  - 'D': Daily (reset mỗi ngày)
  - 'W': Weekly (reset mỗi tuần)
  - 'M': Monthly (reset mỗi tháng)

**Output**: 
- **Kiểu**: `pd.Series`
- **Tên**: `VWAP_{anchor}`
- **Giá trị**: Float
- **NaN**: Không có NaN (tất cả giá trị có sẵn)

**Ví dụ**:

```python
vwap = indicator.vwap(anchor='D')
print(vwap.tail())
```

**Output**:
```
time
2024-11-26    61.250333
2024-11-27    61.583000
2024-11-28    61.671333
2024-11-29    61.782000
2024-12-02    62.689333
Name: VWAP_D, dtype: float64
```

**Cách sử dụng**:
- Dùng cho intraday trading
- Giá > VWAP: Khối lượng mua vượt bán
- Giá < VWAP: Khối lượng bán vượt mua
- VWAP là level hỗ trợ/kháng cự động

---

### 4. VWMA - Volume Weighted Moving Average

**Mô tả**: Trung bình di động có trọng số theo khối lượng. Phối hợp khối lượng vào SMA.

**Tham số**:
- `length` (int): Số kỳ. Mặc định: 20

**Output**: 
- **Kiểu**: `pd.Series`
- **Tên**: `VWMA_{length}`
- **Giá trị**: Float
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
vwma = indicator.vwma(length=20)
print(vwma.tail())
```

**Output**:
```
time
2024-11-26    61.073848
2024-11-27    61.093005
2024-11-28    61.010031
2024-11-29    60.979734
2024-12-02    61.035027
Name: VWMA_20, dtype: float64
```

---

### 5. ADX - Average Directional Index

**Mô tả**: Đo cường độ xu hướng (0-100). Không chỉ hướng mà chỉ độ mạnh. ADX > 25 = xu hướng mạnh, ADX < 20 = range.

**Tham số**:
- `length` (int): Số kỳ. Mặc định: 14

**Output**: 
- **Kiểu**: `pd.DataFrame` (3 cột)
- **Cột**: 
  - `ADX_{length}`: Chỉ số ADX (0-100)
  - `DMP_{length}`: Directional Movement Plus (động lực tăng)
  - `DMN_{length}`: Directional Movement Minus (động lực giảm)
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
adx = indicator.adx(length=14)
print(adx.tail())
```

**Output**:
```
           ADX_14     DMP_14     DMN_14
time                                   
2024-11-26  21.155068  21.387804  16.548436
2024-11-27  20.846265  22.043203  15.648889
2024-11-28  20.860897  22.526996  14.693783
2024-11-29  20.874425  21.402043  13.960004
2024-12-02  22.361214  29.887667  12.452849
```

**Cách sử dụng**:
- ADX > 25: Xu hướng mạnh (nên theo xu hướng)
- ADX 20-25: Xu hướng trung bình
- ADX < 20: Range (nên giao dịch trong range)
- DMP > DMN: Xu hướng tăng
- DMN > DMP: Xu hướng giảm

---

### 6. AROON - Aroon & Aroon Oscillator

**Mô tả**: Chỉ báo đo vị trí của cao/thấp gần nhất. Aroon > 50 = có xu hướng.

**Tham số**:
- `length` (int): Số kỳ. Mặc định: 14

**Output**: 
- **Kiểu**: `pd.DataFrame` (3 cột)
- **Cột**:
  - `AROONU_{length}`: Aroon Up (0-100)
  - `AROOND_{length}`: Aroon Down (0-100)
  - `AROONOSC_{length}`: Aroon Oscillator (-100 to 100)
- **Giá trị**: 0-100 cho Up/Down, -100 to 100 cho Oscillator
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
aroon = indicator.aroon(length=14)
print(aroon.tail())
```

**Output**:
```
            AROOND_14   AROONU_14  AROONOSC_14
time                                          
2024-11-26  71.428571   14.285714   -57.142857
2024-11-27  64.285714    7.142857   -57.142857
2024-11-28  57.142857    0.000000   -57.142857
2024-11-29  50.000000   92.857143    42.857143
2024-12-02  42.857714  100.000000    57.142857
```

**Cách sử dụng**:
- Aroon Up > 50 & Aroon Down < 50: Xu hướng tăng
- Aroon Down > 50 & Aroon Up < 50: Xu hướng giảm
- Oscillator > 0: Ưu thế tăng
- Oscillator < 0: Ưu thế giảm

---

### 7. PSAR - Parabolic Stop and Reverse

**Mô tả**: Chỉ báo dừng động sử dụng để xác định điểm dừng lỗ. Theo xu hướng từ từ dừng lỗ cao dần.

**Tham số**:
- `af0` (float): Initial Acceleration Factor. Mặc định: 0.02
- `af` (float): Acceleration Factor. Mặc định: 0.02
- `max_af` (float): Maximum Acceleration Factor. Mặc định: 0.2

**Output**: 
- **Kiểu**: `pd.DataFrame` (4 cột)
- **Cột**:
  - `PSARl_{af0}_{max_af}`: SAR (điểm dừng lỗ)
  - `PSARs_{af0}_{max_af}`: SAR (khi đảo chiều)
  - `PSARaf_{af0}_{max_af}`: Acceleration Factor
  - `PSARr_{af0}_{max_af}`: Reversal (0/1)
- **NaN**: PSARl/s có NaN khi không có giá trị

**Ví dụ**:

```python
psar = indicator.psar()
print(psar.tail())
```

**Output**:
```
            PSARl_0.02_0.2  PSARs_0.02_0.2  PSARaf_0.02_0.2  PSARr_0.02_0.2
time                                                                       
2024-11-26       59.701000             NaN             0.02               1
2024-11-27       59.740840             NaN             0.04               0
2024-11-28       59.826926             NaN             0.06               0
2024-11-29       59.962831             NaN             0.06               0
2024-12-02       60.090581             NaN             0.08               0
```

**Cách sử dụng**:
- Dùng làm stop loss tự động
- PSARr = 1: Đảo chiều (đổi hướng)
- Giá xuyên qua PSAR: Có thể là tín hiệu dừng lỗ

---

### 8. SUPERTREND - Supertrend

**Mô tả**: Kết hợp ATR và moving average để xác định xu hướng và điểm dừng lỗ. Dùng phổ biến cho swing trading.

**Tham số**:
- `length` (int): Kỳ cho ATR. Mặc định: 10
- `multiplier` (float): Hệ số nhân với ATR. Mặc định: 3

**Output**: 
- **Kiểu**: `pd.DataFrame` (4 cột)
- **Cột**:
  - `SUPERT_{length}_{multiplier}`: Giá Supertrend
  - `SUPERTd_{length}_{multiplier}`: Direction (-1=down, 1=up)
  - `SUPERTl_{length}_{multiplier}`: Lower band
  - `SUPERTs_{length}_{multiplier}`: Upper band
- **NaN**: l/s có NaN khi không cần thiết

**Ví dụ**:

```python
supertrend = indicator.supertrend(length=10, multiplier=3)
print(supertrend.tail())
```

**Output**:
```
            SUPERT_10_3.0  SUPERTd_10_3.0  SUPERTl_10_3.0  SUPERTs_10_3.0
time                                                                     
2024-11-26      62.546202              -1             NaN       62.546202
2024-11-27      62.546202              -1             NaN       62.546202
2024-11-28      62.546202              -1             NaN       62.546202
2024-11-29      62.546202              -1             NaN       62.546202
2024-12-02      60.335578               1       60.335578             NaN
```

**Cách sử dụng**:
- SUPERTd = 1: Xu hướng tăng, dùng SUPERTl làm support
- SUPERTd = -1: Xu hướng giảm, dùng SUPERTs làm resistance
- Đảo chiều của direction: Tín hiệu dừng lỗ

---

## II. MOMENTUM INDICATORS (Chỉ Báo Động Lực)

### 1. RSI - Relative Strength Index

**Mô tả**: Chỉ báo mua bán quá mức. RSI > 70 = overbought, RSI < 30 = oversold. Phạm vi 0-100.

**Tham số**:
- `length` (int): Số kỳ. Mặc định: 14

**Output**: 
- **Kiểu**: `pd.Series`
- **Tên**: `RSI_{length}`
- **Giá trị**: 0-100 (nên sử dụng 0-100)
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
rsi = indicator.rsi(length=14)
print(rsi.tail())
```

**Output**:
```
time
2024-11-26    55.991046
2024-11-27    57.988177
2024-11-28    57.054102
2024-11-29    61.668936
2024-12-02    66.634464
Name: RSI_14, dtype: float64
```

**Cách sử dụng**:
- RSI > 70: Overbought (có thể bán)
- RSI < 30: Oversold (có thể mua)
- RSI 40-60: Trung tính
- Divergence: RSI không tạo high/low mới trong khi giá tạo = tín hiệu đảo chiều

---

### 2. MACD - Moving Average Convergence Divergence

**Mô tả**: Kết hợp EMA ngắn/dài để xác định xu hướng. Gồm MACD line, Signal line, và Histogram.

**Tham số**:
- `fast` (int): EMA ngắn. Mặc định: 12
- `slow` (int): EMA dài. Mặc định: 26
- `signal` (int): EMA signal. Mặc định: 9

**Output**: 
- **Kiểu**: `pd.DataFrame` (3 cột)
- **Cột**:
  - `MACD_{fast}_{slow}_{signal}`: MACD line
  - `MACDs_{fast}_{slow}_{signal}`: Signal line
  - `MACDh_{fast}_{slow}_{signal}`: Histogram (MACD - Signal)
- **Giá trị**: Float (có thể âm/dương)
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
macd = indicator.macd(fast=12, slow=26, signal=9)
print(macd.tail())
```

**Output**:
```
            MACD_12_26_9  MACDh_12_26_9  MACDs_12_26_9
time                                                  
2024-11-26     -0.123636      -0.042217      -0.081420
2024-11-27     -0.046673       0.027797      -0.074470
2024-11-28      0.008813       0.066627      -0.057814
2024-11-29      0.089279       0.117674      -0.028395
2024-12-02      0.199008       0.181922       0.017085
```

**Cách sử dụng**:
- MACD vượt Signal từ dưới lên: Tín hiệu mua (bullish crossover)
- MACD xuyên Signal từ trên xuống: Tín hiệu bán (bearish crossover)
- Histogram > 0 & tăng: Xu hướng tăng mạnh
- Histogram < 0 & giảm: Xu hướng giảm mạnh
- Divergence: MACD không tạo low/high mới = tín hiệu đảo chiều

---

### 3. WILLR - Williams %R

**Mô tả**: Chỉ báo mua bán tương tự RSI. Phạm vi -100 to 0. Còn gọi là Williams R.

**Tham số**:
- `length` (int): Số kỳ. Mặc định: 14

**Output**: 
- **Kiểu**: `pd.Series`
- **Tên**: `WILLR_{length}`
- **Giá trị**: -100 to 0
  - -20 to 0: Overbought
  - -50: Trung tính
  - -100 to -80: Oversold
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
willr = indicator.willr(length=14)
print(willr.tail())
```

**Output**:
```
time
2024-11-26   -37.500000
2024-11-27   -29.969880
2024-11-28   -25.010456
2024-11-29    -5.562526
2024-12-02   -17.289314
Name: WILLR_14, dtype: float64
```

---

### 4. CMO - Chande Momentum Oscillator

**Mô tả**: Chỉ báo động lực lựa chọn giữa mua và bán. Phạm vi -100 to 100.

**Tham số**:
- `length` (int): Số kỳ. Mặc định: 9

**Output**: 
- **Kiểu**: `pd.Series`
- **Tên**: `CMO_{length}`
- **Giá trị**: -100 to 100
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
cmo = indicator.cmo(length=9)
print(cmo.tail())
```

**Output**:
```
time
2024-11-26    -2.059637
2024-11-27    14.899071
2024-11-28    20.013387
2024-11-29    51.087320
2024-12-02    95.415669
Name: CMO_9, dtype: float64
```

**Cách sử dụng**:
- CMO > 50: Overbought
- CMO < -50: Oversold
- Cao CMO: Động lực mạnh
- Thấp CMO: Động lực yếu

---

### 5. STOCH - Stochastic Oscillator

**Mô tả**: Chỉ báo so sánh giá đóng với phạm vi cao/thấp. Gồm %K (nhanh) và %D (chậm).

**Tham số**:
- `k` (int): Kỳ %K. Mặc định: 14
- `d` (int): Kỳ %D. Mặc định: 3
- `smooth_k` (int): Làm mượt %K. Mặc định: 3

**Output**: 
- **Kiểu**: `pd.DataFrame` (2 cột)
- **Cột**:
  - `STOCHk_{k}_{d}_{smooth_k}`: %K line (0-100)
  - `STOCHd_{k}_{d}_{smooth_k}`: %D line (0-100)
- **Giá trị**: 0-100
  - > 80: Overbought
  - < 20: Oversold
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
stoch = indicator.stoch(k=14, d=3, smooth_k=3)
print(stoch.tail())
```

**Output**:
```
            STOCHk_14_3_3  STOCHd_14_3_3
time                                    
2024-11-26      38.340863      23.858184
2024-11-27      55.848394      38.468552
2024-11-28      69.173222      54.454160
2024-11-29      79.819046      68.280220
2024-12-02      84.045901      77.679390
```

**Cách sử dụng**:
- %K vượt %D từ dưới lên & < 50: Tín hiệu mua
- %K xuyên %D từ trên xuống & > 50: Tín hiệu bán
- %K & %D > 80: Overbought
- %K & %D < 20: Oversold

---

### 6. ROC - Rate of Change

**Mô tả**: Tỷ lệ thay đổi giá theo phần trăm. ROC = (Close - Close[n]) / Close[n] * 100

**Tham số**:
- `length` (int): Số kỳ để so sánh. Mặc định: 9

**Output**: 
- **Kiểu**: `pd.Series`
- **Tên**: `ROC_{length}`
- **Giá trị**: Phần trăm (%)
  - > 0: Tăng
  - < 0: Giảm
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
roc = indicator.roc(length=9)
print(roc.tail())
```

**Output**:
```
time
2024-11-26   -0.109071
2024-11-27    0.761097
2024-11-28    0.982002
2024-11-29    2.526807
2024-12-02    4.666377
Name: ROC_9, dtype: float64
```

**Cách sử dụng**:
- Dùng để đo tốc độ thay đổi giá
- ROC > 0: Giá tăng so với N kỳ trước
- ROC < 0: Giá giảm so với N kỳ trước
- ROC cao: Động lực mạnh

---

### 7. MOM - Momentum

**Mô tả**: Động lực giá đơn giản. MOM = Close - Close[n]

**Tham số**:
- `length` (int): Số kỳ. Mặc định: 10

**Output**: 
- **Kiểu**: `pd.Series`
- **Tên**: `MOM_{length}`
- **Giá trị**: Float (đơn vị giống giá)
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
mom = indicator.mom(length=10)
print(mom.tail())
```

**Output**:
```
time
2024-11-26    0.332
2024-11-27    0.133
2024-11-28    0.398
2024-11-29    1.063
2024-12-02    2.125
Name: MOM_10, dtype: float64
```

---

## III. VOLATILITY INDICATORS (Chỉ Báo Biến Động)

### 1. BBANDS - Bollinger Bands

**Mô tả**: Dải bao quanh SMA với độ lệch chuẩn. Dùng để xác định mức overbought/oversold.

**Tham số**:
- `length` (int): Số kỳ cho SMA. Mặc định: 14
- `std` (float): Số độ lệch chuẩn. Mặc định: 2

**Output**: 
- **Kiểu**: `pd.DataFrame` (5 cột)
- **Cột**:
  - `BBL_{length}_{std}`: Lower band
  - `BBM_{length}_{std}`: Middle (SMA)
  - `BBU_{length}_{std}`: Upper band
  - `BBB_{length}_{std}`: Bandwidth (BBU - BBL)
  - `BBP_{length}_{std}`: Percent B (vị trí giá trong dải)
- **Giá trị**: Float (cùng đơn vị giá)
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
bbands = indicator.bbands(length=14, std=2)
print(bbands.tail())
```

**Output**:
```
            BBL_14_2.0  BBM_14_2.0  BBU_14_2.0  BBB_14_2.0  BBP_14_2.0
time                                                                  
2024-11-26   59.580592   60.792286   62.003979    3.986340    0.734677
2024-11-27   59.633396   60.768571   61.903747    3.736061    0.849034
2024-11-28   59.614054   60.787500   61.960946    3.860815    0.801036
2024-11-29   59.535102   60.849143   62.163183    4.319011    0.922307
2024-12-02   59.376143   60.958286   62.540429    5.190904    1.005237
```

**Cách sử dụng**:
- Giá chạm BBU: Overbought (có thể bán)
- Giá chạm BBL: Oversold (có thể mua)
- Dải rộng (BBB cao): Biến động cao
- Dải hẹp (BBB thấp): Biến động thấp, sắp xảy ra breakout
- BBP: 0 = tại BBL, 1 = tại BBU, 0.5 = tại BBM

---

### 2. KC - Keltner Channels

**Mô tả**: Tương tự Bollinger Bands nhưng dùng ATR thay vì độ lệch chuẩn. Phù hợp hơn cho các loại tài sản khác nhau.

**Tham số**:
- `length` (int): Số kỳ. Mặc định: 20
- `scalar` (float): Hệ số nhân ATR. Mặc định: 2.0
- `mamode` (str): Loại moving average. Mặc định: 'ema'

**Output**: 
- **Kiểu**: `pd.DataFrame` (3 cột)
- **Cột**:
  - `KCLe_{length}_{scalar}`: Lower band
  - `KCBe_{length}_{scalar}`: Basis (middle)
  - `KCUe_{length}_{scalar}`: Upper band
- **Giá trị**: Float
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
kc = indicator.kc(length=20, scalar=2.0, mamode='ema')
print(kc.tail())
```

**Output**:
```
            KCLe_20_2.0  KCBe_20_2.0  KCUe_20_2.0
time                                             
2024-11-26    59.162780    60.810633    62.458486
2024-11-27    59.277277    60.882097    62.486916
2024-11-28    59.361918    60.940373    62.518829
2024-11-29    59.508116    61.037385    62.566654
2024-12-02    59.570867    61.182110    62.793354
```

**Cách sử dụng**:
- Tương tự Bollinger Bands
- Phù hợp hơn cho thị trường có ATR biến động

---

### 3. ATR - Average True Range

**Mô tả**: Đo phạm vi giao dịch trung bình. ATR cao = biến động cao, ATR thấp = biến động thấp.

**Tham số**:
- `length` (int): Số kỳ. Mặc định: 14

**Output**: 
- **Kiểu**: `pd.Series`
- **Tên**: `ATRr_{length}`
- **Giá trị**: Float (cùng đơn vị giá)
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
atr = indicator.atr(length=14)
print(atr.tail())
```

**Output**:
```
time
2024-11-26    0.810465
2024-11-27    0.795109
2024-11-28    0.785641
2024-11-29    0.767266
2024-12-02    0.798108
Name: ATRr_14, dtype: float64
```

**Cách sử dụng**:
- ATR cao: Biến động cao, cần stop loss xa hơn
- ATR thấp: Biến động thấp, sắp xảy ra breakout
- Stop loss = Entry - (ATR * 2)
- Target = Entry + (ATR * 3)

---

### 4. STDEV - Standard Deviation

**Mô tả**: Độ lệch chuẩn của giá. Dùng để đo volatility.

**Tham số**:
- `length` (int): Số kỳ. Mặc định: 14
- `ddof` (int): Delta degrees of freedom. Mặc định: 1

**Output**: 
- **Kiểu**: `pd.Series`
- **Tên**: `STDEV_{length}`
- **Giá trị**: Float
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
stdev = indicator.stdev(length=14, ddof=1)
print(stdev.tail())
```

**Output**:
```
time
2024-11-26    0.628717
2024-11-27    0.589014
2024-11-28    0.608871
2024-11-29    0.681822
2024-12-02    0.820934
Name: STDEV_14, dtype: float64
```

---

### 5. LINREG - Linear Regression

**Mô tả**: Đường hồi quy tuyến tính qua dữ liệu giá. Dùng để xác định xu hướng.

**Tham số**:
- `length` (int): Số kỳ. Mặc định: 14

**Output**: 
- **Kiểu**: `pd.Series`
- **Tên**: `LR_{length}`
- **Giá trị**: Float (giá dự phóng)
- **NaN**: Có NaN ở đầu

**Ví dụ**:

```python
linreg = indicator.linreg(length=14)
print(linreg.tail())
```

**Output**:
```
time
2024-11-26    60.307319
2024-11-27    60.603982
2024-11-28    60.820391
2024-11-29    61.122064
2024-12-02    61.532196
Name: LR_14, dtype: float64
```

---

## IV. VOLUME INDICATORS (Chỉ Báo Khối Lượng)

### 1. OBV - On Balance Volume

**Mô tả**: Khối lượng cân bằng. Dùng để xác định xu hướng khối lượng. OBV tăng = khối lượng mua, OBV giảm = khối lượng bán.

**Tham số**: Không có

**Output**: 
- **Kiểu**: `pd.Series`
- **Tên**: `OBV`
- **Giá trị**: Số nguyên (tích lũy khối lượng)
- **NaN**: Không có NaN

**Ví dụ**:

```python
obv = indicator.obv()
print(obv.tail())
```

**Output**:
```
time
2024-11-26    3436700.0
2024-11-27    4483900.0
2024-11-28    3194000.0
2024-11-29    4204500.0
2024-12-02    5777600.0
Name: OBV, dtype: float64
```

**Cách sử dụng**:
- OBV tăng: Khối lượng mua tích lũy (bullish)
- OBV giảm: Khối lượng bán tích lũy (bearish)
- OBV divergence: Giá tạo high mới nhưng OBV không = tín hiệu đảo chiều
- Dùng kết hợp với chỉ báo xu hướng để xác nhận tín hiệu

---

## Tóm Tắt & So Sánh Nhanh

| Loại | Chỉ báo | Phạm vi | Ý nghĩa |
|------|---------|---------|---------|
| Trend | SMA/EMA | Float | Xu hướng |
| Trend | VWAP | Float | Giá TB khối lượng |
| Trend | ADX | 0-100 | Cường độ xu hướng |
| Trend | SUPERTREND | Float | Xu hướng & Stop loss |
| Momentum | RSI | 0-100 | Overbought/Oversold |
| Momentum | MACD | Float | Crossover |
| Momentum | Stoch | 0-100 | Overbought/Oversold |
| Volatility | BBANDS | Float | Dải biến động |
| Volatility | ATR | Float | Biến động tuyệt đối |
| Volume | OBV | Float | Khối lượng tích lũy |

