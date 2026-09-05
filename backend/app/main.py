from fastapi import FastAPI

from app.routes.priority import router as priority_router
from app.routes.optimized_blocks import router as optimized_blocks_router
from app.routes.planning import router as planning_router
from app.routes.dashboard import router as dashboard_router
from app.routes.corridors import router as corridors_router
from app.routes.maintenance_tasks import router as maintenance_tasks_router
from app.routes.block_requests import router as block_requests_router
from app.routes.optimized_block_details import (
    router as optimized_block_details_router
)
from app.routes.optimization_runs import (
    router as optimization_runs_router
)

from app.routes.trains import router as trains_router
from app.routes.goods_forecasts import (
    router as goods_forecasts_router
)
from app.routes import what_if

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Railway Automatic Block Planning",
    description="AI-powered automatic block planning system for Indian Railways",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(priority_router)
app.include_router(optimized_blocks_router)
app.include_router(planning_router)
app.include_router(dashboard_router)
app.include_router(corridors_router)
app.include_router(maintenance_tasks_router)
app.include_router(block_requests_router)
app.include_router(optimized_block_details_router)
app.include_router(optimization_runs_router)
app.include_router(trains_router)
app.include_router(goods_forecasts_router)
app.include_router(what_if.router)


@app.get("/")
def root():
    return {
        "message": "Railway Automatic Block Planning API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

