# 🔗 Model Integration Guide

## Overview

The SmartGrid dashboard now has **full integration** with trained models! Here's how it works:

---

## 🔄 Complete Workflow

```
┌─────────────────┐
│  Train Models   │  (Step 1: Run Jupyter notebook)
│   in Notebook   │
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Save Trained Models to outputs/      │
│  ✓ lstm.keras                        │
│  ✓ scaler_X.pkl                      │
│  ✓ scaler_y.pkl                      │
│  ✓ feature_columns.pkl               │
│  ✓ model_metadata.pkl                │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Start Dashboard                      │
│  streamlit run app.py                │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Model Manager Checks:                │
│  1. Are trained models in outputs/?  │
│  2. Load them ✅                     │
│  3. Use them for predictions 🚀      │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Dashboard Display:                   │
│  ✅ Uses trained LSTM for forecasts  │
│  ✅ Shows real model accuracy metrics│
│  ✅ Uses real data if available      │
└──────────────────────────────────────┘
```

---

## 📋 What Happens At Each Stage

### Stage 1: Training Models (Notebook)

**File:** `notebooks/LSTM-Model.ipynb`

```python
# This notebook:
✅ Loads data
✅ Preprocesses
✅ Trains LSTM
✅ Trains Isolation Forest
✅ Saves all models to outputs/
```

**Output Files Created:**

```
outputs/
├── demand_forecasting_lstm.keras    (Trained neural network)
├── scaler_X.pkl                     (Feature scaler)
├── scaler_y.pkl                     (Target scaler)
├── feature_columns.pkl              (Feature names)
└── model_metadata.pkl               (Model stats & accuracy)
```

---

### Stage 2: Dashboard Initialization

**File:** `src/model_manager.py` (New Integration Layer)

When dashboard starts:

```
1. Initialize ModelManager
   └─ Check if outputs/demand_forecasting_lstm.keras exists
   └─ If YES: Load pre-trained models ✅
   └─ If NO:  Use fallback (sample data + on-the-fly training) ⚠️

2. Initialize DataManager
   └─ Check if real CEEW data exists in data/raw/
   └─ If YES: Use real data
   └─ If NO:  Generate realistic sample data

3. Log status
   └─ Tell user which models are loaded
   └─ Show data source (real vs sample)
```

---

### Stage 3: Dashboard Execution

#### Demand Forecasting Page

**Header Shows:**

```
📊 Demand Forecasting Dashboard

Model Status: ✅ Using Pre-Trained Models (from notebook training)
```

**When user selects zone & clicks predict:**

```
1. Load data for selected zone (real or sample)
2. Use pre-trained LSTM model to generate forecast
3. Use pre-trained scalers for inverse transformation
4. Display forecast with trained model's confidence intervals
5. Show actual model accuracy metrics from training
```

#### Anomaly Detection Page

**Header Shows:**

```
⚠️ Anomaly Detection Dashboard

Model Status: ✅ Using Pre-Trained Models (from notebook training)
```

**When detector runs:**

```
1. Load meter data (real or sample)
2. Extract features (consumption, voltage, current, power_factor)
3. Use pre-trained Isolation Forest to score anomalies
4. Flag meters with severity levels
5. Generate inspection evidence based on trained detector
```

---

## 🎯 Expected Behavior

### ✅ Scenario 1: After Running Notebook Training

**You'll see:**

```
═══════════════════════════════════════════
Initializing SmartGrid Model & Data Managers
═══════════════════════════════════════════

📊 Model Status:
   Models Loaded: ✅
   LSTM Model: ✅
   Scalers: ✅

📁 Data Status:
   Real Data Available: ❌
   Using: Pre-trained models (from notebook)

═══════════════════════════════════════════
```

**Dashboard Pages Show:**

- `✅ Using Pre-Trained Models (from notebook training)`
- Actual accuracy metrics from training (e.g., "R²: 0.914")
- Trained model performance data

---

### ⚠️ Scenario 2: Without Running Notebook

**You'll see:**

```
═══════════════════════════════════════════
Initializing SmartGrid Model & Data Managers
═══════════════════════════════════════════

📊 Model Status:
   Models Loaded: ❌
   LSTM Model: ❌
   Scalers: ❌

📁 Data Status:
   Real Data Available: ❌
   Using: Sample data with on-the-fly training

═══════════════════════════════════════════
```

**Dashboard Pages Show:**

- `⚠️ Using Sample Data & On-the-Fly Training (Run notebook for better results)`
- Generated synthetic accuracy metrics
- Models trained on sample data (less accurate but functional)

---

## 🚀 Complete End-to-End Example

### Step 1: Train Models

```bash
# Open Jupyter
jupyter notebook

# Run all cells in: notebooks/LSTM-Model.ipynb
# Expected output:
# ✓ Model training complete
# ✓ Total files saved: 5
# ✓ demand_forecasting_lstm.keras (45.2 MB)
# ✓ scaler_X.pkl
# ✓ scaler_y.pkl
# ✓ feature_columns.pkl
# ✓ model_metadata.pkl
```

### Step 2: Start Dashboard

```bash
cd dashboard
streamlit run app.py
```

### Step 3: See Trained Models in Action

**Demand Forecasting Page:**

