# Market (Explorer Layer) - Đánh Giá Thị Trường

> ⚠️ **Migration Notice**: Lớp `Market` cũ từ explorer layer sẽ chuyển đổi sang [Unified UI](./14-unified-ui.md) structure sau ngày **31/8/2026**. Vui lòng bắt đầu sử dụng cấu trúc mới: `Market().equity()` để truy cập dữ liệu thị trường, thay vì sử dụng các method trực tiếp trên lớp `Market` của explorer layer.
>
> **Lưu ý**: Có sự xung đột tên không gian (namespace collision) giữa lớp `Market` của explorer layer cũ và lớp `Market` mới của Unified UI. Giới hạn truy cập chỉ được giữ cho đến 31/8/2026 để cho phép chuyển đổi dần dần.

Lớp `Market` cung cấp các chỉ số đánh giá thị trường và dữ liệu định giá chứng chỉ từ SSI.

## Phương Thức Hiện Có (Sẽ Được Loại Bỏ)

### pe() - Tỷ Giá Giá/Lợi Nhuận

```python
from vnstock_data.api.market import Market

market = Market()
df = market.pe()
```

**Trả về**: DataFrame chứa các dữ liệu PE (Price-to-Earnings) từ SSI:
- `symbol`: Mã chứng chỉ
- `pe_ratio`: Tỷ số PE
- `last_updated`: Thời gian cập nhật dữ liệu

**Migration Path**:
```python
# ❌ CŨ (sẽ không hoạt động sau 31/8/2026)
from vnstock_data.api.market import Market
market = Market()
df = market.pe()

# ✅ MỚI (sử dụng Unified UI)
from vnstock_data import Market as UnifiedMarket
market = UnifiedMarket()
df = market.equity().valuation().pe()
```

### pb() - Tỷ Giá Giá/Sổ Sách

```python
from vnstock_data.api.market import Market

market = Market()
df = market.pb()
```

**Trả về**: DataFrame chứa các dữ liệu PB (Price-to-Book) từ SSI:
- `symbol`: Mã chứng chỉ
- `pb_ratio`: Tỷ số PB
- `last_updated`: Thời gian cập nhật dữ liệu

**Migration Path**:
```python
# ❌ CŨ
from vnstock_data.api.market import Market
market = Market()
df = market.pb()

# ✅ MỚI
from vnstock_data import Market as UnifiedMarket
market = UnifiedMarket()
df = market.equity().valuation().pb()
```

### evaluation() - Đánh Giá Chung

```python
from vnstock_data.api.market import Market

market = Market()
df = market.evaluation()
```

**Trả về**: DataFrame chứa tổng hợp các chỉ số đánh giá:
- `symbol`: Mã chứng chỉ
- `pe_ratio`: Tỷ số PE
- `pb_ratio`: Tỷ số PB
- `valuation_score`: Điểm đánh giá tổng hợp
- `last_updated`: Thời gian cập nhật

**Migration Path**:
```python
# ❌ CŨ
from vnstock_data.api.market import Market
market = Market()
df = market.evaluation()

# ✅ MỚI
from vnstock_data import Market as UnifiedMarket
market = UnifiedMarket()
df = market.equity().valuation().all()  # Hoặc truy cập các metric riêng lẻ
```

## Quy Trình Chuyển Đổi từ Explorer sang Unified UI

### Bước 1: Hiểu Cấu Trúc Mới
Unified UI tổ chức dữ liệu thành các lớp miền (Domain) theo chủ đề:
- `Market.equity()`: Dữ liệu chứng chỉ vốn chủ yếu
- `Market.derivatives()`: Dữ liệu chứng chỉ phái sinh (warrant, futures)
- `Market.commodity()`: Dữ liệu hàng hóa

### Bước 2: Cập Nhật Import

```python
# ❌ CŨ (Import từ API layer)
from vnstock_data.api.market import Market

# ✅ MỚI (Import từ UI layer)
from vnstock_data import Market
```

### Bước 3: Cập Nhật Gọi Hàm

```python
# ❌ CŨ
market = Market()
pe_df = market.pe()
pb_df = market.pb()
eval_df = market.evaluation()

# ✅ MỚI
market = Market()
pe_df = market.equity().valuation().pe()
pb_df = market.equity().valuation().pb()
eval_df = market.equity().valuation().all()
```

## Lịch Sử Phiên Bản

- **v2.0.0**: Giới thiệu Unified UI, đánh dấu explorer layer Market class là deprecated
- **31/8/2026**: Ngắt kết nối hoàn toàn lớp `Market` của explorer layer, bắt buộc sử dụng Unified UI

## Tham Khảo Thêm

- [Unified UI - Market Layer](./02-market-layer.md)
- [Unified UI - Equity Valuation](./14-unified-ui.md#equity-valuation---đánh-giá-định-giá)
- [Migration Guide from Explorer to Unified UI](./14-unified-ui.md#migration-note---chuyển-đổi-từ-legacy-api)

**Status**: DEPRECATED (Sẽ bị xóa sau 31/8/2026)
