from app.utils.security import get_password_hash, verify_password


def test_password_hash_round_trip() -> None:
    password = "Password123!"
    hashed = get_password_hash(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_verify_password_rejects_invalid_hash() -> None:
    assert verify_password("Password123!", "not-a-valid-bcrypt-hash") is False


class TestUtcNow:
    """utc_now() must stay a drop-in for the deprecated datetime.utcnow():
    naive UTC. An aware value here would break comparisons against the naive
    DateTime columns used throughout the schema."""

    def test_returns_naive_datetime(self):
        from app.utils.time import utc_now
        assert utc_now().tzinfo is None

    def test_tracks_current_utc(self):
        from datetime import datetime, timezone
        from app.utils.time import utc_now
        delta = abs((utc_now() - datetime.now(timezone.utc).replace(tzinfo=None)).total_seconds())
        assert delta < 5

    def test_aware_variant_carries_utc_offset(self):
        from datetime import timezone
        from app.utils.time import utc_now_aware
        assert utc_now_aware().utcoffset() == timezone.utc.utcoffset(None)
