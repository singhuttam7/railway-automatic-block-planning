from fastapi import APIRouter, Depends, HTTPException

from app.schemas.optimization_run import OptimizationRunResponse
from app.services.optimization_run_service import OptimizationRunService


router = APIRouter(
    prefix="/api/optimization-runs",
    tags=["Optimization Runs"],
)


def get_optimization_run_service():
    service = OptimizationRunService()

    try:
        yield service
    finally:
        service.close()


@router.get(
    "/",
    response_model=list[OptimizationRunResponse],
)
def get_all_optimization_runs(
    service: OptimizationRunService = Depends(
        get_optimization_run_service
    ),
):
    """Return all optimization runs."""

    return service.get_all_runs()


@router.get(
    "/latest",
    response_model=OptimizationRunResponse,
)
def get_latest_optimization_run(
    service: OptimizationRunService = Depends(
        get_optimization_run_service
    ),
):
    """Return the latest completed optimization run."""

    run = service.get_latest_completed_run()

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="No completed optimization run found",
        )

    return run


@router.get(
    "/{optimization_run_id}",
    response_model=OptimizationRunResponse,
)
def get_optimization_run(
    optimization_run_id: int,
    service: OptimizationRunService = Depends(
        get_optimization_run_service
    ),
):
    """Return a specific optimization run."""

    run = service.get_run_by_id(optimization_run_id)

    if run is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Optimization run "
                f"'{optimization_run_id}' not found"
            ),
        )

    return run