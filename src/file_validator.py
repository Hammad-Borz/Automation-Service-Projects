from pathlib import Path


SUPPORTED_EXTENSIONS = {".txt", ".csv"}


def validate_file(file_path):
    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return False, "Unsupported file type"

    if file_path.stat().st_size == 0:
        return False, "File is empty"

    return True, "File is valid"