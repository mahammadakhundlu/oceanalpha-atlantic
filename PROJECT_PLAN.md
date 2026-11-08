# OCEANALPHA
## Predicting Atlantic Fish-Market Disruptions from Ocean Signals

**HackTheBurgh 2026 — Team build plan (HRT + G-Research)**  
**Plan prepared:** Saturday, 7 November 2026  
**Official submission:** Sunday, 8 November 2026, 12:00 UK time — verify against the live event schedule  
**Scope:** Research prototype. No real trades; no claim of profitable arbitrage or established causal relationships.

> **30-second pitch:** Fish prices are observed on land, but many forces affecting supply are visible at sea first. OceanAlpha combines historical fish-auction transactions with Atlantic wave, wind, ocean-colour and (optionally) fishing-vessel activity to test whether these underused signals help forecast *where and when fish supply or first-sale prices will change*. The demo travels back to a historical date, hides the future, issues a forecast, and reveals what actually happened.

---

## 0. EXECUTIVE DECISION — READ FIRST

**Do not start by downloading the entire Atlantic.** Start with **one Atlantic-facing market, one species, and one forecast frequency**. Expand only after a usable time-indexed target dataset exists.

**Preferred pilot:** Portuguese Atlantic **sardine (`Sardina pilchardus`) first-sale quantity and unit price**, using **EUMOFA weekly first-sale data** for whichever *specific Portuguese place of sale* has a long, sufficiently complete history. Sardine and Portugal are **candidates**, not an assertion that the required weekly series has already been downloaded or verified. Verify the actual species, port, units, dates and coverage before confirming.

**If sardine/Portugal weekly data are sparse:** choose another well-covered Portuguese/Spanish Atlantic species + place of sale from EUMOFA; alternatively aggregate to a seaboard/country; alternatively switch to monthly data from EUMOFA or Portugal's DGRM. If fewer than ~150 usable weekly observations remain after the join, **do not sell the result as a robust one-port ML price predictor**. Pool across ports/species, change to monthly regional anomaly detection, or forecast supply-disruption *risk* descriptively.

**Primary promise:** A clean historical comparison showing whether **past observed ocean conditions** improve future first-sale **volume forecasts**, versus a seasonal/lagged-sales baseline.  
**Secondary promise:** Evaluate future first-sale **unit-price** forecasts and quantify how much, if anything, the physical signals add.  
**Stretch:** Incorporate AIS-derived apparent fishing effort and estimate when an early signal is most predictive.  
**Not required:** “AI agent”, massive ocean raster datasets, perfect fish population prediction, live trading, or guaranteed 90% accuracy.

### Minimum winning demo (MVP)

1. At least one real historical first-sale time series, correctly dated and unit-labelled.
2. One matching environmental time series (waves/wind); chlorophyll added if possible.
3. A **time-split baseline and enhanced model**, with honestly reported results.
4. One striking visual: a coastal map/time slider showing marine anomalies alongside market outcomes.
5. A **historical replay:** as-of date → forecast → reveal real volume/price → compare with baseline.
6. Clear caveats: correlation is not causation; fish prices also depend on quotas, demand, fleet, seasonality, imports and other forces.

### Two possible product stories

| Approach | Scientific mechanism | Target and lead time | Feasibility |
|---|---|---|---|
| **Storm2Shelf (prioritise)** | Rough seas can reduce fishing activity / landings | Next-week first-sale *volume*, optionally price | **Best MVP**; waves/wind and market data are easier to align |
| **OceanBioAlpha (upgrade)** | Temperature / chlorophyll can relate to habitats, food web and fish availability | Supply anomalies **several weeks** later; perhaps monthly | More aligned with “satellite predicts fish”; harder to prove in one night |

**Recommendation:** Make **OceanAlpha** the product name, with Storm2Shelf as the working first model and ocean-colour as the headline explanatory/ablation layer if the data support it. Do not imply a phytoplankton bloom automatically raises fish abundance one week later.

---

## 1. WHY THESE TWO SPONSORS?

**HRT — Best Use of Data for Predictions & Decision Making**
- Forecast supply/prices with a defined target and decision timestamp.
- Compare against strong historical/seasonal benchmarks; use MAE and out-of-time performance.
- Provide an explicit decision tool: alert a seafood buyer that a chosen species/market has *high predicted supply disruption risk*, with uncertainty and evidence, rather than an investment promise.

**G-Research — Make the Invisible Visible**
- Reveal hidden ocean processes and their *timing* in relation to markets.
- Visualise an observed wave/chlorophyll anomaly over a coastal region, connect it to historical first-sale data, and show feature importance/lag relationships.
- Be memorable: a **time machine** that forecasts a fish market from conditions at sea.

**Metaview / overall-project story, if entered:** Show a fully working, intuitive research tool rather than a model zoo. Don't claim compatibility with any sponsor rubric that hasn't been checked.

---

## 2. RESEARCH QUESTIONS & TESTABLE HYPOTHESES

