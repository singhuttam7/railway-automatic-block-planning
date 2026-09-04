from fastapi import APIRouter, Depends

from app.schemas.planning import (
    DailyPlanResponse,
    PlanningBlockResponse,
    PlanningResponse,
)

from app.schemas.planning import (
    DailyPlanResponse,
    MonthlyPlanResponse,
    PlanningBlockResponse,
    PlanningResponse,
)

from app.services.planning_service import PlanningService


router = APIRouter(
    prefix="/api/planning",
    tags=["Planning"]
)


def get_planning_service():
    service = PlanningService()
    try:
        yield service
    finally:
        service.close()


@router.get("/daily", response_model=PlanningResponse)
def get_daily_planning(
    service: PlanningService = Depends(get_planning_service),
):
    """
    Return optimized blocks grouped by planning date
    from the latest completed optimization run.
    """

    result = service.get_blocks_grouped_by_date()

    if result["optimization_run_id"] is None:
        return PlanningResponse(
            optimization_run_id=0,
            total_dates=0,
            total_blocks=0,
            dates=[]
        )

    grouped_blocks = result["dates"]

    daily_plans = []
    total_blocks = 0

    for block_date, date_blocks in grouped_blocks.items():

        planning_blocks = []

        for block in date_blocks:
            planning_blocks.append(
                PlanningBlockResponse(
                    optimized_block_id=block.optimized_block_id,
                    corridor_id=block.corridor_id,
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

        daily_plans.append(
            DailyPlanResponse(
                block_date=block_date,
                total_blocks=len(planning_blocks),
                blocks=planning_blocks,
            )
        )

        total_blocks += len(planning_blocks)

    return PlanningResponse(
        optimization_run_id=result["optimization_run_id"],
        total_dates=len(daily_plans),
        total_blocks=total_blocks,
        dates=daily_plans,
    )

@router.get("/weekly", response_model=list[PlanningResponse])
def get_weekly_planning(
    service: PlanningService = Depends(get_planning_service),
):
    """
    Return optimized blocks grouped into weekly plans.
    """

    result = service.get_blocks_grouped_by_date()

    if result["optimization_run_id"] is None:
        return []

    grouped_blocks = result["dates"]

    dates = sorted(grouped_blocks.keys())

    weekly_plans = []

    for i in range(0, len(dates), 7):
        week_dates = dates[i:i + 7]

        daily_plans = []
        total_blocks = 0

        for block_date in week_dates:
            date_blocks = grouped_blocks[block_date]

            planning_blocks = []

            for block in date_blocks:
                planning_blocks.append(
                    PlanningBlockResponse(
                        optimized_block_id=block.optimized_block_id,
                        corridor_id=block.corridor_id,
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

            daily_plans.append(
                DailyPlanResponse(
                    block_date=block_date,
                    total_blocks=len(planning_blocks),
                    blocks=planning_blocks,
                )
            )

            total_blocks += len(planning_blocks)

        weekly_plans.append(
            PlanningResponse(
                optimization_run_id=result["optimization_run_id"],
                total_dates=len(daily_plans),
                total_blocks=total_blocks,
                dates=daily_plans,
            )
        )

    return weekly_plans

@router.get("/monthly", response_model=list[MonthlyPlanResponse])
def get_monthly_planning(
    service: PlanningService = Depends(get_planning_service),
):
    """
    Return optimized blocks grouped into monthly plans.
    """
    result = service.get_blocks_grouped_by_date()

    if result["optimization_run_id"] is None:
        return []

    grouped_blocks = result["dates"]

    monthly_data = {}

    for block_date, date_blocks in grouped_blocks.items():
        month_key = block_date.strftime("%Y-%m")

        if month_key not in monthly_data:
            monthly_data[month_key] = []

        planning_blocks = []

        for block in date_blocks:
            planning_blocks.append(
                PlanningBlockResponse(
                    optimized_block_id=block.optimized_block_id,
                    corridor_id=block.corridor_id,
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

        monthly_data[month_key].append(
            DailyPlanResponse(
                block_date=block_date,
                total_blocks=len(planning_blocks),
                blocks=planning_blocks,
            )
        )

    monthly_plans = []

    for month, daily_plans in sorted(monthly_data.items()):
        monthly_plans.append(
            MonthlyPlanResponse(
                optimization_run_id=result["optimization_run_id"],
                month=month,
                total_dates=len(daily_plans),
                total_blocks=sum(
                    day.total_blocks for day in daily_plans
                ),
                dates=daily_plans,
            )
        )

    return monthly_plans