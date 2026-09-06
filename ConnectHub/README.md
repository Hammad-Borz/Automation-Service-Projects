# 🔌 ConnectHub — Multi-API Integration & Automation System

> **A professional Python automation project for connecting REST APIs through a reliable fetch → validate → transform → send workflow.**

ConnectHub demonstrates a practical API integration pipeline that retrieves records from a source REST API, validates them individually, transforms them into a destination schema, and sends valid records to another REST API. Individual failures are handled without unnecessarily stopping the entire batch.

---

## 🚀 Project Highlights

- 🔗 **Reusable API client** supporting GET and POST requests
- 🛡️ **Clear error handling** for HTTP, network, and invalid JSON failures
- ✅ **Record-level validation** with actionable error messages
- 🔄 **Schema transformation** between source and destination APIs
- ⚙️ **End-to-end orchestration** through a dedicated integration service
- 🧩 **Partial-failure resilience** so valid records can continue processing
- 📊 **Structured execution summary** with key processing metrics
- 📝 **File-based logging** without duplicate handlers
- 🧪 **11 automated tests** using `pytest` and mocked HTTP behavior
- 🔐 **Environment-based configuration** with no secrets stored in the repository

---

## 🧠 The Problem It Solves

Businesses frequently need to move data between systems with different APIs and different data formats.

ConnectHub provides a reusable foundation for this workflow:

```text
Source REST API
       │
       ▼
  Fetch Records
       │
       ▼
 Validate Records
   │           │
   │           └── Invalid records → Log & Skip
   ▼
Transform Records
       │
       ▼
Destination REST API
   │           │
   │           └── Failed requests → Log & Count
   ▼
Execution Summary
```

---

## 🏗️ Architecture

```text
src/
├── api_client.py          # Reusable HTTP client and custom API errors
├── data_validator.py      # Source-record validation
├── data_transformer.py    # Source → destination schema conversion
├── integration_service.py # Complete workflow orchestration
├── logger.py              # Application logging configuration
└── main.py                # Command-line entry point
```

### 🔄 Data Flow

```text
Source API
   ↓
APIClient.get()
   ↓
DataValidator
   ↓
DataTransformer
   ↓
APIClient.post()
   ↓
Destination API
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Core application development |
| 🌐 `requests` | REST API communication |
| 🔐 `python-dotenv` | Environment-based configuration |
| 🧪 `pytest` | Automated testing |
| 🎭 `unittest.mock` | Mocking HTTP behavior during tests |
| 📝 `logging` | Operational and error logging |

---

## 📁 Project Structure

```text
ConnectHub/
├── src/
│   ├── api_client.py
│   ├── data_validator.py
│   ├── data_transformer.py
│   ├── integration_service.py
│   ├── logger.py
│   └── main.py
│
├── tests/
│   ├── test_api_client.py
│   ├── test_data_validator.py
│   ├── test_data_transformer.py
│   └── test_integration_service.py
│
├── logs/
├── reports/
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 📋 Workflow

ConnectHub processes records through four core stages:

### 1️⃣ Fetch
Retrieves JSON data from the configured source REST API.

### 2️⃣ Validate
Each source record must be a dictionary containing:

```text
id
name
email
```

Invalid records are retained in the validation results, logged, and excluded from sending.

### 3️⃣ Transform
Valid records are converted into the destination schema:

```json
{
  "external_id": 123,
  "full_name": "Ada Lovelace",
  "contact_email": "ada@example.com"
}
```

### 4️⃣ Send
Each transformed record is sent individually to the destination REST API. A failure for one record is counted and logged without automatically stopping the remaining records.

---

## 📊 Execution Summary

After processing, the integration returns a structured summary:

```python
{
    "total_fetched": 3,
    "valid_records": 2,
    "invalid_records": 1,
    "successfully_sent": 1,
    "failed_to_send": 1,
}
```

This makes the outcome easy to inspect and integrate into larger automation systems.

---

## ⚙️ Installation

### Clone or navigate to the project

```bash
cd ConnectHub
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate it on Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration

Copy `.env.example` to `.env`:

```text
.env.example → .env
```

Then configure your endpoints:

```env
SOURCE_API_URL=https://your-source-api.example/data
DESTINATION_API_URL=https://your-destination-api.example/data
```

> ⚠️ Never commit your `.env` file if it contains credentials or sensitive configuration. ConnectHub uses environment-based configuration to keep secrets out of source code.

---

## ▶️ Usage

Run the application from the ConnectHub project directory:

```bash
python src/main.py
```

The application will:

1. Fetch records from the source API.
2. Validate each record.
3. Skip and log invalid records.
4. Transform valid records.
5. Send transformed records to the destination API.
6. Display a processing summary.

---

## 🧪 Testing

Run the complete automated test suite:

```bash
pytest
```

### Current test coverage includes

- Successful GET requests
- Successful POST requests
- HTTP failures
- Network failures
- Invalid JSON responses
- Invalid source records
- Data transformation
- Successful end-to-end integration
- Partial sending failures

### Latest verified result

```text
11 passed
```

---

## 🛡️ Error Handling

The project defines clear API-related error categories:

- `APIClientError`
- `APIHTTPError`
- `APINetworkError`
- `APIResponseError`

This separation makes failures easier to understand, log, test, and handle within automation workflows.

---

## 💼 Portfolio Value

ConnectHub demonstrates practical skills relevant to freelance and client automation work:

- API integration
- REST API communication
- Python automation
- Data validation
- Data transformation
- Error handling
- Environment configuration
- Logging
- Automated testing
- Modular software architecture

The architecture can be extended for real-world integrations such as CRM synchronization, customer-data migration, lead transfer, reporting pipelines, and other cross-platform automation workflows.

---

## 🔮 Future Improvements

Potential production-level extensions include:

- 🔑 API authentication and authorization
- 🔁 Retry and exponential backoff
- 📄 Pagination support
- 🚦 Rate-limit handling
- 🆔 Idempotency keys
- 💾 Persistent storage for failed records
- 📨 Dead-letter queues
- 🔔 Webhook integrations
- 📊 Advanced reporting and monitoring

---

## 👨‍💻 Author

**Hammad Borz**

Python • AI Automation • API Integration • Automation Systems

---

### ⭐ If you find this project useful, feel free to explore the code and its architecture.