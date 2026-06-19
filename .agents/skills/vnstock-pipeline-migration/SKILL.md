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

## 2. Migration Workflow

When a user asks you to help them migrate their code or fix their imports for `vnstock_pipeline`:

1. **Understand the Target Files**: Ask the user which directory or specific files they want to migrate, or assume the current working directory if they don't specify. Note that you should migrate `.py`, `.ipynb`, and `.md` files!
2. **Review Mapping Rules**: Read `references/mapping_rules.md` to see the exact import transformations required.
3. **Handle Deprecations**: Look out for deprecated modules `utils.governance` and `utils.fetcher_helper`. Inform the user that they should use `VNValidator` and `Scheduler` respectively.
4. **Execute the Migration**:
   - Write a python script using the `run_command` tool to walk through their `.py`, `.ipynb`, and `.md` files and apply Regex transformations based on the mapping rules.
   - Alternatively, use `multi_replace_file_content` if they only want to migrate a single file.
5. **Explain the Changes**: Inform the user about what changed. Use "Theory of Mind" to explain *why* the changes were made (e.g., "The old `core/exporter.py` was a 750-line monolith, so it was split into `core/exporters/` for better maintainability").

## 3. Strict Constraints

- Do NOT attempt to migrate code related to `vnstock_data` or `vnstock` unless the user explicitly provides rules for those libraries. Focus strictly on `vnstock_pipeline`.
- Do NOT use `sed` in bash commands for mass replacement. Always use a python script via `run_command` or the `multi_replace_file_content` tool.
