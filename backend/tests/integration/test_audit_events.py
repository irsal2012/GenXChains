"""
Integration Tests — Audit / Domain Event Correctness

Regression coverage for defects where audit records were written with wrong or
missing data:
- status transitions recorded `old_status == new_status`
- audit writes were silently dropped when a payload contained a Decimal
"""
import pytest
from decimal import Decimal
from fastapi.testclient import TestClient

from app.utils.events import (
    AuditLogHandler,
    DomainEvent,
    EventHandler,
    PlanStatusChangedEvent,
    get_event_bus,
)


class CapturingHandler(EventHandler):
    """Test observer that records every event published on the bus."""

    def __init__(self):
        self.events: list[DomainEvent] = []

    def handle(self, event: DomainEvent) -> None:
        self.events.append(event)


@pytest.fixture
def captured_events():
    handler = CapturingHandler()
    bus = get_event_bus()
    bus.subscribe(handler)
    try:
        yield handler.events
    finally:
        bus.unsubscribe(handler)


def _status_changes(events, entity_type: str) -> list[PlanStatusChangedEvent]:
    return [
        e for e in events
        if isinstance(e, PlanStatusChangedEvent) and e.entity_type == entity_type
    ]


class TestStatusTransitionAudit:

    def test_supply_plan_submit_records_previous_status(
        self, client: TestClient, admin_headers, supply_plan, captured_events
    ):
        resp = client.post(
            f"/api/v1/supply/plans/{supply_plan.id}/submit", headers=admin_headers
        )
        assert resp.status_code == 200

        changes = _status_changes(captured_events, "supply_plan")
        assert len(changes) == 1
        assert changes[0].old_status == "draft"
        assert changes[0].new_status == "submitted"

    def test_supply_plan_approve_records_submitted_as_previous_status(
        self, client: TestClient, admin_headers, supply_plan, captured_events
    ):
        client.post(f"/api/v1/supply/plans/{supply_plan.id}/submit", headers=admin_headers)
        captured_events.clear()

        resp = client.post(
            f"/api/v1/supply/plans/{supply_plan.id}/approve", headers=admin_headers
        )
        assert resp.status_code == 200

        changes = _status_changes(captured_events, "supply_plan")
        assert len(changes) == 1
        assert changes[0].old_status == "submitted"
        assert changes[0].new_status == "approved"

    def test_supply_plan_reject_returns_to_draft_with_reason(
        self, client: TestClient, admin_headers, supply_plan, captured_events
    ):
        client.post(f"/api/v1/supply/plans/{supply_plan.id}/submit", headers=admin_headers)
        captured_events.clear()

        resp = client.post(
            f"/api/v1/supply/plans/{supply_plan.id}/reject",
            headers=admin_headers,
            json={"reason": "Capacity constraints"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "draft"

        changes = _status_changes(captured_events, "supply_plan")
        assert len(changes) == 1
        assert changes[0].old_status == "submitted"
        assert changes[0].new_status == "draft"
        assert changes[0].comment == "Capacity constraints"

    def test_demand_plan_approve_records_previous_status(
        self, client: TestClient, admin_headers, demand_plan, captured_events
    ):
        client.post(f"/api/v1/demand/plans/{demand_plan.id}/submit", headers=admin_headers)
        captured_events.clear()

        resp = client.post(
            f"/api/v1/demand/plans/{demand_plan.id}/approve",
            headers=admin_headers,
            json={"comments": "Looks good"},
        )
        assert resp.status_code == 200

        changes = _status_changes(captured_events, "demand_plan")
        assert len(changes) == 1
        assert changes[0].old_status == "submitted"
        assert changes[0].new_status == "approved"

    def test_scenario_transitions_record_previous_status(
        self, client: TestClient, admin_headers, captured_events
    ):
        scenario_id = client.post(
            "/api/v1/scenarios/",
            headers=admin_headers,
            json={"name": "Audit Scenario", "scenario_type": "baseline"},
        ).json()["id"]
        captured_events.clear()

        client.post(f"/api/v1/scenarios/{scenario_id}/submit", headers=admin_headers)
        client.post(f"/api/v1/scenarios/{scenario_id}/approve", headers=admin_headers)

        changes = _status_changes(captured_events, "scenario")
        assert [(c.old_status, c.new_status) for c in changes] == [
            ("draft", "submitted"),
            ("submitted", "approved"),
        ]


class TestAuditLogSerialization:

    def test_decimal_payloads_are_serialized_not_dropped(self):
        """Audit writes must survive Decimal values — AuditLogHandler swallows
        exceptions, so a serialization failure loses the record entirely."""
        dumped = AuditLogHandler._dump({"qty": Decimal("480.00"), "status": "draft"})
        assert '"480.00"' in dumped
        assert '"draft"' in dumped

    def test_none_payload_serializes_to_null(self):
        assert AuditLogHandler._dump(None) == "null"
