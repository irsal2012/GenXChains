# Core module: exceptions, base classes, interfaces
from app.core.exceptions import (
    GenXChainsException,
    EntityNotFoundException,
    BusinessRuleViolationException,
    DuplicateEntityException,
    InvalidStateTransitionException,
    InsufficientPermissionsException,
    AuthenticationException,
    ForecastGenerationException,
    InsufficientDataException,
    to_http_exception,
)

__all__ = [
    "GenXChainsException",
    "EntityNotFoundException",
    "BusinessRuleViolationException",
    "DuplicateEntityException",
    "InvalidStateTransitionException",
    "InsufficientPermissionsException",
    "AuthenticationException",
    "ForecastGenerationException",
    "InsufficientDataException",
    "to_http_exception",
]
