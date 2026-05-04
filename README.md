# Theme 8: AI-Based Smart Meter Intelligence & Loss Detection

This project provides a comprehensive solution for electricity distribution networks, leveraging smart meter data to deliver predictive insights and detect anomalies. It is designed for collaboration and can be extended to support various smart meter datasets.

**Core Components:**
1.  **Demand Forecasting**: Predicts short-term electricity demand to help identify high-risk zones for peak load and grid stress.
2.  **Anomaly & Theft Detection**: Identifies abnormal consumption patterns, flagging potential theft, tampering, or other irregularities.

**Dataset**: The system is built using the CEEW Smart Meter data from Kaggle, which includes data from Bareilly and Mathura, India (2019-2021).

---

## 🚀 Getting Started

Follow these instructions to set up the project for development and collaboration.

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone <your-repository-url>
cd theme8
```

### 2. Set Up the Environment

Create a virtual environment to manage project dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required packages for the core application and for development:

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (for running notebooks, tests, etc.)
pip install -r requirements-dev.txt
```

### 4. Data and Model Setup

**Important**: This project is configured to keep large data files and trained models out of the Git repository.

-   **Data**: Download the required CSV files from the [Kaggle dataset](https://www.kaggle.com/datasets/pythonafroz/electricity-smart-meter-data-from-india) and place them in the `data/raw/` directory.
-   **Models**: If you are training your models on Kaggle or another external environment, you will get a `model.pkl` file. Place this file in the `outputs/models/` directory. This location is included in the `.gitignore` file, so your model artifacts will not be committed to the repository.

---

## Running the Application

You can run the individual components of the project as follows:

### EDA Notebook

To explore the data, run the Jupyter Notebook:

```bash
jupyter notebook notebooks/01_eda.ipynb
```

### Streamlit Dashboard

To visualize the results and interact with the models, run the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

### API Server

To start the FastAPI server for model inference:

```bash
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🏛️ Project Structure

The project is organized to separate concerns and facilitate collaboration:

```
theme8/
├── .gitignore          # Specifies files to ignore in Git
├── README.md           # This file
├── requirements.txt    # Production dependencies
├── requirements-dev.txt # Development dependencies
├── src/                # Core application source code
│   ├── data/           # Data loading, processing, and feature engineering
│   ├── models/         # Model definitions (demand and anomaly)
│   ├── api.py          # FastAPI endpoints
│   └── inference.py    # Prediction pipeline
├── dashboard/          # Streamlit dashboard application
├── notebooks/          # Jupyter notebooks for EDA and development
├── tests/              # Unit and integration tests
└── configs/            # Configuration files (data, model params)
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1.  Create a new branch for your feature or bug fix.
2.  Ensure your code follows the project's coding standards.
3.  Write tests for your changes.
4.  Submit a pull request with a clear description of your work.

│   ├── 02_demand_forecasting_dev.ipynb      # Demand model development
│   ├── 03_anomaly_detection_dev.ipynb       # Anomaly model development
│   └── 04_evaluation_report.ipynb           # Full evaluation & metrics
├── tests/
│   ├── __init__.py
│   ├── test_data_loading.py                 # Data loader tests
│   ├── test_models.py                       # Model tests
│   └── test_api.py                          # API tests
├── configs/
│   ├── model_params.yaml                    # Hyperparameters
│   ├── data_config.yaml                     # Data paths & settings
│   └── thresholds.yaml                      # Anomaly thresholds
├── data/
│   ├── raw/                                 # Raw CEEW CSV files
│   └── processed/                           # Cleaned & aggregated data
└── outputs/
    ├── forecasts_latest.csv                 # Latest forecasts
    ├── anomalies_latest.csv                 # Latest anomalies
    ├── evaluation_report.html                # Evaluation metrics
    └── model_versions.log                    # Model audit trail
```

## Implementation Phases

| Phase | Focus | Days |
|-------|-------|------|
| 1 | Data loading, EDA, preprocessing | 2-3 |
| 2 | Demand forecasting (ARIMA, LSTM, Ensemble) | 3-4 |
| 3 | Anomaly detection (Isolation Forest, Classification) | 3-4 |
| 4 | API integration & inference pipeline | 2 |
| 5 | Dashboard & visualization | 2-3 |
| 6 | Evaluation, documentation, risk analysis | 2 |

## Key Features

### Part A: Demand Forecasting
- ✅ Ensemble combining ARIMA + Exponential Smoothing + LSTM
- ✅ Zone-level aggregation and risk flagging
- ✅ Uncertainty quantification (confidence intervals)
- ✅ SHAP feature importance visualization
- ✅ Historical comparison baselines

### Part B: Anomaly Detection
- ✅ Unsupervised Isolation Forest (per-zone models)
- ✅ Statistical baselines (z-score, IQR validation)
- ✅ Anomaly classification (theft/tampering/normal)
- ✅ False positive mitigation via peer comparison
- ✅ Temporal consistency checking
- ✅ SHAP explainability for flagged meters

### Explainability & Audit
- ✅ SHAP force plots for each prediction
- ✅ Feature decomposition (trend + seasonality + residual)
- ✅ Confidence/severity scoring (low/medium/high)
- ✅ Complete audit logging (inputs, outputs, model versions, timestamps)
- ✅ Exportable reports (PDF/CSV)

## Configuration

Edit `configs/` YAML files to customize:
- **data_config.yaml**: Data paths, aggregation intervals, zones
- **model_params.yaml**: ARIMA order, LSTM layers, ensemble weights
- **thresholds.yaml**: Anomaly detection thresholds per zone

## API Endpoints

### Demand Forecasting
```
GET  /forecast/zone/{zone_id}
     → Returns day-ahead hourly forecast + risk flags

POST /batch_forecast
     → Batch forecast for multiple zones
```

### Anomaly Detection
```
GET  /anomalies/meter/{meter_id}
     → Recent anomalies with classification + confidence

POST /batch_anomalies
     → Batch anomaly detection for multiple meters

GET  /anomalies/zone/{zone_id}
     → Zone-level anomaly summary
```

### Audit & Health
```
GET  /models/versions
     → Model versions & deployment info

GET  /health
     → System health check
```

## Evaluation Metrics

### Demand Forecasting
- MAPE (Mean Absolute Percentage Error) < 15% target
- RMSE & MAE on zone-level forecasts
- Risk zone detection precision ≥ 70%
- Comparison to naive baselines

### Anomaly Detection
- Recall > 80% on injected anomalies
- False positive rate < 5% on normal data
- Precision on classified anomalies
- Cross-validation with peer patterns

## Non-Modification & Compliance

- ✅ **No system changes**: All outputs are decision-support only
- ✅ **Full audit trail**: Every prediction logged with inputs, model version, timestamp
- ✅ **Explainability**: SHAP plots explain individual predictions
- ✅ **No external LLM**: All models local, no sensitive data sent externally
- ✅ **Public data**: Using anonymized Kaggle dataset (CC0 license)

## Development Roadmap

- [ ] Phase 1: Data loading & EDA
- [ ] Phase 2: Demand forecasting models
- [ ] Phase 3: Anomaly detection models
- [ ] Phase 4: API & integration
- [ ] Phase 5: Dashboard
- [ ] Phase 6: Evaluation & documentation

## Contributing

1. Create a feature branch: `git checkout -b feature/xyz`
2. Implement changes with tests
3. Run tests: `pytest tests/`
4. Format code: `black src/ dashboard/ tests/`
5. Submit PR with evaluation results

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov=dashboard

# Run specific test
pytest tests/test_models.py::test_forecast_ensemble
```

## References

- Dataset: https://www.kaggle.com/datasets/pythonafroz/electricity-smart-meter-data-from-india
- SHAP Documentation: https://shap.readthedocs.io/
- Prophet: https://facebook.github.io/prophet/
- Statsmodels: https://www.statsmodels.org/

## License

CC0 Public Domain (matches Kaggle dataset license)

## Contact

For questions or issues, create an issue in the repository.
