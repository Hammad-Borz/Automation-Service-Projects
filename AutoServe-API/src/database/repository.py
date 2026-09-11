from __future__ import annotations

import json
import sqlite3
from typing import Any

from src.database.connection import get_connection
from src.models.automation import ActionResult, AuditLog, AutomationJob, AutomationRun, JobStatus, RunStatus


class RepositoryError(RuntimeError):
    """Raised when repository operations fail."""


class AutomationRepository:
    """Repository layer for automation jobs, runs, results, and audit records."""

    def __init__(self, connection_factory=get_connection):
        self._connection_factory = connection_factory

    def initialize(self) -> None:
        from src.database.connection import initialize_database

        initialize_database()

    def create_job(self, job: AutomationJob) -> AutomationJob:
        with self._connection_factory() as conn:
            conn.execute(
                """
                INSERT INTO automation_jobs (
                    id, request_id, automation_type, payload, status, retry_count,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job.id,
                    job.request_id,
                    job.automation_type,
                    json.dumps(job.payload),
                    job.status.value,
                    job.retry_count,
                    job.created_at.isoformat(),
                    job.updated_at.isoformat(),
                ),
            )
            conn.commit()
        return job

    def get_job_by_id(self, job_id: str) -> AutomationJob | None:
        with self._connection_factory() as conn:
            row = conn.execute(
                "SELECT * FROM automation_jobs WHERE id = ?",
                (job_id,),
            ).fetchone()
        if row is None:
            return None
        return AutomationJob.from_row(dict(row))

    def get_job_by_request_id(self, request_id: str) -> AutomationJob | None:
        with self._connection_factory() as conn:
            row = conn.execute(
                "SELECT * FROM automation_jobs WHERE request_id = ?",
                (request_id,),
            ).fetchone()
        if row is None:
            return None
        return AutomationJob.from_row(dict(row))

    def list_jobs(self, status: str | None = None, automation_type: str | None = None) -> list[AutomationJob]:
        query = "SELECT * FROM automation_jobs"
        clauses: list[str] = []
        values: list[str] = []
        if status:
            clauses.append("status = ?")
            values.append(status)
        if automation_type:
            clauses.append("automation_type = ?")
            values.append(automation_type)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY created_at DESC"
        with self._connection_factory() as conn:
            rows = conn.execute(query, values).fetchall()
        return [AutomationJob.from_row(dict(row)) for row in rows]

    def update_job(self, job: AutomationJob) -> AutomationJob:
        with self._connection_factory() as conn:
            conn.execute(
                """
                UPDATE automation_jobs
                SET status = ?, retry_count = ?, updated_at = ?
                WHERE id = ?
                """,
                (job.status.value, job.retry_count, job.updated_at.isoformat(), job.id),
            )
            conn.commit()
        return job

    def create_run(self, run: AutomationRun) -> AutomationRun:
        with self._connection_factory() as conn:
            conn.execute(
                """
                INSERT INTO automation_runs (
                    id, job_id, status, attempt_number, started_at, completed_at, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run.id,
                    run.job_id,
                    run.status.value,
                    run.attempt_number,
                    run.started_at.isoformat(),
                    run.completed_at.isoformat() if run.completed_at else None,
                    run.error_message,
                ),
            )
            conn.commit()
        return run

    def get_run_by_id(self, run_id: str) -> AutomationRun | None:
        with self._connection_factory() as conn:
            row = conn.execute(
                "SELECT * FROM automation_runs WHERE id = ?",
                (run_id,),
            ).fetchone()
        if row is None:
            return None
        return AutomationRun.from_row(dict(row))

    def list_runs(self, job_id: str | None = None, status: str | None = None) -> list[AutomationRun]:
        query = "SELECT * FROM automation_runs"
        clauses: list[str] = []
        values: list[str] = []
        if job_id:
            clauses.append("job_id = ?")
            values.append(job_id)
        if status:
            clauses.append("status = ?")
            values.append(status)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY started_at DESC"
        with self._connection_factory() as conn:
            rows = conn.execute(query, values).fetchall()
        return [AutomationRun.from_row(dict(row)) for row in rows]

    def update_run(self, run: AutomationRun) -> AutomationRun:
        with self._connection_factory() as conn:
            conn.execute(
                """
                UPDATE automation_runs
                SET status = ?, completed_at = ?, error_message = ?
                WHERE id = ?
                """,
                (
                    run.status.value,
                    run.completed_at.isoformat() if run.completed_at else None,
                    run.error_message,
                    run.id,
                ),
            )
            conn.commit()
        return run

    def create_action_result(self, result: ActionResult) -> ActionResult:
        with self._connection_factory() as conn:
            conn.execute(
                """
                INSERT INTO action_results (id, run_id, action_type, success, result, error_message, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    result.id,
                    result.run_id,
                    result.action_type,
                    int(result.success),
                    json.dumps(result.result),
                    result.error_message,
                    result.created_at.isoformat(),
                ),
            )
            conn.commit()
        return result

    def get_action_result_for_run(self, run_id: str) -> ActionResult | None:
        with self._connection_factory() as conn:
            row = conn.execute(
                "SELECT * FROM action_results WHERE run_id = ? ORDER BY created_at DESC LIMIT 1",
                (run_id,),
            ).fetchone()
        if row is None:
            return None
        return ActionResult.from_row(dict(row))

    def create_audit_log(self, log: AuditLog) -> AuditLog:
        with self._connection_factory() as conn:
            conn.execute(
                """
                INSERT INTO audit_logs (id, job_id, run_id, event_type, message, metadata, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    log.id,
                    log.job_id,
                    log.run_id,
                    log.event_type,
                    log.message,
                    json.dumps(log.metadata),
                    log.created_at.isoformat(),
                ),
            )
            conn.commit()
        return log

    def list_audit_logs(self, job_id: str | None = None, run_id: str | None = None) -> list[AuditLog]:
        query = "SELECT * FROM audit_logs"
        clauses: list[str] = []
        values: list[str] = []
        if job_id:
            clauses.append("job_id = ?")
            values.append(job_id)
        if run_id:
            clauses.append("run_id = ?")
            values.append(run_id)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY created_at DESC"
        with self._connection_factory() as conn:
            rows = conn.execute(query, values).fetchall()
        return [AuditLog.from_row(dict(row)) for row in rows]

    def metrics_summary(self) -> dict[str, Any]:
        with self._connection_factory() as conn:
            total_jobs = conn.execute("SELECT COUNT(*) FROM automation_jobs").fetchone()[0]
            pending_jobs = conn.execute("SELECT COUNT(*) FROM automation_jobs WHERE status = 'pending'").fetchone()[0]
            running_jobs = conn.execute("SELECT COUNT(*) FROM automation_jobs WHERE status = 'running'").fetchone()[0]
            completed_jobs = conn.execute("SELECT COUNT(*) FROM automation_jobs WHERE status = 'completed'").fetchone()[0]
            failed_jobs = conn.execute("SELECT COUNT(*) FROM automation_jobs WHERE status = 'failed'").fetchone()[0]
            total_runs = conn.execute("SELECT COUNT(*) FROM automation_runs").fetchone()[0]
            successful_runs = conn.execute("SELECT COUNT(*) FROM automation_runs WHERE status = 'completed'").fetchone()[0]
            failed_runs = conn.execute("SELECT COUNT(*) FROM automation_runs WHERE status = 'failed'").fetchone()[0]
        success_rate = 0.0
        if total_runs:
            success_rate = round((successful_runs / total_runs) * 100, 2)
        return {
            "total_jobs": total_jobs,
            "pending_jobs": pending_jobs,
            "running_jobs": running_jobs,
            "completed_jobs": completed_jobs,
            "failed_jobs": failed_jobs,
            "total_runs": total_runs,
            "successful_runs": successful_runs,
            "failed_runs": failed_runs,
            "success_rate": success_rate,
        }
