"""
Supply Service — Service Layer (SRP / DIP)
"""
from math import ceil
from typing import Optional, List
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session

from app.repositories.supply_repository import SupplyPlanRepository
from app.repositories.demand_repository import DemandPlanRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.inventory_repository import InventoryRepository
from app.models.supply_plan import SupplyPlan
from app.schemas.supply import (
    SupplyPlanCreate, SupplyPlanUpdate, SupplyPlanListResponse, GapAnalysisItem,
)
from app.core.exceptions import EntityNotFoundException, to_http_exception
from app.utils.events import get_event_bus, EntityCreatedEvent, EntityUpdatedEvent, EntityDeletedEvent, PlanStatusChangedEvent


class SupplyService:

    def __init__(self, db: Session):
        self._repo = SupplyPlanRepository(db)
        self._demand_repo = DemandPlanRepository(db)
        self._product_repo = ProductRepository(db)
        self._inventory_repo = InventoryRepository(db)
        self._bus = get_event_bus()

    def list_plans(self, page: int = 1, page_size: int = 20, **filters) -> SupplyPlanListResponse:
        items, total = self._repo.list_paginated(page=page, page_size=page_size, **filters)
        return SupplyPlanListResponse(
            items=items, total=total, page=page, page_size=page_size,
            total_pages=ceil(total / page_size) if total else 0,
        )

    def get_plan(self, plan_id: int) -> SupplyPlan:
        plan = self._repo.get_by_id(plan_id)
        if not plan:
            raise to_http_exception(EntityNotFoundException("SupplyPlan", plan_id))
        return plan

    def create_plan(self, data: SupplyPlanCreate, created_by: int) -> SupplyPlan:
        plan = SupplyPlan(**data.model_dump(), created_by=created_by)
        result = self._repo.create(plan)
        self._bus.publish(EntityCreatedEvent(
            entity_type="supply_plan", entity_id=result.id, user_id=created_by,
        ))
        return result

    def update_plan(self, plan_id: int, data: SupplyPlanUpdate, user_id: int) -> SupplyPlan:
        plan = self.get_plan(plan_id)
        updates = data.model_dump(exclude_unset=True)
        updates["version"] = plan.version + 1
        result = self._repo.update(plan, updates)
        self._bus.publish(EntityUpdatedEvent(
            entity_type="supply_plan", entity_id=plan_id, user_id=user_id, new_values=updates,
        ))
        return result

    def _transition(
        self,
        plan_id: int,
        new_status: str,
        user_id: int,
        comment: Optional[str] = None,
        **extra_updates,
    ) -> SupplyPlan:
        """Apply a status transition and emit an accurate audit event.

        `old_status` must be captured *before* the update — `plan` is the same
        ORM instance the repository mutates, so reading it afterwards reports
        the new status and the audit trail loses the original value.
        """
        plan = self.get_plan(plan_id)
        old_status = plan.status
        result = self._repo.update(plan, {"status": new_status, **extra_updates})
        self._bus.publish(PlanStatusChangedEvent(
            entity_type="supply_plan", entity_id=plan_id, user_id=user_id,
            old_status=old_status, new_status=new_status, comment=comment,
        ))
        return result

    def submit_plan(self, plan_id: int, user_id: int) -> SupplyPlan:
        return self._transition(plan_id, "submitted", user_id)

    def approve_plan(self, plan_id: int, user_id: int) -> SupplyPlan:
        return self._transition(plan_id, "approved", user_id)

    def reject_plan(self, plan_id: int, user_id: int, reason: Optional[str] = None) -> SupplyPlan:
        """Reject a plan, returning it to draft for revision.

        Mirrors demand-plan rejection: `ck_supply_plans_status` permits only
        draft/submitted/approved, so rejection is modelled as a return to draft
        with the reason captured in the audit event.
        """
        return self._transition(plan_id, "draft", user_id, comment=reason)

    def delete_plan(self, plan_id: int, user_id: int) -> None:
        plan = self.get_plan(plan_id)
        self._repo.delete(plan)
        self._bus.publish(EntityDeletedEvent(
            entity_type="supply_plan", entity_id=plan_id, user_id=user_id,
        ))

    def gap_analysis(self, period: Optional[date] = None, product_id: Optional[int] = None) -> List[GapAnalysisItem]:
        """Demand vs Supply gap analysis for a given period."""
        target_period = period or date.today().replace(day=1)
        demand_plans = self._demand_repo.get_by_period(target_period)
        if product_id is not None:
            demand_plans = [dp for dp in demand_plans if int(dp.product_id) == int(product_id)]

        supply_plans = self._repo.get_by_period(target_period)
        if product_id is not None:
            supply_plans = [sp for sp in supply_plans if int(sp.product_id) == int(product_id)]

        supply_map = {sp.product_id: (sp.planned_prod_qty or Decimal("0")) for sp in supply_plans}
        actual_prod_map = {sp.product_id: (sp.actual_prod_qty or Decimal("0")) for sp in supply_plans}

        inventory_records = self._inventory_repo.get_all_inventory()
        if product_id is not None:
            inventory_records = [inv for inv in inventory_records if int(inv.product_id) == int(product_id)]
        inventory_available_map = {}
        for inv in inventory_records:
            on_hand = inv.on_hand_qty or Decimal("0")
            allocated = inv.allocated_qty or Decimal("0")
            in_transit = inv.in_transit_qty or Decimal("0")
            available = on_hand - allocated + in_transit
            if available < 0:
                available = Decimal("0")
            inventory_available_map[inv.product_id] = inventory_available_map.get(inv.product_id, Decimal("0")) + available

        result = []
        for dp in demand_plans:
            product = self._product_repo.get_by_id(dp.product_id)
            demand = dp.consensus_qty or dp.adjusted_qty or dp.forecast_qty
            planned_supply = supply_map.get(dp.product_id, Decimal("0"))
            actual_production = actual_prod_map.get(dp.product_id, Decimal("0"))
            inventory_available = inventory_available_map.get(dp.product_id, Decimal("0"))
            effective_supply = planned_supply + inventory_available
            additional_prod_required = max(demand - inventory_available, Decimal("0"))

            # Plan alignment gap: production plan vs consensus demand.
            plan_gap = planned_supply - demand
            plan_gap_pct = float(plan_gap / demand * 100) if demand else 0.0

            # Execution alignment gap: realized production vs consensus demand.
            actual_gap = actual_production - demand
            actual_gap_pct = float(actual_gap / demand * 100) if demand else 0.0

            # Coverage gap: production + inventory vs consensus demand.
            coverage_gap = effective_supply - demand
            coverage_gap_pct = float(coverage_gap / demand * 100) if demand else 0.0

            # Backward-compatible aliases retained for existing consumers.
            gap = coverage_gap
            gap_pct = coverage_gap_pct

            status = "balanced"
            if gap_pct < -20:
                status = "critical"
            elif gap_pct < 0:
                status = "shortage"
            elif gap_pct > 20:
                status = "excess"

            result.append(GapAnalysisItem(
                product_id=dp.product_id,
                product_name=product.name if product else "Unknown",
                sku=product.sku if product else "N/A",
                period=target_period,
                consensus_demand_qty=demand,
                demand_qty=demand,
                planned_production_qty=planned_supply,
                actual_production_qty=actual_production,
                planned_supply_qty=planned_supply,
                inventory_available_qty=inventory_available,
                effective_supply_qty=effective_supply,
                additional_prod_required_qty=additional_prod_required,
                plan_gap_qty=plan_gap,
                plan_gap_pct=plan_gap_pct,
                actual_gap_qty=actual_gap,
                actual_gap_pct=actual_gap_pct,
                coverage_gap_qty=coverage_gap,
                coverage_gap_pct=coverage_gap_pct,
                supply_qty=effective_supply,
                gap=gap,
                gap_pct=gap_pct,
                status=status,
            ))
        return result
