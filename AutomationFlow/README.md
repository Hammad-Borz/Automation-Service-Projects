# ⚙️ AutomationFlow — n8n & Make Business Automation

> **Service Focus:** n8n & Make Workflow Automation  
> **Implementation:** n8n + Make + Python/FastAPI  
> **Status:** Complete / Portfolio Ready

AutomationFlow demonstrates how a practical **lead-processing business requirement** can be implemented across two automation platforms: **n8n** and **Make**, with a lightweight Python/FastAPI service providing deterministic lead analysis for the n8n implementation.

---

## 1. 📌 Project Title

**AutomationFlow — n8n & Make Business Automation**

---

## 2. 📝 One-Line Description

A webhook-driven lead-processing automation system that validates, classifies, scores, routes, and returns structured results using n8n, Make, and a supporting Python API.

---

## 3. 🔴 Problem

Businesses commonly receive leads from forms, websites, CRMs, and other sources that require repetitive processing before they can be routed to the appropriate business workflow.

A typical requirement includes:

- Receiving structured lead data
- Validating required information
- Identifying the lead category
- Determining priority
- Routing the lead according to business rules
- Returning a predictable automation result

Without a structured workflow, these steps can become repetitive, inconsistent, and difficult to maintain.

---

## 4. 🟢 Solution

AutomationFlow turns that requirement into a documented, webhook-driven workflow.

It provides **two implementations of the same business objective**:

- **n8n:** workflow orchestration with an HTTP call to the Python lead-processing service.
- **Make:** native Make webhook, classification, routing, and response logic.

The separation between workflow orchestration and deterministic processing logic keeps the system understandable and reusable.

---

## 5. 🔑 Key Features

| Capability | Implementation |
|---|---|
| Webhook lead intake | n8n / Make |
| Field normalization | n8n |
| Email validation | n8n / Make |
| Lead classification | Python / Make |
| Priority calculation | Python |
| Lead scoring | Python |
| Conditional routing | n8n / Make |
| HTTP API integration | n8n → FastAPI |
| Structured JSON responses | n8n / Make / FastAPI |
| Exportable workflow artifacts | n8n JSON / Make blueprint |
| Safe portfolio execution | No required real-world notification credentials |

### Lead Categories

- `sales`
- `support`
- `billing`
- `general`

### Priority Levels

- `high`
- `medium`
- `low`

The Python processor produces a bounded score from **0–100** together with a human-readable classification reason.

---

## 6. 🔄 How It Works

### n8n Flow

```text
Lead Source
    ↓
Webhook
    ↓
Edit Fields
    ↓
Email Validation
    ├── Invalid → Webhook Response
    └── Valid
          ↓
   HTTP Request
          ↓
 Python Lead Processor
          ↓
    Priority Check
          ↓
    Action Preparation
          ↓
   Structured Response
```

### Make Flow

```text
Lead Source
    ↓
Custom Webhook
    ↓
Lead Classification
    ├── Invalid
    ├── Sales
    ├── Support
    ├── Billing
    └── General
          ↓
   Webhook Response
```

---

## 7. 🏗️ Architecture / Workflow

### High-Level Architecture

```text
                         BUSINESS LEAD
                              │
                              ▼
                    ┌───────────────────┐
                    │   Webhook Input   │
                    │     JSON Data     │
                    └─────────┬─────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
        ┌───────────────┐          ┌────────────────┐
        │      n8n      │          │      Make      │
        │ Orchestration │          │  Orchestration │
        └───────┬───────┘          └───────┬────────┘
                │                           │
                ▼                           ▼
        ┌───────────────┐          ┌────────────────┐
        │ Python/FastAPI│          │ Native Make    │
        │ Lead Processor│          │ Classification │
        └───────┬───────┘          └───────┬────────┘
                │                           │
                ▼                           ▼
        Lead Type / Score /         Lead Type / Routing
        Priority / Reason
                │                           │
                └─────────────┬─────────────┘
                              ▼
                    Structured JSON Result
```