**RQ1 — Storm exposure:** Does preceding rough sea weather improve **next-week first-sale volume** forecasts over (i) seasonal normal and (ii) prior sales alone?

**RQ2 — Marine biology:** Does lagged chlorophyll-a or sea-surface-temperature *anomaly*, rather than raw level, improve forecasts over ocean/weather + seasonality?

**RQ3 — Price transmission:** Conditional on previous market prices and seasonal factors, do ocean signals help predict **next-week first-sale unit price** or the **sign of its movement**?

**RQ4 — Lead times:** Are signals strongest at 1, 2, 4 or 8 weeks? The lag must be chosen on validation data, not after looking at the test period.

**Null hypothesis:** Ocean features do **not** improve held-out prediction over a properly constructed baseline. A credible null result is a valid research finding: the market may already incorporate these signals or other determinants may dominate.

**Do not confuse:**
- Fish population ≠ satellite chlorophyll ≠ estimated fishing hours ≠ fish landed ≠ fish sold.
- First-sale auction prices ≠ supermarket retail prices.
- Sea-weather *reanalysis* ≠ a forecast that could have been known in advance. Only use ocean information already observable at the prediction cutoff; for predicting future environmental variables, use a truly archived forecast if available.

---

## 3. DATA SOURCES, ACCESS ROUTES & REALITY CHECKS

The links below were checked against public source descriptions on 7 November 2026. **Actual download success, available dates for the selected port/species, and licensing for your chosen use still need verification.**

