from datetime import date

from pydantic import BaseModel


class MaintenanceTaskResponse(BaseModel):
    task_id: str
    asset_id: str
    task_type: str
    priority: int
    priority_score: float | None
    priority_level: str | None
    due_date: date
    estimated_duration_hours: float
    status: str