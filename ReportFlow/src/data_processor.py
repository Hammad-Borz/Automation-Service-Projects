"""Cleaning and normalization of business data."""

import pandas as pd


class DataProcessor:
    """Normalize columns and derive row-level revenue."""

    def process(self, frame: pd.DataFrame) -> pd.DataFrame:
        result = frame.copy()
        result.columns = [str(column).strip().lower() for column in result.columns]
        text_columns = ["order_id", "product", "category", "region"]
        for column in text_columns:
            result[column] = result[column].fillna("Unknown").astype(str).str.strip()
        result["order_date"] = pd.to_datetime(result["order_date"], errors="coerce")
        result["quantity"] = pd.to_numeric(result["quantity"], errors="coerce").fillna(0)
        result["unit_price"] = pd.to_numeric(result["unit_price"], errors="coerce").fillna(0)
        result["revenue"] = (result["quantity"] * result["unit_price"]).round(2)
        result["month"] = result["order_date"].dt.to_period("M").astype(str)
        return result
