"""
Audit logging for predictions and model inputs
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd

logger = logging.getLogger(__name__)


class AuditLogger:
    """Log all model predictions for auditability"""

    def __init__(self, log_file: str = "outputs/audit_log.jsonl"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Audit logger initialized: {self.log_file}")

    def log_prediction(
        self,
        prediction_type: str,
        model_name: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        model_version: str = "1.0",
        metadata: Optional[Dict] = None,
    ) -> None:
        """
        Log a prediction with full audit trail

        Args:
            prediction_type: 'forecast' or 'anomaly'
            model_name: Name of model used
            inputs: Input features/data
            outputs: Model predictions
            model_version: Model version
            metadata: Additional metadata
        """
        try:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "prediction_type": prediction_type,
                "model_name": model_name,
                "model_version": model_version,
                "inputs": self._serialize(inputs),
                "outputs": self._serialize(outputs),
                "metadata": metadata or {},
            }

            # Append to log file
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")

            logger.info(
                f"Logged {prediction_type} prediction from {model_name} v{model_version}"
            )

        except Exception as e:
            logger.error(f"Error logging prediction: {e}")

    def log_model_training(
        self,
        model_name: str,
        parameters: Dict[str, Any],
        metrics: Dict[str, float],
        training_data_size: int,
        model_version: str = "1.0",
    ) -> None:
        """
        Log model training event

        Args:
            model_name: Name of model
            parameters: Model parameters
            metrics: Training metrics
            training_data_size: Size of training data
            model_version: Model version
        """
        try:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "event_type": "model_training",
                "model_name": model_name,
                "model_version": model_version,
                "parameters": self._serialize(parameters),
                "metrics": metrics,
                "training_data_size": training_data_size,
            }

            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")

            logger.info(f"Logged training for {model_name} v{model_version}")

        except Exception as e:
            logger.error(f"Error logging model training: {e}")

    def get_prediction_history(self, limit: int = 100) -> pd.DataFrame:
        """
        Retrieve recent prediction history

        Args:
            limit: Maximum number of entries to retrieve

        Returns:
            DataFrame with prediction history
        """
        try:
            entries = []
            with open(self.log_file, "r") as f:
                for i, line in enumerate(f):
                    if i >= len(self) - limit:
                        entries.append(json.loads(line))

            return pd.DataFrame(entries) if entries else pd.DataFrame()

        except Exception as e:
            logger.error(f"Error reading prediction history: {e}")
            return pd.DataFrame()

    @staticmethod
    def _serialize(obj: Any) -> Any:
        """Serialize objects for JSON logging"""
        if isinstance(obj, (dict, list)):
            return obj
        elif isinstance(obj, (pd.DataFrame, pd.Series)):
            return obj.to_dict()
        elif isinstance(obj, (np.ndarray)):
            return obj.tolist()
        else:
            try:
                return float(obj)
            except:
                return str(obj)

    def __len__(self) -> int:
        """Get number of log entries"""
        try:
            count = 0
            with open(self.log_file, "r") as f:
                for _ in f:
                    count += 1
            return count
        except:
            return 0


# Global audit logger instance
audit_logger = AuditLogger()


import numpy as np
