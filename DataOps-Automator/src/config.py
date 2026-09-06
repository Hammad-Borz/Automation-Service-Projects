"""Centralized filesystem configuration."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Project paths used by the workflow."""

    project_root: Path
    data_dir: Path
    input_dir: Path
    output_dir: Path
    database_dir: Path
    database_path: Path
    logs_dir: Path
    required_columns: tuple[str, ...] = (
        "order_id", "order_date", "customer", "region", "product",
        "category", "quantity", "unit_price",
    )

    @classmethod
    def from_project_root(cls, project_root: Path | None = None) -> "Settings":
        root = (project_root or Path(__file__).resolve().parents[1]).resolve()
        settings = cls(
            project_root=root,
            data_dir=root / "data",
            input_dir=root / "data" / "input",
            output_dir=root / "data" / "output",
            database_dir=root / "database",
            database_path=root / "database" / "dataops.db",
            logs_dir=root / "logs",
        )
        settings.ensure_directories()
        return settings

    def ensure_directories(self) -> None:
        for directory in (self.data_dir, self.input_dir, self.output_dir, self.database_dir, self.logs_dir):
            directory.mkdir(parents=True, exist_ok=True)
