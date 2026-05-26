# QueueForge

QueueForge is a backend-focused distributed asynchronous job processing system built to learn core backend engineering concepts like queues, workers, async processing, and state management.

## Phase 1 Features
- Create jobs via FastAPI
- Store job metadata in PostgreSQL (Supabase)
- Enqueue jobs in Redis with Celery
- Background worker processes jobs asynchronously
- Track job status and results

## Tech Stack
- FastAPI
- PostgreSQL (Supabase)
- Redis
- Celery
- SQLAlchemy
- Alembic
- Pydantic

## Local Run (High Level)
1. Set up `.env` with Supabase Postgres URL and Redis URL
2. Install dependencies: `pip install -r requirements.txt`
3. Create DB tables with Alembic
4. Start API and Celery worker

## Status
Phase 1 core pipeline implemented.
