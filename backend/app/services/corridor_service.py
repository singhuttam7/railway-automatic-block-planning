from app.database.database import SessionLocal
from app.models.corridor import Corridor


class CorridorService:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_corridors(self):
        return (
            self.db.query(Corridor)
            .order_by(Corridor.corridor_id)
            .all()
        )

    def get_corridor_by_id(self, corridor_id: str):
        return (
            self.db.query(Corridor)
            .filter(Corridor.corridor_id == corridor_id)
            .first()
        )

    def close(self):
        self.db.close()