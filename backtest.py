"""Run the annual Portugal feasibility screen from pinned source snapshots."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
TEST_START = 2018
LAG = 2


def load_market():
    source = json.loads((DATA / "eurostat.json").read_text(encoding="utf-8"))
    dimensions = source["dimension"]
    unit_index = dimensions["unit"]["category"]["index"]
    year_index = dimensions["time"]["category"]["index"]
    if source["size"] != [1, 1, 1, 1, 1, 3, 1, len(year_index)]:
        raise ValueError("Unexpected Eurostat data dimensions")
    if any(list(dimensions[key]["category"]["index"]) != [value] for key, value in {
        "freq": "A", "geo": "PT", "species": "PIL", "pres": "TOTAL",
        "natvessr": "TOTAL", "dest_use": "TOTAL",
    }.items()):
        raise ValueError("Unexpected Eurostat scope")

    def series(unit):
        offset = unit_index[unit] * len(year_index)
        return pd.Series({int(year): source["value"].get(str(offset + position))
                          for year, position in year_index.items()}, dtype=float)

    return pd.DataFrame({
        "tonnes": series("TPW"),
        "eur_per_kg": series("EUR_T") / 1000,
        "gross_value_eur": series("EUR"),
    })


def load_ocean(filename, variable):
    pixels = pd.read_csv(DATA / filename, skiprows=[1])
    pixels["month"] = pd.to_datetime(pixels.time, utc=True).dt.strftime("%Y-%m")
    values = pixels[variable]
    if variable == "chlor_a":
        values = values.where(values.gt(0))
    monthly = values.groupby(pixels.month).median()
    # Require a valid regional observation in every month before computing a year.
    groups = monthly.groupby(monthly.index.str[:4].astype(int))
    return groups.mean().where(groups.count().eq(12)).rename(variable)


def make_panel(market, ocean):
    years = pd.RangeIndex(market.index.min(), market.index.max() + 1, name="year")
    panel = market.reindex(years).join(ocean)
    for column in market.columns:
        panel[f"{column}_lag"] = panel[column].shift(LAG)
    panel["log_chlorophyll_lag"] = np.log(panel.chlor_a).shift(LAG)
    panel["sst_lag"] = panel.sst.shift(LAG)
    panel["feature_year"] = years - LAG
    return panel


def main():
    ocean = pd.concat([
        load_ocean("modis_chlorophyll.csv", "chlor_a"),
        load_ocean("mur_temperature.csv", "sst"),
    ], axis=1)
    panel = make_panel(load_market(), ocean)
    predictions = []
    results = {}
    for target in ["tonnes", "eur_per_kg", "gross_value_eur"]:
        baseline = [f"{target}_lag"]
        chlorophyll = baseline + ["log_chlorophyll_lag"]
        enhanced = chlorophyll + ["sst_lag"]
        eligible = panel.dropna(subset=[target, *enhanced])
        train = eligible.loc[eligible.index <= TEST_START - LAG]
        test = eligible.loc[eligible.index >= TEST_START].copy()
        if train.empty or test.empty:
            raise ValueError("Insufficient complete annual rows")
        test["persistence"] = test[baseline[0]]
        for model, columns in [
            ("market_only", baseline),
            ("market_chlorophyll", chlorophyll),
            ("market_chlorophyll_sst", enhanced),
        ]:
            fit = make_pipeline(StandardScaler(), Ridge(alpha=1))
            fit.fit(train[columns], train[target])
            test[model] = fit.predict(test[columns])
        summary = {"train_years": train.index.tolist(), "test_years": test.index.tolist()}
        models = ["persistence", "market_only", "market_chlorophyll", "market_chlorophyll_sst"]
        for model in models:
            error = test[model] - test[target]
            summary[model] = {"mae": float(error.abs().mean()),
                              "rmse": float(np.sqrt(error.pow(2).mean()))}
        results[target] = summary
        predictions.append(test[[target, "feature_year", *models]]
                           .rename(columns={target: "actual"}).assign(target=target))

    pd.concat(predictions).to_csv(DATA / "predictions.csv")
    report = json.dumps(results, indent=2)
    (DATA / "metrics.json").write_text(report + "\n", encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
