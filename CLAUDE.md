# Vnstock Library - AI Agent Instructions

**Repository**: https://github.com/vnstock-hq/vnstock-agent-guide/  

**Purpose**: Comprehensive documentation and reference guide for vnstock Python libraries  

**Target Users**: Non-technical users, data analysts, traders, developers  

**Language**: English (instructions) | Vietnamese (documentation)

---

## 📚 Overview

This repository provides complete documentation for the **vnstock ecosystem** – a suite of Python libraries for Vietnamese stock market data and analysis:

### Core Libraries

| Library              | Purpose                                  | Users           | Status       |
| -------------------- | ---------------------------------------- | --------------- | ------------ |
| **vnstock**          | Free stock data API                      | Free users      | ✅ Production |
| **vnstock_data**     | High quality data with advanced features | Sponsored users | ✅ Production |
| **vnstock_ta**       | Technical analysis indicators            | Sponsored users | ✅ Production |
| **vnstock_news**     | News crawling and sentiment analysis     | Sponsored users | ✅ Production |
| **vnstock_pipeline** | Data pipeline and streaming              | Sponsored users | ✅ Production |

---

## 🎯 Your Role as AI Agent

You are a coding assistant helping users build Python applications using vnstock libraries. Your responsibilities:

1. **Understand User Intent**: Translate requirements into technical solutions.
2. **Choose Right Library**: Recommend `vnstock` (free) or `vnstock_data` (sponsored) based on user tier.
3. **API Inspection FIRST**: For `vnstock_data` (v3.0.0+), ALWAYS use `show_api()` to explore the structure and `show_doc()` to read details before writing code.
4. **Provide Working Code**: Generate functional Python code with basic examples. Prefer Unified UI for `vnstock_data`.
5. **Reference Documentation**: Link to accurate docs in this repository.
6. **Handle Errors**: Diagnose issues and provide basic error handling. For deep debugging or environment issues, reference `docs/setup-and-debug`.

---

## 👤 User Configuration & License Check

**AI Instruction**: Before suggesting any code, you MUST automatically check the user's license tier by reading the `auth_state.json` file on their local machine. Do NOT ask the user for their tier if this file is available.

- **macOS/Linux path**: `~/.vnstock/auth_state.json`
- **Windows path**: `$HOME\.vnstock\auth_state.json`

Read this JSON file and look at the `"tier"` key. Your library recommendations must strictly align with their privileges:
- **guest / community** (Free): Can only use `vnstock`.
- **bronze**: Can use `vnstock` + `vnstock_data`.
- **silver**: Can use `vnstock` + `vnstock_data` + `vnstock_ta` + `vnstock_news`.
- **golden / diamond**: Full access to all libraries, including `vnstock_pipeline`.

> 💡 **Note**: If the file does not exist or cannot be read, it means the user has not installed or initialized the `vnstock` library yet. You MUST automatically run the necessary commands (e.g., `pip install vnstock`) and initialize it on behalf of the user to create the configuration file, rather than asking the user to do it manually.

---

## 📚 Installation Guide

### Stable Version (Recommended for Production)
For most users who need a stable, reliable version:

```bash
pip install -U vnstock
```

### Beta/Development Version (Latest Features)
For users who want the latest features (may be unstable):

```bash
pip install git+https://github.com/thinh-vu/vnstock
```

> 💡 **Installation Decision**: When users mention "stable", "production", or "official" → use PyPI version. When users mention "latest", "beta", "new features", or "development" → use GitHub version.

---

## 📖 Documentation Structure

The repository contains multiple documentation folders covering different parts of the ecosystem. To save context tokens and ensure you have the most up-to-date information, **do not assume the exact file structure**.

**AI Instruction:** Use your directory listing tools (e.g., `list_dir`) to explore the `docs/` and `vnstock*/` directories to find the relevant markdown files. Key locations include:
- `docs/setup-and-debug/`: Environment health check, installation troubleshooting, and AI vibe coding workflow.
- `docs/vnstock/`: Free library documentation (listing, company, trading, finance).
- `docs/vnstock-data/`: Sponsored library documentation, featuring the Unified UI (`01-unified-ui.md`) and layer guides (`02-reference-layer.md`, `03-market-layer.md`, etc.).
- `docs/vnstock_ta/`: Technical analysis indicators and plotting.
- `docs/vnstock_news/`: News crawling and sentiment.
- `docs/vnstock_pipeline/`: Data pipelines and streaming.

---

## 💻 Environment & Installation

