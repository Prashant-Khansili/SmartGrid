"""
Unit tests for data loading and processing
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.data.data_loader import DataLoader
from src.data.data_processor import DataProcessor


class TestDataLoader:
    """Tests for DataLoader"""

    def test_loader_initialization(self):
        """Test DataLoader initialization"""
        loader = DataLoader(data_dir="data/raw")
        assert loader.data_dir == Path("data/raw")

    def test_file_status(self):
        """Test file status checking"""
        loader = DataLoader(data_dir="data/raw")
        status = loader.get_file_status()
        assert isinstance(status, dict)
        assert len(status) > 0


class TestDataProcessor:
    """Tests for DataProcessor"""

    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        dates = pd.date_range("2021-01-01", periods=100, freq="15min")
        df = pd.DataFrame({
            "timestamp": dates,
            "kwh": np.random.rand(100) * 10,
            "zone": ["Bareilly"] * 50 + ["Mathura"] * 50,
        })
        return df

    def test_processor_initialization(self, sample_data):
        """Test DataProcessor initialization"""
        processor = DataProcessor(sample_data)
        assert processor.original_shape == sample_data.shape

    def test_timestamp_standardization(self, sample_data):
        """Test timestamp standardization"""
        processor = DataProcessor(sample_data, timestamp_col="timestamp")
        processor.standardize_timestamps()
        assert pd.api.types.is_datetime64_any_dtype(processor.df["timestamp"])

    def test_missing_value_handling(self, sample_data):
        """Test missing value handling"""
        sample_data.loc[0, "kwh"] = np.nan
        processor = DataProcessor(sample_data)
        processor.handle_missing_values(strategy="forward_fill")
        assert processor.df.isnull().sum().sum() == 0


if __name__ == "__main__":
    pytest.main([__file__])
