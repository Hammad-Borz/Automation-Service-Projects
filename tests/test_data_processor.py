from data_processor import process_text_file, process_csv_file


def test_process_text_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello world\nThis is a test file.")

    result = process_text_file(file_path)

    assert result["file_name"] == "sample.txt"
    assert result["file_type"] == "Text"
    assert result["line_count"] == 2
    assert result["word_count"] == 7


def test_process_csv_file(tmp_path):
    file_path = tmp_path / "sample.csv"
    file_path.write_text(
        "name,email\n"
        "John,john@example.com\n"
        "Sara,sara@example.com\n"
    )

    result = process_csv_file(file_path)

    assert result["file_name"] == "sample.csv"
    assert result["file_type"] == "CSV"
    assert result["columns"] == ["name", "email"]
    assert result["row_count"] == 2