from typing import Any
import pandas as pd


def compare_periods(frame: pd.DataFrame) -> dict[str, Any]:
    if frame.empty:
        return {"revenue": _metric(0, 0), "orders": _metric(0, 0), "aov": _metric(0, 0), "units": _metric(0, 0), "customers": _metric(0, 0)}
    periods = sorted(frame["order_date"].dt.to_period("M").unique())
    current = frame[frame["order_date"].dt.to_period("M") == periods[-1]]
    previous = frame[frame["order_date"].dt.to_period("M") == periods[-2]] if len(periods) > 1 else frame.iloc[0:0]
    values = {"revenue": (current.calculated_total.sum(), previous.calculated_total.sum()), "orders": (len(current), len(previous)), "aov": (_aov(current), _aov(previous)), "units": (current.quantity.sum(), previous.quantity.sum()), "customers": (current.customer_id.nunique(), previous.customer_id.nunique())}
    return {key: _metric(*value) for key, value in values.items()}


def _aov(frame: pd.DataFrame) -> float: return float(frame.calculated_total.sum() / len(frame)) if len(frame) else 0.0

def _metric(current: float, previous: float) -> dict[str, float]:
    change = float(current - previous)
    growth = round(change / previous * 100, 2) if previous else 0.0
    return {"current": round(float(current), 2), "previous": round(float(previous), 2), "change": round(change, 2), "growth_percent": growth}
