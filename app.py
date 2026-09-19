import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(page_title="Netra | Analytics Platform", layout="wide")
st.title("Netra: Social Media Analytics Platform")
st.caption("Real-time sentiment monitoring, trend volume, and misinformation early warning system")

# Sidebar controls
st.sidebar.header("Controls")
min_score = st.sidebar.slider("Minimum Engagement Score", min_value=0, max_value=500, value=50)

# Embedded dataset matching the SIH project architecture
base_time = datetime.now()
data = [
    {
        "title": "SHOCKING truth about water supply exposed! Wake up before it's deleted!",
        "topic": "Environment",
        "sentiment_score": -0.82,
        "sentiment_label": "Negative",
        "misinfo_probability": 0.94,
        "engagement_score": 480,
        "created_at": base_time - timedelta(minutes=15)
    },
    {
        "title": "Quarterly trade review indicates stable baseline economic growth",
        "topic": "Economy",
        "sentiment_score": 0.45,
        "sentiment_label": "Positive",
        "misinfo_probability": 0.08,
        "engagement_score": 140,
        "created_at": base_time - timedelta(minutes=45)
    },
    {
        "title": "Secret miracle health remedy cured everything in 24 hours, doctors silent",
        "topic": "Health",
        "sentiment_score": -0.61,
        "sentiment_label": "Negative",
        "misinfo_probability": 0.89,
        "engagement_score": 310,
        "created_at": base_time - timedelta(hours=1, minutes=20)
    },
    {
        "title": "Local municipal council approves timeline for new metro transit line",
        "topic": "Infrastructure",
        "sentiment_score": 0.65,
        "sentiment_label": "Positive",
        "misinfo_probability": 0.04,
        "engagement_score": 95,
        "created_at": base_time - timedelta(hours=2)
    },
    {
        "title": "Unverified reports claim secret weather experiment caused local outage",
        "topic": "Technology",
        "sentiment_score": -0.73,
        "sentiment_label": "Negative",
        "misinfo_probability": 0.87,
        "engagement_score": 520,
        "created_at": base_time - timedelta(hours=3, minutes=10)
    },
    {
        "title": "Space agency releases high-resolution panoramic imaging from satellite",
        "topic": "Science",
        "sentiment_score": 0.58,
        "sentiment_label": "Positive",
        "misinfo_probability": 0.05,
        "engagement_score": 230,
        "created_at": base_time - timedelta(hours=4)
    }
]

df = pd.DataFrame(data)
filtered_df = df[df["engagement_score"] >= min_score].copy()
filtered_df["high_risk"] = (filtered_df["misinfo_probability"] >= 0.70) & (filtered_df["sentiment_label"] == "Negative")

# Top Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Analyzed Posts", len(filtered_df))
col2.metric("Flagged Narratives", int(filtered_df["high_risk"].sum()))
col3.metric("Negative Sentiment Rate", f"{(filtered_df['sentiment_label'] == 'Negative').mean():.0%}")
col4.metric("Avg Misinfo Risk", f"{filtered_df['misinfo_probability'].mean():.2f}")

st.divider()

# Visualization Section
c1, c2 = st.columns(2)
with c1:
    st.subheader("Sentiment Distribution")
    fig_pie = px.pie(
        filtered_df,
        names="sentiment_label",
        color="sentiment_label",
        color_discrete_map={"Positive": "#2ECC71", "Negative": "#E74C3C", "Neutral": "#95A5A6"}
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.subheader("Misinformation Risk vs Engagement")
    fig_scatter = px.scatter(
        filtered_df,
        x="created_at",
        y="misinfo_probability",
        size="engagement_score",
        color="high_risk",
        color_discrete_map={True: "#E74C3C", False: "#3498DB"},
        hover_data=["title", "topic"],
        labels={"created_at": "Time", "misinfo_probability": "Misinfo Probability"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# Alerts Queue
st.subheader("Priority Alert Queue (Flagged Narratives)")
alerts = filtered_df[filtered_df["high_risk"]][["title", "topic", "sentiment_label", "misinfo_probability", "engagement_score"]]
if not alerts.empty:
    st.dataframe(alerts, use_container_width=True)
else:
    st.info("No high-risk narratives match current thresholds.")
