from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    scraper_interval_hours: int = 6
    max_retries: int = 3
    request_timeout: int = 10
    user_agent_rotate: bool = True
    enable_scheduler: bool = True
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
