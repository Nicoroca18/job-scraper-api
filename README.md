# Job Scraper API

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Automated web scraper with REST API for collecting and analyzing tech job listings from multiple sources.

## Features

- ✅ **Automated Scraping** - Scheduled job collection every 6 hours
- ✅ **REST API** - Query jobs with filters (company, location, type)
- ✅ **Multiple Sources** - Extensible scraper architecture
- ✅ **Data Storage** - PostgreSQL database
- ✅ **Analytics** - Statistics and insights
- ✅ **Web Dashboard** - Simple UI for viewing data
- ✅ **Rate Limiting** - Respectful scraping with delays
- ✅ **Duplicate Detection** - Avoid storing duplicate jobs
- ✅ **Background Tasks** - Async scraping with FastAPI
- ✅ **Docker Support** - Easy deployment

## Quick Start

### Using Docker (Recommended)
```bash
# Start services (PostgreSQL + Redis)
docker-compose up -d

# Install dependencies
pip install -r requirements.txt

# Run API
uvicorn app.main:app --reload

# API runs at: http://localhost:8000
# Dashboard at: http://localhost:8000
# Docs at: http://localhost:8000/docs
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env

# Start PostgreSQL and Redis
# (or use docker-compose for databases only)

# Run API
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

### Jobs
```bash
# Get all jobs
GET /api/v1/jobs/
Query params: ?skip=0&limit=100&company=TechCorp&location=Madrid&job_type=remote

# Get job by ID
GET /api/v1/jobs/{job_id}

# Get statistics
GET /api/v1/jobs/stats

Response:
{
  "total_jobs": 150,
  "active_jobs": 145,
  "companies_count": 45,
  "avg_salary": 65000,
  "top_technologies": [...],
  "jobs_by_source": [...]
}
```

### Scraper
```bash
# Trigger scraper manually
POST /api/v1/scraper/run

# Get scraper status
GET /api/v1/scraper/status
```

## Project Structure
```
job-scraper-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── jobs.py         # Job endpoints
│   │       ├── scraper.py      # Scraper endpoints
│   │       └── router.py       # API router
│   ├── core/
│   │   ├── config.py          # Settings
│   │   └── logging.py         # Logging setup
│   ├── db/
│   │   └── database.py        # Database connection
│   ├── models/
│   │   └── job.py             # SQLAlchemy models
│   ├── schemas/
│   │   └── job.py             # Pydantic schemas
│   ├── scrapers/
│   │   └── example_scraper.py # Scraper implementations
│   ├── services/
│   │   ├── job_service.py     # Job business logic
│   │   └── scraper_service.py # Scraper orchestration
│   ├── utils/
│   │   └── scraper_helpers.py # Helper functions
│   ├── scheduler.py           # Background scheduler
│   └── main.py               # FastAPI app
├── templates/
│   └── index.html            # Dashboard UI
├── static/
├── tests/
│   ├── test_jobs.py
│   └── test_scraper.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Adding New Scrapers

1. **Create scraper class** in `app/scrapers/`:
```python
from app.schemas.job import JobCreate
from app.utils.scraper_helpers import fetch_page

class LinkedInScraper:
    def __init__(self):
        self.base_url = "https://linkedin.com"
        self.source_name = "LinkedIn"
    
    def scrape_jobs(self, max_pages=3):
        jobs = []
        # Your scraping logic here
        return jobs
```

2. **Register scraper** in `app/services/scraper_service.py`:
```python
self.scrapers = [
    ExampleJobScraper(),
    LinkedInScraper(),  # Add new scraper
]
```

## Web Scraping Best Practices

### Implemented in This Project

- ✅ **User-Agent Rotation** - Avoid detection
- ✅ **Request Delays** - Respect rate limits
- ✅ **Retry Logic** - Handle temporary failures
- ✅ **Error Handling** - Graceful failure recovery
- ✅ **Duplicate Detection** - Avoid storing duplicates

### Legal Considerations

- Read and respect `robots.txt`
- Follow website Terms of Service
- Don't overload servers (use delays)
- Only scrape publicly available data
- For educational purposes

## Configuration

Environment variables (`.env`):
```env
DATABASE_URL=postgresql://user:password@localhost:5432/jobsdb
REDIS_URL=redis://localhost:6379/0
SCRAPER_INTERVAL_HOURS=6
MAX_RETRIES=3
REQUEST_TIMEOUT=10
USER_AGENT_ROTATE=true
ENABLE_SCHEDULER=true
LOG_LEVEL=INFO
```

## Testing
```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test
pytest tests/test_jobs.py -v
```

## Deployment

### Docker
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f app
```

### Production Checklist

- [ ] Use production database
- [ ] Configure proper rate limits
- [ ] Set up monitoring (Sentry)
- [ ] Enable logging to external service
- [ ] Use environment variables for secrets
- [ ] Set up CI/CD pipeline
- [ ] Add authentication for scraper endpoints
- [ ] Configure CORS properly

## Interview Talking Points

### Web Scraping
- **BeautifulSoup vs Selenium**: When to use each
- **Rate Limiting**: Exponential backoff strategy
- **Error Handling**: Retry logic with delays
- **Legal/Ethical**: robots.txt, ToS compliance

### Architecture
- **Background Tasks**: FastAPI BackgroundTasks vs Celery
- **Scheduling**: APScheduler for periodic tasks
- **Data Storage**: Duplicate detection strategy
- **Scalability**: How to scale scrapers (workers, queues)

### API Design
- **Filtering**: Query parameters for flexible search
- **Pagination**: skip/limit pattern
- **Statistics**: Aggregation queries with SQLAlchemy

### Real-World Use Cases
- Job aggregator platforms (Indeed, Glassdoor)
- Price comparison sites
- News aggregators
- Market research tools
- Competitive analysis

## Performance

- **Async Requests**: Non-blocking I/O
- **Database Indexing**: On url, company, scraped_at
- **Connection Pooling**: Efficient DB connections
- **Caching**: Redis for frequently accessed data

## Monitoring

Check logs in `logs/scraper.log`:
```bash
tail -f logs/scraper.log
```

## License

MIT License

## Author

[Tu Nombre] - Data Engineer / Backend Engineer

---

**Built with:** FastAPI, BeautifulSoup, PostgreSQL, APScheduler, Docker
