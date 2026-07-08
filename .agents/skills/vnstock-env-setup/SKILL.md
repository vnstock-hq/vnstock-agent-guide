---
name: vnstock-env-setup
description: Trigger this skill whenever a user reports installation errors, pip issues, or asks to set up the environment for the Vnstock ecosystem. Do NOT use this skill for general coding or data analysis questions.
---

# Vnstock Environment Setup & Diagnostics

> **PURPOSE**: This skill transforms you into the **Vnstock Environment Doctor & Setup Expert**. You are responsible for ensuring users have the perfect local or cloud setup for `vnstock` (Free) or `vnstock_data` (Sponsor). You will run diagnostics, set up python/venv, migrate legacy code, and optionally install the latest Agent Guide. **All actions must be CLI-driven; do not ask users to run UI installers unless explicitly requested.**

## ⚡ TRIGGER DETECTION

**✅ ACTIVATE WHEN:**
1. User reports an installation error ("error installing vnstock", "ModuleNotFoundError: vnstock_data", "pip error").
2. User asks you to initialize or check their environment ("chuẩn bị môi trường", "cài đặt vnstock", "setup project").
3. User asks you to install or update the **Agent Guide** ("cài đặt agent guide", "tải docs mới").

**❌ DO NOT ACTIVATE WHEN:**
1. User is asking a pure finance or data visualization question (Use `vnstock-solution-architect`).
2. User wants to write code logic right away (Unless they explicitly suffer from an import error).

---

## 📊 QUICK REFERENCE: COMMANDS

| Task | Command / Script to Execute |
| :--- | :--- |
| **1. Diagnostics Check** | **Mac/Linux:** `python3 .agents/skills/vnstock-env-setup/scripts/diagnostics.py`<br>**Win:** `py .agents/skills/vnstock-env-setup/scripts/diagnostics.py` (if `py` fails, test `python`) |
| **2. Create Venv (Mac/Linux)** | `python3 -m venv ~/.venv && source ~/.venv/bin/activate` |
| **3. Create Venv (Win)**| `py -m venv $env:USERPROFILE\.venv; & "$env:USERPROFILE\.venv\Scripts\Activate.ps1"` |
| **4. Install Dependencies**| `pip install -r https://vnstocks.com/files/requirements.txt` |
| **5. Free Tier Setup** | `pip install vnstock -U` |
| **6. Sponsor Tier Setup** | **Linux**: `wget -qO- https://vnstocks.com/files/vnstock-cli-installer.run \| bash -s -- --non-interactive --api-key "API_KEY"`<br>**Mac**: `curl -fsSL https://vnstocks.com/files/vnstock-cli-installer.run \| bash -s -- --non-interactive --api-key "API_KEY"`<br>**Win (PowerShell)**: `pip install -r https://vnstocks.com/files/requirements.txt; pip install --extra-index-url https://vnstocks.com/api/simple vnstock_installer; py -m vnstock_installer` |
| **7. Agent Guide Install** | **Mac/Linux:** `python3 .agents/skills/vnstock-env-setup/scripts/setup_agent_guide.py --confirm-docs-overwrite`<br>**Win:** `py .agents/skills/vnstock-env-setup/scripts/setup_agent_guide.py --confirm-docs-overwrite` |

---

## ⚠️ CRITICAL RULES

> [!CRITICAL]
> **1. The Virtual Environment Mandate**
> If the user is on a Local machine (macOS, Linux, Windows), always set up a virtual environment (e.g., `~/.venv`). Installing packages globally using `--break-system-packages` can lead to dependency conflicts and break their system Python installation.

> [!CRITICAL]
> **2. Sponsor Tier Migration Checks**
> If you detect the user is on the **Sponsor Tier** (`vnstock_data`), actively search the workspace for legacy `from vnstock import ...` code. Legacy code will fail or lack advanced features. If found, invoke `vnstock-migration-expert` to migrate their scripts to the Unified UI.

> [!IMPORTANT]
> **3. Safe Overwrites for Agent Guide**
> When installing the Agent Guide, pause if the `docs/` directory already exists. Ask the user for explicit permission before overwriting to prevent accidental loss of any custom documentation they may have written.

---

## ⛔ ANTI-PATTERNS (COMMON TRAPS)

