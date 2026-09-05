from fastapi import APIRouter, Depends, HTTPException

from app.schemas.optimized_block_detail import (
    OptimizedBlockDetailResponse,
    OptimizedBlockRequestDetail,
)
from app.services.optimized_block_detail_service import (
    OptimizedBlockDetailService,
)


router = APIRouter(
    prefix="/api/optimized-block-details",
    tags=["Optimized Block Details"],
)


def get_optimized_block_detail_service():
    service = OptimizedBlockDetailService()

    try:
        yield service
    finally:
        service.close()


@router.get(
    "/{optimized_block_id}",
    response_model=OptimizedBlockDetailResponse,
)
def get_optimized_block_detail(
    optimized_block_id: str,
    service: OptimizedBlockDetailService = Depends(
        get_optimized_block_detail_service
    ),
):
    """Return an optimized block with all coordinated block requests."""

    block = service.get_block_detail(optimized_block_id)

    if block is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Optimized block "
                f"'{optimized_block_id}' not found"
            ),
        )

    block_requests = [
        OptimizedBlockRequestDetail(
            block_request_id=request.block_request_id,
            task_id=request.task_id,
            corridor_id=request.corridor_id,
            location_km=request.location_km,
            requested_date=request.requested_date,
            start_time=request.start_time,
            end_time=request.end_time,
            duration_hours=request.duration_hours,
            reason=request.reason,
            status=request.status,
        )
        for request in block.block_requests
    ]

    return OptimizedBlockDetailResponse(
        optimized_block_id=block.optimized_block_id,
        optimization_run_id=block.optimization_run_id,
        corridor_id=block.corridor_id,
        block_date=block.block_date,
        start_time=block.start_time,
        end_time=block.end_time,
        duration_hours=block.duration_hours,
        department_count=block.department_count,
        optimization_score=block.optimization_score,
        status=block.status,
        block_requests=block_requests,
    )

@router.get("/")
def get_all_optimized_blocks(
    service: OptimizedBlockDetailService = Depends(
        get_optimized_block_detail_service
    ),
):
    """Return all optimized blocks."""
    blocks = service.get_all_blocks()

    return [
        {
            "optimized_block_id": block.optimized_block_id,
            "corridor_id": block.corridor_id,
            "block_date": block.block_date,
            "start_time": block.start_time,
            "end_time": block.end_time,
            "duration_hours": block.duration_hours,
            "department_count": block.department_count,
            "optimization_score": block.optimization_score,
            "status": block.status,
        }
        for block in blocks
    ]