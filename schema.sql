-- Tennis SportRadar Analytics: normalized schema (SQLite/PostgreSQL friendly)
CREATE TABLE categories (category_id VARCHAR(50) PRIMARY KEY, category_name VARCHAR(100) NOT NULL);
CREATE TABLE competitions (
  competition_id VARCHAR(50) PRIMARY KEY, competition_name VARCHAR(150) NOT NULL,
  parent_id VARCHAR(50), type VARCHAR(20) NOT NULL, gender VARCHAR(20) NOT NULL,
  category_id VARCHAR(50) REFERENCES categories(category_id)
);
CREATE TABLE complexes (complex_id VARCHAR(50) PRIMARY KEY, complex_name VARCHAR(150) NOT NULL);
CREATE TABLE venues (
  venue_id VARCHAR(50) PRIMARY KEY, venue_name VARCHAR(150) NOT NULL,
  city_name VARCHAR(100), country_name VARCHAR(100), country_code CHAR(3), timezone VARCHAR(100),
  complex_id VARCHAR(50) REFERENCES complexes(complex_id)
);
CREATE TABLE competitors (
  competitor_id VARCHAR(50) PRIMARY KEY, name VARCHAR(150) NOT NULL,
  country VARCHAR(100), country_code CHAR(3), abbreviation VARCHAR(20)
);
CREATE TABLE competitor_rankings (
  rank_id INTEGER PRIMARY KEY, rank INTEGER NOT NULL, movement INTEGER NOT NULL, points INTEGER NOT NULL,
  competitions_played INTEGER NOT NULL, competitor_id VARCHAR(50) NOT NULL REFERENCES competitors(competitor_id),
  ranking_type VARCHAR(20) NOT NULL DEFAULT 'doubles', retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(competitor_id, ranking_type)
);
CREATE INDEX idx_competitions_category ON competitions(category_id);
CREATE INDEX idx_competitions_parent ON competitions(parent_id);
CREATE INDEX idx_venues_complex ON venues(complex_id);
CREATE INDEX idx_venues_country ON venues(country_code);
CREATE INDEX idx_rankings_rank ON competitor_rankings(rank);
