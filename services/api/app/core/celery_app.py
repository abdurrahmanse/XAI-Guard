from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "xaiguard",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json", # msgspec can be configured here natively if wrapped
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Queue Routing
    task_routes={
        'app.modules.events.tasks.*': {'queue': 'events'},
        'app.modules.explanations.tasks.*': {'queue': 'explanations'},
        'app.modules.drift.tasks.*': {'queue': 'pipeline'},
        'app.modules.registry.tasks.*': {'queue': 'pipeline'},
        'app.modules.training.tasks.*': {'queue': 'pipeline'},
    },
    
    # Task scheduling (Beat)
    beat_schedule={
        'nightly-champion-evaluation': {
            'task': 'app.modules.registry.tasks.nightly_eval',
            'schedule': 86400.0, # Every 24 hours
        },
    }
)
