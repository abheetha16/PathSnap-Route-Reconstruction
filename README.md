# Abhinav: API, UI, visualisation and report

**Stage 4 of 4.** This stage covers the two-laptop deployment and every figure, map and report.

| File | What it does |
|---|---|
| `pathsnap/api/main.py` | FastAPI backend (Laptop 1): `/health`, `/api/trips`, `POST /api/evaluate`, `GET /api/evaluate/{trip_id}`; logs every request |
| `pathsnap/ui/app.py` | Streamlit evaluator UI (Laptop 2): trip dropdown, KPI cards, Folium map |
| `pathsnap/visualizations/generate_plots.py` | CV/test/log-loss bars, confusion matrices, Optuna history, HMM comparison, MLP loss curve |
| `pathsnap/visualizations/folium_maps.py` | Interactive HTML maps for trips 00000000 and 00000040 |
| `pathsnap/visualizations/generate_static_map_view.py` | PNG map for the report |
| `pathsnap/visualizations/generate_deployment_screenshots.py` | Mock-up images of the terminal and UI (not real screenshots) |
| `pathsnap/report/generate_report.py` | Builds the technical report PDF |
| `pathsnap/hmm/viterbi.py`, `models/train_models.py` | *shared copies (owners: Abeetha, Abheek)* |
| `pathsnap/data_processing/loader.py`, `feature_engineering/extractor.py` | *shared copies (owner: Abhay)* |

**Needs:** everything the earlier stages write to `../artifacts/`. The API needs only `trained_models/lightgbm_tuned.joblib` and the raw trips.

```bash
pip install -r requirements.txt
python -m pathsnap.visualizations.generate_plots
python -m pathsnap.visualizations.folium_maps
python -m pathsnap.visualizations.generate_static_map_view
python -m pathsnap.visualizations.generate_deployment_screenshots
python -m pathsnap.report.generate_report

# Laptop 1 (set PATHSNAP_EVAL_DIR to the evaluator trips folder on evaluation day)
python -m uvicorn pathsnap.api.main:app --host 0.0.0.0 --port 8000
# Laptop 2
streamlit run pathsnap/ui/app.py
```

Laptop 2 needs only `pathsnap/ui/app.py`, its requirements, and `../artifacts/results/hmm_vs_classifier_comparison.csv`
for the summary table on the start page.
