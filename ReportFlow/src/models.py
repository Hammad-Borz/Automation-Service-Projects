"""Data models used by the reporting workflow."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class AnalyticsResult:
    """Calculated business views used by report exporters."""

    kpis: dict[str, Any]
    by_product: pd.DataFrame
    by_category: pd.DataFrame
    by_region: pd.DataFrame
    monthly: pd.DataFrame
    top_products: pd.DataFrame


@dataclass(frozen=True)
class WorkflowResult:
    """Locations and metrics produced by one completed run."""

    source: Path
    excel_report: Path
    text_report: Path
    csv_exports: tuple[Path, ...]
    analytics: AnalyticsResult
