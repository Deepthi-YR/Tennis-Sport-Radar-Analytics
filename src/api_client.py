"""Resilient client for SportRadar Tennis API endpoints."""
from __future__ import annotations
import time
import requests
from src.config import settings

class SportRadarClient:
    def __init__(self, timeout: int = 30, retries: int = 3) -> None:
        if not settings.api_key:
            raise ValueError("SPORTRADAR_API_KEY is missing. Copy .env.example to .env first.")
        self.timeout, self.retries = timeout, retries

    def get(self, endpoint: str) -> dict:
        """Fetch JSON, retrying rate-limit and server failures."""
        url = f"{settings.base_url}/{endpoint.lstrip('/')}"
        for attempt in range(self.retries):
            try:
                response = requests.get(
                    url,
                    headers={"accept": "application/json", "x-api-key": settings.api_key},
                    timeout=self.timeout,
                )
            except requests.RequestException:
                if attempt < self.retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise
            if (response.status_code == 429 or response.status_code >= 500) and attempt < self.retries - 1:
                time.sleep(2 ** attempt)
                continue
            response.raise_for_status()
            return response.json()
        raise RuntimeError(f"Unable to retrieve {endpoint} after {self.retries} attempts.")
