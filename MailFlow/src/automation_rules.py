"""Configurable automation rule evaluation and action execution."""

from .models import ActionResult, AutomationRule, EmailCategory, EmailMessage, Priority


_PRIORITY_RANK = {Priority.LOW: 1, Priority.MEDIUM: 2, Priority.HIGH: 3}


class RuleEngine:
    """Evaluate rules and return safe, non-delivery action results."""

    def __init__(self, rules: list[AutomationRule] | None = None) -> None:
        self.rules = rules or self.default_rules()

    @staticmethod
    def default_rules() -> list[AutomationRule]:
        return [
            AutomationRule(name="process-all", actions=["mark_processed"]),
            AutomationRule(name="flag-high-priority", minimum_priority=Priority.HIGH, actions=["flag_high_priority"]),
            AutomationRule(name="draft-customer-response", categories={EmailCategory.SUPPORT, EmailCategory.SALES, EmailCategory.URGENT}, actions=["generate_response"]),
            AutomationRule(name="prepare-notification", minimum_priority=Priority.HIGH, actions=["prepare_notification"]),
        ]

    def matching_rules(self, email: EmailMessage, category: EmailCategory, priority: Priority) -> list[AutomationRule]:
        matches = []
        for rule in self.rules:
            if rule.categories and category not in rule.categories:
                continue
            if rule.minimum_priority and _PRIORITY_RANK[priority] < _PRIORITY_RANK[rule.minimum_priority]:
                continue
            if rule.sender_contains and rule.sender_contains.lower() not in email.sender.lower():
                continue
            matches.append(rule)
        return matches

    def apply(self, email: EmailMessage, category: EmailCategory, priority: Priority) -> list[ActionResult]:
        results: list[ActionResult] = []
        for rule in self.matching_rules(email, category, priority):
            for action in rule.actions:
                detail = "Demo mode: no external side effect"
                if action == "mark_processed":
                    detail = "Email marked as processed"
                elif action == "flag_high_priority":
                    detail = "High-priority email flagged for review"
                elif action == "generate_response":
                    detail = "Response draft requested"
                elif action == "prepare_notification":
                    detail = "Notification prepared, not sent"
                results.append(ActionResult(action=action, detail=detail))
        return results
