from app.database.database import SessionLocal
from app.models.optimized_block import OptimizedBlock


class OptimizedBlockDetailService:

    def __init__(self):
        self.db = SessionLocal()

    def get_block_detail(self, optimized_block_id: str):
        return (
            self.db.query(OptimizedBlock)
            .filter(
                OptimizedBlock.optimized_block_id
                == optimized_block_id
            )
            .first()
        )
    def get_all_blocks(self):
        return (
            self.db.query(OptimizedBlock)
            .order_by(
                OptimizedBlock.block_date,
                OptimizedBlock.start_time,
            )
            .all()
        )


    def close(self):
        self.db.close()