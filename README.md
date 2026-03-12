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

| Thư Viện             | Mục Đích                                                                     | Đối Tượng           | Trạng Thái   |
| -------------------- | ---------------------------------------------------------------------------- | ------------------- | ------------ |
| **vnstock**          | API dữ liệu chứng khoán miễn phí (Quote, Company, Finance, Trading, Listing) | Người dùng miễn phí | ✅ Hoạt động |
| **vnstock_data**     | Lớp dữ liệu với tính năng nâng cao (Macro, Insights, Screener)       | Người tài trợ       | ✅ Hoạt động |
| **vnstock_ta**       | Chỉ báo phân tích kỹ thuật và vẽ biểu đồ                                     | Người tài trợ       | ✅ Hoạt động |
| **vnstock_news**     | Thu thập tin tức và phân tích cảm xúc                                        | Người tài trợ       | ✅ Hoạt động |
| **vnstock_pipeline** | Pipeline dữ liệu và streaming cho production                                 | Người tài trợ       | ✅ Hoạt động |

---

## 🤖 Hướng Dẫn AI Agent

Kho lưu trữ này cung cấp file hướng dẫn chuyên biệt cho các nền tảng AI khác nhau:

- **[.cursor/rules/instructions.md](.cursor/rules/instructions.md)** - Cho Cursor IDE
- **[.agent/rules/GEMINI.md](.agent/rules/GEMINI.md)** - Cho Google Antigravity
- **[AGENTS.md](AGENTS.md)** - Cho Windsurf IDE
- **[CLAUDE.md](CLAUDE.md)** - Cho Claude Code
- **[GEMINI.md](GEMINI.md)** - Cho Google Gemini CLI

---

## 🚀 Cách sử dụng nhanh

Chạy lệnh dưới đây tại **thư mục gốc của dự án của bạn** để tải về bộ hướng dẫn và chép vào môi trường làm việc. Chọn lệnh phù hợp với hệ điều hành bạn dùng.

```bash
# 1. Tải về bộ hướng dẫn
git clone https://github.com/vnstock-hq/vnstock-agent-guide.git

# 2. Sao chép vào dự án của bạn (Chọn lệnh phù hợp với OS)

# macOS / Linux:
mv -f vnstock-agent-guide/docs vnstock-agent-guide/.agent vnstock-agent-guide/.cursor vnstock-agent-guide/.github vnstock-agent-guide/AGENTS.md vnstock-agent-guide/CLAUDE.md ./

# Windows (PowerShell):
Move-Item -Path vnstock-agent-guide/docs, vnstock-agent-guide/.agents, vnstock-agent-guide/.cursor, vnstock-agent-guide/.github, vnstock-agent-guide/AGENTS.md, vnstock-agent-guide/CLAUDE.md -Destination ./ -Force
```

### Bước 3: Sử Dụng Với AI Agents

| AI Agent               | File Instruction                  | Đặt tại thư mục gốc | Link Tải IDE                                                                                         |
| ---------------------- | --------------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------- |
| **Google Antigravity** | `.agent/rules/GEMINI.md`          | ✅                  | [Tải tại đây](https://antigravity.google/)                                                           |
| **Cursor IDE**         | `.cursor/rules/instructions.md`   | ✅                  | [Tải tại đây](https://cursor.com/download)                                                           |
| **Windsurf IDE**       | `AGENTS.md`                       | ✅                  | [Tải tại đây](https://windsurf.com/editor)                                                           |
| **Claude Code**        | `CLAUDE.md`                       | ✅                  | [Tải tại đây](https://claude.com/product/claude-code)                                                |
| **VS Code + Copilot**  | `.github/copilot-instructions.md` | ✅                  | [VS Code](https://code.visualstudio.com/download) + [Github Copilot](https://github.com/features/copilot/plans) |

### Bước 4: Demo Notebook (Colab)

Sử dụng notebook minh hoạ nhanh trên Google Colab:

📓 **[demo/vnstock_agent_guide_quickstart.ipynb](demo/vnstock_agent_guide_quickstart.ipynb)**

Notebook này bao gồm:

- Clone repository tự động
- Cấu hình user tier và use case
- Generate AI Agent context
- Code examples để test ngay

> 💡 **Lưu ý**: Clone repository để luôn có phiên bản mới nhất thay vì dùng context7 MCP (có thể không được update mới nhất).

---

## 📚 Cấu Trúc Tài Liệu

### Setup & Debugging (`docs/setup-and-debug/`)

Hướng dẫn thiết lập môi trường, kiểm tra lỗi và quy trình "Vibe Coding"

### Thư Viện Miễn Phí (`docs/vnstock/`)

Kiến trúc, cài đặt, APIs, và hướng dẫn di chuyển

### Thư Viện Tài Trợ (`docs/vnstock-data/`)

Tính năng nâng cao, phân tích nâng cao, và best practices

### Thư Viện Chuyên Biệt

- **[docs/vnstock_ta/](docs/vnstock_ta/)** - Phân tích kỹ thuật & chỉ báo
- **[docs/vnstock_news/](docs/vnstock_news/)** - Thu thập tin tức & cảm xúc
- **[docs/vnstock_pipeline/](docs/vnstock_pipeline/)** - Pipeline dữ liệu & streaming