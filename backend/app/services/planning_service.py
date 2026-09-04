from collections import defaultdict
from datetime import date

from app.database.database import SessionLocal
from app.models.optimized_block import OptimizedBlock
from app.models.optimization_run import OptimizationRun


class PlanningService:

    def __init__(self):
        self.db = SessionLocal()

    def get_latest_completed_run(self):
        """
        Return the latest completed optimization run.
        """

        return (
            self.db.query(OptimizationRun)
            .filter(
                OptimizationRun.status == "Completed"
            )
            .order_by(
                OptimizationRun.optimization_run_id.desc()
            )
            .first()
        )

    def get_blocks_for_run(self, optimization_run_id):
        """
        Return all optimized blocks belonging to
        the specified optimization run.
        """

        return (
            self.db.query(OptimizedBlock)
            .filter(
                OptimizedBlock.optimization_run_id
                == optimization_run_id
            )
            .order_by(
                OptimizedBlock.block_date,
                OptimizedBlock.start_time
            )
            .all()
        )

    def get_blocks_grouped_by_date(self):
        """
        Return optimized blocks from the latest completed
        optimization run grouped by block date.
        """

        latest_run = self.get_latest_completed_run()

        if latest_run is None:
            return {
                "optimization_run_id": None,
                "dates": {}
            }

        blocks = self.get_blocks_for_run(
            latest_run.optimization_run_id
        )

        grouped_blocks = defaultdict(list)

        for block in blocks:
            grouped_blocks[block.block_date].append(
                block
            )

        return {
            "optimization_run_id": latest_run.optimization_run_id,
            "dates": dict(grouped_blocks)
        }

    def close(self):
        """
        Close the database session.
        """

        self.db.close()