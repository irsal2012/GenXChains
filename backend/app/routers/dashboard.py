"""
Dashboard Router — Thin Controller (SRP / DIP)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardService(db)


@router.get("/summary")
def dashboard_summary(
    service: DashboardService = Depends(get_dashboard_service),
    _: User = Depends(get_current_user),
):
    return service.get_summary()


@router.get("/alerts")
def dashboard_alerts(
    service: DashboardService = Depends(get_dashboard_service),
    _: User = Depends(get_current_user),
):
    return service.get_alerts()


@router.get("/kpi-overview")
def kpi_overview(
    service: DashboardService = Depends(get_dashboard_service),
    _: User = Depends(get_current_user),
):
    return service.get_kpi_overview()


@router.get("/sop-status")
def sop_status(
    service: DashboardService = Depends(get_dashboard_service),
    _: User = Depends(get_current_user),
):
    return service.get_sop_status()
