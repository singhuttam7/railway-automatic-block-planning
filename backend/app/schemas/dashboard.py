from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    optimization_run_id: int
    total_blocks: int
    total_planning_days: int
    total_block_hours: float
    multi_department_blocks: int
    average_optimization_score: float