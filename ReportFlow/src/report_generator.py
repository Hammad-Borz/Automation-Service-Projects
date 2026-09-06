"""Human-readable report generation."""

from pathlib import Path

from .models import AnalyticsResult


class ReportGenerator:
    """Render a concise executive report as plain text."""

    def generate(self, analytics: AnalyticsResult, destination: Path) -> Path:
        kpi = analytics.kpis
        lines = [
            "REPORTFLOW BUSINESS PERFORMANCE REPORT", "=" * 44, "",
            "EXECUTIVE SUMMARY", "------------------",
            f"Revenue reached ${kpi['total_revenue']:,.2f} across {kpi['total_orders']} orders and {kpi['total_units']} units.",
            f"Average order value was ${kpi['average_order_value']:,.2f}.", "",
            "KPI SUMMARY", "-----------",
            f"Total revenue: ${kpi['total_revenue']:,.2f}", f"Total orders: {kpi['total_orders']}",
            f"Average order value: ${kpi['average_order_value']:,.2f}", f"Units sold: {kpi['total_units']}", "",
        ]
        for title, table in ((
            ("REVENUE BY PRODUCT", analytics.by_product),
            ("REVENUE BY CATEGORY", analytics.by_category),
            ("REVENUE BY REGION", analytics.by_region),
            ("MONTHLY PERFORMANCE", analytics.monthly),
            ("TOP PERFORMERS", analytics.top_products),
        )):
            lines.extend([title, "-" * len(title), table.to_string(index=False, float_format=lambda value: f"{value:,.2f}"), ""])
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("\n".join(lines), encoding="utf-8")
        return destination
