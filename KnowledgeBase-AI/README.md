# 📚 KnowledgeBase AI — Advanced RAG & Intelligent Knowledge System

> **A portfolio-quality Python document intelligence system that ingests PDF and DOCX files, performs multi-stage retrieval, evaluates relevance, and produces grounded answers with precise source attribution.**

![Python](https://img.shields.io/badge/Python-3.14+-3776AB?logo=python&logoColor=white)
![Advanced RAG](https://img.shields.io/badge/AI-Advanced%20RAG-7C3AED)
![Tests](https://img.shields.io/badge/Tests-38%20Passed-16A34A)
![Mode](https://img.shields.io/badge/Demo-Offline-F59E0B)
![Status](https://img.shields.io/badge/Portfolio-Ready-16A34A)

---

# 🎯 Overview

KnowledgeBase AI is an **Advanced RAG & Intelligent Knowledge System** built for document-grounded question answering.

Rather than relying on a single retrieval strategy, the system uses a **multi-stage retrieval pipeline** that combines independent semantic and BM25 keyword rankings, fuses them deterministically, reranks broader candidates, evaluates relevance, and abstains when the indexed knowledge base does not contain sufficient evidence.

The project supports:

- 🟢 **Demo mode** — deterministic, local, and offline
- 🤖 **OpenAI mode** — API-backed embeddings and answer generation

---

# 💼 The Business Problem

Organizations accumulate policy manuals, product guides, procedures, and operational documents that are difficult to search efficiently.

A basic document chatbot can retrieve weakly related content, cite irrelevant sources, or attempt to answer questions that the available documents do not support.

A stronger knowledge system should:

- 📄 Work across multiple documents
- 🔎 Combine lexical and semantic retrieval signals
- 🧭 Filter retrieval using document metadata
- 🧠 Rerank broad candidates before answering
- 🛡️ Detect weak evidence and abstain when appropriate
- 📌 Cite only sources that genuinely support the answer
- 💬 Support follow-up questions during a conversation

---

# 🧠 Advanced RAG Retrieval Pipeline

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
Relevance / Confidence Evaluation
      ↓
Grounded Answer OR Abstention
      ↓
Precise Citation Selection
```

This architecture separates **retrieval**, **rank fusion**, **reranking**, **relevance evaluation**, and **citation selection** into explicit stages.

---

# 🚀 Key Capabilities

## 🔍 Hybrid Retrieval

- 🧠 Independent semantic/vector-style retrieval
- 🔤 Genuine BM25 lexical retrieval
- 🔀 Deterministic Reciprocal Rank Fusion (RRF)
- ⚙️ Configurable `RRF_K`

## 🧭 Multi-Stage Ranking

- 📥 Broad candidate retrieval using configurable `CANDIDATE_K`
- 🧠 Independent second-stage local reranking
- 🎯 Final ranking based on query-to-chunk relevance

## 🛡️ Grounding & Abstention

- 📏 Configurable `MINIMUM_RELEVANCE`
- 🚫 Weak-result detection
- 💬 Explicit insufficient-information responses
- 🧾 No unsupported answer when evidence is inadequate

## 🏷️ Metadata-Aware Retrieval

Filtering supports:

- Document ID
- Filename
- File type
- Page number where available

## 📌 Citation Precision

- Only meaningful supporting sources are selected
- Filename preserved
- Chunk ID preserved
- Page information preserved where available
- Unsupported questions return **no irrelevant sources**

## 📚 Knowledge-Base Management

- Add and index documents
- List indexed documents
- Remove documents
- Clear the knowledge base

---

# 🏗️ System Architecture

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
     ┌────┴────┐
     ▼         ▼
Semantic    BM25 Keyword
Retrieval    Retrieval
     └────┬────┘
          ▼
┌───────────────────┐
│ HybridRetriever   │  Fuse rankings with RRF
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Reranker          │  Second-stage relevance ranking
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ RAGPipeline       │  Orchestrate answer generation
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ ResultValidator   │  Validate grounding + citations
└───────────────────┘
```

---

# 📁 Project Structure

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
│   ├── keyword_retriever.py
│   ├── hybrid_retriever.py
│   ├── reranker.py
│   ├── rag_pipeline.py
│   ├── llm_client.py
│   ├── conversation_manager.py
│   ├── knowledge_base.py
│   └── result_validator.py
│
├── tests/
│   ├── test_advanced_retrieval.py
│   └── ...
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# ⚙️ Technology Stack

| Area | Technology |
|---|---|
| 🐍 Language | Python 3.14+ |
| 🛡️ Validation | Pydantic v2 |
| ⚙️ Configuration | python-dotenv |
| 📕 PDF Processing | pypdf |
| 📘 DOCX Processing | python-docx |
| 🧠 Retrieval | Semantic/vector-style retrieval + BM25 |
| 🔀 Rank Fusion | Reciprocal Rank Fusion (RRF) |
| 🧭 Reranking | Deterministic local second-stage reranker |
| 🗄️ Knowledge Storage | JSON-backed local vector store |
| 🤖 Answer Generation | Demo extractive client or OpenAI |
| 🧪 Testing | pytest |

---

# 🛠️ Installation

From the `KnowledgeBase-AI` directory:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

# 🔐 Configuration

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
| `TOP_K` | Number of final retrieved chunks |
| `CANDIDATE_K` | Broad hybrid candidate set before reranking |
| `MINIMUM_RELEVANCE` | Minimum score required for grounding |
| `RRF_K` | RRF rank-smoothing constant |
| `EMBEDDING_DIMENSION` | Local embedding dimension |

> 🔒 Never commit `.env` files or API keys.

---

# ▶️ Run the Application

```powershell
python -m src.main
```

Available modes:

```powershell
# Offline demonstration mode
python -m src.main --mode demo

# Interactive mode
python -m src.main --interactive

# OpenAI-backed interactive mode
python -m src.main --mode openai --interactive
```

The demonstration verifies document indexing, grounded answers, precise sources, unsupported-question abstention, conversation-aware retrieval, document removal, and knowledge-base clearing.

---

# 🧪 Verification

Run the complete automated test suite:

```powershell
pytest
```

## Current Verified Result

```text
38 passed
```

The verified runtime demo also demonstrates:

- ✅ Relevant source precision for supported questions
- ✅ Improved exclusion of irrelevant secondary sources
- ✅ Grounded answers from indexed documents
- ✅ Abstention for unsupported questions
- ✅ `Sources: none` when no source meaningfully supports the answer

---

# 🎯 Skills Demonstrated

`Python` • `Advanced RAG` • `Hybrid Retrieval` • `BM25` • `Reciprocal Rank Fusion` • `Reranking` • `Metadata Filtering` • `Document Intelligence` • `PDF` • `DOCX` • `Embeddings` • `Vector Search` • `OpenAI API` • `Pydantic` • `Testing` • `Error Handling` • `Modular Architecture`

---

# ⚠️ Current Limitations

The project deliberately uses a lightweight local architecture. Current limitations include:

- 🧠 The reranker is deterministic lexical scoring rather than a cross-encoder model
- 🗄️ The JSON-backed store is intended for small local knowledge bases
- 📄 DOCX page-level mapping is limited by document layout extraction
- 💬 Conversation history exists only for the active process session
- 🔐 No multi-user authentication or isolation layer
- 🌐 No dedicated API or web interface in this phase
- 🎯 Relevance scores are deterministic retrieval signals, not calibrated probabilities

---

# 🟢 Project Status

## **Advanced RAG Upgrade Complete · Tested · Runtime Verified · Portfolio Ready**

> **38 automated tests passing with successful end-to-end runtime verification.**

KnowledgeBase AI now represents a genuine **Advanced RAG & Intelligent Knowledge System** with hybrid retrieval, deterministic rank fusion, second-stage reranking, metadata-aware filtering, relevance thresholds, abstention behavior, and precise source attribution.
