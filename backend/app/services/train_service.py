from app.database.database import SessionLocal
from app.models.train import Train


class TrainService:

    def __init__(self):
        self.db = SessionLocal()

    def get_all_trains(self):
        return (
            self.db.query(Train)
            .order_by(
                Train.date,
                Train.start_time
            )
            .all()
        )

    def get_train_by_id(self, train_id: str):
        return (
            self.db.query(Train)
            .filter(
                Train.train_id == train_id
            )
            .first()
        )

    def get_trains_by_corridor(self, corridor_id: str):
        return (
            self.db.query(Train)
            .filter(
                Train.corridor_id == corridor_id
            )
            .order_by(
                Train.date,
                Train.start_time
            )
            .all()
        )

    def close(self):
        self.db.close()