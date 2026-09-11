from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    project_root: Path
    data_dir: Path
    input_dir: Path
    output_dir: Path
    database_path: Path
    default_input_path: Path
    anomaly_z_threshold: float = 2.0
    high_value_threshold: float = 1000.0
    logging_level: str = "INFO"

    @classmethod
    def for_project(cls, root: Path | None = None) -> "Settings":
        project_root = (root or Path(__file__).resolve().parents[1]).resolve()
        data_dir = project_root / "data"
        return cls(project_root, data_dir, data_dir / "input", data_dir / "output", data_dir / "insightflow.sqlite3", data_dir / "input" / "sample_sales_data.csv", float(os.getenv("INSIGHTFLOW_ANOMALY_Z", "2.0")), float(os.getenv("INSIGHTFLOW_HIGH_VALUE", "1000")), os.getenv("INSIGHTFLOW_LOG_LEVEL", "INFO"))

    def ensure_directories(self) -> None:
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
