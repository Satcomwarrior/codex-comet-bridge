import csv
import json
import os
import hashlib
from datetime import datetime

RAW_STATEMENTS_DIR = 'financial_discovery/statements/raw'
PROCESSED_STATEMENTS_DIR = 'financial_discovery/statements/processed'
UNIFIED_LEDGER_FILE = 'financial_discovery/ledger/unified_ledger.jsonl'
SCHEMA_FILE = 'financial_discovery/schema/unified_ledger_schema.json'

def generate_transaction_id(row_data):
    """Generates a unique transaction ID from a row of data."""
    row_string = json.dumps(row_data, sort_keys=True)
    return hashlib.sha256(row_string.encode()).hexdigest()

def load_existing_transaction_ids():
    """Loads all existing transaction IDs from the ledger into a set for fast lookups."""
    ids = set()
    if not os.path.exists(UNIFIED_LEDGER_FILE):
        return ids
    with open(UNIFIED_LEDGER_FILE, 'r') as f:
        for line in f:
            try:
                transaction = json.loads(line)
                if 'transaction_id' in transaction:
                    ids.add(transaction['transaction_id'])
            except json.JSONDecodeError:
                continue # Ignore corrupted lines
    return ids

def process_csv_statement(filepath, source, existing_ids):
    """Processes a single CSV financial statement and appends it to the unified ledger."""
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            transaction = {
                'transaction_id': generate_transaction_id(row),
                'timestamp': row.get('Date', row.get('Timestamp', datetime.now().isoformat())),
                'account_number': row.get('Account Number'),
                'amount': float(row.get('Amount', 0.0)),
                'currency': row.get('Currency', 'USD'),
                'description': row.get('Description'),
                'source': source,
                'reconciliation_status': 'new',
                'metadata': {
                    'original_row': row
                }
            }
            append_to_ledger(transaction, existing_ids)

def process_pdf_statement(filepath, source, existing_ids):
    """Processes a single PDF financial statement."""
    # Placeholder for PDF processing logic
    print(f"PDF processing for {filepath} is not yet implemented.")
    pass

def append_to_ledger(transaction, existing_ids):
    """Appends a transaction to the unified ledger after checking for duplicates."""
    transaction_id = transaction['transaction_id']
    if transaction_id in existing_ids:
        transaction['reconciliation_status'] = 'overlapping'
    else:
        existing_ids.add(transaction_id)
    
    with open(UNIFIED_LEDGER_FILE, 'a') as f:
        f.write(json.dumps(transaction) + '\n')

def ingest_statements():
    """Ingests all financial statements from the raw statements directory."""
    existing_ids = load_existing_transaction_ids()
    
    # Check if RAW_STATEMENTS_DIR exists
    if not os.path.exists(RAW_STATEMENTS_DIR):
        print(f"Raw statements directory not found: {RAW_STATEMENTS_DIR}")
        return
        
    for filename in os.listdir(RAW_STATEMENTS_DIR):
        filepath = os.path.join(RAW_STATEMENTS_DIR, filename)
        source = 'Comet' if 'cloud' in filename.lower() else 'LegalCodex'

        if filename.endswith('.csv'):
            process_csv_statement(filepath, source, existing_ids)
        elif filename.endswith('.pdf'):
            process_pdf_statement(filepath, source, existing_ids)
        else:
            print(f"Unsupported file format: {filename}")
            continue

        # Move processed file
        processed_filepath = os.path.join(PROCESSED_STATEMENTS_DIR, filename)
        os.rename(filepath, processed_filepath)
        print(f"Processed and moved {filename}")

if __name__ == '__main__':
    # Ensure processed and ledger directories exist
    os.makedirs(PROCESSED_STATEMENTS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(UNIFIED_LEDGER_FILE), exist_ok=True)

    ingest_statements()
    print("Ingestion complete.")
