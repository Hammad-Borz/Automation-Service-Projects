"""Discover and process incoming files through the AutoFlow pipeline."""

from pathlib import Path

from data_processor import process_csv_file, process_text_file
from file_organizer import organize_file
from file_validator import validate_file
from logger import setup_logger
from report_generator import generate_report


def discover_files() -> None:
    """Run the end-to-end AutoFlow workflow for files in the input directory."""
    logger = setup_logger()

    project_folder = Path(__file__).resolve().parent.parent
    input_folder = project_folder / "input"
    input_folder.mkdir(parents=True, exist_ok=True)

    files = sorted(file for file in input_folder.iterdir() if file.is_file())
    processed_files = []

    print(f"\nFiles found: {len(files)}\n")
    logger.info("Automation started")
    logger.info("Files found: %s", len(files))

    for file in files:
        is_valid, message = validate_file(file)

        if not is_valid:
            print(f"❌ {file.name} → {message}")
            logger.warning("%s → %s", file.name, message)
            continue

        print(f"✅ {file.name} → {message}")
        logger.info("%s → %s", file.name, message)

        organized, destination = organize_file(file)

        if not organized:
            print(f"❌ {file.name} → {destination}")
            logger.error("%s → %s", file.name, destination)
            continue

        print(f"📂 {file.name} → Moved to {destination.parent.name}")
        logger.info(
            "%s moved to %s", file.name, destination.parent.name
        )

        if destination.suffix.lower() == ".txt":
            processed_data = process_text_file(destination)
        elif destination.suffix.lower() == ".csv":
            processed_data = process_csv_file(destination)
        else:
            logger.warning("No processor available for %s", destination.name)
            continue

        processed_files.append(processed_data)
        print(f"📊 Processed data: {processed_data}")
        logger.info("%s processed successfully", file.name)

    if processed_files:
        report_path = generate_report(processed_files)
        print(f"\n📄 Report generated successfully: {report_path}")
        logger.info("Report generated successfully: %s", report_path)
    else:
        logger.info("No files were processed; report was not generated")

    logger.info("Automation completed successfully")


if __name__ == "__main__":
    discover_files()
