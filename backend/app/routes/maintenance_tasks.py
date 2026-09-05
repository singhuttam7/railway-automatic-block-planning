from fastapi import APIRouter, Depends, HTTPException

from app.schemas.maintenance_task import MaintenanceTaskResponse
from app.services.maintenance_task_service import MaintenanceTaskService


router = APIRouter(
    prefix="/api/maintenance-tasks",
    tags=["Maintenance Tasks"]
)


def get_maintenance_task_service():
    service = MaintenanceTaskService()
    try:
        yield service
    finally:
        service.close()


@router.get(
    "/",
    response_model=list[MaintenanceTaskResponse]
)
def get_all_maintenance_tasks(
    service: MaintenanceTaskService = Depends(
        get_maintenance_task_service
    ),
):
    """
    Return all maintenance tasks ordered by AI priority score.
    """
    return service.get_all_tasks()


@router.get(
    "/{task_id}",
    response_model=MaintenanceTaskResponse
)
def get_maintenance_task(
    task_id: str,
    service: MaintenanceTaskService = Depends(
        get_maintenance_task_service
    ),
):
    """
    Return a specific maintenance task by ID.
    """
    task = service.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Maintenance task '{task_id}' not found"
        )

    return task


@router.get(
    "/priority/{priority_level}",
    response_model=list[MaintenanceTaskResponse]
)
def get_tasks_by_priority(
    priority_level: str,
    service: MaintenanceTaskService = Depends(
        get_maintenance_task_service
    ),
):
    """
    Return maintenance tasks filtered by priority level.
    """
    tasks = service.get_tasks_by_priority_level(priority_level)

    return tasks