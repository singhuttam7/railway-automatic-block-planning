from datetime import date, time

from pydantic import BaseModel


class BlockRequestResponse(BaseModel):
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