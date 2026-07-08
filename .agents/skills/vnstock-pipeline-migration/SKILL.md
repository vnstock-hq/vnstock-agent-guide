---
name: vnstock-pipeline-migration
description: Use this skill whenever the user wants to upgrade, migrate, or fix imports for vnstock_pipeline to version 2.3.1. ALWAYS trigger this skill if the user mentions 'upgrade vnstock_pipeline', 'fix imports', 'migration', or 'v2.3.1'. This skill automatically scans and converts legacy code to the new architecture.
---

# vnstock_pipeline Migration Skill (v2.3.1)

You are the migration assistant for `vnstock_pipeline`. In version 2.3.1, the library underwent an aggressive deep-cleanup refactoring. The monolithic `core/` directory was split into specific sub-packages (`storage/`, `quality/`, `exporters/`), and all legacy import stubs were permanently deleted. 

Any user code (or `job_examples`, documentation, Jupyter Notebooks) written for older versions will break unless the imports are updated.

## 1. Things That Did NOT Change (Reassure the User)
- **High-level API (`tasks/`, `template/`, `stream/`)**: Functions like `run_task`, `VNFetcher`, `Scheduler`, `CSVProcessor` are completely unchanged (except for `intraday` -> `trades`, `price_board` -> `quote`, `trading_stats` -> `session_stats`).
- **CLI Commands**: Most commands remain identical. However, `run intraday` is now `run trades`, `run price-board` is now `run quote`, and `run trading-stats` is now `run session-stats`. Users must update their scripts using these commands.

## 2. New Capabilities in v2.3.1 (To Recommend)
- **Exchange Group Support**: The CLI `--group` argument and `UniverseManager` now fully support filtering by exchange (`HOSE`, `HNX`, `UPCOM`) in addition to `VN30`/`VN100`.
- **Automatic Directory Creation**: `DataManager.save_data()` automatically ensures parent directories exist, preventing "missing directory" crashes.
- **Config-Aware Error Logs**: The CLI `--retry-errors` flag now properly resolves the `error_log.csv` path from the global Config Hub (`pipeline.toml`) rather than assuming local execution paths.
- **Python Executable**: When writing orchestration scripts (e.g., cron jobs wrapper), always advise the user to use `sys.executable` instead of hardcoding `python3` to perfectly respect active virtual environments.

## 3. Code & Import Migration Workflow

When a user asks you to help them migrate their code or fix their imports for `vnstock_pipeline`:

1. **Understand the Target Files**: Ask the user which directory or specific files they want to migrate, or assume the current working directory if they don't specify. Note that you should migrate `.py`, `.ipynb`, and `.md` files!
2. **Review Mapping Rules**: Read `references/mapping_rules.md` to see the exact import transformations required.
3. **Handle Deprecations**: Look out for deprecated modules `utils.governance` and `utils.fetcher_helper`. Inform the user that they should use `VNValidator` and `Scheduler` respectively.
4. **Execute the Migration**:
   - Write a Python script and run it with the available command execution tool to walk through their `.py`, `.ipynb`, and `.md` files and apply Regex transformations based on the mapping rules.
   - Alternatively, use precise file edits if they only want to migrate a single file.
5. **Explain the Changes**: Inform the user about what changed. Use "Theory of Mind" to explain *why* the changes were made (e.g., "The old `core/exporter.py` was a 750-line monolith, so it was split into `core/exporters/` for better maintainability").

## 4. Data & Storage Migration Workflow

Legacy `vnstock_pipeline` (pre-2.3.0) relied on hardcoded `base_path` (e.g., `./data`) in user scripts. The new version uses a centralized **Config Hub (`pipeline.toml`)** and `StorageConfig` singleton.

When a user wants to migrate their existing database or update their data-reading programs:
1. **Migrate Legacy Data Files**: Instruct the user to run the automated CLI migration tool to move their old data folder into the new centralized storage (with automatic schema alignment):
   `python -m vnstock_pipeline.cli storage migrate-legacy --source <path_to_old_data>`
2. **Update User Scripts**: If they have custom scripts reading parquet/csv files, replace hardcoded paths (`./data/ohlcv/ACB.parquet`) with dynamic paths fetched from config:
   ```python
   from vnstock_pipeline.core.storage.config import StorageConfig
   config = StorageConfig.load()
   base_path = config.resolve_base_path()
   file_path = base_path / "ohlcv" / "ACB.parquet"
   ```
3. **Recommend CLI Queries**: Tell the user they can now directly query/inspect files without writing pandas scripts via:
   `python -m vnstock_pipeline.cli inspect <file_path>`
   `python -m vnstock_pipeline.cli query <file_path> "close > 50"`

## 5. Strict Constraints

- Do NOT attempt to migrate code related to `vnstock_data` or `vnstock` unless the user explicitly provides rules for those libraries. Focus strictly on `vnstock_pipeline`.
- Do NOT use `sed` in bash commands for mass replacement. Always use a Python script for bulk migrations, or precise file edits for a single file.
