from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import OUTPUT_DIR


class ReportingService:
    def __init__(self, output_dir: str | Path | None = None):
        self.output_dir = Path(output_dir) if output_dir else OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_report(self, analytics: dict[str, Any], customers: list[Any], orders: list[Any], tasks: list[Any], notifications: list[Any]) -> dict[str, Any]:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        txt_path = self.output_dir / "businesscore_report.txt"
        json_path = self.output_dir / "businesscore_analytics.json"
        csv_path = self.output_dir / "businesscore_orders.csv"
        xlsx_path = self.output_dir / "businesscore_report.xlsx"

        order_df = pd.DataFrame([
            {
                "id": o.id,
                "customer_id": o.customer_id,
                "product": o.product,
                "category": o.category,
                "quantity": o.quantity,
                "unit_price": o.unit_price,
                "total_amount": o.total_amount,
                "priority": o.priority,
                "status": o.status,
                "source": o.source,
                "created_at": str(o.created_at),
            }
            for o in orders
        ])

        if not order_df.empty:
            order_df.to_csv(csv_path, index=False)
        else:
            pd.DataFrame(columns=["id", "customer_id", "product", "category", "quantity", "unit_price", "total_amount", "priority", "status", "source", "created_at"]).to_csv(csv_path, index=False)

        txt_content = self._build_text_report(analytics, timestamp)
        txt_path.write_text(txt_content, encoding="utf-8")

        json_path.write_text(json.dumps(analytics, indent=2, sort_keys=True), encoding="utf-8")

        workbook = {
            "report_title": "BusinessCore Operating Report",
            "generated_at": timestamp,
            "summary": analytics,
            "customer_count": len(customers),
            "order_count": len(orders),
            "task_count": len(tasks),
            "notification_count": len(notifications),
        }
        pd.DataFrame([workbook]).to_excel(xlsx_path, index=False)

        return {
            "report_file": str(txt_path),
            "analytics_file": str(json_path),
            "csv_file": str(csv_path),
            "excel_file": str(xlsx_path),
        }

    def _build_text_report(self, analytics: dict[str, Any], timestamp: str) -> str:
        lines = [
            "BusinessCore — End-to-End Business Automation System",
            "=" * 60,
            f"Generated: {timestamp}",
            "",
            "Business Summary",
            "-" * 60,
            f"Total customers: {analytics.get('total_customers', 0)}",
            f"Active customers: {analytics.get('active_customers', 0)}",
            f"Total orders: {analytics.get('total_orders', 0)}",
            f"Total revenue: ${analytics.get('total_revenue', 0):,.2f}",
            f"Average order value: ${analytics.get('average_order_value', 0):,.2f}",
            f"Pending tasks: {analytics.get('pending_tasks', 0)}",
            f"Generated notifications: {analytics.get('notifications_generated', 0)}",
            "",
            "Operational Observations",
            "-" * 60,
            "1. Automated order intake is validated and routed through the business workflow.",
            "2. Customer matching and creation are handled deterministically for repeat requests.",
            "3. Business rules create operational tasks and notification records automatically.",
            "4. The workflow maintains an immutable audit trail and KPI summaries.",
        ]
        return "\n".join(lines) + "\n"
