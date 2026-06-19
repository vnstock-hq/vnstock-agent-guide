# Import Mapping Rules for v2.3.1

When migrating user code, apply the following exact string replacements to update the import paths. Remember to scan not just `.py` files, but also `.ipynb`, `.md`, `.txt`, and `.rst` documentation/notebook files!

## 1. Core Interfaces
- `vnstock_pipeline.core.fetcher` -> `vnstock_pipeline.core.interfaces`
- `vnstock_pipeline.core.validator` -> `vnstock_pipeline.core.interfaces`
- `vnstock_pipeline.core.transformer` -> `vnstock_pipeline.core.interfaces`

## 2. Storage Sub-package
- `vnstock_pipeline.core.storage_config` -> `vnstock_pipeline.core.storage.config`
- `vnstock_pipeline.core.storage_enums` -> `vnstock_pipeline.core.storage.enums`
- `vnstock_pipeline.core.path_builder` -> `vnstock_pipeline.core.storage.path_builder`
- `vnstock_pipeline.core.data_manager` -> `vnstock_pipeline.core.storage.data_manager`
- `vnstock_pipeline.core.metadata` -> `vnstock_pipeline.core.storage.metadata`
- `vnstock_pipeline.core.audit` -> `vnstock_pipeline.core.storage.audit`

## 3. Quality Sub-package
- `vnstock_pipeline.core.dataguard` (as a module) -> `vnstock_pipeline.core.quality`
- `vnstock_pipeline.core.schema_guard` -> `vnstock_pipeline.core.quality.schema_guard`
- `vnstock_pipeline.core.schema_registry` -> `vnstock_pipeline.core.quality.schema_registry`
- `vnstock_pipeline.core.quarantine` -> `vnstock_pipeline.core.quality.quarantine`

## 4. Exporters Sub-package
- `vnstock_pipeline.core.exporter` -> `vnstock_pipeline.core.exporters`
- `vnstock_pipeline.core.amb_exporter` -> `vnstock_pipeline.core.exporters.amibroker`
- `vnstock_pipeline.core.flexible_exporter` -> `vnstock_pipeline.core.exporters.flexible`

## 5. Utils & Helpers
- `vnstock_pipeline.helpers.*` -> `vnstock_pipeline.utils.*`
  - *(Specifically, `helpers.preview` becomes `utils.preview`, and `helpers.migration` becomes `utils.migration`)*

## 6. Deprecated Utils
If you encounter these imports, warn the user and optionally ask if they want to remove/replace them:
- `vnstock_pipeline.utils.governance` -> **Deprecated!** Logic is now fully inside `VNValidator`.
- `vnstock_pipeline.utils.fetcher_helper` -> **Deprecated!** Retry and fallback logic is now natively inside the `Scheduler`.

## 7. Unified UI Terminology (Renames)
- `vnstock_pipeline.tasks.intraday` -> `vnstock_pipeline.tasks.trades`
- `vnstock_pipeline.tasks.price_board` -> `vnstock_pipeline.tasks.quote`
- `vnstock_pipeline.tasks.trading_stats` -> `vnstock_pipeline.tasks.session_stats`
- CLI `run intraday` -> `run trades`
- CLI `run price-board` -> `run quote`
- CLI `run trading-stats` -> `run session-stats`

## Python Regex Translation (For automated scripts)

If writing a python script to automatically migrate a directory, you can use the following mapping dictionary with `re.sub`:

```python
import os
import re

import_mappings = [
    (r"vnstock_pipeline\.core\.storage_config", r"vnstock_pipeline.core.storage.config"),
    (r"vnstock_pipeline\.core\.storage_enums", r"vnstock_pipeline.core.storage.enums"),
    (r"vnstock_pipeline\.core\.path_builder", r"vnstock_pipeline.core.storage.path_builder"),
    (r"vnstock_pipeline\.core\.data_manager", r"vnstock_pipeline.core.storage.data_manager"),
    (r"vnstock_pipeline\.core\.metadata", r"vnstock_pipeline.core.storage.metadata"),
    (r"vnstock_pipeline\.core\.audit", r"vnstock_pipeline.core.storage.audit"),
    
    (r"vnstock_pipeline\.core\.dataguard(?!/)", r"vnstock_pipeline.core.quality"),
    (r"vnstock_pipeline\.core\.schema_guard", r"vnstock_pipeline.core.quality.schema_guard"),
    (r"vnstock_pipeline\.core\.schema_registry", r"vnstock_pipeline.core.quality.schema_registry"),
    (r"vnstock_pipeline\.core\.quarantine", r"vnstock_pipeline.core.quality.quarantine"),
    
    (r"vnstock_pipeline\.core\.exporter", r"vnstock_pipeline.core.exporters"),
    (r"vnstock_pipeline\.core\.amb_exporter", r"vnstock_pipeline.core.exporters.amibroker"),
    (r"vnstock_pipeline\.core\.flexible_exporter", r"vnstock_pipeline.core.exporters.flexible"),
    
    (r"vnstock_pipeline\.core\.fetcher", r"vnstock_pipeline.core.interfaces"),
    (r"vnstock_pipeline\.core\.validator", r"vnstock_pipeline.core.interfaces"),
    (r"vnstock_pipeline\.core\.transformer", r"vnstock_pipeline.core.interfaces"),

    (r"vnstock_pipeline\.helpers\.", r"vnstock_pipeline.utils."),
    
    (r"\bvnstock_pipeline\.tasks\.intraday\b", "vnstock_pipeline.tasks.trades"),
    (r"\bvnstock_pipeline\.tasks\.price_board\b", "vnstock_pipeline.tasks.quote"),
    (r"\bvnstock_pipeline\.tasks\.trading_stats\b", "vnstock_pipeline.tasks.session_stats"),
    
    (r"\brun intraday\b", "run trades"),
    (r"\brun price-board\b", "run quote"),
    (r"\brun trading-stats\b", "run session-stats"),
]

# Note: Deprecated utils are intentionally left out of automated silent replacement 
# to ensure the user manually verifies their custom VNValidator or Scheduler logic.

def refactor_imports(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            # Scan python, notebooks, and markdown docs
            if not file.endswith((".py", ".ipynb", ".md", ".txt", ".rst")):
                continue
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = content
            for old, new in import_mappings:
                new_content = re.sub(old, new, new_content)
                
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated: {path}")
```
