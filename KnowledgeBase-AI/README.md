# KnowledgeBase AI — Multi-Document RAG Assistant

> **A production-style Python application that ingests PDF and DOCX files into a local knowledge base and answers questions with a grounded Retrieval-Augmented Generation (RAG) pipeline, source citations, and session conversation history.**

---

## The Business Problem

Teams accumulate policy manuals, product guides, and operational documents that are hard to search. Staff ask the same questions repeatedly, and generic chat tools invent answers that are not present in the source files.

A useful assistant must:

- ingest more than one document
- retrieve the passages that actually support an answer
- refuse to fabricate facts when the files are silent
- show which document (and chunk) the answer came from

---

## The Solution

KnowledgeBase AI turns supported documents into chunked, embedded records in a local vector store. User questions are embedded, matched against those chunks, and passed to an answer generator that is instructed to stay inside the retrieved context.

```text
User Question
      ↓
Query Processing (+ conversation history)
      ↓
Retrieve Relevant Chunks
      ↓
Build Context
      ↓
AI Model (demo extractive or OpenAI)
      ↓
Grounded Answer + Source Citations
```

The default **demo** mode runs entirely offline with deterministic local embeddings and an extractive answerer. Switching to **openai** mode uses an API key from `.env` for embeddings and chat generation.

---

## Key Features

- Multi-document ingestion for **PDF** and **DOCX**
- Safe extraction with clear errors for missing, empty, unsupported, or unreadable files
- Configurable, testable chunking that preserves document identity and optional page numbers
- Replaceable embedding and vector-store layers
- RAG answers that stay inside retrieved context
- Source citations (document name, chunk id, optional page number, similarity score)
- Session conversation history for follow-up questions
- Document management: add, list, remove, and clear
- Centralized file logging without recording API keys
- pytest suite that does not require a live AI provider

---

## RAG Architecture

```text
PDF / DOCX files
        ↓
DocumentReader → extract text + metadata
        ↓
DocumentProcessor → normalize text
        ↓
Chunker → overlapping chunks with source metadata
        ↓
EmbeddingProvider → chunk vectors
        ↓
VectorStore → local JSON knowledge base
        ↓
Retriever → top-k chunks for a question
        ↓
LLMClient → grounded answer
        ↓
ResultValidator → RAGResponse + SourceCitation
```

| Component | Responsibility |
|---|---|
| `document_reader` | Extract text from PDF/DOCX and capture metadata. |
| `document_processor` | Clean extracted text before indexing. |
| `chunker` | Split text into overlapping chunks with source identifiers. |
| `embeddings` | Hashing embeddings (demo) or OpenAI embeddings. |
| `vector_store` | Persist documents, chunks, and vectors locally. |
| `retriever` | Embed the query and return ranked chunks. |
| `rag_pipeline` | Orchestrate retrieval, generation, citations, and history. |
| `llm_client` | Isolated LLM adapter with a demo implementation. |
| `conversation_manager` | Session turns and follow-up query expansion. |
| `knowledge_base` | Add / list / remove / clear indexed documents. |
| `result_validator` | Enforce the RAG response contract. |

---

## Project Structure

```text
KnowledgeBase-AI/
│
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
├── requirements.txt
│
├── data/
│   ├── documents/
│   │   └── .gitkeep
│   └── vector_store/
│       └── .gitkeep
│
├── logs/
│   └── .gitkeep
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── config.py
│   ├── logger.py
│   ├── exceptions.py
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
└── tests/
    ├── conftest.py
    ├── test_document_reader.py
    ├── test_document_processor.py
    ├── test_chunker.py
    ├── test_retriever.py
    ├── test_conversation_manager.py
    ├── test_knowledge_base.py
    ├── test_rag_pipeline.py
    └── test_result_validator.py
```

---

## Technologies Used

| Area | Choice |
|---|---|
| Language | Python 3.11+ |
| Validation | Pydantic v2 |
| Configuration | python-dotenv |
| PDF extraction | pypdf |
| DOCX extraction | python-docx |
| Embeddings | Local hashing vectors (demo) or OpenAI embeddings |
| Vector store | JSON-backed cosine search (replaceable) |
| LLM | Demo extractive client or OpenAI Chat Completions |
| Tests | pytest |

