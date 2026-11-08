"""Build a weekly replay with observed ocean pixels and simulated auction receipts."""
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from backtest import DATA

SPLIT = pd.Timestamp("2023-01-02", tz="UTC")
MARKET = ["last_sales", "season_sin", "season_cos"]
MODELS = ["persistence", "market_only", "market_satellite"]


def satellite_pixels():
    pixels = pd.read_csv(DATA / "modis_8day.csv", skiprows=[1], parse_dates=["time"])
    pixels["chlor_a"] = pixels.chlor_a.where(pixels.chlor_a.gt(0))
    return pixels


def weekly_inputs(pixels):
    composites = pixels.groupby("time").chlor_a.agg(["median", "count"]).reset_index()
    composites = composites.loc[composites["count"].ge(5)].copy()
    # The timestamp is the composite centre. Four days to close the window,
    # plus fourteen days assumed for processing and delivery.
    composites["available"] = composites.time + pd.Timedelta(days=18)
    dates = pd.DataFrame({"week": pd.date_range(
        "2017-02-06", "2024-12-30", freq="W-MON", tz="UTC"
    )})
    frame = pd.merge_asof(dates, composites, left_on="week", right_on="available",
                          tolerance=pd.Timedelta(days=32)).set_index("week")
    frame["log_chl"] = np.log(frame["median"])
    assert (frame.available.dropna() <= frame.available.dropna().index).all()
    angle = 2 * np.pi * (frame.index.day_of_year - 1) / 365.25
    frame["season_sin"], frame["season_cos"] = np.sin(angle), np.cos(angle)
    return frame


def simulate(inputs, strength):
    frame = inputs.copy()
    rng = np.random.default_rng(2608)
    # Both scenarios share the same season and random draws. The planted effect
    # changes quantity only. Price moves independently around a seasonal level.
    signal = frame.log_chl.ffill().fillna(np.log(0.35)) - np.log(0.35)
    frame["kg"] = np.exp(10.1 + 0.55 * frame.season_sin
                         + rng.normal(0, 0.32, len(frame)) + strength * signal)
    frame["eur_per_kg"] = np.exp(0.22 - 0.18 * frame.season_sin
                                 + rng.normal(0, 0.18, len(frame)))
    frame["simulated_sales_eur"] = frame.kg * frame.eur_per_kg
    # Assume the previous week's receipts are available on Monday at issue.
    frame["last_sales"] = frame.simulated_sales_eur.shift(1)
    return frame


def score(frame, target="simulated_sales_eur", horizon=1):
    frame = frame.copy()
    frame["outcome"] = frame[target].shift(1 - horizon)
    eligible = frame.dropna(subset=MARKET + ["log_chl", "outcome"])
    # A target week must finish by the first held-out issue date.
    train = eligible.loc[eligible.index + pd.Timedelta(weeks=horizon) <= SPLIT]
    test = eligible.loc[eligible.index >= SPLIT].copy()
    if train.empty or test.empty:
        raise ValueError("Insufficient weekly coverage for the chronological split")
    test["persistence"] = test.last_sales
    for model, columns in [
        ("market_only", MARKET), ("market_satellite", MARKET + ["log_chl"]),
    ]:
        fit = make_pipeline(StandardScaler(), Ridge(alpha=10))
        fit.fit(train[columns], np.log(train.outcome))
        test[model] = np.exp(fit.predict(test[columns]))
    return test, len(train)


def main():
    inputs = weekly_inputs(satellite_pixels())
    predictions = []
    metrics = []
    for name, strength in [("No planted signal", 0.0), ("Planted signal", 0.65)]:
        test, n_train = score(simulate(inputs, strength))
        predictions.append(test.assign(scenario=name)[[
            "scenario", "time", "available", "kg", "eur_per_kg",
            "simulated_sales_eur", *MODELS,
        ]])
        for model in MODELS:
            error = test[model] - test.simulated_sales_eur
            metrics.append({"scenario": name, "model": model, "train_weeks": n_train,
                            "test_weeks": len(test), "mae_eur": error.abs().mean()})
    pd.concat(predictions).to_csv(DATA / "weekly_simulation_predictions.csv")
    scores = pd.DataFrame(metrics)
    scores.to_csv(DATA / "weekly_simulation_metrics.csv", index=False)
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
