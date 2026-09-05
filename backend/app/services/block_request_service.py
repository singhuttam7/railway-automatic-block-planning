from app.database.database import SessionLocal
from app.models.block_request import BlockRequest


class BlockRequestService:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_requests(self):
        return (
            self.db.query(BlockRequest)
            .order_by(
                BlockRequest.requested_date,
                BlockRequest.start_time
            )
            .all()
        )

    def get_request_by_id(self, block_request_id: str):
        return (
            self.db.query(BlockRequest)
            .filter(
                BlockRequest.block_request_id == block_request_id
            )
            .first()
        )

    def get_requests_by_corridor(self, corridor_id: str):
        return (
            self.db.query(BlockRequest)
            .filter(
                BlockRequest.corridor_id == corridor_id
            )
            .order_by(
                BlockRequest.requested_date,
                BlockRequest.start_time
            )
            .all()
        )

    def close(self):
        self.db.close()