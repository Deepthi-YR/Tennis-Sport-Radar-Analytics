"""Command line ETL entry point for the three required SportRadar datasets."""
from src.api_client import SportRadarClient
from src.database import initialize_database, upsert_rows
from src.transform import competitions_payload, complexes_payload, rankings_payload

def main():
    engine, client = initialize_database(), SportRadarClient()
    categories, competitions = competitions_payload(client.get("competitions.json"))
    complexes, venues = complexes_payload(client.get("complexes.json"))
    competitors, rankings = rankings_payload(client.get("double_competitors_rankings.json"))
    for table, rows, key in [("categories", categories, "category_id"), ("competitions", competitions, "competition_id"), ("complexes", complexes, "complex_id"), ("venues", venues, "venue_id"), ("competitors", competitors, "competitor_id"), ("competitor_rankings", rankings, "rank_id")]:
        print(f"{table}: {upsert_rows(engine, table, rows, key)} loaded")

if __name__ == "__main__":
    main()
