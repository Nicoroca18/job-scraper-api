import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from typing import Optional
import time
import logging
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)
ua = UserAgent()


def get_random_user_agent() -> str:
    """Get random user agent"""
    if settings.user_agent_rotate:
        return ua.random
    return ua.chrome


def fetch_page(url: str, retries: int = None) -> Optional[BeautifulSoup]:
    """Fetch and parse web page with retries"""
    if retries is None:
        retries = settings.max_retries
    
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(
                url, 
                headers=headers, 
                timeout=settings.request_timeout
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            return soup
            
        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt + 1}/{retries} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error(f"Failed to fetch {url} after {retries} attempts")
                return None
    
    return None


def clean_text(text: Optional[str]) -> Optional[str]:
    """Clean and normalize text"""
    if not text:
        return None
    return ' '.join(text.strip().split())


def extract_salary(text: str) -> tuple[Optional[float], Optional[float]]:
    """Extract salary range from text"""
    import re
    
    # Simple salary extraction (can be improved)
    salary_pattern = r'\$?([\d,]+)k?\s*-\s*\$?([\d,]+)k?'
    match = re.search(salary_pattern, text, re.IGNORECASE)
    
    if match:
        try:
            min_sal = float(match.group(1).replace(',', ''))
            max_sal = float(match.group(2).replace(',', ''))
            
            # If values are in thousands (e.g., 80k)
            if 'k' in text.lower():
                min_sal *= 1000
                max_sal *= 1000
            
            return min_sal, max_sal
        except ValueError:
            return None, None
    
    return None, None
