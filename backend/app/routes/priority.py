from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.maintenance_task import MaintenanceTask


router = APIRouter(
    prefix="/api/priority",
    tags=["Priority"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/tasks")
def get_prioritized_tasks(db: Session = Depends(get_db)):
    tasks = (
        db.query(MaintenanceTask)
        .order_by(MaintenanceTask.priority_score.desc())
        .all()
    )

    return [
        {
            "task_id": task.task_id,
            "asset_id": task.asset_id,
            "task_type": task.task_type,
            "due_date": task.due_date,
            "priority": task.priority,
            "priority_score": task.priority_score,
            "priority_level": task.priority_level,
            "status": task.status,
        }
        for task in tasks
    ]


@router.get("/summary")
def get_priority_summary(db: Session = Depends(get_db)):
    tasks = db.query(MaintenanceTask).all()

    summary = {
        "total_tasks": len(tasks),
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for task in tasks:
        level = task.priority_level

        if level == "Critical":
            summary["critical"] += 1
        elif level == "High":
            summary["high"] += 1
        elif level == "Medium":
            summary["medium"] += 1
        elif level == "Low":
            summary["low"] += 1

    return summary