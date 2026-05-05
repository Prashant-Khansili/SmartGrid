# 🚀 SmartGrid Dashboard - Quick Start (5 Minutes)

## ⚡ Fast Track Setup

### **Windows Users (PowerShell)**

```powershell
# 1️⃣ Run automatic setup
.\setup.bat

# OR manual setup:
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start dashboard
cd dashboard
streamlit run app.py

# 2️⃣ Open browser
# → http://localhost:8501
```

---

### **macOS/Linux Users (Bash)**

```bash
# 1️⃣ Run automatic setup
bash setup.sh

# OR manual setup:
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start dashboard
cd dashboard
streamlit run app.py

# 2️⃣ Open browser
# → http://localhost:8501
```

---

## 📋 Complete Step-by-Step (From Fresh Clone)

### **Step 1: Navigate to Project**

```bash
cd /path/to/SmartGrid
```

### **Step 2: Set Up Python Environment**

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install All Dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt  # (optional) for notebooks
```

### **Step 4: Verify Installation**

```bash
python -c "import streamlit, tensorflow, sklearn; print('✅ Ready!')"
```

### **Step 5: (Optional) Train Models**

#### Option A - Using Jupyter Notebook

```bash
# Start Jupyter
jupyter notebook

# Then open and run: notebooks/LSTM-Model.ipynb
# This trains the LSTM demand forecasting model
```

#### Option B - Quick Python Script

```bash
# Run quick training
python -c "
import sys, pandas as pd, numpy as np
from src.models.demand.lstm_model import LSTMForecaster

# Generate sample data
dates = pd.date_range('2024-01-01', '2024-03-31', freq='15min')
consumption = 25 + 15*np.sin(np.arange(len(dates))*2*np.pi/(24*4)) + np.random.normal(0,2,len(dates))

# Train LSTM
lstm = LSTMForecaster(lookback=168, epochs=5)
lstm.fit(pd.Series(consumption))
print('✅ Model trained!')
"
```

### **Step 6: Start Dashboard**

```bash
cd dashboard
streamlit run app.py
```

### **Step 7: View in Browser**

- Automatically opens at `http://localhost:8501`
- OR manually navigate to that URL

---

## 📊 Dashboard Pages & Features

### **🏠 Home Hub** (Main Page)

- System status overview
- KPI metrics (Alerts, Meters, Accuracy, Loss)
- Recent anomalies feed
- Quick navigation

### **📈 Demand Forecasting** (Page 1)

```
Sidebar Options:
├─ Zone: Bareilly / Mathura / All Zones
├─ Forecast Horizon: 1-168 hours
└─ Model: LSTM / ARIMA / Ensemble

Features:
├─ 📊 Demand forecast chart with confidence intervals
├─ ⚡ Risk classification (LOW/MEDIUM/HIGH)
├─ 📈 Statistical metrics
└─ 🕐 Hourly breakdown table
```

### **⚠️ Anomaly Detection** (Page 2)

```
Sidebar Options:
├─ Zone: Bareilly / Mathura / All Zones
├─ Method: Isolation Forest / Statistical / Hybrid
├─ Sensitivity: 5%-30%
└─ Days: 7-90 days

Features:
├─ 🎯 Real-time anomaly scoring
├─ 🔴 Severity levels (CRITICAL/HIGH/MEDIUM)
├─ 📋 Flagged meters with evidence
├─ 🔍 Inspection reports
└─ 💰 Estimated loss calculations
```

### **📋 Audit Log** (Page 3)

```
Sidebar Options:
├─ Date Range
├─ Log Type: Forecast/Anomaly/Training/System/API
└─ Severity: INFO/WARNING/ERROR/CRITICAL

Features:
├─ 📈 Activity timeline
├─ 📊 Performance metrics
├─ 📥 CSV/JSON export
└─ 🎯 Accuracy trends
```

---

## 🎯 What Happens When You Run

### On First Launch:

1. ✅ Loads or generates sample smart meter data
2. ✅ Auto-trains LSTM model (takes ~30 seconds first time)
3. ✅ Initializes Isolation Forest anomaly detector
4. ✅ Generates realistic consumption patterns with embedded anomalies
5. ✅ Displays interactive visualizations

### Sample Data Characteristics:

- 📅 90 days of 15-minute interval readings
- 🌍 2 zones: Bareilly & Mathura
- 📊 10 smart meters (5 per zone)
- ⚡ Realistic consumption patterns with:
  - Hourly cyclical demand
  - Daily noise
  - Weekly patterns
  - Embedded anomalies (10% of readings)

---

## 🛠️ Customization

### Change Forecast Horizon

Use sidebar slider: **1-168 hours** (default: 24 hours)

### Adjust Anomaly Sensitivity

Use sidebar slider: **5-30%** (default: 10%)

- **Lower (5%)**: Fewer but more certain anomalies
- **Higher (30%)**: More anomalies detected, higher false positive rate

### Change Zone

Dropdown: **Bareilly**, **Mathura**, or **All Zones**

### Select Detection Method

Radio button: **Isolation Forest** (default), Statistical, or Hybrid

---

## 📁 File Locations After Training

```
SmartGrid/
├── outputs/
│   ├── demand_forecasting_lstm.keras     ← Trained LSTM model
│   ├── scaler_X.pkl                      ← Feature scaler
│   ├── scaler_y.pkl                      ← Target scaler
│   ├── feature_columns.pkl               ← Feature names
│   └── model_metadata.pkl                ← Model metadata
└── dashboard/
    ├── .streamlit/
    │   └── config.toml                   ← Streamlit configuration
    └── __pycache__/                      ← Cache files
```

---

## 🐛 Common Issues & Quick Fixes

| Issue                       | Fix                                            |
| --------------------------- | ---------------------------------------------- |
| "No module named streamlit" | `pip install streamlit --upgrade`              |
| "No module named src"       | Run from `SmartGrid` root directory            |
| Port 8501 already in use    | `streamlit run app.py --server.port 8502`      |
| TensorFlow errors           | `pip install tensorflow-cpu`                   |
| "Address already in use"    | Kill process: `lsof -ti:8501 \| xargs kill -9` |
| Dashboard not loading       | Check internet (first model download)          |

---

## 🔄 Development Workflow

If you want to make changes:

```bash
# 1. Activate environment
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate  # Mac/Linux

# 2. Edit files (e.g., dashboard pages)
code dashboard/pages/01_demand_forecasting.py

# 3. Streamlit auto-reloads on save
# (Just save and refresh browser)

# 4. Or manually restart
# Ctrl+C in terminal and re-run:
# streamlit run dashboard/app.py
```

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] In `SmartGrid` root directory
- [ ] Virtual environment created
- [ ] Virtual environment activated (shows `(venv)` in prompt)
- [ ] Dependencies installed: `pip list | grep streamlit`
- [ ] Can import packages: `python -c "import streamlit"`
- [ ] Dashboard starts: `streamlit run dashboard/app.py`
- [ ] Browser opens at `http://localhost:8501`
- [ ] Can see home page with 4 metrics
- [ ] Sidebar navigation works

---

## 📞 Help & Support

For detailed troubleshooting: See **`SETUP_GUIDE.md`**

For API documentation: See **`src/api.py`**

For model details: See **`src/models/demand/lstm_model.py`** and **`src/models/anomaly/isolation_forest.py`**

---

## 🎉 You're All Set!

**Time to completion:** 5-10 minutes (including installs)

**Next steps:**

1. Explore the three dashboards
2. Try different zones and timeframes
3. Check anomaly detection sensitivity
4. Review inspection evidence reports
5. Export audit logs

**Happy forecasting! 🚀**
