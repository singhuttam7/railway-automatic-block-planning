from fastapi import APIRouter

from app.database.database import SessionLocal
from app.models.maintenance_task import MaintenanceTask
from app.models.optimized_block import OptimizedBlock
from app.models.optimization_run import OptimizationRun


router = APIRouter(
    prefix="/api/ai-intelligence",
    tags=["AI Intelligence"],
)


@router.get("/summary")
def get_ai_intelligence_summary():

    db = SessionLocal()

    try:
        # ---------------------------------------------------------
        # Latest optimization run
        # ---------------------------------------------------------

        latest_run = (
            db.query(OptimizationRun)
            .order_by(
                OptimizationRun.optimization_run_id.desc()
            )
            .first()
        )

        if latest_run is None:
            return {
                "priority_intelligence": {},
                "optimization_intelligence": {},
                "department_coordination": {},
                "ai_insights": [],
            }

        # ---------------------------------------------------------
        # Maintenance priority intelligence
        # ---------------------------------------------------------

        tasks = db.query(MaintenanceTask).all()

        priority_counts = {
            "Critical": 0,
            "High": 0,
            "Medium": 0,
            "Low": 0,
        }

        priority_scores = []

        for task in tasks:

            level = getattr(task, "priority_level", None)

            if level in priority_counts:
                priority_counts[level] += 1

            score = getattr(task, "priority_score", None)

            if score is not None:
                priority_scores.append(float(score))

        average_priority_score = (
            round(
                sum(priority_scores)
                / len(priority_scores),
                2,
            )
            if priority_scores
            else 0
        )

        # ---------------------------------------------------------
        # Optimization intelligence
        # ---------------------------------------------------------

        blocks = (
            db.query(OptimizedBlock)
            .filter(
                OptimizedBlock.optimization_run_id
                == latest_run.optimization_run_id
            )
            .all()
        )

        total_blocks = len(blocks)

        total_block_hours = round(
            sum(
                float(block.duration_hours or 0)
                for block in blocks
            ),
            2,
        )

        coordinated_blocks = sum(
            1
            for block in blocks
            if (block.department_count or 0) > 1
        )

        average_optimization_score = round(
            sum(
                float(block.optimization_score or 0)
                for block in blocks
            )
            / total_blocks,
            2,
        ) if total_blocks else 0

        # ---------------------------------------------------------
        # Department coordination
        # ---------------------------------------------------------

        department_coordination = {
            "ENG": 0,
            "SNT": 0,
            "TRD": 0,
        }

        for block in blocks:

            departments = set()

            for request in block.block_requests:

                if request.task_id:

                    department = (
                        request.task_id.split("-")[0]
                    )

                    if department in department_coordination:
                        departments.add(department)

            for department in departments:
                department_coordination[department] += 1

        # ---------------------------------------------------------
        # AI-generated planning insights
        # ---------------------------------------------------------

        ai_insights = []

        if coordinated_blocks > 0:
            ai_insights.append(
                f"AI consolidated {coordinated_blocks} "
                "multi-department maintenance blocks "
                "to improve corridor utilization."
            )

        if priority_counts["Critical"] > 0:
            ai_insights.append(
                f"{priority_counts['Critical']} critical "
                "maintenance tasks require priority attention."
            )

        if average_optimization_score >= 70:
            ai_insights.append(
                "The latest optimization run achieved "
                "a strong scheduling efficiency score."
            )
        elif average_optimization_score >= 50:
            ai_insights.append(
                "The latest optimization run achieved "
                "moderate scheduling efficiency."
            )
        else:
            ai_insights.append(
                "The AI optimizer identified opportunities "
                "for further scheduling improvement."
            )

        return {
            "optimization_run_id": latest_run.optimization_run_id,

            "priority_intelligence": {
                "total_tasks": len(tasks),
                "critical": priority_counts["Critical"],
                "high": priority_counts["High"],
                "medium": priority_counts["Medium"],
                "low": priority_counts["Low"],
                "average_priority_score": average_priority_score,
            },

            "optimization_intelligence": {
                "total_blocks": total_blocks,
                "total_block_hours": total_block_hours,
                "coordinated_blocks": coordinated_blocks,
                "average_optimization_score":
                    average_optimization_score,
            },

            "department_coordination":
                department_coordination,

            "ai_insights": ai_insights,
        }

    finally:
        db.close()