"""Database schema, connection helpers, and safe upsert operations."""
from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.config import settings


DDL = """
CREATE TABLE IF NOT EXISTS categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(150) NOT NULL,
    parent_id VARCHAR(50),
    type VARCHAR(20) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    category_id VARCHAR(50) REFERENCES categories(category_id)
);
CREATE INDEX IF NOT EXISTS idx_competitions_category ON competitions(category_id);
CREATE INDEX IF NOT EXISTS idx_competitions_parent ON competitions(parent_id);
CREATE TABLE IF NOT EXISTS complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(150) NOT NULL
);
CREATE TABLE IF NOT EXISTS venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(150) NOT NULL,
    city_name VARCHAR(100), country_name VARCHAR(100), country_code CHAR(3),
    timezone VARCHAR(100),
    complex_id VARCHAR(50) REFERENCES complexes(complex_id)
);
CREATE INDEX IF NOT EXISTS idx_venues_complex ON venues(complex_id);
CREATE INDEX IF NOT EXISTS idx_venues_country ON venues(country_code);
CREATE TABLE IF NOT EXISTS competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    country VARCHAR(100), country_code CHAR(3), abbreviation VARCHAR(20)
);
CREATE TABLE IF NOT EXISTS competitor_rankings (
    rank_id INTEGER PRIMARY KEY,
    rank INTEGER NOT NULL, movement INTEGER NOT NULL, points INTEGER NOT NULL,
    competitions_played INTEGER NOT NULL,
    competitor_id VARCHAR(50) NOT NULL REFERENCES competitors(competitor_id),
    ranking_type VARCHAR(20) NOT NULL DEFAULT 'doubles',
    retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(competitor_id, ranking_type)
);
CREATE INDEX IF NOT EXISTS idx_rankings_rank ON competitor_rankings(rank);
"""


def get_engine() -> Engine:
    """Build the configured SQLAlchemy engine."""
    return create_engine(settings.database_url, future=True)


def initialize_database(engine: Engine | None = None) -> Engine:
    """Create all normalized tables and indexes, safely on repeated runs."""
    engine = engine or get_engine()
    with engine.begin() as connection:
        for statement in DDL.split(";"):
            if statement.strip():
                connection.execute(text(statement))
    return engine


def upsert_rows(engine: Engine, table: str, rows: list[dict], key: str) -> int:
    """Insert or update records by primary key on SQLite/PostgreSQL/MySQL."""
    if not rows:
        return 0
    columns = list(rows[0])
    placeholders = ", ".join(f":{column}" for column in columns)
    assignments = ", ".join(f"{column}=excluded.{column}" for column in columns if column != key)
    sql = text(
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders}) "
        f"ON CONFLICT ({key}) DO UPDATE SET {assignments}"
    )
    with engine.begin() as connection:
        connection.execute(sql, rows)
    return len(rows)
