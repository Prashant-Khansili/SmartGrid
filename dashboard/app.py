"""
Streamlit dashboard for smart meter intelligence
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Smart Meter Intelligence Dashboard", layout="wide")

st.title("🔌 Smart Meter Intelligence Dashboard")
st.markdown("AI-based demand forecasting and anomaly detection for BESCOM")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📊 Demand Forecasts", "⚠️ Anomalies", "📋 Audit Log"])

with tab1:
    st.header("Demand Forecasting")
    st.info("Forecast forecasts will be displayed here once models are trained")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Forecast Accuracy (MAPE)", "TBD", "TBD")
    with col2:
        st.metric("High-Risk Zones Flagged", "TBD", "TBD")

with tab2:
    st.header("Anomaly Detection")
    st.info("Detected anomalies will be displayed here once models are trained")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Meters Monitored", "TBD", "TBD")
    with col2:
        st.metric("Anomalies Detected", "TBD", "TBD")

with tab3:
    st.header("Audit Log")
    st.info("Prediction audit trail will be displayed here")
    
    st.text("Audit log file: outputs/audit_log.jsonl")

st.markdown("---")
st.markdown("*Dashboard auto-refreshes every 5 minutes*")
st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
