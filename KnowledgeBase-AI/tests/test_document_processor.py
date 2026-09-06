from src.document_processor import DocumentProcessor, clean_text
from tests.conftest import sample_extracted


def test_clean_text_collapses_whitespace() -> None:
    raw = "Hello,\t\tworld.\r\n\r\n\r\nNext\x00 paragraph."
    assert clean_text(raw) == "Hello, world.\n\nNext paragraph."


def test_processor_updates_document_and_pages() -> None:
    document = sample_extracted("Policy\t\talerts.\n\n\nSecond   line.")
    processed = DocumentProcessor().process(document)
    assert "\t" not in processed.text
    assert processed.metadata.document_id == "doc_test"
    assert processed.text.startswith("Policy")
