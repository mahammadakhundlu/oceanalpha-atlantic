"""Repeat the two-week buyer simulation across price conditions and seeds."""
import argparse
from html import escape
from pathlib import Path

import numpy as np
import pandas as pd

from weekly import satellite_pixels, score, weekly_inputs


def write_chart(summary, output):
    """Draw paired median savings bars for the 5% quote scenario."""
    panel = summary.xs(0.05, level="premium")
    limit = max(abs(panel.market_eur).max(), abs(panel.satellite_eur).max(), 1)
    scale = 300 / limit
    zero = 540
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="930" height="458" viewBox="0 0 930 458">',
        '<rect width="930" height="458" fill="#f0f8f7"/>',
        '<g font-family="Arial,sans-serif" fill="#103342">',
        '<text x="24" y="37" font-size="25" font-weight="bold">Two-week buyer simulation</text>',
        '<text x="24" y="65" font-size="16">Median savings vs waiting · € per 100 kg · 40 runs · 5% quote premium</text>',
        '<text x="24" y="94" font-size="15" fill="#405f75">Blue: market only</text>',
        '<text x="205" y="94" font-size="15" fill="#006b65">Green: market + satellite</text>',
        '<path d="M540 110V423" stroke="#8aada9"/>',
    ]
    for i, (name, row) in enumerate(panel.iterrows()):
        y = 124 + i * 76
        svg.append(f'<text x="24" y="{y + 21}" font-size="16">{escape(name)}</text>')
        for offset, value, color in [(0, row.market_eur, "#405f75"),
                                     (24, row.satellite_eur, "#006b65")]:
            end = zero + value * scale
            x = min(end, zero)
            svg.append(f'<rect x="{x:.1f}" y="{y + offset}" '
                       f'width="{abs(end-zero):.1f}" height="18" fill="{color}"/>')
            anchor = "start" if value >= 0 else "end"
            label_x = end + (6 if value >= 0 else -6)
            svg.append(f'<text x="{label_x:.1f}" y="{y + offset + 14}" '
                       f'text-anchor="{anchor}" font-size="14">€{value:.2f}</text>')
    svg.extend(['<text x="24" y="441" font-size="14">Simulated purchase costs. No real trades.</text>',
                '</g></svg>'])
    output.write_text("\n".join(svg), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--visits", type=Path, help="Optional verified Peniche weekly AIS CSV")
    parser.add_argument("--out", type=Path, default=Path("results"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    inputs = weekly_inputs(satellite_pixels())
    activity = 0
    if args.visits:
        visits = pd.read_csv(args.visits)
        dates = pd.to_datetime(visits.week, utc=True, errors="raise")
        counts = pd.Series(pd.to_numeric(visits.detected_visits).to_numpy(), index=dates)
        if not dates.eq(dates.dt.normalize()).all() or not dates.dt.dayofweek.eq(0).all():
            raise ValueError("Visit dates must be UTC Mondays")
        counts = counts.reindex(inputs.index)
        if counts.isna().any() or not np.isfinite(counts).all() or (
            (counts < 0) | (counts % 1 != 0)
        ).any():
            raise ValueError("Supply verified counts for every simulation week")
        # Activity grounds the generated supply proxy, under an assumed price response.
        activity = -0.15 * np.log((counts + 1) / 10)

    signal = inputs.log_chl.ffill().fillna(np.log(0.35)) - np.log(0.35)
    rows = []
    for scenario, effect, noise in [
        ("No satellite effect", 0, 0.18),
        ("Weak effect", -0.15, 0.18),
        ("Planted effect", -0.45, 0.18),
        ("Planted effect, noisy prices", -0.45, 0.36),
    ]:
        for seed in range(40):
            rng = np.random.default_rng(seed)
            frame = inputs.copy()
            frame["eur_per_kg"] = np.exp(
                0.22 - 0.18 * frame.season_sin + effect * signal + activity
                + rng.normal(0, noise, len(frame))
            )
            frame["last_sales"] = frame.eur_per_kg.shift()
            test, _ = score(frame, "eur_per_kg", horizon=2)
            for premium in [0, 0.05, 0.10]:
                quote = test.last_sales * (1 + premium)
                savings = {}
                for model in ["market_only", "market_satellite"]:
                    cost = test.outcome.where(test[model] <= quote, quote)
                    savings[model] = 100 * (test.outcome - cost).mean()
                rows.append({"scenario": scenario, "seed": seed, "premium": premium,
                             "test_weeks": len(test), **savings,
                             "extra_savings": savings["market_satellite"] - savings["market_only"]})
    runs = pd.DataFrame(rows)
    runs.to_csv(args.out / "buyer_runs.csv", index=False)
    summary = runs.groupby(["scenario", "premium"], sort=False).agg(
        market_eur=("market_only", "median"),
        satellite_eur=("market_satellite", "median"),
        extra_eur=("extra_savings", "median"),
        wins=("extra_savings", lambda x: int((x > 0).sum())),
        worst_extra_eur=("extra_savings", "min"),
    )
    summary.to_csv(args.out / "buyer_summary.csv")
    write_chart(summary, args.out / "buyer_savings.svg")
    print(summary.round(2).to_string())


if __name__ == "__main__":
    main()
