from datetime import datetime
from pydantic import BaseModel


class OptimizationRunResponse(BaseModel):
    optimization_run_id: int
    run_date: datetime
    status: str