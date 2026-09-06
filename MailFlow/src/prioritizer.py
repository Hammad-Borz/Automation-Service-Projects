"""Email priority scoring."""

from .models import EmailCategory, EmailMessage, Priority


class EmailPrioritizer:
    """Assign priority using category, sender, and text signals."""

    HIGH_TERMS = ("urgent", "asap", "critical", "outage", "immediately")
    MEDIUM_TERMS = ("invoice", "quote", "support", "issue", "demo")

    def prioritize(self, email: EmailMessage, category: EmailCategory) -> Priority:
        text = f"{email.subject} {email.body}".lower()
        if category == EmailCategory.URGENT or any(term in text for term in self.HIGH_TERMS):
            return Priority.HIGH
        if category == EmailCategory.NEWSLETTER and "noreply" in email.sender.lower():
            return Priority.LOW
        if category in {EmailCategory.SUPPORT, EmailCategory.INVOICE, EmailCategory.SALES}:
            return Priority.MEDIUM
        if any(term in text for term in self.MEDIUM_TERMS):
            return Priority.MEDIUM
        if "@" not in email.sender or "noreply" in email.sender.lower():
            return Priority.LOW
        return Priority.MEDIUM if category == EmailCategory.GENERAL else Priority.LOW
