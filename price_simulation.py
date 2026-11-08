"""Test whether satellite features recover a deliberately planted price signal."""
import numpy as np
import pandas as pd

from backtest import DATA
from weekly import MODELS, satellite_pixels, score, simulate, weekly_inputs


def main():
    inputs = weekly_inputs(satellite_pixels())
    results = []
    for scenario, strength in [("No planted price signal", 0), ("Planted price signal", -0.45)]:
        frame = simulate(inputs, strength=0)
        # This hypothetical inverse price effect is a scenario, not an estimate.
        signal = frame.log_chl.ffill().fillna(np.log(0.35)) - np.log(0.35)
        frame["eur_per_kg"] *= np.exp(strength * signal)
        frame["simulated_sales_eur"] = frame.kg * frame.eur_per_kg
        frame["last_sales"] = frame.eur_per_kg.shift(1)
        for horizon in range(1, 5):
            test, _ = score(frame, target="eur_per_kg", horizon=horizon)
            actual_direction = np.sign(test.outcome - test.last_sales)
            supplier_quote = test.last_sales * 1.05
            for model in MODELS:
                predicted_direction = np.sign(test[model] - test.last_sales)
                lock = test[model] > supplier_quote
                cost = test.outcome.where(~lock, supplier_quote)
                results.append({
                    "scenario": scenario, "horizon_weeks": horizon,
                    "model": model, "test_weeks": len(test),
                    "mae_eur_per_kg": (test[model] - test.outcome).abs().mean(),
                    "direction_accuracy": (
                        None if model == "persistence"
                        else (predicted_direction == actual_direction).mean()
                    ),
                    "lock_count": int(lock.sum()),
                    "savings_vs_wait_eur_per_100kg": 100 * (test.outcome - cost).mean(),
                })
    results = pd.DataFrame(results)
    results.to_csv(DATA / "weekly_price_simulation_metrics.csv", index=False)
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
