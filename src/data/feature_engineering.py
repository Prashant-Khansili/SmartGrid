"""
Feature engineering for time-series forecasting and anomaly detection
"""

import pandas as pd
import numpy as np
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Create features for forecasting and anomaly detection"""

    def __init__(self, df: pd.DataFrame, timestamp_col: str = "timestamp"):
        """
        Initialize FeatureEngineer

        Args:
            df: DataFrame with timestamp and consumption data
            timestamp_col: Name of timestamp column
        """
        self.df = df.copy()
        self.timestamp_col = timestamp_col
        logger.info(f"FeatureEngineer initialized")

    def create_temporal_features(self) -> "FeatureEngineer":
        """
        Create temporal features from timestamp

        Returns:
            Self for method chaining
        """
        logger.info("Creating temporal features...")

        if self.timestamp_col not in self.df.columns:
            logger.error(f"Timestamp column '{self.timestamp_col}' not found")
            return self

        # Ensure datetime
        self.df[self.timestamp_col] = pd.to_datetime(self.df[self.timestamp_col])

        # Extract features
        self.df["year"] = self.df[self.timestamp_col].dt.year
        self.df["month"] = self.df[self.timestamp_col].dt.month
        self.df["day"] = self.df[self.timestamp_col].dt.day
        self.df["hour"] = self.df[self.timestamp_col].dt.hour
        self.df["minute"] = self.df[self.timestamp_col].dt.minute
        self.df["dayofweek"] = self.df[self.timestamp_col].dt.dayofweek
        self.df["dayofyear"] = self.df[self.timestamp_col].dt.dayofyear
        self.df["quarter"] = self.df[self.timestamp_col].dt.quarter
        self.df["is_weekend"] = self.df["dayofweek"].isin([5, 6]).astype(int)

        logger.info("  ✓ Created temporal features")
        return self

    def create_cyclical_features(self) -> "FeatureEngineer":
        """
        Create cyclical features (sin/cos encoding of hour, month, etc.)

        Returns:
            Self for method chaining
        """
        logger.info("Creating cyclical features...")

        # Hour cyclical encoding
        self.df["hour_sin"] = np.sin(2 * np.pi * self.df["hour"] / 24)
        self.df["hour_cos"] = np.cos(2 * np.pi * self.df["hour"] / 24)

        # Month cyclical encoding
        self.df["month_sin"] = np.sin(2 * np.pi * self.df["month"] / 12)
        self.df["month_cos"] = np.cos(2 * np.pi * self.df["month"] / 12)

        # Day of week cyclical encoding
        self.df["dow_sin"] = np.sin(2 * np.pi * self.df["dayofweek"] / 7)
        self.df["dow_cos"] = np.cos(2 * np.pi * self.df["dayofweek"] / 7)

        logger.info("  ✓ Created cyclical features")
        return self

    def create_lag_features(
        self, column: str, lags: List[int] = None, groupby: str = None
    ) -> "FeatureEngineer":
        """
        Create lag features for time-series

        Args:
            column: Column to create lags for
            lags: List of lag values (e.g., [1, 24, 168])
            groupby: Column to group by before lagging (e.g., 'meter_id')

        Returns:
            Self for method chaining
        """
        if lags is None:
            lags = [1, 24, 168]  # 1, 24, 168 hour lags

        logger.info(f"Creating lag features for '{column}' with lags {lags}...")

        if groupby:
            for lag in lags:
                self.df[f"{column}_lag_{lag}"] = self.df.groupby(groupby)[column].shift(lag)
        else:
            for lag in lags:
                self.df[f"{column}_lag_{lag}"] = self.df[column].shift(lag)

        logger.info(f"  ✓ Created lag features")
        return self

    def create_rolling_features(
        self, column: str, windows: List[int] = None, groupby: str = None
    ) -> "FeatureEngineer":
        """
        Create rolling window statistics

        Args:
            column: Column to compute rolling stats for
            windows: List of window sizes (e.g., [24, 168])
            groupby: Column to group by

        Returns:
            Self for method chaining
        """
        if windows is None:
            windows = [24, 168]  # 24-hour and 7-day rolling windows

        logger.info(f"Creating rolling features for '{column}' with windows {windows}...")

        if groupby:
            grouped = self.df.groupby(groupby)
            for window in windows:
                self.df[f"{column}_rolling_mean_{window}"] = grouped[column].transform(
                    lambda x: x.rolling(window=window, min_periods=1).mean()
                )
                self.df[f"{column}_rolling_std_{window}"] = grouped[column].transform(
                    lambda x: x.rolling(window=window, min_periods=1).std()
                )
        else:
            for window in windows:
                self.df[f"{column}_rolling_mean_{window}"] = self.df[column].rolling(
                    window=window, min_periods=1
                ).mean()
                self.df[f"{column}_rolling_std_{window}"] = self.df[column].rolling(
                    window=window, min_periods=1
                ).std()

        logger.info(f"  ✓ Created rolling features")
        return self

    def create_deviation_features(
        self, column: str, reference_window: int = 168, groupby: str = None
    ) -> "FeatureEngineer":
        """
        Create deviation features for anomaly detection

        Args:
            column: Column to compute deviations for
            reference_window: Window size for computing reference mean
            groupby: Column to group by

        Returns:
            Self for method chaining
        """
        logger.info(f"Creating deviation features for '{column}'...")

        if groupby:
            grouped = self.df.groupby(groupby)
            self.df[f"{column}_deviation"] = grouped[column].transform(
                lambda x: x - x.rolling(window=reference_window, min_periods=1).mean()
            )
            self.df[f"{column}_deviation_pct"] = grouped[column].transform(
                lambda x: (x - x.rolling(window=reference_window, min_periods=1).mean())
                / x.rolling(window=reference_window, min_periods=1).mean()
            )
        else:
            rolling_mean = self.df[column].rolling(window=reference_window, min_periods=1).mean()
            self.df[f"{column}_deviation"] = self.df[column] - rolling_mean
            self.df[f"{column}_deviation_pct"] = (self.df[column] - rolling_mean) / rolling_mean

        logger.info("  ✓ Created deviation features")
        return self

    def handle_missing_features(self, method: str = "forward_fill") -> "FeatureEngineer":
        """
        Handle missing values in engineered features

        Args:
            method: 'forward_fill', 'backward_fill', or 'interpolate'

        Returns:
            Self for method chaining
        """
        logger.info(f"Handling missing feature values using '{method}'...")

        if method == "forward_fill":
            self.df = self.df.fillna(method="ffill")
        elif method == "backward_fill":
            self.df = self.df.fillna(method="bfill")
        elif method == "interpolate":
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numeric_cols] = self.df[numeric_cols].interpolate(method="linear")

        missing_count = self.df.isnull().sum().sum()
        logger.info(f"  ✓ Missing values: {missing_count}")

        return self

    def get_dataframe(self) -> pd.DataFrame:
        """Return engineered DataFrame"""
        logger.info(f"Returning engineered DataFrame with {len(self.df.columns)} features")
        return self.df
