
import csv
import json
import hashlib
import os
import shutil
from datetime import datetime

# --- Configuration ---
# This dictionary maps the CSV column headers to the unified transaction schema fields.
# You may need to adjust this mapping for different CSV formats.
# For example, if your CSV has a "Date" column instead of "Timestamp", you would change:
# "timestamp": "Timestamp" to "timestamp": "Date"
COLUMN_MAPPING = {
    "timestamp": "Date",
    "description": "Description",
    "amount": "Amount",
    "currency": "Currency"
}

# The path to the directory containing the raw CSV statements.
RAW_STATEMENTS_DIR = "financial_discovery/statements/raw"
PROCESSED_STATEMENTS_DIR = "financial_discovery/statements/processed"


# The path to the output unified ledger file.
LEDGER_FILE = "financial_discovery/ledger/unified_ledger.jsonl"

def create_transaction_id(row_data):
    """Creates a unique transaction ID by hashing the row data."""
    # We create a string from the row data to ensure a consistent hash
    row_string = "".join(str(value) for value in row_data.values())
    return hashlib.sha256(row_string.encode()).hexdigest()

def process_csv_file(filepath):
    """Processes a single CSV file and appends its transactions to the ledger."""
    try:
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            transactions = []
            for i, row in enumerate(reader):
                try:
                    # Attempt to parse date from common formats
                    date_str = row[COLUMN_MAPPING["timestamp"]]
                    timestamp = ""
                    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
                        try:
                            timestamp = datetime.strptime(date_str, fmt).isoformat()
                            break
                        except ValueError:
                            pass
                    if not timestamp:
                        raise ValueError(f"Date format not recognized: {date_str}")

                    transaction = {
                        "timestamp": timestamp,
                        "description": row[COLUMN_MAPPING["description"]],
                        "amount": float(row[COLUMN_MAPPING["amount"]]),
                        "currency": row[COLUMN_MAPPING["currency"]],
                        "source_file": filepath
                    }
                    transaction["transaction_id"] = create_transaction_id(transaction)
                    transactions.append(transaction)
                except KeyError as e:
                    print(f"Error processing row {i+2} in {filepath}: Missing column {e}")
                except ValueError as e:
                    print(f"Error processing row {i+2} in {filepath}: {e}")

        if not transactions:
            print(f"No valid transactions found in {filepath}")
            # Move the file even if no transactions are found to avoid reprocessing
            os.makedirs(PROCESSED_STATEMENTS_DIR, exist_ok=True)
            shutil.move(filepath, os.path.join(PROCESSED_STATEMENTS_DIR, os.path.basename(filepath)))
            return

        # Ensure the ledger directory exists
        os.makedirs(os.path.dirname(LEDGER_FILE), exist_ok=True)

        with open(LEDGER_FILE, 'a') as ledger:
            for transaction in transactions:
                ledger.write(json.dumps(transaction) + '\n')

        # Move the processed file
        os.makedirs(PROCESSED_STATEMENTS_DIR, exist_ok=True)
        shutil.move(filepath, os.path.join(PROCESSED_STATEMENTS_DIR, os.path.basename(filepath)))
        print(f"Successfully processed {filepath} with {len(transactions)} transactions.")

    except Exception as e:
        print(f"Failed to process {filepath}: {e}")


if __name__ == "__main__":
    os.makedirs(RAW_STATEMENTS_DIR, exist_ok=True)
    for filename in os.listdir(RAW_STATEMENTS_DIR):
        if filename.endswith(".csv"):
            filepath = os.path.join(RAW_STATEMENTS_DIR, filename)
            print(f"Processing {filepath}...")
            process_csv_file(filepath)
    print("Done.")
