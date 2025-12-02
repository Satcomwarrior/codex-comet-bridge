import unittest
import os
import json
import csv
from financial_discovery.scripts import ingest_statements

class TestIngestStatements(unittest.TestCase):

    def setUp(self):
        self.raw_dir = ingest_statements.RAW_STATEMENTS_DIR
        self.processed_dir = ingest_statements.PROCESSED_STATEMENTS_DIR
        self.ledger_file = ingest_statements.UNIFIED_LEDGER_FILE

        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)

        # Create dummy CSV file
        self.csv_filepath = os.path.join(self.raw_dir, 'test.csv')
        with open(self.csv_filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date', 'Account Number', 'Amount', 'Currency', 'Description'])
            writer.writerow(['2025-01-01', '12345', 100.00, 'USD', 'Test transaction'])
            writer.writerow(['2025-01-01', '12345', 100.00, 'USD', 'Test transaction']) # Duplicate

    def tearDown(self):
        # Use a loop to handle potential file not found errors
        files_to_remove = [
            self.csv_filepath,
            self.ledger_file,
            os.path.join(self.processed_dir, 'test.csv')
        ]
        for f in files_to_remove:
            if os.path.exists(f):
                os.remove(f)

    def test_ingest_statements(self):
        ingest_statements.ingest_statements()

        # Check that the file was moved
        self.assertFalse(os.path.exists(self.csv_filepath))
        self.assertTrue(os.path.exists(os.path.join(self.processed_dir, 'test.csv')))

        # Check that the ledger was updated
        with open(self.ledger_file, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)
            first_transaction = json.loads(lines[0])
            second_transaction = json.loads(lines[1])
            self.assertEqual(first_transaction['reconciliation_status'], 'new')
            self.assertEqual(second_transaction['reconciliation_status'], 'overlapping')

if __name__ == '__main__':
    unittest.main()
