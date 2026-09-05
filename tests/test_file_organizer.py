import file_organizer
from file_organizer import organize_file


def test_organize_csv_file(tmp_path, monkeypatch):
    fake_src_folder = tmp_path / "src"
    fake_src_folder.mkdir()

    fake_file = fake_src_folder / "file_organizer.py"
    fake_file.touch()

    monkeypatch.setattr(
        file_organizer,
        "__file__",
        str(fake_file)
    )

    input_folder = tmp_path / "input"
    input_folder.mkdir()

    file_path = input_folder / "sample.csv"
    file_path.write_text(
        "name,email\nJohn,john@example.com"
    )

    organized, destination = organize_file(file_path)

    assert organized is True
    assert destination.exists()
    assert destination.name == "sample.csv"
    assert destination.parent.name == "csv_files"


def test_organize_text_file(tmp_path, monkeypatch):
    fake_src_folder = tmp_path / "src"
    fake_src_folder.mkdir()

    fake_file = fake_src_folder / "file_organizer.py"
    fake_file.touch()

    monkeypatch.setattr(
        file_organizer,
        "__file__",
        str(fake_file)
    )

    input_folder = tmp_path / "input"
    input_folder.mkdir()

    file_path = input_folder / "sample.txt"
    file_path.write_text("Hello world")

    organized, destination = organize_file(file_path)

    assert organized is True
    assert destination.exists()
    assert destination.name == "sample.txt"
    assert destination.parent.name == "text_files"