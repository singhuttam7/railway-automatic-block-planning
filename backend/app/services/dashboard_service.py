from app.database.database import SessionLocal
from app.models.optimized_block import OptimizedBlock
from app.models.optimization_run import OptimizationRun


class DashboardService:
    def __init__(self):
        self.db = SessionLocal()

    def get_latest_completed_run(self):
        return (
            self.db.query(OptimizationRun)
            .filter(OptimizationRun.status == "Completed")
            .order_by(OptimizationRun.optimization_run_id.desc())
            .first()
        )

    def get_summary(self):
        latest_run = self.get_latest_completed_run()

        if latest_run is None:
            return {
                "optimization_run_id": 0,
                "total_blocks": 0,
                "total_planning_days": 0,
                "total_block_hours": 0.0,
                "multi_department_blocks": 0,
                "average_optimization_score": 0.0,
            }

        blocks = (
            self.db.query(OptimizedBlock)
            .filter(
                OptimizedBlock.optimization_run_id
                == latest_run.optimization_run_id
            )
            .all()
        )

        if not blocks:
            return {
                "optimization_run_id": latest_run.optimization_run_id,
                "total_blocks": 0,
                "total_planning_days": 0,
                "total_block_hours": 0.0,
                "multi_department_blocks": 0,
                "average_optimization_score": 0.0,
            }

        total_blocks = len(blocks)

        total_planning_days = len(
            {block.block_date for block in blocks}
        )

        total_block_hours = sum(
            block.duration_hours for block in blocks
        )

        multi_department_blocks = sum(
            1 for block in blocks
            if block.department_count > 1
        )

        average_optimization_score = (
            sum(block.optimization_score for block in blocks)
            / total_blocks
        )

        return {
            "optimization_run_id": latest_run.optimization_run_id,
            "total_blocks": total_blocks,
            "total_planning_days": total_planning_days,
            "total_block_hours": round(total_block_hours, 2),
            "multi_department_blocks": multi_department_blocks,
            "average_optimization_score": round(
                average_optimization_score, 2
            ),
        }


    def get_department_coordination(self):
        latest_run = self.get_latest_completed_run()

        if latest_run is None:
            return {
                "ENG": 0,
                "SNT": 0,
                "TRD": 0,
            }

        blocks = (
            self.db.query(OptimizedBlock)
            .filter(
                OptimizedBlock.optimization_run_id
                == latest_run.optimization_run_id
            )
            .all()
        )

        department_counts = {
            "ENG": 0,
            "SNT": 0,
            "TRD": 0,
        }

        for block in blocks:
            departments_in_block = set()

            for request in block.block_requests:
                if request.task_id:
                    department = request.task_id.split("-")[0]

                    if department in department_counts:
                        departments_in_block.add(department)

            for department in departments_in_block:
                department_counts[department] += 1

        return department_counts        

    def close(self):
        self.db.close()