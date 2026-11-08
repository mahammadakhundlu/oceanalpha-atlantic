"""Compare two-week Peniche port-visit forecasts on a verified weekly AIS export."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from weekly import SPLIT, satellite_pixels, weekly_inputs


def evaluate(visits):
    weeks = pd.to_datetime(visits.week, utc=True, errors="raise")
    counts = pd.to_numeric(visits.detected_visits, errors="raise")
    if weeks.isna().any() or weeks.duplicated().any() or (
        (weeks.dt.dayofweek != 0) | (weeks != weeks.dt.normalize())
    ).any():
        raise ValueError("Use unique Monday UTC week starts")
    if (~np.isfinite(counts) | (counts < 0) | (counts % 1 != 0)).any():
        raise ValueError("Covered weeks must have nonnegative integer visit counts")

    frame = weekly_inputs(satellite_pixels())
    observed = pd.Series(counts.to_numpy(), index=weeks).reindex(frame.index)
    # Leave the preceding week for event completion and reporting.
    frame["last_visits"] = observed.shift(2)
    frame["observed"] = observed.shift(-1)
    market = ["last_visits", "season_sin", "season_cos"]
    eligible = frame.dropna(subset=market + ["log_chl", "observed"])
    train = eligible.loc[eligible.index + pd.Timedelta(weeks=3) <= SPLIT]
    test = eligible.loc[eligible.index >= SPLIT].copy()
    if len(train) < 52 or len(test) < 26:
        raise ValueError(f"Insufficient matched coverage: {len(train)} train, {len(test)} test")

    test["persistence"] = test.last_visits
    for model, features in [
        ("activity_only", market), ("activity_and_satellite", market + ["log_chl"]),
    ]:
        fitted = make_pipeline(StandardScaler(), Ridge(alpha=10))
        fitted.fit(train[features], train.observed)
        test[model] = fitted.predict(test[features]).clip(min=0)
    test["delivery_week"] = test.index + pd.Timedelta(weeks=1)
    columns = ["delivery_week", "observed", "persistence", "activity_only",
               "activity_and_satellite", "time", "available"]
    return test[columns], len(train)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ais_csv", type=Path)
    parser.add_argument("--output", type=Path, default=Path("port_activity_predictions.csv"))
    args = parser.parse_args()
    predictions, n_train = evaluate(pd.read_csv(args.ais_csv))
    print(f"{n_train} training weeks and {len(predictions)} held-out weeks")
    for model in ["persistence", "activity_only", "activity_and_satellite"]:
        error = predictions[model] - predictions.observed
        print(f"{model}: average miss {error.abs().mean():.2f} visits/week")
    predictions.to_csv(args.output, index_label="issue_week")


if __name__ == "__main__":
    main()
