# 📚 KnowledgeBase AI — Multi-Document RAG Assistant

> **A production-style Python RAG system that ingests PDF and DOCX files, builds a local knowledge base, retrieves relevant context, and produces grounded answers with source citations.**

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![RAG](https://img.shields.io/badge/AI-RAG-purple)
![Tests](https://img.shields.io/badge/Tests-32%20Passed-brightgreen)
![Mode](https://img.shields.io/badge/Demo-Offline-yellow)

---

## ✨ Overview

KnowledgeBase AI is a modular **Retrieval-Augmented Generation (RAG)** application for working with multiple documents. It converts supported files into chunked, embedded records, retrieves the most relevant context for a question, and generates answers that are grounded in the indexed knowledge base.

The project supports both:

- 🟢 **Demo mode** — deterministic, local, and offline
- 🤖 **OpenAI mode** — API-backed embeddings and answer generation

---

## 💼 The Business Problem

Organizations accumulate policy manuals, product guides, procedures, and operational documents that become difficult to search efficiently. Employees repeatedly ask questions, while generic AI systems can produce answers that are not supported by the actual documents.

A useful knowledge assistant should:

- 📄 Work with multiple documents
- 🔎 Retrieve passages relevant to the user's question
- 🛡️ Avoid fabricating information outside the available context
- 📌 Show where an answer came from
- 💬 Support follow-up questions during a conversation

---

## 💡 The Solution

KnowledgeBase AI implements the following RAG workflow:

```text
User Question
      ↓
Query Processing + Conversation History
      ↓
🔎 Retrieve Relevant Chunks
      ↓
📚 Build Grounded Context
      ↓
🤖 Answer Generation
      ↓
📌 Answer + Source Citations
```

The default demo mode uses local deterministic embeddings and an extractive answerer, allowing the project to run without external API calls.

---

## 🚀 Key Features

- 📄 Multi-document ingestion for **PDF** and **DOCX**
- 🧹 Document processing and text normalization
- ✂️ Configurable chunking with metadata preservation
- 🧠 Local or API-backed embedding architecture
- 🗄️ Local JSON-backed vector storage
- 🔎 Top-k similarity retrieval
- 🤖 Grounded RAG answers
- 📌 Source citations with document, chunk, and optional page information
- 💬 Session conversation history for follow-up questions
- 📚 Knowledge-base management: add, list, remove, and clear
- ⚠️ Robust validation and error handling
- 📝 Centralized logging
- 🧪 **32 automated tests passing** without requiring a live AI provider

---

## 🏗️ RAG Architecture

```text
PDF / DOCX Files
        │
        ▼
┌───────────────────┐
│ DocumentReader    │  Extract text + metadata
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ DocumentProcessor │  Normalize content
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Chunker           │  Create source-aware chunks
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ EmbeddingProvider │  Generate chunk vectors
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ VectorStore       │  Persist local knowledge base
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Retriever         │  Find relevant chunks
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ RAGPipeline       │  Build context + orchestrate answer
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ LLMClient         │  Generate grounded response
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ ResultValidator   │  Validate response + citations
└───────────────────┘
```

### Core Components

| Component | Responsibility |
|---|---|
| `document_reader` | Extract text from PDF/DOCX files and capture metadata. |
| `document_processor` | Normalize extracted text before indexing. |
| `chunker` | Split text into overlapping chunks with source identifiers. |
| `embeddings` | Provide local hashing or OpenAI embeddings. |
| `vector_store` | Persist documents, chunks, and vectors locally. |
| `retriever` | Embed queries and return ranked chunks. |
| `rag_pipeline` | Coordinate retrieval, generation, citations, and history. |
| `llm_client` | Isolate demo and OpenAI answer-generation implementations. |
| `conversation_manager` | Maintain session turns and support follow-up context. |
| `knowledge_base` | Add, list, remove, and clear indexed documents. |
| `result_validator` | Enforce the RAG response contract. |

---

## 📁 Project Structure

```text
KnowledgeBase-AI/
│
├── data/
│   ├── documents/          # Local indexed documents
│   └── vector_store/       # Generated knowledge-base data
│
├── logs/                   # Runtime logs
│
├── src/
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── exceptions.py
│   ├── logger.py
│   ├── document_reader.py
│   ├── document_processor.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── rag_pipeline.py
│   ├── llm_client.py
│   ├── conversation_manager.py
│   ├── knowledge_base.py
│   └── result_validator.py
│
├── tests/                  # Automated test suite
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## ⚙️ Technologies Used

| Area | Technology |
|---|---|
| 🐍 Language | Python 3.11+ |
| 🛡️ Validation | Pydantic v2 |
| ⚙️ Configuration | python-dotenv |
| 📕 PDF Processing | pypdf |
| 📘 DOCX Processing | python-docx |
| 🧠 Embeddings | Local hashing vectors or OpenAI embeddings |
| 🗄️ Vector Storage | JSON-backed cosine search |
| 🤖 Answer Generation | Demo extractive client or OpenAI |
| 🧪 Testing | pytest |

---

## 🛠️ Installation

From the `KnowledgeBase-AI` directory:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

For macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Copy the example environment file:

```powershell
copy .env.example .env
```

| Variable | Purpose |
|---|---|
| `KNOWLEDGEBASE_MODE` | `demo` or `openai` |
| `OPENAI_API_KEY` | Required only for OpenAI mode |
| `OPENAI_MODEL` | Chat model selection |
| `OPENAI_EMBEDDING_MODEL` | Embedding model selection |
| `CHUNK_SIZE` | Target chunk size |
| `CHUNK_OVERLAP` | Overlap between chunks |
| `TOP_K` | Number of retrieved chunks |
| `EMBEDDING_DIMENSION` | Local embedding dimension |

> 🔒 **Security:** Never commit `.env` files or API keys.

---

## ▶️ Run the Application

Run the complete demonstration:

```powershell
python -m src.main
```

### Available Modes

```powershell
# Offline demonstration mode
python -m src.main --mode demo

# Interactive mode
python -m src.main --interactive

# OpenAI-backed interactive mode
python -m src.main --mode openai --interactive
```

The standard demonstration:

1. 📄 Creates and indexes sample documents
2. 📚 Lists indexed knowledge-base documents
3. ❓ Answers grounded questions
4. 📌 Displays retrieved sources
5. 🚫 Demonstrates handling of an unanswerable question
6. 💬 Demonstrates follow-up context
7. 🗑️ Removes a document
8. 🧹 Clears the knowledge base

---

## 💬 Example Interaction

```text
Q: How many PTO days do employees receive?

A: Employees receive 20 days of paid time off (PTO) each calendar year.

Grounded: True

Sources:
  - acme_employee_handbook.pdf
    [chunk_a1b2c3d4e5f6, page 1]
```

### Unanswerable Question

```text
Q: What is the company's current stock price?

A: The indexed documents do not contain enough information to answer this question.

Grounded: False
```

This behavior is important because a RAG system should identify when the available documents **do not support an answer** instead of fabricating one.

---

## 🧪 Testing

Run the full automated test suite:

```powershell
pytest
```

### Current Verified Result

```text
32 passed
```

The tests use local hashing embeddings and scripted test doubles, so the normal test suite **does not require OpenAI or external API access**.

---

## 🎯 Skills Demonstrated

`Python` • `RAG` • `AI Automation` • `Document Processing` • `PDF` • `DOCX` • `Embeddings` • `Vector Search` • `Similarity Retrieval` • `OpenAI API` • `Pydantic` • `Dependency Injection` • `Testing` • `Error Handling` • `Modular Architecture`

---

## 🔮 Limitations & Future Improvements

- 🔍 Demo embeddings are lexical hashed n-grams rather than large-model semantic embeddings
- 🗄️ The JSON vector store is designed for small local knowledge bases
- 📄 PDF page citations are supported, while DOCX page mapping requires a future layout-aware reader
- 💬 Conversation history currently exists only for the active process session
- 🔐 No authentication or multi-user isolation yet
- 🌐 No web interface or API layer yet

### Possible Next Steps

- Persistent chat sessions
- Hybrid keyword + vector retrieval
- Chroma or FAISS vector-store integration
- Page-accurate citations directly inside answer text
- FastAPI service layer
- Web-based chat interface
- Multi-user authentication and isolated knowledge bases

---

## 🟢 Project Status

**Complete · Tested · Portfolio Ready**

> **32 automated tests passing, with successful end-to-end runtime verification.**

KnowledgeBase AI demonstrates a practical, modular RAG architecture suitable for portfolio presentation and future expansion into a production-grade document intelligence system.
