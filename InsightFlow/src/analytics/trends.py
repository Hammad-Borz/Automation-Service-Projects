from typing import Any
import pandas as pd


def calculate_trends(frame: pd.DataFrame) -> dict[str, Any]:
    if frame.empty:
        return {"daily_revenue": {}, "weekly_revenue": {}, "monthly_revenue": {}, "monthly_orders": {}, "monthly_units": {}, "monthly_aov": {}, "trend_direction": "stable", "revenue_growth_percent": 0.0, "order_growth_percent": 0.0, "aov_growth_percent": 0.0}
    data = frame.copy()
    data["period"] = data["order_date"].dt.to_period("M").astype(str)
    monthly = data.groupby("period").agg(revenue=("calculated_total", "sum"), orders=("order_id", "count"), units=("quantity", "sum"))
    monthly["aov"] = monthly["revenue"].div(monthly["orders"].replace(0, pd.NA)).fillna(0)
    revenue = data.groupby(data["order_date"].dt.strftime("%Y-%m-%d"))["calculated_total"].sum()
    weekly = data.groupby(data["order_date"].dt.to_period("W").astype(str))["calculated_total"].sum()
    growth = _growth(monthly["revenue"]); order_growth = _growth(monthly["orders"]); aov_growth = _growth(monthly["aov"])
    return {"daily_revenue": _series(revenue), "weekly_revenue": _series(weekly), "monthly_revenue": _series(monthly["revenue"]), "monthly_orders": {str(k): int(v) for k, v in monthly["orders"].items()}, "monthly_units": {str(k): int(v) for k, v in monthly["units"].items()}, "monthly_aov": _series(monthly["aov"]), "trend_direction": _direction(growth), "revenue_growth_percent": growth, "order_growth_percent": order_growth, "aov_growth_percent": aov_growth}


def _growth(series: pd.Series) -> float:
    if len(series) < 2 or series.iloc[-2] == 0: return 0.0
    return round(float((series.iloc[-1] - series.iloc[-2]) / series.iloc[-2] * 100), 2)


def _direction(growth: float) -> str:
    return "increasing" if growth > 5 else "decreasing" if growth < -5 else "stable"


def _series(series: pd.Series) -> dict[str, float]:
    return {str(k): round(float(v), 2) for k, v in series.items()}
