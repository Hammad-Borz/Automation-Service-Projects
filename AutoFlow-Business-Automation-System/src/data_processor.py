import csv


def process_text_file(file_path):
    content = file_path.read_text(encoding="utf-8")

    lines = content.splitlines()
    words = content.split()

    return {
        "file_name": file_path.name,
        "file_type": "Text",
        "line_count": len(lines),
        "word_count": len(words),
    }


def process_csv_file(file_path):
    with file_path.open(encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    headers = rows[0] if rows else []
    data_rows = rows[1:] if len(rows) > 1 else []

    return {
        "file_name": file_path.name,
        "file_type": "CSV",
        "columns": headers,
        "row_count": len(data_rows),
    }