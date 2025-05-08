from celery import shared_task
from dashboard.scraper import run_scraper as scrape

@shared_task
def run_scraper():
    return scrape()