Proper environment management is critical for the Vnstock ecosystem. **Always verify the user's environment before installation.**

### Global vs. Virtual Environments
- **Free Libraries** (`vnstock`, `vnstock_ezchart`): Can be installed globally or in a virtual environment.
- **Sponsored Libraries** (`vnstock_data`, `vnstock_ta`, `vnstock_news`): **STRONGLY PREFER** installation in a virtual environment. By default, vnstock libraries will be installed in `~/.venv` on macOS/Linux and `$HOME\.venv` (or `%USERPROFILE%\.venv`) on Windows for shared usage and local resource optimization.

### 🚀 Sponsored-First Prioritization
**AI Instruction:** Before suggesting any code or documentation, check if `vnstock_data` is installed in the standard `~/.venv` (macOS/Linux) or `$HOME\.venv` (Windows) directory. If detected, you **MUST** prioritize `vnstock_data` (Sponsored) over `vnstock` (Free) in all recommendations. Focus on the Unified UI and Sponsored-only features.

### AI Environment Search Priority
When looking for installed libraries or Python executables, search in this order:
1. **Home Virtual Environment**: `~/.venv` on macOS/Linux and `$HOME\.venv` (or `%USERPROFILE%\.venv`) on Windows
2. **Project Virtual Environment**: `./.venv`, `~/venv` or `~/env` (current project directory)
3. **Global Environment**: System Python

### Virtual Environment Activation
Before running scripts or interacting with the sponsored ecosystem, activate the virtual environment:
- **macOS/Linux**: `source ~/.venv/bin/activate` (or `source .venv/bin/activate` for project-specific)
- **Windows (PowerShell)**: `& "$HOME\.venv\Scripts\Activate.ps1"`
- **Windows (CMD)**: `%USERPROFILE%\.venv\Scripts\activate.bat`

