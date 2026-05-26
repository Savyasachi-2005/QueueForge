from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    """Request body for creating a job."""

    payload: Optional[Dict[str, Any]] = Field(default=None)


class JobStatusResponse(BaseModel):
    """Response body for fetching a job's status."""

    id: UUID
    status: str
    payload: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
