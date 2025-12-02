
import json
import hashlib
import os
import re
import shutil
from PyPDF2 import PdfReader
from datetime import datetime

# --- Configuration ---
RAW_STATEMENTS_DIR = "financial_discovery/statements/raw"
PROCESSED_STATEMENTS_DIR = "financial_discovery/statements/processed"
LEDGER_FILE = "financial_discovery/ledger/unified_ledger.jsonl"

# --- Regular Expression for Transaction Parsing ---
# This is a simple regex that looks for a date, a description, and an amount.
# It will likely need to be adjusted for different PDF statement formats.
TRANSACTION_REGEX = re.compile(r"(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([\d,]+\.\d{2})")

def create_transaction_id(row_data):
    """Creates a unique transaction ID by hashing the row data."""
    row_string = "".join(str(value) for value in row_data.values())
    return hashlib.sha256(row_string.encode()).hexdigest()

def extract_text_from_pdf(filepath):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(filepath, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from {filepath}: {e}")
    return text

def parse_transactions_from_text(text, source_file):
    """Parses transactions from text using a regular expression."""
    transactions = []
    for match in TRANSACTION_REGEX.finditer(text):
        try:
            date_str = match.group(1)
            # Convert MM/DD/YYYY to ISO 8601 format
            timestamp = datetime.strptime(date_str, "%m/%d/%Y").isoformat()
            description = match.group(2).strip()
            amount_str = match.group(3).replace(",", "")
            amount = float(amount_str)

            transaction = {
                "timestamp": timestamp,
                "description": description,
                "amount": amount,
                "currency": "USD",  # Assuming USD for now, this may need to be extracted
                "source_file": source_file
            }
            transaction["transaction_id"] = create_transaction_id(transaction)
            transactions.append(transaction)
        except Exception as e:
            print(f"Error parsing transaction: {e}")
    return transactions

def process_pdf_file(filepath):
    """Processes a single PDF file and appends its transactions to the ledger."""
    print(f"Processing {filepath}...")
    text = extract_text_from_pdf(filepath)
    if text:
        transactions = parse_transactions_from_text(text, filepath)
        if transactions:
            # Ensure the ledger directory exists
            os.makedirs(os.path.dirname(LEDGER_FILE), exist_ok=True)
            with open(LEDGER_FILE, 'a') as ledger:
                for transaction in transactions:
                    ledger.write(json.dumps(transaction) + '\n')

            # Move the processed file
            os.makedirs(PROCESSED_STATEMENTS_DIR, exist_ok=True)
            shutil.move(filepath, os.path.join(PROCESSED_STATEMENTS_DIR, os.path.basename(filepath)))
            print(f"Successfully processed {filepath} and found {len(transactions)} transactions.")
        else:
            print(f"No transactions found in {filepath}.")
            # Move the file even if no transactions are found to avoid reprocessing
            os.makedirs(PROCESSED_STATEMENTS_DIR, exist_ok=True)
            shutil.move(filepath, os.path.join(PROCESSED_STATEMENTS_DIR, os.path.basename(filepath)))


if __name__ == "__main__":
    os.makedirs(RAW_STATEMENTS_DIR, exist_ok=True)
    for filename in os.listdir(RAW_STATEMENTS_DIR):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(RAW_STATEMENTS_DIR, filename)
            process_pdf_file(filepath)
    print("Done.")
