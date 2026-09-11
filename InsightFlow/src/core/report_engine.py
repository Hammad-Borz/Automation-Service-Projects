import json
from pathlib import Path
from typing import Any
import pandas as pd


def generate_reports(frame: pd.DataFrame, analytics: dict[str, Any], insights: list[dict[str, Any]], quality: dict[str, Any], output_dir: Path) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = [output_dir / name for name in ("executive_summary.txt", "analytics_report.json", "kpis.json", "clean_sales_data.csv", "insightflow_report.xlsx")]
    (output_dir / "clean_sales_data.csv").write_text(frame.to_csv(index=False), encoding="utf-8")
    (output_dir / "analytics_report.json").write_text(json.dumps({"analytics": analytics, "insights": insights, "quality": quality}, indent=2, default=str), encoding="utf-8")
    (output_dir / "kpis.json").write_text(json.dumps(analytics["kpis"], indent=2), encoding="utf-8")
    (output_dir / "executive_summary.txt").write_text(_summary(analytics, insights, quality), encoding="utf-8")
    with pd.ExcelWriter(output_dir / "insightflow_report.xlsx", engine="openpyxl") as writer:
        pd.DataFrame([_summary_row(analytics)]).to_excel(writer, sheet_name="Executive Summary", index=False)
        pd.DataFrame([analytics["kpis"]]).to_excel(writer, sheet_name="KPIs", index=False)
        pd.DataFrame(analytics["comparison"]).T.to_excel(writer, sheet_name="Period Comparison")
        pd.DataFrame(analytics["trends"]["monthly_revenue"].items(), columns=["month", "revenue"]).to_excel(writer, sheet_name="Monthly Trends", index=False)
        for key, title in (("categories", "Categories"), ("products", "Products"), ("regions", "Regions"), ("channels", "Sales Channels")):
            pd.DataFrame(analytics[key]["items"]).to_excel(writer, sheet_name=title, index=False)
        pd.DataFrame(analytics["customers"]["summary"]).T.to_excel(writer, sheet_name="Customer Segments")
        pd.DataFrame(analytics["anomalies"]).to_excel(writer, sheet_name="Anomalies", index=False)
        pd.DataFrame([quality]).to_excel(writer, sheet_name="Data Quality", index=False)
        frame.to_excel(writer, sheet_name="Clean Data", index=False)
        for sheet in writer.sheets.values():
            sheet.freeze_panes = "A2"
            for column in sheet.columns:
                letter = column[0].column_letter
                sheet.column_dimensions[letter].width = min(max(max(len(str(cell.value or "")) for cell in column) + 2, 12), 32)
    return [str(path) for path in paths]


def _summary_row(analytics):
    k = analytics["kpis"]; return {"total_revenue": k["total_revenue"], "total_orders": k["total_orders"], "completed_orders": k["completed_orders"], "average_order_value": k["average_order_value"], "unique_customers": k["unique_customers"], "revenue_growth_percent": analytics["trends"]["revenue_growth_percent"]}


def _summary(analytics, insights, quality):
    k = analytics["kpis"]
    top = {key: (analytics[key]["top"] or {}) for key in ("categories", "products", "regions", "channels")}
    lines = ["InsightFlow Executive Summary", "=" * 30, f"Reporting period: {', '.join(analytics['trends']['monthly_revenue'])}", f"Total revenue: {k['total_revenue']:.2f}", f"Total orders: {k['total_orders']}", f"Completed orders: {k['completed_orders']}", f"Average order value: {k['average_order_value']:.2f}", f"Total customers: {k['unique_customers']}", f"Revenue growth: {analytics['trends']['revenue_growth_percent']:.2f}%", f"Top category: {top['categories'].get('category', 'n/a')}", f"Top product: {top['products'].get('product', 'n/a')}", f"Top region: {top['regions'].get('region', 'n/a')}", f"Top channel: {top['channels'].get('sales_channel', 'n/a')}", f"Quality score: {quality['quality_score']:.2f}%", "", "Key insights:"]
    lines.extend(f"- {item['title']}: {item['description']} Recommendation: {item['recommendation']}" for item in insights)
    return "\n".join(lines)
