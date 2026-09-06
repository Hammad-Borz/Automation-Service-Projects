"""Application-specific exceptions."""


class MailFlowError(Exception):
    """Base exception for expected MailFlow failures."""


class ConfigurationError(MailFlowError):
    """Raised when required configuration is missing or invalid."""


class EmailValidationError(MailFlowError):
    """Raised when an email cannot be processed safely."""


class EmailDeliveryError(MailFlowError):
    """Raised when an email cannot be delivered."""
