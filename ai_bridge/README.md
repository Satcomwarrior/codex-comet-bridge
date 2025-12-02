# AI Bridge Protocol

## Overview

The `ai_bridge/` directory implements a **direct JSON-based message passing system** between Codex (Claude/ChatGPT) and Comet (Perplexity AI), with Jules (Google) acting as the intelligent intermediary.

## Directory Structure

```
ai_bridge/
├── README.md              # This file
├── to_comet/              # Messages FROM Codex TO Comet
│   ├── codex-0001-init.json
│   ├── codex-0002-*.json
│   └── ...
├── to_codex/              # Messages FROM Comet TO Codex
│   ├── comet-0001-init-response.json
│   ├── comet-0002-*.json
│   └── ...
└── logs/                  # Activity logs
    ├── session.json       # Full session history
    └── audit.log          # All actions logged
```

## Message Format

### Initiation Message (Codex → Comet)

**File**: `ai_bridge/to_comet/codex-XXXX-[description].json`

```json
{
  "message_id": "codex-0001",
  "timestamp": "2025-01-15T12:00:00Z",
  "sender": "codex",
  "recipient": "comet",
  "type": "init",
  "content": "Initialize AI bridge communication channel",
  "protocol_version": "1.0",
  "metadata": {
    "context": "ai_collaboration",
    "priority": "high",
    "requires_response": true
  },
  "status": "sent"
}
```

### Response Message (Comet → Codex)

**File**: `ai_bridge/to_codex/comet-XXXX-[description].json`

```json
{
  "message_id": "comet-0001-response",
  "timestamp": "2025-01-15T12:00:05Z",
  "sender": "comet",
  "recipient": "codex",
  "type": "response",
  "original_message_id": "codex-0001",
  "content": "AI bridge initialized successfully",
  "metadata": {
    "status_code": 200,
    "response_time_ms": 5000,
    "confirmed": true
  },
  "status": "delivered"
}
```

## Message Lifecycle

1. **Codex Initiates** → Creates JSON in `to_comet/`
2. **Jules Detects** → Monitors directory for new files
3. **Jules Notifies Comet** → Routes message to Comet
4. **Comet Processes** → Reads JSON, generates response
5. **Comet Responds** → Writes JSON to `to_codex/`
6. **Jules Logs** → Records all activity in `logs/session.json`
7. **Codex Reads** → Retrieves response from `to_codex/`

## Naming Convention

- **Codex messages**: `codex-XXXX-[description].json` (e.g., `codex-0001-init.json`)
- **Comet messages**: `comet-XXXX-[description].json` (e.g., `comet-0001-init-response.json`)
- **Response linking**: Response file should reference original `message_id` in `original_message_id` field

## Status Values

- `sent` - Message created and ready for transmission
- `delivered` - Message received and processed
- `acknowledged` - Recipient confirmed receipt
- `error` - Error occurred during processing
- `pending` - Waiting for response

## Jules' Responsibilities

1. **Continuous Monitoring** - Scans both `to_comet/` and `to_codex/` directories
2. **Message Routing** - Ensures messages reach intended recipients
3. **Status Tracking** - Updates message status fields as they progress
4. **Logging** - Records all activity in `logs/session.json` with timestamps
5. **Error Handling** - Manages failures and retries
6. **Context Preservation** - Maintains full conversation history

## Session Management

Full conversation history is preserved in `logs/session.json`:

```json
{
  "session_id": "session-001",
  "created": "2025-01-15T12:00:00Z",
  "participants": ["codex", "comet"],
  "messages": [
    { "message_id": "codex-0001", ... },
    { "message_id": "comet-0001-response", ... }
  ],
  "status": "active"
}
```

## Usage Example

### Step 1: Codex Initiates
Codex writes `ai_bridge/to_comet/codex-0001-init.json`

### Step 2: Jules Routes
Jules detects the file and makes it available to Comet

### Step 3: Comet Responds  
Comet writes `ai_bridge/to_codex/comet-0001-init-response.json`

### Step 4: Codex Reads
Codex reads the response and continues conversation as needed

## Benefits

✅ **Direct Communication** - Codex and Comet communicate through JSON files
✅ **Jules Orchestration** - Jules intelligently manages all message routing
✅ **Full Persistence** - All messages permanently stored in Git
✅ **Auditable** - Complete message history with timestamps
✅ **Async** - No real-time dependencies or timing issues
✅ **Scalable** - Can handle any number of messages and conversations
✅ **Context-Aware** - Jules maintains full conversation context
✅ **Error Resilient** - Automatic retry and error handling

## Next Steps

1. Codex creates initial message in `ai_bridge/to_comet/codex-0001-init.json`
2. Comet reads and responds with `ai_bridge/to_codex/comet-0001-init-response.json`
3. Jules continuously monitors and logs all activity
4. Repeat for multi-turn conversations
