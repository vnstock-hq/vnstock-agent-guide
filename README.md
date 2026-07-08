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

| Thư Viện             | Mục Đích                                                                     | Đối Tượng           | Trạng Thái  |
| -------------------- | ---------------------------------------------------------------------------- | ------------------- | ----------- |
| **vnstock**          | API dữ liệu chứng khoán miễn phí (Quote, Company, Finance, Trading, Listing) | Người dùng miễn phí | ✅ Hoạt động |
| **vnstock_data**     | Lớp dữ liệu với tính năng nâng cao (Macro, Insights, Screener, vv)           | Người tài trợ       | ✅ Hoạt động |
| **vnstock_ta**       | Chỉ báo phân tích kỹ thuật và vẽ biểu đồ                                     | Người tài trợ       | ✅ Hoạt động |
| **vnstock_news**     | Thu thập tin tức và phân tích cảm xúc                                        | Người tài trợ       | ✅ Hoạt động |
| **vnstock_pipeline** | Pipeline dữ liệu và streaming cho production                                 | Người tài trợ       | ✅ Hoạt động |

---

## 🤖 Hướng Dẫn AI Agent

Bộ tài liệu này cung cấp tệp hướng dẫn chuyên biệt cho các nền tảng AI khác nhau ngay tại thư mục gốc để giảm thiểu tình trạng context bloat khi AI Agent quét thư mục (sắp xếp theo thứ tự ưu tiên đề xuất):

- **[AGENTS.md](AGENTS.md)** - Quy tắc chuẩn chung dùng cho **Google Antigravity IDE**, **OpenAI Codex**, **Cursor IDE**, và **Windsurf IDE**
- **[CLAUDE.md](CLAUDE.md)** - Cho **Claude Code** (CLI tool)

---

## 🚀 Cách Thiết Lập (Dành Cho AI Agent)

Thay vì phải gõ lệnh thủ công, bạn chỉ cần copy prompt (câu lệnh) dưới đây và dán vào IDE của bạn (Google Antigravity, Claude Code, Codex, Cursor, Windsurf) để AI tự động cấu hình toàn bộ:

> *"Hãy clone thư viện `https://github.com/vnstock-hq/vnstock-agent-guide.git` vào thư mục tạm. Đọc nội dung tệp `AGENTS.md` và thư mục `docs/`. Áp dụng các quy tắc này làm ngữ cảnh dự án của tôi để code với thư viện vnstock. Xóa thư mục tạm sau khi hoàn tất."*

### Thiết lập thủ công

Nếu bạn không muốn dùng Prompt trên, hãy mở Terminal tại **thư mục gốc của dự án** và chạy lệnh:

```bash
# Tải về bộ hướng dẫn
git clone https://github.com/vnstock-hq/vnstock-agent-guide.git

# Sao chép vào dự án (macOS/Linux)
cp -rf vnstock-agent-guide/AGENTS.md vnstock-agent-guide/docs vnstock-agent-guide/.agents vnstock-agent-guide/.github vnstock-agent-guide/CLAUDE.md ./

# Sao chép vào dự án (Windows PowerShell)
Copy-Item -Path vnstock-agent-guide/AGENTS.md, vnstock-agent-guide/docs, vnstock-agent-guide/.agents, vnstock-agent-guide/.github, vnstock-agent-guide/CLAUDE.md -Destination ./ -Recurse -Force
```

> **Ghi chú**: Hãy sử dụng `AGENTS.md` cho hầu hết các môi trường AI (Antigravity, Codex, Cursor, Windsurf), ngoại trừ Claude Code thì dùng `CLAUDE.md`. Lưu ý riêng:

### Tóm Tắt Tệp Hướng Dẫn Theo IDE

| AI Agent / IDE         | Tệp Hướng Dẫn                                                                     |
| :--------------------- | :-------------------------------------------------------------------------------- |
| **Google Antigravity** | `AGENTS.md` (chép ở thư mục gốc, hoặc lưu ở `~/.gemini/GEMINI.md` để dùng Global) |
| **Claude Code**        | `CLAUDE.md` (chép ở thư mục gốc)                                                  |
| **OpenAI Codex**       | `AGENTS.md` (chép ở thư mục gốc)                                                  |
| **Cursor IDE**         | `AGENTS.md` (chép ở thư mục gốc, có thể include nội dung vào `.cursorrules`)      |
| **Windsurf IDE**       | `AGENTS.md` (chép ở thư mục gốc)                                                  |

### Bước 4: Demo Notebook (Colab)

Sử dụng notebook minh hoạ nhanh trên Google Colab:

📓 **[notebooks/vnstock_agent_guide_quickstart.ipynb](notebooks/vnstock_agent_guide_quickstart.ipynb)**

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
