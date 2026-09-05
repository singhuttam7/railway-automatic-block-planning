from pydantic import BaseModel


class CorridorResponse(BaseModel):
    corridor_id: str
    corridor_name: str
    start_km: float
    end_km: float