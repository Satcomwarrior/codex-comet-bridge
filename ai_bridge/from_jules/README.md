# Financial Discovery Tooling Documentation for Codex and Comet

## Overview

This document explains how to use the automated financial discovery tooling that has been set up in this repository. The tooling is designed to ingest financial statements from various sources (initially CSV and PDF files) and produce a unified transaction ledger in a consistent, machine-readable format.

## Directory Structure

The financial discovery tooling is organized into the following directories:

- `financial_discovery/`: The root directory for the tooling.
  - `schema/`: Contains the JSON schema that defines the structure of a unified transaction.
  - `statements/raw/`: **This is where you should drop new raw statement files (e.g., `.csv`, `.pdf`).**
  - `statements/processed/`: This directory is used by the ingestion scripts to store processed statements. You should not need to interact with this directory directly.
  - `ledger/`: Contains the unified transaction ledger, `unified_ledger.jsonl`.
  - `scripts/`: Contains the ingestion scripts that process the raw statements.

## How to Use the Tooling

### 1. Adding New Statements

To add new financial statements for processing, simply drop the raw files (e.g., `account-statement-2025-01.csv` or `bank-statement-2025-01.pdf`) into the `financial_discovery/statements/raw/` directory.

### 2. Running the Ingestion Scripts

The ingestion scripts are designed to be run automatically. For now, you can trigger them manually if needed by running the following commands from the root of the repository:

To process CSV files:
```bash
python financial_discovery/scripts/ingest_csv.py
```

To process PDF files:
```bash
python financial_discovery/scripts/ingest_pdf.py
```

### 3. Accessing the Normalized Output

The normalized transaction data is stored in the `financial_discovery/ledger/unified_ledger.jsonl` file. This is a JSON Lines file, where each line is a valid JSON object representing a single transaction.

The structure of each transaction object is defined by the schema in `financial_discovery/schema/transaction.schema.json`.

## The Unified Transaction Schema

The unified transaction schema ensures that all financial data is stored in a consistent format. Here are the key fields:

- `transaction_id`: A unique identifier for the transaction.
- `timestamp`: The date and time of the transaction (ISO 8601 format).
- `description`: A description of the transaction.
- `amount`: The monetary value of the transaction.
- `currency`: The ISO 4217 currency code.
- `source_file`: The original file from which the transaction was extracted.
