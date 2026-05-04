"""
Exponential Smoothing forecasting model
"""

import numpy as np
import pandas as pd
from typing import Tuple
import logging
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from src.models.base import BaseForecaster

logger = logging.getLogger(__name__)


class ExponentialSmoothingForecaster(BaseForecaster):
    """Exponential Smoothing forecasting model"""

    def __init__(
        self,
        trend: str = "add",
        seasonal: str = "add",
        seasonal_periods: int = 168,
        name: str = "ExponentialSmoothing",
    ):
        super().__init__(name)
        self.trend = trend
        self.seasonal = seasonal
        self.seasonal_periods = seasonal_periods
        self.model = None

    def fit(self, y_train: pd.Series, **kwargs) -> None:
        """
        Fit Exponential Smoothing model

        Args:
            y_train: Time series data to fit
            **kwargs: Additional arguments
        """
        try:
            logger.info(f"Fitting {self.name}...")
            self.model = ExponentialSmoothing(
                y_train,
                trend=self.trend,
                seasonal=self.seasonal,
                seasonal_periods=self.seasonal_periods,
                initialization_method="estimated",
            )
            self.fitted_model = self.model.fit(optimized=True)
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
            forecast = self.fitted_model.forecast(steps=steps)
            return forecast.values
        except Exception as e:
            logger.error(f"Error predicting with {self.name}: {e}")
            return None
