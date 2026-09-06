from src.automation_rules import RuleEngine
from src.models import EmailCategory, Priority


def test_high_priority_gets_flag_and_notification(sample_email) -> None:
    actions = RuleEngine().apply(sample_email, EmailCategory.URGENT, Priority.HIGH)
    names = {action.action for action in actions}
    assert {"mark_processed", "flag_high_priority", "generate_response", "prepare_notification"} <= names


def test_matching_rule_can_filter_sender(sample_email) -> None:
    from src.models import AutomationRule
    engine = RuleEngine([AutomationRule(name="vendor", sender_contains="vendor", actions=["mark_processed"])])
    assert engine.apply(sample_email, EmailCategory.GENERAL, Priority.LOW) == []
