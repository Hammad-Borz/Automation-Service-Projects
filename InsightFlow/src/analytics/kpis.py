from typing import Any
import pandas as pd


def calculate_kpis(frame: pd.DataFrame, high_value_threshold: float = 1000.0) -> dict[str, Any]:
    if frame.empty:
        return {key: 0 for key in ("total_revenue", "completed_revenue", "total_orders", "completed_orders", "cancelled_orders", "refunded_orders", "pending_orders", "total_units_sold", "average_order_value", "average_units_per_order", "unique_customers", "revenue_per_customer", "high_value_order_count", "completion_rate", "cancellation_rate", "refund_rate")}
    revenue = frame["calculated_total"]
    completed = frame[frame["status"] == "completed"]
    total_orders = len(frame)
    completed_orders = len(completed)
    completed_revenue = float(completed["calculated_total"].sum())
    return {
        "total_revenue": round(float(revenue.sum()), 2), "completed_revenue": round(completed_revenue, 2),
        "total_orders": total_orders, "completed_orders": completed_orders,
        "cancelled_orders": int((frame["status"] == "cancelled").sum()), "refunded_orders": int((frame["status"] == "refunded").sum()),
        "pending_orders": int((frame["status"] == "pending").sum()), "total_units_sold": int(frame["quantity"].sum()),
        "average_order_value": round(completed_revenue / completed_orders, 2) if completed_orders else 0.0,
        "average_units_per_order": round(float(frame["quantity"].mean()), 2), "unique_customers": int(frame["customer_id"].nunique()),
        "revenue_per_customer": round(float(revenue.sum()) / frame["customer_id"].nunique(), 2) if frame["customer_id"].nunique() else 0.0,
        "high_value_order_count": int((revenue >= high_value_threshold).sum()),
        "completion_rate": round(completed_orders / total_orders * 100, 2) if total_orders else 0.0,
        "cancellation_rate": round((frame["status"] == "cancelled").sum() / total_orders * 100, 2) if total_orders else 0.0,
        "refund_rate": round((frame["status"] == "refunded").sum() / total_orders * 100, 2) if total_orders else 0.0,
    }
