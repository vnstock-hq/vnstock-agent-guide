---
title: "01. Tra cứu thông tin (Reference)"
nav_order: 2
parent: "Giao diện Hợp nhất (Unified UI)"
---

# Domain: Reference - Tra cứu Thông tin & Danh mục

Domain `Reference` cung cấp các công cụ để khám phá thị trường, từ việc liệt kê danh sách cổ phiếu, thành phần chỉ số đến việc tra cứu thông tin chi tiết của một doanh nghiệp.

---

## 1. Khởi tạo

```python
from vnstock.ui import Reference

ref = Reference()
```

---

## 2. Các lớp và phương thức chi tiết

### A. Lớp `equity` (Cổ phiếu)

Cung cấp danh sách các mã cổ phiếu đang niêm yết và phân loại theo nhóm/ngành.

| Phương thức | Tham số | Mô tả |
| :--- | :--- | :--- |
| **`list()`** | `source='kbs'` | Liệt kê toàn bộ mã cổ phiếu niêm yết. |
| **`list_by_industry()`**| `source=None` | Liệt kê cổ phiếu theo ngành (ICB). |
| **`list_by_exchange()`**| `source='kbs'` | Liệt kê cổ phiếu theo sàn (HOSE, HNX, UPCOM). |
| **`list_by_group()`** | `group='VN30', source='kbs'` | Liệt kê cổ phiếu theo nhóm chỉ số/sàn. |

> [!WARNING]
> **Lưu ý về nguồn VCI**: Nguồn dữ liệu VCI (`list_by_industry`) rất đa dạng và chuyên sâu nhưng **không ổn định trên môi trường Google Colab** do các biện pháp bảo mật hạn chế bot của VCI. Nếu bạn sử dụng Colab, hệ thống sẽ tự động chuyển sang nguồn KBS.

**Dữ liệu mẫu (`list()`):**
| symbol | organ_name |
| :--- | :--- |
| VCB | Ngân hàng TMCP Ngoại thương Việt Nam |
| HPG | Tập đoàn Hòa Phát |

---

### B. Lớp `index` (Chỉ số)

Quản lý danh sách các bộ chỉ số thị trường.

| Phương thức | Tham số | Mô tả |
| :--- | :--- | :--- |
| **`list()`** | `source=None` | Danh sách tất cả các chỉ số (VNINDEX, VN30...). |
| **`groups()`** | `source=None` | Danh sách các nhóm chỉ số hỗ trợ. |
| **`members()`** | `symbol, source=None` | Danh sách các mã thành phần trong rổ chỉ số. |

**Dữ liệu mẫu (`list()`):**
| symbol | name | group | index_id |
| :--- | :--- | :--- | :--- |
| VN30 | VN30 | VN30 | 5 |
| VNINDEX | VNINDEX | HOSE | 1 |

---

### C. Lớp `company` (Thông tin Doanh nghiệp)

Tra cứu hồ sơ chi tiết của một mã chứng khoán cụ thể.

```python
# Cách sử dụng
vcb = ref.company("VCB")
vcb.info()
```

| Phương thức | Tham số | Mô tả |
| :--- | :--- | :--- |
| **`info()`** | `source='kbs'` | Tổng quan về doanh nghiệp (ngành, vốn hóa...). |
| **`shareholders()`** | `source='kbs'` | Danh sách cổ đông lớn. |
| **`officers()`** | `source='kbs'` | Ban lãnh đạo công ty. |
| **`subsidiaries()`** | `source='kbs'` | Các công ty con, công ty liên kết. |
| **`ownership()`** | `source='kbs'` | Cơ cấu sở hữu. |
| **`insider_trading()`**| `source='kbs'` | Lịch sử giao dịch nội bộ. |
| **`capital_history()`**| `source='kbs'` | Lịch sử thay đổi vốn. |
| **`news()`** | `source='kbs'` | Tin tức liên quan. |
| **`events()`** | `source='kbs'` | Các sự kiện doanh nghiệp (Cổ tức, đại hội...). |

---

### D. Các nhóm tài sản khác

-   **`etf.list()`**: Danh sách các chứng chỉ quỹ ETF.
-   **`futures.list()`**: Danh sách hợp đồng tương lai.
-   **`warrant.list()`**: Danh sách chứng quyền.
-   **`bond.list()`**: Danh sách trái phiếu doanh nghiệp & chính phủ.
-   **`fund.list()`**: Danh sách các quỹ mở (Nguồn FMarket).

---

## 3. Tìm kiếm (Search)

Hỗ trợ tìm kiếm mã chứng khoán và thông tin tài sản toàn cầu.

| Phương thức | Tham số | Mô tả |
| :--- | :--- | :--- |
| **`symbol()`** | `query` | Tìm kiếm mã chứng khoán theo từ khóa. |
| **`info()`** | `query` | Tìm kiếm thông tin chi tiết tài sản. |

```python
# Tìm kiếm ngân hàng
results = ref.search.symbol("Ngân hàng")
```
