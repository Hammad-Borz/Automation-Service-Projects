"""Business metric calculations."""

import pandas as pd

from .models import AnalyticsResult


class Analytics:
    """Build reusable aggregate views from processed orders."""

    def calculate(self, frame: pd.DataFrame) -> AnalyticsResult:
        total_revenue = float(frame["revenue"].sum())
        total_orders = int(frame["order_id"].nunique())
        total_units = int(frame["quantity"].sum())
        kpis = {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "total_units": total_units,
            "average_order_value": round(total_revenue / total_orders, 2) if total_orders else 0.0,
        }
        by_product = self._aggregate(frame, "product")
        by_category = self._aggregate(frame, "category")
        by_region = self._aggregate(frame, "region")
        monthly = self._aggregate(frame, "month").sort_values("month")
        top_products = by_product.head(5).copy()
        return AnalyticsResult(kpis, by_product, by_category, by_region, monthly, top_products)

    @staticmethod
    def _aggregate(frame: pd.DataFrame, dimension: str) -> pd.DataFrame:
        return (frame.groupby(dimension, as_index=False)
                .agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"), units=("quantity", "sum"))
                .sort_values("revenue", ascending=False)
                .reset_index(drop=True))
