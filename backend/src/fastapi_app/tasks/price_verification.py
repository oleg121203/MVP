from celery import Celery
import os
import asyncio

from ..ai.vector_db_service import VectorDBService
from ..ai.price_verification_service import PriceVerificationService

# Initialize Celery app
app = Celery('ventai_tasks', broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'))
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour timeout
    task_soft_time_limit=3300,  # 55 minutes soft timeout
    task_acks_late=True,
    task_default_retry_delay=300,  # 5 minutes retry delay
    task_max_retries=3,
    task_retry_backoff=True,
    task_retry_backoff_max=1800,  # 30 minutes max backoff
    task_retry_jitter=True
)

# Initialize services
vector_db_service = VectorDBService()
price_verification_service = PriceVerificationService(vector_db_service)

def run_async(coroutine):
    """
    Helper to run async coroutines in a synchronous context for Celery tasks.
    """
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # If loop is already running, create a new one (rare case in Celery)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coroutine)

@app.task(
    name='ventai.price_verification.verify_prices',
    retry_backoff=True,
    retry_jitter=True,
    retry_max_delay=1800,
    max_retries=3,
    time_limit=3600
)
def verify_prices_task(material_ids=None, force_update=False):
    """
    Celery task to verify prices for materials in the vector database.

    Args:
        material_ids: Optional list of material IDs to verify. If None, check all materials.
        force_update: If True, update prices even for large discrepancies without manual review.

    Returns:
        Summary of the verification process including counts of checked, updated, and flagged items.
    """
    return run_async(price_verification_service.verify_prices(material_ids, force_update))
