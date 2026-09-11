from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    project_dir: Path
    database_path: Path
    default_input_path: Path
    output_dir: Path
    high_value_threshold: float = 1000.0
    environment: str = "development"
    logging_level: str = "INFO"

    @classmethod
    def for_project(cls, project_dir: Path | None = None) -> "Settings":
        root = (project_dir or Path(__file__).resolve().parents[1]).resolve()
        data_dir = root / "data"
        return cls(
            project_dir=root,
            database_path=Path(os.getenv("DATAFLOW_DATABASE_PATH", data_dir / "dataflow.sqlite3")),
            default_input_path=data_dir / "input" / "sample_business_data.csv",
            output_dir=data_dir / "output",
            high_value_threshold=float(os.getenv("DATAFLOW_HIGH_VALUE_THRESHOLD", "1000")),
            environment=os.getenv("DATAFLOW_ENVIRONMENT", "development"),
            logging_level=os.getenv("DATAFLOW_LOGGING_LEVEL", "INFO"),
        )

    def ensure_directories(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
