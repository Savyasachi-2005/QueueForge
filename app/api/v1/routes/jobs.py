from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.models.job import Job, JobStatus
from app.schemas.job import JobCreate, JobStatusResponse
from app.workers.tasks import process_job


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobStatusResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_in: JobCreate,
    db_session: AsyncSession = Depends(get_db_session),
) -> JobStatusResponse:
    """Create a job and mark it as queued."""

    job = Job(payload=job_in.payload, status=JobStatus.QUEUED)
    db_session.add(job)
    await db_session.commit()
    await db_session.refresh(job)

    process_job.delay(str(job.id))

    return job


@router.get("/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: UUID,
    db_session: AsyncSession = Depends(get_db_session),
) -> JobStatusResponse:
    """Fetch the latest job status by ID."""

    result = await db_session.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    return job
