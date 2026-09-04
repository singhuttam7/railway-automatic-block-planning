from datetime import date, time

from pydantic import BaseModel


class PlanningBlockResponse(BaseModel):
    optimized_block_id: str
    corridor_id: str
    start_time: time
    end_time: time
    duration_hours: float
    department_count: int
    optimization_score: float
    status: str
    block_request_ids: list[str]


class DailyPlanResponse(BaseModel):
    block_date: date
    total_blocks: int
    blocks: list[PlanningBlockResponse]


class PlanningResponse(BaseModel):
    optimization_run_id: int
    total_dates: int
    total_blocks: int
    dates: list[DailyPlanResponse]

class MonthlyPlanResponse(BaseModel):
    optimization_run_id: int
    month: str
    total_dates: int
    total_blocks: int
    dates: list[DailyPlanResponse]

