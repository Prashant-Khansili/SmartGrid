"""
Isolation Forest anomaly detection
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple
import logging
from sklearn.ensemble import IsolationForest
from src.models.base import BaseAnomalyDetector

logger = logging.getLogger(__name__)


class IsolationForestDetector(BaseAnomalyDetector):
    """Isolation Forest-based anomaly detector"""

    def __init__(
        self,
        contamination: float = 0.1,
        n_estimators: int = 100,
        max_samples: str = "auto",
        random_state: int = 42,
        name: str = "IsolationForest",
    ):
        super().__init__(name, contamination)
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.random_state = random_state

    def fit(self, X: np.ndarray, **kwargs) -> None:
        """
        Fit Isolation Forest model

        Args:
            X: Feature matrix (n_samples, n_features)
            **kwargs: Additional arguments
        """
        try:
            logger.info(f"Fitting {self.name}...")
            self.model = IsolationForest(
                contamination=self.contamination,
                n_estimators=self.n_estimators,
                max_samples=self.max_samples,
                random_state=self.random_state,
            )
            self.model.fit(X)
            self.is_fitted = True
            logger.info(f"  ✓ {self.name} fitted on {len(X)} samples")
        except Exception as e:
            logger.error(f"Error fitting {self.name}: {e}")
            raise

    def predict(self, X: np.ndarray, threshold: float = None) -> np.ndarray:
        """
        Predict anomalies

        Args:
            X: Feature matrix
            threshold: Custom anomaly threshold (optional)

        Returns:
            1 for anomaly, 0 for normal
        """
        if not self.is_fitted:
            logger.error(f"{self.name} not fitted yet")
            return None

        try:
            predictions = self.model.predict(X)
            # Convert -1 (anomaly) to 1, and 1 (normal) to 0
            return ((predictions == -1) * 1).astype(int)
        except Exception as e:
            logger.error(f"Error predicting with {self.name}: {e}")
            return None

    def score(self, X: np.ndarray) -> np.ndarray:
        """
        Get anomaly scores (higher = more anomalous)

        Args:
            X: Feature matrix

        Returns:
            Anomaly scores
        """
        if not self.is_fitted:
            logger.error(f"{self.name} not fitted yet")
            return None

        try:
            # Get decision function (lower = more anomalous)
            scores = self.model.score_samples(X)
            # Convert to 0-1 range where 1 = most anomalous
            scores = -scores  # Invert so higher = more anomalous
            scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-10)
            return scores
        except Exception as e:
            logger.error(f"Error getting scores from {self.name}: {e}")
            return None

    def get_params(self) -> Dict:
        """Get model parameters"""
        return {
            "contamination": self.contamination,
            "n_estimators": self.n_estimators,
            "max_samples": self.max_samples,
            "random_state": self.random_state,
        }

    def set_params(self, **params) -> None:
        """Set model parameters"""
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
