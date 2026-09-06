"""Custom exceptions for DataOps Automator."""


class DataOpsError(Exception):
    """Base exception for expected application failures."""


class DataLoadError(DataOpsError):
    """Raised when input data cannot be loaded."""


class DataValidationError(DataOpsError):
    """Raised when input data violates the business contract."""


class DatabaseError(DataOpsError):
    """Raised when database setup or operations fail."""


class ReportExportError(DataOpsError):
    """Raised when report output cannot be written."""
