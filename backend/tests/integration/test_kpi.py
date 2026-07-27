"""
Integration Tests — KPI Endpoints

Tests:
- GET/POST/PUT /api/v1/kpi/metrics
- KPI summary
- KPI alerts
- KPI targets
"""
import pytest
from fastapi.testclient import TestClient


class TestKPIMetricCRUD:

    def test_create_kpi_metric(self, client: TestClient, admin_headers):
        resp = client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
            "metric_name": "Forecast Accuracy",
            "metric_category": "forecast_accuracy",
            "period": "2026-03-01",
            "value": 87.5,
            "target": 90.0,
            "unit": "percent",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["metric_name"] == "Forecast Accuracy"
        assert float(data["value"]) == 87.5
        assert "id" in data

    def test_list_kpi_metrics(self, client: TestClient, admin_headers):
        client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
            "metric_name": "OTIF",
            "metric_category": "otif",
            "period": "2026-03-01",
            "value": 95.0,
            "target": 98.0,
            "unit": "percent",
        })
        resp = client.get("/api/v1/kpi/metrics", headers=admin_headers)
        assert resp.status_code == 200
        data = resp.json()
        items = data.get("items", data) if isinstance(data, dict) else data
        assert len(items) >= 1

    def test_get_kpi_metric_by_id(self, client: TestClient, admin_headers):
        create_resp = client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
            "metric_name": "Inventory Turns",
            "metric_category": "inventory_turns",
            "period": "2026-03-01",
            "value": 6.2,
            "target": 8.0,
            "unit": "turns",
        })
        kpi_id = create_resp.json()["id"]
        resp = client.get(f"/api/v1/kpi/metrics/{kpi_id}", headers=admin_headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == kpi_id

    def test_get_nonexistent_kpi_returns_404(self, client: TestClient, admin_headers):
        resp = client.get("/api/v1/kpi/metrics/99999", headers=admin_headers)
        assert resp.status_code == 404

    def test_update_kpi_metric(self, client: TestClient, admin_headers):
        create_resp = client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
            "metric_name": "Service Level",
            "metric_category": "service_level",
            "period": "2026-03-01",
            "value": 92.0,
            "target": 95.0,
            "unit": "percent",
        })
        kpi_id = create_resp.json()["id"]
        resp = client.put(f"/api/v1/kpi/metrics/{kpi_id}", headers=admin_headers, json={
            "value": 93.5,
        })
        assert resp.status_code == 200
        assert float(resp.json()["value"]) == 93.5

    def test_list_kpi_unauthenticated_returns_401(self, client: TestClient):
        resp = client.get("/api/v1/kpi/metrics")
        assert resp.status_code == 401


class TestKPISummary:

    def test_kpi_summary_endpoint(self, client: TestClient, admin_headers):
        resp = client.get("/api/v1/kpi/summary", headers=admin_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, (list, dict))

    def test_kpi_alerts_endpoint(self, client: TestClient, admin_headers):
        # Create a KPI below target to trigger alert
        client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
            "metric_name": "Low Forecast Accuracy",
            "metric_category": "forecast_accuracy",
            "period": "2026-03-01",
            "value": 60.0,  # well below target
            "target": 90.0,
            "unit": "percent",
        })
        resp = client.get("/api/v1/kpi/alerts", headers=admin_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, (list, dict))


class TestKPIFilters:

    def test_filter_by_category(self, client: TestClient, admin_headers):
        client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
            "metric_name": "OTIF Q1",
            "metric_category": "otif",
            "period": "2026-01-01",
            "value": 94.0,
            "target": 98.0,
            "unit": "percent",
        })
        resp = client.get("/api/v1/kpi/metrics?category=otif", headers=admin_headers)
        assert resp.status_code == 200
        data = resp.json()
        items = data.get("items", data) if isinstance(data, dict) else data
        for item in items:
            assert item["metric_category"] == "otif"

    def test_filter_by_period(self, client: TestClient, admin_headers):
        client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
            "metric_name": "March KPI",
            "metric_category": "forecast_accuracy",
            "period": "2026-03-01",
            "value": 88.0,
            "target": 90.0,
            "unit": "percent",
        })
        resp = client.get(
            "/api/v1/kpi/metrics?period_from=2026-03-01&period_to=2026-03-31",
            headers=admin_headers,
        )
        assert resp.status_code == 200