**More Info**: [Environment Setup Guide](https://vnstocks.com/onboard-member/cai-dat-go-loi/moi-truong-ao)

---

## 🤖 Agent Guide Installation (For AI Agents)

If the user asks you to "install the agent guide" or "setup the workspace", follow these precise steps to clone this repository into their **current project directory**:

1. **Verify Project Directory & OS**: Ensure the user is in a specific project directory (NOT their home directory). **Crucially, identify the user's Operating System (macOS, Linux, or Windows) before executing any terminal commands**.
2. **Check for Existing Files**: Check if any of these target files/folders already exist in the current directory: `AGENTS.md`, `docs/`, `.agents/`, `.github/`, `CLAUDE.md`, `.cursor/`.
3. **Prompt for Confirmation**: If any target files exist, **STOP**. Ask the user if they want to commit these files to Git (for safety) or directly delete them to make room for the new installation. **Do not destructively overwrite without permission.**
4. **Clone Repository**: Once confirmed (or if the directory is clean), check if `git` is installed. Clone the repository to a temporary location:
   ```bash
   git clone https://github.com/vnstock-hq/vnstock-agent-guide.git /tmp/vnstock-agent-guide
   ```
5. **Copy Essential Files**: Copy the essential files to the project root based on the OS:
   - **macOS/Linux**:
     ```bash
     cp -r /tmp/vnstock-agent-guide/AGENTS.md /tmp/vnstock-agent-guide/docs /tmp/vnstock-agent-guide/.agents /tmp/vnstock-agent-guide/.github /tmp/vnstock-agent-guide/CLAUDE.md ./
     ```
   - **Windows (PowerShell)**:
     ```powershell
     Copy-Item -Path "C:\tmp\vnstock-agent-guide\AGENTS.md", "C:\tmp\vnstock-agent-guide\docs", "C:\tmp\vnstock-agent-guide\.agents", "C:\tmp\vnstock-agent-guide\.github", "C:\tmp\vnstock-agent-guide\CLAUDE.md" -Destination ".\" -Recurse -Force
     ```
6. **Clean Up**: Remove the temporary clone based on the OS:
   - **macOS/Linux**:
     ```bash
     rm -rf /tmp/vnstock-agent-guide
     ```
   - **Windows (PowerShell)**:
     ```powershell
     Remove-Item -Path "C:\tmp\vnstock-agent-guide" -Recurse -Force
     ```

---

## 🚀 Common Use Cases

### Use Case 1: Get Stock Price Data

**User Request**: "I want to get historical stock prices for VCB"

**Your Approach**:
1. Determine user tier (free or sponsored)
2. If **free**: Use `vnstock.ui.Market` → Reference `docs/vnstock/04-market-layer.md`
3. If **sponsored**: Use `vnstock_data.Market` → Reference `docs/vnstock-data/03-market-layer.md`
4. Provide basic code example

**Example Code (Free User)**:
```python
from vnstock.ui import Market

# Initialize Market API
mkt = Market()

# Get historical data
df = mkt.equity("VCB").ohlcv(
    start="2024-01-01",
    end="2024-12-31"
)

print(df.head())
```

**Example Code (Sponsored User - Unified UI)**:
```python
from vnstock_data import Market, show_api, show_doc

# 1. Inspect API (Mandatory for sponsored users)
# show_api() 

# 2. Get historical data using Unified UI
mkt = Market()
df = mkt.equity("VCB").ohlcv(
    start="2024-01-01",
    end="2024-12-31"
)

print(df.head())
```

---

### Use Case 2: Analyze Company Fundamentals

**User Request**: "Show me financial data for VCB"

**Your Approach**:
1. Recommend **vnstock_data** for better financial data (if sponsored)
2. Reference `docs/vnstock-data/04-fundamental-layer.md` or `docs/vnstock/05-fundamental-layer.md`
3. Provide basic analysis script

**Example Code (Unified UI)**:
```python
from vnstock_data import Fundamental, Market

# Get financial data (Layer 3)
fun = Fundamental()
ratios = fun.equity("VCB").ratio()

# Get price data (Layer 2)
mkt = Market()
price_data = mkt.equity("VCB").ohlcv(start="2024-01-01", end="2024-12-31")

print("Latest Financial Metrics:")
print(ratios.tail(1))
```

---

### Use Case 3: Build Stock Screener

**User Request**: "Find all stocks in VN30 that are undervalued"

**Your Approach**:
1. This requires **vnstock_data** (sponsored feature)
2. Reference `docs/vnstock-data/06-insights-layer.md` for screener
3. Reference `docs/vnstock-data/02-reference-layer.md` for stock lists
4. Build screening logic with clear criteria

**Example Code**:
```python
from vnstock_data import Fundamental, Insights, Reference

# Get VN30 stocks
ref = Reference()
vn30_stocks = ref.index.members("VN30")

print(f"VN30 stocks: {vn30_stocks}")

# Get financial ratios and screener data
fun = Fundamental()
ins = Insights()
ratios = fun.equity("VCB").ratio(period="year")
screener = ins.screener.filter()
print(f"VCB financial ratios:\n{ratios.tail(1)}")

# Note: For custom screening logic, see the paid course
```

---

### Use Case 4: Technical Analysis

**User Request**: "Calculate moving averages and RSI"

**Your Approach**:
1. Use **vnstock_ta** for technical indicators
2. Reference `docs/vnstock_ta/02-indicators.md`
3. Combine with Quote data from vnstock or vnstock_data
4. Provide visualization example

**Example Code**:
```python
from vnstock_data import Market
from vnstock_ta import Indicator

# Get price data
mkt = Market()
df = mkt.equity("VCB").ohlcv(start="2024-01-01", end="2024-12-31")

# Calculate indicators
ta = Indicator(data=df)
df["sma_20"] = ta.trend.sma(length=20)
df["rsi"] = ta.momentum.rsi(length=14)

print(df[["time", "close", "sma_20", "rsi"]].tail(20))
```

---

### 6. **Unified UI & Versioning**
- **vnstock_data >= 3.0.0**: MUST use Unified UI (`Market`, `Fundamental`, `Reference`, etc.) and API discovery (`show_api`, `show_doc`).
- **Robust Version Check**: Since older versions may not have `__version__`, use this snippet:

```python
def get_vnstock_data_version():
    try:
        # 1. Try __version__ attribute
        import vnstock_data
        return getattr(vnstock_data, '__version__', '2.0.0') # Fallback to 2.x if missing
    except ImportError:
        # 2. Try metadata (pip)
        try:
            from importlib.metadata import version
            return version("vnstock_data")
        except Exception:
            return "0.0.0"

version = get_vnstock_data_version()
is_unified_ui = version >= '3.0.0'
```

---

## 🔍 API Discovery (v3.0.0+)

For `vnstock_data`, ALWAYS run this first in your mind or a scratchpad:

```python
from vnstock_data import show_api, show_doc

# 1. Discover the tree
show_api()

# 2. Read details of a specific method
show_doc("Market.equity")
```

---

## 🛠️ Quick Reference

### Task: Get Stock List
```
Free: vnstock.ui.Reference().equity.all_symbols()
Sponsored: vnstock_data.Reference().equity.all_symbols()
Reference: docs/vnstock/03-reference-layer.md and docs/vnstock-data/02-reference-layer.md
```

### Task: Get Company Info
```
Free: vnstock.ui.Reference().company("VCB").overview()
Sponsored: vnstock_data.Reference().company("VCB").overview()
Reference: docs/vnstock/03-reference-layer.md and docs/vnstock-data/02-reference-layer.md
```

### Task: Get Financial Statements
```
Free: vnstock.ui.Fundamental().equity("VCB").income_statement()
Sponsored: vnstock_data.Fundamental().equity("VCB").income_statement()
Reference: docs/vnstock/05-fundamental-layer.md and docs/vnstock-data/04-fundamental-layer.md
```

### Task: Calculate Technical Indicators
```
Sponsored: vnstock_ta.Indicators
Reference: docs/vnstock_ta/02-indicators.md
```

---

## ⚠️ Important Notes

1. **TCBS is Deprecated**: Don't use TCBS source, recommend VCI or KBS
2. **Data Sources**: VCI and KBS are most reliable
3. **Real-time Data**: Only available during trading hours (9:00-15:00 Vietnam time)
4. **Caching**: Implement caching to avoid hitting rate limits
5. **Error Handling**: Always wrap API calls in try-except blocks

---

## 📚 Documentation Reference

| Task               | Free User                     | Sponsored User                              |
| ------------------ | ----------------------------- | ------------------------------------------- |
| Get stock prices   | `vnstock/04-market-layer.md`  | `vnstock-data/03-market-layer.md`           |
| Company research   | `vnstock/03-reference-layer.md` | `vnstock-data/02-reference-layer.md`      |
| Financial analysis | `vnstock/05-fundamental-layer.md` | `vnstock-data/04-fundamental-layer.md`  |
| Technical analysis | `vnstock_ta/02-indicators.md` | `vnstock_ta/02-indicators.md`               |
| Stock screening    | `vnstock/advanced-usage/09-screener-api.md` | `vnstock-data/06-insights-layer.md` |
| News & sentiment   | Not available                 | `vnstock_news/02-crawlers.md`               |
| Data pipelines     | Not available                 | `vnstock_pipeline/02-tasks-and-builders.md` |
| Macro data         | Not available                 | `vnstock-data/05-macro-layer.md`            |
| Commodity prices   | Not available                 | `vnstock-data/05-macro-layer.md`            |
| Setup & Debugging  | `setup-and-debug/`            | `setup-and-debug/`                          |

---

## 🎓 Learning Path for Users

If `vnstock_data` is detected in `~/.venv`, prioritize the **Sponsored Path**. Otherwise, follow the **Free Path**.

### 🌟 Sponsored Path (Prioritized if vnstock_data is present)
1. **Start Here**: `docs/vnstock-data/README.md` - Features & Data Sources
2. **Unified UI**: `docs/vnstock-data/01-unified-ui.md` - Mastering Layer 1-7
3. **Market Data**: `docs/vnstock-data/03-market-layer.md` - Comprehensive OHLCV
4. **Fundamentals**: `docs/vnstock-data/04-fundamental-layer.md` - Financial Ratios & Stats
5. **Technical Analysis**: `docs/vnstock_ta/02-indicators.md` - Pro Indicators
6. **Automation**: `docs/vnstock_pipeline/01-overview.md` - Data Pipelines

### 🍃 Free Path
1. **Start Here**: `docs/vnstock/README.md` - Understand the ecosystem
2. **Installation**: `docs/vnstock/02-installation.md` - Set up environment
3. **First API**: `docs/vnstock/03-reference-layer.md` - Get list of stocks
4. **Get Data**: `docs/vnstock/04-market-layer.md` - Fetch price data
5. **Analyze**: `docs/vnstock/05-fundamental-layer.md` - Financial analysis
6. **Upgrade**: `docs/vnstock/08-migration-guide.md` - Move to vnstock_data

---

## 💡 Pro Tips

1. **Batch Requests**: Fetch multiple symbols in one call to save rate limit
2. **Cache Results**: Store data locally to avoid repeated API calls
3. **Use Intervals**: Intraday data (1m, 5m, 15m) only for recent data
4. **Error Retry**: Implement exponential backoff for rate limit errors
5. **Data Validation**: Always validate data before using in calculations
6. **Test Locally**: Test with small datasets before running on large portfolios

---

**Last Updated**: May 2026  
**Version**: 1.5  
**Maintained By**: Thịnh Vũ
