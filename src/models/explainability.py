"""
Explainability utilities using SHAP
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ExplainabilityEngine:
    """Generate explainability for model predictions"""

    @staticmethod
    def calculate_shap_values(model, X: np.ndarray, sample_indices: Optional[list] = None):
        """
        Calculate SHAP values for model explanations

        Args:
            model: Trained model with predict method
            X: Feature matrix
            sample_indices: Specific samples to explain (None = all)

        Returns:
            SHAP values
        """
        try:
            import shap

            logger.info("Calculating SHAP values...")

            # Create explainer based on model type
            if hasattr(model, "predict"):
                explainer = shap.KernelExplainer(model.predict, X[:100])  # Use 100 samples as background
                shap_values = explainer.shap_values(X[sample_indices] if sample_indices else X)
                logger.info("  ✓ SHAP values calculated")
                return shap_values
            else:
                logger.warning("Model does not have predict method")
                return None

        except ImportError:
            logger.warning("SHAP not installed, skipping SHAP calculation")
            return None
        except Exception as e:
            logger.error(f"Error calculating SHAP values: {e}")
            return None

    @staticmethod
    def calculate_feature_importance(
        predictions: np.ndarray, features: np.ndarray, method: str = "correlation"
    ) -> Dict[str, float]:
        """
        Calculate feature importance for forecasts

        Args:
            predictions: Model predictions
            features: Feature matrix
            method: 'correlation' or 'permutation'

        Returns:
            Feature importance dictionary
        """
        try:
            logger.info(f"Calculating feature importance using {method}...")

            if method == "correlation":
                # Correlation-based importance
                correlations = np.corrcoef(features.T, predictions)[:-1, -1]
                correlations = np.abs(correlations)

            elif method == "permutation":
                # Permutation importance (simplified)
                baseline_error = np.mean((predictions - features.mean(axis=0)) ** 2)
                correlations = []
                for i in range(features.shape[1]):
                    perm_features = features.copy()
                    np.random.shuffle(perm_features[:, i])
                    perm_error = np.mean((predictions - perm_features.mean(axis=0)) ** 2)
                    correlations.append(baseline_error - perm_error)
                correlations = np.array(correlations)

            else:
                logger.error(f"Unknown method: {method}")
                return {}

            # Normalize to 0-1
            correlations = (correlations - correlations.min()) / (correlations.max() - correlations.min() + 1e-10)

            logger.info("  ✓ Feature importance calculated")
            return {"importances": correlations, "method": method}

        except Exception as e:
            logger.error(f"Error calculating feature importance: {e}")
            return {}

    @staticmethod
    def generate_anomaly_explanation(
        features: Dict[str, float], anomaly_threshold: float, triggering_features: list
    ) -> Dict[str, Any]:
        """
        Generate human-readable explanation for anomaly detection

        Args:
            features: Feature dictionary
            anomaly_threshold: Threshold that was exceeded
            triggering_features: Features that triggered the anomaly

        Returns:
            Explanation dictionary
        """
        explanation = {
            "reason": "Anomaly detected",
            "triggering_features": triggering_features,
            "feature_values": features,
            "threshold": anomaly_threshold,
            "explanation_text": f"Anomaly triggered by: {', '.join(triggering_features)}",
        }

        # Create severity score
        severity = len(triggering_features) / max(len(features), 1)
        explanation["severity"] = min(severity, 1.0)

        return explanation

    @staticmethod
    def get_forecast_decomposition(
        forecast: np.ndarray, seasonal_component: Optional[np.ndarray] = None, trend_component: Optional[np.ndarray] = None
    ) -> Dict[str, np.ndarray]:
        """
        Decompose forecast into components

        Args:
            forecast: Original forecast
            seasonal_component: Seasonal component (optional)
            trend_component: Trend component (optional)

        Returns:
            Decomposition dictionary
        """
        decomposition = {
            "forecast": forecast,
            "seasonal": seasonal_component,
            "trend": trend_component,
        }

        if seasonal_component is not None and trend_component is not None:
            residual = forecast - seasonal_component - trend_component
            decomposition["residual"] = residual

        return decomposition
