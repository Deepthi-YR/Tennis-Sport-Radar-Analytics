"""Application configuration loaded from environment variables."""
from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("SPORTRADAR_API_KEY", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///tennis_analytics.db")
    base_url: str = os.getenv(
        "SPORTRADAR_BASE_URL", "https://api.sportradar.com/tennis/trial/v3/en"
    ).rstrip("/")


settings = Settings()
