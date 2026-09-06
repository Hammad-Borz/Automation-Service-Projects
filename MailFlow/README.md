# MailFlow — Intelligent Email Automation System

MailFlow is a modular, safe-by-default Python system for turning an inbound email queue into prioritized, explainable work. It demonstrates production-minded email ingestion, classification, automation rules, response drafting, and guarded SMTP delivery without requiring paid APIs or real credentials.

## The business problem

Teams lose time triaging repetitive support, sales, billing, and operational messages. Important requests can be buried, responses become inconsistent, and automations that send too aggressively create operational and security risk.

## The solution

MailFlow normalizes incoming messages, classifies them with transparent rules, scores priority, applies configurable actions, and records an auditable processing result. Demo mode uses realistic local messages and never sends email.

## Key features

- Configurable IMAP ingestion with read-only mailbox access
- Local demo provider requiring no credentials
- Categories: urgent, support, sales, newsletter, invoice, and general
- Explainable high/medium/low prioritization
- Pydantic validation for domain models
- Configurable automation rules and action results
- Deterministic response generator with an interface for future LLM providers
- SMTP sender guarded by explicit non-demo configuration
- JSON-structured console and file logging
- Focused pytest suite

## Workflow

```text
IMAP or demo provider -> parse and validate -> classify -> prioritize
       -> evaluate rules -> draft response (optional) -> record result
```

## Architecture

- `email_reader.py`: provider boundary for Demo and IMAP readers
- `email_parser.py`: standard-library MIME parsing
- `classifier.py`: replaceable rule-based classifier
- `prioritizer.py`: category and signal scoring
- `automation_rules.py`: configurable rule matching and safe action execution
- `response_generator.py`: provider interface plus deterministic implementation
- `email_sender.py`: SMTP delivery with demo-mode guard
- `workflow.py`: central orchestration boundary
- `models.py`: validated domain contracts

## Project structure

```text
MailFlow/
├── .env.example
├── README.md
├── requirements.txt
├── pytest.ini
├── data/                 # local runtime data, ignored by Git
├── logs/                 # structured runtime logs, ignored by Git
├── src/
│   ├── config.py, models.py, logger.py, exceptions.py
│   ├── email_reader.py, email_parser.py, email_sender.py
│   ├── classifier.py, prioritizer.py, automation_rules.py
│   ├── response_generator.py, workflow.py, demo_data.py, main.py
└── tests/
```

## Technologies

Python 3.11+, Pydantic 2, python-dotenv, standard-library `imaplib`/`smtplib`, and pytest.

## Installation

```bash
cd MailFlow
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and adjust `MAILFLOW_*` values. The default `MAILFLOW_DEMO_MODE=true` is intentional. Set it to `false` only when SMTP credentials and a controlled delivery environment are ready. IMAP and SMTP passwords are read from environment variables and are never stored in source code.

`MAILFLOW_RESPONSE_PROVIDER=demo` selects the local response provider. The `ResponseGenerator` interface is the extension point for an approved AI provider later.

## Run the demo

```bash
python -m src.main
```

Example output:

```text
Demo mode: True | Received: 5 emails
[HIGH  ] urgent     | URGENT: production checkout outage
         Actions: mark_processed, flag_high_priority, generate_response, prepare_notification
[MEDIUM] support    | Unable to export my report
         Draft: Thanks for reaching out. Our support team will review the issue and follow up shortly.
Processing complete. No real emails were sent.
```

## Run tests

```bash
pytest
```

## Security notes

- Demo mode is the default and SMTP delivery returns without sending.
- Secrets belong in environment variables or a secret manager, never in Git.
- IMAP access is read-only and does not delete or mutate messages.
- Notification and forwarding actions prepare outcomes only; they do not create external side effects in the demo.
- Review generated drafts and rules before enabling production delivery.

## Future improvements

- Add OAuth2 IMAP authentication and mailbox pagination
- Persist processing state in a database with idempotency keys
- Add an approval queue and policy-based outbound controls
- Add a production AI response provider behind the existing interface
- Add metrics, tracing, and a web dashboard

MailFlow is designed as a portfolio-quality foundation: readable modules, explicit boundaries, testable behavior, and operationally cautious defaults.
