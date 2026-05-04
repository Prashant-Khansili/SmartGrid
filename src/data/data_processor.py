"""
Data processor for cleaning, validation, and time-series aggregation
"""

import pandas as pd
import numpy as np
from typing import Tuple, List
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Clean, validate, and aggregate smart meter data"""

    def __init__(self, df: pd.DataFrame, timestamp_col: str = "timestamp"):
        """
        Initialize DataProcessor

        Args:
            df: Raw DataFrame
            timestamp_col: Name of timestamp column
        """
        self.df = df.copy()
        self.timestamp_col = timestamp_col
        self.original_shape = self.df.shape
        logger.info(f"DataProcessor initialized with {self.original_shape[0]} rows")

    def standardize_timestamps(self) -> "DataProcessor":
        """
        Convert timestamp column to datetime format

        Returns:
            Self for method chaining
        """
        logger.info("Standardizing timestamps...")

        # Try to parse timestamp column
        if self.timestamp_col in self.df.columns:
            try:
                self.df[self.timestamp_col] = pd.to_datetime(self.df[self.timestamp_col])
                logger.info(f"  ✓ Parsed {self.timestamp_col}")
            except Exception as e:
                logger.error(f"  ✗ Error parsing {self.timestamp_col}: {e}")
        else:
            # Try to find timestamp column by name pattern
            timestamp_candidates = [col for col in self.df.columns if "time" in col.lower()]
            if timestamp_candidates:
                self.timestamp_col = timestamp_candidates[0]
                logger.info(f"  Found timestamp column: {self.timestamp_col}")
                self.df[self.timestamp_col] = pd.to_datetime(self.df[self.timestamp_col])
            else:
                logger.warning("  ✗ No timestamp column found")

        return self

    def handle_missing_values(self, strategy: str = "forward_fill") -> "DataProcessor":
        """
        Handle missing values in the dataset

        Args:
            strategy: 'forward_fill', 'backward_fill', 'interpolate', or 'drop'

        Returns:
            Self for method chaining
        """
        logger.info(f"Handling missing values using '{strategy}' strategy...")
        missing_before = self.df.isnull().sum().sum()

        if strategy == "forward_fill":
            self.df = self.df.fillna(method="ffill")
        elif strategy == "backward_fill":
            self.df = self.df.fillna(method="bfill")
        elif strategy == "interpolate":
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numeric_cols] = self.df[numeric_cols].interpolate(method="linear")
        elif strategy == "drop":
            self.df = self.df.dropna()

        missing_after = self.df.isnull().sum().sum()
        logger.info(f"  ✓ Missing values: {missing_before} → {missing_after}")

        return self

    def remove_outliers(self, columns: List[str] = None, threshold: float = 3.0) -> "DataProcessor":
        """
        Remove outliers using z-score method

        Args:
            columns: List of columns to check (None = all numeric)
            threshold: Z-score threshold for outlier detection

        Returns:
            Self for method chaining
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()

        logger.info(f"Removing outliers (z-score > {threshold}) from {len(columns)} columns...")
        rows_before = len(self.df)

        for col in columns:
            if col in self.df.columns:
                z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
                self.df = self.df[z_scores < threshold]

        rows_after = len(self.df)
        logger.info(f"  ✓ Rows: {rows_before} → {rows_after} ({rows_after/rows_before*100:.1f}%)")

        return self

    def aggregate_to_interval(
        self, interval: str = "15min", consumption_col: str = "kwh"
    ) -> pd.DataFrame:
        """
        Aggregate data from 3-minute to specified interval (15-min or hourly)

        Args:
            interval: Pandas frequency string ('15min', 'H' for hourly, etc.)
            consumption_col: Name of consumption column (will be summed)

        Returns:
            Aggregated DataFrame
        """
        logger.info(f"Aggregating data to {interval} intervals...")

        if self.timestamp_col not in self.df.columns:
            logger.error("Timestamp column not found. Call standardize_timestamps() first.")
            return self.df

        # Find consumption column
        if consumption_col not in self.df.columns:
            # Try to find it by pattern
            candidates = [col for col in self.df.columns if "kwh" in col.lower()]
            if candidates:
                consumption_col = candidates[0]
                logger.info(f"  Using consumption column: {consumption_col}")
            else:
                logger.error(f"Consumption column '{consumption_col}' not found")
                return self.df

        # Set timestamp as index and aggregate
        df_agg = self.df.set_index(self.timestamp_col)

        # Group by meter/zone and timestamp, then aggregate
        numeric_cols = df_agg.select_dtypes(include=[np.number]).columns

        agg_dict = {col: "sum" if col == consumption_col else "mean" for col in numeric_cols}

        df_agg = df_agg.groupby([pd.Grouper(freq=interval)]).agg(agg_dict)

        logger.info(f"  ✓ Aggregated to {len(df_agg)} rows")

        return df_agg.reset_index()

    def create_meter_zone_mapping(
        self, meter_col: str = None, zone_col: str = "zone"
    ) -> pd.DataFrame:
        """
        Create mapping of meter IDs to zones

        Args:
            meter_col: Name of meter column
            zone_col: Name of zone column

        Returns:
            DataFrame with meter → zone mapping
        """
        if meter_col is None:
            # Try to find meter column
            candidates = [col for col in self.df.columns if "meter" in col.lower()]
            if candidates:
                meter_col = candidates[0]
            else:
                logger.warning("No meter column found")
                return None

        mapping = self.df[[meter_col, zone_col]].drop_duplicates()
        logger.info(f"Created meter→zone mapping: {len(mapping)} unique meters")
        return mapping

    def get_statistics(self) -> dict:
        """
        Get summary statistics of the processed data

        Returns:
            Dictionary with statistics
        """
        stats = {
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "date_range": None,
            "null_count": self.df.isnull().sum().sum(),
            "duplicates": self.df.duplicated().sum(),
            "memory_mb": self.df.memory_usage(deep=True).sum() / 1024**2,
        }

        if self.timestamp_col in self.df.columns:
            stats["date_range"] = (
                self.df[self.timestamp_col].min(),
                self.df[self.timestamp_col].max(),
            )

        logger.info(f"Data statistics: {stats}")
        return stats
