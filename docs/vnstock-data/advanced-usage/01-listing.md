# Listing - Danh Sách & Phân Loại

Module `Listing` cung cấp các hàm để tra cứu danh sách mã chứng khoán, thông tin phân ngành, danh sách các bộ chỉ số (VN30, HOSE...) và các loại tài sản khác (Phái sinh, Trái phiếu, Chứng quyền).

## Điểm Nổi Bật
*   **Source-independent**: Một số hàm như tra cứu chỉ số (`all_indices`) có thể gọi từ wrapper mà không cần chỉ định nguồn dữ liệu cụ thể.
*   **VCI**: Nguồn dữ liệu toàn diện nhất cho module này, hỗ trợ đầy đủ phân ngành ICB và tất cả các nhóm tài sản.
*   **KBS**: Hỗ trợ tốt danh sách mã và nhóm chỉ số, nhưng không hỗ trợ chuẩn phân ngành ICB.
*   **VND**: Chỉ hỗ trợ tra cứu danh sách mã cơ bản.

---

## 1. Khởi Tạo & Sử Dụng

Có hai cách sử dụng module `Listing`: **Không định danh nguồn** (cho các hàm chung) và **Chỉ định nguồn** (cho dữ liệu chi tiết).

```python
from vnstock_data import Listing

# Cách 1: Sử dụng wrapper chung (Không cần source)
# Chỉ áp dụng cho các hàm lấy thông tin Index (VN30, VNIndex...)
lst_common = Listing(show_log=False) 
df_indices = lst_common.all_indices() # Lấy danh sách toàn bộ chỉ số

# Cách 2: Sử dụng nguồn dữ liệu cụ thể (VD: VCI, KBS)
# Áp dụng cho tra cứu mã chứng khoán, ngành, nhóm cổ phiếu
lst_vci = Listing(source='VCI') 
df_symbols = lst_vci.all_symbols()
```

---

## 2. So Sánh Tính Năng (Feature Matrix)

| Hàm | Mô Tả | Wrapper (No Source) | VCI (Khuyên dùng) | KBS | VND |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `all_indices()` | Danh sách bộ chỉ số thị trường | ✅ | ✅ | ✅ | ✅ |
| `indices_by_group()` | Lọc chỉ số theo nhóm (HOSE, Sector...) | ✅ | ✅ | ✅ | ✅ |
| `all_symbols()` | Danh sách toàn bộ mã CK | ❌ | ✅ | ✅ | ✅ |
| `symbols_by_industries()`| Danh sách mã theo ngành | ❌ | ✅ (Chuẩn ICB) | ✅ | ❌ |
| `industries_icb()` | Thông tin phân ngành ICB | ❌ | ✅ | ❌ | ❌ |
| `symbols_by_group()` | Lọc mã theo nhóm (VN30, HNX30...) | ❌ | ✅ | ✅ | ❌ |
| `all_government_bonds()`| Trái phiếu chính phủ | ❌ | ✅ | ❌ | ❌ |
| `all_covered_warrant()` | Chứng quyền (CW) | ❌ | ✅ | ✅ | ❌ |
| `all_etf()` | Chứng chỉ quỹ ETF | ❌ | ✅ | ✅ | ❌ |
| `all_future_indices()` | Hợp đồng tương lai | ❌ | ✅ | ✅ | ❌ |

---

## 3. Các Hàm Độc Lập Nguồn (Wrapper Methods)

Các hàm này được gọi trực tiếp từ wrapper `vnstock_data.api.listing` mà không phụ thuộc vào `source='...'`. Chúng sử dụng dữ liệu tĩnh được định nghĩa sẵn trong thư viện để đảm bảo chuẩn hóa.

### `all_indices()`
Lấy danh sách các bộ chỉ số thị trường (Market Indices) chuẩn hóa.