| ❌ AVOID | ✅ PREFER |
| :--- | :--- |
| Asking the user "Are you in a venv?" | Running `diagnostics.py` to check for `VIRTUAL_ENV` automatically. |
| Overwriting `docs/` blindly during guide setup | Asking: *"Thư mục docs/ đã tồn tại, bạn có muốn ghi đè để cập nhật Agent Guide không?"* |
| Assuming pip installs successfully globally | Always activate Venv explicitly before running `pip`. |
| Ignoring Windows aliases loops | Telling users to turn off "App Execution Aliases" for Python in Windows Settings, or using `py` command instead of `python`. |
| Assuming `~` maps to home dir on Windows natively | Using `$env:USERPROFILE\.venv` instead of `~/.venv` when interacting via PowerShell on Windows. |

---

## ⚙️ THE UNIFIED SETUP WORKFLOW

Follow this exact sequence to ensure a flawless setup for any user.

### Step 1: Run Diagnostics
Run the provided python script to detect OS, Python version, Venv, and installed packages.
```bash
# Mac/Linux
python3 .agents/skills/vnstock-env-setup/scripts/diagnostics.py

# Windows
# Note: Try 'py' first to avoid Windows Store aliases. If it fails, fallback to 'python' or prompt user.
py .agents/skills/vnstock-env-setup/scripts/diagnostics.py
```

### Step 2: Ensure Python & Git exist
*Evaluate output from Step 1:* 
- If Python < 3.10, suggest `brew install python@3.12` (Mac) or `winget install Python.Python.3.12` (Win).
- Ensure `git` is installed (the Agent Guide script in Step 3 will also verify this).

### Step 3: Install/Update Agent Guide
Before proceeding, install the latest Agent Guide to provide the AI with the deepest context ($docs/$ and skills).

1. **Check for existing docs:** `ls -d docs/ 2>/dev/null`
2. **Request Permission:** If `docs/` exists, you MUST pause and ask the user directly: *"Thư mục `docs/` đã tồn tại. Quá trình cài đặt Agent Guide sẽ ghi đè thư mục này (nhưng tự động sao lưu Git trước). Bạn có đồng ý không?"*
3. **Execute Setup:**
```bash
# Mac/Linux (append --confirm-docs-overwrite if permission was granted)
python3 .agents/skills/vnstock-env-setup/scripts/setup_agent_guide.py

```powershell
# Windows (append --confirm-docs-overwrite if permission was granted)
py .agents/skills/vnstock-env-setup/scripts/setup_agent_guide.py
```
> **AI Instruction**: Once the guide is installed, actively reference the setup instructions in `docs/setup-and-debug` for the remainder of this setup process if needed.

### Step 4: Establish Virtual Environment & Requirements
Create a virtual environment (`~/.venv`) to isolate dependencies. Install the baseline requirements to ensure no package conflicts happen later.

```bash
# Mac/Linux
python3 -m venv ~/.venv
source ~/.venv/bin/activate
pip install -r https://vnstocks.com/files/requirements.txt
```

```powershell
# Windows
py -m venv $env:USERPROFILE\.venv
& "$env:USERPROFILE\.venv\Scripts\Activate.ps1"
pip install -r https://vnstocks.com/files/requirements.txt
```

### Step 5: Install Vnstock Packages
Based on the user's tier discovered in Step 1 (or if they provided an API key):

**If they are a Free User:**
```bash
pip install vnstock -U
```

**If they are a Sponsor User (requires API key):**
```bash
# Linux
wget -qO- https://vnstocks.com/files/vnstock-cli-installer.run | bash -s -- --non-interactive --api-key "USER_API_KEY" --accept

# Mac
curl -fsSL https://vnstocks.com/files/vnstock-cli-installer.run | bash -s -- --non-interactive --api-key "USER_API_KEY" --accept

# Windows (PowerShell)
pip install --extra-index-url https://vnstocks.com/api/simple vnstock_installer
py -m vnstock_installer
# ⚠️ Note on Windows: If the installer runs successfully on the browser but the terminal shows "uv install failed... Access is denied", it is due to a Windows file lock issue. Inform the user that they can safely ignore it if the main packages (vnstock_data) were successfully installed, or suggest they close terminal/VSCode and retry.
```

### Step 6: Verification & Migration Check (⭐ CRITICAL)
Run `diagnostics.py` again. If `vnstock_data` is now installed, BẮT BUỘC search the workspace for legacy imports using a fast code search tool (for example `rg "from vnstock import"`). If found, run `vnstock-migration-expert` to migrate the user's code.

---

## ✅ QUALITY CHECKLIST

Before concluding your interaction, verify:
- [ ] Did you properly diagnose using `diagnostics.py` instead of guessing?
- [ ] If setting up Python, did you ensure they are in a `.venv`?
- [ ] If Sponsor tier was detected, did you trigger the `vnstock-migration-expert`?
- [ ] During Agent Guide setup, did you warn the user before overwriting `docs/` and run the backup script?
