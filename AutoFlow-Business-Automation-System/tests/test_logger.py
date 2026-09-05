import logging

import logger
from logger import setup_logger


def test_setup_logger(tmp_path, monkeypatch):
    fake_src_folder = tmp_path / "src"
    fake_src_folder.mkdir()

    fake_file = fake_src_folder / "logger.py"
    fake_file.touch()

    monkeypatch.setattr(
        logger,
        "__file__",
        str(fake_file)
    )

    test_logger = setup_logger()

    assert test_logger.name == "autoflow"

    test_logger.info("Test log message")

    logging.shutdown()

    log_file = tmp_path / "logs" / "autoflow.log"

    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")

    assert "Test log message" in content
    assert "INFO" in content