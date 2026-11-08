# Annual Portugal feasibility screen

### Observed annual gross landed value

| Forecast | Mean absolute error |
|---|---:|
| Last eligible annual value | €5.46 million |
| Market-only Ridge | €8.35 million |
| Market + chlorophyll | €8.05 million |
| Market + chlorophyll + surface temperature | €6.07 million |

The two satellite inputs together improved on market-only Ridge, but the last reported annual value still had the lowest error. This comparison uses the same seven national test years as the landings and unit value experiments below.


## Results

Average absolute forecast error across seven held-out years (2018–2024). Lower is better.

| Model | Landings error (tonnes) | Unit value error (€/kg) |
|---|---:|---:|
| Last eligible annual observation | 7,025 | 0.366 |
| Market-only Ridge | 8,612 | 0.592 |
| Market + satellite chlorophyll | 12,847 | 0.645 |
| Market + satellite chlorophyll + surface temperature | 15,171 | 0.702 |

Both satellite variants increased error for both targets. With seven held-out years, one offshore region and nationwide annual targets, this run does not resolve the weekly forecasting question. Quotas, closures, fleet activity and market demand can all affect the targets.

## Reproduce

```bash
python -m pip install -r requirements.txt
python backtest.py
```

The run used Python 3.12. It writes `data/predictions.csv` and `data/metrics.json` from the bundled snapshots. A perturbation check confirmed that changing 2023 and later inputs leaves the 2024 predictors unchanged.

## Source snapshots and timing

- **Eurostat** `fish_ld_main`, Portugal, European sardine (`PIL`), total vessel nationalities, uses and presentations, 2000–2025. Targets are tonnes of product weight and reported annual unit value converted from €/tonne to €/kg. Unit value can include estimates for products not immediately sold. It is broader than a single-port auction price. [Metadata](https://ec.europa.eu/eurostat/cache/metadata/en/fish_ld_esms.htm) · [Exact query](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/fish_ld_main?lang=en&geo=PT&species=PIL&pres=TOTAL&dest_use=TOTAL)
- **NASA Aqua MODIS R2022 Science Quality** monthly satellite chlorophyll-a (mg/m³), sampled from 4 km pixels via NOAA ERDDAP. [Dataset](https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMH1chlamday_R2022SQ.html) · [Exact subset](https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMH1chlamday_R2022SQ.csv?chlor_a%5B(2003-01-16):1:(2024-12-16)%5D%5B(40):12:(38)%5D%5B(-10.5):12:(-9)%5D)
- **NASA/JPL MUR v4.1** monthly satellite-derived sea-surface temperature analysis (°C), sampled from 0.01° pixels via NOAA ERDDAP. [Dataset](https://coastwatch.pfeg.noaa.gov/erddap/griddap/jplMURSST41mday.html) · [Exact subset](https://coastwatch.pfeg.noaa.gov/erddap/griddap/jplMURSST41mday.csv?sst%5B(2003-01-16):1:(2024-12-16)%5D%5B(38):50:(40)%5D%5B(-10.5):50:(-9)%5D)

Snapshots retrieved 8 November 2026. The ocean subsets sample a small rectangle off western Portugal (approximately 38–40°N, 9–10.5°W). Monthly spatial medians are averaged into annual features, requiring all twelve months. The MUR subset has incomplete 2023 coverage, so the 2025 target is excluded from every model for a matched comparison.

For target year Y, the cutoff is 1 January Y and predictors use Y−2, leaving a full intervening year for reporting. Vintage and actual release dates are unverified, so this is a retrospective comparison. The models use the same 12 training years (2005–2016), fixed Ridge alpha 1 and training-only standardization. Training labels exclude 2017 under the same lag assumption. A single rectangle represents local ocean conditions and cannot account for all fishing grounds behind nationwide landings.
