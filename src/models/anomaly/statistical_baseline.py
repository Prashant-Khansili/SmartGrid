"""
Statistical baseline anomaly detection (z-score, IQR)
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple
import logging
from src.models.base import BaseAnomalyDetector

logger = logging.getLogger(__name__)


class StatisticalBaseline(BaseAnomalyDetector):
    """Statistical baseline for anomaly detection"""

    def __init__(
        self,
        zscore_threshold: float = 3.0,
        iqr_multiplier: float = 1.5,
        name: str = "StatisticalBaseline",
    ):
        super().__init__(name, contamination=None)
        self.zscore_threshold = zscore_threshold
        self.iqr_multiplier = iqr_multiplier
        self.mean = None
        self.std = None
        self.q1 = None
        self.q3 = None
        self.iqr = None

    def fit(self, X: np.ndarray, **kwargs) -> None:
        """
        Calculate statistical parameters

        Args:
            X: Feature matrix or 1D array
        """
        try:
            logger.info(f"Fitting {self.name}...")

            if X.ndim == 1:
                X = X.reshape(-1, 1)

            # Calculate statistics
            self.mean = np.mean(X, axis=0)
            self.std = np.std(X, axis=0)
            self.q1 = np.percentile(X, 25, axis=0)
            self.q3 = np.percentile(X, 75, axis=0)
            self.iqr = self.q3 - self.q1

            self.is_fitted = True
            logger.info(f"  ✓ {self.name} fitted")

        except Exception as e:
            logger.error(f"Error fitting {self.name}: {e}")
            raise

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict anomalies using z-score method

        Args:
            X: Feature matrix or 1D array

        Returns:
            1 for anomaly, 0 for normal
        """
        if not self.is_fitted:
            logger.error(f"{self.name} not fitted yet")
            return None

        try:
            if X.ndim == 1:
                X = X.reshape(-1, 1)

            # Z-score method
            z_scores = np.abs((X - self.mean) / (self.std + 1e-10))
            z_anomalies = (z_scores > self.zscore_threshold).astype(int)

            # IQR method
            lower_bound = self.q1 - self.iqr_multiplier * self.iqr
            upper_bound = self.q3 + self.iqr_multiplier * self.iqr
            iqr_anomalies = ((X < lower_bound) | (X > upper_bound)).astype(int)

            # Combine (anomaly if either method flags)
            predictions = np.maximum(z_anomalies, iqr_anomalies)

            if predictions.shape[1] == 1:
                return predictions.flatten()
            return predictions

        except Exception as e:
            logger.error(f"Error predicting with {self.name}: {e}")
            return None

    def score(self, X: np.ndarray) -> np.ndarray:
        """
        Get anomaly scores based on z-scores

        Args:
            X: Feature matrix or 1D array

        Returns:
            Anomaly scores (0-1 range)
        """
        if not self.is_fitted:
            logger.error(f"{self.name} not fitted yet")
            return None

        try:
            if X.ndim == 1:
                X = X.reshape(-1, 1)

            z_scores = np.abs((X - self.mean) / (self.std + 1e-10))

            # Convert to 0-1 range
            scores = np.minimum(z_scores / self.zscore_threshold, 1.0)

            if scores.shape[1] == 1:
                return scores.flatten()
            return scores

        except Exception as e:
            logger.error(f"Error getting scores from {self.name}: {e}")
            return None
