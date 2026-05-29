from celery import Celery

from app.core.config import settings


# Create a Celery application using Redis as the broker
celery_app = Celery(
    "queueforge",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.autodiscover_tasks(["app.workers"])

# Optional defaults for development-friendly behavior
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


# Ensure the async DB engine/sessionmaker is initialized in worker child processes
from celery.signals import worker_process_init

from app.db.session import init_db_engine


@worker_process_init.connect
def on_worker_process_init(**_kwargs):
    # Called in each worker process after it starts (or after fork).
    init_db_engine()
