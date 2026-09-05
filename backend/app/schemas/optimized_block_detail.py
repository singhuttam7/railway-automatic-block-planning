from datetime import date, time
from pydantic import BaseModel


class OptimizedBlockRequestDetail(BaseModel):
    block_request_id: str
    task_id: str
    corridor_id: str
    location_km: float
    requested_date: date
    start_time: time
    end_time: time
    duration_hours: float
    reason: str
    status: str


class OptimizedBlockDetailResponse(BaseModel):
    optimized_block_id: str
    optimization_run_id: int
    corridor_id: str
    block_date: date
    start_time: time
    end_time: time
    duration_hours: float
    department_count: int
    optimization_score: float
    status: str
    block_requests: list[OptimizedBlockRequestDetail]