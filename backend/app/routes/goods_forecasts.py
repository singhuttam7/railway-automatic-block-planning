from fastapi import APIRouter, Depends, HTTPException

from app.schemas.goods_forecast import GoodsForecastResponse
from app.services.goods_forecast_service import GoodsForecastService


router = APIRouter(
    prefix="/api/goods-forecasts",
    tags=["Goods Forecasts"],
)


def get_goods_forecast_service():
    service = GoodsForecastService()
    try:
        yield service
    finally:
        service.close()


@router.get(
    "/",
    response_model=list[GoodsForecastResponse],
)
def get_all_goods_forecasts(
    service: GoodsForecastService = Depends(
        get_goods_forecast_service
    ),
):
    """Return all goods train forecasts."""
    return service.get_all_forecasts()


@router.get(
    "/corridor/{corridor_id}",
    response_model=list[GoodsForecastResponse],
)
def get_goods_forecasts_by_corridor(
    corridor_id: str,
    service: GoodsForecastService = Depends(
        get_goods_forecast_service
    ),
):
    """Return goods forecasts for a specific corridor."""
    return service.get_forecasts_by_corridor(corridor_id)


@router.get(
    "/{forecast_id}",
    response_model=GoodsForecastResponse,
)
def get_goods_forecast(
    forecast_id: str,
    service: GoodsForecastService = Depends(
        get_goods_forecast_service
    ),
):
    """Return a specific goods forecast."""

    forecast = service.get_forecast_by_id(
        forecast_id
    )

    if forecast is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Goods forecast "
                f"'{forecast_id}' not found"
            ),
        )

    return forecast