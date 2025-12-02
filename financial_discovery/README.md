# Financial Discovery Tool

## Overview

This tool is designed to ingest and process financial statements from various sources into a unified financial ledger. It provides a structured and automated way to manage financial data for the Candi Court matter, enabling reconciliation and analysis of transactions from both LegalCodex and Comet.

## Directory Structure

```
financial_discovery/
├── README.md                # This file
├── ledger/
│   └── unified_ledger.jsonl # The unified financial ledger
├── schema/
│   └── unified_ledger_schema.json # The JSON schema for the unified ledger
├── scripts/
│   └── ingest_statements.py   # The Python script for ingesting statements
└── statements/
    ├── raw/                 # Raw financial statements to be processed
    └── processed/           # Processed financial statements
```

## Usage

1. **Place raw financial statements** in the `financial_discovery/statements/raw/` directory. The tool currently supports `.csv` files only. PDF processing is not yet implemented.

2. **Run the ingestion script** from the root of the repository:
   ```bash
   python financial_discovery/scripts/ingest_statements.py
   ```

3. **The script will:**
   - Process each statement in the `raw` directory.
   - Append the transactions to the `unified_ledger.jsonl` file.
   - Move the processed statements to the `processed` directory.

## Reconciliation

The ingestion script includes basic reconciliation logic to identify overlapping transactions. If a transaction with the same unique ID already exists in the ledger, it will be marked as `overlapping`. Otherwise, it will be marked as `new`.
