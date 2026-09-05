"""Validate files before they enter the AutoFlow pipeline."""

from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".csv"}


def validate_file(file_path: Path) -> tuple[bool, str]:
    """Validate that a file is supported and contains data."""
    if not file_path.is_file():
        return False, "Path is not a file"

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return False, "Unsupported file type"

    if file_path.stat().st_size == 0:
        return False, "File is empty"

    return True, "File is valid"
