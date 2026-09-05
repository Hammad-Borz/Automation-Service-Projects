from pathlib import Path

from file_validator import validate_file


def test_valid_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello, this is a test file.", encoding="utf-8")

    is_valid, message = validate_file(file_path)

    assert is_valid is True
    assert message == "File is valid"


def test_empty_file(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.touch()

    is_valid, message = validate_file(file_path)

    assert is_valid is False
    assert message == "File is empty"


def test_unsupported_file(tmp_path):
    file_path = tmp_path / "document.pdf"
    file_path.write_text("Test content", encoding="utf-8")

    is_valid, message = validate_file(file_path)

    assert is_valid is False
    assert message == "Unsupported file type"


def test_missing_path(tmp_path):
    file_path = tmp_path / "missing.txt"

    is_valid, message = validate_file(file_path)

    assert is_valid is False
    assert message == "Path is not a file"
