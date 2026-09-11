import json
from pathlib import Path
from typing import Any

import pandas as pd


def generate_reports(frame: pd.DataFrame, quality: dict[str, Any], analytics: dict[str, Any], output_dir: Path) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    clean_path = output_dir / "clean_business_data.csv"
    quality_path = output_dir / "data_quality_report.json"
    analytics_path = output_dir / "business_analytics.json"
    summary_path = output_dir / "business_summary.txt"
    excel_path = output_dir / "business_report.xlsx"
    frame.to_csv(clean_path, index=False)
    quality_path.write_text(json.dumps(quality, indent=2), encoding="utf-8")
    analytics_path.write_text(json.dumps(analytics, indent=2), encoding="utf-8")
    summary_path.write_text(_summary(quality, analytics), encoding="utf-8")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        pd.DataFrame([analytics]).to_excel(writer, sheet_name="Summary", index=False)
        frame.to_excel(writer, sheet_name="Clean Data", index=False)
        pd.DataFrame([quality]).to_excel(writer, sheet_name="Data Quality", index=False)
        _mapping_frame(analytics["revenue_by_category"], "category").to_excel(writer, sheet_name="Revenue by Category", index=False)
        _mapping_frame(analytics["revenue_by_region"], "region").to_excel(writer, sheet_name="Revenue by Region", index=False)
    return [str(path) for path in (clean_path, quality_path, analytics_path, summary_path, excel_path)]


def _mapping_frame(mapping: dict[str, float], label: str) -> pd.DataFrame:
    return pd.DataFrame([{label: key, "revenue": value} for key, value in mapping.items()])


def _summary(quality: dict[str, Any], analytics: dict[str, Any]) -> str:
    return "\n".join([
        "DataFlow Pro Business Summary", "=" * 30,
        f"Quality score: {quality['quality_score']}%",
        f"Input records: {quality['input_records']}",
        f"Valid records: {quality['valid_records']}",
        f"Invalid records: {quality['invalid_records']}",
        f"Duplicate records: {quality['duplicate_records']}",
        f"Total revenue: {analytics['total_revenue']:.2f}",
        f"Total orders: {analytics['total_orders']}",
        f"High-value orders: {analytics['high_value_order_count']}",
    ])
