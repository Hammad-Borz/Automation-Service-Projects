from pathlib import Path

from src.config import Settings


def test_settings_create_all_directories(tmp_path: Path) -> None:
    settings = Settings.from_project_root(tmp_path)
    assert settings.project_root == tmp_path.resolve()
    assert all(path.is_dir() for path in (settings.data_dir, settings.input_dir, settings.output_dir, settings.database_dir, settings.logs_dir))
    assert settings.database_path == tmp_path.resolve() / "database" / "dataops.db"
