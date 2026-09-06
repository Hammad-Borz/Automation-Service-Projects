# TaskPilot — AI Business Assistant

TaskPilot is a portfolio-ready Python service that turns business requests into safe, validated task operations. It works immediately in deterministic demo mode and can optionally route requests through OpenAI function calling.

## Business problem

Teams lose time moving simple work requests between chat, email, and task lists. TaskPilot demonstrates a small but realistic assistant that understands a request, selects an action, persists the result locally, and returns a dependable structured response.

## Features

- Create, list, update, complete, and delete tasks
- Priority and status validation with Pydantic
- Atomic local JSON persistence with safe missing-task handling
- Deterministic, API-key-free command interpretation
- Optional OpenAI tool-calling adapter, with no live API calls in tests
- Structured tool/assistant result validation, logging, and text reports

## Architecture and workflow

```text
User request → Assistant → Intent/tool selection → Python tool
     ↑                                                ↓
Structured response ← Result validation ← Task manager / JSON store
```

```text
src/
  assistant.py          demo parser + optional OpenAI provider
  tools.py              tool contracts and execution dispatch
  task_manager.py       business logic and JSON persistence
  models.py             Pydantic domain models
  result_validator.py   response boundary checks
  report_generator.py   human-readable reports
  logger.py             local file logging
```

## Installation

```bash
cd TaskPilot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` only if you want to configure a mode or an API key. Do not commit `.env`.

## Run it

```bash
python -m src.main
python -m src.main --interactive
pytest
```

Demo mode is the default and understands clear requests such as:

```text
Create a high priority task called Finish proposal
List my tasks
Complete task task_abc123
Delete task task_abc123
Show my task summary
```

## Optional OpenAI tool calling

Set `TASKPILOT_MODE=openai` and `OPENAI_API_KEY` in your local `.env` or shell environment. The OpenAI adapter provides the model with function schemas, receives a tool selection, and then executes the same validated Python tool layer used by demo mode. The test suite uses a mock provider, never an external API.

## Testing

The suite covers task CRUD, missing data, summary calculations, tools, deterministic routing, mocked tool calling, validation, and report generation. Tests use pytest-managed isolated storage and a project-local pytest temp directory to avoid Windows system-temp permission problems.

## Skills demonstrated

Python architecture, Pydantic validation, tool/function calling, persistence, error handling, logging, testing, dependency boundaries, and CLI design.

## Future improvements

Add user accounts, a SQLite/PostgreSQL repository, richer natural-language updates, audit trails, authentication, and a web/API interface.
