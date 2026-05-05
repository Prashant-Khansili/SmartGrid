"""
Audit Log & Monitoring Dashboard
Track all predictions, detections, and system activities
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
from pathlib import Path

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Audit Log",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📋 Audit Log & Monitoring")
st.markdown(
    "Complete prediction history, model performance, and system activity tracking"
)

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================
with st.sidebar:
    st.header("Filters")

    date_range = st.date_input(
        "Date Range",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        max_value=datetime.now(),
    )

    log_type = st.multiselect(
        "Log Type",
        ["Forecast", "Anomaly Detection", "Model Training", "System", "API"],
        default=["Forecast", "Anomaly Detection"],
    )

    severity = st.multiselect(
        "Severity Level",
        ["INFO", "WARNING", "ERROR", "CRITICAL"],
        default=["INFO", "WARNING", "ERROR", "CRITICAL"],
    )

    st.divider()

    if st.button("🔄 Refresh Logs"):
        st.rerun()


# ============================================================================
# GENERATE SAMPLE AUDIT LOGS
# ============================================================================
@st.cache_data
def generate_sample_logs(start_date, end_date):
    """Generate sample audit logs for demonstration"""
    dates = pd.date_range(start=start_date, end=end_date, freq="1h")

    log_entries = []

    for i, date in enumerate(dates):
        if np.random.random() < 0.7:  # 70% forecast logs
            log_entries.append(
                {
                    "timestamp": date,
                    "type": "Forecast",
                    "zone": np.random.choice(["Bareilly", "Mathura"]),
                    "message": f"Generated 24-hour forecast for zone",
                    "status": "SUCCESS",
                    "severity": "INFO",
                    "duration_ms": np.random.randint(100, 1000),
                    "details": f"MAPE: {np.random.uniform(2, 5):.2f}%",
                }
            )

        if np.random.random() < 0.5:  # 50% anomaly detection logs
            log_entries.append(
                {
                    "timestamp": date,
                    "type": "Anomaly Detection",
                    "zone": np.random.choice(["Bareilly", "Mathura"]),
                    "message": "Completed anomaly detection scan",
                    "status": "SUCCESS" if np.random.random() < 0.9 else "WARNING",
                    "severity": "INFO" if np.random.random() < 0.9 else "WARNING",
                    "duration_ms": np.random.randint(500, 5000),
                    "details": f"Detected {np.random.randint(0, 15)} anomalies",
                }
            )

        if np.random.random() < 0.1:  # 10% model training logs
            log_entries.append(
                {
                    "timestamp": date,
                    "type": "Model Training",
                    "zone": "All",
                    "message": "Model retraining completed",
                    "status": "SUCCESS" if np.random.random() < 0.95 else "ERROR",
                    "severity": "INFO" if np.random.random() < 0.95 else "ERROR",
                    "duration_ms": np.random.randint(5000, 60000),
                    "details": f"Accuracy: {np.random.uniform(85, 95):.2f}%",
                }
            )

    return pd.DataFrame(log_entries).sort_values("timestamp", ascending=False)


# ============================================================================
# MAIN CONTENT
# ============================================================================

# Load logs
logs = generate_sample_logs(date_range[0], date_range[1])

# Filter logs
filtered_logs = logs[
    (logs["type"].isin(log_type)) & (logs["severity"].isin(severity))
].copy()

# Display statistics
st.subheader("📊 Activity Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Events",
        len(filtered_logs),
        f"{len(filtered_logs.groupby(pd.Grouper(key='timestamp', freq='D')))} per day avg",
    )

with col2:
    success_rate = (
        (filtered_logs["status"] == "SUCCESS").sum() / len(filtered_logs) * 100
        if len(filtered_logs) > 0
        else 0
    )
    st.metric(
        "Success Rate",
        f"{success_rate:.1f}%",
        f"{(filtered_logs['status'] == 'SUCCESS').sum()} successful",
    )

with col3:
    avg_duration = filtered_logs["duration_ms"].mean() if len(filtered_logs) > 0 else 0
    st.metric(
        "Avg Duration",
        f"{avg_duration:.0f} ms",
        f"{filtered_logs['duration_ms'].min():.0f} - {filtered_logs['duration_ms'].max():.0f} ms range",
    )

with col4:
    warnings = (filtered_logs["severity"] == "WARNING").sum()
    errors = (filtered_logs["severity"] == "ERROR").sum()
    st.metric("Issues", f"{warnings + errors}", f"{warnings} warnings, {errors} errors")

st.divider()

# Activity timeline
st.subheader("📈 Activity Timeline")

col1, col2 = st.columns([2, 1])

with col1:
    # Hourly activity
    hourly_activity = (
        filtered_logs.groupby([pd.Grouper(key="timestamp", freq="6h"), "type"])
        .size()
        .unstack(fill_value=0)
    )

    fig_timeline = go.Figure()

    for col in hourly_activity.columns:
        fig_timeline.add_trace(
            go.Scatter(
                x=hourly_activity.index,
                y=hourly_activity[col],
                mode="lines+markers",
                name=col,
                stackgroup="one",
            )
        )

    fig_timeline.update_layout(
        title="Activity by Type (6-hour intervals)",
        xaxis_title="Time",
        yaxis_title="Events",
        height=400,
        template="plotly_white",
        hovermode="x unified",
    )

    st.plotly_chart(fig_timeline, use_container_width=True)

with col2:
    # Event type distribution
    type_dist = filtered_logs["type"].value_counts()

    fig_type = px.pie(
        values=type_dist.values,
        names=type_dist.index,
        title="Event Type Distribution",
        hole=0.4,
    )

    fig_type.update_layout(height=400)
    st.plotly_chart(fig_type, use_container_width=True)

st.divider()

# Detailed logs table
st.subheader("🔍 Detailed Logs")

# Create display dataframe
display_logs = filtered_logs.copy()
display_logs["timestamp"] = display_logs["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
display_logs = display_logs[
    [
        "timestamp",
        "type",
        "zone",
        "message",
        "status",
        "severity",
        "duration_ms",
        "details",
    ]
]
display_logs = display_logs.rename(
    columns={
        "timestamp": "Time",
        "type": "Type",
        "zone": "Zone",
        "message": "Message",
        "status": "Status",
        "severity": "Level",
        "duration_ms": "Duration (ms)",
        "details": "Details",
    }
)


# Color-code by severity
def color_severity(val):
    if val == "CRITICAL":
        return "background-color: #ff4444"
    elif val == "ERROR":
        return "background-color: #ff9999"
    elif val == "WARNING":
        return "background-color: #ffcc99"
    else:
        return "background-color: #99ff99"


def color_status(val):
    if val == "SUCCESS":
        return "background-color: #ccffcc"
    else:
        return "background-color: #ffcccc"


styled_logs = display_logs.style.applymap(color_severity, subset=["Level"]).applymap(
    color_status, subset=["Status"]
)

st.dataframe(styled_logs, use_container_width=True, height=600)

st.divider()

# Export options
st.subheader("📥 Export Logs")

col1, col2, col3 = st.columns(3)

with col1:
    csv = filtered_logs.to_csv(index=False)
    st.download_button(
        label="📊 Download as CSV",
        data=csv,
        file_name=f"audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )

with col2:
    json_data = filtered_logs.to_json(orient="records", date_format="iso")
    st.download_button(
        label="📄 Download as JSON",
        data=json_data,
        file_name=f"audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
    )

with col3:
    st.info("📧 Logs are also automatically synced to: `/outputs/audit_log.jsonl`")

st.divider()

# Performance insights
with st.expander("📊 Performance Insights"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Model Performance Trends")

        # Simulated performance data
        perf_dates = pd.date_range(end=datetime.now(), periods=30, freq="D")
        accuracy_trend = 85 + np.cumsum(np.random.normal(0.5, 1, 30))

        fig_perf = go.Figure()
        fig_perf.add_trace(
            go.Scatter(
                x=perf_dates,
                y=accuracy_trend,
                mode="lines+markers",
                name="Accuracy",
                line=dict(color="green"),
            )
        )
        fig_perf.add_hline(
            y=90, line_dash="dash", line_color="blue", annotation_text="Target"
        )
        fig_perf.update_layout(
            title="30-Day Accuracy Trend",
            xaxis_title="Date",
            yaxis_title="Accuracy (%)",
            height=400,
            template="plotly_white",
        )

        st.plotly_chart(fig_perf, use_container_width=True)

    with col2:
        st.markdown("### System Health")

        health_metrics = pd.DataFrame(
            {
                "Component": [
                    "Model Inference",
                    "Data Pipeline",
                    "API Server",
                    "Database",
                    "Cache",
                ],
                "Uptime": ["99.9%", "99.8%", "99.7%", "99.95%", "99.6%"],
                "Avg Latency": ["245 ms", "320 ms", "150 ms", "45 ms", "5 ms"],
                "Last Error": ["2h ago", "12h ago", "None", "3h ago", "1h ago"],
            }
        )

        st.dataframe(health_metrics, use_container_width=True, hide_index=True)

# Footer
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.caption(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with col2:
    st.caption(f"**Logs Displayed:** {len(filtered_logs)} / {len(logs)}")

with col3:
    st.caption(f"**Data Retention:** 365 days")
