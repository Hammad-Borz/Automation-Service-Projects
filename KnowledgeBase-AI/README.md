# 📚 KnowledgeBase AI — Advanced RAG & Intelligent Knowledge System

> **A multi-document Python RAG system that indexes PDF/DOCX files, combines semantic and BM25 retrieval, fuses rankings with RRF, reranks candidates, validates relevance, and returns grounded answers with precise source attribution or abstains when evidence is insufficient.**

![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?logo=python&logoColor=white)
![Advanced RAG](https://img.shields.io/badge/AI-Advanced%20RAG-7C3AED)
![Tests](https://img.shields.io/badge/Tests-38%20Passed-16A34A)
![Mode](https://img.shields.io/badge/Demo-Offline-F59E0B)
![Status](https://img.shields.io/badge/Portfolio-Ready-16A34A)

---

## 1. 🎯 Project Title

**KnowledgeBase AI — Advanced RAG & Intelligent Knowledge System**

KnowledgeBase AI is a service-specific document intelligence project for grounded question answering across indexed PDF and DOCX knowledge bases.

---

## 2. 📝 One-Line Description

> **PDF/DOCX → extract → process → chunk → embed → hybrid retrieve → RRF → rerank → evaluate relevance → answer with citations or abstain.**

---

## 3. 🔴 Problem

Organizations accumulate policies, product guides, procedures, and operational documents that become difficult to search efficiently.

A basic document chatbot can retrieve weakly related content, cite irrelevant sources, or attempt to answer questions that the indexed documents do not support.

A stronger knowledge system needs to:

- 📄 Work across multiple documents
- 🔎 Combine lexical and semantic retrieval signals
- 🧭 Filter retrieval using document metadata
- 🧠 Rerank broad candidate sets
- 🛡️ Detect insufficient evidence
- 🚫 Abstain instead of producing unsupported answers
- 📌 Select only meaningful supporting citations
- 💬 Use conversation context for follow-up questions

---

## 4. 🟢 Solution

KnowledgeBase AI implements a multi-stage, deterministic retrieval pipeline with two runtime modes:

- 🟢 **Demo mode** — local, deterministic, and offline
- 🤖 **OpenAI mode** — API-backed embeddings and answer generation

```text
User Question
      ↓
Optional Conversation Context
      ↓
Metadata Filtering
      ↓
┌─────────────────────────────┐
│ Semantic Retrieval          │
└──────────────┬──────────────┘
               │
               ├── Reciprocal Rank Fusion (RRF)
               │
┌──────────────┴──────────────┐
│ BM25 Keyword Retrieval      │
└──────────────┬──────────────┘
               ↓
Broader Candidate Set
      ↓
Second-Stage Reranking
      ↓
Relevance Threshold
      ↓
Grounded Answer OR Abstention
      ↓
Supporting-Chunk Selection
      ↓
Precise Citations
```

---

## 5. ⚙️ Key Features

- 📄 PDF and DOCX document ingestion
- 🧩 Source-aware document chunking
- 🧠 Semantic/vector-style retrieval
- 🔤 Genuine BM25 lexical retrieval
- 🔀 Deterministic Reciprocal Rank Fusion
- ⚙️ Configurable `RRF_K`
- 📥 Configurable broad candidate set with `CANDIDATE_K`
- 🧭 Metadata filtering by document ID, filename, file type, and page number where available
- 🎯 Deterministic second-stage lexical reranking
- 📏 Configurable `MINIMUM_RELEVANCE` threshold
- 🚫 Abstention when retrieved evidence is insufficient
- 📌 Precise source citations with filename, chunk ID, page, and score
- 💬 Conversation-aware query expansion
- 📚 Add, list, remove, and clear indexed documents
- 🗄️ JSON-backed local vector store
- 🤖 Demo extractive client or OpenAI answer generation
- 🧪 **38 automated tests**

---

## 6. 🔄 How It Works

### Ingestion

1. **Read** — Load PDF or DOCX content and document metadata.
2. **Process** — Normalize the extracted document representation.
3. **Chunk** — Create source-aware chunks with document/page metadata.
4. **Embed** — Generate local hashing embeddings in demo mode or OpenAI embeddings in OpenAI mode.
5. **Store** — Persist document metadata, chunks, and embeddings in the local JSON vector store.

### Question Answering

1. **Receive question** — Validate the query.
2. **Expand context** — Include relevant active conversation history.
3. **Filter** — Apply optional document metadata filters.
4. **Semantic retrieval** — Search the local vector store.
5. **BM25 retrieval** — Independently search lexical matches.
6. **Fuse** — Combine the independent rankings with Reciprocal Rank Fusion.
7. **Rerank** — Apply deterministic second-stage lexical relevance scoring.
8. **Threshold** — Remove results below `MINIMUM_RELEVANCE`.
9. **Generate** — Produce a grounded answer using the selected context.
10. **Validate citations** — Select chunks containing meaningful lexical evidence from the final answer.
11. **Return** — Provide the answer, grounding state, retrieved chunk IDs, and precise citations.

---

## 7. 🏗️ Architecture / Workflow

```text
                 DOCUMENT INGESTION

PDF / DOCX
    ↓
DocumentReader
    ↓
DocumentProcessor
    ↓
Chunker
    ↓
EmbeddingProvider
    ↓
JsonVectorStore
    │
    ├──────────────────────────────┐
    │                              │
    ↓                              ↓
Semantic Retrieval           BM25 Retrieval
    │                              │
    └──────────────┬───────────────┘
                   ↓
          Reciprocal Rank Fusion
                   ↓
          Lexical Second-Stage
              Reranking
                   ↓
             RAGPipeline
                   ↓
        Grounded Answer / Abstain
                   ↓
          Result Validation
                   ↓
            Source Citations
```

### Component Responsibilities

| Component | Responsibility |
|---|---|
| `document_reader.py` | Extract PDF/DOCX text and document metadata |
| `document_processor.py` | Normalize extracted content |
| `chunker.py` | Create source-aware document chunks |
| `embeddings.py` | Provide demo hashing or OpenAI embeddings |
| `vector_store.py` | Persist metadata, chunks, embeddings, and perform semantic search |
| `keyword_retriever.py` | Independent BM25 retrieval |
| `hybrid_retriever.py` | Deterministic Reciprocal Rank Fusion |
| `reranker.py` | Local second-stage lexical relevance scoring |
| `rag_pipeline.py` | Orchestrate retrieval, answer generation, and response validation |
| `result_validator.py` | Validate grounding and select supporting citations |
| `knowledge_base.py` | Add, list, remove, and clear indexed documents |
| `conversation_manager.py` | Maintain active-session conversation context |

---

## 8. 🔎 Retrieval & Grounding Logic

### Hybrid Retrieval

Semantic and BM25 retrieval are executed independently:

```text
Semantic Ranking ──┐
                   ├── RRF ──→ Candidate Ranking
BM25 Ranking ──────┘
```

RRF uses the configurable `RRF_K` smoothing constant and normalizes the fused score.

### Second-Stage Reranking

The local reranker evaluates query-token coverage and lexical density against each fused candidate. It is intentionally deterministic and separate from both semantic similarity and BM25 candidate generation.

### Relevance Threshold

Candidates are returned only when their final score meets `MINIMUM_RELEVANCE`.

### Abstention

If no retrieved evidence passes the relevance boundary, the system can return an insufficient-information response rather than forcing an unsupported answer.

### Citation Selection

Supporting chunks are selected from meaningful lexical overlap between the final answer and retrieved content. A grounded response must contain at least one source citation.

---

## 9. 🛡️ Grounding & Citation Contract

A valid RAG response contains:

```json
{
  "question": "...",
  "answer": "...",
  "grounded": true,
  "sources": [
    {
      "document_id": "doc_...",
      "document_name": "example.pdf",
      "chunk_id": "chunk_...",
      "page_number": 1,
      "score": 0.82
    }
  ],
  "retrieved_chunk_ids": ["chunk_..."]
}
```

The validation model enforces that grounded responses include citations and retrieved chunk references.

Unsupported questions can return:

```text
Grounded: false
Sources: none
```

---

## 10. 📚 Knowledge-Base Management

KnowledgeBase provides operations to:

- ➕ Add and index documents
- 📋 List indexed documents
- 🗑️ Remove a document by ID
- 🧹 Clear the complete knowledge base
- 🔎 Check whether the knowledge base is empty

Supported document types in the current reader are:

- 📕 PDF
- 📘 DOCX

---

## 11. 🛠️ Technology Stack

| Area | Technology |
|---|---|
| 🐍 Language | Python 3.14+ |
| 🛡️ Validation | Pydantic v2 |
| ⚙️ Configuration | python-dotenv |
| 📕 PDF Processing | pypdf |
| 📘 DOCX Processing | python-docx |
| 🧠 Retrieval | Semantic/vector-style retrieval + BM25 |
| 🔀 Rank Fusion | Reciprocal Rank Fusion |
| 🧭 Reranking | Deterministic local lexical reranker |
| 🗄️ Knowledge Storage | JSON-backed local vector store |
| 🤖 Answer Generation | Demo client or OpenAI |
| 🧪 Testing | pytest |

---

## 12. 📁 Project Structure

```text
KnowledgeBase-AI/
├── data/
│   ├── documents/
│   └── vector_store/
├── logs/
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
│   ├── keyword_retriever.py
│   ├── hybrid_retriever.py
│   ├── reranker.py
│   ├── rag_pipeline.py
│   ├── llm_client.py
│   ├── conversation_manager.py
│   ├── knowledge_base.py
│   └── result_validator.py
├── tests/
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

Runtime storage is organized under `data/`, while logs are written under `logs/`.

---

## 13. 🚀 Installation & Quick Start

From the `KnowledgeBase-AI` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Configure

```powershell
copy .env.example .env
```

### Offline Demo

```powershell
python -m src.main --mode demo
```

The demo creates local sample PDF/DOCX documents, indexes them, asks supported and unsupported questions, demonstrates conversation-aware retrieval, removes a document, and clears the knowledge base.

### Interactive Demo Mode

```powershell
python -m src.main --interactive
```

### OpenAI-Backed Mode

```powershell
python -m src.main --mode openai --interactive
```

OpenAI mode requires `OPENAI_API_KEY`.

---

## 14. 🔧 Configuration

| Variable | Default / Requirement | Purpose |
|---|---|---|
| `KNOWLEDGEBASE_MODE` | `demo` | Runtime mode: `demo` or `openai` |
| `OPENAI_API_KEY` | Required for OpenAI mode | OpenAI authentication |
| `OPENAI_MODEL` | `gpt-4o-mini` | Answer-generation model |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model |
| `CHUNK_SIZE` | `400` | Target chunk size |
| `CHUNK_OVERLAP` | `80` | Chunk overlap |
| `TOP_K` | `4` | Final retrieved chunk count |
| `CANDIDATE_K` | `12` | Broad hybrid candidate count |
| `MINIMUM_RELEVANCE` | `0.35` | Minimum final retrieval score |
| `RRF_K` | `60` | RRF rank-smoothing constant |
| `EMBEDDING_DIMENSION` | `256` | Demo embedding dimension |

Configuration validation also enforces relationships such as `CANDIDATE_K >= TOP_K`, a valid relevance range, and `CHUNK_OVERLAP < CHUNK_SIZE`.

### 🔒 Security

- Never commit `.env` files.
- Never commit API keys.
- Keep OpenAI credentials outside source code.
- Use `.env.example` as the safe configuration template.

---

## 15. ▶️ Usage

### Application Commands

```powershell
python -m src.main
python -m src.main --mode demo
python -m src.main --interactive
python -m src.main --mode openai --interactive
```

### Interactive Commands

```text
add <path>     → index a document
list           → list indexed documents
remove <id>    → remove a document
clear          → clear the knowledge base
quit           → exit
```

### Typical Question Flow

```text
Question
  ↓
Conversation context
  ↓
Metadata filters (when supplied)
  ↓
Hybrid retrieval
  ↓
RRF
  ↓
Reranking
  ↓
Relevance threshold
  ↓
Answer + citations OR abstention
```

---

## 16. 🧪 Example

### Demo Knowledge

The built-in demo creates:

- `acme_employee_handbook.pdf`
- `nova_widget_product_guide.docx`

### Supported Question

```text
Q: How many PTO days do employees receive?
A: Employees receive 20 days of paid time off (PTO) each calendar year.
Grounded: True
Sources:
  - acme_employee_handbook.pdf
```

### Another Supported Question

```text
Q: What is the battery life of the Nova Widget?
A: The Nova Widget battery lasts 48 hours on a full charge.
Grounded: True
Sources:
  - nova_widget_product_guide.docx
```

### Unsupported Question

```text
Q: What is the company's current stock price?
Grounded: False
Sources: none
```

This demonstrates the intended abstention behavior when the indexed documents do not provide sufficient evidence.

---

## 17. 📸 Screenshots

> **Reserved area — screenshots will be added later.**

Planned portfolio evidence:

- 📚 Indexed document list
- 🔎 Retrieval results
- 🧠 Grounded answer
- 📌 Source citations
- 🚫 Unsupported-question abstention
- 💬 Conversation follow-up
- 🗑️ Document removal
- 🧹 Knowledge-base clearing
- 🧪 Test results

---

## 18. 🎥 Demo Video / GIF

> **Reserved area — demo video/GIF will be added later.**

Planned demonstration:

```text
Launch KnowledgeBase AI
        ↓
Index PDF + DOCX
        ↓
Show knowledge-base documents
        ↓
Ask grounded question
        ↓
Show hybrid retrieval
        ↓
Show citation
        ↓
Ask unsupported question
        ↓
Show abstention + Sources: none
        ↓
Ask follow-up question
        ↓
Remove document
        ↓
Clear knowledge base
```

The demonstration will clearly distinguish offline demo behavior from OpenAI-backed runtime behavior.

---

## 19. 📊 Results, Benefits & Verification

### Verified Project Results

- 🧪 **38 automated tests passing**
- 🟢 Offline demo mode available
- 🤖 OpenAI mode available
- 🔎 Hybrid semantic + BM25 retrieval
- 🔀 Deterministic RRF
- 🧭 Second-stage reranking
- 📏 Relevance thresholding
- 🚫 Unsupported-question abstention
- 📌 Precise source attribution
- 💬 Conversation-aware retrieval
- 📚 Knowledge-base lifecycle management

### Portfolio Value

KnowledgeBase AI demonstrates advanced document intelligence rather than a basic single-retriever chatbot:

- Hybrid information retrieval
- Ranking fusion
- Second-stage reranking
- Grounding controls
- Citation validation
- Metadata-aware retrieval
- Configurable retrieval thresholds
- Local persistence
- Replaceable embedding/LLM providers
- Automated verification

---

## 20. ⚠️ Limitations, Future Improvements & Contact

### Current Limitations

- 🧠 The reranker is deterministic lexical scoring rather than a cross-encoder.
- 🗄️ The JSON-backed store is intended for small local knowledge bases.
- 📄 DOCX page-level mapping is limited by document layout extraction.
- 💬 Conversation history exists only for the active process session.
- 🔐 There is no multi-user authentication or isolation layer.
- 🌐 There is no dedicated API or web interface in this phase.
- 🎯 Relevance scores are deterministic retrieval signals, not calibrated probabilities.

### Future Improvements

- 🧠 Cross-encoder or learned reranking
- 🗄️ Production vector database
- 🔐 Multi-user authentication and isolation
- 🌐 Dedicated API/web interface
- 💬 Persistent conversation history
- 📊 Retrieval evaluation and observability dashboards
- 📌 Stronger citation/evidence evaluation
- 📦 Larger-scale indexing and retrieval infrastructure

### License

No dedicated `LICENSE` file is currently documented for this project.

### Author / Contact

**Hammad Borz**

- GitHub: [@Hammad-Borz](https://github.com/Hammad-Borz)
- Repository: [Automation-Service-Projects](https://github.com/Hammad-Borz/Automation-Service-Projects)

---

## 💼 Portfolio Positioning

**KnowledgeBase AI** is a service-specific **Advanced RAG & Intelligent Knowledge Systems** project demonstrating:

- Python
- Advanced RAG
- Hybrid Retrieval
- BM25
- Reciprocal Rank Fusion
- Deterministic Reranking
- Metadata Filtering
- Document Intelligence
- PDF/DOCX Processing
- Embeddings
- Vector Search
- OpenAI integration
- Pydantic
- Testing
- Error Handling
- Modular Architecture

> **Portfolio note:** The visual evidence sections are intentionally reserved for the later Visual Presentation and Demo Video phases.