| Priority | Source | Variables | What is verified | Access / caveat |
|---|---|---|---|---|
| **P0** | [EUMOFA first-sale dashboards](https://fishery-aquaculture-market-observatory.ec.europa.eu/index.php/de/node/51) | Weekly/monthly volume, sales value; derive unit price from value / volume if consistent | European Commission dashboards explicitly include weekly and monthly first sales | Dashboard and [bulk download via EU data portal](https://data.europa.eu/data/datasets/european-market-observatory-for-fisheries-and-aquaculture-products?locale=en); download can involve interactive selection; check date coverage, sales location and release lag |
| **P0 fallback** | [Portugal DGRM monthly fishing statistics](https://www.dgrm.pt/en/estatisticasmensais) | Monthly landings quantity, monthly average price for fresh/chilled fish | DGRM describes monthly national/port-related statistics | May be HTML-linked tables/Excel; verify species and port breakout before using |
| **P1** | [Copernicus global wave reanalysis](https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_WAV_001_032/services) | Significant wave height, periods/direction (check actual variable names) | Product `GLOBAL_MULTIYEAR_WAV_001_032`, dataset `cmems_mod_glo_wav_my_0.2deg_PT3H-i`, historical 3-hourly data from 1980 | Copernicus Marine Toolbox; subset a **tiny** coastal rectangle and time window |
| **P1 quick substitute** | [Open-Meteo Historical Weather](https://open-meteo.com/en/docs/historical-weather-api) | Wind, precipitation, air temperature; ERA5 back to 1940 | Public historical weather endpoint | Not a direct ocean-wave substitute; useful to establish a weather baseline quickly; check free-tier terms and acknowledgement |
| **P2** | [Copernicus Atlantic ocean-colour L4](https://data.marine.copernicus.eu/product/OCEANCOLOUR_ATL_BGC_L4_MY_009_118/services) | Chlorophyll-a / phytoplankton proxies | Atlantic product from 1997; daily and monthly, 1 km products; dataset ID for daily product below | Large grids: use small spatial subset, preferably monthly or coastal aggregate; historical L4 is processed/interpolated and release timeliness matters |
| **P2** | [Copernicus ERA5 single-level daily stats](https://cds.climate.copernicus.eu/datasets/derived-era5-single-levels-daily-statistics?tab=download) | SST, wind, significant wave height | Daily atmospheric/ocean fields, historical; wave grid coarser | Requires CDS setup/terms; avoid if marine-wave subset already works |
| **P3** | [Global Fishing Watch (GFW)](https://globalfishingwatch.org/dataset-and-code-fishing-activity/) | Apparent fishing hours by grid/time | AIS-based apparent fishing activity from 2012 | Requires portal account/token for some services; **not actual catch**, incomplete for smaller vessels; **non-commercial CC BY-NC 4.0** |
| **P3 alternative** | [GFW fixed 2012–2024 dataset](https://zenodo.org/records/14982712) | Static AIS-based fishing effort | Public fixed historical release available | Often huge files; do not block MVP on download |

**Important caution:** EUMOFA first-sale data may include both quantities and *values*, not precomputed price; calculate `unit_price = value_eur / quantity_kg` **only after verifying measurement units and comparable sale definitions**. Do not treat a market with no sale as €0/kg. Some data are aggregated across ports or countries; never invent port-level specificity.

### Market-data intake, first 45 minutes (decisive)

1. Open EUMOFA weekly first-sales; filter **country = Portugal**, **main commercial species = sardine**; inspect available places of sale and time range.
2. Download export CSV/XLSX **for all years available**. If portal export is troublesome, check EU bulk download link. **Assign one person to this immediately.**
3. Print: count of observations, date min/max, unique markets, unique species, missing weeks, units, zero quantities, value/price ranges.
4. Choose the **best coverage**, not necessarily the prettiest species. Target ≥ 150 usable weekly observations for a narrow demo and ideally ≥ 250–400 for model validation; more is better, especially for seasonal analysis.
5. Check whether price and volume refer to exactly the same species, port, aggregation interval and units.
6. **If weekly export isn't usable within 45 minutes**, pivot to monthly DGRM/EUMOFA or change market/species; do not lose the evening fighting an export button.

### Ocean-data extraction strategy

- Work with an illustrative **Portuguese Atlantic coastal box** e.g. latitude **38–42°N**, longitude **−12 to −9°**; this is a *starting engineering region*, **not a scientifically validated fishery footprint**. Refine to the chosen port's relevant fishing grounds once known.
- For a given week aggregate ocean observations to regional mean/median, 90th-percentile wave height, number of rough-sea days and fraction of ocean grid cells above a threshold.
- Never download a full global raster just to calculate three weekly features.
- Save compact, tidy tables; all downstream modeling uses weekly rows rather than NetCDF files.

**Copernicus starter command — schematic; run `copernicusmarine describe` first to check variables/auth/version:**

```bash
pip install copernicusmarine xarray netCDF4
copernicusmarine subset \
  --dataset-id cmems_mod_glo_wav_my_0.2deg_PT3H-i \
  --minimum-longitude -12 --maximum-longitude -9 \
  --minimum-latitude 38 --maximum-latitude 42 \
  --start-datetime '2021-01-01' --end-datetime '2022-01-01'
```

**Ocean-colour candidate dataset:** `cmems_obs-oc_atl_bgc-plankton_my_l4-gapfree-multi-1km_P1D`. Confirm variable names and dataset version using the toolbox; 1 km daily data may be too large. The published **monthly** dataset `cmems_obs-oc_atl_bgc-plankton_my_l4-multi-1km_P1M` may be more practical for a biological pilot.

**Practical shortcut:** 2020–2025 wave/wind **plus the matching first-sale series** is a better MVP than 1997–2026 chlorophyll with no usable fish-market labels.

---

## 4. TIMESTAMP CONTRACT — PREVENT FALSE PREDICTIONS

**Forecast timing for weekly MVP:** At the end of week `t` (e.g. Sunday 23:59 UTC), predict first-sale **quantity in week `t+1`**; price forecast is optional. All inputs must be available as of this decision time.

The dangerous part: **market data are often published with a delay.** If EUMOFA releases week `t` transactions after week `t+1` has started, you CANNOT use week `t` price/volume for a hypothetical Sunday-`t` forecast. Explicitly estimate publication latency. Set a conservative **market observation lag `L`** (e.g. 2–4 weeks, if supported), or show a retrospective *research* forecast and do not claim it was real-time actionable.

**As-of rule:** Every source row must have:
- `observation_start`, `observation_end` — when measurement occurred;
- `published_at` (if verifiable), or a conservative source-specific publication-lag assumption;
- `as_of` — the time the prediction would be issued.

Only use rows with `published_at <= as_of`. Ocean reanalyses may be revised after the fact, making retrospective use **a backtest with hindsight-reprocessed physical observations**, not proof those exact values were available operationally. Be transparent. For a strict real-time-capable variant, limit features to observations known at the cutoff or archived historical *forecasts* issued earlier.

**Never use** week `t+1` wave heights, catches, prices or fishing activity to predict `t+1`; contemporaneous market quantities should not be used to forecast prices in the same week unless a separate quantity forecast supplies them (using only pre-cutoff information).

**Lagged ecological pathway:** For chlorophyll/SST experiments, build lagged/anomaly windows *ending before as-of*; test horizons 2/4/8 weeks or the next month. Marine ecology is not instantaneous.

---

## 5. CANONICAL DATA CONTRACT

One row represents **one market / species / prediction cutoff / forecast horizon**.

```text
country, market_id, market_name, species_id, species_name,
week_start, week_end, forecast_as_of, target_week_start,
first_sale_qty_kg, first_sale_value_eur, unit_price_eur_per_kg,
price_available_at, volume_available_at,
lagged_qty_1, lagged_qty_2, lagged_qty_4,
lagged_price_1, lagged_price_2, lagged_price_4,
season_week_sin, season_week_cos, holiday_flag (optional),
wave_height_mean_lag1, wave_height_p90_lag1,
rough_sea_days_lag1, wind_speed_p90_lag1,
sst_anomaly_lag4 (optional), chl_anomaly_lag4 (optional),
fishing_hours_lag2 (optional),
label_qty_next_week, label_price_next_week,
feature_source_dates_max, missingness_flags
```

**Schema rules**
- Use stable identifiers; market and species names need a mapping, not fuzzy joins silently applied.
- Convert values to euros and quantities to kg **after checking metadata**; use `unit_price = value / qty` only when `qty > 0`.
- Keep zero sales distinct from absent data and protected closures; add a `sale_present` label if relevant.
- All predictors for target week `t+1` are shifted to information available at `as_of`.
- All ocean spatial masks and aggregation rules are fixed before looking at test outcomes.
- Keep an `observed`, `reanalysis`, or `forecast_archive` field for each environmental feature so claims can be precise.
- Keep a `source_log.csv` with original URL, retrieval date, data version and licence/attribution notes.

### Data quality acceptance tests

- `first_sale_qty_kg >= 0`; positive quantity needed for a valid unit price.
- Non-negative physical wave height/chlorophyll; anomalous values reviewed and never silently clipped to improve results.
- Duplicate `(market_id, species_id, week_start)` checked and resolved with documented aggregation.
- Every predictor timestamp passes `feature_known_at <= forecast_as_of` (with publication-lag caveat).
- No feature or scaler fitted on any row from after the model training cutoff.
- Plot number of available weeks by market/species before choosing the pilot.

---

## 6. FEATURE ENGINEERING AND SCIENCE

### A. Market-only baseline features (mandatory)
- Seasonal week-of-year sine/cosine, year trend.
- Most recent **actually available** prices and quantities (not necessarily last week's).
- 4-, 8-, 12-week rolling averages and volatility; use `shift(1)` *and* source publication lags.
- Previous-year same-month or same-week level where coverage allows.
- If pooling across markets/species: market/species identifiers, possibly normalized by each series' seasonal baseline.

### B. Weather/storm features (highest priority)
- Previous 7/14 days' mean and max significant wave height.
- Count of days with significant wave height above a *pre-registered* threshold, e.g. > 3 m; report sensitivity to reasonable alternatives only on validation.
- 90th/95th percentile wind speed; proportion of days with exceptionally high waves relative to local historical monthly climatology.
- `storm_exposure = fraction_of_days_above_local_90th_percentile` is more comparable across ports than a global raw threshold.
- No assumptions that all boats cease fishing at an arbitrary wave height: large and small vessels behave differently.

### C. Ocean-colour / ecosystem features (secondary)
- Chlorophyll-a median, trailing mean and anomaly vs same calendar month historical baseline.
- Sea-surface-temperature anomaly, warming trend and variability.
- Lagged cross-correlations at 2/4/8 weeks (exploratory, not evidence alone).
- Start with the simplest 2–4 features; avoid thousands of pixels and small sample overfitting.

### D. Apparent fishing effort (optional)
- GFW estimated fishing hours in a **predefined regional polygon**, trailing windows and seasonal anomaly.
- AIS receiver changes and coverage may create artificial trend shifts; GFW explicitly warns AIS coverage is incomplete, especially for smaller boats.
- Use as a proxy, not a direct measure of catches or landings; treat licence as non-commercial.

### Mechanisms and confounders

| Hypothesized link | Plausible reason | Major confounder |
|---|---|---|
| Higher waves → lower landings | Vessels may remain in port, reduced catch effort | Fishing quotas, fleet composition, storms shift delivery to other ports |
| Chlorophyll change → later catch change | Ecosystem productivity/habitat can change | Species life history, trophic delay, currents, seasonal co-movement |
| Lower supply → higher auction unit price | Short-run scarcity can raise first-sale prices | Demand, substitution/imports, fish size/quality, seasonality |

**Never present SHAP values, lag correlation or model fit as proof of causal effect.**

---

## 7. MODELS — BUILD IN THIS ORDER

**M0: Seasonal naive.** Forecast next week with the median for similar calendar weeks from preceding years, with fallback to last observed quantity/price. This is your minimum bar.

**M1: Market-only regression.** Ridge/ElasticNet or `HistGradientBoostingRegressor` using lagged market features and seasonality. This tests whether simply predicting from market history is already enough.

**M2: Market + storm.** LightGBM regressor with market history + wind/wave features. Main experimental comparison: **M2 vs M1** on unseen later dates.

**M3: Market + storm + bio.** Add lagged chlorophyll/SST features if usable. Main novelty test: **M3 vs M2**. Keep only if it helps consistently.

**M4 optional:** Add GFW effort, time-lagged and coverage-adjusted. No full ocean-model neural network needed.

### Recommended targets

**Primary:** `log1p(next_week_quantity_kg)` or next week's percentage deviation from seasonal typical quantity; transform predictions back carefully.  
**Secondary:** `log(next_week_unit_price_eur_per_kg)` for positive-price weeks, or direction `price_up_next_week` defined in advance.  
**Alternative:** binary risk `supply_drop_gt_20pct_relative_to_seasonal_baseline` for a readable alert **only if enough positive cases exist**.

**Important:** When predicting price, do not train using actual quantity from the same future week. You may chain a quantity *prediction* into a price model, but train that chain using **out-of-fold historical quantity forecasts**, not ground truth future volume.

### Train / validate / test

Use chronological cuts based on **available observations**, not arbitrary promises about data coverage:

1. Earliest ~60% = train; next ~20% = validation; final ~20% = sealed test.
2. Require at least one complete annual cycle in training; preferably several years. If fewer than 3 years exist, report exploratory results, not strong claims.
3. Use **expanding-window backtesting** within development data (e.g. retrain quarterly, predict subsequent 4 weeks), with a gap where necessary for target horizon/publication lags.
4. Freeze target, window, model selection and feature list before touching test data.
5. Report per-port/species sample sizes; for pooled data, avoid target leakage from series aggregates computed using future rows.
6. Track all experiments to avoid cherry-picking one lucky lead time.

### Metrics that matter

- **Volume:** MAE, RMSE, WAPE (only when denominators make sense), relative MAE vs seasonal baseline, and 95% interval coverage where available.
- **Price:** MAE in €/kg, MAE for price direction if classification is used, and change in MAE vs market-only model.
- **Risk classification (optional):** precision, recall, F1, PR-AUC and calibration, particularly if a drop is rare; don't report plain accuracy alone.
- **Uncertainty:** Bootstrap forecast-error intervals by **contiguous time blocks** or multiple walk-forward folds. If improvements are noisy or overlapping, say so.
- **Ablation:** `market-only` vs `+weather` vs `+chlorophyll` vs `+GFW`. This is the HRT/G-Research headline.

**Claim template:** “On a held-out [dates] test set of [N] observations, adding lagged [feature group] reduced forecast MAE from [A] to [B] ([X]%). This is a retrospective association, not evidence the signal was operationally available at this frequency.” Only fill real numbers.

---

## 8. DEMO — THE “ATLANTIC TIME MACHINE”

**Single page built with Streamlit + Plotly** (or a small web frontend if someone already has one).

1. **Hero:** “Can the Atlantic predict tomorrow's fish market?” Subtitle: “Historical first-sale prices, ocean state and honest forecasts.”
2. **Map:** Coastal Portugal/Atlantic with region bounding box; select a market and species. Show a visual heatmap for an actual selected historical ocean variable. For missing raw-map integration, show a sourced environmental time-series panel, not fabricated animation.
3. **Historical date slider:** Choose a date **inside held-out history**. Show only data observable before that cutoff; label retrospective reanalysis distinctly.
4. **Forecast card:** Next-week quantity / price estimate, seasonal normal, model uncertainty, and a simple descriptive “risk of lower-than-normal landings” indicator.
5. **Hidden signal panel:** Plot storm severity, chlorophyll anomalies and following sales against time. Show which features the model uses; do not call them causal explanations.
6. **Reveal the future:** Button reveals actual later sale quantity/price, forecast error, and baseline error for this date.
7. **Research scoreboard:** Out-of-time MAE for baseline/M1/M2/M3 and errors by season. If enhancements failed, show that transparently.
8. **Decision:** Fictional seafood buyer receives a research-only early-warning alert: “Consider checking supply/alternative suppliers,” not an executable trading instruction.

### Suggested 3-minute judge script

**0:00–0:25 — Hook.** “Fishermen work at sea, fish prices appear at auctions. We asked whether the ocean reveals supply disruptions before those auctions.”

**0:25–1:05 — Hidden data.** Show real historical waves/chlorophyll and source acknowledgements; say what each variable is and **what it is not**.

**1:05–1:50 — Time machine.** Select a historical week, hide actual sales, show predictions, reveal outcome.

**1:50–2:30 — Evidence.** Point to test-set model-vs-baseline table and ablation. Clearly state whether bio features really improved predictions.

**2:30–3:00 — Decision + limitations.** Show an alert for buyer risk planning, acknowledge quotas, seasonality, market-release delays and non-causal inference.

### Visual polish priorities
- Ocean map / satellite colour palette, large legible price/volume numbers, a dramatic “reveal future” button.
- Source stamps on every chart; badge dates in UTC; no synthetic figures labelled as actual.
- Loading/missing-data states: never silently display placeholders as model outputs.

---

## 9. TEAM ROLES (ASSUMING FOUR PEOPLE)

| Person | Ownership | First deliverable | End deliverable |
|---|---|---|---|
| **A — Market data lead** | EUMOFA/DGRM downloads, metadata, species/port selection | Real `market_weekly.csv` with units and coverage report | Versioned cleaned series, publication-lag notes |
| **B — Ocean lead** | Copernicus wave/wind, chlorophyll later, spatial masks | One `ocean_weekly.csv` joined to the selected coast | Map/plots and precise dataset provenance |
| **C — Modelling/evaluation** | Baselines, LightGBM, splits, timestamp safety, metrics | M0 baseline; backtest interface | Ablation report + sealed test |
| **D — Demo/integration** | Streamlit app, plotting, presentation, merges | Running app with real/placeholder schema | Time-machine demo, slides, submission |

**If only 3 people:** A manages market + ocean acquisition; B models; C app/presentation.  
**If 2 people:** One data + model, one app + evaluation; cut chlorophyll/GFW immediately.

**Rule:** Data/market schema agreed before parallel work. Every teammate owns a separate directory; use branches/PRs or disciplined small merges. Nobody runs expensive ocean downloads on all of the Atlantic without approval.

### Repository skeleton

```text
oceanalpha/
├── README.md
├── PROJECT_PLAN.md
├── requirements.txt
├── config.yaml               # chosen species/market, region, lag, dates
├── data/
│   ├── raw/                  # gitignored downloads
│   ├── processed/
│   │   ├── market_weekly.csv
│   │   ├── ocean_weekly.csv
│   │   └── joined.parquet
│   └── source_log.csv
├── src/
│   ├── market.py             # unit cleanup, harmonise species + place of sale
│   ├── ocean.py              # Copernicus subset -> weekly aggregates
│   ├── features.py           # as-of lags and anomaly features
│   ├── train.py              # chronological baseline and LightGBM
│   ├── evaluate.py           # metrics, tables, ablations, leak checks
│   └── inference.py          # frozen historical predictions
├── tests/
│   ├── test_asof.py
│   ├── test_units.py
│   └── test_no_future.py
├── artifacts/
│   ├── predictions.csv
│   └── metrics.json
├── app/
│   └── streamlit_app.py
└── slides/
    └── pitch_outline.md
```

### Lean dependencies

```text
pandas
numpy
pyarrow
scikit-learn
lightgbm
plotly
streamlit
requests
xarray
netCDF4
copernicusmarine
pytest
```

`duckdb`, `geopandas`, `shap` are optional. Install only if they directly enable a needed feature and work on the team's machines.

---

## 10. IMPLEMENTATION SPEC AND ACCEPTANCE TESTS

### `market.py`
- Export EUMOFA dataset manually first if needed; record the export URL/date.
- Parse locale-sensitive numbers (`1.234,56` vs `1,234.56`) and date formats correctly.
- Normalize columns to `week_start`, `species_id`, `market_id`, `quantity_kg`, `value_eur`, `unit_price_eur_kg`.
- Print `coverage_report.md`: record count, date range, gaps, duplicate keys, available species/places.
- **Done:** clean chronological market CSV for ≥1 series; raw original preserved, licensing checked.

### `ocean.py`
- Verify Copernicus toolbox account, dataset version, exact variable names.
- Subset one small region and a limited historical period; transform 3-hourly ocean waves into daily and weekly summary features.
- Add weekly SST or chlorophyll where practical. Save aggregated CSV, not raw raster in Git.
- **Done:** ≥80% date overlap with selected market period, with units and spatial coverage documented.

### `features.py`
- Construct temporal keys from week boundaries; explicitly encode publication lag.
- Shift rolling and lagged market and ocean features; choose target horizon.
- Test with a random date `d`: no predictor comes from after `d` or a later publication date.
- **Done:** feature contract plus deterministic reproducible join.

### `train.py` + `evaluate.py`
- Set seasonal naive baseline; calculate MAE before installing complex libraries.
- Fit M1 market-only; then M2 market+weather; M3 market+bio only if available.
- Save out-of-sample **per-row** predictions including timestamps, so dashboard never needs to refit live.
- Freeze split/config before final test; log every variant.
- **Done:** actual-versus-predicted time series, baseline comparison, metrics.json, error analysis.

### `app/streamlit_app.py`
- Read frozen `predictions.csv` and geo/ocean summaries.
- Show historical date selection, forecast and **reveal** outcome, plus aggregate results.
- Gracefully handle data gaps; don't pretend that maps represent a different date/species.
- **Done:** reliable local demo without API calls during the pitch.

### Critical tests

```python
# Pseudocode — actual columns depend on chosen schema.
assert (df['feature_source_dates_max'] <= df['forecast_as_of']).all()
assert df.groupby(['market_id','species_id','week_start']).size().max() == 1
assert (df.loc[df['first_sale_qty_kg'] > 0, 'unit_price_eur_per_kg'] > 0).all()
assert train['forecast_as_of'].max() < test['forecast_as_of'].min()
# Recalculate a sample of lagged features using ONLY observations available at as_of.
```

**Scientific red line:** If the model performs extraordinarily well (e.g. near-perfect price accuracy), suspect leakage (future sales, future waves, duplicated lagged labels, using data-processing revisions) before celebrating.

---

## 11. CLOCK — SATURDAY 17:00 TO SUNDAY 12:00

This is a proposed schedule, not a claim that work has already started. Times are UK local.

| Time | Gate | Deliverable / decision |
|---|---|---|
| **17:00–17:45** | **Gate 0 — Market dataset** | Download EUMOFA weekly export; identify best country × port × species. If not possible, move to DGRM monthly or alternate market. |
| **17:45–18:30** | **Gate 1 — Real join** | Market CSV + wave/wind CSV for a small region; join by as-of week and inspect coverage. |
| **18:30–20:00** | **Gate 2 — Baseline** | Seasonal naive, market-only baseline, date split, MAE. If no credible label history, switch target or stop pivot. |
| **20:00–22:00** | **Gate 3 — First research finding** | Add weather, compute leak-safe M1 vs M2; one error plot and ablation. Decide whether waves add value. |
| **22:00–00:00** | **Gate 4 — Product** | Streamlit time machine and reveal; use frozen predictions. Ocean lead tests chlorophyll as optional. |
| **00:00–02:00** | Upgrade or trim | Chlorophyll/SST with lagged anomaly, or add another port/species to increase observations. Stop if no improvement. |
| **02:00–05:00** | Quality | Rerun checks, troubleshoot UI/data issues, implement uncertainty/decision panel; stagger rest if possible. |
| **05:00–07:30** | Freeze candidate | Choose the single defensible model and target, prepare provenance, source attributions and benchmark charts. |
| **07:30–09:30** | **Final evaluation** | Lock code/config; run held-out test once; prepare truthful conclusion whether positive or negative. |
| **09:30–10:45** | Demo rehearsal | 3-minute story + screenshots fallback + README + pitch. Test offline/local start. |
| **10:45–11:30** | Upload & verify | Submit early, confirm repository and presentation open; no late critical features. |
| **12:00 Sunday** | **Event deadline** | Do not plan on needing the final 30 minutes. |

**Hard stop rules:**
- If EUMOFA access takes >45 minutes with no usable historical export, use another public species/market dataset or DGRM monthly.
- If ocean download takes >45 minutes, use Open-Meteo historical wind plus a small Copernicus-derived sample; disclose that the baseline lacks satellite chlorophyll.
- If M2 doesn't beat M1 on validation, demonstrate **lack of added skill** or investigate another defensible physical signal. Do not keep tuning until test performance looks good.
- If no coherent model exists by 22:00, prioritize a real interactive exploratory “Ocean-to-Market Observatory” with statistical associations, **not fabricated predictive claims**.
- No extra model family after 05:00. No major infrastructure rewrites on Sunday morning.

---

## 12. FALLBACK DECISION TREE

**A. Weekly market labels exist and align with ocean data** → build next-week volume forecasting; price as secondary.

**B. Weekly prices exist but volumes are sparse** → forecast price *changes* with historical price + weather; call volume mechanism unverified.

**C. Monthly volume and value exist only** → switch to a 1-month forecast; use monthly ocean SST/chlorophyll, less emphasis on storms; pool multiple ports or species to obtain enough rows.

**D. EUMOFA bulk export fails but Portugal DGRM usable** → show “Portugal fish-market risk forecast”, using whatever country/species aggregation is actually available.

**E. Ocean features don't improve test predictions** → make the central finding “Ocean conditions explain less than seasonality/market history in this sample”; show benchmark, limitations, and a decision aid warning about forecast uncertainty.

**F. Everything is too sparse** → choose **Storm2Port**: forecast fishing-operation disruption probability from marine weather and observed fishing effort, without claiming price forecasts. Requires an appropriate historical target/label; otherwise present it strictly as a risk indicator, not a validated prediction.

---

## 13. WHAT TO CUT, EVEN IF IT SOUNDS IMPRESSIVE

**Never make these critical-path requirements:** a deep neural network on satellite images; large satellite data downloads; full Atlantic map; all fish species; agentic automatic trading; simultaneous multi-market optimization; real-time vessel scraping; causal inference claims; sophisticated Bayesian models; ten hypothesis tests and cherry-picked graphs.

**What will win more points:** strong data provenance, a surprising real example, a transparent baseline, a reproducible history replay, a clean uncertainty-aware decision and a polished demo.

---

## 14. EVALUATION / JUDGING CHECKLIST

### HRT
- [ ] A specific decision timestamp and a specific forecast target.
- [ ] Meaningful forecast horizon and sample count.
- [ ] Appropriate seasonal/market baseline; actual out-of-time model-vs-baseline comparison.
- [ ] Explicit units and metrics; uncertainty and risk explained.
- [ ] Leak-free feature timestamps and publication-lag discussion.
- [ ] Useful downstream decision made from the forecast (even if research-only).

### G-Research
- [ ] Unexpected relationship made visually accessible.
- [ ] Maps and historical charts show **real** data and source attribution.
- [ ] Interactive reveal: ocean conditions → predicted market movement → actual later movement.
- [ ] A concrete discovery (including a credible null result if that's what happened).
- [ ] Clear caveats about fishing ecology, AIS bias and observational inference.

### General / Metaview-style overall prize
- [ ] Live demo works with no network.
- [ ] One-sentence explanation understandable without knowing ML or marine biology.
- [ ] Source code, README, method and reproducibility instructions.
- [ ] Screenshots/video fallback for demo failures.
- [ ] A polished “why this matters” scenario.

---

## 15. RISKS AND SCIENTIFIC DEFENCES

| Risk | Likely damage | Mitigation |
|---|---|---|
| Not enough weekly observations per species/port | Model fits noise | Pool ports/species or use monthly; report counts |
| Historical first-sale records released late | Impossible real-time backtest | Track publication lag, shift inputs, describe retrospective constraints |
| Satellite/reanalysis data retrospectively revised | Artificially optimistic operational claims | Label reanalysis, use only dates <= as-of, distinguish from forecast archive |
| Biological response not immediate | Chlorophyll doesn't help weekly targets | Use longer ecological lags, monthly target or drop bio |
| Ocean area unrelated to fishing grounds | Spurious results | Fix a geographically justified region; sensitivity on validation only |
| Quotas, holidays, imports, fish size alter prices | Ocean features weak | Include time/season baseline and limitations; avoid causality |
| Market unit or fish-name mismatches | Nonsensical unit-price result | Inspect metadata, explicit mapping, unit tests |
| Regressions exploit seasonality | Fake discovery | Use seasonality-aware M1 and seasonal-anomaly features |
| Multiple lead-time tests and hyperparameters | Selection bias | Log trials, seal final test, limit search |
| Small AIS vessels untracked | Wrong fishing-effort signal | Use GFW only as an optional proxy, cite coverage limits |
| Raw grids/large downloads | Time wasted | Coastal subset, aggregate and cache |
| Data rights and portal friction | Submission risk | Observe source licences, attribution; don't redistribute restricted raw data |

---

## 16. SOURCES AND PROVENANCE TO INCLUDE IN README

**Market**
1. European Commission / EUMOFA, [First-sale dashboards](https://fishery-aquaculture-market-observatory.ec.europa.eu/index.php/de/node/51), [EU data portal bulk dataset listing](https://data.europa.eu/data/datasets/european-market-observatory-for-fisheries-and-aquaculture-products?locale=en). Weekly and monthly first-sale volume/value series exist, but **port/species/time coverage must be checked in exported data**.
2. Portugal DGRM, [Monthly Fishing Statistics](https://www.dgrm.pt/en/estatisticasmensais). Monthly quantity and mean-price reporting, with its own species/geographic reporting scope.

**Physical environment**
3. Copernicus Marine, [Global Ocean Waves Reanalysis `GLOBAL_MULTIYEAR_WAV_001_032`](https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_WAV_001_032/services), dataset `cmems_mod_glo_wav_my_0.2deg_PT3H-i`.
4. Copernicus Marine, [Atlantic Ocean Colour `OCEANCOLOUR_ATL_BGC_L4_MY_009_118`](https://data.marine.copernicus.eu/product/OCEANCOLOUR_ATL_BGC_L4_MY_009_118/services), e.g. daily `cmems_obs-oc_atl_bgc-plankton_my_l4-gapfree-multi-1km_P1D`.
5. Copernicus Marine, [Toolbox subset usage](https://help.marine.copernicus.eu/en/articles/8283072-copernicus-marine-toolbox-api-subset).
6. ECMWF / Copernicus Climate Data Store, [ERA5 daily statistics](https://cds.climate.copernicus.eu/datasets/derived-era5-single-levels-daily-statistics?tab=download).
7. Open-Meteo, [Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api), subject to API use conditions.

**Fishing activity**
8. Global Fishing Watch, [Apparent Fishing Activity](https://globalfishingwatch.org/dataset-and-code-fishing-activity/), AIS-based estimates since 2012; non-commercial licence and coverage limitations.
9. Global Fishing Watch, [2025 fixed historical effort archive on Zenodo](https://zenodo.org/records/14982712).

**Must credit in the README:** dataset owner, exact product/dataset ID, spatial and temporal extent, retrieval date, date/version metadata, transformations, data gaps and licence. If a portal offers only an image preview but not a usable export, do **not** cite the preview as if it were raw training data.

---

## 17. QUICK START: FIRST THREE COMMANDS AFTER DATA ACQUISITION

Once the team has manually obtained its actual market CSV and downloaded a small ocean subset:

```bash
# 1. Put original exports in data/raw/ and inspect columns/units carefully.
python -m src.market --input data/raw/first_sales.csv --report

# 2. Aggregate the chosen coastal ocean data to weekly features.
python -m src.ocean --input data/raw/waves.nc --weekly

# 3. Build strictly historical features, then run benchmark and ablation.
python -m src.features --market data/processed/market_weekly.csv --ocean data/processed/ocean_weekly.csv
python -m src.train --experiment market_only
python -m src.train --experiment market_plus_storm
streamlit run app/streamlit_app.py
```

**These commands are a proposed interface, not existing scripts.** Implement them or update the README to the interface the team actually built.

---

## FINAL RULE

**A small, well-validated fish-market prediction from one real ocean region is a stronger HRT + G-Research entry than a giant, unvalidated “AI predicts all Atlantic fish prices” claim.**

The make-or-break question for the first hour is not “Which neural network?” It is **“Can we get a clean, timestamped fish-market series and link it to an earlier ocean signal?”** Answer that first, then build everything else around the evidence.
