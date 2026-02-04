from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.job import JobResponse, JobStats
from app.services.job_service import JobService

router = APIRouter()


@router.get("/", response_model=List[JobResponse])
def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    company: Optional[str] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    source: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get job listings with optional filters"""
    jobs = JobService.get_jobs(
        db=db,
        skip=skip,
        limit=limit,
        company=company,
        location=location,
        job_type=job_type,
        source=source
    )
    return jobs


@router.get("/stats", response_model=JobStats)
def get_stats(db: Session = Depends(get_db)):
    """Get job statistics"""
    return JobService.get_stats(db)


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get specific job by ID"""
    job = JobService.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
