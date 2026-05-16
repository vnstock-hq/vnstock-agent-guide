# Vnstock TA - Toàn Bộ Chỉ Báo Kỹ Thuật

Tài liệu này cung cấp danh sách đầy đủ 60 chỉ báo kỹ thuật được tích hợp trong thư viện `vnstock_ta`, chia thành 5 danh mục chính: Trend, Momentum, Volatility, Volume, và Statistics. 
Động cơ tính toán được cung cấp bởi `pta_reload` cho độ chính xác và hiệu suất cao.

## Cách Gọi Chỉ Báo

Tất cả các chỉ báo đều được truy cập thông qua lớp `Indicator`:

```python
from vnstock_ta import Indicator

# Khởi tạo với DataFrame (yêu cầu các cột: open, high, low, close, volume)
ta = Indicator(data=df)
```

Bạn có thể gọi chỉ báo qua thuộc tính danh mục tương ứng:
- `ta.trend.[method]()`
- `ta.momentum.[method]()`
- `ta.volatility.[method]()`
- `ta.volume.[method]()`
- `ta.statistics.[method]()`

---

## TREND INDICATORS

### `sma` - Simple Moving Average

**Mô tả**: Tính toán chỉ báo Simple Moving Average.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.trend.sma(length=14)
```

---

### `ema` - Exponential Moving Average

**Mô tả**: Tính toán chỉ báo Exponential Moving Average.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.trend.ema(length=14)
```

---

### `wma` - Weighted Moving Average

**Mô tả**: Tính toán chỉ báo Weighted Moving Average.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.trend.wma(length=10)
```

---

### `hma` - Hull Moving Average

**Mô tả**: Tính toán chỉ báo Hull Moving Average.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.trend.hma(length=10)
```

---

### `smma` - Smoothed Moving Average

**Mô tả**: Tính toán chỉ báo Smoothed Moving Average.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.trend.smma(length=7)
```

---

### `alma` - Arnaud Legoux Moving Average

**Mô tả**: Tính toán chỉ báo Arnaud Legoux Moving Average.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.trend.alma(length=10, sigma=6.0, offset=0.85)
```

---

### `vwma` - Volume-Weighted Moving Average

**Mô tả**: Tính toán chỉ báo Volume-Weighted Moving Average.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.trend.vwma(length=20)
```

---

### `adx` - Average Directional Index

**Mô tả**: Tính toán chỉ báo Average Directional Index.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.trend.adx(length=14)
```

---

### `ichimoku` - Ichimoku Cloud

**Mô tả**: Tính toán chỉ báo Ichimoku Cloud.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.trend.ichimoku(tenkan=9, kijun=26, senkou=52)
```

---

### `psar` - Parabolic SAR

**Mô tả**: Tính toán chỉ báo Parabolic SAR.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.trend.psar(af0=0.02, af=0.02, max_af=0.2)
```

---

### `supertrend` - Supertrend

**Mô tả**: Tính toán chỉ báo Supertrend.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.trend.supertrend(length=10, multiplier=3.0)
```

---

### `dm` - Directional Movement

**Mô tả**: Tính toán chỉ báo Directional Movement.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.trend.dm(length=14)
```

---

### `linreg` - Linear Regression

**Mô tả**: Tính toán chỉ báo Linear Regression.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.trend.linreg(length=14)
```

---

### `aroon` - Aroon Indicator

**Mô tả**: Tính toán chỉ báo Aroon Indicator.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.trend.aroon(length=14)
```

---

## MOMENTUM INDICATORS

### `rsi` - Relative Strength Index

**Mô tả**: Tính toán chỉ báo Relative Strength Index.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.momentum.rsi(length=14)
```

---

### `stoch` - Stochastic Oscillator

**Mô tả**: Tính toán chỉ báo Stochastic Oscillator.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.momentum.stoch(k=14, d=3, smooth_k=3)
```

---

### `stochrsi` - Stochastic RSI

**Mô tả**: Tính toán chỉ báo Stochastic RSI.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.momentum.stochrsi(length=14, rsi_length=14, k=3, d=3)
```

---

### `roc` - Rate of Change

**Mô tả**: Tính toán chỉ báo Rate of Change.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.momentum.roc(length=9)
```

---

### `ao` - Awesome Oscillator

**Mô tả**: Tính toán chỉ báo Awesome Oscillator.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.momentum.ao(fast=5, slow=34)
```

---

### `cci` - Commodity Channel Index

**Mô tả**: Tính toán chỉ báo Commodity Channel Index.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.momentum.cci(length=14, c=0.015)
```

---

### `willr` - Williams %R

**Mô tả**: Tính toán chỉ báo Williams %R.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.momentum.willr(length=14)
```

---

### `tsi` - True Strength Index

**Mô tả**: Tính toán chỉ báo True Strength Index.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.momentum.tsi(fast=13, slow=25, signal=13)
```

---

### `cmo` - Chande Momentum Oscillator

**Mô tả**: Tính toán chỉ báo Chande Momentum Oscillator.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.momentum.cmo(length=9)
```

---

### `uo` - Ultimate Oscillator

**Mô tả**: Tính toán chỉ báo Ultimate Oscillator.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.momentum.uo(fast=7, medium=14, slow=28)
```

---

### `fisher` - Fisher Transform

