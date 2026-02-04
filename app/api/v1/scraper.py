from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.scraper_service import ScraperService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


def run_scraper_task(db: Session):
    """Background task to run scraper"""
    scraper_service = ScraperService()
    results = scraper_service.run_all_scrapers(db)
    logger.info(f"Scraper completed: {results}")


@router.post("/run")
def trigger_scraper(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Manually trigger scraper"""
    background_tasks.add_task(run_scraper_task, db)
    return {
        "message": "Scraper started in background",
        "status": "running"
    }


@router.get("/status")
def scraper_status():
    """Get scraper status"""
    return {
        "status": "available",
        "scrapers_configured": 1,
        "message": "Use POST /api/v1/scraper/run to trigger scraping"
    }
