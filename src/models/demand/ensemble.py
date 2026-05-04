"""
Ensemble forecasting combining ARIMA, Exponential Smoothing, and LSTM
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, List
import logging
from src.models.base import BaseForecaster
from src.models.demand.arima_model import ARIMAForecaster
from src.models.demand.exponential_smoothing import ExponentialSmoothingForecaster
from src.models.demand.lstm_model import LSTMForecaster

logger = logging.getLogger(__name__)


class EnsembleForecaster(BaseForecaster):
    """Ensemble forecaster combining multiple models"""

    def __init__(
        self,
        arima_weight: float = 0.3,
        exp_smooth_weight: float = 0.3,
        lstm_weight: float = 0.4,
        arima_order: Tuple = (1, 1, 1),
        lstm_lookback: int = 168,
        optimize_weights: bool = False,
    ):
        super().__init__("EnsembleForecaster")
        self.arima_weight = arima_weight
        self.exp_smooth_weight = exp_smooth_weight
        self.lstm_weight = lstm_weight
        self.arima_order = arima_order
        self.lstm_lookback = lstm_lookback
        self.optimize_weights = optimize_weights

        # Initialize component models
        self.arima = ARIMAForecaster(order=arima_order)
        self.exp_smooth = ExponentialSmoothingForecaster()
        self.lstm = LSTMForecaster(lookback=lstm_lookback)

        self.is_fitted = False

    def fit(self, y_train: pd.Series, y_val: pd.Series = None, **kwargs) -> None:
        """
        Fit all component models

        Args:
            y_train: Training time series
            y_val: Validation set for weight optimization (optional)
            **kwargs: Additional arguments
        """
        try:
            logger.info("Fitting ensemble components...")

            # Fit each model
            logger.info("  1. Fitting ARIMA...")
            self.arima.fit(y_train)

            logger.info("  2. Fitting Exponential Smoothing...")
            self.exp_smooth.fit(y_train)

            logger.info("  3. Fitting LSTM...")
            self.lstm.fit(y_train)

            # Optimize weights on validation set if provided
            if self.optimize_weights and y_val is not None:
                logger.info("  4. Optimizing ensemble weights on validation set...")
                self._optimize_weights(y_train, y_val)

            self.is_fitted = True
            logger.info("  ✓ Ensemble fitted successfully")

        except Exception as e:
            logger.error(f"Error fitting ensemble: {e}")
            raise

    def predict(self, y_recent: pd.Series, steps: int = 24) -> Dict[str, np.ndarray]:
        """
        Make ensemble forecasts

        Args:
            y_recent: Recent values for context
            steps: Number of steps to forecast

        Returns:
            Dictionary with forecasts and metadata
        """
        if not self.is_fitted:
            logger.error("Ensemble not fitted yet")
            return None

        try:
            logger.info(f"Making {steps}-step ensemble forecast...")

            # Get predictions from each model
            arima_forecast = self.arima.predict(steps=steps)
            exp_smooth_forecast = self.exp_smooth.predict(steps=steps)
            lstm_forecast = self.lstm.predict(y_recent.values, steps=steps)

            # Combine forecasts with weights
            ensemble_forecast = (
                self.arima_weight * arima_forecast
                + self.exp_smooth_weight * exp_smooth_forecast
                + self.lstm_weight * lstm_forecast
            )

            # Get confidence intervals
            arima_ci_lower, arima_ci_upper = self.arima.get_confidence_intervals(steps=steps)

            result = {
                "ensemble_forecast": ensemble_forecast,
                "arima_forecast": arima_forecast,
                "exp_smooth_forecast": exp_smooth_forecast,
                "lstm_forecast": lstm_forecast,
                "confidence_lower": arima_ci_lower,
                "confidence_upper": arima_ci_upper,
                "weights": {
                    "arima": self.arima_weight,
                    "exp_smooth": self.exp_smooth_weight,
                    "lstm": self.lstm_weight,
                },
            }

            logger.info("  ✓ Ensemble forecast complete")
            return result

        except Exception as e:
            logger.error(f"Error making ensemble prediction: {e}")
            return None

    def _optimize_weights(self, y_train: pd.Series, y_val: pd.Series) -> None:
        """
        Optimize ensemble weights based on validation set performance

        Args:
            y_train: Training data (for reference)
            y_val: Validation data
        """
        from scipy.optimize import minimize
        from sklearn.metrics import mean_absolute_percentage_error

        def objective(weights):
            """MSE objective for optimization"""
            w_arima, w_exp, w_lstm = weights
            w_sum = w_arima + w_exp + w_lstm

            # Get forecasts
            arima_f = self.arima.predict(steps=len(y_val))
            exp_f = self.exp_smooth.predict(steps=len(y_val))
            lstm_f = self.lstm.predict(y_train.values[-self.lstm_lookback :], steps=len(y_val))

            # Normalize weights
            w_arima_norm = w_arima / w_sum
            w_exp_norm = w_exp / w_sum
            w_lstm_norm = w_lstm / w_sum

            # Ensemble forecast
            ensemble_f = w_arima_norm * arima_f + w_exp_norm * exp_f + w_lstm_norm * lstm_f

            # Calculate error
            return np.mean((y_val.values - ensemble_f) ** 2)

        # Optimize
        result = minimize(
            objective,
            x0=[self.arima_weight, self.exp_smooth_weight, self.lstm_weight],
            method="Nelder-Mead",
            options={"maxiter": 100},
        )

        # Update weights
        w_opt = result.x
        w_sum = w_opt.sum()
        self.arima_weight = w_opt[0] / w_sum
        self.exp_smooth_weight = w_opt[1] / w_sum
        self.lstm_weight = w_opt[2] / w_sum

        logger.info(
            f"  Optimized weights: ARIMA={self.arima_weight:.3f}, "
            f"ExpSmooth={self.exp_smooth_weight:.3f}, LSTM={self.lstm_weight:.3f}"
        )
