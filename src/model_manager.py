"""
Model Loading & Management Module
Handles loading pre-trained models and switching between sample/real data
"""

import os
import sys
import pickle
import logging
from pathlib import Path
from typing import Tuple, Optional, Dict, Any

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

logger = logging.getLogger(__name__)

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"
DATASETS_DIR = PROJECT_ROOT / "datasets"  # Real data folder
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

# Model file paths
LSTM_MODEL_PATH = OUTPUT_DIR / "demand_forecasting_lstm.keras"
SCALER_X_PATH = OUTPUT_DIR / "scaler_X.pkl"
SCALER_Y_PATH = OUTPUT_DIR / "scaler_y.pkl"
FEATURES_PATH = OUTPUT_DIR / "feature_columns.pkl"
METADATA_PATH = OUTPUT_DIR / "model_metadata.pkl"


class ModelManager:
    """Manages model loading and inference"""

    def __init__(self):
        self.lstm_model = None
        self.scaler_x = None
        self.scaler_y = None
        self.feature_columns = None
        self.metadata = None
        self.models_loaded = False

    def check_models_exist(self) -> bool:
        """Check if trained models exist"""
        required_files = [
            LSTM_MODEL_PATH,
            SCALER_X_PATH,
            SCALER_Y_PATH,
            FEATURES_PATH,
            METADATA_PATH,
        ]

        exist = all(f.exists() for f in required_files)

        if exist:
            logger.info(f"✅ All trained models found in {OUTPUT_DIR}")
        else:
            logger.warning(f"⚠️  Some models missing in {OUTPUT_DIR}")
            logger.warning(
                f"   Missing: {[f.name for f in required_files if not f.exists()]}"
            )

        return exist

    def load_models(self) -> bool:
        """Load pre-trained models"""
        if not self.check_models_exist():
            logger.info("Using sample data mode (models will be trained on-the-fly)")
            return False

        try:
            logger.info("Loading trained models...")

            # Load scalers
            with open(SCALER_X_PATH, "rb") as f:
                self.scaler_x = pickle.load(f)

            with open(SCALER_Y_PATH, "rb") as f:
                self.scaler_y = pickle.load(f)

            # Load feature columns
            with open(FEATURES_PATH, "rb") as f:
                self.feature_columns = pickle.load(f)

            # Load metadata
            with open(METADATA_PATH, "rb") as f:
                self.metadata = pickle.load(f)

            # Load LSTM model
            try:
                import tensorflow as tf

                self.lstm_model = tf.keras.models.load_model(str(LSTM_MODEL_PATH))
            except Exception as e:
                logger.warning(f"Could not load LSTM model: {e}")
                self.lstm_model = None

            self.models_loaded = True
            logger.info("✅ All models loaded successfully!")
            logger.info(
                f"   Model accuracy (R²): {self.metadata.get('test_r2', 'N/A')}"
            )
            logger.info(
                f"   Samples trained on: {self.metadata.get('training_samples', 'N/A')}"
            )

            return True

        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False

    def get_model_status(self) -> Dict[str, Any]:
        """Get current model status"""
        return {
            "models_loaded": self.models_loaded,
            "lstm_model": self.lstm_model is not None,
            "scalers": self.scaler_x is not None and self.scaler_y is not None,
            "metadata": self.metadata,
            "model_files": {
                "lstm": LSTM_MODEL_PATH.exists(),
                "scaler_x": SCALER_X_PATH.exists(),
                "scaler_y": SCALER_Y_PATH.exists(),
                "features": FEATURES_PATH.exists(),
                "metadata": METADATA_PATH.exists(),
            },
        }


