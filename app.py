"""Replay simulated weekly receipts alongside real satellite composites."""
import json

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from backtest import DATA
from weekly import satellite_pixels

LABELS = {
    "persistence": "Previous week",
    "market_only": "Sales history + season",
    "market_satellite": "Sales history + season + satellite",
}
st.set_page_config(page_title="OceanAlpha Atlantic", page_icon="🌊", layout="wide")
st.title("OceanAlpha Atlantic")
st.write("Could satellite ocean colour help forecast weekly sardine auction receipts?")
weekly, annual = st.tabs(["Weekly port simulation", "Observed Portugal annual backtest"])


@st.cache_data
def load_weekly():
    predictions = pd.read_csv(DATA / "weekly_simulation_predictions.csv",
                              parse_dates=["week", "time", "available"])
    scores = pd.read_csv(DATA / "weekly_simulation_metrics.csv")
    return predictions, scores, satellite_pixels()


with weekly:
    st.warning("Simulated weekly sales. NASA chlorophyll observations are real. "
               "The sales outcomes are generated and provide no evidence about actual port income.")
    predictions, scores, pixels = load_weekly()
    scenario = st.radio("Simulation scenario", predictions.scenario.unique(), horizontal=True)
    rows = predictions.loc[predictions.scenario.eq(scenario)].set_index("week")
    week = st.select_slider("Forecast issue date (Monday, UTC)", rows.index.tolist(),
                            format_func=lambda value: str(value.date()))
    row = rows.loc[week]
    for column, (key, label) in zip(st.columns(3), LABELS.items()):
        column.metric(label, f"€{row[key]:,.0f}")
    st.caption("Target is gross simulated sardine sale value during the following seven days.")
    grid = pixels.loc[pixels.time.eq(row.time)].pivot(
        index="latitude", columns="longitude", values="chlor_a"
    ).sort_index()
    figure = px.imshow(np.log10(grid), origin="lower", aspect="auto",
                       color_continuous_scale="Viridis",
                       labels={"color": "log₁₀ mg/m³", "x": "Longitude", "y": "Latitude"})
    figure.update_layout(title=f"Off Peniche · Aqua MODIS composite centred {row.time.date()}",
                         height=320, margin=dict(l=0, r=0, b=0))
    st.plotly_chart(figure, width="stretch")
    st.caption(f"Assumed available {row.available.date()}. Blank cells lack a valid retrieval.")
    if st.button("Reveal simulated receipts", key=f"{scenario}-{week.date()}"):
        st.success(f"Simulated gross receipts €{row.simulated_sales_eur:,.0f}")
        st.write(f"Simulated volume {row.kg:,.0f} kg · simulated unit price €{row.eur_per_kg:.2f}/kg")
    with st.expander("Simulation scoreboard"):
        table = scores.loc[scores.scenario.eq(scenario)].set_index("model")
        st.dataframe(table.drop(columns="scenario").rename(index=LABELS).round(0))

with annual:
    st.info("Observed Portuguese national totals, compared year by year. "
            "Gross landed value is reported by Eurostat and can include estimated value.")
    result = json.loads((DATA / "metrics.json").read_text(encoding="utf-8"))["gross_value_eur"]
    st.write(f"Held-out years {result['test_years'][0]}–{result['test_years'][-1]}")
    st.dataframe(pd.DataFrame({key: value for key, value in result.items()
                               if isinstance(value, dict)}).T.round(0))
    st.caption("MAE and RMSE are in euros. The annual backtest uses chlorophyll and surface temperature.")
