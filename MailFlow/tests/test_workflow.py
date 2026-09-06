from src.models import EmailCategory, Priority
from src.response_generator import DemoResponseGenerator
from src.workflow import EmailWorkflow


def test_workflow_processes_and_records_result(sample_email) -> None:
    result = EmailWorkflow(response_generator=DemoResponseGenerator()).process(sample_email)
    assert result.category == EmailCategory.SUPPORT
    assert result.priority == Priority.MEDIUM
    assert result.suggested_response is not None
    assert any(action.action == "mark_processed" for action in result.actions)


def test_workflow_process_many(sample_email) -> None:
    assert len(EmailWorkflow().process_many([sample_email, sample_email])) == 2
