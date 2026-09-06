"""Application-specific exceptions."""


class ReportFlowError(Exception):
    """Base exception for expected ReportFlow failures."""


class DataLoadError(ReportFlowError):
    """Raised when an input file cannot be loaded."""


class DataValidationError(ReportFlowError):
    """Raised when business data does not meet the input contract."""
