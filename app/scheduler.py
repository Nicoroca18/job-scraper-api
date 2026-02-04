from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.services.scraper_service import ScraperService
from app.db.database import SessionLocal
from app.core.config import get_settings
import logging

settings = get_settings()
logger = logging.getLogger(__name__)


def scheduled_scrape_job():
    """Job to run on schedule"""
    logger.info("Running scheduled scrape job")
    db = SessionLocal()
    try:
        scraper_service = ScraperService()
        results = scraper_service.run_all_scrapers(db)
        logger.info(f"Scheduled scrape completed: {results}")
    finally:
        db.close()


def start_scheduler():
    """Start the scheduler"""
    if not settings.enable_scheduler:
        logger.info("Scheduler disabled in settings")
        return None
    
    scheduler = BackgroundScheduler()
    
    # Run every X hours (configured in settings)
    scheduler.add_job(
        scheduled_scrape_job,
        'interval',
        hours=settings.scraper_interval_hours,
        id='scraper_job',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info(f"Scheduler started - will run every {settings.scraper_interval_hours} hours")
    
    return scheduler
