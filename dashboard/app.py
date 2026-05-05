"""
Smart Meter Intelligence Dashboard - Main Hub
AI-powered demand forecasting and anomaly detection for BESCOM
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Smart Meter Intelligence Hub",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🔌 Smart Meter Intelligence Hub")
st.markdown("""
**AI-Powered Energy Loss Detection & Demand Forecasting for BESCOM**

Navigate using the sidebar to access:
- 📊 **Demand Forecasting** - Short-term electricity demand predictions
- ⚠️ **Anomaly Detection** - Theft and tampering identification
""")

st.divider()

# ============================================================================
# MAIN DASHBOARD OVERVIEW
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🔴 Critical Alerts", value="12", delta="+3 today", delta_color="inverse"
    )

with col2:
    st.metric(label="⚡ Meters Monitored", value="15,432", delta="+234 this month")

with col3:
    st.metric(label="📈 Forecast Accuracy", value="91.4%", delta="+2.3%")

with col4:
    st.metric(
        label="💰 Est. Loss (Monthly)",
        value="₹ 4.2 Cr",
        delta="-12% vs last month",
        delta_color="inverse",
    )

st.divider()

# ============================================================================
# SYSTEM STATUS
# ============================================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 System Status")

    status_data = pd.DataFrame(
        {
            "Component": [
                "Demand Forecasting",
                "Anomaly Detection",
                "Data Pipeline",
                "API Server",
            ],
            "Status": ["🟢 Healthy", "🟢 Healthy", "🟢 Healthy", "🟢 Healthy"],
            "Last Update": [
                "2024-03-15 14:32:15",
                "2024-03-15 14:31:48",
                "2024-03-15 14:30:22",
                "2024-03-15 14:29:58",
            ],
            "Uptime": ["99.8%", "99.8%", "99.9%", "99.9%"],
        }
    )

    st.dataframe(status_data, use_container_width=True, hide_index=True)

with col2:
    st.subheader("🎯 Key Metrics")

    metrics_data = pd.DataFrame(
        {
            "Metric": [
                "Avg Demand Forecast Error",
                "Anomaly Detection Precision",
                "False Positive Rate",
                "Avg Detection Latency",
            ],
            "Value": ["3.2%", "94.7%", "5.1%", "2.3 minutes"],
            "Target": ["< 5%", "> 90%", "< 10%", "< 5 min"],
            "Status": ["✅", "✅", "✅", "✅"],
        }
    )

    st.dataframe(metrics_data, use_container_width=True, hide_index=True)

st.divider()

# ============================================================================
# RECENT ACTIVITY
# ============================================================================

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("⚠️ Recent Anomalies (Last 7 Days)")

    recent_anomalies = pd.DataFrame(
        {
            "Meter ID": [
                "METER_BRL_001",
                "METER_MTH_045",
                "METER_BRL_089",
                "METER_MTH_012",
                "METER_BRL_156",
            ],
            "Zone": ["Bareilly", "Mathura", "Bareilly", "Mathura", "Bareilly"],
            "Type": ["Drop 65%", "Volatility", "Drop 48%", "Power Factor", "Drop 72%"],
            "Date": [
                "2024-03-15",
                "2024-03-14",
                "2024-03-13",
                "2024-03-12",
                "2024-03-11",
            ],
            "Status": [
                "🔴 Critical",
                "🟡 Medium",
                "🔴 Critical",
                "🟡 Medium",
                "🔴 Critical",
            ],
        }
    )

    st.dataframe(recent_anomalies, use_container_width=True, hide_index=True)

with col2:
    st.subheader("📊 Demand Forecast Summary")

    forecast_summary = pd.DataFrame(
        {
            "Zone": ["Bareilly", "Mathura", "Combined"],
            "Avg Demand (24h)": ["145.2 kWh", "132.8 kWh", "278.0 kWh"],
            "Peak Expected": ["178.5 kWh", "165.3 kWh", "343.8 kWh"],
            "Risk Level": ["🟢 Normal", "🟢 Normal", "🟢 Normal"],
        }
    )

    st.dataframe(forecast_summary, use_container_width=True, hide_index=True)

st.divider()

# ============================================================================
# QUICK START GUIDE
# ============================================================================

st.subheader("🚀 Quick Start")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("""
        ### 📊 Demand Forecasting
        
        View short-term electricity demand predictions with:
        - Hourly forecasts (24-168 hours)
        - Confidence intervals
        - Risk assessments
        - Zone-level aggregation
        
        **→ Go to Demand Forecasting**
        """)

with col2:
    with st.container(border=True):
        st.markdown("""
        ### ⚠️ Anomaly Detection
        
        Identify suspicious consumption patterns:
        - Real-time monitoring
        - Three-layer detection system
        - Inspection evidence reports
        - Priority-ranked alerts
        
        **→ Go to Anomaly Detection**
        """)

with col3:
    with st.container(border=True):
        st.markdown("""
        ### 📋 Audit Log
        
        Track all predictions and detections:
        - Full prediction history
        - Model performance metrics
        - User actions & timestamps
        - Export capabilities
        
        **→ Go to Audit Log**
        """)

st.divider()

# ============================================================================
# SYSTEM INFORMATION
# ============================================================================

with st.expander("ℹ️ System Information"):
    info_col1, info_col2, info_col3 = st.columns(3)

    with info_col1:
        st.markdown("""
        **Models Deployed**
        - Demand: LSTM Ensemble
        - Anomaly: Isolation Forest + Statistical
        - Version: 1.2.0
        """)

    with info_col2:
        st.markdown("""
        **Data Coverage**
        - Meters: 15,432
        - Zones: 2 (Bareilly, Mathura)
        - History: 3 years
        - Update Frequency: 15 minutes
        """)

    with info_col3:
        st.markdown("""
        **Performance**
        - Avg Latency: 2.3s
        - Model Accuracy: 91.4%
        - System Uptime: 99.8%
        - Last Training: 2024-03-10
        """)

# ============================================================================
# FOOTER
# ============================================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.caption(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with col2:
    st.caption("**Environment:** Production v1.2.0")

with col3:
    st.caption("**Support:** analytics@bescom.co.in")
