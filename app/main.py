from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.api.v1.router import api_router
from app.db.database import init_db
from app.scheduler import start_scheduler
from app.core.config import get_settings
import os

settings = get_settings()

# Create logs directory
os.makedirs('logs', exist_ok=True)

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="Job Scraper API",
    description="Web scraper with REST API for tech job listings",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Start scheduler
scheduler = start_scheduler()


@app.on_event("shutdown")
def shutdown_event():
    """Shutdown scheduler on app shutdown"""
    if scheduler:
        scheduler.shutdown()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with simple dashboard"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "scheduler_enabled": settings.enable_scheduler,
        "scraper_interval_hours": settings.scraper_interval_hours
    }
