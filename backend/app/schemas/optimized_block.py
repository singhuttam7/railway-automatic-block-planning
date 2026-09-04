from datetime import date, time

from pydantic import BaseModel


class OptimizedBlockResponse(BaseModel):
    optimized_block_id: str
    corridor_id: str
    block_date: date
    start_time: time
    end_time: time
    duration_hours: float
    department_count: int
    optimization_score: float
    status: str
    block_request_ids: list[str]