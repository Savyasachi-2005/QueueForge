from fastapi import FastAPI

from app.api.v1.routes.jobs import router as jobs_router
from app.db.session import init_db_engine
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine


app = FastAPI(title="QueueForge")

app.include_router(jobs_router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup() -> None:
	# Ensure the async engine/sessionmaker are initialized for the server process.
	init_db_engine()


@app.on_event("shutdown")
async def on_shutdown() -> None:
	# Attempt to dispose the engine cleanly if present.
	try:
		from app.db.session import engine

		if engine is not None:
			await engine.dispose()
	except Exception:
		pass
