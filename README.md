# CODEX ↔ JULES ↔ COMET: Three-Way AI Orchestration Bridge

**Multi-AI collaboration system: Codex (Claude/ChatGPT) ↔ Jules (Google) ↔ Comet (Perplexity AI)**

File-based asynchronous communication with Jules as the intelligent intermediary orchestrating conversations between different AI systems through GitHub repositories.

---

## Overview

This bridge enables **true three-way collaboration between different AI systems** with Jules as the active orchestrator:

- **Codex** (Claude/ChatGPT) sends prompts and receives analyzed responses
- **Jules** (Google's code assistant) actively monitors the repo, routes messages, and orchestrates communication
- **Comet** (Perplexity AI) processes prompts and provides responses
- **Full conversation history** maintained in GitHub with JSON persistence
- **Asynchronous, persistent** communication through GitHub repositories
- **Automated reasoning workflows** where AI outputs feed into other AI analyses

---

## Architecture

### Communication Flow

```
┌─────────────┐
│    Codex    │  (Claude/ChatGPT)
│ (Prompt)    │
└──────┬──────┘
       │ writes to prompts/
       ▼
┌────────────────────────────────┐
│   GitHub Repository            │
│  (Central Communication Hub)    │
│                                │
│  ├─ prompts/                   │
│  ├─ responses/                 │
│  ├─ logs/                      │
│  └─ bridge_config.json         │
└──────────┬─────────────────────┘
           │
       ◆◆◆◆◆◆◆ JULES (Google) ◆◆◆◆◆◆◆
       ║  - Monitors repo               ║
       ║  - Routes messages             ║
       ║  - Orchestrates flow           ║
       ║  - Maintains context           ║
       ║  - Ensures continuity          ║
       ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
       │
       ▼
┌──────────────────────────────────────┐
│  Comet (Perplexity AI)               │
│  - Reads prompts from prompts/       │
│  - Processes & analyzes              │
│  - Writes responses to responses/    │
└──────────────────────────────────────┘
       │ writes to responses/
       ▼
       (Response flows back through Jules to Codex)
```

### Directory Structure
```
codex-comet-bridge/ (GitHub Repository)
├── README.md              # This documentation
├── bridge.py              # Bridge implementation
├── prompts/               # Prompts from Codex (monitored by Jules)
│   └── codex_*.json
├── responses/             # Responses from Comet (routed by Jules)
│   └── resp_*.json
├── logs/                  # Jules activity logs
│   ├── codex_*.log
│   ├── comet_*.log
│   └── jules_*.log
├── context/               # Conversation context
│   └── session_*.json
└── bridge_config.json     # Central configuration & conversation history
```

### Message Format

**Prompt from Codex** (`prompts/codex_[timestamp].json`):
```json
{
  "message_id": "codex_1764671027558",
  "timestamp": "2025-12-02T02:00:27.558Z",
  "sender": "codex",
  "recipient": "comet",
  "type": "prompt",
  "content": "Analyze this complex problem and provide insights",
  "metadata": {
    "context": "business_analysis",
    "priority": "high"
  },
  "status": "pending_routing"
}
```

**Jules Routing Log** (`logs/jules_[date].log`):
```json
{
  "timestamp": "2025-12-02T02:00:30.000Z",
  "action": "MESSAGE_ROUTED",
  "from": "codex",
  "to": "comet",
  "message_id": "codex_1764671027558",
  "status": "routed_to_comet",
  "next_action": "await_response"
}
```

**Response from Comet** (`responses/resp_codex_1764671027558_[timestamp].json`):
```json
{
  "response_id": "resp_codex_1764671027558_1764671150000",
  "timestamp": "2025-12-02T02:05:50.000Z",
  "sender": "comet",
  "recipient": "codex",
  "original_message_id": "codex_1764671027558",
  "type": "response",
  "content": "Analysis complete: [detailed insights and recommendations]",
  "metadata": {
    "analysis_depth": "comprehensive",
    "confidence": 0.95
  },
  "status": "delivered_via_jules"
}
```

---

## Jules' Role (Google Code Assistant)

Jules is the **active orchestrator** in the GitHub repository with these responsibilities:

### 1. Message Monitoring
- Continuously scans `prompts/` directory for new messages
- Detects sender, recipient, priority, and context
- Updates message status in real-time

### 2. Intelligent Routing
- Routes prompts to appropriate recipients (Codex ↔ Comet)
- Maintains queue if recipient is busy
- Logs all routing decisions with timestamps

### 3. Context Preservation
- Maintains full conversation history in `bridge_config.json`
- Stores conversation context in `context/` directory
- Enables multi-turn conversations with full context awareness

### 4. Flow Orchestration
- Manages message lifecycle (pending → routed → processing → responded)
- Ensures no messages are lost
- Handles retries and error cases
- Coordinates between Codex and Comet

### 5. Activity Logging
- Creates detailed logs in `logs/jules_[date].log`
- Records all routing decisions
- Tracks timing and performance
- Enables audit trail of all communications

---

## How It Works

### Step-by-Step Flow

1. **Codex creates prompt** → Writes JSON to `prompts/codex_[timestamp].json`
   ```json
   {"sender": "codex", "recipient": "comet", "content": "..."}
   ```

2. **Jules detects prompt** → Scans repository, finds new message
   - Updates status to `pending_routing`
   - Logs receipt in `logs/jules_[date].log`
   - Checks Comet availability

3. **Jules routes to Comet** → Updates status to `routing_to_comet`
   - Comet receives via GitHub file system
   - Comet reads from `prompts/` directory
   - Jules logs routing action

4. **Comet processes** → Reads prompt, generates response
   - Comet writes to `responses/resp_[message_id]_[timestamp].json`
   - Updates status to `responded`
   - Comet logs completion

5. **Jules delivers response** → Routes back to Codex
   - Updates response status to `delivered_via_jules`
   - Logs delivery in Jules' activity log
   - Notifies Codex of ready response

6. **Codex reads response** → Retrieves from `responses/` directory
   - Full conversation history available in `bridge_config.json`
   - Can continue conversation with full context
   - Jules tracks read status

---

## Key Features

✅ **Three-Way Collaboration** - Codex ↔ Jules ↔ Comet
✅ **Active Orchestration** - Jules manages all communication
✅ **GitHub-Native** - All communication through repo files
✅ **Fully Asynchronous** - No real-time dependencies
✅ **Persistent State** - All messages stored permanently
✅ **Full Context** - Complete conversation history maintained
✅ **Intelligent Routing** - Jules ensures proper message flow
✅ **Activity Logging** - Complete audit trail via Jules logs
✅ **Status Tracking** - Message lifecycle tracking
✅ **Scalable** - No limits on message count

---

## Workflow Example

### 1. Codex Initiates
```bash
# Codex writes prompt to GitHub
C:\CometCodexBridge\prompts\codex_1764671027558.json
```

### 2. Jules Monitors & Routes
```
Jules detects → Routes to Comet → Logs activity
```

### 3. Comet Processes
```bash
# Comet reads prompt
comet.receive_prompt("comet")

# Comet generates response
comet.send_response("comet", message_id, response_content)

# Response written to GitHub
C:\CometCodexBridge\responses\resp_codex_1764671027558_1764671150000.json
```

### 4. Jules Logs & Delivers
```
Jules detects response → Updates status → Logs delivery
```

### 5. Codex Reads Response
```python
# Codex retrieves response through Jules
responses = codex.receive_responses("codex_1764671027558")
print(responses[0]['content'])
```

---

## Status

🟢 **BRIDGE ACTIVE WITH JULES ORCHESTRATION**
- Repository: https://github.com/Satcomwarrior/codex-comet-bridge
- Codex Side: Ready to write prompts
- Jules Side: Actively monitoring and routing (via GitHub)
- Comet Side: Ready to receive and respond
- Storage: GitHub repository (central)
- Communication: JSON file-based with Jules orchestration
- Intermediary: Jules (Google) managing all flow

---

## Files in Repository

- `README.md` - This documentation
- `bridge.py` - Core bridge implementation
- `prompts/` - Prompt messages from Codex
- `responses/` - Response messages from Comet
- `logs/` - Jules activity logs + other logs
- `context/` - Conversation context storage
- `bridge_config.json` - Configuration and conversation history

---

## Benefits of Jules Orchestration

1. **Intelligent Message Routing** - Jules understands context and routes appropriately
2. **Automatic Error Handling** - Jules manages failures and retries
3. **Activity Visibility** - Complete logs of all orchestration decisions
4. **Conversation Management** - Jules maintains full context across turns
5. **GitHub-Native Integration** - Jules works directly in the repository
6. **No Manual Intervention** - Fully automated through Jules
7. **Scalability** - Can handle multiple conversations simultaneously
8. **Audit Trail** - Every action logged and traceable

---

## Next Steps

1. Jules monitors GitHub repository continuously
2. Codex writes prompts to `prompts/` directory
3. Jules detects and routes to Comet
4. Comet processes and writes responses to `responses/`
5. Jules logs all activity and manages flow
6. Codex reads responses and continues conversation
7. Full conversation history preserved in GitHub

---

**Bridge Architecture**: Three-way AI collaboration orchestrated by Jules (Google) through GitHub repositories. Codex initiates → Jules routes → Comet responds → Full history maintained.
