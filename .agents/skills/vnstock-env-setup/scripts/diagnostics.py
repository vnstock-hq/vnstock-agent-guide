import sys
import os
import json
import platform
from pathlib import Path

def check_python_version():
    major, minor = sys.version_info.major, sys.version_info.minor
    status = "✅" if major >= 3 and minor >= 10 else "❌"
    print(f"{status} Python Version: {major}.{minor} (Requires >= 3.10)")
    return major >= 3 and minor >= 10

def check_venv():
    in_venv = "VIRTUAL_ENV" in os.environ or "CONDA_PREFIX" in os.environ
    status = "✅" if in_venv else "⚠️"
    print(f"{status} Virtual Environment Active: {in_venv}")
    if in_venv:
        print(f"   -> Path: {os.environ.get('VIRTUAL_ENV') or os.environ.get('CONDA_PREFIX')}")

def get_hosting():
    if 'google.colab' in sys.modules: return "Google Colab"
    if 'CODESPACE_NAME' in os.environ: return "GitHub Codespace"
    if 'KAGGLE_CONTAINER_NAME' in os.environ: return "Kaggle"
    return "Local/Unknown"

def read_auth_state():
    auth_path = Path.home() / ".vnstock" / "auth_state.json"
    if not auth_path.exists():
        return auth_path, None

    try:
        with auth_path.open(encoding="utf-8") as fh:
            return auth_path, json.load(fh)
    except Exception as exc:
        return auth_path, {"_error": str(exc)}

def check_auth_state():
    print("\n--- License State ---")
    auth_path, auth_state = read_auth_state()
    print(f"Auth file: {auth_path}")

    if auth_state is None:
        print("⚠️ auth_state.json not found. Vnstock may not be installed or initialized.")
        return None

    if "_error" in auth_state:
        print(f"❌ Could not read auth_state.json: {auth_state['_error']}")
        return None

    tier = auth_state.get("tier") or auth_state.get("license_tier") or "unknown"
    print(f"✅ License Tier: {tier}")
    return str(tier).lower()

def check_packages():
    print("\n--- Package Inventory ---")
    packages = ['vnstock', 'vnstock_data', 'vnstock_ta', 'vnstock_news', 'vnstock_pipeline', 'vnii', 'vnai']
    is_sponsor = False
    is_free = False
    
    for pkg in packages:
        try:
            mod = __import__(pkg)
            version = getattr(mod, '__version__', 'unknown')
            print(f"✅ {pkg:16} : Installed (v{version})")
            if pkg == 'vnstock': is_free = True
            if pkg == 'vnstock_data': is_sponsor = True
        except ImportError:
            print(f"❌ {pkg:16} : Not Installed")
            
    print("\n--- Tier Assessment ---")
    if is_sponsor:
        print("🏆 Detected Tier: SPONSOR (vnstock_data is present)")
    elif is_free:
        print("🌱 Detected Tier: FREE (only vnstock is present)")
    else:
        print("⚠️ Detected Tier: NONE (Ecosystem not installed)")

if __name__ == "__main__":
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Hosting: {get_hosting()}")
    check_python_version()
    check_venv()
    check_auth_state()
    check_packages()
