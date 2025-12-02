#!/bin/bash

# A simple runner script to demonstrate the execution of the bridge maintenance scripts.

# --- Run summarize_activity.py ---
# This script is intended to be run periodically (e.g., via a cron job).
# For demonstration purposes, we will just run it once.
echo "Running the activity summarizer..."
python3 ai_bridge/summarize_activity.py

# --- Run index_cloud_discovery.py ---
# This script is intended to be run as a background process.
# We will start it in the background and then kill it after a short period.
echo "Starting the cloud discovery indexer in the background..."
python3 ai_bridge/index_cloud_discovery.py &
INDEXER_PID=$!

# Let the indexer run for a bit
sleep 15

echo "Stopping the cloud discovery indexer..."
kill $INDEXER_PID

echo "Maintenance script demonstration complete."
