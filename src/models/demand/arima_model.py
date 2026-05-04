"""
ARIMA forecasting model
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional
import logging
from statsmodels.tsa.arima.model import ARIMA
from src.models.base import BaseForecaster

logger = logging.getLogger(__name__)


class ARIMAForecaster(BaseForecaster):
    """ARIMA forecasting model"""

    def __init__(self, order: Tuple[int, int, int] = (1, 1, 1), name: str = "ARIMA"):
        super().__init__(name)
        self.order = order
        self.model = None

    def fit(self, y_train: pd.Series, **kwargs) -> None:
        """
        Fit ARIMA model to time series data

        Args:
            y_train: Time series data to fit
            **kwargs: Additional arguments for ARIMA
        """
        try:
            logger.info(f"Fitting {self.name} with order {self.order}...")
            self.model = ARIMA(y_train, order=self.order)
            self.fitted_model = self.model.fit()
            self.is_fitted = True
            logger.info(f"  ✓ {self.name} fitted successfully")
        except Exception as e:
            logger.error(f"Error fitting {self.name}: {e}")
            raise

    def predict(self, steps: int = 24) -> np.ndarray:
        """
        Make forecasts

        Args:
            steps: Number of steps to forecast

        Returns:
            Forecast values
        """
        if not self.is_fitted:
            logger.error(f"{self.name} not fitted yet")
            return None

        try:
            forecast = self.fitted_model.get_forecast(steps=steps)
            return forecast.predicted_mean.values
        except Exception as e:
            logger.error(f"Error predicting with {self.name}: {e}")
            return None

    def get_confidence_intervals(self, steps: int = 24, alpha: float = 0.05) -> Tuple[np.ndarray, np.ndarray]:
        """Get confidence intervals for forecasts"""
        if not self.is_fitted:
            logger.error(f"{self.name} not fitted yet")
            return None, None

        forecast = self.fitted_model.get_forecast(steps=steps)
        ci = forecast.conf_int(alpha=alpha)
        return ci.iloc[:, 0].values, ci.iloc[:, 1].values
