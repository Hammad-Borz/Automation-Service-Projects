import pytest
from pydantic import ValidationError

from src.api.schemas import CreateJobRequest


def test_valid_job_request():
    request = CreateJobRequest(
        automation_type="create_task",
        payload={"title": "Follow up with customer", "priority": "high"},
        request_id="REQ-001",
    )
    assert request.automation_type == "create_task"
    assert request.payload["priority"] == "high"


def test_missing_required_fields():
    with pytest.raises(ValidationError):
        CreateJobRequest(automation_type="create_task", payload={})


def test_empty_automation_type_invalid():
    with pytest.raises(ValidationError):
        CreateJobRequest(automation_type="  ", payload={"title": "x"}, request_id="REQ-002")


def test_payload_validation_rejects_empty_object():
    with pytest.raises(ValidationError):
        CreateJobRequest(automation_type="create_task", payload={}, request_id="REQ-003")