class DataManager:
    """Manages data loading (real or sample)"""

    def __init__(self):
        self.use_real_data = False
        self.data = None
        self.data_source = "sample"

    def check_real_data(self) -> bool:
        """Check if real CEEW data exists in /datasets folder"""
        if not DATASETS_DIR.exists():
            logger.info(f"⚠️  Datasets folder not found at {DATASETS_DIR}")
            return False

        csv_files = list(DATASETS_DIR.glob("*.csv"))

        if len(csv_files) >= 1:
            logger.info(f"✅ Found {len(csv_files)} real dataset files in /datasets")
            self.use_real_data = True
            return True

        logger.info(f"⚠️  No CSV files found in /datasets")
        return False

    def load_real_data(self) -> Optional[pd.DataFrame]:
        """Load real CEEW dataset from /datasets folder"""
        try:
            logger.info("Loading real CEEW data from /datasets...")

            if not DATASETS_DIR.exists():
                logger.warning(f"Datasets folder not found at {DATASETS_DIR}")
                return None

            csv_files = sorted(list(DATASETS_DIR.glob("*.csv")))

            if not csv_files:
                logger.warning("No CSV files found in /datasets")
                return None

            logger.info(f"Found {len(csv_files)} files: {[f.name for f in csv_files]}")

            dfs = []
            for file in csv_files:
                try:
                    df = pd.read_csv(file)

                    # Standardize column names based on actual format
                    if "x_Timestamp" in df.columns:
                        df = df.rename(columns={"x_Timestamp": "timestamp"})
                    elif "Date" in df.columns:
                        df = df.rename(columns={"Date": "timestamp"})

                    if "t_kWh" in df.columns:
                        df = df.rename(columns={"t_kWh": "consumption_kwh"})

                    if "meter" in df.columns:
                        df = df.rename(columns={"meter": "meter_id"})

                    # Extract zone from filename if available
                    filename = file.name.lower()
                    if "bareilly" in filename or "br" in filename:
                        df["zone"] = "Bareilly"
                    elif "mathura" in filename or "mh" in filename:
                        df["zone"] = "Mathura"
                    else:
                        df["zone"] = "Unknown"

                    dfs.append(df)
                    logger.info(f"  ✓ Loaded {file.name}: {len(df):,} rows")

                except Exception as e:
                    logger.warning(f"  ✗ Error loading {file.name}: {e}")

            if dfs:
                combined = pd.concat(dfs, ignore_index=True)
                combined["timestamp"] = pd.to_datetime(combined["timestamp"])
                combined = combined.sort_values("timestamp").reset_index(drop=True)

                logger.info(
                    f"\n✅ Successfully loaded {len(combined):,} total records from real CEEW data"
                )
                logger.info(
                    f"   Date range: {combined['timestamp'].min()} to {combined['timestamp'].max()}"
                )
                logger.info(
                    f"   Duration: {(combined['timestamp'].max() - combined['timestamp'].min()).days} days"
                )

                self.data = combined
                self.data_source = "real_ceew"
                return combined

            return None

        except Exception as e:
            logger.error(f"Error loading real data: {e}")
            return None

    def load_or_generate_data(self) -> pd.DataFrame:
        """Load real data if available, otherwise use sample data"""
        if self.use_real_data:
            data = self.load_real_data()
            if data is not None:
                return data

        # Fallback to sample data if real data not available
        logger.info("⚠️  No real data available, generating sample data for demo...")
        return self._generate_sample_data()

    def _generate_sample_data(self, days: int = 90) -> pd.DataFrame:
        """Generate demo sample smart meter data (FALLBACK ONLY)"""
        logger.info(f"Generating demo sample data: {days} days")

        zones = ["Bareilly", "Mathura"]
        meters_per_zone = 5
        dates = pd.date_range(end=pd.Timestamp.now(), periods=days * 96, freq="15min")

        all_data = []

        for zone in zones:
            for meter_num in range(1, meters_per_zone + 1):
                hourly = 20 + 10 * np.sin(np.arange(len(dates)) * 2 * np.pi / (24 * 4))
                daily_noise = np.random.normal(0, 1.5, len(dates))
                weekly = 3 * np.sin(np.arange(len(dates)) * 2 * np.pi / (7 * 24 * 4))

                consumption = (
                    hourly + daily_noise + weekly + np.random.normal(0, 0.5, len(dates))
                )
                anomaly_mask = np.random.random(len(dates)) < 0.01
                consumption[anomaly_mask] *= np.random.choice(
                    [0.3, 2.5], np.sum(anomaly_mask)
                )
                consumption = np.maximum(consumption, 1)

                df = pd.DataFrame(
                    {
                        "timestamp": dates,
                        "meter_id": f"METER_{zone}_{meter_num:03d}",
                        "zone": zone,
                        "consumption_kwh": consumption,
                        "voltage": 230 + np.random.normal(0, 5, len(dates)),
                        "current": 10 + np.random.normal(0, 2, len(dates)),
                        "power_factor": 0.95 + np.random.normal(0, 0.02, len(dates)),
                    }
                )
                all_data.append(df)

        combined = pd.concat(all_data, ignore_index=True).sort_values("timestamp")

        logger.info(f"✅ Generated demo sample data: {len(combined)} records")
        self.data = combined
        self.data_source = "sample_demo"
        return combined

    def get_data_by_zone(self, zone: str) -> pd.DataFrame:
        """Get data for specific zone"""
        if self.data is None:
            if self.use_real_data:
                self.load_real_data()
            else:
                self._generate_sample_data()

        if zone == "All Zones":
            return self.data

        return self.data[self.data["zone"] == zone]


# Global instances
model_manager = ModelManager()
data_manager = DataManager()


def initialize_managers():
    """Initialize managers and log status"""
    logger.info("\n" + "=" * 70)
    logger.info("Initializing SmartGrid Model & Data Managers")
    logger.info("=" * 70)

    # Load models
    model_manager.load_models()

    # Check for real data in datasets folder
    real_data_available = data_manager.check_real_data()

    # Load real data if available
    if real_data_available:
        data_manager.load_real_data()

    # Log status
    status = model_manager.get_model_status()
    logger.info(f"\n📊 Model Status:")
    logger.info(f"   Models Loaded: {'✅' if status['models_loaded'] else '❌'}")
    logger.info(f"   LSTM Model: {'✅' if status['lstm_model'] else '❌'}")
    logger.info(f"   Scalers: {'✅' if status['scalers'] else '❌'}")

    logger.info(f"\n📁 Data Status:")
    logger.info(f"   Real Data Available: {'✅' if real_data_available else '❌'}")
    logger.info(f"   Data source: {data_manager.data_source}")

    if status["models_loaded"]:
        logger.info(f"   Using: Pre-trained models (from notebook training)")
    else:
        logger.info(f"   Using: Sample data with on-the-fly training")

    logger.info("=" * 70 + "\n")


def get_model_status_message() -> str:
    """Get human-readable model status message"""
    status = model_manager.get_model_status()

    if status["models_loaded"]:
        return "✅ **Using Pre-Trained Models** (from notebook training)"
    else:
        return "⚠️ **Using Sample Data & On-the-Fly Training** (Run notebook to use trained models)"