### Architecture Boundary

The implementations intentionally differ at the processing layer:

- **n8n** uses the Python service through HTTP.
- **Make** performs classification and routing natively.
- The Make scenario does **not** call the local Python service because the cloud-hosted scenario cannot directly access the local Docker/Windows `host.docker.internal` endpoint.

### Python Processing Logic

```text
Lead Message + Source
        ↓
Keyword Groups
        ↓
Sales / Support / Billing Classification
        ↓
Base Score
        ↓
Source + Urgency Adjustments
        ↓
Final Score (0–100)
        ↓
Priority
        ↓
Structured JSON
```

---

## 8. 🧰 Technologies

| Technology | Role |
|---|---|
| **n8n** | Primary workflow orchestration |
| **Make** | Alternative native automation implementation |
| **Python** | Supporting business-logic layer |
| **FastAPI** | Python HTTP API |
| **Uvicorn** | Local ASGI server |
| **HTTP / JSON** | Workflow-to-service integration |
| **Docker** | Local n8n runtime |
| **Git / GitHub** | Version control and portfolio delivery |

---

## 9. 📁 Project Structure

```text
AutomationFlow/
├── README.md
│
├── docs/
│   ├── README.md
│   ├── architecture/
│   │   └── architecture.md
│   └── setup/
│       └── setup.md
│
├── make/
│   ├── README.md
│   └── scenarios/
│       └── automationflow-make-lead-processing.json
│
├── n8n/
│   ├── README.md
│   └── workflows/
│       └── automationflow-lead-processing.json
│
└── python/
    ├── README.md
    ├── app.py
    ├── processor.py
    └── requirements.txt
```

---

## 10. 🚀 Installation

### Prerequisites

- Python 3.10+
- Git
- Docker Desktop
- n8n Community Edition
- Make account for the Make implementation

### 1. Set Up the Python Service

From the `python/` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start the API:

```powershell
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

The local API is available at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

### 2. Start Local n8n

Create the persistent Docker volume:

```powershell
docker volume create n8n_data
```

Start n8n:

```powershell
docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n
```

Open:

```text
http://localhost:5678
```

### 3. Import the Workflow

Import:

```text
n8n/workflows/automationflow-lead-processing.json
```

Review the nodes, connections, and local service URL before running it.

---

## 11. ⚙️ Configuration

### Python Service

The Python service has no required secrets for the portfolio implementation.

The n8n HTTP Request node uses:

```text
http://host.docker.internal:8000/process-lead
```

This address is appropriate for the documented local Docker-to-host development setup and should be changed for another deployment environment.

### Make

The Make implementation is self-contained and uses native Make routing rather than the local Python service.

Its portable blueprint is:

```text
make/scenarios/automationflow-make-lead-processing.json
```

For production/client deployments, credentials should be managed through the target platform's credential or secret-management facilities rather than committed to source control.

---

## 12. ▶️ Usage

### Start the Python Service

```powershell
cd AutomationFlow\python
.\.venv\Scripts\Activate.ps1
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### Start n8n

```powershell
docker start n8n
```

Then open:

```text
http://localhost:5678
```

Import and open the AutomationFlow workflow.

For local testing, use the n8n test webhook path:

```text
POST /webhook-test/automationflow/leads
```

The Make implementation can be imported from its blueprint and configured inside the target Make environment.

---

## 13. 🧪 Example

### Example Lead Input

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "company": "Example Corp",
  "message": "We are interested in automation services and would like pricing.",
  "source": "website"
}
```

### Python API

The n8n workflow sends a valid lead to:

```text
POST /process-lead
```

The supporting service returns structured analysis containing:

```json
{
  "lead_type": "sales",
  "priority": "high",
  "score": 80,
  "reason": "Lead classified as sales based on message content. Calculated lead score: 80/100."
}
```

The exact score is determined by the processor's configured keyword and adjustment rules.

### Available Python Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Service health check |
| `POST` | `/process-lead` | Classify and score a lead |
| `POST` | `/notify-sales` | Prepare a sales notification result |

---

## 14. 📸 Screenshots

> **Reserved area — screenshots will be added later.**

### Planned Visual Evidence

```text
[ Screenshot area reserved ]

