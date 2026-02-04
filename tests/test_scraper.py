from app.scrapers.example_scraper import ExampleJobScraper


def test_example_scraper():
    scraper = ExampleJobScraper()
    jobs = scraper.scrape_jobs(max_pages=1)
    
    assert len(jobs) > 0
    assert jobs[0].title is not None
    assert jobs[0].company is not None
    assert jobs[0].url is not None


def test_scraper_api_trigger(client):
    response = client.post("/api/v1/scraper/run")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["status"] == "running"
