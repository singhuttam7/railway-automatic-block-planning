from fastapi import FastAPI

from app.routes.priority import router as priority_router
from app.routes.optimized_blocks import router as optimized_blocks_router
from app.routes.planning import router as planning_router

app = FastAPI(
    title="Railway Automatic Block Planning",
    description="AI-powered automatic block planning system for Indian Railways",
    version="1.0.0",
)

app.include_router(priority_router)
app.include_router(optimized_blocks_router)
app.include_router(planning_router)



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

