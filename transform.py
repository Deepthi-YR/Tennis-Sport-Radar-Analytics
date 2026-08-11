"""Normalize SportRadar JSON payloads into relational records."""
from __future__ import annotations

def _value(item: dict, *names: str, default=None):
    return next((item[n] for n in names if item.get(n) is not None), default)

def competitions_payload(payload: dict):
    categories, competitions = {}, []
    for item in payload.get("competitions", []):
        category = item.get("category") or {}
        category_id = _value(category, "id", default="uncategorized")
        categories[category_id] = {"category_id": category_id, "category_name": _value(category, "name", default="Unknown")}
        competitions.append({"competition_id": _value(item, "id"), "competition_name": _value(item, "name", default="Unknown"), "parent_id": _value(item.get("parent") or {}, "id"), "type": _value(item, "type", default="unknown"), "gender": _value(item, "gender", default="unknown"), "category_id": category_id})
    return list(categories.values()), competitions

def complexes_payload(payload: dict):
    complexes, venues = [], []
    for item in payload.get("complexes", []):
        complexes.append({"complex_id": item["id"], "complex_name": item.get("name", "Unknown")})
        for venue in item.get("venues", []):
            country = venue.get("country") or {}
            venues.append({"venue_id": venue["id"], "venue_name": venue.get("name", "Unknown"), "city_name": venue.get("city_name"), "country_name": _value(country, "name", default=venue.get("country_name")), "country_code": _value(country, "code", default=venue.get("country_code")), "timezone": venue.get("timezone"), "complex_id": item["id"]})
    return complexes, venues

def rankings_payload(payload: dict):
    competitors, rankings = [], []
    for league_index, league in enumerate(payload.get("rankings", [])):
        # The endpoint contains one ranking group each for ATP and WTA.
        # A prefixed integer avoids clashes where both groups have rank 1, 2, etc.
        for item in league.get("competitor_rankings", []):
            competitor = item.get("competitor") or {}
            competitor_id = competitor.get("id")
            if not competitor_id:
                continue
            competitors.append({"competitor_id": competitor_id, "name": competitor.get("name", "Unknown"), "country": competitor.get("country"), "country_code": competitor.get("country_code"), "abbreviation": competitor.get("abbreviation")})
            ranking_group = league.get("name") or league.get("gender") or str(league_index + 1)
            rankings.append({"rank_id": (league_index + 1) * 10000 + item.get("rank", len(rankings) + 1), "rank": item.get("rank", 0), "movement": item.get("movement", 0), "points": item.get("points", 0), "competitions_played": item.get("competitions_played", 0), "competitor_id": competitor_id, "ranking_type": f"doubles_{ranking_group.lower()}"})
    return competitors, rankings
