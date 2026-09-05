from fastapi import APIRouter, Depends, HTTPException

from app.schemas.corridor import CorridorResponse
from app.services.corridor_service import CorridorService


router = APIRouter(
    prefix="/api/corridors",
    tags=["Corridors"]
)


def get_corridor_service():
    service = CorridorService()
    try:
        yield service
    finally:
        service.close()


@router.get(
    "/",
    response_model=list[CorridorResponse]
)
def get_all_corridors(
    service: CorridorService = Depends(get_corridor_service),
):
    """
    Return all railway corridors.
    """
    return service.get_all_corridors()


@router.get(
    "/{corridor_id}",
    response_model=CorridorResponse
)
def get_corridor(
    corridor_id: str,
    service: CorridorService = Depends(get_corridor_service),
):
    """
    Return a specific corridor by ID.
    """
    corridor = service.get_corridor_by_id(corridor_id)

    if corridor is None:
        raise HTTPException(
            status_code=404,
            detail=f"Corridor '{corridor_id}' not found"
        )

    return corridor