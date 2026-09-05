from fastapi import APIRouter, Depends

from app.schemas.dashboard import DashboardSummaryResponse
from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


def get_dashboard_service():
    service = DashboardService()

    try:
        yield service
    finally:
        service.close()


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse
)
def get_dashboard_summary(
    service: DashboardService = Depends(get_dashboard_service),
):
    """
    Return summary statistics for the latest completed
    optimization run.
    """
    return service.get_summary()

@router.get("/department-coordination")
def get_department_coordination(
    service: DashboardService = Depends(get_dashboard_service),
):
    return service.get_department_coordination()