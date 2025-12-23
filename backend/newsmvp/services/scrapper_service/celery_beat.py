from celery import Celery
from celery.schedules import crontab

from core.config import settings

celery_app = Celery(
    main="tasks_service",
    broker=settings.broker_url,
    backend=settings.result_backend_url,
    include=["services.scrapper_service.celery_worker"],
)

celery_app.conf.beat_schedule = {
    "rss_parser_news": {
        "task": "services.scrapper_service.celery_worker.execute_parser_rss",
        "schedule": crontab(minute="*/1"),
    },
}

celery_app.conf.beat_schedule_filename = "celerybeat-schedule/"

celery_app.conf.timezone = "UTC"
