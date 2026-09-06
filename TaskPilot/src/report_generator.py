"""Human-readable task reporting."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .models import Status
from .task_manager import TaskManager


def generate_report(manager: TaskManager, report_dir: str | Path | None = None) -> Path:
    destination = Path(report_dir) if report_dir else Path(__file__).resolve().parents[1] / "reports"
    destination.mkdir(parents=True, exist_ok=True)
    tasks = manager.list_tasks()
    summary = manager.get_task_summary()
    grouped = {Status.PENDING: [], Status.COMPLETED: []}
    for task in tasks:
        grouped[task.status].append(task.title)
    timestamp = datetime.now(timezone.utc)
    lines = ["TASKPILOT TASK REPORT", f"Generated (UTC): {timestamp.isoformat()}", "", f"Total tasks: {summary.total_tasks}", f"Pending tasks: {summary.pending_tasks}", f"Completed tasks: {summary.completed_tasks}", "", "Priority breakdown:"]
    lines.extend(f"- {priority.title()}: {count}" for priority, count in summary.priority_breakdown.items())
    for status in (Status.PENDING, Status.COMPLETED):
        lines.append("")
        lines.append(f"{status.value.title()} tasks:")
        lines.extend(f"- {title}" for title in grouped[status])
        if not grouped[status]:
            lines.append("- None")
    path = destination / f"task_report_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
