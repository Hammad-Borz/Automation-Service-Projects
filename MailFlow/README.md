# 📧 MailFlow

## 1. Project Title

**MailFlow — Intelligent Email Automation System**

A portfolio-focused Python automation project for processing inbound business emails through a structured, explainable, and safe-by-default workflow.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-12%20Passing-16A34A)
![Mode](https://img.shields.io/badge/Demo%20Mode-Safe-7C3AED)
![Status](https://img.shields.io/badge/Status-Complete-16A34A)

---

## 2. One-Line Description

> **MailFlow classifies, prioritizes, applies business rules to, and prepares responses for inbound emails while keeping external side effects disabled in demo mode.**

---

## 3. Problem

Business teams receive recurring **support requests, sales inquiries, invoices, urgent operational messages, newsletters, and general emails**.

Manual triage creates several practical problems:

- 🚨 Important messages can be missed.
- ⏳ Repetitive classification consumes staff time.
- 📨 Responses can become inconsistent.
- ⚠️ Uncontrolled automation can create unwanted external side effects.
- 🔍 Manual processing makes it harder to apply consistent business rules.

MailFlow addresses the processing and triage layer while keeping the automation behavior explicit and testable.

---

## 4. Solution

MailFlow implements a modular email-processing pipeline:

1. 📥 Receive or load email messages.
2. 🔎 Parse and normalize messages.
3. 🏷️ Classify each message.
4. 🚦 Assign a priority.
5. ⚙️ Evaluate configurable automation rules.
6. ✍️ Generate a deterministic response draft when requested.
7. 📋 Produce a structured processing result.
8. 🔒 Keep demo-mode external side effects disabled.

The project separates email ingestion, classification, prioritization, rules, response generation, and delivery so individual components can be replaced or extended independently.

---

## 5. Key Features

### 📥 Email Ingestion

- Local deterministic demo email provider.
- IMAP reader for real mailbox ingestion.
- IMAP connection supports SSL configuration.
- Mailbox selection is configurable.
- IMAP messages are selected with `readonly=True`.

### 🏷️ Email Classification

Transparent weighted keyword classification supports:

- `urgent`
- `support`
- `sales`
- `newsletter`
- `invoice`
- `general`

The classifier is implemented as a replaceable component rather than being coupled to the workflow.

### 🚦 Priority Detection

Messages are assigned:

- 🔴 **High**
- 🟡 **Medium**
- 🟢 **Low**

Priority decisions use category, sender, subject, and body signals.

### ⚙️ Automation Rules

The default rule engine can:

- Mark messages as processed.
- Flag high-priority messages.
- Request a response draft.
- Prepare a notification.

### ✍️ Response Generation

- Deterministic local response generator.
- Category-specific draft responses.
- Provider interface for future AI/LLM implementations.
- No paid API is required for the demo implementation.

### 📤 Guarded SMTP Delivery

- SMTP delivery is implemented behind a dedicated sender.
- Demo mode prevents external delivery.
- Real delivery requires demo mode to be disabled and SMTP credentials to be configured.
- TLS can be enabled for SMTP connections.

### 🔐 Safe Configuration

- Environment-based configuration.
- Pydantic settings validation.
- `SecretStr` for password/API-key fields.
- Demo mode enabled by default.

### 🧪 Testing

The project includes **12 automated tests** covering configuration, parsing, classification, prioritization, automation rules, response generation, and workflow orchestration.

---

## 6. How It Works

For the normal local demo:

```text
📥 Demo Email Dataset
        │
        ▼
📨 Email Reader
        │
        ▼
🔎 Parse / Normalize
        │
        ▼
🏷️ Classifier
        │
        ▼
🚦 Prioritizer
        │
        ▼
⚙️ Rule Engine
        │
        ├── mark_processed
        ├── flag_high_priority
        ├── generate_response
        └── prepare_notification
        │
        ▼
✍️ Response Generator
        │
        ▼
📋 Processing Result
        │
        ▼
📝 Logging / CLI Output
```

The same workflow abstraction accepts injected components, so the processing logic is not tied to the demo reader.

---

## 7. Architecture / Workflow

### 🧩 Architectural Components

| Component | Responsibility |
|---|---|
| `email_reader.py` | Demo and IMAP ingestion boundary |
| `email_parser.py` | MIME parsing and email normalization |
| `classifier.py` | Transparent category classification |
| `prioritizer.py` | Priority assignment |
| `automation_rules.py` | Rule matching and action results |
| `response_generator.py` | Response-provider interface and demo generator |
| `email_sender.py` | Guarded SMTP delivery |
| `workflow.py` | Central processing orchestration |
| `models.py` | Domain models and validated contracts |
| `config.py` | Environment-backed runtime configuration |
| `logger.py` | Logging configuration |
| `demo_data.py` | Local demo messages |

### 🔄 Processing Boundary

```text
External / Demo Input
        │
        ▼
┌─────────────────────┐
│   Email Reader      │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│   Email Workflow    │
├─────────────────────┤
│ Classification      │
│ Prioritization      │
│ Rule Evaluation     │
│ Response Generation │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Processing Result   │
└──────────┬──────────┘
           ▼
     Logging / Output

SMTP delivery is a separate guarded boundary.
```

---

## 8. Technologies

| Category | Technology |
|---|---|
| 🐍 Language | Python 3.11+ |
| 🛡️ Data validation | Pydantic |
| 📥 IMAP | Python `imaplib` |
| 📤 SMTP | Python `smtplib` |
| ✉️ Email parsing | Python `email` package |
| 🔐 Configuration | `python-dotenv` |
| 🧪 Testing | `pytest` |
| 📝 Logging | Python `logging` |

Runtime dependencies are intentionally lightweight; the project does not require a database or external AI API for its demo workflow.

---

## 9. Project Structure

```text
MailFlow/
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── pytest.ini
│
├── data/
│   └── .gitkeep
│
├── logs/
│   └── .gitkeep
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── exceptions.py
│   ├── logger.py
│   ├── email_reader.py
│   ├── email_parser.py
│   ├── email_sender.py
│   ├── classifier.py
│   ├── prioritizer.py
│   ├── automation_rules.py
│   ├── response_generator.py
│   ├── workflow.py
│   └── demo_data.py
│
└── tests/
    ├── conftest.py
    ├── test_automation_rules.py
    ├── test_classifier.py
    ├── test_config.py
    ├── test_email_parser.py
    ├── test_prioritizer.py
    ├── test_response_generator.py
    └── test_workflow.py
```

---

## 10. Installation

### 1️⃣ Clone the portfolio repository

```bash
git clone https://github.com/Hammad-Borz/Automation-Service-Projects.git
cd Automation-Service-Projects/MailFlow
```

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3️⃣ Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## 11. Configuration

MailFlow reads configuration from `MAILFLOW_*` environment variables.

Create a local `.env` from the supplied example:

```bash
cp .env.example .env
```

### Safe default

```text
MAILFLOW_DEMO_MODE=true
```

### Main configuration groups

- `MAILFLOW_DEMO_MODE`
- `MAILFLOW_LOG_LEVEL`
- `MAILFLOW_LOG_FILE`
- `MAILFLOW_IMAP_*`
- `MAILFLOW_SMTP_*`
- `MAILFLOW_RESPONSE_PROVIDER`
- `MAILFLOW_AI_API_KEY`

### Important security boundary

Do not commit real passwords, SMTP credentials, or API keys.

When demo mode is disabled, the application requires the necessary SMTP/IMAP credentials for the corresponding real integration.

---

## 12. Usage

### ▶️ Run the local demo

```bash
python -m src.main
```

The demo:

1. Loads local sample emails.
2. Processes them through the workflow.
3. Displays category and priority.
4. Displays the actions generated by the rule engine.
5. Displays response drafts when requested.
6. Confirms that no real email was sent.

### 🧪 Run tests

```bash
pytest
```

Expected project result:

```text
12 passed
```

---

## 13. Example

A representative demo flow looks like:

```text
MailFlow - Intelligent Email Automation System
==================================================
Demo mode: True | Received: 5 emails

[HIGH  ] urgent     | URGENT: production checkout outage
         Actions: mark_processed, flag_high_priority,
                  generate_response, prepare_notification

[MEDIUM] support    | Unable to export my report
         Draft: Thanks for reaching out. Our support team
                will review the issue and follow up shortly.

[LOW   ] newsletter | Weekly newsletter
         Actions: mark_processed

Processing complete. No real emails were sent.
```

The exact output is generated by the current demo implementation; the project uses deterministic demo response generation rather than an external LLM.

---

## 14. Screenshots

> 🟡 **Reserved area — screenshots will be added later.**

Planned visual proof:

- 📥 Demo email input / received-message view.
- 🏷️ Classification and priority results.
- ⚙️ Generated automation actions.
- ✍️ Response draft output.
- 🔒 Demo-mode safety behavior.
- 🧪 Test execution result.
- 📝 Log output where useful.

---

## 15. Demo Video / GIF

> 🟡 **Reserved area — demo video/GIF will be added later.**

### Planned demonstration

```text
Start MailFlow
      ↓
Load demo emails
      ↓
Classify
      ↓
Prioritize
      ↓
Apply rules
      ↓
Generate draft
      ↓
Show structured results
      ↓
Confirm no real email was sent
```

A later portfolio demo can also show the guarded boundary between processing logic and real SMTP delivery.

---

## 16. Results / Benefits

### 🧪 Current Verification

- **12 automated tests** are documented for the project.
- Demo mode provides a local workflow without external email delivery.
- IMAP ingestion is isolated behind an email-reader abstraction.
- Classification uses transparent keyword scoring.
- Priority assignment is deterministic and explainable.
- Automation rules are represented as explicit rule objects.
- Response generation has a replaceable provider interface.
- SMTP delivery is isolated and guarded by demo mode.
- Configuration is environment-backed and secret fields use Pydantic `SecretStr`.

### 💼 Portfolio / Service Relevance

MailFlow demonstrates practical capabilities in:

`Python` • `Email Automation` • `IMAP` • `SMTP` • `Pydantic` • `Workflow Automation` • `Environment Configuration` • `Logging` • `pytest`

---

## 17. Limitations

The current implementation has deliberate boundaries:

- The demo workflow uses deterministic local sample data.
- The classifier is rule/keyword based rather than an AI classifier.
- The demo response generator is deterministic rather than LLM-generated.
- There is no database-backed processing history.
- There is no production web dashboard.
- The current project does not implement OAuth2 mailbox authentication.
- Production deployment, monitoring, mailbox pagination, and incremental processing are not implemented.

These are documented extension boundaries rather than capabilities currently claimed by the project.

---

## 18. Future Improvements

Potential next iterations include:

- 🔑 OAuth2 authentication for supported email providers.
- 📚 Mailbox pagination and incremental processing.
- 🗄️ Persistent storage with idempotency keys.
- 👤 Human approval queues for outbound actions.
- 🤖 Production AI/LLM response providers.
- 📊 Metrics and observability.
- 🌐 Web dashboard.
- ⚡ Integration with workflow automation platforms.

---

## 19. License

No license file is currently documented for MailFlow.

Until a license is added to the repository, users should not assume that the project is released under an open-source license.

---

## 20. Author / Contact

**Hammad Borz**

> Python • AI Automation • API Integration • Data Automation • Automation Systems

MailFlow is part of the **Automation-Service-Projects** portfolio and is positioned as a service-specific email automation implementation.

---

### 🔗 Repository

[Automation-Service-Projects](../)

### 📌 Project

[MailFlow](./)
