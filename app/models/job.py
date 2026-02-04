from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from datetime import datetime
from app.db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False, index=True)
    location = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    url = Column(String, unique=True, nullable=False)
    source = Column(String, nullable=False, index=True)  # website scraped from
    job_type = Column(String, nullable=True)  # remote, hybrid, onsite
    experience_level = Column(String, nullable=True)  # junior, mid, senior
    technologies = Column(String, nullable=True)  # comma-separated
    posted_date = Column(DateTime, nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow, index=True)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Job {self.title} at {self.company}>"
