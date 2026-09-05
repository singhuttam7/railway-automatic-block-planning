from app.database.database import SessionLocal
from app.models.goods_forecast import GoodsForecast


class GoodsForecastService:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_forecasts(self):
        return (
            self.db.query(GoodsForecast)
            .order_by(
                GoodsForecast.date,
                GoodsForecast.start_time
            )
            .all()
        )

    def get_forecast_by_id(self, forecast_id: str):
        return (
            self.db.query(GoodsForecast)
            .filter(
                GoodsForecast.forecast_id == forecast_id
            )
            .first()
        )

    def get_forecasts_by_corridor(self, corridor_id: str):
        return (
            self.db.query(GoodsForecast)
            .filter(
                GoodsForecast.corridor_id == corridor_id
            )
            .order_by(
                GoodsForecast.date,
                GoodsForecast.start_time
            )
            .all()
        )

    def close(self):
        self.db.close()