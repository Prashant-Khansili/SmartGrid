"""
Base classes for forecasting and anomaly detection models
"""

from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from typing import Dict, Tuple, Any
import logging

logger = logging.getLogger(__name__)


class BaseForecaster(ABC):
    """Base class for forecasting models"""

    def __init__(self, name: str):
        self.name = name
        self.is_fitted = False
        self.model = None

    @abstractmethod
    def fit(self, X_train: np.ndarray, y_train: np.ndarray, **kwargs) -> None:
        """Fit the model to training data"""
        pass

    @abstractmethod
    def predict(self, X_test: np.ndarray, **kwargs) -> np.ndarray:
        """Make predictions on test data"""
        pass

    def get_params(self) -> Dict[str, Any]:
        """Get model parameters"""
        raise NotImplementedError

    def set_params(self, **params) -> None:
        """Set model parameters"""
        raise NotImplementedError


class BaseAnomalyDetector(ABC):
    """Base class for anomaly detection models"""

    def __init__(self, name: str, contamination: float = 0.1):
        self.name = name
        self.contamination = contamination
        self.is_fitted = False
        self.model = None

    @abstractmethod
    def fit(self, X: np.ndarray, **kwargs) -> None:
        """Fit the model to data"""
        pass

    @abstractmethod
    def predict(self, X: np.ndarray, **kwargs) -> np.ndarray:
        """Predict anomalies (1 for anomaly, 0 for normal)"""
        pass

    @abstractmethod
    def score(self, X: np.ndarray, **kwargs) -> np.ndarray:
        """Get anomaly scores (higher = more anomalous)"""
        pass

    def get_params(self) -> Dict[str, Any]:
        """Get model parameters"""
        raise NotImplementedError

    def set_params(self, **params) -> None:
        """Set model parameters"""
        raise NotImplementedError
