from celery import shared_task
from datetime import datetime

@shared_task
def test_celery():
    print(f"[{datetime.now()}] Celery is working!")
    return "Celery task complete."
