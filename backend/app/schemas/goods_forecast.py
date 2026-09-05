from datetime import date, time

from pydantic import BaseModel


class GoodsForecastResponse(BaseModel):
    forecast_id: str
    corridor_id: str
    date: date
    start_time: time
    end_time: time
    expected_goods_trains: int