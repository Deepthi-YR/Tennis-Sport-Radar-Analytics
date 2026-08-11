"""Application configuration loaded from environment variables or Streamlit secrets."""

from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


def get_config_value(name: str, default: str = "") -> str:
    """Read configuration from environment variables or Streamlit secrets."""

    value = os.getenv(name)

    if value:
        return value

    try:
        import streamlit as st

        value = st.secrets.get(name)

        if value:
            return str(value)

    except Exception:
        pass

    return default


@dataclass(frozen=True)
class Settings:

    api_key: str = get_config_value(
        "SPORTRADAR_API_KEY"
    )

    database_url: str = get_config_value(
        "DATABASE_URL",
        "sqlite:///tennis_analytics.db"
    )

    base_url: str = get_config_value(
        "SPORTRADAR_BASE_URL",
        "https://api.sportradar.com/tennis/trial/v3/en"
    ).rstrip("/")


settings = Settings()
