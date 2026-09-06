"""Typed result models for the pipeline."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class AnalyticsResult:
    """SQL-derived business analytics."""

    kpis: dict[str, Any]
    by_region: pd.DataFrame
    by_product: pd.DataFrame
    by_category: pd.DataFrame
    monthly: pd.DataFrame
    top_products: pd.DataFrame


@dataclass(frozen=True)
class WorkflowResult:
    """Summary returned by a completed workflow."""

    source: Path
    database_path: Path
    records_processed: int
    database_records: int
    analytics: AnalyticsResult
    report_paths: tuple[Path, ...]
