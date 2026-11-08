# OceanAlpha Atlantic

Can satellite-derived ocean signals help predict Portuguese sardine landings and first-sale prices?

The port-income target is **gross sardine auction receipts** (kilograms sold × euros per kilogram). The prototype tracks sale value before costs. It measures neither port operator fees nor profit.

## Run the replay

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The weekly tab shows a dated satellite chlorophyll grid off Peniche and forecasts the following seven days of **simulated** sardine receipts. Choose a Monday and reveal the simulated quantity, price and receipts. The annual tab reports the separate backtest on real Portuguese national data.

To rebuild the demo, run `python backtest.py` and `python weekly.py` in that order. Both read the bundled snapshots.

### Weekly simulation

The input is a real NASA Aqua MODIS eight-day satellite chlorophyll composite, sampled off Peniche from 2017 through 2024. The timestamp marks the composite centre. The backtest assumes four days to finish the observation window and another fourteen for delivery. Each Monday uses the most recent eligible composite, requiring five valid pixels and skipping model scores when no qualifying composite was available within the prior 32 days. Actual delivery dates have not been verified. [Dataset](https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMH1chla8day_R202SQ.html) · [Exact subset](https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMH1chla8day_R202SQ.csv?chlor_a%5B(2017-01-05):1:(2025-01-05)%5D%5B(39.75):6:(39.0)%5D%5B(-10.5):6:(-9.5)%5D)

Both simulations use the same seasonal patterns and random draws for quantity and price. In one scenario, simulated sales are independent of the satellite measurements given the seasonal inputs. In the other, higher chlorophyll deliberately raises simulated quantity. The planted effect is a test of the pipeline. It does not establish a relationship at Peniche. The models train on weeks before 2 January 2023 and score the same later weeks within each scenario. Previous-week receipts are assumed available at the Monday cutoff.

### Observed annual gross landed value

| Forecast | Mean absolute error |
|---|---:|
| Last eligible annual value | €5.46 million |
| Market-only Ridge | €8.35 million |
| Market + chlorophyll | €8.05 million |
| Market + chlorophyll + surface temperature | €6.07 million |

The two satellite inputs together improved on market-only Ridge, but the last reported annual value still had the lowest error. This comparison uses the same seven national test years as the landings and unit value experiments below.

## Original research target

Start with one Portuguese Atlantic port and weekly sardine landings. Evaluate first-sale price separately. Compare seasonality and past landings or prices against the same model with lagged satellite chlorophyll-a and sea-surface temperature. Then test what modeled currents and subsurface conditions add. Use chronological backtests and a replay that shows a dated ocean map, a forecast, and the recorded market outcome.

## Data and validation

1. Verify the port, species, units, dates and release timing in a downloadable EUMOFA first-sale export. Use DGRM monthly data if weekly coverage is insufficient.
2. Extract satellite ocean colour and surface temperature over a small, documented coastal region. Add depth-resolved Iberian currents or temperature only after checking product availability at each historical forecast cutoff.
3. Freeze the date split, compare models on identical held-out dates, and report whether the ocean variables improve error. Keep missing sales separate from zero landings.

## Status

The first run is an **annual, nationwide feasibility screen** using real Portuguese sardine landings and Atlantic satellite data. The EUMOFA weekly dashboard was reachable, but its bulk download returned an access error and no usable weekly export was obtained. The DGRM page checked exposes a table image. The weekly port-level experiment, currents and subsurface features remain open.

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

## Original weekly plan

- [Original HackTheBurgh plan](PROJECT_PLAN.md)
- [EUMOFA weekly series guide](https://eumofa.eu/documents/20178/128560/weekly%20metadata_time%20series.pdf)
- [DGRM monthly statistics](https://www.dgrm.pt/en/estatisticasmensais)
- [Copernicus Atlantic Ocean Colour](https://data.marine.copernicus.eu/product/OCEANCOLOUR_ATL_BGC_L4_MY_009_118)
- [Copernicus Iberian ocean physics](https://data.marine.copernicus.eu/product/IBI_MULTIYEAR_PHY_005_002/description)
