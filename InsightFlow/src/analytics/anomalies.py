from typing import Any
import pandas as pd


def detect_anomalies(frame: pd.DataFrame, z_threshold: float = 2.0) -> list[dict[str, Any]]:
    if frame.empty: return []
    daily = frame.groupby(frame["order_date"].dt.strftime("%Y-%m-%d")).agg(revenue=("calculated_total", "sum"), orders=("order_id", "count"))
    anomalies = []
    for metric in ("revenue", "orders"):
        values = daily[metric]
        if len(values) < 4 or values.std(ddof=0) == 0: continue
        mean = float(values.mean()); std = float(values.std(ddof=0))
        for date, value in values.items():
            deviation = (float(value) - mean) / std
            if abs(deviation) >= z_threshold:
                anomalies.append({"date": str(date), "metric": metric, "value": round(float(value), 2), "baseline": round(mean, 2), "deviation": round(deviation, 2), "anomaly_type": "spike" if deviation > 0 else "drop", "severity": "high" if abs(deviation) >= 3 else "medium" if abs(deviation) >= 2.5 else "low"})
    return anomalies
