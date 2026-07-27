"""Time helpers.

`datetime.utcnow()` is deprecated from Python 3.12 and slated for removal. The
obvious replacement, `datetime.now(timezone.utc)`, is NOT a drop-in: it returns
an aware datetime, while every DateTime column in this schema is naive and the
JWT/serialization code paths assume naive UTC. Mixing the two raises
"can't compare offset-naive and offset-aware datetimes" at runtime.

`utc_now()` is exactly equivalent to the old `datetime.utcnow()` — current UTC,
no tzinfo — without the deprecation. Use `utc_now_aware()` only where an
explicit offset is genuinely wanted.
"""
from datetime import datetime, timezone

__all__ = ["utc_now", "utc_now_aware"]


def utc_now() -> datetime:
    """Current UTC time as a naive datetime (tzinfo=None)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def utc_now_aware() -> datetime:
    """Current UTC time as a timezone-aware datetime."""
    return datetime.now(timezone.utc)
