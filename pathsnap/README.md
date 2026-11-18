# Abhay: Data processing and feature engineering

**Stage 1 of 4.** This stage reads the raw trips, projects coordinates to metres, finds candidate road segments for
every GPS point and computes the 10 features.

| File | What it does |
|---|---|
| `pathsnap/data_processing/loader.py` | `TripData`, `load_trip()`, `project_coordinates()` (WGS-84 metres per degree at the trip's mean latitude) |
| `pathsnap/feature_engineering/extractor.py` | `CandidateExtractor`: STRtree index, ±40 m candidate query, nearest-arc fallback, 10 features, labels from the route |
| `pathsnap/feature_engineering/build_dataset.py` | Runs the extractor over all train and student_test trips |
| `pathsnap/paths.py` | Data and artifact locations |

**Input:** `../../Student folder/{train,student_test}` (or `$PATHSNAP_DATA`)
**Output:** `../artifacts/features_train.parquet`, `../artifacts/features_student_test.parquet`, `../artifacts/results/eda_summary.json`

```bash
pip install -r requirements.txt
python -m pathsnap.feature_engineering.build_dataset
```
