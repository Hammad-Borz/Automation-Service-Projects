import report_generator
from report_generator import generate_report


def test_generate_report(tmp_path, monkeypatch):
    fake_src_folder = tmp_path / "src"
    fake_src_folder.mkdir()

    fake_file = fake_src_folder / "report_generator.py"
    fake_file.touch()

    monkeypatch.setattr(
        report_generator,
        "__file__",
        str(fake_file)
    )

    processed_files = [
        {
            "file_name": "sample.txt",
            "file_type": "Text",
            "line_count": 2,
            "word_count": 5,
        },
        {
            "file_name": "sample.csv",
            "file_type": "CSV",
            "columns": ["name", "email"],
            "row_count": 2,
        },
    ]

    report_path = generate_report(processed_files)

    assert report_path.exists()

    content = report_path.read_text(encoding="utf-8")

    assert "AUTO FLOW BUSINESS AUTOMATION REPORT" in content
    assert "Total files processed: 2" in content

    assert "File: sample.txt" in content
    assert "Type: Text" in content
    assert "Lines: 2" in content
    assert "Words: 5" in content

    assert "File: sample.csv" in content
    assert "Type: CSV" in content
    assert "Columns: name, email" in content
    assert "Rows: 2" in content