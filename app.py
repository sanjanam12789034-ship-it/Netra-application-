import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page setup
st.set_page_config(page_title="Netra | Analytics Platform", layout="wide")
st.title("Netra: Social Media Analytics Platform")
st.caption("Real-time sentiment monitoring, trend volume, and misinformation early warning system")

# Sidebar controls
st.sidebar.header("Controls")
topic_filter = st.sidebar.selectbox("Select Monitored Topic", ["All Topics", "Environment", "Economy", "Health", "Technology", "Science"])
min_score = st.sidebar.slider("Minimum Post Engagement Score", min_value=0, max_value=500, value=50)

# Embedded baseline dataset
base_time = datetime.now()
data = [
    {
        "title": "SHOCKING truth about water supply exposed! Wake up before it's deleted!",
        "topic": "Environment",
        "sentiment_score": -0.82,
        "sentiment_label": "Negative",
        "misinfo_probability": 0.94,
        "engagement_score": 480,
        "time_offset": "15m ago"
    },
    {
        "title": "Quarterly trade review indicates stable baseline economic growth",
        "topic": "Economy",
        "sentiment_score": 0.45,
        "sentiment_label": "Positive",
        "misinfo_probability": 0.08,
        "engagement_score": 140,
        "time_offset": "45m ago"
    },
    {
        "title": "Secret miracle health remedy cured everything in 24 hours, doctors silent",
        "topic": "Health",
        "sentiment_score": -0.61,
        "sentiment_label": "Negative",
        "misinfo_probability": 0.89,
        "engagement_score": 310,
        "time_offset": "1h ago"
    },
    {
        "title": "Local municipal council approves timeline for new metro transit line",
        "topic": "Economy",
        "sentiment_score": 0.65,
        "sentiment_label": "Positive",
        "misinfo_probability": 0.04,
        "engagement_score": 95,
        "time_offset": "2h ago"
    },
    {
        "title": "Unverified reports claim secret weather experiment caused local outage",
        "topic": "Technology",
        "sentiment_score": -0.73,
        "sentiment_label": "Negative",
        "misinfo_probability": 0.87,
        "engagement_score": 520,
        "time_offset": "3h ago"
    },
    {
        "title": "Space agency releases high-resolution panoramic imaging from satellite",
        "topic": "Science",
        "sentiment_score": 0.58,
        "sentiment_label": "Positive",
        "misinfo_probability": 0.05,
        "engagement_score": 230,
        "time_offset": "4h ago"
    }
]

df = pd.DataFrame(data)

# Filtering logic
if topic_filter != "All Topics":
    filtered_df = df[df["topic"] == topic_filter].copy()
else:
    filtered_df = df.copy()

filtered_df = filtered_df[filtered_df["engagement_score"] >= min_score]
filtered_df["high_risk"] = (filtered_df["misinfo_probability"] >= 0.70) & (filtered_df["sentiment_label"] == "Negative")

# Top KPI Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Analyzed Posts", len(filtered_df))
col2.metric("Flagged Narratives", int(filtered_df["high_risk"].sum()) if not filtered_df.empty else 0)
col3.metric("Negative Sentiment", f"{(filtered_df['sentiment_label'] == 'Negative').mean():.0%}" if not filtered_df.empty else "0%")
col4.metric("Avg Misinfo Score", f"{filtered_df['misinfo_probability'].mean():.2f}" if not filtered_df.empty else "0.00")

st.divider()

# Native Streamlit Visualizations (Requires no extra libraries)
c1, c2 = st.columns(2)

with c1:
    st.subheader("Sentiment Count")
    if not filtered_df.empty:
        sentiment_counts = filtered_df["sentiment_label"].value_counts()
        st.bar_chart(sentiment_counts)
    else:
        st.write("No data matching filters.")

with c2:
    st.subheader("Misinformation Risk Scores")
    if not filtered_df.empty:
        chart_data = filtered_df.set_index("title")["misinfo_probability"]
        st.bar_chart(chart_data)
    else:
        st.write("No data matching filters.")

# Alert Queue Table
st.subheader("Priority Alert Queue (Flagged Narratives)")
alerts = filtered_df[filtered_df["high_risk"]][["title", "topic", "sentiment_label", "misinfo_probability", "engagement_score"]]

if not alerts.empty:
    st.dataframe(alerts, use_container_width=True)
else:
    st.success("No high-risk narratives match current filters.")
