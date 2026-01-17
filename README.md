# Vnstock Agent Guide

> 🤖 **Tài Liệu Toàn Diện & Hướng Dẫn AI Agent cho Hệ Sinh Thái Vnstock**
>
> Hướng dẫn chính xác cho AI agents để hiểu, tham chiếu và sử dụng hệ sinh thái thư viện **vnstock** Python cho thị trường chứng khoán Việt Nam.

---

## 📚 Tổng Quan

**vnstock-agent-guide** là kho tài liệu toàn diện được thiết kế đặc biệt cho **AI Agents** (Claude, Gemini, GitHub Copilot, Cursor, Windsurf, Google Antigravity) để cung cấp hướng dẫn chính xác, cập nhật về cách sử dụng hệ sinh thái thư viện **vnstock**.

### 🎯 Mục Đích Chính

- **Hỗ Trợ AI Agent**: Trang bị cho AI assistants với ngữ cảnh hoàn chỉnh để giúp người dùng xây dựng ứng dụng phân tích và đầu tư chứng khoán viết riêng cho cộng đồng Việt Nam
- **Tài Liệu Tham Chiếu**: Tài liệu chi tiết cho tất cả thư viện vnstock và tính năng của chúng
- **Hướng Dẫn User Tier**: Phân biệt rõ ràng giữa khả năng của người dùng miễn phí và tài trợ
- **Ví Dụ Sẵn Sàng**: Mẫu code cho các trường hợp sử dụng
- **Best Practices**: Mẹo tối ưu, xử lý lỗi, và hiệu suất

---

## 🏗️ Hệ Sinh Thái Thư Viện

### Thư Viện Cốt Lõi

| Thư Viện           | Mục Đích                                                                | Đối Tượng       | Trạng Thái    |
| ------------------ | ---------------------------------------------------------------------- | -------------- | ------------ |
| **vnstock**        | API dữ liệu chứng khoán miễn phí (Quote, Company, Finance, Trading, Listing) | Người dùng miễn phí | ✅ Hoạt động |
| **vnstock_data**   | Lớp dữ liệu cao cấp với tính năng nâng cao (Macro, Insights, Screener) | Người tài trợ | ✅ Hoạt động |
| **vnstock_ta**     | Chỉ báo phân tích kỹ thuật và vẽ biểu đồ                             | Người tài trợ | ✅ Hoạt động |
| **vnstock_news**   | Thu thập tin tức và phân tích cảm xúc                                 | Người tài trợ | ✅ Hoạt động |
| **vnstock_pipeline** | Pipeline dữ liệu và streaming cho production                            | Người tài trợ | ✅ Hoạt động |

---

## 🤖 Hướng Dẫn AI Agent

Kho lưu trữ này cung cấp file hướng dẫn chuyên biệt cho các nền tảng AI khác nhau:

- **[.cursor/rules/instructions.md](.cursor/rules/instructions.md)** - Cho Cursor & Windsurf IDE
- **[.agent/rules/GEMINI.md](.agent/rules/GEMINI.md)** - Cho Cursor & Windsurf IDE
- **[AGENTS.md](AGENTS.md)** - Hướng dẫn cho Windsurf IDE
- **[CLAUDE.md](CLAUDE.md)** - Cho Claude Code
- **[GEMINI.md](GEMINI.md)** - Cho Gemini

---

## 📚 Cấu Trúc Tài Liệu

### Thư Viện Miễn Phí (`docs/vnstock/`)
Kiến trúc, cài đặt, APIs, và hướng dẫn di chuyển

### Thư Viện Cao Cấp (`docs/vnstock-data/`)
Tính năng nâng cao, phân tích nâng cao, và best practices

### Thư Viện Chuyên Biệt
- **[docs/vnstock_ta/](docs/vnstock_ta/)** - Phân tích kỹ thuật & chỉ báo
- **[docs/vnstock_news/](docs/vnstock_news/)** - Thu thập tin tức & cảm xúc
- **[docs/vnstock_pipeline/](docs/vnstock_pipeline/)** - Pipeline dữ liệu & streaming