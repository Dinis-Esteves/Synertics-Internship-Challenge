from celery import shared_task
from dashboard.scraper import run_scraper as scrape
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

@shared_task
def run_scraper():
    try:
        result = scrape()

        product_list = "\n- " + "\n- ".join(result["products"]) if result["products"] else "None"
        body = (
            f"✅ Scraper ran successfully.\n\n"
            f"Date: {result['date']}\n"
            f"Total Products: {result['count']}\n"
            f"Products:{product_list}"
        )

        logger.info("Sending scraper success email.")
        send_mail(
            subject=f'✅ Scraper succeeded: {result["date"]}',
            message=body,
            from_email='alerts@example.com',
            recipient_list=['dinis.dme@gmail.com'],
            fail_silently=False,
        )

        return result

    except Exception as e:
        logger.exception("Scraper crashed.")
        send_mail(
            subject='❌ Scraper Failed',
            message=f'Scraper error:\n\n{str(e)}',
            from_email='alerts@example.com',
            recipient_list=['dinis.dme@gmail.com'],
            fail_silently=False,
        )
        raise
