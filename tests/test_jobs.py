from app.schemas.job import JobCreate
from app.services.job_service import JobService
from datetime import datetime


def test_create_job(db):
    job_data = JobCreate(
        title="Software Engineer",
        company="TechCorp",
        location="Madrid, Spain",
        description="Great opportunity",
        salary_min=50000,
        salary_max=70000,
        url="https://example.com/job/123",
        source="TestSource",
        job_type="remote",
        experience_level="mid",
        technologies="Python, FastAPI",
        posted_date=datetime.utcnow()
    )
    
    job = JobService.create_job(db, job_data)
    
    assert job.id is not None
    assert job.title == "Software Engineer"
    assert job.company == "TechCorp"


def test_get_jobs_api(client, db):
    # Create a job first
    job_data = JobCreate(
        title="Backend Developer",
        company="StartupXYZ",
        url="https://example.com/job/456",
        source="TestSource"
    )
    JobService.create_job(db, job_data)
    
    response = client.get("/api/v1/jobs/")
    assert response.status_code == 200
    jobs = response.json()
    assert len(jobs) > 0
    assert jobs[0]["title"] == "Backend Developer"


def test_get_stats(client, db):
    # Create some jobs
    for i in range(3):
        job_data = JobCreate(
            title=f"Job {i}",
            company=f"Company {i}",
            url=f"https://example.com/job/{i}",
            source="TestSource"
        )
        JobService.create_job(db, job_data)
    
    response = client.get("/api/v1/jobs/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_jobs"] == 3
    assert stats["companies_count"] == 3
