# 🤖 TaskPilot

## 1. Project Title

**TaskPilot — AI Business Assistant**

A modular Python assistant that converts natural-language business task requests into validated tool operations, persists tasks locally, and produces structured results and reports.

![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-17%20Passing-16A34A)
![Architecture](https://img.shields.io/badge/Architecture-Modular-7C3AED)
![Mode](https://img.shields.io/badge/Default-Demo%20Mode-F59E0B)

---

## 2. One-Line Description

> **TaskPilot interprets business task requests, selects validated Python tools, executes task operations, persists the results in JSON, and validates the resulting response.**

---

## 3. Problem

Teams frequently receive simple operational requests through chat or other communication channels:

- Create a task.
- Change a task.
- Complete a task.
- Remove a task.
- List current work.
- Summarize task status.

Turning those requests into structured operations manually can become repetitive and error-prone.

TaskPilot demonstrates a controlled architecture where a request is converted into a known tool operation instead of allowing arbitrary business logic to be executed.

---

## 4. Solution

TaskPilot separates **request interpretation**, **tool selection**, **business logic**, **validation**, **persistence**, and **reporting**.

The system supports two execution modes:

### 🟢 Deterministic Demo Mode

Natural-language patterns are routed locally to supported tools without requiring an external API.

### 🤖 Optional OpenAI Mode

OpenAI function/tool calling can select one of the predefined TaskPilot tools. The selected tool is still executed through the same validated Python tool layer.

This keeps the AI/provider layer separate from the actual business operations.

---

## 5. Key Features

### ➕ Task Creation

Create structured tasks with:

- Title
- Description
- Priority
- Generated task ID
- Creation timestamp
- Update timestamp

Supported priorities:

- `low`
- `medium`
- `high`

### 📋 Task Listing

Retrieve stored tasks and their structured fields.

### ✏️ Task Updates

Update:

- Title
- Description
- Priority

The update model requires at least one field to change.

### ✅ Task Completion

Mark an existing task as `completed`.

### 🗑️ Task Deletion

Remove an existing task by task ID.

### 📊 Task Summaries

Generate:

- Total tasks
- Pending tasks
- Completed tasks
- Priority breakdown

### 🔧 Tool Calling

The assistant exposes six defined business tools:

- `create_task`
- `list_tasks`
- `update_task`
- `complete_task`
- `delete_task`
- `task_summary`

### 🛡️ Validation

Pydantic validates:

- Task fields
- Priority/status values
- Tool results
- Assistant responses

Successful tool results must contain data, while failed results must contain an error.

### 💾 Local Persistence

Tasks are stored in a local JSON file with:

- Thread locking
- JSON validation on read
- Temporary-file replacement on write
- Flush + `fsync` before replacement
- Structured storage errors

### 📄 Reporting

TaskPilot generates human-readable timestamped text reports containing task totals, status groups, and priority breakdowns.

### 📝 Logging

Application activity and important task operations are logged.

### 🧪 Testing

The project documents **17 automated tests** covering CRUD operations, validation, routing, mocked AI tool calling, result validation, and report generation.

---

## 6. How It Works

### 🟢 Demo Mode

```text
💬 Natural-Language Request
          ↓
🤖 TaskPilot Assistant
          ↓
🧠 Deterministic Intent Routing
          ↓
🔧 Supported Python Tool
          ↓
🗂️ TaskManager
          ↓
💾 JSON Storage
          ↓
🛡️ Tool Result Validation
          ↓
📋 Assistant Response
```

### 🤖 OpenAI Mode

```text
💬 User Request
      ↓
🤖 OpenAI Tool Calling
      ↓
🔧 One of the Defined TaskPilot Tools
      ↓
🗂️ TaskManager
      ↓
💾 JSON Storage
      ↓
🛡️ Result Validation
      ↓
📋 Structured Assistant Response
```

The OpenAI layer chooses from predefined tools; it does not directly manipulate the JSON store.

---

## 7. Architecture / Workflow

### 🧩 Core Components

| Module | Responsibility |
|---|---|
| `assistant.py` | Request routing and optional OpenAI provider |
| `tools.py` | Tool definitions and execution dispatch |
| `task_manager.py` | Task business logic and JSON persistence |
| `models.py` | Pydantic domain and response models |
| `result_validator.py` | Tool-result and assistant-response validation |
| `report_generator.py` | Human-readable task reports |
| `logger.py` | Application logging |
| `main.py` | CLI/demo entry point |

### 🔄 Separation of Concerns

```text
                    ┌──────────────────┐
                    │  User Request    │
                    └────────┬─────────┘
                             ▼
                 ┌──────────────────────┐
                 │ TaskPilot Assistant  │
                 └──────────┬───────────┘
                            ▼
                  ┌──────────────────┐
                  │ Tool Selection   │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │ Validated Tools  │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │   TaskManager    │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │   JSON Storage   │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │ Result Validator │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │ Structured Reply │
                  └──────────────────┘
```

---

## 8. Technologies

| Category | Technology |
|---|---|
| 🐍 Language | Python 3.14+ |
| 🛡️ Validation | Pydantic 2.x |
| 🤖 Optional AI | OpenAI API / function-tool calling |
| 💾 Persistence | JSON |
| 🔐 Configuration | `python-dotenv` |
| 🧪 Testing | `pytest` |
| 🧰 Mocking | `unittest.mock` |
| 📝 Logging | Python `logging` |

### Dependencies

```text
pydantic>=2.7,<3
python-dotenv>=1.0,<2
openai>=1.30,<2
pytest>=8,<9
```

Demo mode does not require a live OpenAI API call.

---

## 9. Project Structure

```text
TaskPilot/
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── pytest.ini
│
├── data/
│   └── tasks.json
│
├── logs/
│
├── reports/
│
├── src/
│   ├── __init__.py
│   ├── assistant.py
│   ├── tools.py
│   ├── task_manager.py
│   ├── models.py
│   ├── result_validator.py
│   ├── report_generator.py
│   ├── logger.py
│   └── main.py
│
└── tests/
    └── ...
```

The task store is created under `data/tasks.json` when the application initializes the default `TaskManager`.

---

## 10. Installation

### 1️⃣ Navigate to TaskPilot

From the portfolio repository:

```powershell
cd Automation-Service-Projects/TaskPilot
```

### 2️⃣ Create a virtual environment

```powershell
python -m venv .venv
```

### 3️⃣ Activate it on Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4️⃣ Install dependencies

```powershell
python -m pip install -r requirements.txt
```

---

## 11. Configuration

TaskPilot uses a local `.env` file when optional configuration is required.

Copy the supplied example:

```text
OPENAI_API_KEY=
TASKPILOT_MODE=demo
OPENAI_MODEL=gpt-4o-mini
```

### 🟢 Default

```text
TASKPILOT_MODE=demo
```

### 🤖 OpenAI Mode

```text
TASKPILOT_MODE=openai
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

Never commit a real API key or `.env` file containing secrets.

Automated tests use mocked AI boundaries and therefore do not require a live OpenAI API call.

---

## 12. Usage

### ▶️ Run the deterministic demo

Because TaskPilot uses package-relative imports:

```powershell
python -m src.main
```

The demo creates sample tasks, lists them, completes one task, displays a summary, and generates a report.

### 💬 Interactive Mode

```powershell
python -m src.main --interactive
```

Then enter requests such as:

```text
Create a high priority task called Finish proposal
Create a low priority task called Book team meeting
List my tasks
Complete task task_abc123
Show my task summary
Delete task task_abc123
```

### 🧪 Run Tests

```powershell
pytest
```

---

## 13. Example

A representative deterministic interaction:

```text
> Create a high priority task called Finish proposal
Request completed.

> Create a low priority task called Book team meeting
Request completed.

> List my tasks
Request completed.

> Complete task task_xxxxxxxxxxxx
Request completed.

> Show my task summary
Request completed.

Report generated: reports/task_report_YYYYMMDD_HHMMSS.txt
```

### 🔧 Tool Mapping

| Request Pattern | Tool |
|---|---|
| Create/add task | `create_task` |
| List/show tasks | `list_tasks` |
| Update task | `update_task` |
| Complete task | `complete_task` |
| Delete task | `delete_task` |
| Task summary | `task_summary` |

Task IDs are generated dynamically, so example IDs are placeholders rather than fixed values.

---

## 14. Screenshots

> 🟡 **Reserved area — screenshots will be added later.**

Planned visual proof:

- 💬 Natural-language task request.
- 🤖 Assistant response.
- 🔧 Tool selection/execution.
- 📋 Created task structure.
- 💾 JSON persistence.
- 📊 Task summary.
- 📝 Generated report.
- 🧪 Test execution.
- 🤖 Optional OpenAI tool-calling flow where appropriate.

---

## 15. Demo Video / GIF

> 🟡 **Reserved area — demo video/GIF will be added later.**

### Planned demonstration

```text
Start TaskPilot
      ↓
Create tasks using natural language
      ↓
Route requests to tools
      ↓
Persist tasks
      ↓
List / update / complete tasks
      ↓
Generate summary
      ↓
Generate report
      ↓
Show validated structured results
```

A separate segment can demonstrate optional OpenAI tool calling while keeping the same Python execution layer.

---

## 16. Results / Benefits

### 🧪 Current Verification

- **17 automated tests** are documented.
- Demo mode works without a live AI API.
- Six business tools are explicitly defined.
- Task data is validated with Pydantic.
- Tool results are validated before assistant responses are returned.
- JSON persistence uses guarded read/write operations.
- Task updates require at least one field.
- Missing tasks produce structured failures.
- Report generation produces timestamped text reports.
- OpenAI boundaries can be mocked for testing.

### 💼 Portfolio / Service Relevance

TaskPilot demonstrates practical capabilities in:

`Python` • `AI Assistants` • `Tool Calling` • `Pydantic` • `JSON Persistence` • `Workflow Automation` • `Validation` • `Testing` • `CLI Applications`

---

## 17. Limitations

The current implementation has deliberate boundaries:

- Demo-mode intent routing uses deterministic pattern matching.
- OpenAI mode depends on an externally configured API key and provider.
- Persistence is local JSON rather than a database.
- There is no multi-user account system.
- There is no authentication or authorization layer.
- There is no REST API.
- There is no web UI.
- There is no audit-trail database.
- Natural-language understanding in demo mode is limited to supported request patterns.

These are current implementation boundaries, not claimed capabilities.

---

## 18. Future Improvements

Potential next iterations include:

- 👥 User accounts and task ownership.
- 🗄️ SQLite or PostgreSQL persistence.
- 🔐 Authentication and authorization.
- 📜 Durable audit trails.
- 🧠 Richer natural-language task updates.
- 🌐 REST API interface.
- 🖥️ Web application interface.
- 📊 More advanced reporting and analytics.
- 🔄 Additional business tools and integrations.

---

## 19. License

No license file is currently documented for TaskPilot.

Until a license is added to the repository, users should not assume that the project is released under an open-source license.

---

## 20. Author / Contact

**Hammad Borz**

> Python • AI Automation • API Integration • Data Automation • Automation Systems

TaskPilot is part of the **Automation-Service-Projects** portfolio and is positioned as a service-specific AI assistant and business tool-calling implementation.

---

### 🔗 Repository

[Automation-Service-Projects](../)

### 📌 Project

[TaskPilot](./)
