from pathlib import Path

from src.config import Settings


def test_settings_create_project_directories(tmp_path: Path) -> None:
    settings = Settings.from_project_root(tmp_path)
    assert settings.input_dir.is_dir()
    assert settings.output_dir.is_dir()
    assert settings.logs_dir.is_dir()
