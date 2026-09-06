from fastapi import FastAPI

from app.database.base import Base
from app.database.database import engine

from app.models.asset import Asset
from app.models.block_request import BlockRequest
from app.models.corridor import Corridor
from app.models.defect import Defect
from app.models.department import Department
from app.models.maintenance_task import MaintenanceTask
from app.models.optimization_run import OptimizationRun
from app.models.optimized_block_request import OptimizedBlockRequest
from app.models.optimized_block import OptimizedBlock
from app.models.train import Train

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
from app.routes import ai_intelligence

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Railway Automatic Block Planning",
    description="AI-powered automatic block planning system for Indian Railways",
    version="1.0.0",
)

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
],
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
app.include_router(ai_intelligence.router)


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

