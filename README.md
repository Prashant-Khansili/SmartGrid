# SmartGrid: AI-Based Smart Meter Intelligence & Loss Detection

An AI-powered solution for electricity distribution networks to predict electricity demand and detect anomalies in smart meter consumption patterns.

## Overview

This project provides two core capabilities:

- **Demand Forecasting**: Predict short-term electricity demand to identify peak loads and grid stress zones
- **Anomaly Detection**: Identify abnormal consumption patterns indicating theft, tampering, or irregularities

**Dataset**: Built using CEEW Smart Meter data from Kaggle (Bareilly & Mathura, India, 2019-2021)

---

## Quick Start

### 1. Clone & Setup

```bash
git clone <your-repository-url>
cd SmartGrid
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Prepare Data

Download CSV files from [Kaggle](https://www.kaggle.com/datasets/pythonafroz/electricity-smart-meter-data-from-india) and place in `datasets/` folder.

### 4. Run the Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard pages:

- **01_demand_forecasting.py** - View demand predictions
- **02_anomaly_detection.py** - Detect meter anomalies
- **03_audit_log.py** - View audit trail

---

## Project Structure

```
SmartGrid/
├── README.md                        # This file
├── requirements.txt                 # Production dependencies
├── requirements-dev.txt             # Dev dependencies
├── run_dashboard.py                 # Run Streamlit dashboard
├── setup.sh / setup.bat             # Setup scripts
│
├── dashboard/
│   ├── app.py                       # Main dashboard
│   └── pages/
│       ├── 01_demand_forecasting.py
│       ├── 02_anomaly_detection.py
│       └── 03_audit_log.py
│
├── src/
│   ├── api.py                       # FastAPI server
│   ├── inference.py                 # Prediction pipeline
│   ├── model_manager.py             # Load/manage models
│   ├── audit_log.py                 # Audit logging
│   │
│   ├── data/
│   │   ├── data_loader.py
│   │   ├── data_processor.py
│   │   ├── data_masking.py
│   │   └── feature_engineering.py
│   │
│   └── models/
│       ├── base.py
│       ├── explainability.py
│       ├── demand/
│       │   ├── lstm_model.py
│       │   ├── arima_model.py
│       │   ├── exponential_smoothing.py
│       │   └── ensemble.py
│       └── anomaly/
│           ├── isolation_forest.py
│           └── statistical_baseline.py
│
├── notebooks/
│   ├── 01_eda.ipynb
│   └── LSTM-Model.ipynb
│
├── configs/
│   ├── data_config.yaml             # Data settings
│   ├── model_params.yaml            # Model hyperparameters
│   └── thresholds.yaml              # Anomaly thresholds
│
├── datasets/                        # Raw CSV data
│   ├── CEEW - Smart meter data Bareilly 2020.csv
│   ├── CEEW - Smart meter data Mathura 2019.csv
│   └── ...
│
├── keras-trained model/             # Pre-trained models
│   └── demand_forecasting_lstm.keras
│
└── tests/
    ├── test_data_loading.py
    └── test_models.py
```

---

## Features

### Demand Forecasting

- ✅ LSTM neural networks
- ✅ ARIMA statistical models
- ✅ Exponential smoothing
- ✅ Ensemble combining all methods
- ✅ Zone-level predictions
- ✅ Uncertainty quantification

### Anomaly Detection

- ✅ Isolation Forest (unsupervised)
- ✅ Statistical baselines (z-score, IQR)
- ✅ Anomaly classification (theft/tampering/normal)
- ✅ SHAP explainability
- ✅ Per-zone models
- ✅ Audit logging

### Dashboard Features

- 📊 Interactive visualizations with Plotly
- 🎯 Real-time predictions
- 📋 Anomaly flagging & severity levels
- 📝 Complete audit trail
- 💾 Export results to CSV

---

## Running the Application

### Dashboard (Main UI)

```bash
streamlit run dashboard/app.py
```

Includes: Demand forecasting, anomaly detection, and audit logs

### API Server

```bash
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

Access docs at: http://localhost:8000/docs

### Jupyter Notebooks

```bash
jupyter notebook notebooks/
```

---

## Configuration

Edit files in `configs/` to customize:

**data_config.yaml** - Data paths, zones, aggregation intervals

**model_params.yaml** - LSTM layers, ARIMA order, ensemble weights

**thresholds.yaml** - Anomaly detection sensitivity per zone

---

## API Endpoints

### Demand Forecasting

- `GET /forecast/zone/{zone_id}` - Day-ahead hourly forecast
- `POST /batch_forecast` - Forecast multiple zones

### Anomaly Detection

- `GET /anomalies/meter/{meter_id}` - Recent anomalies for meter
- `POST /batch_anomalies` - Batch anomaly detection
- `GET /anomalies/zone/{zone_id}` - Zone-level summary

### Utilities

- `GET /models/versions` - Model versions & info
- `GET /health` - System health check

---

## Evaluation Metrics

### Demand Forecasting

- MAPE (Mean Absolute Percentage Error) < 15%
- RMSE & MAE on test data
- Risk zone detection precision ≥ 70%

### Anomaly Detection

- Recall > 80% on test anomalies
- False positive rate < 5%
- Precision on classified anomalies > 75%

---

## Development

### Run Tests

```bash
pytest tests/
pytest tests/ --cov=src --cov=dashboard
```

### Format Code

```bash
black src/ dashboard/ tests/
```

### Contributing

1. Create feature branch: `git checkout -b feature/xyz`
2. Add tests for changes
3. Run `pytest` before submitting
4. Submit pull request

---

## Key Technologies

- **Frameworks**: Streamlit, FastAPI, Scikit-learn
- **ML Models**: LSTM, ARIMA, Isolation Forest
- **Data**: Pandas, NumPy
- **Visualization**: Plotly, SHAP
- **Infrastructure**: Python 3.8+, conda/pip

---

## Important Notes

- ✅ All predictions are **decision-support only** (no system changes)
- ✅ **Full audit trail** for all predictions and model versions
- ✅ **Local processing** - no sensitive data sent externally
- ✅ **Public dataset** from Kaggle (CC0 license)
- ✅ **Explainability** via SHAP force plots

---

## References

- [CEEW Smart Meter Dataset](https://www.kaggle.com/datasets/pythonafroz/electricity-smart-meter-data-from-india)
- [SHAP Documentation](https://shap.readthedocs.io/)
- [Scikit-learn](https://scikit-learn.org/)
- [Statsmodels](https://www.statsmodels.org/)

---

## License

CC0 Public Domain (matches Kaggle dataset license)

## Support

For issues or questions, please create an issue in the repository.
