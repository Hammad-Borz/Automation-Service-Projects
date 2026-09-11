from pathlib import Path

import pandas as pd

from src.core.cleaner import clean_dataframe
from src.core.quality import detect_duplicates
from src.core.transformer import transform_dataframe
from src.core.validator import validate_dataframe


def process_frame(frame: pd.DataFrame, source: str, high_value_threshold: float) -> dict:
    cleaned = clean_dataframe(frame, source)
    validation = validate_dataframe(cleaned)
    valid_ids = {result.record_id for result in validation if result.valid}
    valid = cleaned[cleaned["record_id"].isin(valid_ids)].copy()
    canonical, duplicate_count = detect_duplicates(valid)
    transformed = transform_dataframe(canonical, high_value_threshold) if not canonical.empty else canonical
    return {"cleaned": cleaned, "validation": validation, "valid": transformed, "duplicate_count": duplicate_count}