**Mô tả**: Tính toán chỉ báo Fisher Transform.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.momentum.fisher(length=9, signal=1)
```

---

### `cg` - Center of Gravity

**Mô tả**: Tính toán chỉ báo Center of Gravity.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.momentum.cg(length=10)
```

---

### `kst` - Know Sure Thing

**Mô tả**: Tính toán chỉ báo Know Sure Thing.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.momentum.kst(roc1=10, roc2=15, roc3=20, roc4=30)
```

---

### `macd` - Moving Average Convergence Divergence

**Mô tả**: Tính toán chỉ báo Moving Average Convergence Divergence.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.momentum.macd(fast=12, slow=26, signal=9)
```

---

## VOLATILITY INDICATORS

### `bbands` - Bollinger Bands

**Mô tả**: Tính toán chỉ báo Bollinger Bands.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volatility.bbands(length=14, std=2.0)
```

---

### `kc` - Keltner Channels

**Mô tả**: Tính toán chỉ báo Keltner Channels.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volatility.kc(length=20, scalar=2.0)
```

---

### `atr` - Average True Range

**Mô tả**: Tính toán chỉ báo Average True Range.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volatility.atr(length=14)
```

---

### `stdev` - Standard Deviation

**Mô tả**: Tính toán chỉ báo Standard Deviation.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volatility.stdev(length=14)
```

---

### `donchian` - Donchian Channels

**Mô tả**: Tính toán chỉ báo Donchian Channels.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volatility.donchian(lower_length=20, upper_length=20)
```

---

### `massi` - Mass Index

**Mô tả**: Tính toán chỉ báo Mass Index.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volatility.massi(fast=9, slow=25)
```

---

### `ui` - Ulcer Index

**Mô tả**: Tính toán chỉ báo Ulcer Index.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volatility.ui(length=14)
```

---

### `squeeze` - Squeeze Momentum

**Mô tả**: Tính toán chỉ báo Squeeze Momentum.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volatility.squeeze(bb_length=20, bb_std=2.0, kc_length=20, kc_scalar=1.5)
```

---

### `squeeze_pro` - Squeeze Momentum Pro

**Mô tả**: Tính toán chỉ báo Squeeze Momentum Pro.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volatility.squeeze_pro(bb_length=20, bb_std=2.0, kc_length=20)
```

---

### `true_range` - True Range

**Mô tả**: Tính toán chỉ báo True Range.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volatility.true_range()
```

---

## VOLUME INDICATORS

### `obv` - On-Balance Volume

**Mô tả**: Tính toán chỉ báo On-Balance Volume.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volume.obv()
```

---

### `cmf` - Chaikin Money Flow

**Mô tả**: Tính toán chỉ báo Chaikin Money Flow.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volume.cmf(length=20)
```

---

### `ad` - Accumulation/Distribution

**Mô tả**: Tính toán chỉ báo Accumulation/Distribution.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volume.ad()
```

---

### `vp` - Volume Profile

**Mô tả**: Tính toán chỉ báo Volume Profile.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volume.vp(width=10)
```

---

### `vwap` - Volume Weighted Average Price

**Mô tả**: Tính toán chỉ báo Volume Weighted Average Price.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volume.vwap(anchor="D")
```

---

### `pvo` - Percentage Volume Oscillator

**Mô tả**: Tính toán chỉ báo Percentage Volume Oscillator.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volume.pvo(fast=12, slow=26, signal=9)
```

---

### `efi` - Force Index

**Mô tả**: Tính toán chỉ báo Force Index.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volume.efi(length=13)
```

---

### `eom` - Ease of Movement

**Mô tả**: Tính toán chỉ báo Ease of Movement.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volume.eom(length=14, divisor=100000000)
```

---

### `nvi` - Negative Volume Index

**Mô tả**: Tính toán chỉ báo Negative Volume Index.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volume.nvi(length=1)
```

---

### `mfi` - Money Flow Index

**Mô tả**: Tính toán chỉ báo Money Flow Index.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.volume.mfi(length=14)
```

---

## STATISTICS INDICATORS

### `pivots` - Pivot Points

**Mô tả**: Tính toán chỉ báo Pivot Points.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.statistics.pivots(method="traditional")
```

---

### `mad` - Mean Absolute Deviation

**Mô tả**: Tính toán chỉ báo Mean Absolute Deviation.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.statistics.mad(length=30)
```

---

### `variance` - Variance

**Mô tả**: Tính toán chỉ báo Variance.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.statistics.variance(length=30)
```

---

### `hl2` - High-Low Average

**Mô tả**: Tính toán chỉ báo High-Low Average.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.statistics.hl2()
```

---

### `hlc3` - High-Low-Close Average

**Mô tả**: Tính toán chỉ báo High-Low-Close Average.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.statistics.hlc3()
```

---

### `ohlc4` - Open-High-Low-Close Average

**Mô tả**: Tính toán chỉ báo Open-High-Low-Close Average.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.statistics.ohlc4()
```

---

### `midprice` - Midprice

**Mô tả**: Tính toán chỉ báo Midprice.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.statistics.midprice(length=14)
```

---

### `decreasing` - Decreasing Series

**Mô tả**: Tính toán chỉ báo Decreasing Series.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.statistics.decreasing(length=1)
```

---

### `increasing` - Increasing Series

**Mô tả**: Tính toán chỉ báo Increasing Series.

**Cách gọi**:
```python
# Trả về pd.Series hoặc pd.DataFrame
result = ta.statistics.increasing(length=1)
```

---

