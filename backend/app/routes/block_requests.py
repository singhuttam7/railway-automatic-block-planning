from fastapi import APIRouter, Depends, HTTPException

from app.schemas.block_request import BlockRequestResponse
from app.services.block_request_service import BlockRequestService


router = APIRouter(
    prefix="/api/block-requests",
    tags=["Block Requests"]
)


def get_block_request_service():
    service = BlockRequestService()

    try:
        yield service
    finally:
        service.close()


@router.get(
    "/",
    response_model=list[BlockRequestResponse]
)
def get_all_block_requests(
    service: BlockRequestService = Depends(
        get_block_request_service
    ),
):
    """Return all block requests."""
    return service.get_all_requests()


@router.get(
    "/corridor/{corridor_id}",
    response_model=list[BlockRequestResponse]
)
def get_block_requests_by_corridor(
    corridor_id: str,
    service: BlockRequestService = Depends(
        get_block_request_service
    ),
):
    """Return block requests for a specific corridor."""
    return service.get_requests_by_corridor(corridor_id)


@router.get(
    "/{block_request_id}",
    response_model=BlockRequestResponse
)
def get_block_request(
    block_request_id: str,
    service: BlockRequestService = Depends(
        get_block_request_service
    ),
):
    """Return a specific block request."""

    request = service.get_request_by_id(
        block_request_id
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Block request "
                f"'{block_request_id}' not found"
            )
        )

    return request