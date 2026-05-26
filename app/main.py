from fastapi import FastAPI

from app.api.v1.routes.jobs import router as jobs_router


app = FastAPI(title="QueueForge")

app.include_router(jobs_router, prefix="/api/v1")
