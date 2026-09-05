from app.database.database import SessionLocal
from app.models.optimization_run import OptimizationRun


class OptimizationRunService:

    def __init__(self):
        self.db = SessionLocal()

    def get_all_runs(self):
        return (
            self.db.query(OptimizationRun)
            .order_by(
                OptimizationRun.optimization_run_id.desc()
            )
            .all()
        )

    def get_run_by_id(self, optimization_run_id: int):
        return (
            self.db.query(OptimizationRun)
            .filter(
                OptimizationRun.optimization_run_id
                == optimization_run_id
            )
            .first()
        )

    def get_latest_completed_run(self):
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

    def close(self):
        self.db.close()