• n8n workflow canvas
• Make scenario
• FastAPI /docs
• Example webhook execution
• Structured automation response
```

---

## 15. 🎥 Demo Video / GIF

> **Reserved area — demo video/GIF will be added later.**

### Planned Demonstration

```text
[ Demo area reserved ]

Lead Input
   ↓
Webhook
   ↓
Validation
   ↓
Classification
   ↓
Priority
   ↓
Automation Result
```

---

## 16. 📊 Results / Benefits

AutomationFlow demonstrates a reusable automation pattern rather than a single hard-coded business interface.

### Demonstrated Capabilities

- **Webhook-driven automation** for structured lead intake.
- **Cross-platform workflow design** using both n8n and Make.
- **HTTP API integration** between n8n and a Python service.
- **Deterministic business rules** that are inspectable and reproducible.
- **Lead classification and prioritization** using structured processing logic.
- **Portable workflow artifacts** through exported n8n and Make files.
- **Safe portfolio execution** without requiring real customer credentials or live sales notifications.

### Portfolio / Freelancing Relevance

This project demonstrates the ability to translate a business requirement into:

```text
Business Requirement
        ↓
Workflow Design
        ↓
Platform Implementation
        ↓
API Integration
        ↓
Business Rules
        ↓
Structured Automation Result
```

---

## 17. 🔴 Limitations

The current implementation is intentionally scoped as a portfolio-grade local automation project.

- Lead classification is deterministic and keyword-based rather than AI/LLM-based.
- The Python service is designed for local development and demonstration.
- The n8n workflow uses a local Docker-to-host networking configuration.
- The Make implementation does not call the local Python service.
- Production authentication and authorization are not implemented.
- Production observability, rate limiting, persistent monitoring, and advanced retry handling are outside the current scope.
- Real external sales notifications are represented as prepared results rather than automatically sent messages.

---

## 18. 🔮 Future Improvements

Potential extensions include:

1. Add configurable AI/LLM-assisted lead classification.
2. Add persistent lead storage and processing history.
3. Add authentication for externally exposed API/webhook endpoints.
4. Add production-grade logging and observability.
5. Add configurable retry, timeout, and failure-handling policies.
6. Add CRM integrations for systems such as HubSpot or Salesforce.
7. Add real notification connectors behind explicit credentials and authorization.
8. Add automated tests for the Python processing layer and API endpoints.
9. Add deployment configurations for cloud-hosted n8n and FastAPI.
10. Add analytics for lead volume, categories, priorities, and routing outcomes.

---

## 19. 📄 License

No license file is currently included in this project directory.

Until an explicit repository license is added, the code should be treated as **all rights reserved** rather than assumed to be open-source licensed.

---

## 20. 👤 Author / Contact

**Hammad Borz**

- GitHub: [@Hammad-Borz](https://github.com/Hammad-Borz)
- Repository: [Automation-Service-Projects](https://github.com/Hammad-Borz/Automation-Service-Projects)

For portfolio or service inquiries, the repository provides the project architecture, workflow exports, setup documentation, and supporting Python implementation for technical review.

---

## 📚 Documentation

- [Architecture](docs/architecture/architecture.md)
- [Setup Guide](docs/setup/setup.md)
- [n8n Implementation](n8n/README.md)
- [Make Implementation](make/README.md)
- [Python Supporting Service](python/README.md)

---

> **Portfolio Note:** This README follows the project's 20-point professional README structure. **Points 14 and 15 are intentionally reserved** for the visual evidence that will be added during the later GitHub portfolio phases.
