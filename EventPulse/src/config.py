from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    database_path: str = "data/eventpulse.sqlite3"
    environment: str = "development"
    logging_level: str = "INFO"

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            database_path=os.getenv("EVENTPULSE_DATABASE_PATH", cls.database_path),
            environment=os.getenv("EVENTPULSE_ENVIRONMENT", cls.environment),
            logging_level=os.getenv("EVENTPULSE_LOGGING_LEVEL", cls.logging_level),
        )

    def ensure_database_directory(self) -> None:
        if self.database_path != ":memory:":
            Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
