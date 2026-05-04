"""
Theme 8: AI-Based Smart Meter Intelligence & Loss Detection
Smart meter data analysis for demand forecasting and anomaly detection
"""

__version__ = "0.1.0"
__author__ = "AI for Bharat"
__description__ = "Smart meter intelligence system for BESCOM"

from src.data.data_loader import DataLoader
from src.data.data_processor import DataProcessor
from src.data.feature_engineering import FeatureEngineer

__all__ = [
    "DataLoader",
    "DataProcessor",
    "FeatureEngineer",
]
