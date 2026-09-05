"""Organize supported input files into type-specific folders."""

from pathlib import Path
import shutil


def organize_file(file_path: Path) -> tuple[bool, Path | str]:
    """Move a supported file into its destination folder."""
    project_folder = Path(__file__).resolve().parent.parent
    output_folder = project_folder / "output"

    extension = file_path.suffix.lower()

    if extension == ".txt":
        destination_folder = output_folder / "text_files"
    elif extension == ".csv":
        destination_folder = output_folder / "csv_files"
    else:
        return False, "No destination folder available"

    destination_folder.mkdir(parents=True, exist_ok=True)
    destination = destination_folder / file_path.name

    if destination.exists():
        return False, f"Destination already exists: {destination.name}"

    try:
        shutil.move(str(file_path), str(destination))
    except OSError as exc:
        return False, f"Failed to move file: {exc}"

    return True, destination
