from pathlib import Path
import shutil


def organize_file(file_path):
    project_folder = Path(__file__).resolve().parent.parent
    output_folder = project_folder / "output"

    if file_path.suffix.lower() == ".txt":
        destination_folder = output_folder / "text_files"

    elif file_path.suffix.lower() == ".csv":
        destination_folder = output_folder / "csv_files"

    else:
        return False, "No destination folder available"

    destination_folder.mkdir(parents=True, exist_ok=True)

    destination = destination_folder / file_path.name

    shutil.move(str(file_path), str(destination))

    return True, destination