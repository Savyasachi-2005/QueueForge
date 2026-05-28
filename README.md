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
1. Start Redis with Docker: `docker compose up -d redis`
2. Set up `.env` with Supabase Postgres URL and Redis URL
3. Install dependencies: `pip install -r requirements.txt`
4. Create DB tables with Alembic
5. Start API and Celery worker

## GitHub Codespaces
1. Open the repository in Codespaces.
2. The devcontainer starts the app container and Redis automatically.
3. Copy `.env.example` to `.env` and set `DATABASE_URL` for your Supabase Postgres instance.
4. Run the API with `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
5. Start the worker with `celery -A app.workers.celery_app.celery_app worker --loglevel=info`.

## Redis
QueueForge expects Redis to be reachable on `localhost:6379` by default. The included Docker Compose service exposes that port, so the default `REDIS_URL=redis://localhost:6379/0` works for local development.

Inside Codespaces, the Redis service is reachable as `redis://redis:6379/0` from the app container.

## Status
Phase 1 core pipeline implemented.
