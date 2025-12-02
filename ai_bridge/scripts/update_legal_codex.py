import os
import json
import time

TO_CODEX_DIR = "ai_bridge/to_codex"
PROCESSED_FILES_LOG = "ai_bridge/logs/processed_comet_files.json"

def get_processed_files():
    if not os.path.exists(PROCESSED_FILES_LOG):
        return set()
    with open(PROCESSED_FILES_LOG, "r") as f:
        return set(json.load(f))

def save_processed_files(processed_files):
    if not os.path.exists("ai_bridge/logs"):
        os.makedirs("ai_bridge/logs")
    with open(PROCESSED_FILES_LOG, "w") as f:
        json.dump(list(processed_files), f)

def update_legal_codex(data):
    # Placeholder for LegalCodex update logic
    print(f"Updating LegalCodex with data from: {data.get('response_id')}")
    # In a real implementation, this would involve API calls or other interactions
    # with the LegalCodex system.
    print("LegalCodex update successful.")

def monitor_to_codex_directory():
    processed_files = get_processed_files()
    while True:
        for filename in os.listdir(TO_CODEX_DIR):
            if filename.endswith(".json") and filename not in processed_files:
                filepath = os.path.join(TO_CODEX_DIR, filename)
                try:
                    with open(filepath, "r") as f:
                        data = json.load(f)
                    
                    update_legal_codex(data)
                    
                    processed_files.add(filename)
                    save_processed_files(processed_files)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {filename}")
                except Exception as e:
                    print(f"An unexpected error occurred processing {filename}: {e}")
        
        time.sleep(10) # Check for new files every 10 seconds

if __name__ == "__main__":
    if not os.path.exists("ai_bridge/logs"):
        os.makedirs("ai_bridge/logs")
    monitor_to_codex_directory()
