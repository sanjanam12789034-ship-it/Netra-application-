import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page layout & styling
st.set_page_config(page_title="Netra | Analytics & News Verification", layout="wide", page_icon="📰")

st.title("🌐 Netra: Social Media Analytics & News Verification Platform")
st.caption("Integrated intelligence system: Social stream monitoring, sentiment analytics, and newspaper cross-verification")

# Unified Navigation
tab_dash, tab_checker, tab_alerts, tab_sources = st.tabs([
    "📊 Analytics Dashboard",
    "🔍 Newspaper Fake News Checker",
    "🚨 Flagged Alert Queue",
    "ℹ️ Verified Press Archives"
])

# ----------------- REPOSITORY OF TRUSTED NEWSPAPER REPORTS -----------------
NEWSPAPER_ARCHIVES = [
    {
        "headline": "RBI keeps repo rate unchanged at 6.5 percent amid inflation control",
        "newspaper": "The Hindu / Business Standard",
        "date": "September 2026",
        "category": "Economy",
        "status": "Verified True"
    },
    {
        "headline": "Government approves expansion of regional metro and rapid transit lines",
        "newspaper": "Times of India",
        "date": "September 2026",
        "category": "Infrastructure",
        "status": "Verified True"
    },
    {
        "headline": "ISRO and global space partners release panoramic satellite telemetry data",
        "newspaper": "Indian Express",
        "date": "September 2026",
        "category": "Science & Tech",
        "status": "Verified True"
    },
    {
        "headline": "Health Ministry issues seasonal guidelines for dengue and viral fever management",
        "newspaper": "Hindustan Times",
        "date": "September 2026",
        "category": "Healthcare",
        "status": "Verified True"
    }
]

# ----------------- BASELINE SOCIAL MEDIA STREAM DATA -----------------
base_time = datetime.now()
stream_data = [
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

df = pd.DataFrame(stream_data)

# ==================== TAB 1: ANALYTICS DASHBOARD ====================
with tab_dash:
    st.subheader("Social Stream Monitoring & Sentiment Overview")
    
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        selected_topic = st.selectbox("Filter Monitored Topic", ["All Topics", "Environment", "Economy", "Health", "Technology", "Science"])
    with col_filter2:
        score_threshold = st.slider("Minimum Engagement Filter", 0, 500, 50)
    
    # Filter calculation
    if selected_topic != "All Topics":
        filtered_df = df[df["topic"] == selected_topic].copy()
    else:
        filtered_df = df.copy()
        
    filtered_df = filtered_df[filtered_df["engagement_score"] >= score_threshold]
    filtered_df["high_risk"] = (filtered_df["misinfo_probability"] >= 0.70) & (filtered_df["sentiment_label"] == "Negative")
    
    # Top KPI Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Analyzed Posts", len(filtered_df))
    m2.metric("Flagged High-Risk", int(filtered_df["high_risk"].sum()) if not filtered_df.empty else 0)
    m3.metric("Negative Sentiment Rate", f"{(filtered_df['sentiment_label'] == 'Negative').mean():.0%}" if not filtered_df.empty else "0%")
    m4.metric("Avg Misinfo Score", f"{filtered_df['misinfo_probability'].mean():.2f}" if not filtered_df.empty else "0.00")
    
    st.divider()
    
    # Charts
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Sentiment Distribution")
        if not filtered_df.empty:
            st.bar_chart(filtered_df["sentiment_label"].value_counts())
        else:
            st.info("No data matching current filters.")
            
    with c2:
        st.subheader("Misinformation Risk by Post")
        if not filtered_df.empty:
            st.bar_chart(filtered_df.set_index("title")["misinfo_probability"])
        else:
            st.info("No data matching current filters.")

# ==================== TAB 2: NEWSPAPER FAKE NEWS CHECKER ====================
with tab_checker:
    st.subheader("Cross-Reference Claims Against Mainstream Press")
    st.write("Input a news headline, circulating claim, or viral post to benchmark against verified reporting:")
    
    claim_text = st.text_area("Headline or Claim to Check", placeholder="e.g., Secret miracle medicine cures disease in 24 hours, doctors silent...")
    source_choice = st.selectbox("Benchmark Source", ["All Verified Press", "The Hindu", "Times of India", "Indian Express", "Reuters"])
    
    if st.button("Run Newspaper Cross-Check"):
        if claim_text.strip():
            claim_lower = claim_text.lower()
            sensational_phrases = ["miracle", "shocking", "exposed", "secret", "wake up", "urgent warning", "banned by doctors", "hidden truth"]
            hits = [word for word in sensational_phrases if word in claim_lower]
            
            # Check overlap against newspaper archive headlines
            matched_news = []
            for item in NEWSPAPER_ARCHIVES:
                common_words = set(claim_lower.split()) & set(item["headline"].lower().split())
                meaningful = [w for w in common_words if len(w) > 3]
                if len(meaningful) >= 2:
                    matched_news.append((item, len(meaningful)))
            
            st.divider()
            
            if hits and not matched_news:
                st.error("🚨 Verdict: HIGH PROBABILITY OF FAKE / SENSATIONALIZED NEWS")
                r1, r2 = st.columns(2)
                with r1:
                    st.metric("Credibility Score", "14%", "-86% Risk")
                    st.write(f"**Detected Sensationalist Terms:** {', '.join(hits)}")
                with r2:
                    st.warning("⚠️ **Press Check:** No corroborating coverage found in verified newspaper databases.")
            elif matched_news:
                st.success("✅ Verdict: CONFIRMED / REPORTED BY MAINSTREAM PRESS")
                best = sorted(matched_news, key=lambda x: x[1], reverse=True)[0][0]
                r1, r2 = st.columns(2)
                with r1:
                    st.metric("Credibility Score", "95%", "+Verified")
                    st.write(f"**Newspaper Source:** {best['newspaper']}")
                with r2:
                    st.write(f"**Matched Press Headline:** {best['headline']}")
                    st.caption(f"Archived Release Date: {best['date']}")
            else:
                st.warning("⚠️ Verdict: UNVERIFIED / INSUFFICIENT ARCHIVE DATA")
                st.metric("Credibility Score", "48%", "Needs Manual Fact-Checking")
                st.write("This claim has no sensationalist triggers, but lacks confirmation in our archived news records.")
        else:
            st.warning("Please enter a headline or claim before checking.")

# ==================== TAB 3: ALERT QUEUE ====================
with tab_alerts:
    st.subheader("Priority Alert Queue (Flagged Narratives)")
    st.write("Real-time feed of posts exceeding misinformation and negative sentiment thresholds:")
    alerts = df[df["misinfo_probability"] >= 0.70][["title", "topic", "sentiment_label", "misinfo_probability", "engagement_score", "time_offset"]]
    st.dataframe(alerts, use_container_width=True)

# ==================== TAB 4: VERIFIED SOURCES ====================
with tab_sources:
    st.subheader("Verified Newspaper Archives Database")
    st.write("These verified news reports serve as the benchmark for cross-referencing incoming claims:")
    st.dataframe(pd.DataFrame(NEWSPAPER_ARCHIVES), use_container_width=True)
