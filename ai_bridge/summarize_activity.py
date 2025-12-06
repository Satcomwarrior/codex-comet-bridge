
import os
import json
from datetime import datetime

def summarize_activity():
    # Directories to scan
    to_comet_dir = 'ai_bridge/to_comet'
    to_codex_dir = 'ai_bridge/to_codex'
    cloud_discovery_dir = 'cloud_discovery'
    log_file = 'ai_bridge/logs/session.json'
    state_file = 'ai_bridge/logs/summarize_activity.state'

    # --- State Management ---
    last_run_timestamp = 0
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            try:
                last_run_timestamp = float(f.read())
            except (ValueError, TypeError):
                print(f"Warning: Invalid state file content. Reprocessing all files.")
                last_run_timestamp = 0

    current_run_timestamp = datetime.now().timestamp()

    # --- Collect New Messages ---
    new_messages = []

    def scan_directory(directory_path):
        """Scans a directory for new JSON files and adds them to new_messages."""
        try:
            if not os.path.exists(directory_path):
                print(f"Warning: Directory not found: {directory_path}")
                return
            for filename in os.listdir(directory_path):
                filepath = os.path.join(directory_path, filename)
                if filename.endswith('.json') and os.path.getmtime(filepath) > last_run_timestamp:
                    try:
                        with open(filepath, 'r') as f:
                            new_messages.append(json.load(f))
                    except json.JSONDecodeError:
                        print(f"Error: Could not decode JSON from {filepath}")
                    except IOError as e:
                        print(f"Error reading file {filepath}: {e}")
        except OSError as e:
            print(f"Error accessing directory {directory_path}: {e}")

    def scan_cloud_discovery(directory_path):
        """Recursively scans cloud_discovery for new files."""
        try:
            if not os.path.exists(directory_path):
                print(f"Warning: Directory not found: {directory_path}")
                return
            for root, _, files in os.walk(directory_path):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    if os.path.getmtime(filepath) > last_run_timestamp:
                        try:
                            with open(filepath, 'r', errors='ignore') as f:
                                new_messages.append({
                                    "type": "cloud_discovery_file",
                                    "filepath": filepath,
                                    "content": f.read(5000)  # Read up to 5000 chars
                                })
                        except IOError as e:
                            print(f"Error reading file {filepath}: {e}")
        except OSError as e:
            print(f"Error accessing directory {directory_path}: {e}")

    scan_directory(to_comet_dir)
    scan_directory(to_codex_dir)
    scan_cloud_discovery(cloud_discovery_dir)

    # --- Update Log File ---
    if not new_messages:
        print("No new activity found.")
        # Update state file even if no new messages to avoid reprocessing
        with open(state_file, 'w') as f:
            f.write(str(current_run_timestamp))
        return

    try:
        if not os.path.exists(log_file) or os.path.getsize(log_file) == 0:
            sessions = [{
                "session_id": f"session-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "created": datetime.now().isoformat(),
                "participants": ["codex", "comet", "jules"],
                "messages": new_messages,
                "status": "active"
            }]
        else:
            with open(log_file, 'r') as f:
                sessions = json.load(f)
            # Append to the latest session
            if sessions:
                sessions[-1]['messages'].extend(new_messages)
            else: # If the file exists but is empty or contains an empty list
                 sessions = [{
                    "session_id": f"session-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "created": datetime.now().isoformat(),
                    "participants": ["codex", "comet", "jules"],
                    "messages": new_messages,
                    "status": "active"
                }]

        with open(log_file, 'w') as f:
            json.dump(sessions, f, indent=2)
            f.write('\n') # Add trailing newline

        # --- Update State File ---
        with open(state_file, 'w') as f:
            f.write(str(current_run_timestamp))

        print(f"Successfully processed {len(new_messages)} new item(s).")

    except (IOError, json.JSONDecodeError) as e:
        print(f"Error updating log file {log_file}: {e}")


if __name__ == '__main__':
    summarize_activity()
