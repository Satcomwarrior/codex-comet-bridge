
import os
import time
import json
from datetime import datetime

# --- Configuration ---
FINANCIAL_DIR = 'cloud_discovery/financial'
EVIDENCE_DIR = 'cloud_discovery/evidence'
OUTPUT_DIR = 'ai_bridge/from_jules'
STATE_FILE = 'ai_bridge/logs/index_cloud_discovery.state'


def index_cloud_discovery():
    """Monitors directories for new files and creates summaries."""

    # --- State Management ---
    processed_files = set()
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                processed_files = set(json.load(f))
        except (IOError, json.JSONDecodeError):
            print(f"Warning: Could not load state file. Starting fresh.")
            processed_files = set()

    # --- Monitoring Loop ---
    try:
        while True:
            new_files_processed = False
            for directory in [FINANCIAL_DIR, EVIDENCE_DIR]:
                try:
                    if not os.path.exists(directory):
                        print(f"Warning: Directory not found: {directory}")
                        continue
                    for filename in os.listdir(directory):
                        filepath = os.path.join(directory, filename)
                        if filepath not in processed_files:
                            print(f"Processing new file: {filepath}")
                            try:
                                # Summarize the file content
                                with open(filepath, 'r', errors='ignore') as f:
                                    content = f.read()
                                    summary = f"File '{filepath}' was added at {datetime.now().isoformat()}.\n\n"
                                    summary += "Content Snippet:\n"
                                    summary += content[:500] + ('...' if len(content) > 500 else '')

                                # Write the summary to a new file in from_jules
                                summary_filename = f"summary-{os.path.basename(filepath)}-{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
                                summary_filepath = os.path.join(OUTPUT_DIR, summary_filename)
                                with open(summary_filepath, 'w') as f_out:
                                    f_out.write(summary)

                                # Mark the file as processed
                                processed_files.add(filepath)
                                new_files_processed = True
                            except IOError as e:
                                print(f"Error processing file {filepath}: {e}")
                except OSError as e:
                    print(f"Error accessing directory {directory}: {e}")

            # --- Update State File ---
            if new_files_processed:
                try:
                    with open(STATE_FILE, 'w') as f:
                        json.dump(list(processed_files), f)
                    print("State file updated.")
                except IOError as e:
                    print(f"Error writing to state file {STATE_FILE}: {e}")

            time.sleep(10)
    except KeyboardInterrupt:
        print("\nIndexer stopped by user. Saving final state.")
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(list(processed_files), f)
            print("Final state saved.")
        except IOError as e:
            print(f"Error writing to state file on exit: {e}")

if __name__ == '__main__':
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    index_cloud_discovery()
