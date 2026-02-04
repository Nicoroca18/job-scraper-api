import logging
import sys
from app.core.config import get_settings

settings = get_settings()


def setup_logging():
    """Configure application logging"""
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/scraper.log')
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()
