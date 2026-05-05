# SmartGrid Dashboard - Complete Setup & Execution Guide

## 📋 Table of Contents

1. [Initial Setup](#initial-setup)
2. [Install Dependencies](#install-dependencies)
3. [Data Preparation](#data-preparation)
4. [Model Training](#model-training)
5. [Run Dashboard](#run-dashboard)
6. [Troubleshooting](#troubleshooting)

---

## 1️⃣ Initial Setup

### Step 1: Clone the Repository (if not already done)

```bash
git clone <repository-url>
cd SmartGrid
```

### Step 2: Verify Project Structure

```bash
# You should see this structure:
SmartGrid/
├── dashboard/
│   ├── app.py
│   └── pages/
│       ├── 01_demand_forecasting.py
│       ├── 02_anomaly_detection.py
│       └── 03_audit_log.py
├── src/
│   ├── models/
│   │   ├── demand/
│   │   │   └── lstm_model.py
│   │   ├── anomaly/
│   │   │   └── isolation_forest.py
│   │   └── base.py
│   ├── data/
│   │   ├── data_loader.py
│   │   ├── data_processor.py
│   │   └── feature_engineering.py
│   └── inference.py
├── configs/
│   ├── data_config.yaml
│   └── model_params.yaml
├── requirements.txt
└── README.md
```

### Step 3: Create Python Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux (Bash):**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 2️⃣ Install Dependencies

### Step 1: Upgrade pip, setuptools, wheel

```bash
pip install --upgrade pip setuptools wheel
```

### Step 2: Install Production Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Install Development Dependencies (Optional but Recommended)

```bash
pip install -r requirements-dev.txt
```

### Step 4: Verify Installation

```bash
python -c "import streamlit; import tensorflow; import sklearn; print('✅ All packages installed!')"
```

### Expected Output:

```
✅ All packages installed!
```

---

## 3️⃣ Data Preparation

### Option A: Using Sample Data (Recommended for First Run)

The dashboard **auto-generates realistic sample data**, so you don't need to download anything initially. Just proceed to model training.

### Option B: Using Real CEEW Dataset (For Production)

**Download from Kaggle:**

1. Go to: https://www.kaggle.com/datasets/pythonafroz/electricity-smart-meter-data-from-india
2. Download the CSV files
3. Create directory and place files:
   ```bash
   mkdir -p data/raw
   # Place CSV files here:
   # - CEEW - Smart meter data Bareilly 2019.csv
   # - CEEW - Smart meter data Bareilly 2020.csv
   # - CEEW - Smart meter data Bareilly 2021.csv
   # - CEEW - Smart meter data Mathura 2019.csv
   # - CEEW - Smart meter data Mathura 2020.csv
   # - CEEW - Smart meter data Mathura 2021.csv
   ```

---

## 4️⃣ Model Training

### Option A: Train Models Using Notebook (Recommended)

#### Step 1: Start Jupyter

```bash
jupyter notebook
```

#### Step 2: Open and Run Training Notebooks

- Navigate to `notebooks/LSTM-Model.ipynb`
- Run all cells sequentially
  - **Cell 1**: Import libraries ✅
  - **Cell 2**: Load dataset (uses sample data if CEEW not available)
  - **Cell 3**: Data preprocessing
  - **Cell 4**: Feature engineering
  - **Cell 5-6**: Prepare & reshape data for LSTM
  - **Cell 7**: Build LSTM model
  - **Cell 8**: Train model (100 epochs)
  - **Cell 9-10**: Evaluate model
  - **Cell 11**: Save trained model & artifacts

#### Expected Output:

```
✓ All libraries imported successfully
✓ Successfully loaded all 8 files!
Combined dataset shape: (450000, 5)
Total records: 450,000

✓ Model training complete
Train RMSE: 2.34 kWh
Test RMSE: 2.87 kWh
Test R²: 0.9142

✓ Total files saved: 5
  ✓ demand_forecasting_lstm.keras (45.2 MB)
  ✓ scaler_X.pkl (12.4 KB)
  ✓ scaler_y.pkl (5.2 KB)
  ✓ feature_columns.pkl (8.3 KB)
  ✓ model_metadata.pkl (3.1 KB)

✓✓✓ ALL FILES SAVED SUCCESSFULLY ✓✓✓
```

### Option B: Quick Train (Automated Script)

**Create `train_models.py` in root:**

```python
"""Quick model training script"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import pandas as pd
import numpy as np
from src.models.demand.lstm_model import LSTMForecaster
from src.models.anomaly.isolation_forest import IsolationForestDetector
from sklearn.preprocessing import StandardScaler

print("🚀 Starting model training...")

# 1. Generate/Load data
print("\n1️⃣ Loading data...")
dates = pd.date_range(start="2024-01-01", end="2024-03-31", freq="15min")
hourly = 25 + 15 * np.sin(np.arange(len(dates)) * 2 * np.pi / (24 * 4))
noise = np.random.normal(0, 2, len(dates))
consumption = np.maximum(hourly + noise, 5)

data = pd.DataFrame({'kwh': consumption})
print(f"   ✓ Loaded {len(data)} records")

# 2. Train LSTM
print("\n2️⃣ Training LSTM demand forecaster...")
lstm = LSTMForecaster(lookback=168, hidden_units=64, epochs=10)
lstm.fit(data['kwh'])
print("   ✓ LSTM training complete")

# 3. Train Isolation Forest
print("\n3️⃣ Training Isolation Forest anomaly detector...")
features = np.random.randn(len(data), 4)
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
iso_forest = IsolationForestDetector(contamination=0.1)
iso_forest.fit(features_scaled)
print("   ✓ Isolation Forest training complete")

print("\n✅ All models trained successfully!")
```

**Run it:**

```bash
python train_models.py
```

---

## 5️⃣ Run Dashboard

### Step 1: Navigate to Dashboard Directory

```bash
cd dashboard
```

### Step 2: Start Streamlit

```bash
streamlit run app.py
```

### Expected Output:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

  Ready to accept user input...
```

### Step 3: Dashboard Opens Automatically

- Browser opens at `http://localhost:8501`
- You'll see the **main hub dashboard**

---

## 📊 Using the Dashboard

### Main Hub (Home Page)

- **Overview**: System status, KPIs, recent alerts
- **Navigation**: Click sidebar links to access other pages

### 📈 Demand Forecasting Page

1. **Sidebar Configuration:**
   - Select Zone: Bareilly, Mathura, or All Zones
   - Forecast Horizon: 1-168 hours (default 24)
   - Model Type: LSTM, ARIMA, or Ensemble

2. **Dashboard Shows:**
   - Average & Peak Demand
   - Risk Level (🟢 LOW / 🟡 MEDIUM / 🔴 HIGH)
   - Forecast chart with confidence intervals
   - Hourly breakdown table
   - Risk assessment metrics

### ⚠️ Anomaly Detection Page

1. **Sidebar Configuration:**
   - Select Zone
   - Detection Method: Isolation Forest, Statistical, or Hybrid
   - Sensitivity: 5%-30%
   - Days to Analyze: 7-90 days

2. **Dashboard Shows:**
   - Anomalies detected, critical meters
   - Timeline of anomalies
   - Anomaly score distribution
   - Flagged meters with severity
   - Detailed inspection reports
   - Field visit recommendations with estimated loss

### 📋 Audit Log Page

1. **Sidebar Filters:**
   - Date Range
   - Log Type: Forecast, Anomaly Detection, Model Training, System, API
   - Severity: INFO, WARNING, ERROR, CRITICAL

2. **Dashboard Shows:**
   - Activity timeline
   - Event type distribution
   - Success rates & performance metrics
   - Download logs (CSV/JSON)
   - 30-day accuracy trends

---

## 🔄 Full Workflow Example

### Complete Flow from Start to Finish:

```bash
# 1. Clone and setup
git clone <repo>
cd SmartGrid
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate   # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Train models using notebook
jupyter notebook
# Open notebooks/LSTM-Model.ipynb and run all cells

# 4. Start dashboard
cd dashboard
streamlit run app.py

# 5. Open browser at http://localhost:8501
# ✅ Dashboard is live!
```

---

## 📁 Output Files Generated

After model training, check:

**From Notebook:**

```
outputs/
├── demand_forecasting_lstm.keras      # Trained LSTM model
├── scaler_X.pkl                       # Feature scaler
├── scaler_y.pkl                       # Target scaler
├── feature_columns.pkl                # Feature names
└── model_metadata.pkl                 # Model info & metrics
```

**From Dashboard:**

```
dashboard/
└── .streamlit/
    └── config.toml                    # Streamlit config
```

---

## 🐛 Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**

```bash
pip install streamlit --upgrade
```

### Issue 2: "ModuleNotFoundError: No module named 'src'"

**Solution:**

- Ensure you're in the `SmartGrid` directory
- Or run: `export PYTHONPATH="${PYTHONPATH}:$(pwd)"`

### Issue 3: TensorFlow/CUDA Issues

**Solution:**

```bash
# Install CPU version if no GPU
pip install tensorflow-cpu

# Or for GPU:
pip install tensorflow[and-cuda]
```

### Issue 4: "Address already in use" (Port 8501)

**Solution:**

```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Issue 5: Dashboard not loading data

**Solution:**

- Ensure you have internet (for downloading models first time)
- Check `configs/data_config.yaml` paths
- Regenerates sample data automatically if files not found

### Issue 6: "No module named src.models..."

**Solution:**

```bash
# From SmartGrid root directory:
pip install -e .
# OR set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

## ✅ Verification Checklist

- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip list | grep streamlit`)
- [ ] In `SmartGrid` root directory
- [ ] `dashboard/` folder exists with `app.py`
- [ ] `src/models/` folders exist
- [ ] Can run: `python -c "import src.models.demand.lstm_model"`
- [ ] Dashboard starts: `streamlit run dashboard/app.py`
- [ ] Browser opens at `http://localhost:8501`

---

## 📞 Quick Reference

| Task                      | Command                                   |
| ------------------------- | ----------------------------------------- |
| Activate venv (Windows)   | `.\venv\Scripts\Activate.ps1`             |
| Activate venv (Mac/Linux) | `source venv/bin/activate`                |
| Install dependencies      | `pip install -r requirements.txt`         |
| Train models              | `jupyter notebook` (run LSTM-Model.ipynb) |
| Start dashboard           | `cd dashboard && streamlit run app.py`    |
| Open browser              | http://localhost:8501                     |
| Stop dashboard            | Press Ctrl+C                              |
| Deactivate venv           | `deactivate`                              |

---

## 🎯 Next Steps After Dashboard Runs

1. **Explore Demand Forecasting**: Try different zones and forecast horizons
2. **Check Anomalies**: View detected patterns and inspection reports
3. **Review Audit Log**: Monitor prediction history
4. **Train with Real Data**: Replace sample data with CEEW dataset
5. **Deploy Models**: Use `src/api.py` for API deployment

---

**🚀 You're ready to go!** If you get stuck, check the Troubleshooting section above.
