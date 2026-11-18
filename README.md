# PathSnap: Distributed Map-Matching & Route Reconstruction

![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=FastAPI&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.33+-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)
![LightGBM](https://img.shields.io/badge/Model-LightGBM-blue.svg)
![Optuna](https://img.shields.io/badge/Tuning-Optuna-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)

**Course:** UE24CS352A – Machine Learning  
**Institution:** Department of Computer Science and Engineering, RR Campus, PES University

---

## 1. Project Overview

PathSnap is an end-to-end distributed machine learning system designed to reconstruct realistic vehicle trajectories from noisy GPS observations by matching observations to a directed road network.

GPS tracking systems frequently suffer from multipath distortions, urban canyon reflections, signal attenuation and low sampling frequencies. These issues cause observed trajectories to deviate from actual road geometry.

PathSnap addresses these challenges through:

1. **Geospatial Processing:** Geodesic metric projection to eliminate angular coordinate distortion.
2. **Spatial Indexing:** STRtree-based spatial candidate generation.
3. **Feature Engineering:** Extraction of spatial and kinematic features for road-segment classification.
4. **Machine Learning:** Training and comparison of five different model families.
5. **Bayesian Optimization:** Optuna-based hyperparameter optimization using the TPE sampler.
6. **HMM and Viterbi:** Topology-aware sequence decoding for continuous route reconstruction.
7. **Distributed Deployment:** FastAPI backend and Streamlit evaluator interface running across two laptops.

## 2. Repository Structure

The repository is organised into two main directories: the `pathsnap/` application source folder and the separate `datasets/` folder.

```text
PathSnap-Route-Reconstruction/
│
├── pathsnap/                            # Main project source code
│   │
│   ├── data_processing/
│   │   ├── __init__.py
│   │   └── loader.py                    # Data ingestion, coordinate projection and trip loading
│   │
│   ├── feature_engineering/
│   │   ├── __init__.py
│   │   ├── extractor.py                 # Candidate generation and feature extraction
│   │   └── build_dataset.py             # Feature dataset generation
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── train_models.py              # Model training, cross-validation and evaluation
│   │
│   ├── hyperparameter_tuning/
│   │   ├── __init__.py
│   │   └── bayesian_opt.py              # Optuna Bayesian optimization
│   │
│   ├── hmm/
│   │   ├── __init__.py
│   │   ├── viterbi.py                   # HMM transition/emission scoring and Viterbi decoding
│   │   └── evaluate_hmm.py              # Classifier vs HMM evaluation
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py                      # FastAPI backend and evaluation endpoints
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   └── app.py                       # Streamlit evaluator interface
│   │
│   ├── visualizations/
│   │   ├── __init__.py
│   │   ├── folium_maps.py               # Interactive Folium map generation
│   │   ├── generate_plots.py            # Model comparison and evaluation plots
│   │   └── generate_deployment_screenshots.py
│   │
│   ├── artifacts/
│   │   ├── trained_models/              # Saved model weights and scalers
│   │   ├── results/                     # CSV and JSON evaluation results
│   │   ├── figures/                     # Generated plots and figures
│   │   └── maps/                        # Interactive Folium HTML maps
│   │
│   └── report/
│       ├── generate_report.py
│       └── PathSnap_Technical_Report.pdf
│
├── datasets/                            # Separate dataset directory
│   ├── training/                        # Training trips
│   ├── student_testing/                  # Student-testing trips
│   └── evaluator_testing/                # Evaluator-testing data, if permitted
│
├── requirements.txt                     # Python dependencies
├── README.md                            # Project documentation
└── .gitignore                            # Git ignored files
```

*Note: The tree documents the intended organisation. Retain the actual filenames and subfolder names present in the project ZIP. Do not add empty or nonexistent directories just to match this example.*

## 3. Dataset Description

The dataset consists of GPS trajectories and their corresponding road network information.

Each trip package contains:

| File | Description |
|---|---|
| `.track` | GPS coordinates: longitude, latitude and timestamp |
| `.nodes` | Road network vertices |
| `.arcs` | Directed road edges |
| `.route` | Ground-truth sequence of traversed arc IDs |

The dataset is divided into:

- 80 training trips
- 10 student-testing trips
- 10 evaluator-testing trips

Evaluator-only ground truth must remain protected and must not be exposed through the client-side inference pipeline.

## 4. Feature Engineering

For each GPS observation, candidate road segments are extracted within a 40-metre search radius.

The system computes ten spatial and kinematic features:

1. `dist_to_seg` – Perpendicular distance to the road segment.
2. `heading_diff` – Difference between GPS heading and road orientation.
3. `sin_hdiff` – Sine of heading difference.
4. `cos_hdiff` – Cosine of heading difference.
5. `speed` – Instantaneous vehicle speed.
6. `u_proj` – Projection fraction along the segment.
7. `arc_len` – Length of the candidate road segment.
8. `dist_to_start` – Distance to segment starting point.
9. `dist_to_end` – Distance to segment ending point.
10. `dt` – GPS sampling interval.

## 5. Machine Learning Models

Five different model families were trained and compared:

| Model | Algorithm Family |
|---|---|
| Logistic Regression | Linear and probabilistic |
| K-Nearest Neighbors | Instance-based |
| Random Forest | Ensemble learning |
| LightGBM | Gradient boosting |
| Multi-Layer Perceptron | Neural networks |

Models were evaluated using 5-Fold GroupKFold cross-validation, grouped by trip ID to avoid cross-trip data leakage.

## 6. Experimental Results

### Model Comparison

| Model | CV Macro F1 | Top-1 Accuracy | Student-Test Macro F1 | Log Loss |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.7501 | 76.32% | 0.7501 | 0.2766 |
| KNN | 0.8208 | 76.14% | 0.8452 | 0.1956 |
| Random Forest | 0.8286 | 80.05% | 0.8342 | 0.1803 |
| LightGBM | 0.8381 | 80.44% | 0.8478 | 0.1526 |
| MLP | 0.8495 | 79.85% | 0.8703 | 0.1170 |

### Bayesian Hyperparameter Optimization

Optuna's Tree-structured Parzen Estimator (TPE) sampler was used to optimise LightGBM over 20 trials.

**Best configuration:**

- `num_leaves = 18`
- `max_depth = 7`
- `learning_rate = 0.1075`
- `n_estimators = 150`
- `min_child_samples = 120`
- `subsample = 0.734`
- `colsample_bytree = 0.670`
- `scale_pos_weight = 2.082`

**Improvement after optimization:**

| Metric | Before | After |
|---|---:|---:|
| CV Macro F1 | 0.8381 | 0.8561 |
| Student-Test Macro F1 | 0.8478 | 0.8663 |
| Log Loss | 0.1526 | 0.1258 |

### HMM and Viterbi Route Reconstruction

A topology-aware Hidden Markov Model was implemented to improve route continuity and observation accuracy.

The Viterbi algorithm finds the most probable sequence of road segments using:

- Candidate road segments as hidden states.
- Classifier predictions and GPS distances for emission probabilities.
- Road network connectivity for transition probabilities.
- Dynamic programming for optimal sequence decoding.

| Metric | Classifier Only | Classifier + HMM |
|---|---:|---:|
| Mean Top-1 Accuracy | 82.67% | 88.70% |
| Mean Route Continuity | 89.68% | 98.14% |

## 7. Installation and Setup

### Prerequisites

- Python 3.10 or above
- Git
- pip
- VS Code or another Python IDE

### Clone the repository

```bash
git clone https://github.com/abheetha16/PathSnap-Route-Reconstruction.git

cd PathSnap-Route-Reconstruction
```

### Install dependencies

```bash
python -m venv venv
```

Activate the environment:

**Windows CMD:**

```cmd
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

Install the required packages:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 8. Execution Guide

Run the following commands from the repository root.

### Step 1: Feature Extraction and Dataset Generation

```bash
python -m pathsnap.feature_engineering.build_dataset
```

### Step 2: Model Training and Evaluation

```bash
python -m pathsnap.models.train_models
```

### Step 3: Bayesian Hyperparameter Optimization

```bash
python -m pathsnap.hyperparameter_tuning.bayesian_opt
```

### Step 4: HMM and Viterbi Evaluation

```bash
python -m pathsnap.hmm.evaluate_hmm
```

### Step 5: Generate Visualizations

```bash
python -m pathsnap.visualizations.generate_plots
```

Generate interactive Folium maps:

```bash
python -m pathsnap.visualizations.folium_maps
```

*Run these commands according to the actual module entry points and configuration in the repository.*

## 9. API and UI Deployment

PathSnap uses a distributed two-laptop architecture.

### Architecture

**Laptop 1 – Backend and Model Inference**

- Hosts the trained LightGBM model.
- Executes candidate extraction and HMM Viterbi decoding.
- Hosts the FastAPI application.
- Processes route reconstruction and evaluation requests.

**Laptop 2 – Evaluator Interface**

- Hosts the Streamlit application.
- Allows evaluators to select testing trips.
- Sends requests to the backend.
- Displays evaluation metrics and interactive Folium maps.

### Start the Backend

On Laptop 1, run:

```bash
python -m uvicorn pathsnap.api.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:

```text
http://localhost:8000
```

### Start the Streamlit UI

On Laptop 2, run:

```bash
streamlit run pathsnap/ui/app.py
```

Configure the backend API URL in the Streamlit interface.

For example:

```text
http://192.168.1.10:8000
```

Replace the IP address with Laptop 1's actual local network IP address.

### Evaluation Workflow

1. Start the FastAPI backend.
2. Start the Streamlit evaluator interface.
3. Select an evaluation trip.
4. Trigger route reconstruction.
5. View the reconstructed route and evaluation metrics.
6. Inspect the interactive Folium map.

## 10. Visualizations and Supporting Results

The project includes visualizations and supporting experimental outputs:

- Exploratory data analysis plots.
- Candidate distance and heading distributions.
- Model comparison charts.
- Confusion matrices.
- Training loss curves.
- Bayesian optimization trial progression.
- Classifier-only versus HMM evaluation charts.
- Interactive Folium route maps.
- Evaluation CSV and JSON files.

Generated outputs are organised under:

```text
pathsnap/artifacts/
├── trained_models/
├── results/
├── figures/
└── maps/
```

## 11. GitHub and Contribution

The repository contains the source code, model training and evaluation scripts, supporting configurations, documentation and permitted experimental artifacts.

To contribute changes, create a separate development branch:

```bash
git switch -c dev-yourname
```

Stage and commit your changes:

```bash
git add .
git commit -m "Describe your changes"
```

Push your branch:

```bash
git push -u origin dev-yourname
```

Create a Pull Request to merge your changes into `main`.

## 12. Important Repository Notes

- Do not commit API keys, passwords, private credentials or `.env` files.
- Do not commit virtual environments such as `venv/` or `.venv/`.
- Include the source code used to generate trained models and evaluation results.
- Include saved model weights and required configuration files, subject to repository size constraints.
- Use Git LFS or an appropriate external storage solution for large files when necessary.
- Do not expose protected evaluator ground-truth data.
- Ensure that the README commands and dependencies match the actual implementation.

## 13. Academic Integrity and Reproducibility

All reported metrics should correspond to actual model executions and reproducible evaluation outputs.

The project separates training and testing workflows and uses trip-level GroupKFold validation to reduce data leakage.

The evaluator interface communicates with the backend for route reconstruction and evaluation.

---

**PathSnap – Distributed Map-Matching & Route Reconstruction**

UE24CS352A – Machine Learning  
Department of Computer Science and Engineering  
PES University, RR Campus
