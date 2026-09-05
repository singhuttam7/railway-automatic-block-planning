from fastapi import APIRouter, Depends, HTTPException

from app.schemas.train import TrainResponse
from app.services.train_service import TrainService


router = APIRouter(
    prefix="/api/trains",
    tags=["Trains"],
)


def get_train_service():
    service = TrainService()

    try:
        yield service
    finally:
        service.close()


@router.get(
    "/",
    response_model=list[TrainResponse],
)
def get_all_trains(
    service: TrainService = Depends(
        get_train_service
    ),
):
    """Return all trains."""

    return service.get_all_trains()


@router.get(
    "/corridor/{corridor_id}",
    response_model=list[TrainResponse],
)
def get_trains_by_corridor(
    corridor_id: str,
    service: TrainService = Depends(
        get_train_service
    ),
):
    """Return trains operating on a specific corridor."""

    return service.get_trains_by_corridor(corridor_id)


@router.get(
    "/{train_id}",
    response_model=TrainResponse,
)
def get_train(
    train_id: str,
    service: TrainService = Depends(
        get_train_service
    ),
):
    """Return a specific train."""

    train = service.get_train_by_id(train_id)

    if train is None:
        raise HTTPException(
            status_code=404,
            detail=f"Train '{train_id}' not found",
        )

    return train