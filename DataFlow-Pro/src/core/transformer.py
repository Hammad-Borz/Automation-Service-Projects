import pandas as pd


def transform_dataframe(frame: pd.DataFrame, high_value_threshold: float) -> pd.DataFrame:
    transformed = frame.copy()
    transformed["quantity"] = pd.to_numeric(transformed["quantity"], errors="coerce").astype("Int64")
    transformed["unit_price"] = pd.to_numeric(transformed["unit_price"], errors="coerce")
    transformed["total_amount"] = transformed["quantity"] * transformed["unit_price"]
    transformed["total_amount"] = transformed["total_amount"].round(2)
    transformed["order_month"] = pd.to_datetime(transformed["order_date"]).dt.strftime("%Y-%m")
    transformed["order_year"] = pd.to_datetime(transformed["order_date"]).dt.year
    transformed["calculated_total"] = transformed["total_amount"]
    transformed["is_high_value"] = transformed["total_amount"] >= high_value_threshold
    transformed["processing_status"] = "valid"
    return transformed
