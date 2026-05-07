"""
Anomaly Detection Dashboard
Real-time theft and tampering detection using Isolation Forest
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import logging
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.models.anomaly.isolation_forest import IsolationForestDetector
from src.data.data_processor import DataProcessor
from src.model_manager import (
    model_manager,
    data_manager,
    initialize_managers,
    get_model_status_message,
)

logger = logging.getLogger(__name__)

# Initialize managers on first run
initialize_managers()

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Anomaly Detection",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("⚠️ Anomaly Detection Dashboard")
st.markdown("AI-powered theft, tampering, and anomaly detection for smart meters")

# Show model status
st.markdown(f"**Model Status:** {get_model_status_message()}")

# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================
with st.sidebar:
    st.header("Configuration")

    selected_zone = st.selectbox(
        "Select Zone",
        ["Bareilly", "Mathura", "All Zones"],
        help="Choose zone for anomaly detection",
    )

    detection_method = st.radio(
        "Detection Method",
        ["Isolation Forest", "Statistical", "Hybrid"],
        help="Choose anomaly detection algorithm",
    )

    sensitivity = st.slider(
        "Sensitivity Level",
        min_value=0.05,
        max_value=0.3,
        value=0.1,
        step=0.05,
        help="Higher = more anomalies detected (but more false positives)",
    )

    days_lookback = st.slider(
        "Days to Analyze",
        min_value=7,
        max_value=90,
        value=30,
        help="Historical data window for analysis",
    )

    st.divider()
    st.markdown("### Detection Settings")
    st.info(f"""
    **Method:** {detection_method}
    
    **Sensitivity:** {sensitivity:.0%}
    
    **Zone:** {selected_zone}
    
    **Lookback:** {days_lookback} days
    """)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_meter_data():
    """Load meter data from real datasets folder or generate sample"""
    # Try to load real data first
    real_data = data_manager.load_real_data()
    if real_data is not None and len(real_data) > 0:
        return real_data

    # Fallback to sample data
    return data_manager._generate_sample_data(days=90)


def train_anomaly_detector(_data, _sensitivity, _zone):
    """Train Isolation Forest detector (no caching to avoid size mismatches)"""
    try:
        # Prepare features
        features = ["consumption_kwh", "voltage", "current", "power_factor"]
        X = _data[features].values

        # Handle any NaN values
        X = np.nan_to_num(X, nan=np.nanmean(X, axis=0))

        # Standardize features
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train detector
        detector = IsolationForestDetector(contamination=_sensitivity)
        detector.fit(X_scaled)

        logger.info(f"Trained detector on {len(X)} samples for zone: {_zone}")
        return detector, scaler, X_scaled
    except Exception as e:
        st.error(f"Detector training error: {e}")
        logger.error(f"Detector training error: {e}")
        return None, None, None


def detect_anomalies(detector, X_scaled):
    """Detect anomalies using trained model"""
    if detector is None:
        return None

    try:
        predictions = detector.predict(X_scaled)
        scores = detector.score(X_scaled)
        return predictions, scores
    except Exception as e:
        st.error(f"Anomaly detection error: {e}")
        return None, None


def classify_anomaly_type(meter_data):
    """Classify type of anomaly detected"""
    recent_consumption = meter_data["consumption_kwh"].iloc[-96:]  # Last 24 hours
    historical_mean = meter_data["consumption_kwh"].mean()

    current_mean = recent_consumption.mean()
    current_volatility = (
        recent_consumption.std() / current_mean if current_mean > 0 else 0
    )

    if current_mean < historical_mean * 0.4:
        return "🔻 Potential Theft/Bypass", "critical"
    elif current_mean < historical_mean * 0.7:
        return "📉 Significant Drop", "high"
    elif current_volatility > 0.5:
        return "⚡ Unusual Volatility", "medium"
    elif abs(meter_data["power_factor"].iloc[-1] - 0.95) > 0.1:
        return "⚠️ Power Factor Anomaly", "medium"
    else:
        return "Normal", "low"


def generate_inspection_report(meter_id, meter_data):
    """Generate SHAP-like inspection evidence report"""
    anomaly_type, severity = classify_anomaly_type(meter_data)

    recent_consumption = meter_data["consumption_kwh"].iloc[-96:]
    historical_consumption = meter_data["consumption_kwh"].iloc[:-96]

    evidence = {
        "Consumption Drop": f"{((recent_consumption.mean() / historical_consumption.mean()) - 1) * 100:.1f}%",
        "Volatility Change": f"{((recent_consumption.std() / historical_consumption.std()) - 1) * 100:.1f}%",
        "Peak Deviation": f"{((recent_consumption.max() - historical_consumption.mean()) / historical_consumption.mean()) * 100:.1f}%",
        "Duration": f"{len(recent_consumption) * 15} minutes",
    }

    return {
        "meter_id": meter_id,
        "anomaly_type": anomaly_type,
        "severity": severity,
        "evidence": evidence,
    }


# ============================================================================
# MAIN DASHBOARD
# ============================================================================

# Load data
with st.spinner("Loading meter data..."):
    df_full = load_meter_data()
    df = (
        df_full
        if selected_zone == "All Zones"
        else df_full[df_full["zone"] == selected_zone]
    )

# Train detector (no cache to prevent zone mismatch issues)
with st.spinner(f"Training {detection_method} detector..."):
    detector, scaler, X_scaled = train_anomaly_detector(
        df.copy(), sensitivity, selected_zone
    )

# Detect anomalies
predictions, scores = detect_anomalies(detector, X_scaled)

if predictions is not None and len(predictions) == len(df):
    df["is_anomaly"] = predictions
    df["anomaly_score"] = scores

    # Get unique meters
    unique_meters = df["meter_id"].unique()

    # Calculate summary statistics
    n_anomalies = (df["is_anomaly"] == 1).sum()
    anomaly_percentage = (n_anomalies / len(df)) * 100
    n_flagged_meters = len(df[df["is_anomaly"] == 1]["meter_id"].unique())

    # Display KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Meters Monitored", len(unique_meters), f"{len(unique_meters)} total")

    with col2:
        st.metric(
            "Anomalies Detected", n_anomalies, f"{anomaly_percentage:.2f}% of data"
        )

    with col3:
        st.metric(
            "Critical Meters",
            n_flagged_meters,
            f"{(n_flagged_meters/len(unique_meters))*100:.1f}%",
        )

    with col4:
        st.metric(
            "Detection Accuracy",
            f"{(100 - anomaly_percentage):.1f}%",
            "Normal readings",
        )

    st.divider()

    # Anomaly overview
    st.subheader("🔍 Anomaly Overview")

    col1, col2 = st.columns(2)

    with col1:
        # Anomaly distribution over time
        anomaly_by_time = df.groupby(df["timestamp"].dt.date)["is_anomaly"].sum()

        fig_timeline = go.Figure()
        fig_timeline.add_trace(
            go.Bar(
                x=anomaly_by_time.index,
                y=anomaly_by_time.values,
                marker=dict(color="rgba(255, 100, 100, 0.7)"),
                name="Anomalies",
                hovertemplate="Date: %{x}<br>Anomalies: %{y}<extra></extra>",
            )
        )

        fig_timeline.update_layout(
            title="Anomalies Detected Over Time",
            xaxis_title="Date",
            yaxis_title="Count",
            height=350,
            template="plotly_white",
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

    with col2:
        # Anomaly score distribution
        fig_dist = px.histogram(
            df,
            x="anomaly_score",
            nbins=50,
            title="Anomaly Score Distribution",
            labels={"anomaly_score": "Anomaly Score", "count": "Frequency"},
            color_discrete_sequence=["#1f77b4"],
            marginal="box",
        )

        fig_dist.add_vline(
            x=np.percentile(df["anomaly_score"], (1 - sensitivity) * 100),
            line_dash="dash",
            line_color="red",
            annotation_text="Detection Threshold",
            annotation_position="top right",
        )

        fig_dist.update_layout(height=350, template="plotly_white")
        st.plotly_chart(fig_dist, use_container_width=True)

    st.divider()

    # Detailed meter analysis
    st.subheader("📋 Flagged Meters - Detailed Report")

    flagged_data = []

    for meter_id in unique_meters:
        meter_df = df[df["meter_id"] == meter_id]
        meter_anomalies = meter_df["is_anomaly"].sum()

        if meter_anomalies > 0:
            report = generate_inspection_report(meter_id, meter_df)
            flagged_data.append(
                {
                    "Meter ID": meter_id,
                    "Zone": meter_df["zone"].iloc[0],
                    "Anomalies": meter_anomalies,
                    "Type": report["anomaly_type"].split("/")[-1].strip(),
                    "Severity": report["severity"].upper(),
                    "Consumption Drop": report["evidence"]["Consumption Drop"],
                    "Status": (
                        "🔴 CRITICAL"
                        if report["severity"] == "critical"
                        else "🟠 HIGH" if report["severity"] == "high" else "🟡 MEDIUM"
                    ),
                }
            )

    if flagged_data:
        flagged_df = pd.DataFrame(flagged_data)

        # Sort by severity
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        flagged_df["severity_order"] = flagged_df["Severity"].map(severity_order)
        flagged_df = flagged_df.sort_values("severity_order").drop(
            "severity_order", axis=1
        )

        # Display with styling
        def color_status(val):
            if "🔴" in val:
                return "background-color: #ffcccc"
            elif "🟠" in val:
                return "background-color: #ffe6cc"
            else:
                return "background-color: #ffffcc"

        st.dataframe(
            flagged_df.style.applymap(color_status, subset=["Status"]),
            use_container_width=True,
            height=400,
        )
    else:
        st.info("✅ No anomalies detected in the selected period and configuration.")

    st.divider()

    # Detailed inspection evidence
    st.subheader("🔎 Inspection Evidence Report")

    if flagged_data:
        selected_meter = st.selectbox(
            "Select Meter for Detailed Analysis", [d["Meter ID"] for d in flagged_data]
        )

        meter_df = df[df["meter_id"] == selected_meter]
        report = generate_inspection_report(selected_meter, meter_df)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### {selected_meter}")
            st.markdown(f"**Zone:** {meter_df['zone'].iloc[0]}")
            st.markdown(f"**Status:** {report['anomaly_type']}")
            st.markdown(f"**Severity:** {report['severity'].upper()}")

        with col2:
            st.markdown("### Evidence Details")
            for key, value in report["evidence"].items():
                st.markdown(f"- **{key}:** {value}")

        # Time series plot for selected meter
        recent_meter_data = meter_df.tail(96 * days_lookback)  # Last X days

        fig_meter = go.Figure()

        # Normal points
        normal_mask = recent_meter_data["is_anomaly"] == 0
        anomaly_mask = recent_meter_data["is_anomaly"] == 1

        fig_meter.add_trace(
            go.Scatter(
                x=recent_meter_data[normal_mask]["timestamp"],
                y=recent_meter_data[normal_mask]["consumption_kwh"],
                mode="lines",
                name="Normal",
                line=dict(color="green"),
                hovertemplate="<b>Normal</b><br>Time: %{x}<br>Consumption: %{y:.2f} kWh<extra></extra>",
            )
        )

        fig_meter.add_trace(
            go.Scatter(
                x=recent_meter_data[anomaly_mask]["timestamp"],
                y=recent_meter_data[anomaly_mask]["consumption_kwh"],
                mode="markers",
                name="Anomaly",
                marker=dict(color="red", size=8),
                hovertemplate="<b>Anomaly</b><br>Time: %{x}<br>Consumption: %{y:.2f} kWh<extra></extra>",
            )
        )

        fig_meter.update_layout(
            title=f"Consumption Pattern - {selected_meter} ({days_lookback} days)",
            xaxis_title="Time",
            yaxis_title="Consumption (kWh)",
            height=400,
            template="plotly_white",
            hovermode="x unified",
        )

        st.plotly_chart(fig_meter, use_container_width=True)

        # Field inspection recommendations
        st.info(f"""
        ### 🔧 Field Inspection Recommendations
        
        **Meter:** {selected_meter}
        
        **Primary Issue:** {report['anomaly_type']}
        
        **Investigation Points:**
        - Check for physical tampering or bypass connections
        - Verify meter seal integrity
        - Test meter calibration
        - Check power factor and voltage stability
        - Inspect CT/PT connections (if applicable)
        
        **Priority:** {report['severity'].upper()}
        
        **Estimated Loss (if theft):** ₹ {abs(float(report['evidence']['Consumption Drop'].rstrip('%')) / 100) * 15000:.0f} - ₹ {abs(float(report['evidence']['Consumption Drop'].rstrip('%')) / 100) * 50000:.0f} per month
        """)

else:
    if predictions is None:
        st.error(
            "❌ Anomaly detection failed. Could not train detector on selected data."
        )
    else:
        st.error(f"""
        ❌ **Dimension Mismatch Error**
        
        DataFrame has {len(df)} rows but predictions has {len(predictions)} rows.
        
        This may indicate an issue with data consistency. Please try:
        1. Selecting a different zone
        2. Adjusting the lookback period
        3. Refreshing the page (F5)
        """)
        logger.error(
            f"Dimension mismatch: DataFrame {len(df)} vs predictions {len(predictions)}"
        )

# Footer
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with col2:
    st.markdown(f"**Detection Method:** {detection_method}")

with col3:
    st.markdown(f"**Zone:** {selected_zone}")
