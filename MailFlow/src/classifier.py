"""Replaceable rule-based email classifier."""

import re
from collections.abc import Mapping

from .models import EmailCategory, EmailMessage


class EmailClassifier:
    """Classify messages using transparent weighted keyword rules."""

    KEYWORDS: Mapping[EmailCategory, tuple[str, ...]] = {
        EmailCategory.URGENT: ("urgent", "asap", "outage", "critical", "immediately"),
        EmailCategory.SUPPORT: ("support", "bug", "issue", "not working", "help"),
        EmailCategory.SALES: ("quote", "pricing", "demo", "proposal", "purchase"),
        EmailCategory.NEWSLETTER: ("newsletter", "unsubscribe", "weekly digest", "campaign"),
        EmailCategory.INVOICE: ("invoice", "billing", "payment due", "receipt", "statement"),
    }

    def classify(self, email: EmailMessage) -> EmailCategory:
        text = f"{email.subject} {email.body}".lower()
        scores = {category: sum(len(re.findall(re.escape(word), text)) for word in words)
                  for category, words in self.KEYWORDS.items()}
        best_category, best_score = max(scores.items(), key=lambda item: item[1])
        return best_category if best_score else EmailCategory.GENERAL
