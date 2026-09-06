from src.chunker import Chunker
from src.models import DocumentMetadata, ExtractedDocument, PageText


def test_chunk_creation_and_overlap() -> None:
    text = " ".join(f"word{i:02d}" for i in range(80))
    document = ExtractedDocument(
        metadata=DocumentMetadata(
            document_id="doc_1",
            file_name="policy.pdf",
            file_type="pdf",
            source_path="policy.pdf",
        ),
        text=text,
        pages=[PageText(page_number=2, text=text)],
    )
    chunks = Chunker(chunk_size=80, chunk_overlap=20).chunk(document)
    assert len(chunks) > 1
    assert all(chunk.document_id == "doc_1" for chunk in chunks)
    assert all(chunk.document_name == "policy.pdf" for chunk in chunks)
    assert all(chunk.page_number == 2 for chunk in chunks)
    assert [chunk.chunk_index for chunk in chunks] == list(range(len(chunks)))
    assert chunks[0].text[:20] in text


def test_short_document_stays_single_chunk() -> None:
    document = ExtractedDocument(
        metadata=DocumentMetadata(
            document_id="doc_2",
            file_name="short.docx",
            file_type="docx",
            source_path="short.docx",
        ),
        text="Short policy statement.",
    )
    chunks = Chunker(chunk_size=400, chunk_overlap=80).chunk(document)
    assert len(chunks) == 1
    assert chunks[0].text == "Short policy statement."
    assert chunks[0].file_type == "docx"


def test_invalid_chunker_settings() -> None:
    try:
        Chunker(chunk_size=10, chunk_overlap=2)
        raised = False
    except ValueError:
        raised = True
    assert raised
