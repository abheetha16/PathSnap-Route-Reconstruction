# Abheek: Model training and comparison

**Stage 2 of 4.** This stage trains five model families on (GPS point, candidate arc) pairs, with 5-fold GroupKFold
by trip, and scores them on the 10 student-test trips.

Models: Logistic Regression, KNN, Random Forest, LightGBM, MLP.
Metrics: CV Macro F1, test Macro F1, observation-level Top-1, route continuity, log loss, precision, recall,
confusion matrix and inference time.

| File | What it does |
|---|---|
| `pathsnap/models/train_models.py` | `FEATURE_COLS`, `compute_observation_top1()`, `compute_route_continuity()`, `get_model_definitions()`, `train_and_evaluate_all()` |
| `pathsnap/paths.py` | Data and artifact locations |

**Needs:** Abhay's parquet files in `../artifacts/`, plus the raw `student_test` `.arcs` files for the continuity check.
**Output:** `../artifacts/trained_models/*.joblib` (5 models + scaler), `../artifacts/results/model_comparison.csv`, `detailed_model_metrics.json`

```bash
pip install -r requirements.txt
python -m pathsnap.models.train_models
```
