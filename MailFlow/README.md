# 📧 MailFlow
## Intelligent Email Automation System

> **A modular, safe-by-default Python system for turning inbound emails into prioritized, explainable, and actionable business workflows.**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-12_Passing-16A34A)
![Mode](https://img.shields.io/badge/Demo_Mode-Safe-7C3AED)
![Status](https://img.shields.io/badge/Status-Complete-16A34A)

---

# 🎯 The Business Problem

Business teams receive a constant flow of **support requests, sales inquiries, invoices, operational alerts, and newsletters**.

Without automation:

- 🚨 Important messages can be missed.
- ⏳ Teams spend time manually triaging repetitive emails.
- 📨 Responses can become inconsistent.
- ⚠️ Overly aggressive automation can create operational and security risks.

---

# 💡 The Solution

**MailFlow** processes incoming emails through a structured automation pipeline.

It normalizes messages, classifies their purpose, assigns priority, applies automation rules, optionally prepares a response draft, and records the processing result.

## 🔒 Safe by Default

The built-in demo mode uses realistic local sample emails and **never sends real email**.

---

# ⚙️ System Workflow

```text
📥 Incoming Email
        ↓
🔎 Parse & Validate
        ↓
🏷️ Classify
        ↓
🚦 Prioritize
        ↓
⚙️ Apply Automation Rules
        ↓
✍️ Generate Response Draft (Optional)
        ↓
📋 Record Processing Result
```

---

# ✨ Key Features

## 📥 Email Ingestion

- Configurable IMAP email ingestion
- Local demo provider requiring no credentials
- Read-only mailbox access architecture

## 🏷️ Intelligent Classification

Supported categories include:

- 🚨 `urgent`
- 🛠️ `support`
- 💼 `sales`
- 📰 `newsletter`
- 🧾 `invoice`
- 📩 `general`

The classifier is designed as a replaceable component, allowing a future AI-based implementation.

## 🚦 Priority Detection

Emails are assigned:

- 🔴 **High priority**
- 🟡 **Medium priority**
- 🟢 **Low priority**

Priority decisions use category and message signals to keep the process explainable.

## ⚙️ Automation Rules

Configurable rules can produce actions such as:

- ✅ Mark as processed
- 🚩 Flag high-priority messages
- ✍️ Generate a response draft
- 🔔 Prepare a notification

## ✍️ Response Generation

MailFlow includes a deterministic response generator that works without paid APIs or credentials.

A provider interface also creates a clean extension point for an approved AI or LLM provider later.

## 📤 Guarded Email Delivery

The SMTP sender is architected for real delivery, while demo mode prevents external sending.

---

# 🧠 Architecture

| Module | Responsibility |
|---|---|
| `email_reader.py` | Demo and IMAP provider boundary |
| `email_parser.py` | MIME parsing and normalization |
| `classifier.py` | Replaceable email classification |
| `prioritizer.py` | Priority scoring |
| `automation_rules.py` | Rule matching and action execution |
| `response_generator.py` | Response-provider interface and demo implementation |
| `email_sender.py` | Guarded SMTP delivery |
| `workflow.py` | Central orchestration |
| `models.py` | Validated domain contracts |
| `config.py` | Environment-based configuration |

---

# 📁 Project Structure

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

# 🛠️ Technology Stack

| Category | Technology |
|---|---|
| 🐍 Language | Python |
| 🛡️ Validation | Pydantic |
| 📥 Email Reading | IMAP / `imaplib` |
| 📤 Email Delivery | SMTP / `smtplib` |
| 🔐 Configuration | `python-dotenv` |
| 🧪 Testing | `pytest` |
| 📝 Logging | Python `logging` |

---

# 🚀 Installation

## 1️⃣ Clone the repository

```bash
git clone https://github.com/Hammad-Borz/Automation-Service-Projects.git
```

## 2️⃣ Navigate to MailFlow

```bash
cd Automation-Service-Projects/MailFlow
```

## 3️⃣ Create a virtual environment

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

## 4️⃣ Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

# ⚙️ Configuration

Copy the example configuration:

```bash
cp .env.example .env
```

The default configuration intentionally enables demo mode:

```text
MAILFLOW_DEMO_MODE=true
```

Only disable demo mode after configuring a controlled environment with the required credentials.

### 🔐 Security Rule

**Never commit real credentials, passwords, API keys, or SMTP secrets to GitHub.**

MailFlow reads sensitive values from environment variables.

---

# ▶️ Run the Demo

```bash
python -m src.main
```

### Example workflow output

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

---

# 🧪 Run the Tests

```bash
pytest
```

## 🟢 Current Result

```text
12 passed
```

The test suite covers important workflow components, including configuration, parsing, classification, prioritization, automation rules, response generation, and workflow orchestration.

---

# 🔒 Security & Safety

MailFlow is deliberately designed with cautious operational defaults:

- 🔐 Secrets are stored outside source code.
- 🧪 Demo mode is enabled by default.
- 📤 SMTP delivery is guarded in demo mode.
- 📥 IMAP access is designed to be read-only.
- 🔔 Notification and forwarding actions can prepare outcomes without creating demo-mode external side effects.
- 👀 Generated drafts and automation rules should be reviewed before production use.

---

# 🔮 Future Improvements

- 🔑 OAuth2 authentication for email providers
- 📚 Mailbox pagination and incremental processing
- 🗄️ Database persistence with idempotency keys
- 👤 Human approval queues for outbound actions
- 🤖 Production AI response providers
- 📊 Metrics and observability
- 🌐 Web dashboard
- ⚡ Integration with workflow automation platforms

---

# 🏆 Portfolio Value

MailFlow demonstrates practical skills relevant to **business automation and freelance services**:

`Python` • `Email Automation` • `IMAP` • `SMTP` • `Pydantic` • `Workflow Automation` • `Environment Configuration` • `Logging` • `pytest`

---

## 👨‍💻 Author

**Hammad Borz**

> Python • AI Automation • API Integration • Data Automation • Automation Systems

⭐ **MailFlow is designed as a portfolio-quality foundation with readable modules, explicit boundaries, testable behavior, and safe operational defaults.**