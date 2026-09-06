"""Command-line demo for KnowledgeBase AI."""

from __future__ import annotations

import argparse
from pathlib import Path

from docx import Document

from .chunker import Chunker
from .config import Settings
from .conversation_manager import ConversationManager
from .document_processor import DocumentProcessor
from .document_reader import DocumentReader
from .embeddings import HashingEmbeddingProvider, OpenAIEmbeddingProvider
from .exceptions import KnowledgeBaseError
from .knowledge_base import KnowledgeBase
from .llm_client import DemoLLMClient, OpenAILLMClient
from .logger import get_logger
from .rag_pipeline import RAGPipeline
from .retriever import Retriever
from .vector_store import JsonVectorStore

HANDBOOK_TEXT = """Acme Employee Handbook

Remote work policy: Employees work from the office three days each week and may work remotely on the remaining two days.

Paid time off: Employees receive 20 days of paid time off (PTO) each calendar year. Unused PTO does not carry over.

Expense reports: Submit expense reports within 14 days of the purchase date.
"""

PRODUCT_TEXT = """Nova Widget Product Guide

The Nova Widget is a portable sensor for field technicians.

Battery life: The Nova Widget battery lasts 48 hours on a full charge.

Warranty: The Nova Widget includes a 2-year hardware warranty.

Support: Contact support@novawidget.example for replacement parts.
"""


