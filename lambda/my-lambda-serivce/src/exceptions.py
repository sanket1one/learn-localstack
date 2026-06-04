class DomainError(Exception):
    """Base class for all domain-related errors."""
    pass

class ValidationError(DomainError):
    """Raised when input payload fails validation."""
    pass

class PersistenceError(DomainError):
    """Raised when there is a persistence / DB error."""
    pass