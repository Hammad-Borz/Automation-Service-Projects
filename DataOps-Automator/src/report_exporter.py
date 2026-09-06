"""CSV and human-readable report exports."""

from pathlib import Path

from .exceptions import ReportExportError
from .models import AnalyticsResult


class ReportExporter:
    """Write analytics tables and an executive text report."""

    def export(self, analytics: AnalyticsResult, output_dir: Path) -> tuple[Path, ...]:
        output_dir.mkdir(parents=True, exist_ok=True)
        tables = {
            "kpi_summary.csv": self._kpi_frame(analytics),
            "revenue_by_region.csv": analytics.by_region,
            "revenue_by_product.csv": analytics.by_product,
            "revenue_by_category.csv": analytics.by_category,
            "monthly_revenue.csv": analytics.monthly,
            "top_products.csv": analytics.top_products,
        }
        paths: list[Path] = []
        try:
            for filename, frame in tables.items():
                path = output_dir / filename
                frame.to_csv(path, index=False)
                paths.append(path)
            text_path = output_dir / "business_report.txt"
            text_path.write_text(self._text_report(analytics), encoding="utf-8")
            paths.append(text_path)
        except (OSError, ValueError) as exc:
            raise ReportExportError(f"Could not export reports: {exc}") from exc
        return tuple(paths)

    @staticmethod
    def _kpi_frame(analytics: AnalyticsResult):
        import pandas as pd
        return pd.DataFrame([analytics.kpis])

    @staticmethod
    def _text_report(analytics: AnalyticsResult) -> str:
        kpi = analytics.kpis
        top_region = analytics.by_region.iloc[0]["region"] if not analytics.by_region.empty else "N/A"
        top_product = analytics.by_product.iloc[0]["product"] if not analytics.by_product.empty else "N/A"
        return "\n".join([
            "DATAOPS AUTOMATOR - BUSINESS REPORT", "=" * 40, "",
            "EXECUTIVE SUMMARY", "------------------",
            f"Total revenue: ${kpi['total_revenue']:,.2f}",
            f"Total orders: {kpi['total_orders']}",
            f"Average order value: ${kpi['average_order_value']:,.2f}",
            f"Total quantity sold: {kpi['total_quantity_sold']}",
            f"Top region: {top_region}", f"Top product: {top_product}", "",
            "Revenue by region", "------------------", analytics.by_region.to_string(index=False), "",
            "Revenue by product", "-------------------", analytics.by_product.to_string(index=False), "",
        ])
