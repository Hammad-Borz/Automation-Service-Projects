"""Business data contract validation."""

import pandas as pd

from .exceptions import DataValidationError


class DataValidator:
    """Validate required fields and positive numeric values."""

    def __init__(self, required_columns: tuple[str, ...]) -> None:
        self.required_columns = required_columns

    def validate(self, frame: pd.DataFrame) -> None:
        missing = sorted(set(self.required_columns) - set(frame.columns))
        if missing:
            raise DataValidationError(f"Missing required columns: {', '.join(missing)}")
        if frame["order_id"].isna().any() or frame["order_id"].astype(str).str.strip().eq("").any():
            raise DataValidationError("order_id cannot be empty")
        for column in ("quantity", "unit_price"):
            values = pd.to_numeric(frame[column], errors="coerce")
            if values.isna().any():
                raise DataValidationError(f"{column} must be numeric")
            if (values <= 0).any():
                raise DataValidationError(f"{column} must be greater than zero")
        parsed_dates = pd.to_datetime(frame["order_date"], errors="coerce")
        if parsed_dates.isna().any():
            raise DataValidationError("order_date contains invalid dates")
