"""
Tests for anomaly detection models
"""

import pytest
import numpy as np
from src.models.anomaly.isolation_forest import IsolationForestDetector
from src.models.anomaly.statistical_baseline import StatisticalBaseline


class TestIsolationForest:
    """Tests for Isolation Forest detector"""

    @pytest.fixture
    def sample_data(self):
        """Create sample data"""
        normal_data = np.random.normal(0, 1, (100, 5))
        anomaly_data = np.random.normal(5, 1, (10, 5))
        return np.vstack([normal_data, anomaly_data])

    def test_initialization(self):
        """Test detector initialization"""
        detector = IsolationForestDetector(contamination=0.1)
        assert detector.contamination == 0.1
        assert not detector.is_fitted

    def test_fit_predict(self, sample_data):
        """Test fit and predict"""
        detector = IsolationForestDetector(contamination=0.1)
        detector.fit(sample_data)
        predictions = detector.predict(sample_data)
        assert predictions is not None
        assert len(predictions) == len(sample_data)


class TestStatisticalBaseline:
    """Tests for Statistical Baseline detector"""

    @pytest.fixture
    def sample_data(self):
        """Create sample data"""
        return np.random.normal(0, 1, (100, 5))

    def test_initialization(self):
        """Test detector initialization"""
        detector = StatisticalBaseline(zscore_threshold=3.0)
        assert detector.zscore_threshold == 3.0
        assert not detector.is_fitted

    def test_fit_predict(self, sample_data):
        """Test fit and predict"""
        detector = StatisticalBaseline()
        detector.fit(sample_data)
        predictions = detector.predict(sample_data)
        assert predictions is not None


if __name__ == "__main__":
    pytest.main([__file__])
