from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.optimized_block import OptimizedBlock
from app.models.optimization_run import OptimizationRun
from app.schemas.optimized_block import OptimizedBlockResponse


router = APIRouter(
    prefix="/api/optimized-blocks",
    tags=["Optimized Blocks"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/",
    response_model=list[OptimizedBlockResponse]
)
def get_optimized_blocks(
    db: Session = Depends(get_db)
):
    """
    Return optimized blocks from the latest completed
    optimization run, including associated block request IDs.
    """

    latest_run = (
        db.query(OptimizationRun)
        .filter(
            OptimizationRun.status == "Completed"
        )
        .order_by(
            OptimizationRun.optimization_run_id.desc()
        )
        .first()
    )

    if latest_run is None:
        return []

    blocks = (
        db.query(OptimizedBlock)
        .filter(
            OptimizedBlock.optimization_run_id
            == latest_run.optimization_run_id
        )
        .order_by(
            OptimizedBlock.block_date,
            OptimizedBlock.start_time
        )
        .all()
    )

    response = []

    for block in blocks:
        response.append(
            OptimizedBlockResponse(
                optimized_block_id=block.optimized_block_id,
                corridor_id=block.corridor_id,
                block_date=block.block_date,
                start_time=block.start_time,
                end_time=block.end_time,
                duration_hours=block.duration_hours,
                department_count=block.department_count,
                optimization_score=block.optimization_score,
                status=block.status,
                block_request_ids=[
                    request.block_request_id
                    for request in block.block_requests
                ],
            )
        )

    return response


@router.get(
    "/{optimized_block_id}",
    response_model=OptimizedBlockResponse
)
def get_optimized_block(
    optimized_block_id: str,
    db: Session = Depends(get_db)
):
    """
    Return details of a specific optimized block,
    including all associated block request IDs.
    """

    block = (
        db.query(OptimizedBlock)
        .filter(
            OptimizedBlock.optimized_block_id
            == optimized_block_id
        )
        .first()
    )

    if block is None:
        raise HTTPException(
            status_code=404,
            detail=f"Optimized block '{optimized_block_id}' not found"
        )

    return OptimizedBlockResponse(
        optimized_block_id=block.optimized_block_id,
        corridor_id=block.corridor_id,
        block_date=block.block_date,
        start_time=block.start_time,
        end_time=block.end_time,
        duration_hours=block.duration_hours,
        department_count=block.department_count,
        optimization_score=block.optimization_score,
        status=block.status,
        block_request_ids=[
            request.block_request_id
            for request in block.block_requests
        ],
    )