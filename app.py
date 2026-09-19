import streamlit as st
import pandas as pd

# Configure the web application layout
st.set_page_config(page_title="Netra Analytics Portal", layout="wide", page_icon="🌐")

# Top Navigation Bar
st.title("🌐 Netra: Social Media Analytics & Misinformation Portal")
tabs = st.tabs(["📊 Analytics Dashboard", "🔍 Live Text Analyzer", "ℹ️ About Platform"])

# TAB 1: Real-time Analytics Dashboard
with tabs[0]:
    st.subheader("Platform Metrics & Narrative Monitoring")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Analyzed Posts", "1,240", "+12% today")
    col2.metric("Flagged High-Risk", "18", "-3% vs yesterday")
    col3.metric("System Health", "Operational (99.9%)")
    
    st.divider()
    
    st.write("### Trending Misinformation Risk Index")
    sample_trends = pd.DataFrame({
        "Topic": ["Public Health", "Elections", "Cybersecurity", "Finance", "Weather"],
        "Risk Score (%)": [88, 74, 45, 62, 30]
    })
    st.bar_chart(sample_trends.set_index("Topic"))
    
    st.write("### Flagged Feed")
    st.dataframe(sample_trends, use_container_width=True)

# TAB 2: Interactive Prediction Tool (User Input Form)
with tabs[1]:
    st.subheader("Test Post or Article for Misinformation")
    st.write("Enter text below to simulate NLP sentiment and misinformation classification:")
    
    user_input = st.text_area("Post Content / Article Headline", placeholder="Type or paste social media text here...")
    
    if st.button("Analyze Content"):
        if user_input.strip():
            st.success("Analysis Complete!")
            # Sample rule-based demonstration
            has_urgent = any(w in user_input.lower() for w in ["shocking", "urgent", "secret", "wake up", "exposed"])
            if has_urgent:
                st.error("⚠️ Prediction: High Probability of Misinformation / Clickbait (Score: 89%)")
                st.warning("Sentiment: Highly Negative / Alarmist")
            else:
                st.info("✅ Prediction: Verified Baseline / Low Risk (Score: 12%)")
                st.write("Sentiment: Neutral or Positive")
        else:
            st.warning("Please type some text before analyzing.")

# TAB 3: About / Project Overview
with tabs[2]:
    st.subheader("About the Netra Project")
    st.write("""
    **Netra** is an automated intelligence pipeline engineered for:
    * Ingestion of public social streams (Reddit, Twitter/X, News Feeds).
    * Natural Language Processing (NLP) sentiment scoring.
    * Predictive risk modeling for early detection of coordinated misinformation.
    """)
    st.info("Architecture: Built with Python, Scikit-Learn, Streamlit Cloud, and Pandas.")
