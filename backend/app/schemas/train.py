from datetime import date, time

from pydantic import BaseModel


class TrainResponse(BaseModel):
    train_id: str
    corridor_id: str
    train_number: str
    train_type: str
    date: date
    start_time: time
    end_time: time