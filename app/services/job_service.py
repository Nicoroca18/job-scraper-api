from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from app.models.job import Job
from app.schemas.job import JobCreate, JobStats
import logging

logger = logging.getLogger(__name__)


class JobService:
    @staticmethod
    def create_job(db: Session, job: JobCreate) -> Job:
        """Create new job listing"""
        db_job = Job(**job.model_dump())
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job
    
    @staticmethod
    def get_job_by_url(db: Session, url: str) -> Optional[Job]:
        """Get job by URL (to avoid duplicates)"""
        return db.query(Job).filter(Job.url == url).first()
    
    @staticmethod
    def get_jobs(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        company: Optional[str] = None,
        location: Optional[str] = None,
        job_type: Optional[str] = None,
        source: Optional[str] = None
    ) -> List[Job]:
        """Get jobs with filters"""
        query = db.query(Job).filter(Job.is_active == True)
        
        if company:
            query = query.filter(Job.company.ilike(f"%{company}%"))
        if location:
            query = query.filter(Job.location.ilike(f"%{location}%"))
        if job_type:
            query = query.filter(Job.job_type == job_type)
        if source:
            query = query.filter(Job.source == source)
        
        return query.order_by(desc(Job.scraped_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_job_by_id(db: Session, job_id: int) -> Optional[Job]:
        """Get job by ID"""
        return db.query(Job).filter(Job.id == job_id).first()
    
    @staticmethod
    def get_stats(db: Session) -> JobStats:
        """Get job statistics"""
        total_jobs = db.query(func.count(Job.id)).scalar()
        active_jobs = db.query(func.count(Job.id)).filter(Job.is_active == True).scalar()
        companies_count = db.query(func.count(func.distinct(Job.company))).scalar()
        locations_count = db.query(func.count(func.distinct(Job.location))).scalar()
        
        # Average salary
        avg_salary_result = db.query(
            func.avg((Job.salary_min + Job.salary_max) / 2)
        ).filter(
            Job.salary_min.isnot(None),
            Job.salary_max.isnot(None)
        ).scalar()
        
        avg_salary = float(avg_salary_result) if avg_salary_result else None
        
        # Top technologies (simplified - in production use proper parsing)
        tech_query = db.query(
            Job.technologies,
            func.count(Job.id).label('count')
        ).filter(
            Job.technologies.isnot(None)
        ).group_by(Job.technologies).order_by(desc('count')).limit(10).all()
        
        top_technologies = [
            {"technology": tech, "count": count} 
            for tech, count in tech_query
        ]
        
        # Jobs by source
        source_query = db.query(
            Job.source,
            func.count(Job.id).label('count')
        ).group_by(Job.source).all()
        
        jobs_by_source = [
            {"source": source, "count": count}
            for source, count in source_query
        ]
        
        return JobStats(
            total_jobs=total_jobs,
            active_jobs=active_jobs,
            companies_count=companies_count,
            locations_count=locations_count,
            avg_salary=avg_salary,
            top_technologies=top_technologies,
            jobs_by_source=jobs_by_source
        )
    
    @staticmethod
    def bulk_create_jobs(db: Session, jobs: List[JobCreate]) -> int:
        """Create multiple jobs, skip duplicates"""
        created_count = 0
        
        for job_data in jobs:
            # Check if job already exists
            existing_job = JobService.get_job_by_url(db, job_data.url)
            
            if not existing_job:
                try:
                    JobService.create_job(db, job_data)
                    created_count += 1
                except Exception as e:
                    logger.error(f"Error creating job {job_data.url}: {e}")
                    continue
            else:
                logger.debug(f"Job already exists: {job_data.url}")
        
        return created_count
