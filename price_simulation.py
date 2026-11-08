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
        test, _ = score(frame, target="eur_per_kg")
        actual_direction = np.sign(test.eur_per_kg - test.last_sales)
        for model in MODELS:
            predicted_direction = np.sign(test[model] - test.last_sales)
            results.append({
                "scenario": scenario, "model": model, "test_weeks": len(test),
                "mae_eur_per_kg": (test[model] - test.eur_per_kg).abs().mean(),
                "direction_accuracy": (
                    None if model == "persistence"
                    else (predicted_direction == actual_direction).mean()
                ),
            })
    results = pd.DataFrame(results)
    results.to_csv(DATA / "weekly_price_simulation_metrics.csv", index=False)
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
