from pathlib import Path

from file_validator import validate_file
from file_organizer import organize_file
from data_processor import process_text_file, process_csv_file
from report_generator import generate_report
from logger import setup_logger


def discover_files():
    logger = setup_logger()

    project_folder = Path(__file__).resolve().parent.parent
    input_folder = project_folder / "input"

    files = [
        file for file in input_folder.iterdir()
        if file.is_file()
    ]

    processed_files = []

    print(f"\nFiles found: {len(files)}\n")
    logger.info("Automation started")
    logger.info(f"Files found: {len(files)}")

    for file in files:
        is_valid, message = validate_file(file)

        if not is_valid:
            print(f"❌ {file.name} → {message}")
            logger.warning(f"{file.name} → {message}")
            continue

        print(f"✅ {file.name} → {message}")
        logger.info(f"{file.name} → {message}")

        organized, destination = organize_file(file)

        if not organized:
            print(f"❌ {file.name} → {destination}")
            logger.error(f"{file.name} → {destination}")
            continue

        print(f"📂 {file.name} → Moved to {destination.parent.name}")
        logger.info(f"{file.name} moved to {destination.parent.name}")

        if destination.suffix.lower() == ".txt":
            processed_data = process_text_file(destination)

        elif destination.suffix.lower() == ".csv":
            processed_data = process_csv_file(destination)

        else:
            continue

        processed_files.append(processed_data)

        print(f"📊 Processed data: {processed_data}")
        logger.info(f"{file.name} processed successfully")

    if processed_files:
        report_path = generate_report(processed_files)

        print(f"\n📄 Report generated successfully: {report_path}")
        logger.info(f"Report generated successfully: {report_path}")

    logger.info("Automation completed successfully")


if __name__ == "__main__":
    discover_files()