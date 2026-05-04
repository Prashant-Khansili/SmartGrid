"""
Data masking and anonymization utilities
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class DataMasker:
    """Mask or anonymize sensitive meter and zone data"""

    def __init__(self):
        self.meter_mapping = {}
        self.zone_mapping = {}
        logger.info("DataMasker initialized")

    def mask_meter_ids(self, df: pd.DataFrame, meter_col: str = "meter_id") -> pd.DataFrame:
        """
        Replace meter IDs with anonymous IDs

        Args:
            df: DataFrame with meter IDs
            meter_col: Column name containing meter IDs

        Returns:
            DataFrame with masked meter IDs
        """
        df_masked = df.copy()

        if meter_col in df_masked.columns:
            unique_meters = df_masked[meter_col].unique()

            for i, meter_id in enumerate(unique_meters):
                masked_id = f"M{i:06d}"
                self.meter_mapping[meter_id] = masked_id
                df_masked.loc[df_masked[meter_col] == meter_id, meter_col] = masked_id

            logger.info(f"Masked {len(unique_meters)} unique meter IDs")

        return df_masked

    def mask_zone_names(self, df: pd.DataFrame, zone_col: str = "zone") -> pd.DataFrame:
        """
        Replace zone names with codes

        Args:
            df: DataFrame with zone names
            zone_col: Column name containing zone names

        Returns:
            DataFrame with masked zone names
        """
        df_masked = df.copy()

        if zone_col in df_masked.columns:
            unique_zones = df_masked[zone_col].unique()

            for i, zone in enumerate(unique_zones):
                masked_zone = f"Z{i:02d}"
                self.zone_mapping[zone] = masked_zone
                df_masked.loc[df_masked[zone_col] == zone, zone_col] = masked_zone

            logger.info(f"Masked {len(unique_zones)} unique zones")

        return df_masked

    def get_reverse_mapping(self) -> Dict:
        """Get reverse mapping for unmask if needed"""
        return {
            "meters": {v: k for k, v in self.meter_mapping.items()},
            "zones": {v: k for k, v in self.zone_mapping.items()},
        }
