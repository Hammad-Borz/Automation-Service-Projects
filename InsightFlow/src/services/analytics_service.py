import pandas as pd
from src.core.analytics_engine import analyze


def run_analytics(frame: pd.DataFrame, high_value_threshold: float, anomaly_z_threshold: float) -> dict:
    return analyze(frame, high_value_threshold, anomaly_z_threshold)
