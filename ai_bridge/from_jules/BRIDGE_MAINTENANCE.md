# Bridge Maintenance Protocol

## Overview

This document outlines the automated scripts and workflows that Jules, the bridge maintainer, uses to track and save progress within the AI bridge system. These processes ensure that all agent activity is logged and that any changes in the `cloud_discovery` directory are promptly summarized for Codex.

## Scripts

### 1. `summarize_activity.py`

- **Purpose**: To periodically summarize all agent activity into a single log file.
- **Location**: `ai_bridge/summarize_activity.py`
- **Functionality**:
    - Scans the `ai_bridge/to_comet` and `ai_bridge/to_codex` directories for new `.json` message files.
    - Scans the `cloud_discovery` directory for any new files.
    - Appends a new session entry, including all new messages and file content, to `ai_bridge/logs/session.json`.
- **State Management**: This script uses a state file (`ai_bridge/logs/summarize_activity.state`) to keep track of the last run time. This ensures that only new files are processed on each run.
- **Execution**: This script is intended to be run periodically (e.g., via a cron job).

### 2. `index_cloud_discovery.py`

- **Purpose**: To monitor and summarize changes in the `cloud_discovery` directory.
- **Location**: `ai_bridge/index_cloud_discovery.py`
- **Functionality**:
    - Continuously monitors the `cloud_discovery/financial` and `cloud_discovery/evidence` directories for new files.
    - When a new file is detected, it generates a brief summary of the file's content.
    - Saves the summary to a new `.txt` file in the `ai_bridge/from_jules/` directory, making it easily accessible to Codex.
- **State Management**: This script uses a state file (`ai_bridge/logs/index_cloud_discovery.state`) to keep track of processed files. This prevents the script from re-processing all files every time it restarts.
- **Execution**: This script is designed to run as a background process to provide real-time updates on new data.

## Runner Script

- **`run_maintenance.sh`**: A shell script that demonstrates how to execute the maintenance scripts. It runs the summarizer once and the indexer as a background process for a short period.

## Workflow

1. **Agent Communication**: Codex and Comet communicate by exchanging `.json` files in the `ai_bridge/to_comet` and `ai_bridge/to_codex` directories.
2. **Activity Logging**: The `summarize_activity.py` script runs periodically, collecting all new messages and `cloud_discovery` files and adding them to `ai_bridge/logs/session.json`.
3. **Cloud Discovery Monitoring**: The `index_cloud_discovery.py` script runs in the background, watching for new files in the `cloud_discovery/financial` and `cloud_discovery/evidence` directories.
4. **Summary Generation**: When a new file appears in `cloud_discovery`, `index_cloud_discovery.py` generates a summary and places it in `ai_bridge/from_jules/`.
5. **Codex Notification**: By checking the `ai_bridge/from_jules/` directory, Codex can quickly see what new information has been discovered by Comet.

This automated system ensures that all agent activity is properly logged and that important changes are communicated effectively, allowing for seamless collaboration between Codex and Comet.
