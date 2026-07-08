---
name: vnstock-pipeline-cli
description: "Use this skill whenever the user asks to manage, configure, or run tasks related to the vnstock_pipeline database, storage architecture, or CLI. ALWAYS trigger this skill if the user mentions 'vnstock_pipeline', 'storage config', 'migrate-legacy', 'pipeline.toml', 'run ohlcv', 'universe build-liquidity', 'export amibroker' or wants to download/manage stock data via terminal. Do not use this skill for vnstock_data explorer or Python API issues unless it relates to the pipeline."
---

# Vnstock Pipeline CLI Agent Guide

You are the master of the `vnstock_pipeline` CLI. Your goal is to help users manage their centralized stock database, configure storage layouts, and execute data pipelines efficiently using the terminal. 

## Core Concepts & Environment
- **Version Requirement**: The CLI features are **ONLY available in `vnstock_pipeline` versions 2.3.0 and 2.3.1 (and newer)**. Older versions do not have this CLI.
- **Default Environment**: The default virtual environment for the vnstock ecosystem is `~/.venv` on Mac/Linux or `$HOME\.venv` on Windows. Unless the user specifies a different location, assume this path. When suggesting cronjobs or background scripts, explicitly use `~/.venv/bin/python` to ensure the correct environment is loaded.
- **Config Hub (`pipeline.toml`)**: The central configuration file managing the database location (`base_path`), format (`parquet`/`csv`/`excel`), and layout (`flat`/`nested`).
- **CLI Entrypoint**: All commands are executed via `python -m vnstock_pipeline.cli <command>`. If executing within an orchestrator python script, always use `sys.executable` to respect the active virtual environment.

## 1. Configuration & Storage Management

When the user wants to change how or where data is stored, **execute these commands directly on the user's behalf** using your terminal/command tools. *Important: Ask for permission first before running commands that modify configurations or restructure data.* Always use the absolute path to the virtual environment's python (e.g., `~/.venv/bin/python`) when executing:

- **Check current config:** `~/.venv/bin/python -m vnstock_pipeline.cli storage config`
- **Change layout:** `python -m vnstock_pipeline.cli storage set-layout <flat|nested>`. Explain that `flat` is best for retail users (simple folder structure), while `nested` is optimized for AI/Data Engineering workflows (complex Data Lake hierarchy).
- **Change format & Auto-migrate:** `python -m vnstock_pipeline.cli storage set-format <parquet|csv> -y`. This updates the config AND automatically migrates existing files to the new format to prevent data fragmentation.
- **Migrate legacy data:** If the user has old static data (e.g., from an older version), use `python -m vnstock_pipeline.cli storage migrate-legacy --source ./old_data` to automatically restructure it into the new centralized database.

## 2. Quality Control & Database Auditing

Maintaining data integrity is crucial. When the user suspects missing data, schema drift, or wants to free up server space:

- **Audit Database:** `python -m vnstock_pipeline.cli storage audit`. This scans for data gaps, empty files, and stale data. Recommend this before feeding data into Machine Learning models.
- **Preview Data:** `python -m vnstock_pipeline.cli storage preview --category ohlcv`. Use this to quickly check the schema, row counts, and data snapshot without writing a Python script.
- **Cleanup Old Data:** `python -m vnstock_pipeline.cli storage cleanup --days 90`. This deletes files older than the specified days to free up storage space.
- **Manage Quarantine:** If the schema guard detects breaking changes (e.g. missing columns), it isolates files to `.tmp/.quarantine/` to protect the database. Use `python -m vnstock_pipeline.cli quarantine list` to review them.

## 3. Running Data Pipelines & Universe Building

When the user wants to download or update market data:

- **Build Liquidity Universe:** `python -m vnstock_pipeline.cli universe build-liquidity --days 50 --top 300`. This scores and filters the top liquid stocks and saves them to `pipeline.toml` as the `liquidity_auto` watchlist. Recommend running this before bulk data tasks to avoid downloading illiquid or dead stocks.
- **Run Standard Pipelines:** Use the `run` command followed by the task name (`ohlcv`, `reference`, `trading-stats`, `financial`, `news`, `events`, `quote`).
  - *Initialize long history:* `python -m vnstock_pipeline.cli run ohlcv --watchlist liquidity_auto --mode init`
  - *Daily sync:* `python -m vnstock_pipeline.cli run ohlcv --watchlist liquidity_auto --mode daily`
- **Smart Retry:** If a previous run failed due to network errors, DO NOT run the whole list again. Use `python -m vnstock_pipeline.cli run <task> --retry-errors`. This reads from `error_log.csv` to exclusively retry failed tickers, saving significant time and bandwidth.

## 4. Integration & Export

- **Export to Amibroker:** `python -m vnstock_pipeline.cli export amibroker --output ./AmibrokerData`. This command uses DuckDB to scan the local database and instantly export standard CSVs (CafeF format) required by Amibroker users.

## 5. Orchestrating CLI Commands (Example)

When the user wants to combine multiple simple CLI commands into a robust, automated execution flow (e.g., an end-of-day market data sync), recommend creating an orchestrator script in Python instead of a complex bash script. 

Read `scripts/sync_market_data.py` (located in the same directory as this skill) for a complete reference example before writing any code. This example demonstrates how to use `subprocess.run` with `sys.executable` to sequentially trigger CLI tasks (`reference`, `session-stats`, `ohlcv`, `financial`, `news`) while implementing robust logging and error handling.

## 6. Output Formatting
When running audit commands or previewing data on behalf of the user, **always format the results nicely** using Markdown tables, lists, and callouts so the user can easily read the terminal output in the chat interface.

## 7. Collaboration with Other Skills (Migration)

If the user is on an older version of `vnstock_pipeline` and needs to upgrade, fix their imports, or migrate their old static database to the new `pipeline.toml` centralized architecture, you MUST read and follow the instructions in `../vnstock-pipeline-migration/SKILL.md`. Combine the knowledge from both skills to provide a seamless upgrade and CLI execution experience.
