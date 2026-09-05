from app.database.database import SessionLocal
from app.models.maintenance_task import MaintenanceTask


class MaintenanceTaskService:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_tasks(self):
        return (
            self.db.query(MaintenanceTask)
            .order_by(
                MaintenanceTask.priority_score.desc()
            )
            .all()
        )

    def get_task_by_id(self, task_id: str):
        return (
            self.db.query(MaintenanceTask)
            .filter(MaintenanceTask.task_id == task_id)
            .first()
        )

    def get_tasks_by_priority_level(self, priority_level: str):
        return (
            self.db.query(MaintenanceTask)
            .filter(
                MaintenanceTask.priority_level == priority_level
            )
            .order_by(
                MaintenanceTask.priority_score.desc()
            )
            .all()
        )

    def close(self):
        self.db.close()