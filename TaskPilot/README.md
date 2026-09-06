# 🤖 TaskPilot — AI Business Assistant

> **A portfolio-ready Python AI assistant that converts business task requests into validated, structured, and dependable task operations.**

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-17-success.svg)](#-testing)
[![Architecture](https://img.shields.io/badge/architecture-modular-purple.svg)](#-architecture)
[![Mode](https://img.shields.io/badge/default-demo%20mode-yellow.svg)](#-how-it-works)

---

## 🎯 The Business Problem

Teams often receive simple work requests through chat, email, and other communication channels. Converting those requests into organized tasks can become repetitive and error-prone.

**TaskPilot demonstrates how an AI-assisted automation system can:**

- 📝 Understand a task request
- 🧠 Select an appropriate action
- 🔧 Execute validated Python tools
- 💾 Persist task data safely
- 🛡️ Validate structured results
- 📊 Generate summaries and reports

---

# ⚙️ How It Works

```text
💬 User Request
      ↓
🤖 TaskPilot Assistant
      ↓
🧠 Intent & Tool Selection
      ↓
🔧 Validated Python Tool
      ↓
🗂️ Task Manager + JSON Storage
      ↓
🛡️ Result Validation
      ↓
📊 Structured Response + Report
```

The project works immediately in **deterministic demo mode** and can optionally integrate with **OpenAI function/tool calling**.

---

# ✨ Core Capabilities

| Capability | Description |
|---|---|
| ➕ Create tasks | Create structured tasks with priority levels |
| 📋 List tasks | Retrieve stored tasks |
| ✏️ Update tasks | Modify existing task information |
| ✅ Complete tasks | Mark tasks as completed |
| 🗑️ Delete tasks | Safely remove tasks |
| 📊 Task summaries | Generate task and priority breakdowns |
| 🛡️ Validation | Validate domain and result data with Pydantic |
| 💾 Persistence | Store task data locally using JSON |
| 🤖 Tool calling | Optional OpenAI-powered tool selection |
| 📄 Reporting | Generate human-readable task reports |
| 📝 Logging | Record application activity |

---

# 🏗️ Architecture

```text
src/
├── 🤖 assistant.py          Request interpretation + optional AI provider
├── 🔧 tools.py              Tool contracts and execution dispatch
├── 🗂️ task_manager.py       Business logic and JSON persistence
├── 📋 models.py             Pydantic domain models
├── 🛡️ result_validator.py   Response validation
├── 📄 report_generator.py   Human-readable reports
├── 📝 logger.py             Application logging
└── ▶️ main.py               Application entry point
```

### 🧩 Design Principles

- Modular architecture
- Separation of concerns
- Structured validation boundaries
- Testable external dependencies
- Safe local persistence
- Clear error handling

---

# 🚀 Installation

```powershell
cd TaskPilot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` only when you need local configuration.

> 🔐 Never commit your real `.env` file or API keys.

---

# ▶️ Run TaskPilot

Because the project uses Python package-relative imports, run it as a module:

```powershell
python -m src.main
```

You can also use interactive mode:

```powershell
python -m src.main --interactive
```

### 💬 Example Requests

```text
Create a high priority task called Finish proposal
Create a low priority task called Book team meeting
List my tasks
Complete task task_abc123
Show my task summary
Delete task task_abc123
```

---

# 🤖 Optional OpenAI Tool Calling

TaskPilot can optionally route requests through OpenAI function/tool calling.

Configure your local environment:

```text
TASKPILOT_MODE=openai
OPENAI_API_KEY=your_api_key_here
```

The AI layer selects tools, while the same validated Python tool layer remains responsible for executing the actual business operations.

### 🛡️ Testing Boundary

The automated test suite uses mocked AI boundaries, so tests do **not require live API calls**.

---

# 🧪 Testing

Run the complete automated test suite from the `TaskPilot` folder:

```powershell
pytest
```

## 🟢 Current Result

**17 automated tests passed successfully.**

The test suite covers:

- Task CRUD operations
- Priority and status validation
- Missing-task handling
- Task summary calculations
- Tool execution
- Deterministic request routing
- Mocked AI tool calling
- Result validation
- Report generation

---

# 🛠️ Technology Stack

`Python` • `Pydantic` • `OpenAI Tool Calling` • `JSON` • `python-dotenv` • `pytest` • `unittest.mock` • `logging`

---

# 💼 Skills Demonstrated

- 🐍 Python application architecture
- 🤖 AI assistants and tool/function calling
- 🛡️ Pydantic data validation
- 🔧 Tool design and execution layers
- 💾 Local data persistence
- ⚠️ Error handling
- 📝 Logging
- 🧪 Automated testing
- 🖥️ CLI application design

---

# 🔮 Future Improvements

- 👥 User accounts
- 🗄️ SQLite or PostgreSQL persistence
- 🔐 Authentication and authorization
- 📜 Audit trails
- 🧠 Richer natural-language task updates
- 🌐 REST API interface
- 🖥️ Web application interface

---

## 📌 Project Status

🟢 **Complete and tested**

**17 automated tests • End-to-end workflow verified • Portfolio-ready architecture** 🚀
