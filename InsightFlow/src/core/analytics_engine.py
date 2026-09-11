from typing import Any
import pandas as pd
from src.analytics.anomalies import detect_anomalies
from src.analytics.comparisons import compare_periods
from src.analytics.kpis import calculate_kpis
from src.analytics.segmentation import segment_customers
from src.analytics.trends import calculate_trends


def analyze(frame: pd.DataFrame, high_value_threshold: float = 1000.0, anomaly_z_threshold: float = 2.0) -> dict[str, Any]:
    result = {"kpis": calculate_kpis(frame, high_value_threshold), "trends": calculate_trends(frame), "comparison": compare_periods(frame), "categories": _breakdown(frame, "category"), "products": _breakdown(frame, "product"), "regions": _breakdown(frame, "region"), "channels": _breakdown(frame, "sales_channel"), "customers": segment_customers(frame), "anomalies": detect_anomalies(frame, anomaly_z_threshold)}
    for key in ("categories", "products", "regions", "channels"):
        result[key]["top"] = max(result[key]["items"], key=lambda item: item["revenue"], default=None)
    return result


def _breakdown(frame: pd.DataFrame, group: str) -> dict[str, Any]:
    if frame.empty: return {"items": [], "top": None, "lowest": None}
    grouped = frame.groupby(group).agg(revenue=("calculated_total", "sum"), orders=("order_id", "count"), units=("quantity", "sum"), aov=("calculated_total", "mean")).reset_index()
    total = grouped.revenue.sum()
    grouped["revenue_share_percent"] = grouped.revenue / total * 100 if total else 0
    items = [{group: str(row[group]), "revenue": round(float(row["revenue"]), 2), "orders": int(row["orders"]), "units": int(row["units"]), "aov": round(float(row["aov"]), 2), "revenue_share_percent": round(float(row["revenue_share_percent"]), 2)} for row in grouped.to_dict("records")]
    return {"items": sorted(items, key=lambda item: item["revenue"], reverse=True), "top": items[0] if items else None, "lowest": items[-1] if items else None}
