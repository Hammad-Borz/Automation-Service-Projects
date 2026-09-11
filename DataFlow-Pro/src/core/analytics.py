from typing import Any

import pandas as pd


def calculate_analytics(frame: pd.DataFrame) -> dict[str, Any]:
    if frame.empty:
        return {"total_revenue": 0.0, "total_orders": 0, "total_quantity": 0, "average_order_value": 0.0, "completed_revenue": 0.0, "cancelled_order_count": 0, "refunded_order_count": 0, "high_value_order_count": 0, "revenue_by_category": {}, "revenue_by_region": {}, "revenue_by_product": {}, "orders_by_status": {}, "monthly_revenue": {}}
    frame = frame.copy()
    if "order_month" not in frame:
        frame["order_month"] = pd.to_datetime(frame["order_date"]).dt.strftime("%Y-%m")
    frame["is_high_value"] = frame["is_high_value"].astype(bool)
    revenue = frame["total_amount"]
    return {
        "total_revenue": round(float(revenue.sum()), 2),
        "total_orders": int(len(frame)),
        "total_quantity": int(frame["quantity"].sum()),
        "average_order_value": round(float(revenue.mean()), 2),
        "completed_revenue": round(float(frame.loc[frame["status"] == "completed", "total_amount"].sum()), 2),
        "cancelled_order_count": int((frame["status"] == "cancelled").sum()),
        "refunded_order_count": int((frame["status"] == "refunded").sum()),
        "high_value_order_count": int(frame["is_high_value"].sum()),
        "revenue_by_category": _sum_by(frame, "category"),
        "revenue_by_region": _sum_by(frame, "sales_region"),
        "revenue_by_product": _sum_by(frame, "product"),
        "orders_by_status": {str(key): int(value) for key, value in frame["status"].value_counts().to_dict().items()},
        "monthly_revenue": _sum_by(frame, "order_month"),
    }


def _sum_by(frame: pd.DataFrame, column: str) -> dict[str, float]:
    return {str(key): round(float(value), 2) for key, value in frame.groupby(column)["total_amount"].sum().to_dict().items()}