class TestKPITrends:

    def test_trends_returns_series_per_metric_oldest_first(self, client: TestClient, admin_headers):
        for period, value in [("2026-01-01", 90.0), ("2026-03-01", 94.0), ("2026-02-01", 92.0)]:
            client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
                "metric_name": "OTIF",
                "metric_category": "service",
                "period": period,
                "value": value,
                "target": 98.0,
                "unit": "percent",
            })

        resp = client.get("/api/v1/kpi/trends", headers=admin_headers)
        assert resp.status_code == 200
        series = {s["metric_name"]: s for s in resp.json()}
        assert "OTIF" in series

        points = series["OTIF"]["points"]
        assert [p["period"] for p in points] == ["2026-01-01", "2026-02-01", "2026-03-01"]
        assert [p["value"] for p in points] == [90.0, 92.0, 94.0]

    def test_trends_filtered_by_category(self, client: TestClient, admin_headers):
        client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
            "metric_name": "Inventory Turns", "metric_category": "inventory",
            "period": "2026-03-01", "value": 6.0, "unit": "turns",
        })
        client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
            "metric_name": "OTIF", "metric_category": "service",
            "period": "2026-03-01", "value": 95.0, "unit": "percent",
        })

        resp = client.get("/api/v1/kpi/trends?category=inventory", headers=admin_headers)
        assert resp.status_code == 200
        names = {s["metric_name"] for s in resp.json()}
        assert names == {"Inventory Turns"}


class TestKPISummaryRollup:

    def test_summary_counts_on_and_off_target(self, client: TestClient, admin_headers):
        client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
            "metric_name": "On Target KPI", "metric_category": "service",
            "period": "2026-03-01", "value": 99.0, "target": 98.0,
        })
        client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
            "metric_name": "Off Target KPI", "metric_category": "service",
            "period": "2026-03-01", "value": 50.0, "target": 98.0,
        })

        data = client.get("/api/v1/kpi/summary", headers=admin_headers).json()
        assert data["total_metrics"] == 2
        assert data["on_target_count"] == 1
        assert data["off_target_count"] == 1
        assert data["on_target_pct"] == 50.0
        # 50 vs a target of 98 is >20% adrift → a critical alert.
        assert data["critical_alert_count"] >= 1


class TestKPIMetricHistory:

    def test_history_by_name_returns_all_readings(self, client: TestClient, admin_headers):
        for period in ("2026-01-01", "2026-02-01", "2026-03-01"):
            client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
                "metric_name": "OTIF", "metric_category": "service",
                "period": period, "value": 90.0, "target": 98.0,
            })
        client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
            "metric_name": "Other", "metric_category": "service",
            "period": "2026-03-01", "value": 50.0,
        })

        resp = client.get("/api/v1/kpi/metrics/by-name/OTIF", headers=admin_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 3
        assert {d["metric_name"] for d in data} == {"OTIF"}

    def test_history_route_does_not_shadow_lookup_by_id(self, client: TestClient, admin_headers):
        created = client.post("/api/v1/kpi/metrics", headers=admin_headers, json={
            "metric_name": "Fill Rate", "metric_category": "service",
            "period": "2026-03-01", "value": 97.0,
        }).json()

        by_id = client.get(f"/api/v1/kpi/metrics/{created['id']}", headers=admin_headers)
        assert by_id.status_code == 200
        assert by_id.json()["id"] == created["id"]

    def test_history_for_unknown_name_is_empty_not_404(self, client: TestClient, admin_headers):
        resp = client.get("/api/v1/kpi/metrics/by-name/Nonexistent", headers=admin_headers)
        assert resp.status_code == 200
        assert resp.json() == []
