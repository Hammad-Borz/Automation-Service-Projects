"""Central email processing pipeline."""

import logging

from .automation_rules import RuleEngine
from .classifier import EmailClassifier
from .models import EmailMessage, ProcessingResult
from .prioritizer import EmailPrioritizer
from .response_generator import ResponseGenerator


class EmailWorkflow:
    """Validate, enrich, automate, and record one email at a time."""

    def __init__(self, classifier: EmailClassifier | None = None, prioritizer: EmailPrioritizer | None = None,
                 rule_engine: RuleEngine | None = None, response_generator: ResponseGenerator | None = None,
                 logger: logging.Logger | None = None) -> None:
        self.classifier = classifier or EmailClassifier()
        self.prioritizer = prioritizer or EmailPrioritizer()
        self.rule_engine = rule_engine or RuleEngine()
        self.response_generator = response_generator
        self.logger = logger or logging.getLogger("mailflow.workflow")

    def process(self, email: EmailMessage) -> ProcessingResult:
        category = self.classifier.classify(email)
        priority = self.prioritizer.prioritize(email, category)
        actions = self.rule_engine.apply(email, category, priority)
        should_draft = any(action.action == "generate_response" for action in actions)
        response = self.response_generator.generate(email, category, priority) if should_draft and self.response_generator else None
        result = ProcessingResult(message_id=email.message_id, category=category, priority=priority,
                                  actions=actions, suggested_response=response,
                                  metadata={"sender": email.sender, "subject": email.subject})
        self.logger.info("Processed email %s as %s/%s", email.message_id, category.value, priority.value)
        return result

    def process_many(self, emails: list[EmailMessage]) -> list[ProcessingResult]:
        return [self.process(email) for email in emails]
