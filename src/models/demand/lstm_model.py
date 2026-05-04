"""
LSTM deep learning forecasting model
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional
import logging
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from src.models.base import BaseForecaster

logger = logging.getLogger(__name__)


class LSTMForecaster(BaseForecaster):
    """LSTM neural network forecasting model"""

    def __init__(
        self,
        lookback: int = 168,
        hidden_units: int = 64,
        dropout_rate: float = 0.2,
        epochs: int = 100,
        batch_size: int = 32,
        name: str = "LSTM",
    ):
        super().__init__(name)
        self.lookback = lookback
        self.hidden_units = hidden_units
        self.dropout_rate = dropout_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None
        self.scaler = None

    def _create_sequences(self, data: np.ndarray, lookback: int) -> Tuple[np.ndarray, np.ndarray]:
        """Create sequences for LSTM training"""
        X, y = [], []
        for i in range(len(data) - lookback):
            X.append(data[i : i + lookback])
            y.append(data[i + lookback])
        return np.array(X), np.array(y)

    def fit(self, y_train: pd.Series, **kwargs) -> None:
        """
        Fit LSTM model to time series data

        Args:
            y_train: Time series data to fit
            **kwargs: Additional arguments
        """
        try:
            logger.info(f"Fitting {self.name}...")

            # Normalize data
            from sklearn.preprocessing import MinMaxScaler

            self.scaler = MinMaxScaler()
            y_scaled = self.scaler.fit_transform(y_train.values.reshape(-1, 1))

            # Create sequences
            X, y = self._create_sequences(y_scaled, self.lookback)

            # Split into train/validation
            split_idx = int(len(X) * 0.8)
            X_train, X_val = X[:split_idx], X[split_idx:]
            y_train_seq, y_val = y[:split_idx], y[split_idx:]

            # Build model
            self.model = Sequential(
                [
                    LSTM(self.hidden_units, activation="relu", input_shape=(self.lookback, 1)),
                    Dropout(self.dropout_rate),
                    Dense(32, activation="relu"),
                    Dropout(self.dropout_rate),
                    Dense(1),
                ]
            )

            self.model.compile(optimizer="adam", loss="mse", metrics=["mae"])

            # Train model
            early_stop = EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)

            self.model.fit(
                X_train,
                y_train_seq,
                validation_data=(X_val, y_val),
                epochs=self.epochs,
                batch_size=self.batch_size,
                callbacks=[early_stop],
                verbose=0,
            )

            self.is_fitted = True
            logger.info(f"  ✓ {self.name} fitted successfully")

        except Exception as e:
            logger.error(f"Error fitting {self.name}: {e}")
            raise

    def predict(self, y_recent: np.ndarray, steps: int = 24) -> np.ndarray:
        """
        Make forecasts

        Args:
            y_recent: Recent values to use as context (must be >= lookback)
            steps: Number of steps to forecast

        Returns:
            Forecast values
        """
        if not self.is_fitted or self.model is None:
            logger.error(f"{self.name} not fitted yet")
            return None

        try:
            # Scale input
            y_scaled = self.scaler.transform(y_recent.reshape(-1, 1))

            # Take last lookback values
            current_sequence = y_scaled[-self.lookback :].reshape(1, self.lookback, 1)

            forecasts = []
            for _ in range(steps):
                next_pred = self.model.predict(current_sequence, verbose=0)
                forecasts.append(next_pred[0, 0])

                # Update sequence
                current_sequence = np.append(current_sequence[0, 1:, :], [[next_pred[0, 0]]], axis=0)
                current_sequence = current_sequence.reshape(1, self.lookback, 1)

            # Inverse scale
            forecasts = np.array(forecasts).reshape(-1, 1)
            forecasts = self.scaler.inverse_transform(forecasts)

            return forecasts.flatten()

        except Exception as e:
            logger.error(f"Error predicting with {self.name}: {e}")
            return None
