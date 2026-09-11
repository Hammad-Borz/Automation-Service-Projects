from typing import Any
import pandas as pd


def segment_customers(frame: pd.DataFrame) -> dict[str, Any]:
    if frame.empty:
        return {"customers": [], "summary": {}}
    customer = frame.groupby(["customer_id", "customer_name"], as_index=False).agg(revenue=("calculated_total", "sum"), orders=("order_id", "count"))
    low = customer.revenue.quantile(0.25); high = customer.revenue.quantile(0.75)
    customer["segment"] = customer.revenue.map(lambda value: "high_value" if value >= high else "low_value" if value <= low else "regular")
    summary = customer.groupby("segment").agg(customer_count=("customer_id", "count"), revenue=("revenue", "sum"), orders=("orders", "sum"), average_customer_revenue=("revenue", "mean")).round(2).to_dict("index")
    return {"customers": customer.round(2).to_dict("records"), "summary": summary, "thresholds": {"low_value_max": round(float(low), 2), "high_value_min": round(float(high), 2)}}