```
📊 Demand Forecasting Dashboard

Model Status: ✅ Using Pre-Trained Models (from notebook training)

Sidebar: Zone = Bareilly, Forecast Horizon = 24h, Model = LSTM

KPIs Shown:
  • Average Demand (kWh): 34.67
  • Peak Demand (kWh): 42.15
  • Risk Level: 🟡 MEDIUM
  • Model Accuracy: 91.4%  ← FROM TRAINED MODEL!

Chart: Shows forecast using actual LSTM model
Confidence Interval: Based on trained model's standard deviation
```

**Anomaly Detection Page:**

```
⚠️ Anomaly Detection Dashboard

Model Status: ✅ Using Pre-Trained Models (from notebook training)

Sidebar: Zone = Bareilly, Method = Isolation Forest, Sensitivity = 10%

Results:
  • Anomalies Detected: 2,847
  • Critical Meters: 12
  • Flagged: METER_BRL_001, METER_BRL_045, ...

Detailed Report:
  Meter: METER_BRL_001
  Anomaly: 🔻 Potential Theft/Bypass
  Evidence: Consumption dropped 65% vs 30-day average
  Recommendation: Priority inspection
```

---

## 📁 File Structure After Setup

```
SmartGrid/
├── src/
│   ├── model_manager.py              ← NEW Integration Layer
│   ├── models/
│   │   ├── demand/
│   │   │   └── lstm_model.py         (Integrated with manager)
│   │   └── anomaly/
│   │       └── isolation_forest.py   (Integrated with manager)
│   └── data/
├── outputs/
│   ├── demand_forecasting_lstm.keras ← Loaded by dashboard
│   ├── scaler_X.pkl                  ← Loaded by dashboard
│   ├── scaler_y.pkl                  ← Loaded by dashboard
│   ├── feature_columns.pkl           ← Loaded by dashboard
│   └── model_metadata.pkl            ← Loaded by dashboard
├── dashboard/
│   ├── app.py                        (Main hub)
│   └── pages/
│       ├── 01_demand_forecasting.py  (Uses model_manager)
│       ├── 02_anomaly_detection.py   (Uses model_manager)
│       └── 03_audit_log.py           (Audit trail)
└── notebooks/
    └── LSTM-Model.ipynb              (Trains & saves models)
```

---

## 🔍 How to Verify Integration is Working

### Check 1: After Starting Dashboard

Look for this message in browser:

```
Model Status: ✅ Using Pre-Trained Models (from notebook training)
```

### Check 2: Check Terminal Output

```bash
Initializing SmartGrid Model & Data Managers
═══════════════════════════════════════════

📊 Model Status:
   Models Loaded: ✅
   LSTM Model: ✅
   Scalers: ✅
```

### Check 3: Verify Model Files Exist

```bash
ls outputs/
# Should show:
# demand_forecasting_lstm.keras
# feature_columns.pkl
# model_metadata.pkl
# scaler_X.pkl
# scaler_y.pkl
```

### Check 4: Load Models Manually

```python
from src.model_manager import model_manager, initialize_managers
initialize_managers()

status = model_manager.get_model_status()
print(status['models_loaded'])  # Should be True
print(status['metadata'])       # Should show training stats
```

---

## 🛠️ Troubleshooting

### Issue: Dashboard shows ⚠️ "Using Sample Data & On-the-Fly Training"

**Solution:**

```bash
# Check if trained model files exist
ls outputs/
# If empty, run the notebook first:
jupyter notebook notebooks/LSTM-Model.ipynb
# Run all cells
# Then restart dashboard
streamlit run app.py
```

### Issue: "No module named model_manager"

**Solution:**

```bash
# Make sure you're in the SmartGrid root directory
cd /path/to/SmartGrid
streamlit run dashboard/app.py
```

### Issue: Models load but predictions look wrong

**Solution:**

```bash
# Clear Streamlit cache and reload
# Option 1: Click "Always rerun" in Streamlit UI
# Option 2: Clear cache folder
rm -rf ~/.streamlit/
# Option 3: In terminal
Ctrl+C  # Stop app
streamlit run app.py --logger.level=debug  # Restart with debug logging
```

---

## 🎯 Summary

| Aspect             | With Notebook Training | Without Notebook       |
| ------------------ | ---------------------- | ---------------------- |
| **Model Status**   | ✅ Trained             | ⚠️ On-the-fly          |
| **Accuracy**       | Real (e.g., 91.4%)     | Synthetic              |
| **Data Source**    | Real + Sample          | Sample only            |
| **Training Time**  | 1-2 min (notebook)     | <1 sec (per page load) |
| **Reliability**    | ⭐⭐⭐⭐⭐             | ⭐⭐⭐                 |
| **For Production** | ✅ Ready               | ❌ Demo only           |

---

## 🚀 Next Steps

1. **Run notebook**: `jupyter notebook notebooks/LSTM-Model.ipynb`
2. **Train models**: Execute all cells (takes ~2 minutes)
3. **Start dashboard**: `streamlit run dashboard/app.py`
4. **Verify models loaded**: Check header message for ✅
5. **Explore predictions**: Use all three dashboard pages
6. **Export reports**: Download logs from Audit Log page

---

**Integration is complete and automatic! 🎉**
