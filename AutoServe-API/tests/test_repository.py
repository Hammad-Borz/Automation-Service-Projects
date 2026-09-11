from src.database.repository import AutomationRepository
from src.models.automation import ActionResult, AuditLog, AutomationJob, AutomationRun, JobStatus, RunStatus


def test_database_initialization(temp_db):
    repo = AutomationRepository()
    repo.initialize()
    assert repo.get_job_by_id("missing") is None


def test_create_and_retrieve_job(temp_db):
    repo = AutomationRepository()
    job = AutomationJob(
        id="JOB-1",
        request_id="REQ-100",
        automation_type="create_task",
        payload={"title": "Task", "priority": "high"},
        status=JobStatus.PENDING,
    )
    repo.create_job(job)
    fetched = repo.get_job_by_id("JOB-1")
    assert fetched is not None
    assert fetched.request_id == "REQ-100"


def test_list_jobs(temp_db):
    repo = AutomationRepository()
    repo.create_job(AutomationJob("JOB-2", "REQ-200", "update_customer_status", {"customer_id": "CUST-1", "status": "active"}, JobStatus.PENDING))
    repo.create_job(AutomationJob("JOB-3", "REQ-300", "send_notification", {"recipient": "a@b.com", "message": "hello"}, JobStatus.FAILED))
    jobs = repo.list_jobs()
    assert len(jobs) == 2
    assert jobs[0].automation_type in {"update_customer_status", "send_notification"}


def test_create_and_retrieve_run(temp_db):
    repo = AutomationRepository()
    repo.create_job(AutomationJob("JOB-4", "REQ-400", "create_task", {"title": "x"}, JobStatus.PENDING))
    run = AutomationRun("RUN-1", "JOB-4", RunStatus.RUNNING, 1)
    repo.create_run(run)
    fetched = repo.get_run_by_id("RUN-1")
    assert fetched is not None
    assert fetched.job_id == "JOB-4"


def test_action_result_persistence(temp_db):
    repo = AutomationRepository()
    result = ActionResult("RES-1", "RUN-1", "create_task", True, {"status": "ok"})
    repo.create_action_result(result)
    fetched = repo.get_action_result_for_run("RUN-1")
    assert fetched is not None
    assert fetched.success is True


def test_audit_persistence(temp_db):
    repo = AutomationRepository()
    log = AuditLog("AUD-1", "JOB-1", "RUN-1", "JOB_CREATED", "Created", {"request_id": "REQ-1"})
    repo.create_audit_log(log)
    logs = repo.list_audit_logs(job_id="JOB-1")
    assert len(logs) == 1
    assert logs[0].event_type == "JOB_CREATED"
