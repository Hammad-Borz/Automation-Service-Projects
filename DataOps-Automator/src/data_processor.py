"""Data cleaning and transformation."""

import pandas as pd


class DataProcessor:
    """Create a normalized, database-ready copy of sales data."""

    def process(self, frame: pd.DataFrame) -> pd.DataFrame:
        result = frame.copy()
        result.columns = [str(column).strip().lower() for column in result.columns]
        for column in ("order_id", "customer", "region", "product", "category"):
            result[column] = result[column].astype(str).str.strip()
        result["order_date"] = pd.to_datetime(result["order_date"], errors="coerce")
        result["quantity"] = pd.to_numeric(result["quantity"], errors="coerce").astype(int)
        result["unit_price"] = pd.to_numeric(result["unit_price"], errors="coerce").astype(float)
        result["revenue"] = (result["quantity"] * result["unit_price"]).round(2)
        result["month"] = result["order_date"].dt.to_period("M").astype(str)
        return result
