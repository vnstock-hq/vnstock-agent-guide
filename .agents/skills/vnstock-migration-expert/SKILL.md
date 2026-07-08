---
name: vnstock-migration-expert
description: Activate this skill when a user wants to upgrade from the free tier to the sponsor tier, or migrate legacy code to the Unified UI. Do NOT activate this if the error is unrelated to imports or package versions.
---

# vnstock-migration-expert

> **PURPOSE**: Act as a technical guide and mechanic to safely migrate user code when upgrading to the Sponsor package or adopting the latest Unified UI architecture (v3.0.0+).

## 🚀 QUICK REFERENCE

| User Intent | Best Tool / Script | Action |
| :--- | :--- | :--- |
| "Add API Key but still community version?" | Guide `docs/vnstock/08-migration-guide.md` | Explain `vnstock` vs `vnstock_data`. Instruct to install and switch imports. |
| "Migrate large project Free to Sponsor" | `vnstock.core.utils.upgrade.migrate_to_sponsor` | Ensure code is committed, then run the built-in AST migration Python function. |
| "GUI Installation Failed" | `docs/setup-and-debug/02-installation-troubleshooting.md` | Instruct to install from `requirements.txt` first. |
| "externally-managed-environment error" | `docs/setup-and-debug/02-installation-troubleshooting.md` | Instruct to create a Virtual Environment (`.venv`). |
| "Migrate old code to Unified UI (v3)" | `docs/vnstock-data/01-unified-ui.md` and `docs/vnstock-data/migrations/v3.0.md` | Analyze code and map to the 7 Layers (Reference, Market, Fundamental, etc.). |

---

## ⚡ TRIGGER DETECTION

**ACTIVATE WHEN:**
1. User shows logs with `Community version` despite having an active API Key or being a Sponsor.
2. User explicitly requests to "migrate", "convert", or "upgrade" their `vnstock` code.
3. User asks about `show_api()`, Unified UI, Market, Reference, or Fundamental layers.

**DO NOT ACTIVATE WHEN:**
1. The error is unrelated to imports or package installation (e.g., calculation logic errors).
2. The user intentionally uses the free `vnstock` package and does not want to upgrade.

---

## ⚠️ CRITICAL RULES

> [!CRITICAL]
> **1. Backup Code Before Migration**
> Do not run automated migrations like `migrate_to_vnstock_data.py` without verifying that the user has committed their code. Automated replacements can cause irreversible loss of custom logic. Always ensure a backup exists.

> [!CRITICAL]
> **2. Virtual Environments for Sponsor Tier**
> Before installing `vnstock_data`, ensure the user is inside a `.venv` virtual environment. The Sponsor tier often requires precise dependency versions that might conflict with a global environment.

> [!IMPORTANT]
> **3. Use AST for Reliable Migrations**
> Avoid using regex, `sed`, or `awk` for code migrations, as they are fragile and miss context. Instead, use the built-in AST migration function shipped with the library which understands Python syntax reliably:
> `from vnstock.core.utils.upgrade import migrate_to_sponsor; migrate_to_sponsor(".")`

---

## ⛔ ANTI-PATTERNS

| ❌ AVOID | ✅ PREFER |
| :--- | :--- |
| Running `sed -i` across files. | Using the provided `migrate_to_vnstock_data.py` script. |
| Long explanations about API Keys not working. | Telling them directly: "Change the import package name from `vnstock` to `vnstock_data`". |
| Calling old legacy classes (e.g., `LegacyMacro`) in v3.0. | Mapping strictly to Unified UI (`Macro().economy().gdp()`). |

---

## ⚙️ MULTI-STEP WORKFLOW

Follow these exact steps when requested to migrate code.

### Step 1: Context & Backup
- Read the main target files to estimate scope.
- **Exit Condition**: Ask the user: "Is your code committed to Git or backed up?" Proceed only on confirmation.

### Step 2: Automated Refactor
- Use a Python Tool/Snippet to run the built-in AST migration utility provided in `vnstock` v3.5.1+:
  ```python
  from vnstock.core.utils.upgrade import migrate_to_sponsor
  migrate_to_sponsor(target_dir=".")
  ```
- **Expected Outcome**: All `import vnstock` blocks are semantically replaced with `vnstock_data`, bypassing regular expression limitations. Do not edit `.py` files manually if the codebase is large.

### Step 3: Unified UI Adjustments (Optional)
*(Only if migrating to v3.0.0+ Unified UI)*
- Search for legacy instantations. Examples:
  - `Quote(symbol="TCB")` -> `mkt = Market(); mkt.equity("TCB")`
  - `Company(symbol="TCB")` -> `ref = Reference(); ref.company("TCB")`
- Refactor carefully using block replacements, not full file overwrites.

### Step 4: Verification
- Run a basic script (e.g., `Company.overview()`) to verify imports work and API Key is valid.
- Announce migration completion.

---

## 📖 WORKED EXAMPLES

### Example 1: Free to Sponsor Upgrade

**User**: "I bought the Gold package and added the API key but it still says Community!" or the user provides a terminal output with warning: *"Đã tìm thấy thư viện Sponsor..."*

**Agent Thinking:**
- *Trigger*: "still says Community" with API key, or Smart AST Check detects user has `vnstock_data` installed but is running free version scripts.
- *Action*: Explain `vnstock` vs `vnstock_data` and auto-run the built-in migration function.

**Agent Action:**
1. Reply: "The API key alone does not unlock limits in the free version. You need to change the library name from `vnstock` to `vnstock_data` in your imports."
2. Propose running the AST migration auto-script by executing:
   ```python
   from vnstock.core.utils.upgrade import migrate_to_sponsor
   migrate_to_sponsor(target_dir=".")
   ```

### Example 2: Legacy to Unified UI Migration

**❌ LEGACY CODE (Pre v3.0):**
```python
from vnstock_data import Finance, Quote
fin = Finance(symbol="TCB")
print(fin.ratio())

price = Quote(symbol="TCB").history(start="2026-01-01", end="2026-03-01")
```

**✅ MIGRATED CODE (Unified UI v3):**
```python
from vnstock_data import Fundamental, Market
fun = Fundamental()
print(fun.equity("TCB").ratio())

mkt = Market()
price = mkt.equity("TCB").ohlcv(start="2026-01-01", end="2026-03-01")
```

---

## 📋 QUALITY CHECKLIST

Before notifying the user of completion, verify:

- [ ] Code was backed up prior to migration.
- [ ] No residual `import vnstock` remains (if upgrading to sponsor tier).
- [ ] Unified UI correctly utilizes the 7 Layers (Reference, Market, Fundamental, etc.).
- [ ] No hallucinated API endpoints were used (checked via `show_api()`).
- [ ] Linked `docs/vnstock/08-migration-guide.md` or `docs/vnstock-data/01-unified-ui.md` for further reading.