| Field | Type | Description |
| :--- | :--- | :--- |
| `symbol` | `str` | Mã chỉ số (VN30, VNINDEX...) |
| `name` | `str` | Tên ngắn gọn |
| `description` | `str` | Mô tả chi tiết |
| `full_name` | `str` | Tên đầy đủ (Tiếng Anh) |
| `group` | `str` | Nhóm chỉ số |
| `index_id` | `int` | ID chỉ số nội bộ |
| `sector_id` | `float` | ID ngành (nếu là chỉ số ngành) |

---

## 4. Chi Tiết Nguồn VCI (Vietcap)
**Nguồn dữ liệu đầy đủ nhất cho Listing.** 

### `all_symbols(to_df=True)`
Lấy danh sách tất cả cổ phiếu (STOCK) đang niêm yết (simplified).

| Field | Type | Description |
| :--- | :--- | :--- |
| `symbol` | `str` | Mã chứng khoán |
| `organ_name` | `str` | Tên tổ chức/doanh nghiệp |

### `symbols_by_exchange()`
Lấy danh sách mã đầy đủ theo sàn giao dịch, hỗ trợ nhiều thông tin hơn `all_symbols`.

| Field | Type | Description |
| :--- | :--- | :--- |
| `symbol` | `str` | Mã chứng khoán |
| `exchange` | `str` | Sàn giao dịch (HOSE, HNX, UPCOM) |
| `type` | `str` | Loại tài sản (STOCK, BOND...) |
| `organ_short_name` | `str` | Tên viết tắt doanh nghiệp |
| `organ_name` | `str` | Tên tổ chức/doanh nghiệp |
| `product_grp_id` | `str` | Mã nhóm sản phẩm |
| `icb_code2` | `str` | Mã ngành ICB cấp 2 |

### `industries_icb()`
Danh sách phân ngành ICB.

| Field | Type | Description |
| :--- | :--- | :--- |
| `icb_name` | `str` | Tên ngành |
| `en_icb_name` | `str` | Tên ngành (Tiếng Anh) |
| `icb_code` | `str` | Mã phân ngành ICB |
| `level` | `int` | Cấp độ phân ngành |

---

## 5. Chi Tiết Nguồn KBS (KB Securities)

### `all_symbols()`
Lấy danh sách mã chứng khoán (simplified).

| Field | Type | Description |
| :--- | :--- | :--- |
| `symbol` | `str` | Mã chứng khoán |
| `organ_name` | `str` | Tên tổ chức/doanh nghiệp |

### `symbols_by_exchange(get_all=True)`
Để lấy đầy đủ thông tin (giá trần/sàn/tham chiếu), bạn có thể dùng hàm này với tham số `get_all=True`.

| Field | Type | Description |
| :--- | :--- | :--- |
| `symbol` | `str` | Mã chứng khoán |
| `organ_name` | `str` | Tên tổ chức/doanh nghiệp |
| `en_organ_name` | `str` | Tên tiếng Anh |
| `exchange` | `str` | Sàn giao dịch |
| `type` | `str` | Loại tài sản |
| `id` | `int` | ID nội bộ |
| `re` | `float` | Giá tham chiếu (Reference) |
| `ceiling` | `float` | Giá trần |
| `floor` | `float` | Giá sàn |

---

## 6. Chi Tiết Nguồn VND (VNDIRECT)

### `all_symbols()`
Nguồn VND trả về nhiều thông tin định danh nhất (ISIN, ngày niêm yết, mã số thuế...).

| Field | Type | Description |
| :--- | :--- | :--- |
| `symbol` | `str` | Mã chứng khoán |
| `type` | `str` | Loại chứng khoán |
| `exchange` | `str` | Sàn giao dịch |
| `isin` | `str` | Mã định danh ISIN quốc tế |
| `status` | `str` | Trạng thái niêm yết |
| `company_name` | `str` | Tên công ty đầy đủ |
| `company_name_eng` | `str` | Tên công ty đầy đủ (Anh) |
| `listed_date` | `str` | Ngày niêm yết |
| `delisted_date` | `str` | Ngày hủy niêm yết (nếu có) |