---

## Installation

```bash
cd KnowledgeBase-AI
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux, activate with `source .venv/bin/activate`.

---

## Environment Configuration

Copy the example file and add secrets locally. Never commit `.env`.

```bash
copy .env.example .env
```

| Variable | Purpose |
|---|---|
| `KNOWLEDGEBASE_MODE` | `demo` (default, offline) or `openai` |
| `OPENAI_API_KEY` | Required only for `openai` mode |
| `OPENAI_MODEL` | Chat model, default `gpt-4o-mini` |
| `OPENAI_EMBEDDING_MODEL` | Embedding model, default `text-embedding-3-small` |
| `CHUNK_SIZE` | Target chunk size in characters |
| `CHUNK_OVERLAP` | Overlap between adjacent chunks |
| `TOP_K` | Number of chunks retrieved per question |
| `EMBEDDING_DIMENSION` | Dimension used by the local hashing embedder |

---

## How to Run the Application

From the `KnowledgeBase-AI` directory:

```bash
python -m src.main
```

Optional flags:

```bash
python -m src.main --mode demo
python -m src.main --interactive
python -m src.main --mode openai --interactive
```

The non-interactive command writes two sample documents, indexes them, answers questions (including an unanswerable one), shows citations, removes a document, and clears the knowledge base.

---

## How to Run Tests

```bash
pytest
```

The suite uses local hashing embeddings and scripted LLM doubles. It does **not** call OpenAI.

---

## Example Workflow

1. Add PDF and DOCX files to the knowledge base.
2. Clean, chunk, embed, and store them.
3. List indexed documents and chunk counts.
4. Ask a question about employee PTO.
5. Inspect retrieved context and citations.
6. Ask a follow-up about remote work.
7. Ask a question the files cannot answer.
8. Remove a document or clear the store.

---

## Example Question-and-Answer Interaction

```text
Q: How many PTO days do employees receive?
A: Employees receive 20 days of paid time off (PTO) each calendar year.
Grounded: True
Sources:
  - acme_employee_handbook.pdf [chunk_a1b2c3d4e5f6, page 1] score=0.742

Q: What is the company's current stock price?
A: The indexed documents do not contain enough information to answer this question.
Grounded: False
Sources:
  - acme_employee_handbook.pdf [chunk_a1b2c3d4e5f6, page 1] score=0.211
```

Demo-mode wording is extractive. OpenAI mode produces fluent answers from the same retrieved context.

---

## Architecture Overview

```text
                    ┌─────────────────────┐
                    │   ConversationManager│
                    └──────────┬──────────┘
                               │
User ──► RAGPipeline ──► Retriever ──► EmbeddingProvider
               │              │
               │              ▼
               │         VectorStore ◄── KnowledgeBase
               │              ▲              │
               ▼              │              ▼
           LLMClient     chunk vectors   Reader/Processor/Chunker
               │
               ▼
        ResultValidator ──► RAGResponse + SourceCitation
```

The vector store, embedding provider, and LLM client are injected behind small protocols so a later Chroma, FAISS, or other provider swap does not rewrite the pipeline.

---

## Limitations and Possible Future Improvements

- Demo embeddings are lexical hashed n-grams, not large-model semantic vectors.
- The JSON vector store is intended for small local knowledge bases, not multi-GB corpora.
- Page numbers are captured for PDFs; DOCX page mapping is left for a future layout-aware reader.
- Conversation history is in-memory for the process lifetime.
- OpenAI mode requires network access and a valid API key.
- No web UI, authentication, or multi-user isolation yet.

Useful next steps: persistent chat sessions, page-accurate PDF citations in the answer text, hybrid keyword + vector search, and a thin API layer over `KnowledgeBase` and `RAGPipeline`.

---

## License

This project is provided as a portfolio and freelance demonstration of a practical RAG workflow.
