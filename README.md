# Tennis SportRadar Analytics

A production-style Streamlit analytics project implementing the supplied capstone brief: collect SportRadar Tennis competitions, complexes/venues, and doubles rankings; normalize them into SQL; and provide interactive analysis.

## What is included

- API ingestion with retry handling for throttling and transient failures.
- Normalized relational model for categories, competitions, complexes, venues, competitors, and rankings.
- Idempotent upsert loading and indexes for the common analysis paths.
- All 20 required analysis queries in `queries.sql`.
- Streamlit dashboard: executive metrics, rankings filters, competition hierarchy, venue view, and a read-only SQL explorer.
- Credential-safe configuration: no API key is committed.

## Requirements mapping

| PDF requirement | Implementation |
|---|---|
| Competitions and categories | `competitions.json` ETL, hierarchy-aware database table and dashboard |
| Complexes and venues | `complexes.json` ETL, complex/country/timezone analyses |
| Doubles competitor rankings | `rankings.json` ETL and competitor leaderboard |
| SQL analysis | `queries.sql` includes every mandated question |
| Streamlit UI | `app.py` has filtering, tables, Plotly chart, and safe query runner |

## Quick start

1. Create an environment and install dependencies:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env`, then enter your SportRadar API key. Ensure `SPORTRADAR_BASE_URL` matches the version and access level provisioned in your SportRadar console.
3. Load data:

   ```powershell
   python -m src.load_data
   ```

4. Run the application:

   ```powershell
   streamlit run app.py
   ```

SQLite is the default for simple evaluation. For PostgreSQL, set `DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/tennis_analytics` and install a server/database first.

## Architecture

`SportRadar API -> api_client.py -> transform.py -> database.py -> SQL database -> app.py`

The loaders are deliberately separated from the UI so scheduled ingestion can be added without changing dashboard code. API errors are surfaced instead of silently creating partial data.

## Submission checklist

- [ ] Add a valid API key only to local `.env`.
- [ ] Run ETL successfully and capture screenshots of the populated app.
- [ ] Execute representative queries from `queries.sql`.
- [ ] Upload this entire directory to GitHub, excluding `.env` and the local `*.db` file.
- [ ] Include a short demo explaining the three datasets, schema relationships, and insights.

## Notes

SportRadar endpoint names/response fields can differ by subscription version. The client makes the API base configurable, and the transformation layer is isolated so version-specific adjustments remain small and auditable.