def _wrap_pdf_lines(text: str, width: int = 86) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = f"{current} {word}"
            if len(trial) <= width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def write_simple_pdf(path: Path, text: str) -> None:
    """Write a small text-only PDF without extra rendering dependencies."""
    commands = ["BT", "/F1 11 Tf", "72 720 Td"]
    for index, line in enumerate(_wrap_pdf_lines(text)):
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        if index:
            commands.append("0 -14 Td")
        commands.append(f"({escaped}) Tj")
    commands.append("ET")
    stream = "\n".join(commands).encode("latin-1", "replace")

    def pdf_object(number: int, body: bytes) -> bytes:
        return f"{number} 0 obj\n".encode("ascii") + body + b"\nendobj\n"

    objects = [
        pdf_object(1, b"<< /Type /Catalog /Pages 2 0 R >>"),
        pdf_object(2, b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>"),
        pdf_object(
            3,
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
            b"/Resources << /Font << /F1 5 0 R >> >> >>",
        ),
        pdf_object(4, f"<< /Length {len(stream)} >>\nstream\n".encode("ascii") + stream + b"\nendstream"),
        pdf_object(5, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"),
    ]
    header = b"%PDF-1.4\n"
    parts = [header]
    offsets = [0]
    position = len(header)
    for item in objects:
        offsets.append(position)
        parts.append(item)
        position += len(item)
    xref = [b"xref\n0 6\n0000000000 65535 f \n"]
    for offset in offsets[1:]:
        xref.append(f"{offset:010d} 00000 n \n".encode("ascii"))
    trailer = f"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{position}\n%%EOF\n".encode("ascii")
    path.write_bytes(b"".join(parts + xref + [trailer]))


def write_sample_docx(path: Path, text: str) -> None:
    document = Document()
    for line in text.splitlines():
        document.add_paragraph(line)
    document.save(path)


def build_system(settings: Settings, persist: bool = True) -> tuple[KnowledgeBase, RAGPipeline]:
    if settings.mode == "openai":
        embeddings: HashingEmbeddingProvider | OpenAIEmbeddingProvider = OpenAIEmbeddingProvider(
            api_key=settings.openai_api_key or "",
            model=settings.openai_embedding_model,
        )
        llm: DemoLLMClient | OpenAILLMClient = OpenAILLMClient(
            api_key=settings.openai_api_key or "",
            model=settings.openai_model,
        )
    else:
        embeddings = HashingEmbeddingProvider(dimension=settings.embedding_dimension)
        llm = DemoLLMClient()

    store_path = settings.vector_store_dir / "index.json" if persist else None
    store = JsonVectorStore(store_path)
    knowledge_base = KnowledgeBase(
        reader=DocumentReader(),
        processor=DocumentProcessor(),
        chunker=Chunker(settings.chunk_size, settings.chunk_overlap),
        embeddings=embeddings,
        store=store,
    )
    pipeline = RAGPipeline(
        retriever=Retriever(embeddings, store),
        llm=llm,
        conversation=ConversationManager(),
        default_top_k=settings.top_k,
    )
    return knowledge_base, pipeline


def _print_response(response) -> None:
    print(f"Q: {response.question}")
    print(f"A: {response.answer}")
    print(f"Grounded: {response.grounded}")
    if not response.sources:
        print("Sources: none")
        return
    print("Sources:")
    for source in response.sources:
        page = f", page {source.page_number}" if source.page_number else ""
        print(
            f"  - {source.document_name} [{source.chunk_id}{page}] score={source.score:.3f}"
        )


def run_demo(settings: Settings) -> int:
    logger = get_logger(settings.log_dir)
    documents_dir = settings.documents_dir
    documents_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = documents_dir / "acme_employee_handbook.pdf"
    docx_path = documents_dir / "nova_widget_product_guide.docx"
    write_simple_pdf(pdf_path, HANDBOOK_TEXT)
    write_sample_docx(docx_path, PRODUCT_TEXT)

    knowledge_base, pipeline = build_system(settings, persist=True)
    knowledge_base.clear()
    print(f"KnowledgeBase AI demo (mode={settings.mode})")
    print("-" * 60)

    ingest = knowledge_base.add_documents([pdf_path, docx_path])
    for item in ingest.succeeded:
        print(f"Indexed: {item.file_name} ({item.chunk_count} chunks, id={item.document_id})")
    for item in ingest.failed:
        print(f"Failed: {item.path} — {item.error}")
        logger.error("Demo ingest failed for %s: %s", item.path, item.error)

    print("\nIndexed documents:")
    for item in knowledge_base.list_documents():
        print(f"  - {item.file_name} [{item.file_type}] chunks={item.chunk_count} id={item.document_id}")

    questions = [
        "How many PTO days do employees receive?",
        "What is the remote work policy?",
        "What is the battery life of the Nova Widget?",
        "What is the company's current stock price?",
    ]
    print("\nQuestion answering:")
    for question in questions:
        print()
        response = pipeline.ask(question)
        _print_response(response)

    print("\nFollow-up uses conversation history for retrieval.")
    print("\nRetrieved context for the PTO question:")
    print(pipeline.describe_context("How many PTO days do employees receive?"))

    documents = knowledge_base.list_documents()
    if documents:
        removed = knowledge_base.remove_document(documents[0].document_id)
        print(f"\nRemoved {documents[0].file_name}: {removed}")
        print("Remaining documents:", [item.file_name for item in knowledge_base.list_documents()])

    knowledge_base.clear()
    print("Knowledge base cleared.")
    logger.info("Demo completed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="KnowledgeBase AI — Multi-Document RAG Assistant")
    parser.add_argument("--interactive", action="store_true", help="ask questions until 'quit'")
    parser.add_argument("--mode", choices=["demo", "openai"], help="override KNOWLEDGEBASE_MODE")
    args = parser.parse_args()
    try:
        settings = Settings.from_env()
        if args.mode:
            settings = Settings(
                mode=args.mode,
                openai_api_key=settings.openai_api_key,
                openai_model=settings.openai_model,
                openai_embedding_model=settings.openai_embedding_model,
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
                top_k=settings.top_k,
                embedding_dimension=settings.embedding_dimension,
                documents_dir=settings.documents_dir,
                vector_store_dir=settings.vector_store_dir,
                log_dir=settings.log_dir,
            )
        if not args.interactive:
            return run_demo(settings)

        knowledge_base, pipeline = build_system(settings, persist=True)
        print("KnowledgeBase AI interactive mode. Commands: add <path>, list, remove <id>, clear, quit")
        while True:
            request = input("> ").strip()
            if request.lower() in {"quit", "exit"}:
                return 0
            if request.lower() == "list":
                for item in knowledge_base.list_documents():
                    print(f"{item.document_id}  {item.file_name}  chunks={item.chunk_count}")
                continue
            if request.lower() == "clear":
                knowledge_base.clear()
                pipeline.conversation.clear()
                print("Knowledge base cleared.")
                continue
            if request.lower().startswith("add "):
                result = knowledge_base.add_documents([request[4:].strip()])
                if result.succeeded:
                    print("Indexed:", [item.file_name for item in result.succeeded])
                if result.failed:
                    print("Failed:", result.failed)
                continue
            if request.lower().startswith("remove "):
                document_id = request.split(None, 1)[1]
                print("Removed:" if knowledge_base.remove_document(document_id) else "Not found:", document_id)
                continue
            _print_response(pipeline.ask(request))
    except KnowledgeBaseError as exc:
        print(f"KnowledgeBase AI failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
