"""
KPI Service — Service Layer (SRP / DIP)
"""
from typing import Optional, List
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session

from app.repositories.kpi_repository import KPIMetricRepository
from app.models.kpi_metric import KPIMetric
from app.schemas.kpi import KPIMetricCreate, KPIMetricUpdate, KPIDashboardData, KPITargetRequest
from app.core.exceptions import EntityNotFoundException, to_http_exception
from app.utils.events import get_event_bus, EntityCreatedEvent, EntityUpdatedEvent


class KPIService:

    def __init__(self, db: Session):
        self._repo = KPIMetricRepository(db)
        self._bus = get_event_bus()

    def list_metrics(
        self,
        category: Optional[str] = None,
        period_from: Optional[date] = None,
        period_to: Optional[date] = None,
    ) -> List[KPIMetric]:
        return self._repo.list_filtered(category=category, period_from=period_from, period_to=period_to)

    def get_metric(self, metric_id: int) -> KPIMetric:
        m = self._repo.get_by_id(metric_id)
        if not m:
            raise to_http_exception(EntityNotFoundException("KPIMetric", metric_id))
        return m

    @staticmethod
    def _derive(
        value: Decimal,
        target: Optional[Decimal],
        previous_value: Optional[Decimal],
    ) -> dict:
        """Derive variance/trend fields. Single source of truth for create,
        update and target-setting so the three paths cannot drift apart."""
        variance = None
        variance_pct = None
        trend = None
        if target is not None:
            variance = value - target
            variance_pct = (variance / target * 100) if target != 0 else None
        if previous_value is not None and previous_value != 0:
            change = value - previous_value
            trend = "improving" if change > 0 else ("declining" if change < 0 else "stable")
        return {"variance": variance, "variance_pct": variance_pct, "trend": trend}

    def create_metric(self, data: KPIMetricCreate, user_id: int) -> KPIMetric:
        metric = KPIMetric(
            **data.model_dump(),
            **self._derive(data.value, data.target, data.previous_value),
        )
        result = self._repo.create(metric)
        self._bus.publish(EntityCreatedEvent(
            entity_type="kpi_metric", entity_id=result.id, user_id=user_id,
        ))
        return result

    def get_metric_history(self, metric_name: str, limit: int = 12) -> List[KPIMetric]:
        """Readings for one metric, newest period first."""
        return self._repo.get_by_name(metric_name, limit=limit)

    def update_metric(self, metric_id: int, data: KPIMetricUpdate, user_id: int) -> KPIMetric:
        metric = self.get_metric(metric_id)
        updates = data.model_dump(exclude_unset=True)
        if updates:
            merged = {
                "value": updates.get("value", metric.value),
                "target": updates.get("target", metric.target),
                "previous_value": updates.get("previous_value", metric.previous_value),
            }
            updates.update(self._derive(**merged))
            metric = self._repo.update(metric, updates)
            self._bus.publish(EntityUpdatedEvent(
                entity_type="kpi_metric", entity_id=metric_id, user_id=user_id,
                new_values={k: str(v) for k, v in updates.items()},
            ))
        return metric

    def get_summary(self) -> dict:
        """Portfolio-level KPI health roll-up for the dashboard header."""
        metrics = self._repo.list_filtered()
        with_target = [m for m in metrics if m.target is not None and m.value is not None]
        on_target = sum(1 for m in with_target if m.target != 0 and m.value >= m.target)
        alerts = self.get_alerts()
        by_category: dict = {}
        for m in metrics:
            by_category.setdefault(m.metric_category, 0)
            by_category[m.metric_category] += 1
        return {
            "total_metrics": len(metrics),
            "metrics_with_target": len(with_target),
            "on_target_count": on_target,
            "off_target_count": len(with_target) - on_target,
            "on_target_pct": round(on_target / len(with_target) * 100, 2) if with_target else 0.0,
            "alert_count": len(alerts),
            "critical_alert_count": sum(1 for a in alerts if a["severity"] == "critical"),
            "by_category": by_category,
        }

    def get_trends(self, category: Optional[str] = None, months: int = 12) -> List[dict]:
        """Per-metric time series, newest period last, for trend charts."""
        metrics = self._repo.list_filtered(category=category)
        series: dict = {}
        for m in metrics:
            series.setdefault(m.metric_name, []).append(m)
        return [
            {
                "metric_name": name,
                "metric_category": points[0].metric_category,
                "unit": points[0].unit,
                "points": [
                    {
                        "period": str(p.period),
                        "value": float(p.value) if p.value is not None else None,
                        "target": float(p.target) if p.target is not None else None,
                    }
                    # list_filtered returns newest-first; charts read oldest-first.
                    for p in sorted(points[:months], key=lambda p: p.period)
                ],
            }
            for name, points in series.items()
        ]

    def get_dashboard(self) -> KPIDashboardData:
        """Return KPIs grouped by category for the dashboard."""
        return KPIDashboardData(
            demand_kpis=self._repo.get_by_category("demand"),
            supply_kpis=self._repo.get_by_category("supply"),
            inventory_kpis=self._repo.get_by_category("inventory"),
            service_kpis=self._repo.get_by_category("service"),
            financial_kpis=self._repo.get_by_category("financial"),
        )

    def get_alerts(self) -> List[dict]:
        """Return KPIs that are breaching their targets."""
        metrics = self._repo.get_with_targets()
        alerts = []
        for m in metrics:
            if m.target is None or m.value is None:
                continue
            variance_pct = float((m.value - m.target) / m.target * 100) if m.target != 0 else 0
            if abs(variance_pct) > 10:
                severity = "critical" if abs(variance_pct) > 20 else "warning"
                alerts.append({
                    "metric_name": m.metric_name,
                    "category": m.metric_category,
                    "value": float(m.value),
                    "target": float(m.target),
                    "variance_pct": round(variance_pct, 2),
                    "severity": severity,
                    "period": str(m.period),
                })
        return alerts

    def set_target(self, body: KPITargetRequest, user_id: int) -> KPIMetric:
        """Update the target for the most recent KPI metric by name."""
        metric = self._repo.get_latest_by_name(body.metric_name)
        if not metric:
            raise to_http_exception(EntityNotFoundException("KPIMetric", body.metric_name))
        return self._repo.update(metric, {
            "target": body.target,
            **self._derive(metric.value, body.target, metric.previous_value),
        })
