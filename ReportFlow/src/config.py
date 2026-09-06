"""Runtime configuration for ReportFlow."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Filesystem locations and application settings."""

    project_root: Path
    input_dir: Path
    output_dir: Path
    logs_dir: Path
    required_columns: tuple[str, ...] = (
        "order_id", "order_date", "product", "category", "region",
        "quantity", "unit_price",
    )

    @classmethod
    def from_project_root(cls, project_root: Path | None = None) -> "Settings":
        root = (project_root or Path(__file__).resolve().parents[1]).resolve()
        settings = cls(root, root / "data" / "input", root / "data" / "output", root / "logs")
        settings.ensure_directories()
        return settings

    def ensure_directories(self) -> None:
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
