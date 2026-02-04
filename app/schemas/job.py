from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional


class JobBase(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    description: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    url: str
    source: str
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    technologies: Optional[str] = None
    posted_date: Optional[datetime] = None


class JobCreate(JobBase):
    pass


class JobResponse(JobBase):
    id: int
    scraped_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class JobStats(BaseModel):
    total_jobs: int
    active_jobs: int
    companies_count: int
    locations_count: int
    avg_salary: Optional[float]
    top_technologies: list[dict]
    jobs_by_source: list[dict]
