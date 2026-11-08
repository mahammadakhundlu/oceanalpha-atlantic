# OceanAlpha Atlantic

Can satellite-derived ocean signals help predict Portuguese sardine landings and first-sale prices?

Start with one Portuguese Atlantic port and weekly sardine landings. Evaluate first-sale price separately. Compare seasonality and past landings or prices against the same model with lagged satellite chlorophyll-a and sea-surface temperature. Then test what modeled currents and subsurface conditions add. Use chronological backtests and a replay that shows a dated ocean map, a forecast, and the recorded market outcome.

## Data and validation

1. Verify the port, species, units, dates and release timing in a downloadable EUMOFA first-sale export. Use DGRM monthly data if weekly coverage is insufficient.
2. Extract satellite ocean colour and surface temperature over a small, documented coastal region. Add depth-resolved Iberian currents or temperature only after checking product availability at each historical forecast cutoff.
3. Freeze the date split, compare models on identical held-out dates, and report whether the ocean variables improve error. Keep missing sales separate from zero landings.

## Status

This repository contains the original specification. The Portuguese market and Atlantic ocean series still need to be downloaded, validated and joined before a forecast or backtest can be reported.

- [Original HackTheBurgh plan](PROJECT_PLAN.md)
- [EUMOFA weekly series guide](https://eumofa.eu/documents/20178/128560/weekly%20metadata_time%20series.pdf)
- [DGRM monthly statistics](https://www.dgrm.pt/en/estatisticasmensais)
- [Copernicus Atlantic Ocean Colour](https://data.marine.copernicus.eu/product/OCEANCOLOUR_ATL_BGC_L4_MY_009_118)
- [Copernicus Iberian ocean physics](https://data.marine.copernicus.eu/product/IBI_MULTIYEAR_PHY_005_002/description)
