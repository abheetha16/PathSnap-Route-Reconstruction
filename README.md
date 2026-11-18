# Abeetha: Bayesian hyperparameter tuning and HMM/Viterbi decoding

**Stage 3 of 4.**

1. **Tuning:** Optuna TPE runs 20 trials over 8 LightGBM hyperparameters. The objective is 3-fold GroupKFold
   Macro F1 on a 400k-row training sample. The best model is refit on all training rows and compared with the
   untuned one on student_test.
2. **HMM/Viterbi:** the hidden states are each GPS point's candidate arcs. The emission is log(classifier
   probability) minus a Gaussian distance penalty. The transitions are fixed scores from the road graph (same arc,
   successor, two-hop, disconnected), with the penalty relaxed for time gaps. The result is compared against
   classifier-only predictions on all 10 student-test trips.

| File | What it does |
|---|---|
| `pathsnap/hyperparameter_tuning/bayesian_opt.py` | Optuna search, untuned vs tuned comparison, saves `lightgbm_tuned.joblib` |
| `pathsnap/hmm/viterbi.py` | `HMMRouteReconstructor`: topology, emission, transition, Viterbi, backtracking, continuity, polyline |
| `pathsnap/hmm/evaluate_hmm.py` | Classifier-only vs classifier + HMM, per trip |
| `pathsnap/models/train_models.py` | *shared copy (owner: Abheek)*: provides `FEATURE_COLS` and the metric functions |
| `pathsnap/data_processing/loader.py`, `pathsnap/feature_engineering/extractor.py` | *shared copies (owner: Abhay)* |

**Needs:** Abhay's parquet files in `../artifacts/` and the raw `student_test` trips.
**Output:** `../artifacts/trained_models/lightgbm_tuned.joblib`, `results/bayesian_opt_results.json`, `results/tuned_vs_untuned_comparison.csv`, `results/hmm_vs_classifier_comparison.csv`, `results/hmm_evaluation_summary.json`

```bash
pip install -r requirements.txt
python -m pathsnap.hyperparameter_tuning.bayesian_opt
python -m pathsnap.hmm.evaluate_hmm
```
