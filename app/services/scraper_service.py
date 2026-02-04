from sqlalchemy.orm import Session
from app.scrapers.example_scraper import ExampleJobScraper
from app.services.job_service import JobService
import logging

logger = logging.getLogger(__name__)


class ScraperService:
    def __init__(self):
        self.scrapers = [
            ExampleJobScraper(),
            # Add more scrapers here:
            # LinkedInScraper(),
            # IndeedScraper(),
            # etc.
        ]
    
    def run_all_scrapers(self, db: Session) -> dict:
        """Run all configured scrapers"""
        results = {
            "total_scraped": 0,
            "total_created": 0,
            "scrapers_run": 0,
            "details": []
        }
        
        for scraper in self.scrapers:
            try:
                logger.info(f"Running scraper: {scraper.source_name}")
                
                jobs = scraper.scrape_jobs()
                created_count = JobService.bulk_create_jobs(db, jobs)
                
                results["total_scraped"] += len(jobs)
                results["total_created"] += created_count
                results["scrapers_run"] += 1
                
                results["details"].append({
                    "scraper": scraper.source_name,
                    "scraped": len(jobs),
                    "created": created_count
                })
                
                logger.info(
                    f"Scraper {scraper.source_name}: "
                    f"scraped {len(jobs)}, created {created_count}"
                )
                
            except Exception as e:
                logger.error(f"Error running scraper {scraper.source_name}: {e}")
                results["details"].append({
                    "scraper": scraper.source_name,
                    "error": str(e)
                })
        
        return results
