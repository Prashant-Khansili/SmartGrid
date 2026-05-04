"""
Data loader for CEEW Smart Meter dataset from Kaggle
Loads and combines raw CSV files from Bareilly and Mathura
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Load CEEW smart meter data from Kaggle dataset"""

    BAREILLY_FILES = [
        "CEEW - Smart meter data Bareilly 2019.csv",
        "CEEW - Smart meter data Bareilly 2020.csv",
        "CEEW - Smart meter data Bareilly 2021.csv",
    ]

    MATHURA_FILES = [
        "CEEW - Smart meter data Mathura 2019.csv",
        "CEEW - Smart meter data Mathura 2020.csv",
        "CEEW - Smart meter data Mathura 2021.csv",
    ]

    def __init__(self, data_dir: str = "data/raw"):
        """
        Initialize DataLoader

        Args:
            data_dir: Path to directory containing raw CSV files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"DataLoader initialized with data_dir: {self.data_dir}")

    def load_raw_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load raw CSV files from data directory

        Returns:
            Dictionary with keys 'bareilly' and 'mathura', values are DataFrames
        """
        data = {}

        # Load Bareilly data
        bareilly_dfs = []
        for file in self.BAREILLY_FILES:
            filepath = self.data_dir / file
            if filepath.exists():
                logger.info(f"Loading {file}...")
                try:
                    df = pd.read_csv(filepath)
                    bareilly_dfs.append(df)
                    logger.info(f"  ✓ Loaded {len(df)} rows")
                except Exception as e:
                    logger.error(f"  ✗ Error loading {file}: {e}")
            else:
                logger.warning(f"  ✗ File not found: {filepath}")

        if bareilly_dfs:
            data["bareilly"] = pd.concat(bareilly_dfs, ignore_index=True)
            logger.info(f"Bareilly data: {len(data['bareilly'])} total rows")
        else:
            logger.warning("No Bareilly files found")

        # Load Mathura data
        mathura_dfs = []
        for file in self.MATHURA_FILES:
            filepath = self.data_dir / file
            if filepath.exists():
                logger.info(f"Loading {file}...")
                try:
                    df = pd.read_csv(filepath)
                    mathura_dfs.append(df)
                    logger.info(f"  ✓ Loaded {len(df)} rows")
                except Exception as e:
                    logger.error(f"  ✗ Error loading {file}: {e}")
            else:
                logger.warning(f"  ✗ File not found: {filepath}")

        if mathura_dfs:
            data["mathura"] = pd.concat(mathura_dfs, ignore_index=True)
            logger.info(f"Mathura data: {len(data['mathura'])} total rows")
        else:
            logger.warning("No Mathura files found")

        return data

    def combine_data(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Combine Bareilly and Mathura data into single DataFrame

        Args:
            data: Dictionary with 'bareilly' and 'mathura' DataFrames

        Returns:
            Combined DataFrame with zone column
        """
        dfs = []

        if "bareilly" in data:
            df_bareilly = data["bareilly"].copy()
            df_bareilly["zone"] = "Bareilly"
            dfs.append(df_bareilly)

        if "mathura" in data:
            df_mathura = data["mathura"].copy()
            df_mathura["zone"] = "Mathura"
            dfs.append(df_mathura)

        if not dfs:
            raise ValueError("No data to combine")

        combined = pd.concat(dfs, ignore_index=True)
        logger.info(f"Combined data: {len(combined)} rows, {len(combined.columns)} columns")
        logger.info(f"Zones: {combined['zone'].unique()}")

        return combined

    def inspect_data_structure(self, df: pd.DataFrame) -> None:
        """
        Print data structure information

        Args:
            df: DataFrame to inspect
        """
        logger.info("\n" + "=" * 60)
        logger.info("DATA STRUCTURE INSPECTION")
        logger.info("=" * 60)
        logger.info(f"Shape: {df.shape}")
        logger.info(f"\nColumns: {df.columns.tolist()}")
        logger.info(f"\nData types:\n{df.dtypes}")
        logger.info(f"\nFirst few rows:\n{df.head()}")
        logger.info(f"\nData info:")
        logger.info(df.info(verbose=False))
        logger.info(f"\nBasic statistics:\n{df.describe()}")
        logger.info(f"\nMissing values:\n{df.isnull().sum()}")

    def get_file_status(self) -> Dict[str, bool]:
        """
        Check which required files are present

        Returns:
            Dictionary with filename -> exists mapping
        """
        status = {}
        for file in self.BAREILLY_FILES + self.MATHURA_FILES:
            filepath = self.data_dir / file
            status[file] = filepath.exists()
        return status

    @staticmethod
    def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names to lowercase and remove special characters

        Args:
            df: DataFrame with raw column names

        Returns:
            DataFrame with standardized column names
        """
        # Common pattern in CEEW data: x_Timestamp, t_kWh, z_Avg Voltage, etc.
        new_columns = {}
        for col in df.columns:
            # Remove prefix (x_, y_, z_, t_)
            clean_col = col.strip()
            if "_" in clean_col and len(clean_col.split("_")[0]) == 1:
                clean_col = clean_col.split("_", 1)[1]

            # Lowercase and replace spaces with underscores
            clean_col = clean_col.lower().replace(" ", "_").replace("(", "").replace(")", "")
            new_columns[col] = clean_col

        df_std = df.rename(columns=new_columns)
        logger.info(f"Standardized column names. Original: {len(df.columns)} → {len(df_std.columns)}")
        return df_std
