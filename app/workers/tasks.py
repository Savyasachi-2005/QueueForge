import asyncio
from uuid import UUID

from celery.utils.log import get_task_logger
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.job import Job, JobStatus
from app.workers.celery_app import celery_app


logger = get_task_logger(__name__)


@celery_app.task(name="queueforge.process_job")
def process_job(job_id: str) -> None:
    """Entrypoint for Celery to process a job asynchronously."""

    asyncio.run(_process_job(job_id))


async def _process_job(job_id: str) -> None:
    """Async worker logic that updates job status and results."""

    try:
        job_uuid = UUID(job_id)
    except ValueError:
        logger.error("Invalid job_id: %s", job_id)
        return

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Job).where(Job.id == job_uuid))
        job = result.scalar_one_or_none()

        if not job:
            logger.error("Job not found: %s", job_id)
            return

        job.status = JobStatus.PROCESSING
        await session.commit()

        try:
            await asyncio.sleep(1)
            job.result = {"message": "Job completed successfully"}
            job.status = JobStatus.COMPLETED
            job.error_message = None
        except Exception as exc:
            job.status = JobStatus.FAILED
            job.error_message = str(exc)
        finally:
            await session.commit()
