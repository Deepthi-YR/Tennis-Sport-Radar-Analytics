"""Interactive Streamlit dashboard for Tennis SportRadar Analytics."""
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import text
from src.database import get_engine, initialize_database

st.set_page_config(page_title="Tennis Analytics", page_icon="🎾", layout="wide")
initialize_database()
engine = get_engine()

@st.cache_data(ttl=60)
def query(sql, params=None):
    return pd.read_sql(text(sql), engine, params=params or {})

st.title("🎾 Tennis SportRadar Analytics")
st.caption("Competition explorer, venue intelligence, and doubles ranking analysis")
tabs = st.tabs(["Overview", "Competitors", "Competitions", "Venues", "SQL Explorer"])

with tabs[0]:
    metrics = query("SELECT (SELECT COUNT(*) FROM competitors) competitors, (SELECT COUNT(DISTINCT country_code) FROM competitors) countries, (SELECT COALESCE(MAX(points),0) FROM competitor_rankings) highest_points")
    a, b, c = st.columns(3)
    a.metric("Competitors", int(metrics.loc[0, "competitors"]))
    b.metric("Countries represented", int(metrics.loc[0, "countries"]))
    c.metric("Highest points", int(metrics.loc[0, "highest_points"]))
    types = query("SELECT type, COUNT(*) total FROM competitions GROUP BY type")
    if not types.empty: st.plotly_chart(px.pie(types, names="type", values="total", title="Competition type mix"), use_container_width=True)
    else: st.info("Load API data to populate the dashboard: `python -m src.load_data`.")

with tabs[1]:
    data = query("""
        SELECT 
            c.name,
            c.country,
            c.country_code,
            r.rank,
            r.movement,
            r.points,
            r.competitions_played
        FROM competitors c
        JOIN competitor_rankings r 
            ON c.competitor_id = r.competitor_id
        ORDER BY r.rank
    """)

    if not data.empty:

        countries = ["All"] + sorted(
            data["country"].dropna().unique().tolist()
        )

        country = st.selectbox("Country", countries)

        # Calculate maximum rank from the database
        maximum_rank = int(data["rank"].max())

        # Make sure slider has a valid range
        maximum_rank = max(1, maximum_rank)

        # Default value = 50, or maximum rank if fewer than 50
        default_rank = min(50, maximum_rank)

        rank_limit = st.slider(
            "Maximum rank",
            min_value=1,
            max_value=maximum_rank,
            value=default_rank,
            step=1
        )

        shown = data[data["rank"] <= rank_limit]

        if country != "All":
            shown = shown[shown["country"] == country]

        st.dataframe(
            shown,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning("No ranking data available.")

with tabs[2]:
    data = query("SELECT cp.competition_name, cp.type, cp.gender, ca.category_name, parent.competition_name parent_competition FROM competitions cp JOIN categories ca ON cp.category_id=ca.category_id LEFT JOIN competitions parent ON cp.parent_id=parent.competition_id")
    if not data.empty:
        selected = st.multiselect("Competition type", sorted(data.type.unique()), default=sorted(data.type.unique()))
        st.dataframe(data[data.type.isin(selected)], use_container_width=True, hide_index=True)
    else: st.info("No competition data loaded.")

with tabs[3]:
    data = query("SELECT v.venue_name, v.city_name, v.country_name, v.timezone, c.complex_name FROM venues v JOIN complexes c ON v.complex_id=c.complex_id")
    st.dataframe(data, use_container_width=True, hide_index=True)

with tabs[4]:
    st.caption("Read-only analysis query runner. Only SELECT statements are accepted.")
    sql = st.text_area("SQL", "SELECT c.name, r.rank, r.points FROM competitors c JOIN competitor_rankings r ON c.competitor_id=r.competitor_id ORDER BY r.rank LIMIT 10")
    if st.button("Run query"):
        if not sql.strip().lower().startswith("select"):
            st.error("Only SELECT queries are allowed.")
        else:
            try: st.dataframe(query(sql), use_container_width=True, hide_index=True)
            except Exception as exc: st.error(str(exc))
