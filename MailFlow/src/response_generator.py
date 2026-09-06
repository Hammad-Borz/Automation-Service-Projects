"""Response generation interfaces and deterministic demo implementation."""

from abc import ABC, abstractmethod

from .models import EmailCategory, EmailMessage, Priority


class ResponseGenerator(ABC):
    """Provider interface for future LLM-backed response generation."""

    @abstractmethod
    def generate(self, email: EmailMessage, category: EmailCategory, priority: Priority) -> str:
        """Generate a draft response."""


class DemoResponseGenerator(ResponseGenerator):
    """Predictable, local response drafts suitable for demos and tests."""

    def generate(self, email: EmailMessage, category: EmailCategory, priority: Priority) -> str:
        opening = "Thanks for reaching out."
        by_category = {
            EmailCategory.SUPPORT: "Our support team will review the issue and follow up shortly.",
            EmailCategory.SALES: "Thanks for your interest. A member of our sales team will contact you with next steps.",
            EmailCategory.INVOICE: "We have received your billing message and will verify the invoice details.",
            EmailCategory.URGENT: "We have flagged this as a priority and will investigate immediately.",
        }
        return f"{opening} {by_category.get(category, 'Your message has been received and will be reviewed soon.')}"
